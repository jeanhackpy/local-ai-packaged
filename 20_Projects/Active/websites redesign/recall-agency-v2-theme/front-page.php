<?php
/**
 * Front Page Template — REcall Agency v3
 * Positioning: Intelligence Layer for Real Estate (Titleman-style structure)
 * Business Plan 2026
 *
 * @package Recall_Agency
 */
get_header(); ?>

<!-- NAVIGATION (Floating Island) -->
<div class="rc-nav" role="navigation" aria-label="Main navigation">
  <a href="<?php echo esc_url( home_url('/') ); ?>" class="rc-nav__logo">
    RE<span>call</span>
  </a>
  <ul class="rc-nav__links" role="list">
    <li><a href="#solutions">Solutions</a></li>
    <li><a href="#services">Services</a></li>
    <li><a href="<?php echo esc_url( get_permalink( get_page_by_path('blog') ) ); ?>">Insights</a></li>
    <li><a href="<?php echo esc_url( get_permalink( get_page_by_path('about') ) ); ?>">About</a></li>
  </ul>
  <div class="rc-nav__actions">
    <a href="<?php echo esc_url( get_permalink( get_page_by_path('contact') ) ); ?>" class="rc-btn rc-btn--ghost">Contact</a>
    <a href="<?php echo esc_url( get_permalink( get_page_by_path('contact') ) ); ?>" class="rc-btn rc-btn--primary">Book a strategy call →</a>
  </div>
</div>

<main id="main" class="site-main">

<!-- HERO -->
<section class="rc-hero" aria-label="Hero">
  <div class="rc-hero__inner">
    <div class="rc-hero__badge rc-reveal">
      <span class="rc-hero__badge-dot"></span>
      Available for strategic mandates · Thailand &amp; SEA
    </div>
    <h1 class="rc-display rc-hero__h1 rc-reveal">
      The <em>Intelligence Layer</em> for Real Estate
    </h1>
    <p class="rc-hero__sub rc-reveal">
      We build AI-powered systems that give real estate firms in Thailand and Southeast Asia
      structural control over their data, operations, and competitive edge.
    </p>
    <div class="rc-hero__actions rc-reveal">
      <a href="<?php echo esc_url( get_permalink( get_page_by_path('contact') ) ); ?>" class="rc-btn rc-btn--primary">
        Book a strategy call
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </a>
      <a href="#services" class="rc-btn rc-btn--ghost">Explore services</a>
    </div>
    <p style="font-size:0.8rem; color:var(--text-3); margin-top:0; line-height:1.5;">
      Trusted by real estate operators, developers &amp; investors across Bangkok, Phuket &amp; Chiang Mai
    </p>
  </div>
</section>

<!-- TRUST BAR / MARQUEE -->
<div class="rc-trust">
  <p class="rc-trust__label">Trusted by leading real estate firms in Thailand &amp; SEA</p>
  <div class="rc-marquee-wrap">
    <div class="rc-marquee" aria-hidden="true">
      <span class="rc-marquee__item">Sansiri</span>
      <span class="rc-marquee__item">Ananda Development</span>
      <span class="rc-marquee__item">AP Thailand</span>
      <span class="rc-marquee__item">Origin Property</span>
      <span class="rc-marquee__item">Pruksa Holdings</span>
      <span class="rc-marquee__item">MQDC</span>
      <span class="rc-marquee__item">Central Pattana</span>
      <span class="rc-marquee__item">SC Asset</span>
      <span class="rc-marquee__item">Supalai PCL</span>
      <span class="rc-marquee__item">Golden Land</span>
      <!-- Duplicate for loop -->
      <span class="rc-marquee__item">Sansiri</span>
      <span class="rc-marquee__item">Ananda Development</span>
      <span class="rc-marquee__item">AP Thailand</span>
      <span class="rc-marquee__item">Origin Property</span>
      <span class="rc-marquee__item">Pruksa Holdings</span>
      <span class="rc-marquee__item">MQDC</span>
      <span class="rc-marquee__item">Central Pattana</span>
      <span class="rc-marquee__item">SC Asset</span>
      <span class="rc-marquee__item">Supalai PCL</span>
      <span class="rc-marquee__item">Golden Land</span>
    </div>
  </div>
