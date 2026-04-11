#!/usr/bin/env python3
"""
Search API for tagged real estate images
Allows filtering listings by: standing, decoration, room type, condition, amenities
"""

import os
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

def get_db():
    """Get database connection"""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=RealDictCursor
    )
    return conn

@app.route("/health", methods=["GET"])
def health():
    """Health check"""
    return jsonify({"status": "ok"})

@app.route("/search/listings", methods=["GET"])
def search_listings():
    """
    Search listings by image tags
    
    Query parameters:
    - standing: luxury, premium, standard, budget, affordable
    - decoration: modern, minimalist, classic, etc.
    - room_type: bedroom, kitchen, bathroom, living_room, etc.
    - condition: excellent, good, fair, needs_work
    - amenity: pool, garden, etc. (can be repeated)
    - min_confidence: 0.0-1.0
    - limit: 1-100 (default: 20)
    - offset: 0+ (default: 0)
    """
    try:
        standing = request.args.get("standing")
        decoration = request.args.get("decoration")
        room_type = request.args.get("room_type")
        condition = request.args.get("condition")
        amenities = request.args.getlist("amenity")
        min_confidence = float(request.args.get("min_confidence", "0.5"))
        limit = int(request.args.get("limit", "20"))
        offset = int(request.args.get("offset", "0"))
        
        # Validate
        limit = min(max(limit, 1), 100)
        offset = max(offset, 0)
        
        # Build query
        conn = get_db()
        cursor = conn.cursor()
        
        where_clauses = ["confidence >= %s"]
        params = [min_confidence]
        
        if standing:
            where_clauses.append("standing = %s")
            params.append(standing)
        
        if decoration:
            where_clauses.append("decoration_style = %s")
            params.append(decoration)
        
        if room_type:
            where_clauses.append("room_type = %s")
            params.append(room_type)
        
        if condition:
            where_clauses.append("condition = %s")
            params.append(condition)
        
        if amenities:
            placeholders = ",".join(["%s"] * len(amenities))
            where_clauses.append(f"amenities && ARRAY[{placeholders}]::TEXT[]")
            params.extend(amenities)
        
        where_sql = " AND ".join(where_clauses)
        
        # Get total count
        cursor.execute(f"""
            SELECT COUNT(*) as total
            FROM unit_image_tags
            WHERE {where_sql}
        """, params)
        
        total = cursor.fetchone()["total"]
        
        # Get results
        cursor.execute(f"""
            SELECT 
                t.id,
                t.unit_id,
                t.image_url,
                t.standing,
                t.decoration_style,
                t.room_type,
                t.colors,
                t.condition,
                t.amenities,
                t.confidence,
                t.tagged_at,
                u.primary_image_url as unit_primary_image,
                u.source_url,
                u.created_at as unit_created_at
            FROM unit_image_tags t
            LEFT JOIN units u ON t.unit_id = u.id
            WHERE {where_sql}
            ORDER BY t.confidence DESC, t.tagged_at DESC
            LIMIT %s OFFSET %s
        """, params + [limit, offset])
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({
            "status": "ok",
            "total": total,
            "limit": limit,
            "offset": offset,
            "count": len(results),
            "results": results
        })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/search/filters", methods=["GET"])
def search_filters():
    """Get available filter options (distinct values)"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get distinct values
        cursor.execute("""
            SELECT
                ARRAY_AGG(DISTINCT standing ORDER BY standing) as standings,
                ARRAY_AGG(DISTINCT decoration_style ORDER BY decoration_style) as decorations,
                ARRAY_AGG(DISTINCT room_type ORDER BY room_type) as room_types,
                ARRAY_AGG(DISTINCT condition ORDER BY condition) as conditions
            FROM unit_image_tags
            WHERE confidence >= 0.5
        """)
        
        row = cursor.fetchone()
        
        # Get amenities (flatten from array)
        cursor.execute("""
            SELECT ARRAY_AGG(DISTINCT amenity ORDER BY amenity) as amenities
            FROM (
                SELECT UNNEST(amenities) as amenity
                FROM unit_image_tags
                WHERE confidence >= 0.5
                AND amenities IS NOT NULL
            ) t
        """)
        
        amenities_row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "status": "ok",
            "standings": row["standings"] or [],
            "decorations": row["decorations"] or [],
            "room_types": row["room_types"] or [],
            "conditions": row["conditions"] or [],
            "amenities": amenities_row["amenities"] or []
        })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/stats", methods=["GET"])
def stats():
    """Get tagging statistics"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT
                COUNT(*) as total_tags,
                COUNT(DISTINCT unit_id) as units_tagged,
                AVG(confidence) as avg_confidence,
                MIN(tagged_at) as first_tag,
                MAX(tagged_at) as last_tag
            FROM unit_image_tags
        """)
        
        stats = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "status": "ok",
            "stats": stats
        })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
