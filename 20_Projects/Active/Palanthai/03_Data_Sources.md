# 📡 KINNAREE — Data Sources & Intelligence Feeds

> Key Insights, Notifications & Automated Reporting Engine

---

## Primary Sources

### 1. LivePhuket.com (Project Data)
- **URL**: `https://www.livephuket.com/project-directory/`
- **Data**: Projects, developers, prices, amenities, geo coordinates
- **Format**: HTML + JSON-LD Schema.org
- **Extraction**: `phase1_project_extractor.py`, `phase1_developer_extractor.py`
- **Frequency**: Weekly crawl recommended
- **Volume**: ~5,000+ projects, ~1,519 developers

### 2. FazWaz.com (Knowledge Base)
- **URL**: `https://www.fazwaz.com/advice`
- **Data**: FAQ articles on Thai real estate (legal, buying process, areas)
- **Format**: HTML articles with categories
- **Extraction**: `phase1_faq_extractor.py`
- **Use**: RAG pipeline for AI property advisor (GARUDA module)

---

## Financial Sources (KINNAREE Phase 1.5)

### 3. SET Thailand — Stock Exchange
- **URL**: `https://www.set.or.th/en/market/index/set/propcon/prop`
- **Data**: Listed property developers financials
- **Key tickers**: AP, AWC, CPN, LH, ORI, PSH, QH, SIRI, SPALI
- **Metrics**: Market cap, P/E, P/BV, dividend yield, quarterly EPS
- **Format**: HTML tables + API (requires JS rendering)
- **Use**: Developer due diligence, financial health scoring
- **Entity linking**: Developer name ↔ SET ticker (NAGA module)

### 4. Bank of Thailand (BOT)
- **URL**: `https://www.bot.or.th/en/statistics.html`
- **Data**: Housing price index, loan-to-value ratios, mortgage rates
- **Sub-sources**:
  - REIC (Real Estate Information Center): `https://www.reic.or.th`
  - Housing statistics quarterly reports
  - Construction permits by province
- **Format**: Excel/CSV downloads, PDF reports
- **Use**: Macro market context, trend analysis

### 5. CBRE Thailand
- **URL**: `https://www.cbre.co.th/en/research`
- **Data**: Quarterly property market outlook reports
- **Format**: PDF reports
- **Extraction**: `tabula-py` for tables, text extraction for sentiment
- **Use**: Sentiment analysis, market trend confirmation

---

## Regulatory Sources (Phase 2)

### 6. EIA (Environmental Impact Assessment)
- **Authority**: ONEP (Office of Natural Resources and Environmental Policy)
- **URL**: `https://eia.onep.go.th/`
- **Data**: Construction permits, environmental clearances
- **Use**: Project verification, risk assessment

### 7. Land Department
- **Authority**: Department of Lands, Thailand
- **Data**: Land title records, ownership transfer statistics
- **Use**: Ownership verification, market volume analysis

### 8. BOI (Board of Investment)
- **URL**: `https://www.boi.go.th`
- **Data**: Foreign investment incentives, special economic zones
- **Use**: Investment opportunity mapping

---

## Google Drive Resources (SystemMac)

| Folder | Contents | Vault Link |
|:---|:---|:---|
| `Reflection.Asia_ AI-Powered Thai PropTech` | Core strategy docs | [[#GDrive Index]] |
| `SEO-reflexion` | SEO strategy & keyword research | |
| `colab` | Jupyter notebooks (prototype code) | |
| `proptechBOX.txt` | Text data files | |
| `n8n` | Workflow automation configs | |
| `demo-db-csv` | Sample CSV datasets | |
| `db-csv` | Production CSV exports | |
| `db-txt` | Text database dumps | |
| `AI Infrastructure SOP` | Step-by-step setup guide (14.7MB doc) | |

---

## n8n Workflow Architecture (VPS Hostinger)

### Planned Workflows

1. **Weekly Crawl Trigger**
   - Cron: Every Sunday 02:00 ICT
   - Action: Run SIAM extractors → CHANG export → KINNAREE report

2. **Price Change Detection**
   - Trigger: New crawl data arrives
   - Compare: Current vs previous prices
   - Alert: Slack/email notification for >5% changes

3. **New Project Alert**
   - Trigger: New project URLs detected
   - Action: Immediate detail crawl → notification

4. **Developer Financial Update**
   - Cron: Monthly (after SET quarterly reports)
   - Action: Crawl SET → Update developer financial scores

5. **Market Report Generator**
   - Cron: Monthly
   - Action: Aggregate data → Generate PDF report → Email
