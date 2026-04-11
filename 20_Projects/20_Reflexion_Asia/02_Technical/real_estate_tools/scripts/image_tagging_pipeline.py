#!/usr/bin/env python3
"""
Image Tagging Pipeline for Real Estate Listings
Analyzes images with Claude Vision to extract: standing, decoration, room_type, condition, amenities
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Optional
import anthropic
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

# Database connection
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Claude API
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_db_connection():
    """Connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        sys.exit(1)

def create_tags_table(conn):
    """Create unit_image_tags table if not exists"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS unit_image_tags (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            unit_id UUID REFERENCES units(id) ON DELETE CASCADE,
            image_url TEXT NOT NULL,
            standing VARCHAR(50),
            decoration_style VARCHAR(100),
            room_type VARCHAR(100),
            colors TEXT[],
            condition VARCHAR(50),
            amenities TEXT[],
            confidence FLOAT,
            tagged_at TIMESTAMP DEFAULT NOW(),
            tags_json JSONB
        );
        
        CREATE INDEX IF NOT EXISTS idx_unit_tags ON unit_image_tags(unit_id);
        CREATE INDEX IF NOT EXISTS idx_standing ON unit_image_tags(standing);
        CREATE INDEX IF NOT EXISTS idx_decoration ON unit_image_tags(decoration_style);
        CREATE INDEX IF NOT EXISTS idx_room_type ON unit_image_tags(room_type);
    """)
    conn.commit()
    cursor.close()
    print("✅ Tags table ready")

def analyze_image_with_vision(image_url: str) -> Optional[dict]:
    """
    Use Claude Vision to analyze a real estate image
    Returns: {standing, decoration_style, room_type, colors, condition, amenities, confidence}
    """
    try:
        prompt = """Analyze this real estate/apartment image and extract structured data in JSON format:

{
  "standing": "luxury|premium|standard|budget|affordable",
  "decoration_style": "modern|minimalist|classic|bohemian|traditional|industrial|scandinavian|contemporary|eclectic",
  "room_type": "bedroom|kitchen|bathroom|living_room|dining_room|office|balcony|terrace|garden|pool|hallway|other",
  "colors": ["dominant_color_1", "dominant_color_2"],
  "condition": "excellent|good|fair|needs_work",
  "amenities": ["visible_feature_1", "visible_feature_2"],
  "confidence": 0.0-1.0
}

Be conservative with confidence (0.5-0.8 typically). If unsure, lower confidence.
Focus on what's VISIBLE in the image, not assumptions.
For standing: judge by materials, finishes, design quality.
For decoration: identify design aesthetic and era.
For condition: assess wear, cleanliness, maintenance level.
For amenities: list VISIBLE items (furniture, fixtures, fixtures, plants, etc.)."""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "url",
                                "url": image_url,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ],
        )
        
        # Extract JSON from response
        response_text = message.content[0].text
        
        # Try to parse JSON
        try:
            # Find JSON in response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                tags = json.loads(json_str)
                return tags
        except json.JSONDecodeError:
            print(f"⚠️ Failed to parse JSON response: {response_text[:100]}")
            return None
            
    except Exception as e:
        print(f"❌ Vision analysis error: {e}")
        return None

def insert_image_tags(conn, unit_id: str, image_url: str, tags: dict):
    """Insert analyzed tags into database"""
    if not tags:
        return False
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO unit_image_tags 
            (unit_id, image_url, standing, decoration_style, room_type, colors, condition, amenities, confidence, tags_json)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (
            unit_id,
            image_url,
            tags.get("standing"),
            tags.get("decoration_style"),
            tags.get("room_type"),
            tags.get("colors"),
            tags.get("amenities"),
            tags.get("condition"),
            tags.get("confidence"),
            json.dumps(tags)
        ))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"❌ Insert error: {e}")
        cursor.close()
        return False

def get_units_to_process(conn, limit: int = 100, offset: int = 0):
    """Fetch units with images from database"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, primary_image_url, images
        FROM units
        WHERE primary_image_url IS NOT NULL
        AND images IS NOT NULL
        LIMIT %s OFFSET %s
    """, (limit, offset))
    
    rows = cursor.fetchall()
    cursor.close()
    return rows

def process_batch(conn, limit: int = 100, offset: int = 0, dry_run: bool = False):
    """Process a batch of units and their images"""
    units = get_units_to_process(conn, limit, offset)
    
    if not units:
        print(f"✅ No more units to process (offset: {offset})")
        return 0
    
    print(f"\n📊 Processing batch: {offset} to {offset + len(units)}")
    processed = 0
    
    for unit_id, primary_image_url, images_array in units:
        # Analyze primary image first
        images_to_analyze = [primary_image_url]
        
        # Add up to 5 gallery images
        if images_array and len(images_array) > 0:
            images_to_analyze.extend(images_array[:5])
        
        for idx, image_url in enumerate(images_to_analyze):
            if not image_url:
                continue
            
            print(f"  🖼️  Unit {unit_id} - Image {idx+1}/{len(images_to_analyze)}...", end=" ", flush=True)
            
            tags = analyze_image_with_vision(image_url)
            
            if tags:
                if not dry_run:
                    if insert_image_tags(conn, unit_id, image_url, tags):
                        print(f"✅ {tags['standing']}|{tags['decoration_style']}")
                        processed += 1
                    else:
                        print("❌ DB insert failed")
                else:
                    print(f"[DRY] {tags['standing']}|{tags['decoration_style']}")
                    processed += 1
            else:
                print("❌ Analysis failed")
            
            # Rate limit: Claude API
            time.sleep(0.5)
    
    return processed

def main():
    """Main pipeline"""
    conn = get_db_connection()
    create_tags_table(conn)
    
    print("\n🎯 Real Estate Image Tagging Pipeline")
    print("=" * 50)
    
    # Process in batches
    batch_size = 10
    total_processed = 0
    offset = 0
    
    try:
        while True:
            processed = process_batch(conn, limit=batch_size, offset=offset, dry_run=False)
            if processed == 0:
                break
            
            total_processed += processed
            offset += batch_size
            
            # Progress
            print(f"\n📈 Total processed: {total_processed} images")
            print(f"⏱️  Estimated time remaining: {(44988 - offset) * 0.5 / 60:.1f} minutes")
            
            # Optional: Save progress every N batches
            if offset % (batch_size * 10) == 0:
                print(f"💾 Progress saved at offset {offset}")
    
    except KeyboardInterrupt:
        print("\n⏹️  Interrupted by user")
    finally:
        conn.close()
        print(f"\n✅ Pipeline complete! Processed: {total_processed} images")

if __name__ == "__main__":
    main()