</div>

<!-- PRODUCTS / SERVICES -->
<section id="services" class="rc-section">
  <div class="rc-container">
    <div class="rc-products__header">
      <div>
        <p class="rc-eyebrow rc-reveal">What We Build</p>
        <h2 class="rc-display rc-reveal" style="font-size:clamp(2rem,4vw,3rem);margin-top:.75rem;max-width:20ch;">
          Systems that turn data into<br>operational dominance.
        </h2>
      </div>
      <a href="<?php echo esc_url( get_permalink( get_page_by_path('services') ) ); ?>" class="rc-btn rc-btn--ghost rc-reveal">All services →</a>
    </div>

    <div class="rc-products__grid rc-reveal-group">

      <div class="rc-card">
        <div class="rc-card__icon" aria-hidden="true">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M3 13l4-4 3 3 5-6" stroke="#93b4f8" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="3" cy="13" r="1.5" fill="#93b4f8"/><circle cx="15" cy="4" r="1.5" fill="#93b4f8"/></svg>
        </div>
        <span class="rc-card__tag">AI Analytics</span>
        <h3>Market Intelligence at Scale</h3>
        <p>We index 50,000+ properties across Thailand in real time. AI models score investment opportunity, predict pricing movements, and surface signals manual research misses.</p>
        <a href="#" class="rc-card__link">Explore AI Analytics →</a>
      </div>

      <div class="rc-card">
        <div class="rc-card__icon" aria-hidden="true">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><rect x="2" y="8" width="6" height="8" rx="1" stroke="#93b4f8" stroke-width="1.5"/><rect x="10" y="4" width="6" height="12" rx="1" stroke="#93b4f8" stroke-width="1.5"/><path d="M2 8L9 2l7 6" stroke="#93b4f8" stroke-width="1.5" stroke-linecap="round"/></svg>
        </div>
        <span class="rc-card__tag">PropTech</span>
        <h3>Smart Property Infrastructure</h3>
        <p>From IoT-enabled buildings to automated listing pipelines and digital-twin asset management — we wire physical and digital into a single operational layer.</p>
        <a href="#" class="rc-card__link">Explore PropTech →</a>
      </div>

      <div class="rc-card rc-card--featured">
        <div>
          <div class="rc-card__icon" aria-hidden="true">
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M9 2L3 5v5c0 3.3 2.5 6.4 6 7 3.5-.6 6-3.7 6-7V5L9 2z" stroke="#93b4f8" stroke-width="1.5" stroke-linejoin="round"/><path d="M6 9l2 2 4-4" stroke="#93b4f8" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </div>
          <span class="rc-card__tag">Cybersecurity + OSINT</span>
          <h3>Security as a Competitive Advantage</h3>
          <p>Most real estate firms operate with exposed data and vulnerable infrastructure. We harden systems, run OSINT operations, and build threat models that protect assets — and create leverage.</p>
          <a href="#" class="rc-card__link">Explore Security →</a>
        </div>
        <div style="padding:2rem;background:var(--surface);border-radius:.875rem;border:1px solid var(--border-strong);">
          <p class="rc-card__tag" style="margin-bottom:1.5rem;">Recall principle</p>
          <blockquote style="border-left:2px solid var(--blue);padding-left:1rem;font-size:.9rem;color:var(--text-2);line-height:1.65;font-style:italic;">
            "Growth without security is temporary. One exposed database erases years of competitive data — and client trust."
          </blockquote>
        </div>
      </div>

      <div class="rc-card">
        <div class="rc-card__icon" aria-hidden="true">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M14 11a4 4 0 00-4-6.9A4 4 0 004 7a3 3 0 001 5.9h9a2 2 0 000-4" stroke="#93b4f8" stroke-width="1.5" stroke-linecap="round"/></svg>
        </div>
        <span class="rc-card__tag">Cloud &amp; Automation</span>
        <h3>Operational Automation Pipelines</h3>
        <p>We replace manual workflows with intelligent automation — lead scraping, multi-lingual follow-up, market reports. Delivered to your CRM. No manual work required.</p>
        <a href="#" class="rc-card__link">Explore Automation →</a>
      </div>

    </div>
  </div>
