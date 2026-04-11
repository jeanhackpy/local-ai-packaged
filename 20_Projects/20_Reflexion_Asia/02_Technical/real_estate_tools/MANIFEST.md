# 📋 Real Estate Tools - File Manifest

Complete inventory of all files in the organized project structure.

---

## 📍 Root Directory Files

### `README.md` (9.4K)
**Project overview and quick start guide**
- ✅ Complete setup instructions
- ✅ Viewer descriptions
- ✅ AI pipeline documentation
- ✅ Troubleshooting guide
- ✅ Data statistics

**When to use:** First file to read for project overview

### `requirements.txt` (93B)
**Python dependencies list**
- anthropic==0.32.0 (Claude API)
- psycopg2-binary==2.9.9 (PostgreSQL)
- flask==3.0.0 (Web framework)
- flask-cors==4.0.0 (CORS support)
- python-dotenv==1.0.0 (Environment variables)

**When to use:** `pip install -r requirements.txt`

### `setup.sh` (2.5K)
**Automated setup script**
- ✅ Python version check
- ✅ SSH availability check
- ✅ Dependency installation
- ✅ Environment file validation
- ✅ Display next steps

**When to use:** First time setup
```bash
chmod +x setup.sh
./setup.sh
```

### `.env.example` (Template)
**Environment configuration template**
- Database credentials
- Supabase keys
- Claude API key
- Flask settings
- SSH tunnel config

**When to use:** Create `.env` from this template

---

## 🐍 Scripts Directory

### `image_tagging_pipeline.py` (8.9K)
**Claude Vision batch image analyzer**

**Functionality:**
- Reads 44,988 images from units table
- Analyzes each with Claude 3.5 Vision
- Extracts: standing, decoration, room_type, condition, amenities, colors
- Stores results in unit_image_tags table
- Rate-limited (0.5s/image) for API compliance

**Key Functions:**
- `analyze_image_with_vision(url)` - Process single image
- `insert_image_tags()` - Store results in DB
- `process_batch()` - Batch process with progress tracking

**Usage:**
```bash
python3 scripts/image_tagging_pipeline.py
# Duration: 6-8 hours
# Cost: $450-900
```

**Dependencies:** anthropic, psycopg2, python-dotenv

### `search_api.py` (6.8K)
**Flask REST API for tagged image search**

**Functionality:**
- Search listings by aesthetic criteria
- Support complex filtering (multi-select)
- Return available filter options
- Display tagging statistics

**Endpoints:**
- `GET /search/listings` - Search with filters
- `GET /search/filters` - Available options
- `GET /stats` - Tagging progress

**Example Usage:**
```bash
# Start API
python3 scripts/search_api.py

# Search luxury + modern + pool
curl 'http://localhost:5001/search/listings?standing=luxury&decoration=modern&amenity=pool'
```

**Dependencies:** flask, flask-cors, psycopg2, python-dotenv

---

## 🌐 Viewers Directory

### `listings_with_photos.html` (14K)
**Interactive table with embedded photos**

**Features:**
- ✅ Responsive data table
- ✅ Primary image + 5-photo gallery
- ✅ Clickable photos with zoom modal
- ✅ Source link to original listing
- ✅ Photo counter per listing
- ✅ Pagination (10-50 rows/page)
- ✅ API key authentication

**Usage:**
1. Start tunnel: `ssh -L 3000:127.0.0.1:8000 phil@31.97.67.145 "sleep 600" &`
2. Open: `open viewers/listings_with_photos.html`
3. Enter: API URL (`http://localhost:3000`) + ANON_KEY
4. Click: "📡 Charger"

**Requires:** 
- SSH tunnel active on port 3000
- ANON_KEY from Supabase

### `image_viewer.html` (15K)
**Photo gallery with responsive grid**

**Features:**
- ✅ Masonry thumbnail grid (20-100 per page)
- ✅ Modal zoom on click
- ✅ Pagination controls
- ✅ Listing ID + photo count
- ✅ Beautiful gradient design
- ✅ Mobile responsive

**Usage:**
1. Start tunnel: `ssh -L 3000:127.0.0.1:8000 phil@31.97.67.145 "sleep 600" &`
2. Open: `open viewers/image_viewer.html`
3. Load listings

**Requires:**
- SSH tunnel active on port 3000

### `data_viewer.html` (14K)
**Generic Supabase table browser**

**Features:**
- ✅ Table selector dropdown
- ✅ Auto-detect columns
- ✅ Row pagination
- ✅ View any table
- ✅ No build dependencies
- ✅ Direct PostgREST access

**Usage:**
1. Start tunnel
2. Open: `open viewers/data_viewer.html`
3. Select table → Load Data

**Supported Tables:**
- projects (5,387 rows)
- developers (1,522 rows)
- units (44,988 rows)
- alerts
- execution_data
- districts, provinces

---

## 📚 Docs Directory

### `COMMENT_VOIR_MES_DATAS.md` (3.5K)
**French guide: Access your data (3 methods)**

**Contents:**
- 📊 Dashboard web method
- 🔌 Direct API with curl
- 🗄️ PostgreSQL direct SSH

