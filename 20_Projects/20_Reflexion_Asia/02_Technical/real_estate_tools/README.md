# 🏠 Real Estate Tools Suite

Complete system for managing, viewing, and analyzing real estate property data from Supabase with 44,988 listings (899,760 photos).

> Organized project structure for: data viewing, image galleries, AI-powered tagging, and semantic search

---

## 📦 Project Structure

```
real_estate_tools/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── setup.sh                           # Setup script
│
├── scripts/
│   ├── image_tagging_pipeline.py      # Claude Vision batch analyzer
│   └── search_api.py                  # Flask REST API for tagged search
│
├── viewers/
│   ├── listings_with_photos.html      # Interactive table with photos
│   ├── image_viewer.html              # Gallery view with pagination
│   └── data_viewer.html               # Generic Supabase table browser
│
└── docs/
    ├── COMMENT_VOIR_MES_DATAS.md      # French guide: viewing data
    ├── IMAGE_VIEWER_GUIDE.md          # Gallery viewer documentation
    ├── LISTINGS_PHOTOS_SETUP.md       # Complete setup guide (tunnel, API keys)
    └── AI_IMAGE_TAGGING_GUIDE.md      # AI tagging system documentation
```

---

## 🚀 Quick Start

### 1. Setup Python Environment

```bash
cd /Users/phil/Documents/Vaults/SystemMac/real_estate_tools
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. Start SSH Tunnel

```bash
ssh -L 3000:127.0.0.1:8000 phil@31.97.67.145 "sleep 600" &
# Or for database direct access:
ssh -L 5432:127.0.0.1:5432 phil@31.97.67.145 "sleep 600" &
```

### 4. View Your Data

**Option A: Web Viewers (Easiest)**
- Open `viewers/listings_with_photos.html` in your browser
- Enter API URL: `http://localhost:3000`
- Enter your ANON_KEY
- Click "📡 Charger" to load listings

**Option B: AI Search API**
```bash
python3 scripts/search_api.py
# Browse to http://localhost:5001
```

---

## 📊 Viewers

### `listings_with_photos.html`
**Interactive table** displaying your listings with embedded photos

- ✅ Inline primary image + 5-photo gallery
- ✅ Clickable zoom modal
- ✅ Direct link to source listing
- ✅ Pagination (10-50 rows/page)
- ✅ Requires: API URL + ANON_KEY

**Usage:**
```bash
open viewers/listings_with_photos.html
# Then: enter http://localhost:3000 and your ANON_KEY
```

### `image_viewer.html`
**Gallery view** with responsive grid layout

- ✅ Thumbnail grid (20 items/page)
- ✅ Modal zoom on click
- ✅ Pagination
- ✅ Beautiful gradient design

**Usage:**
```bash
open viewers/image_viewer.html
```

### `data_viewer.html`
**Generic Supabase table browser** - view any table

- ✅ Table selector dropdown
- ✅ Dynamic column detection
- ✅ Row-by-row viewing
- ✅ No build dependencies

**Usage:**
```bash
open viewers/data_viewer.html
# Select table → Load Data
```

---

## 🤖 AI Image Tagging System

### Pipeline: `image_tagging_pipeline.py`

Analyze 44,988 images using Claude Vision to extract:
- **Standing** (luxury, premium, standard, budget, affordable)
- **Decoration** (modern, minimalist, classic, bohemian, industrial)
- **Room Type** (bedroom, kitchen, bathroom, living, etc.)
- **Condition** (excellent, good, fair, needs_work)
- **Amenities** (pool, garden, aircon, balcony)
- **Colors** (dominant color palette)

**Setup:**
```bash
# 1. Set ANTHROPIC_API_KEY in .env
export ANTHROPIC_API_KEY="sk-ant-..."

# 2. Start database tunnel
ssh -L 5432:127.0.0.1:5432 phil@31.97.67.145 "sleep 600" &

# 3. Run pipeline
python3 scripts/image_tagging_pipeline.py

# Duration: ~6-8 hours for all 44,988 images
# Cost: ~$450-900 with Claude 3.5 Vision
```

**Features:**
- ✅ Rate-limited (0.5s per image)
- ✅ Progress tracking + time estimation
- ✅ Database persistence
- ✅ Error recovery (can resume)
- ✅ Dry-run mode for testing

### Search API: `search_api.py`

REST API for searching tagged listings

**Endpoints:**

```bash
# Search by standing + decoration
curl "http://localhost:5001/search/listings?standing=luxury&decoration=modern"

# Search by room type + condition
curl "http://localhost:5001/search/listings?room_type=bedroom&condition=good"

# Multi-select amenities
curl "http://localhost:5001/search/listings?amenity=pool&amenity=garden"

# Advanced filtering
curl "http://localhost:5001/search/listings?standing=premium&min_confidence=0.8&limit=50"

# View available filters
curl "http://localhost:5001/search/filters"

# Tagging statistics
curl "http://localhost:5001/stats"
```

**Setup:**
```bash
# Start database tunnel
ssh -L 5432:127.0.0.1:5432 phil@31.97.67.145 "sleep 600" &

# Run API
python3 scripts/search_api.py
# Listening on http://localhost:5001
```

---

## 🔐 Security & Authentication

### SSH Tunnel Setup

**PostgREST API (port 3000):**
```bash
ssh -L 3000:127.0.0.1:8000 phil@31.97.67.145 "sleep 600" &
```
Maps your local port 3000 → Kong Gateway port 8000 on VPS