</section>

<!-- STATS -->
<div class="rc-stats">
  <div class="rc-container">
    <div class="rc-stats__grid rc-reveal-group">
      <div class="rc-stat">
        <div class="rc-stat__number"><span>53</span>K+</div>
        <div class="rc-stat__label">Properties indexed<br>across Thailand</div>
      </div>
      <div class="rc-stat">
        <div class="rc-stat__number"><span>140</span>+</div>
        <div class="rc-stat__label">Data sources<br>monitored in real time</div>
      </div>
      <div class="rc-stat">
        <div class="rc-stat__number"><span>27</span>/min</div>
        <div class="rc-stat__label">New property units<br>processed per minute</div>
      </div>
      <div class="rc-stat">
        <div class="rc-stat__number"><span>4</span></div>
        <div class="rc-stat__label">Verticals: Dev ·<br>Invest · Ops · Hospitality</div>
      </div>
    </div>
  </div>
</div>

<!-- SOLUTIONS TABS -->
<section id="solutions" class="rc-section">
  <div class="rc-container">
    <div class="rc-solutions__header">
      <p class="rc-eyebrow rc-reveal" style="justify-content:center;">Solutions by vertical</p>
      <h2 class="rc-display rc-reveal" style="font-size:clamp(2rem,4vw,3rem);margin-top:.75rem;">
        Built for how real estate<br>actually operates.
      </h2>
    </div>

    <div class="rc-tabs" role="tablist">
      <button class="rc-tab active" role="tab" aria-selected="true" data-tab="developers">Developers</button>
      <button class="rc-tab" role="tab" aria-selected="false" data-tab="investors">Investors</button>
      <button class="rc-tab" role="tab" aria-selected="false" data-tab="operators">Operators</button>
      <button class="rc-tab" role="tab" aria-selected="false" data-tab="hospitality">Hospitality</button>
    </div>

    <div class="rc-tab-panel active" id="tab-developers" role="tabpanel">
      <div class="rc-tab-panel__copy">
        <h3>From land acquisition to sell-out — data-driven, every step.</h3>
        <p>Intelligence systems that let developers analyse land opportunities, score demand, predict sell-out timelines, and automate buyer qualification. Stop relying on broker gut feel.</p>
        <ul class="rc-checklist">
          <li>Land opportunity scoring against comparable projects</li>
          <li>AI-assisted demand forecasting by zone &amp; segment</li>
          <li>Automated lead scoring and CRM enrichment</li>
          <li>Competitor pricing tracker (updated weekly)</li>
        </ul>
        <a href="<?php echo esc_url( get_permalink( get_page_by_path('contact') ) ); ?>" class="rc-btn rc-btn--primary" style="margin-top:1.5rem;">Request a demo →</a>
      </div>
      <div class="rc-tab-panel__visual">
        <div style="padding:2rem;width:100%;">
          <p class="rc-card__tag" style="margin-bottom:1rem;">Demand Score · Bangkok CBD</p>
          <?php $bars = [['Sukhumvit', 88], ['Silom', 74], ['Ratchada', 61], ['Rama 9', 52]]; ?>
          <div style="display:flex;flex-direction:column;gap:1rem;">
            <?php foreach ($bars as [$label, $pct]) : ?>
            <div>
              <div style="display:flex;justify-content:space-between;font-size:.8rem;color:var(--text-2);margin-bottom:.375rem;">
                <span><?php echo esc_html($label); ?></span><span><?php echo esc_html($pct); ?></span>
              </div>
              <div style="height:.5rem;border-radius:.25rem;background:var(--surface-hover);border:1px solid var(--border);overflow:hidden;">
                <div style="height:100%;width:<?php echo esc_attr($pct); ?>%;background:linear-gradient(90deg,var(--blue-dim),rgba(37,99,235,.4));"></div>
              </div>
            </div>
            <?php endforeach; ?>
          </div>
        </div>
      </div>
    </div>

    <div class="rc-tab-panel" id="tab-investors" role="tabpanel">
      <div class="rc-tab-panel__copy">
        <h3>Deploy capital with a structural information edge.</h3>
        <p>We give institutional and private investors data infrastructure that hedge funds use — applied to Thai real estate. Yield modelling, risk scoring, portfolio monitoring.</p>
        <ul class="rc-checklist">
          <li>Automated yield and ROI modelling per asset</li>
          <li>Market-wide price movement signals</li>
          <li>OSINT-backed due diligence automation</li>
          <li>Portfolio risk dashboard, updated in real time</li>
        </ul>
        <a href="<?php echo esc_url( get_permalink( get_page_by_path('contact') ) ); ?>" class="rc-btn rc-btn--primary" style="margin-top:1.5rem;">Request a demo →</a>
      </div>
      <div class="rc-tab-panel__visual">
        <div style="padding:2rem;text-align:center;">
          <p style="font-family:var(--font-mono);font-size:.7rem;color:var(--text-3);margin-bottom:1rem;">AVG GROSS YIELD · PHUKET Q2 2026</p>
          <p style="font-family:var(--font-display);font-size:3.5rem;font-weight:700;letter-spacing:-.04em;">+<span style="color:var(--blue);">7.4</span>%</p>
          <p style="font-size:.8rem;color:var(--text-2);margin-top:.5rem;">Annualised · Beach-adjacent condos</p>
        </div>
      </div>
    </div>

    <div class="rc-tab-panel" id="tab-operators" role="tabpanel">
      <div class="rc-tab-panel__copy">
        <h3>Cut manual work. Scale without scaling headcount.</h3>
        <p>Property management at scale requires intelligent automation. We wire your operations — from inquiry to contract to maintenance — into a single automated pipeline.</p>
        <ul class="rc-checklist">
          <li>Multi-lingual lead automation (EN / TH / ZH / FR)</li>
          <li>Automated follow-up and appointment booking</li>
          <li>Property data syndication across portals</li>
          <li>Maintenance prediction via IoT sensor data</li>
        </ul>
        <a href="<?php echo esc_url( get_permalink( get_page_by_path('contact') ) ); ?>" class="rc-btn rc-btn--primary" style="margin-top:1.5rem;">Request a demo →</a>
      </div>
      <div class="rc-tab-panel__visual">
        <div style="padding:2rem;width:100%;">
          <p class="rc-card__tag" style="margin-bottom:1rem;">Automation pipeline</p>
          <?php
          $steps = [['Inquiry received','0ms'],['Lead scored','1.2s'],['Sequence triggered','1.2s'],['Appointment set','Auto']];
          foreach ($steps as $i => [$step, $time]) : ?>
          <div style="display:flex;align-items:center;gap:.75rem;font-size:.8rem;margin-bottom:.75rem;">
            <div style="width:1.5rem;height:1.5rem;border-radius:50%;background:var(--blue-dim);border:1px solid rgba(37,99,235,.3);display:flex;align-items:center;justify-content:center;font-size:.65rem;color:#93b4f8;flex-shrink:0;"><?php echo esc_html($i + 1); ?></div>
            <span style="color:var(--text-2);"><?php echo esc_html($step); ?></span>
            <span style="margin-left:auto;font-size:.7rem;color:var(--text-3);"><?php echo esc_html($time); ?></span>
          </div>
          <?php endforeach; ?>
        </div>
      </div>
    </div>

    <div class="rc-tab-panel" id="tab-hospitality" role="tabpanel">
      <div class="rc-tab-panel__copy">
        <h3>Hospitality assets that outperform the market.</h3>
        <p>Boutique hotels, serviced apartments, and villa portfolios in Thailand compete on pricing, occupancy, and guest experience. We give operators AI infrastructure to win on all three.</p>
        <ul class="rc-checklist">
          <li>Dynamic pricing engine vs. competitor rates</li>
          <li>Demand forecasting by seasonality &amp; source market</li>
          <li>Guest data activation and retention automation</li>
          <li>OTA performance optimisation dashboard</li>
        </ul>
        <a href="<?php echo esc_url( get_permalink( get_page_by_path('contact') ) ); ?>" class="rc-btn rc-btn--primary" style="margin-top:1.5rem;">Request a demo →</a>
      </div>
      <div class="rc-tab-panel__visual">
        <div style="padding:2rem;text-align:center;">
          <p style="font-family:var(--font-mono);font-size:.7rem;color:var(--text-3);margin-bottom:1rem;">OCCUPANCY LIFT · SAMPLE CLIENT</p>
          <p style="font-family:var(--font-display);font-size:3.5rem;font-weight:700;letter-spacing:-.04em;">+<span style="color:var(--gold);">18</span>%</p>
          <p style="font-size:.8rem;color:var(--text-2);margin-top:.5rem;">Average within 90 days of deployment</p>
        </div>
      </div>
    </div>

  </div>
