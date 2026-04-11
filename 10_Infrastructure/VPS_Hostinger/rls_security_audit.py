#!/usr/bin/env python3
"""
RLS Security Audit Tool for PostgREST-Exposed Tables
=====================================================

Detects PostgreSQL tables that lack Row-Level Security (RLS) protection
in schemas exposed to PostgREST API. Produces automated audit reports
and remediation recommendations.

Usage:
    python3 rls_security_audit.py --host 31.97.67.145 --db postgres --user postgres
    python3 rls_security_audit.py --docker supabase-db  # Via docker exec
    python3 rls_security_audit.py --json              # JSON output for CI/CD
"""

import psycopg2
import json
import sys
import argparse
from datetime import datetime
from typing import List, Dict, Tuple
import subprocess
from collections import defaultdict


class RLSAuditTool:
    """SQL-based RLS security audit for PostgREST exposure."""

    def __init__(self, host: str = None, database: str = "postgres", user: str = "postgres", 
                 password: str = None, port: int = 5432, docker_container: str = None):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.docker_container = docker_container
        self.conn = None
        self.cursor = None

    def connect(self) -> bool:
        """Establish database connection."""
        try:
            if self.docker_container:
                # Use docker exec for connection
                self.docker_mode = True
                return True
            else:
                self.conn = psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    port=self.port
                )
                self.cursor = self.conn.cursor()
                self.docker_mode = False
                return True
        except Exception as e:
            print(f"❌ Connection failed: {e}", file=sys.stderr)
            return False

    def query_docker(self, sql: str) -> List[Tuple]:
        """Execute query via docker exec."""
        try:
            cmd = [
                "docker", "exec", self.docker_container, "psql",
                "-U", self.user, "-d", self.database,
                "-c", sql
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"❌ Docker exec failed: {e.stderr}", file=sys.stderr)
            return None

    def query(self, sql: str) -> List[Tuple]:
        """Execute SQL query and return results."""
        if self.docker_mode:
            return self.query_docker(sql)
        
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"❌ Query failed: {e}", file=sys.stderr)
            return []

    def get_tables_without_rls(self) -> List[Dict]:
        """Find all public schema tables without RLS enabled."""
        sql = """
        SELECT 
            schemaname,
            tablename,
            rowsecurity,
            (SELECT count(*) FROM information_schema.columns 
             WHERE table_schema = schemaname AND table_name = tablename) as column_count
        FROM pg_tables
        WHERE schemaname = 'public' 
            AND tablename NOT IN ('spatial_ref_sys', 'geometry_columns')
            AND rowsecurity = false
        ORDER BY tablename;
        """
        results = self.query(sql)
        return [
            {
                "schema": row[0],
                "table": row[1],
                "rls_enabled": row[2],
                "columns": row[3]
            }
            for row in results
        ]

    def get_tables_with_rls(self) -> List[Dict]:
        """Find all public schema tables with RLS enabled."""
        sql = """
        SELECT 
            schemaname,
            tablename,
            rowsecurity,
            COALESCE((SELECT count(*) FROM pg_policies WHERE tablename = tablename), 0) as policy_count
        FROM pg_tables
        WHERE schemaname = 'public' 
            AND tablename NOT IN ('spatial_ref_sys', 'geometry_columns')
            AND rowsecurity = true
        ORDER BY tablename;
        """
        results = self.query(sql)
        return [
            {
                "schema": row[0],
                "table": row[1],
                "rls_enabled": row[2],
                "policies": row[3]
            }
            for row in results
        ]

    def get_risk_assessment(self) -> List[Dict]:
        """Assess risk level based on RLS status and row count."""
        sql = """
        SELECT 
            schemaname,
            tablename,
            rowsecurity::text as rls_enabled,
            n_live_tup as row_count,
            pg_size_pretty(pg_total_relation_size(to_regclass(schemaname||'.'||tablename))) as size,
            CASE 
                WHEN rowsecurity = true THEN 'PROTECTED'
                WHEN rowsecurity = false AND n_live_tup > 1000 THEN 'CRITICAL'
                WHEN rowsecurity = false AND n_live_tup > 100 THEN 'HIGH'
                WHEN rowsecurity = false THEN 'MEDIUM'
                ELSE 'UNKNOWN'
            END as risk_level
        FROM pg_stat_user_tables
        WHERE schemaname = 'public'
        ORDER BY n_live_tup DESC;
        """
        results = self.query(sql)
        return [
            {
                "schema": row[0],
                "table": row[1],
                "rls_enabled": row[2] == "true",
                "rows": row[3],
                "size": row[4],
                "risk": row[5]
            }
            for row in results
        ]

    def get_statistics(self) -> Dict:
        """Get summary statistics."""
        sql = """
        SELECT 
            (SELECT count(*) FROM pg_tables WHERE schemaname = 'public' 
             AND tablename NOT IN ('spatial_ref_sys', 'geometry_columns')) as total,
            (SELECT count(*) FROM pg_tables WHERE schemaname = 'public' 
             AND rowsecurity = true AND tablename NOT IN ('spatial_ref_sys', 'geometry_columns')) as protected,
            (SELECT count(*) FROM pg_tables WHERE schemaname = 'public' 
             AND rowsecurity = false AND tablename NOT IN ('spatial_ref_sys', 'geometry_columns')) as unprotected;
        """
        results = self.query(sql)
        if results:
            total, protected, unprotected = results[0]
            coverage = round(100.0 * protected / total, 2) if total > 0 else 0
            return {
                "total_tables": total,
                "protected_tables": protected,
                "unprotected_tables": unprotected,
                "rls_coverage_percent": coverage
            }
        return {}

    def generate_remediation_sql(self, table_name: str) -> str:
        """Generate SQL to enable RLS on a table."""
        return f"ALTER TABLE public.{table_name} ENABLE ROW LEVEL SECURITY;"

    def report_text(self) -> str:
        """Generate human-readable audit report."""
        stats = self.get_statistics()
        unprotected = self.get_tables_without_rls()
        protected = self.get_tables_with_rls()
        risks = self.get_risk_assessment()

        report = []
        report.append("╔════════════════════════════════════════════════════════════════════════╗")
        report.append("║  RLS SECURITY AUDIT — PostgREST Exposure Report                      ║")
        report.append(f"║  Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<53}║")
        report.append("╚════════════════════════════════════════════════════════════════════════╝")
        report.append("")

        # Summary
        report.append("📊 SUMMARY STATISTICS")
        report.append(f"  Total Tables:       {stats.get('total_tables', 0)}")
        report.append(f"  Protected (RLS):    {stats.get('protected_tables', 0)} ✅")
        report.append(f"  Unprotected:        {stats.get('unprotected_tables', 0)} ❌")
        report.append(f"  RLS Coverage:       {stats.get('rls_coverage_percent', 0)}%")
        report.append("")

        # Critical Issues
        if unprotected:
            report.append("🔴 CRITICAL: Tables Without RLS (Exposed to PostgREST)")
            report.append("")
            for table in unprotected:
                report.append(f"  ❌ {table['table']}")
                report.append(f"     Schema: {table['schema']}")
                report.append(f"     Columns: {table['columns']}")
                report.append("")
        else:
            report.append("✅ All public tables have RLS enabled!")
            report.append("")

        # Protected Tables
        if protected:
            report.append("✅ PROTECTED: Tables with RLS Enabled")
            report.append("")
            for table in protected:
                report.append(f"  ✅ {table['table']:<30} ({table['policies']} policies)")
            report.append("")

        # Risk Assessment
        report.append("⚠️  RISK ASSESSMENT by Row Count")
        report.append("")
        risk_categories = defaultdict(list)
        for item in risks:
            risk_categories[item['risk']].append(item)

        for risk_level in ['CRITICAL', 'HIGH', 'MEDIUM', 'PROTECTED']:
            tables = risk_categories.get(risk_level, [])
            if tables:
                report.append(f"  {risk_level}: {len(tables)} table(s)")
                for table in tables:
                    emoji = "🔴" if risk_level == "CRITICAL" else "🟠" if risk_level == "HIGH" else "🟡" if risk_level == "MEDIUM" else "✅"
                    report.append(f"    {emoji} {table['table']:<30} {table['rows']:>8} rows  ({table['size']})")
        report.append("")

        # Remediation
        if unprotected:
            report.append("🔧 REMEDIATION: Enable RLS on Unprotected Tables")
            report.append("")
            for table in unprotected:
                report.append(f"  {self.generate_remediation_sql(table['table'])}")
            report.append("")

        report.append("📚 References:")
        report.append("  - PostgreSQL RLS: https://www.postgresql.org/docs/current/ddl-rowsecurity.html")
        report.append("  - PostgREST Security: https://postgrest.org/en/v12/auth.html")
        report.append("  - Supabase RLS Guide: https://supabase.com/docs/guides/auth/row-level-security")
        report.append("")

        return "\n".join(report)

    def report_json(self) -> str:
        """Generate JSON audit report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "audit_type": "RLS_Security_PostgREST",
            "statistics": self.get_statistics(),
            "unprotected_tables": self.get_tables_without_rls(),
            "protected_tables": self.get_tables_with_rls(),
            "risk_assessment": self.get_risk_assessment()
        }
        return json.dumps(report, indent=2, default=str)

    def close(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="RLS Security Audit for PostgREST-Exposed Tables",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Direct PostgreSQL connection
  python3 rls_security_audit.py --host 31.97.67.145 --db postgres --user postgres

  # Via Docker container
  python3 rls_security_audit.py --docker supabase-db --user postgres --db postgres

  # JSON output for CI/CD
  python3 rls_security_audit.py --docker supabase-db --json

  # Save report to file
  python3 rls_security_audit.py --docker supabase-db > rls_audit_report.txt
        """
    )

    parser.add_argument("--host", help="PostgreSQL host (default: localhost)")
    parser.add_argument("--port", type=int, default=5432, help="PostgreSQL port (default: 5432)")
    parser.add_argument("--db", "--database", dest="database", default="postgres", help="Database name")
    parser.add_argument("--user", default="postgres", help="PostgreSQL user")
    parser.add_argument("--password", help="Password (optional)")
    parser.add_argument("--docker", help="Docker container name (alternative to host/port)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # Initialize audit tool
    audit = RLSAuditTool(
        host=args.host or "localhost",
        database=args.database,
        user=args.user,
        password=args.password,
        port=args.port,
        docker_container=args.docker
    )

    # Connect and run audit
    if not audit.connect():
        sys.exit(1)

    try:
        if args.json:
            print(audit.report_json())
        else:
            print(audit.report_text())
    finally:
        audit.close()


if __name__ == "__main__":
    main()