**PostgreSQL Direct (port 5432):**
```bash
ssh -L 5432:127.0.0.1:5432 phil@31.97.67.145 "sleep 600" &
```
Maps your local port 5432 → PostgreSQL port 5432 on VPS

### API Keys

**ANON_KEY** (for web viewers)
- Public JWT token
- Allows: SELECT on public-read tables
- Find: `grep ANON_KEY .env` on VPS

**SERVICE_ROLE_KEY** (for backend)
- Admin JWT token
- Allows: INSERT, UPDATE, DELETE
- ⚠️ Never expose in frontend

### Row-Level Security (RLS)

All 89 tables are protected:
- **Credentials tables**: Admin-only access
- **Data tables**: Public-read via API
- **Workflows**: Public-read via API

---

## 📚 Documentation

### French Guides

1. **`COMMENT_VOIR_MES_DATAS.md`** - 3 ways to access your data
2. **`IMAGE_VIEWER_GUIDE.md`** - Photo gallery documentation
3. **`LISTINGS_PHOTOS_SETUP.md`** - Complete setup (tunnel, API keys, troubleshooting)
4. **`AI_IMAGE_TAGGING_GUIDE.md`** - AI system setup & API reference

---

## 🛠️ Environment Variables

Create `.env` file in project root:

```dotenv
# Database
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password

# Supabase
SUPABASE_URL=your_supabase_url
ANON_KEY=your_anon_key

# Claude API
ANTHROPIC_API_KEY=sk-ant-...

# Flask API
FLASK_PORT=5001
FLASK_ENV=development
```

---

## 📋 Requirements

### Python Packages
- `anthropic` - Claude Vision API
- `psycopg2-binary` - PostgreSQL adapter
- `flask` - Web framework
- `flask-cors` - CORS support
- `python-dotenv` - Environment variables

### System
- Python 3.8+
- SSH access to VPS (31.97.67.145)
- ~10GB disk for analysis results

---

## 🚨 Troubleshooting

### "Connection refused" on port 3000/5432
**Solution**: Restart SSH tunnel
```bash
killall ssh
ssh -L 3000:127.0.0.1:8000 phil@31.97.67.145 "sleep 600" &
```

### "No API key found in request"
**Solution**: Verify ANON_KEY in viewer
```bash
# Get key from VPS
ssh phil@31.97.67.145 "grep ANON_KEY ./local-ai-packaged/.env"
# Copy full value (without "ANON_KEY=")
```

### Images not loading
**Solution**: Verify viewer setup
1. Check tunnel is active: `lsof -i :3000`
2. Verify API URL: `http://localhost:3000`
3. Check ANON_KEY is filled
4. Wait 5s, then refresh page

### Pipeline crashes
**Solution**: Resume from last checkpoint
```bash
python3 scripts/image_tagging_pipeline.py
# Script skips already-tagged images
```

---

## 📊 Data Statistics

| Metric | Value |
|--------|-------|
| **Listings** | 44,988 |
| **Total Photos** | 899,760 |
| **Avg Photos/Listing** | 20 |
| **Tables** | 89 (all RLS-protected) |
| **Core Data** | 51,000+ records |

---

## 🎯 Use Cases

### 1. Browse Listings
```bash
# Open a viewer
open viewers/listings_with_photos.html
# Or
open viewers/image_viewer.html
```

### 2. Search by Aesthetic
```bash
# "Show me luxury modern apartments with pools"
curl "http://localhost:5001/search/listings?standing=luxury&decoration=modern&amenity=pool"
```

### 3. Export Filtered Data
```bash
curl "http://localhost:5001/search/listings?standing=premium&limit=1000" > premium_listings.json
```

### 4. Analyze by Category
```bash
# Via search_api.py /stats endpoint
curl "http://localhost:5001/stats"
```

---

## ✅ Checklist

### Initial Setup
- [ ] Clone/download project
- [ ] Install Python dependencies: `pip install -r requirements.txt`
- [ ] Create `.env` file
- [ ] Test SSH tunnel: `ssh -L 3000:127.0.0.1:8000 phil@31.97.67.145 "sleep 600" &`

### Using Viewers
- [ ] Start SSH tunnel
- [ ] Open HTML viewer
- [ ] Enter API URL: `http://localhost:3000`
- [ ] Enter ANON_KEY
- [ ] Click "Charger"

### Using AI Pipeline
- [ ] Set ANTHROPIC_API_KEY in `.env`
- [ ] Start database tunnel (port 5432)
- [ ] Run: `python3 scripts/image_tagging_pipeline.py`
- [ ] Monitor progress (6-8 hours)
- [ ] Start API: `python3 scripts/search_api.py`

---

## 📞 Support

**SSH Issues?**
- Check auth: `ssh phil@31.97.67.145 ls`
- Verify port: `ssh -vvv -L 3000:127.0.0.1:8000 phil@31.97.67.145`

**API Issues?**
- Check tunnel: `lsof -i :3000`
- Check permissions: RLS policies `SELECT` enabled
- Check key: `curl -H "apikey: $KEY" http://localhost:3000/rest/v1/units?limit=1`

**Image Issues?**
- Check CDN: Direct URL from browser
- Wait for cache: FazWaz CDN TTL ~1 hour
- Alt images: Use fallback placeholder

---

## 🎉 Ready?

```bash
# 1. Setup
pip install -r requirements.txt

# 2. Tunnel
ssh -L 3000:127.0.0.1:8000 phil@31.97.67.145 "sleep 600" &

# 3. View
open viewers/listings_with_photos.html

# 4. Explore!
```

That's it! Start browsing your 44,988 listings with 899,760 photos. 🏠📸