</section>

<!-- ENTERPRISE FEATURES -->
<section class="rc-section rc-section--tight" style="background:var(--bg-warm);">
  <div class="rc-container">
    <div class="rc-features__header">
      <p class="rc-eyebrow rc-reveal" style="justify-content:center;">Why REcall</p>
      <h2 class="rc-display rc-reveal" style="font-size:clamp(1.8rem,3.5vw,2.5rem);margin-top:.75rem;">Built different, by design.</h2>
    </div>
    <div class="rc-features__grid rc-reveal-group">
      <div class="rc-feature"><span class="rc-feature__icon">🔒</span><h4>Privacy-First Architecture</h4><p>Your data never leaves your infrastructure. We deploy open-source models on-premise — no SaaS lock-in, no third-party exposure.</p></div>
      <div class="rc-feature"><span class="rc-feature__icon">⚡</span><h4>Real-Time Intelligence</h4><p>Market signals updated continuously. 50K+ properties indexed. Decisions are made on fresh data, not last month's report.</p></div>
      <div class="rc-feature"><span class="rc-feature__icon">🧩</span><h4>Modular by Design</h4><p>We build systems you own, not platforms you rent. Every component is documented, transferable, and extensible.</p></div>
      <div class="rc-feature"><span class="rc-feature__icon">🌏</span><h4>Thailand-Native Context</h4><p>Built for Thai market structure, language, legal framework, and buyer psychology — not retrofitted from Western SaaS.</p></div>
      <div class="rc-feature"><span class="rc-feature__icon">🤝</span><h4>Human-Supervised Autonomy</h4><p>Agents execute. Humans decide. Every automation has override logic — no black boxes, no surprise actions.</p></div>
      <div class="rc-feature"><span class="rc-feature__icon">📐</span><h4>Auditable &amp; Transparent</h4><p>Every model, every pipeline, every data source is documented. Your compliance team can inspect the system end to end.</p></div>
    </div>
  </div>