**Sections:**
- Quick start (3 steps)
- Data availability table
- Security info
- Troubleshooting
- SQL examples

**Languages:** 🇫🇷 Français

### `IMAGE_VIEWER_GUIDE.md` (3.3K)
**Photo gallery documentation**

**Contents:**
- What it is / Where images are
- How to access (3 steps)
- Features overview
- Data structure
- API endpoint details
- Troubleshooting

**Sections:**
- Quick setup
- Interface description
- Handling 899,760 photos
- CDN variations
- Use cases

**Languages:** 🇫🇷 Français

### `LISTINGS_PHOTOS_SETUP.md` (5.2K)
**Complete setup guide (tunnel + API keys)**

**Contents:**
- 5-minute complete setup
- SSH tunnel creation
- API key retrieval (2 methods)
- HTML viewer configuration
- Interface explanation
- API key types (ANON vs SERVICE_ROLE)
- Troubleshooting (5 scenarios)
- Use cases
- Setup checklists

**Languages:** 🇫🇷 Français

### `AI_IMAGE_TAGGING_GUIDE.md` (7.6K)
**AI image analysis system documentation**

**Contents:**
- Project objective
- Files created (2 main)
- 5-step complete setup
- DB schema
- Cost & performance
- Use cases (4 examples)
- Troubleshooting
- Monitoring & stats
- Next steps

**Languages:** 🇫🇷 Français + 🇬🇧 English examples

---

## 📊 File Size Summary

| Component | Files | Size | Purpose |
|-----------|-------|------|---------|
| **Root** | 4 | 12K | Config + setup |
| **Scripts** | 2 | 15.7K | Python backends |
| **Viewers** | 3 | 43K | HTML interfaces |
| **Docs** | 4 | 19.6K | French guides |
| **TOTAL** | **13** | **116K** | Complete toolkit |

---

## 🎯 Quick File Lookup

### "I want to view my listings"
👉 `viewers/listings_with_photos.html` or `viewers/image_viewer.html`

### "How do I set this up?"
👉 `README.md` (English) or `docs/LISTINGS_PHOTOS_SETUP.md` (French)

### "I need to analyze images with AI"
👉 `scripts/image_tagging_pipeline.py` + read `docs/AI_IMAGE_TAGGING_GUIDE.md`

### "I want to search by standing/decor"
👉 `scripts/search_api.py` endpoint examples in `docs/AI_IMAGE_TAGGING_GUIDE.md`

### "What are my options to view data?"
👉 `docs/COMMENT_VOIR_MES_DATAS.md` (3 methods explained)

### "Something's broken"
👉 See "Troubleshooting" section in:
- `README.md` (general)
- `docs/LISTINGS_PHOTOS_SETUP.md` (setup issues)
- `docs/AI_IMAGE_TAGGING_GUIDE.md` (pipeline issues)

---

## 🔄 Dependency Graph

```
requirements.txt
    ├─→ anthropic (for Claude Vision)
    ├─→ psycopg2-binary (for PostgreSQL)
    ├─→ flask (for search API)
    ├─→ flask-cors
    └─→ python-dotenv

.env.example
    └─→ (copy to .env before running)

setup.sh
    └─→ Installs requirements.txt

scripts/image_tagging_pipeline.py
    ├─→ Requires: anthropic, psycopg2, python-dotenv
    ├─→ Reads: units table
    └─→ Writes: unit_image_tags table

scripts/search_api.py
    ├─→ Requires: flask, psycopg2, python-dotenv
    ├─→ Reads: unit_image_tags table
    └─→ Port: 5001

viewers/*.html
    ├─→ No dependencies! Pure HTML/CSS/JS
    ├─→ Requires: SSH tunnel on port 3000
    ├─→ Requires: ANON_KEY
    └─→ Requires: Browser (any modern browser)
```

---

## 🚀 Execution Paths

### Path 1: Quick Browse (No Python)
```
SSH Tunnel → HTML Viewer → View Listings
(5 minutes)
```

### Path 2: AI Analysis (Full System)
```
Python Setup → .env Config → Pipeline → Search API → Web Search
(Setup: 15 min, Analysis: 6-8 hrs)
```

### Path 3: Data Export
```
SSH Tunnel → Search API → curl fetch → JSON/CSV
(10 minutes)
```

---

## 📌 Important Notes

1. **All HTML viewers are standalone** - no build step needed
2. **All scripts are modular** - can run independently after setup
3. **All docs are in French** - for Francophone team
4. **SSH tunnel is required** - for both viewers and scripts
5. **Total project size: 116K** - lightweight, portable
6. **No server deployment needed** - all HTML run locally

---

## ✅ Verification Checklist

- [x] All 4 markdown docs in `docs/` directory
- [x] All 3 HTML viewers in `viewers/` directory
- [x] All 2 Python scripts in `scripts/` directory
- [x] README.md in root with complete documentation
- [x] requirements.txt with all dependencies
- [x] setup.sh executable for automated setup
- [x] .env.example template for configuration
- [x] Total: 13 files, 116K size

---

**Last Updated:** April 4, 2026
**Project Version:** v1.0 (Fully Organized)
