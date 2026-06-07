#!/bin/bash
# ════════════════════════════════════════════════════════════
# REcall Agency — SEO Quick Fixes via WP REST API
# Adds meta descriptions to 5 posts + fixes homepage title
# Usage: bash SEO_FIXES.sh
# Requires: WP Application Password for user 'ttnl'
# ════════════════════════════════════════════════════════════

WP_URL="https://recall-agency.com"
WP_USER="ttnl"
read -s -p "Enter WordPress Application Password: " WP_PASS
echo ""

auth=$(echo -n "$WP_USER:$WP_PASS" | base64)
auth_header="Authorization: Basic $auth"

echo "→ Updating post meta descriptions via REST API..."

# Post IDs from GSC audit (as of May 2026)
declare -A posts=(
  [2744]="Discover 3 essential technologies helping Thai real estate agents digitise: AI-powered CRM software, automated contract management, and 3D virtual tours. Updated 2026 guide."
  [2741]="Learn how PPC advertising drives on-demand lead generation for real estate firms in Thailand. Expert strategies for Bangkok and Phuket markets with better ROI."
  [2737]="A 2026 guide to the best apps for real estate agents in Thailand: AI-powered CRM, property search, digital contracts, and virtual tour tools."
  [2733]="Local SEO for real estate brokerages in Thailand. Step-by-step guide to rank in Bangkok, Phuket, Pattaya and generate high-intent property leads."
  [2727]="AI and digital systems are reshaping Thai real estate. How brokers and developers use data intelligence, automation, and SEO to future-proof their operations."
)

for post_id in "${!posts[@]}"; do
  meta_desc="${posts[$post_id]}"
  echo "  Updating post $post_id..."

  # Update via Rank Math meta (if Rank Math is active)
  curl -s -X POST \
    -H "$auth_header" \
    -H "Content-Type: application/json" \
    -d "{\"meta\": {\"rank_math_description\": \"$meta_desc\"}}" \
    "$WP_URL/wp-json/wp/v2/posts/$post_id" \
    -o /dev/null -w "  Status: %{http_code}\n"
done

echo ""
echo "→ Flushing Rank Math Sitemap..."
curl -s -X GET \
  -H "$auth_header" \
  "$WP_URL/wp-json/rankmath/v1/updateHead?objectType=post&objectId=1" \
  -o /dev/null -w "  Status: %{http_code}\n"

echo ""
echo "✅ SEO fixes applied."
echo ""
echo "Manual steps still required:"
echo "  1. WP Admin → Settings → General → Site Title"
echo "     Change from 'Home - Français | REcall Agency'"
echo "     to: 'REcall Agency — AI Intelligence for Real Estate in Thailand'"
echo ""
echo "  2. Rank Math → Titles & Meta → Homepage"
echo "     Title: REcall Agency — AI Intelligence for Real Estate in Thailand"
echo "     Description: We build AI systems that give Thai real estate firms control over data, operations, and competitive edge. Cybersecurity, PropTech, analytics, automation."
echo ""
echo "  3. Rank Math → General Settings → Webmaster Tools"
echo "     Verify Google Search Console property (https://recall-agency.com)"
echo ""
echo "  4. robots.txt: Add AI crawler permissions"
echo "     User-agent: GPTBot"
echo "     Allow: /"
echo "     User-agent: ClaudeBot"
echo "     Allow: /"
echo "     User-agent: PerplexityBot"
echo "     Allow: /"