</section>

<!-- LATEST INSIGHTS -->
<?php
$recent = wp_get_recent_posts(['numberposts' => 3, 'post_status' => 'publish']);
if ($recent) : ?>
<section class="rc-section rc-section--tight">
  <div class="rc-container">
    <div class="rc-products__header">
      <div>
        <p class="rc-eyebrow rc-reveal">Intelligence</p>
        <h2 class="rc-display rc-reveal" style="font-size:clamp(1.6rem,3vw,2.25rem);margin-top:.75rem;">Signal, not noise.</h2>
      </div>
      <a href="<?php echo esc_url( get_permalink( get_option('page_for_posts') ) ); ?>" class="rc-btn rc-btn--ghost rc-reveal">All insights →</a>
    </div>
    <div class="rc-blog-grid" style="padding-bottom:0;">
      <?php foreach ($recent as $p) : ?>
      <article class="rc-post-card">
        <div class="rc-post-card__body">
          <p class="rc-post-card__date"><?php echo esc_html( get_the_date('M j, Y', $p['ID']) ); ?></p>
          <h2><a href="<?php echo esc_url( get_permalink($p['ID']) ); ?>" style="color:inherit;"><?php echo esc_html($p['post_title']); ?></a></h2>
          <p><?php echo esc_html( wp_trim_words( strip_tags($p['post_content']), 18, '…' ) ); ?></p>
        </div>
      </article>
      <?php endforeach; wp_reset_postdata(); ?>
    </div>
  </div>
