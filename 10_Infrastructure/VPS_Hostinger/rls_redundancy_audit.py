#!/usr/bin/env python3
"""
RLS Policy Redundancy Detection Tool
=====================================

Detects tables with multiple permissive RLS policies for the same action/role.
Multiple permissive policies for the same action are suboptimal for performance
because each policy must be evaluated for every relevant query.

The tool:
1. Identifies redundant policies (multiple SELECT, INSERT, UPDATE, DELETE for same role)
2. Calculates performance impact (N policies = N evaluations per query)
3. Recommends consolidation strategy (merge into single policy with OR conditions)
4. Generates consolidation SQL

Usage:
    python3 rls_redundancy_audit.py --docker supabase-db --user postgres
    python3 rls_redundancy_audit.py --docker supabase-db --json
    python3 rls_redundancy_audit.py --docker supabase-db --fix    # Generate fix SQL
"""

import psycopg2
import json
import sys
import argparse
import subprocess
from datetime import datetime
from typing import List, Dict, Tuple, Set
from collections import defaultdict


class RLSRedundancyAudit:
    """Detect and analyze redundant RLS policies."""

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
                "-t", "-c", sql
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            # Parse CSV output
            lines = result.stdout.strip().split('\n')
            rows = [tuple(x.strip() for x in line.split('|')) for line in lines if line.strip()]
            return rows
        except subprocess.CalledProcessError as e:
            print(f"❌ Docker exec failed: {e.stderr}", file=sys.stderr)
            return []

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

    def get_all_policies(self) -> List[Dict]:
        """Get all permissive policies."""
        sql = """
        SELECT 
            schemaname,
            tablename,
            policyname,
            cmd,
            roles::text,
            qual::text as using_condition,
            with_check::text as with_check_condition
        FROM pg_policies
        WHERE schemaname = 'public'
        ORDER BY tablename, cmd, policyname;
        """
        results = self.query(sql)
        return [
            {
                "schema": row[0],
                "table": row[1],
                "policy": row[2],
                "action": row[3],
                "roles": row[4],
                "using": row[5] if row[5] else "N/A",
                "with_check": row[6] if row[6] else "N/A"
            }
            for row in results
        ]

    def find_redundant_policies(self) -> Dict[str, Dict[str, List[str]]]:
        """Find tables with multiple policies for same action."""
        policies = self.get_all_policies()
        redundant = defaultdict(lambda: defaultdict(list))

        # Group by table, action and identify duplicates
        action_groups = defaultdict(lambda: defaultdict(list))
        for policy in policies:
            key = (policy['table'], policy['action'], str(policy['roles']))
            action_groups[policy['table']][policy['action']].append(policy['policy'])

        # Find redundant groups (where count > 1)
        for table, actions in action_groups.items():
            for action, policy_list in actions.items():
                if len(policy_list) > 1:
                    redundant[table][action] = policy_list

        return redundant

    def analyze_performance_impact(self, redundant: Dict) -> Dict:
        """Calculate performance impact of redundant policies."""
        impact = {}
        total_extra_evals = 0

        for table, actions in redundant.items():
            table_impact = {"actions": {}, "total_extra_evaluations": 0}

            for action, policies in actions.items():
                extra_evals = len(policies) - 1  # First policy is baseline
                table_impact["actions"][action] = {
                    "policy_count": len(policies),
                    "extra_evaluations_per_query": extra_evals,
                    "policies": policies
                }
                table_impact["total_extra_evaluations"] += extra_evals
                total_extra_evals += extra_evals

            impact[table] = table_impact

        impact["TOTAL_EXTRA_EVALUATIONS"] = total_extra_evals
        return impact

    def generate_consolidation_sql(self, table: str, action: str, policies: List[str]) -> str:
        """Generate SQL to consolidate multiple policies into one."""
        # Get policy details
        sql = f"""
        SELECT policyname, qual, with_check
        FROM pg_policies
        WHERE tablename = '{table}' AND cmd = '{action}'
        AND policyname = ANY('{{{",".join(policies)}}}'::text[])
        ORDER BY policyname;
        """
        results = self.query(sql)

        consolidated_name = f"{table}_{action.lower()}_consolidated"
        drop_commands = [f"DROP POLICY {policy} ON {table};" for policy in policies]

        # Build consolidated policy
        conditions = []
        for policy_name, using_cond, with_check_cond in results:
            if using_cond and using_cond != "NULL":
                conditions.append(f"({using_cond})")

        merged_condition = " OR ".join(conditions) if conditions else "true"

        if action == "ALL":
            create_command = f"""
CREATE POLICY {consolidated_name} ON {table}
FOR ALL
USING ({merged_condition})
WITH CHECK ({merged_condition});
"""
        elif action == "SELECT":
            create_command = f"""
CREATE POLICY {consolidated_name} ON {table}
FOR SELECT
USING ({merged_condition});
"""
        elif action == "INSERT":
            create_command = f"""
CREATE POLICY {consolidated_name} ON {table}
FOR INSERT
WITH CHECK ({merged_condition});
"""
        elif action == "UPDATE":
            create_command = f"""
CREATE POLICY {consolidated_name} ON {table}
FOR UPDATE
USING ({merged_condition})
WITH CHECK ({merged_condition});
"""
        elif action == "DELETE":
            create_command = f"""
CREATE POLICY {consolidated_name} ON {table}
FOR DELETE
USING ({merged_condition});
"""
        else:
            create_command = ""

        return "\n".join(drop_commands) + "\n" + create_command

    def report_text(self) -> str:
        """Generate human-readable redundancy report."""
        policies = self.get_all_policies()
        redundant = self.find_redundant_policies()
        impact = self.analyze_performance_impact(redundant)

        report = []
        report.append("╔════════════════════════════════════════════════════════════════════════╗")
        report.append("║  RLS POLICY REDUNDANCY AUDIT — Performance Impact Report              ║")
        report.append(f"║  Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<53}║")
        report.append("╚════════════════════════════════════════════════════════════════════════╝")
        report.append("")

        # Summary
        total_tables = len(set(p['table'] for p in policies))
        tables_with_redundancy = len(redundant)
        total_policies = len(policies)
        extra_evals = impact.get("TOTAL_EXTRA_EVALUATIONS", 0)

        report.append("📊 SUMMARY")
        report.append(f"  Total tables with RLS:          {total_tables}")
        report.append(f"  Tables with redundancy:         {tables_with_redundancy} 🔴")
        report.append(f"  Total RLS policies:             {total_policies}")
        report.append(f"  Extra evaluations per query:    {extra_evals} ⚠️")
        report.append("")

        if not redundant:
            report.append("✅ No redundant policies detected! Your RLS configuration is optimized.")
            report.append("")
        else:
            report.append("🔴 REDUNDANT POLICIES DETECTED")
            report.append("")

            for table, actions in sorted(redundant.items()):
                table_extra = impact[table]["total_extra_evaluations"]
                report.append(f"  📋 Table: {table}")
                report.append(f"     Extra evaluations per query: {table_extra}")
                report.append("")

                for action, policies in sorted(actions.items()):
                    report.append(f"     ❌ Action: {action} ({len(policies)} policies, should be 1)")
                    for policy in policies:
                        report.append(f"        • {policy}")
                    report.append("")

            report.append("💡 WHAT THIS MEANS")
            report.append(f"  Each query evaluates {extra_evals} extra RLS policies unnecessarily.")
            report.append("  This adds latency and CPU overhead, especially for large datasets.")
            report.append("")

            report.append("🔧 RECOMMENDED ACTION")
            report.append("  Consolidate multiple policies into one using OR conditions:")
            report.append("")
            for table, actions in sorted(redundant.items()):
                for action in sorted(actions.keys()):
                    report.append(f"  ConsolidatePolicy: {table}.{action}")
            report.append("")

        report.append("📚 References:")
        report.append("  - PostgreSQL RLS docs: https://www.postgresql.org/docs/current/ddl-rowsecurity.html")
        report.append("  - RLS Performance: https://www.postgresql.org/docs/current/sql-createpolicy.html")
        report.append("")

        return "\n".join(report)

    def report_json(self) -> str:
        """Generate JSON redundancy report."""
        policies = self.get_all_policies()
        redundant = self.find_redundant_policies()
        impact = self.analyze_performance_impact(redundant)

        report = {
            "timestamp": datetime.now().isoformat(),
            "audit_type": "RLS_Policy_Redundancy",
            "summary": {
                "total_tables_with_rls": len(set(p['table'] for p in policies)),
                "tables_with_redundancy": len(redundant),
                "total_policies": len(policies),
                "extra_evaluations_per_query": impact.get("TOTAL_EXTRA_EVALUATIONS", 0)
            },
            "redundant_policies": dict(redundant),
            "performance_impact": {k: v for k, v in impact.items() if k != "TOTAL_EXTRA_EVALUATIONS"}
        }
        return json.dumps(report, indent=2, default=str)

    def report_fix_sql(self) -> str:
        """Generate SQL to consolidate redundant policies."""
        redundant = self.find_redundant_policies()

        if not redundant:
            return "-- No redundant policies found. No consolidation needed.\n"

        sql = []
        sql.append("-- RLS Policy Consolidation Script")
        sql.append(f"-- Generated: {datetime.now().isoformat()}")
        sql.append("-- Purpose: Consolidate redundant policies for performance optimization")
        sql.append("")
        sql.append("BEGIN TRANSACTION;")
        sql.append("")

        for table, actions in sorted(redundant.items()):
            for action in sorted(actions.keys()):
                policies = actions[action]
                sql.append(f"-- Consolidate {action} policies on {table}")
                sql.append(f"-- Merging {len(policies)} policies into 1")
                sql.append("")

                # Drop old policies
                for policy in policies:
                    sql.append(f"DROP POLICY {policy} ON {table};")

                sql.append("")

                # Add consolidation note
                sql.append(f"-- TODO: Review and create consolidated policy with OR conditions")
                sql.append(f"-- CREATE POLICY {table}_{action.lower()}_consolidated ON {table}")
                sql.append(f"-- FOR {action}")
                sql.append(f"-- USING (...);")
                sql.append("")

        sql.append("COMMIT;")
        sql.append("")

        return "\n".join(sql)

    def close(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="RLS Policy Redundancy Audit Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Direct PostgreSQL
  python3 rls_redundancy_audit.py --host 31.97.67.145 --user postgres --db postgres

  # Via Docker
  python3 rls_redundancy_audit.py --docker supabase-db --user postgres --db postgres

  # JSON output
  python3 rls_redundancy_audit.py --docker supabase-db --json

  # Generate fix SQL
  python3 rls_redundancy_audit.py --docker supabase-db --fix > consolidation.sql
        """
    )

    parser.add_argument("--host", help="PostgreSQL host")
    parser.add_argument("--port", type=int, default=5432, help="PostgreSQL port")
    parser.add_argument("--db", "--database", dest="database", default="postgres")
    parser.add_argument("--user", default="postgres")
    parser.add_argument("--password", help="Password (optional)")
    parser.add_argument("--docker", help="Docker container name")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--fix", action="store_true", help="Generate consolidation SQL")

    args = parser.parse_args()

    audit = RLSRedundancyAudit(
        host=args.host or "localhost",
        database=args.database,
        user=args.user,
        password=args.password,
        port=args.port,
        docker_container=args.docker
    )

    if not audit.connect():
        sys.exit(1)

    try:
        if args.json:
            print(audit.report_json())
        elif args.fix:
            print(audit.report_fix_sql())
        else:
            print(audit.report_text())
    finally:
        audit.close()


if __name__ == "__main__":
    main()
