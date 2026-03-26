<?php
/**
 * Front Page Template — Recall Agency
 *
 * @package Recall_Agency
 */
get_header(); ?>

<main id="main" class="site-main" style="background:transparent;">

  <!-- ════════════ HERO ════════════ -->
  <section class="rc-hero">
    <span class="rc-label rc-reveal">Agentic AI Services</span>
    <h1 class="rc-display rc-reveal">
      Hire AI Agents<br>That Work While<br>You Sleep.
    </h1>
    <p class="rc-subtitle rc-reveal">
      We build autonomous automation pipelines for real estate, e-commerce, and tourism businesses. Less manual work, more closed deals.
    </p>
    <div class="rc-actions rc-reveal">
      <a href="#contact" class="rc-btn">Book Free AI Audit</a>
      <a href="#services" class="rc-btn rc-btn-ghost">See Our Agents →</a>
    </div>
  </section>

  <!-- ════════════ SERVICES BENTO ════════════ -->
  <section id="services" class="rc-section">
    <header class="rc-section-header">
      <span class="rc-label rc-reveal">What We Automate</span>
      <h2 class="rc-display rc-reveal" style="font-size:clamp(2rem,5vw,3.5rem);margin-top:1rem;">
        Your AI workforce, ready to deploy.
      </h2>
    </header>

    <div class="rc-bento">
      <div class="rc-card rc-reveal">
        <span class="rc-label">Lead Scraper Agent</span>
        <h3>24/7 marketplace monitoring</h3>
        <p>Our agents scan property portals, e-commerce platforms, and booking sites around the clock. They extract, clean, and deliver qualified leads directly into your CRM — no manual work required.</p>
      </div>

      <div class="rc-card rc-reveal">
        <span class="rc-label">Follow-Up Agent</span>
        <h3>Multi-lingual automation</h3>
        <p>Automated email and messaging sequences in Thai, English, and French. Your prospects get instant, personalized responses while you focus on closing.</p>
      </div>

      <div class="rc-card rc-reveal">
        <span class="rc-label">Data Analyst Agent</span>
        <h3>Market intelligence on demand</h3>
        <p>GPT-powered reports on pricing trends, competitor analysis, and opportunity scoring. Updated weekly, delivered to your inbox.</p>
      </div>

      <div class="rc-card rc-reveal">
        <span class="rc-label">Content Agent</span>
        <h3>SEO content at scale</h3>
        <p>From listing descriptions to blog articles, our content pipeline produces search-optimized material that ranks. We handle research, writing, and publishing — automatically.</p>
      </div>
    </div>
  </section>

  <!-- ════════════ INDUSTRIES ════════════ -->
  <section class="rc-section">
    <header class="rc-section-header">
      <span class="rc-label rc-reveal">Industries We Serve</span>
      <h2 class="rc-display rc-reveal" style="font-size:clamp(2rem,5vw,3.5rem);margin-top:1rem;">
        AI automation, tailored to your vertical.
      </h2>
    </header>

    <div class="rc-industries">
      <div class="rc-card rc-reveal">
        <span class="rc-label">Real Estate</span>
        <h3>Your AI-powered property pipeline</h3>
        <p>Automated lead generation, market analysis, and CRM workflows for agents, agencies, and developers across Thailand.</p>
      </div>

      <div class="rc-card rc-reveal">
        <span class="rc-label">E-Commerce</span>
        <h3>Inventory, pricing & customer service</h3>
        <p>Automate supplier monitoring, dynamic pricing, and customer support with intelligent agents that scale with your store.</p>
      </div>

      <div class="rc-card rc-reveal">
        <span class="rc-label">Tourism & Hospitality</span>
        <h3>Intelligent booking & guest experience</h3>
        <p>From reservation management to personalized guest communication, our agents handle the operational load so you can focus on experiences.</p>
      </div>
    </div>
  </section>

  <!-- ════════════ ABOUT / WHY RECALL ════════════ -->
  <section class="rc-section">
    <header class="rc-section-header">
      <span class="rc-label rc-reveal">Why Recall Agency</span>
      <h2 class="rc-display rc-reveal" style="font-size:clamp(2rem,5vw,3.5rem);margin-top:1rem;">
        Built different.
      </h2>
    </header>

    <div class="rc-bento">
      <div class="rc-card rc-reveal" style="grid-column:span 6;">
        <h3>Thailand-native, globally minded</h3>
        <p>Based in Bangkok, we understand the local market dynamics — the language barriers, the fragmented data, the operational chaos. We build solutions that work here, first.</p>
      </div>
      <div class="rc-card rc-reveal" style="grid-column:span 6;">
        <h3>From SEO veterans to AI builders</h3>
        <p>We spent years mastering SEO and paid acquisition. Now we apply that same data-driven rigor to building autonomous AI agents. We know what converts.</p>
      </div>
    </div>
  </section>

  <!-- ════════════ CTA ════════════ -->
  <section id="contact" class="rc-cta">
    <span class="rc-label rc-reveal">Ready to automate?</span>
    <h2 class="rc-display rc-reveal" style="margin-top:1rem;">
      Let's build your first AI agent.
    </h2>
    <p class="rc-subtitle rc-reveal" style="margin:1.5rem auto 3rem;text-align:center;">
      Book a free 30-minute audit. We'll show you exactly which manual tasks you can eliminate this month.
    </p>
    <div class="rc-reveal">
      <a href="mailto:hello@recall-agency.com" class="rc-btn">Book Free AI Audit</a>
    </div>
  </section>

</main>

<?php get_footer(); ?>