</section>
<?php endif; ?>

<!-- FOOTER CTA -->
<section class="rc-cta">
  <div class="rc-container">
    <div class="rc-cta__inner">
      <p class="rc-eyebrow rc-reveal" style="justify-content:center;">Ready to build an edge?</p>
      <h2 class="rc-display rc-reveal" style="font-size:clamp(2rem,5vw,3.5rem);max-width:18ch;">
        You don't need more tools.<br>You need <em>architecture</em>.
      </h2>
      <p class="rc-subhead rc-reveal" style="text-align:center;">
        Most firms optimise campaigns. We optimise systems.
        Book a 30-minute strategy call — no pitch, no fluff. Just a direct assessment of where AI creates leverage in your operations.
      </p>
      <div class="rc-hero__actions rc-reveal">
        <a href="<?php echo esc_url( get_permalink( get_page_by_path('contact') ) ); ?>" class="rc-btn rc-btn--primary">Book a strategy call →</a>
        <a href="<?php echo esc_url( get_permalink( get_page_by_path('services') ) ); ?>" class="rc-btn rc-btn--ghost">View services</a>
      </div>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer class="rc-footer" role="contentinfo">
  <div class="rc-container">
    <div class="rc-footer__grid">
      <div class="rc-footer__brand">
        <a href="<?php echo esc_url( home_url('/') ); ?>" style="font-family:var(--font-display);font-size:1.1rem;font-weight:700;letter-spacing:-.025em;color:var(--text-1);">
          RE<span style="color:var(--blue);">call</span>
        </a>
        <p>The intelligence layer for real estate in Thailand and Southeast Asia. We build systems that turn data and infrastructure into strategic dominance.</p>
      </div>
      <div class="rc-footer__col">
        <h5>Services</h5>
        <ul>
          <li><a href="#">AI Analytics</a></li>
          <li><a href="#">PropTech</a></li>
          <li><a href="#">Cybersecurity</a></li>
          <li><a href="#">Automation</a></li>
        </ul>
      </div>
      <div class="rc-footer__col">
        <h5>Company</h5>
        <ul>
          <li><a href="<?php echo esc_url( get_permalink( get_page_by_path('about') ) ); ?>">About</a></li>
          <li><a href="<?php echo esc_url( get_permalink( get_option('page_for_posts') ) ); ?>">Insights</a></li>
          <li><a href="<?php echo esc_url( get_permalink( get_page_by_path('contact') ) ); ?>">Contact</a></li>
        </ul>
      </div>
      <div class="rc-footer__col">
        <h5>Legal</h5>
        <ul>
          <li><a href="<?php echo esc_url( get_permalink( get_page_by_path('privacy-policy') ) ); ?>">Privacy Policy</a></li>
          <li><a href="<?php echo esc_url( get_permalink( get_page_by_path('terms-of-use') ) ); ?>">Terms of Use</a></li>
        </ul>
      </div>
    </div>
    <div class="rc-footer__bottom">
      <span>© <?php echo esc_html( date('Y') ); ?> REcall Agency · Bangkok, Thailand</span>
      <span>Built on open-source AI infrastructure</span>
    </div>
  </div>
</footer>

</main>
<?php get_footer(); ?>
