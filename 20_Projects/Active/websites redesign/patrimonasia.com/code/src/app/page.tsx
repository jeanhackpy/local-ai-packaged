export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 px-8 py-6 bg-navy-900/90 backdrop-blur-md border-b border-gold-500/10">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 border border-gold-500 flex items-center justify-center">
              <span className="font-display text-gold-500 text-xl font-semibold">P</span>
            </div>
            <span className="font-display text-2xl text-cream tracking-wider">PATRIMONASIA</span>
          </div>
          <div className="hidden md:flex items-center gap-12">
            <a href="#philosophy" className="nav-link text-sm tracking-widest uppercase">Philosophy</a>
            <a href="#services" className="nav-link text-sm tracking-widest uppercase">Services</a>
            <a href="#asia" className="nav-link text-sm tracking-widest uppercase">Asia</a>
            <a href="#contact" className="nav-link text-sm tracking-widest uppercase">Contact</a>
          </div>
          <button className="btn-outline text-sm tracking-wider uppercase">
            Private Access
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center px-8 pt-32 pb-20 overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-5">
          <div className="absolute inset-0" style={{
            backgroundImage: `radial-gradient(circle at 1px 1px, var(--color-gold-500) 1px, transparent 0)`,
            backgroundSize: '60px 60px'
          }} />
        </div>

        {/* Gradient Overlays */}
        <div className="absolute top-0 left-0 right-0 h-1/2 bg-gradient-to-b from-navy-900/50 to-transparent" />
        <div className="absolute bottom-0 left-0 right-0 h-1/2 bg-gradient-to-t from-navy-900 via-transparent to-transparent" />

        <div className="relative z-10 max-w-5xl mx-auto text-center">
          <p className="text-gold-500 text-sm tracking-[0.4em] uppercase mb-8 animate-fade-in">
            Private Wealth Advisory
          </p>

          <h1 className="font-display text-5xl md:text-7xl lg:text-8xl text-cream leading-none mb-8 animate-slide-up">
            Where European
            <br />
            <span className="text-gradient-gold italic">Sophistication</span>
            <br />
            Meets Asian Opportunity
          </h1>

          <p className="text-cream/70 text-lg md:text-xl max-w-2xl mx-auto mb-12 animate-slide-up animate-delay-200">
            Exclusive advisory for family offices, CGP, and wealth managers seeking exceptional Thai real estate assets through a trusted institutional lens.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center animate-slide-up animate-delay-300">
            <button className="btn-gold text-sm tracking-wider uppercase">
              Request Private Briefing
            </button>
            <button className="btn-outline text-sm tracking-wider uppercase">
              Explore Our Approach
            </button>
          </div>
        </div>

        {/* Scroll Indicator */}
        <div className="absolute bottom-12 left-1/2 -translate-x-1/2 animate-bounce">
          <div className="w-6 h-10 border border-gold-500/30 rounded-full flex items-start justify-center p-2">
            <div className="w-1 h-2 bg-gold-500/50 rounded-full" />
          </div>
        </div>
      </section>

      {/* Section Divider */}
      <div className="section-divider max-w-4xl mx-auto" />

      {/* Philosophy Section */}
      <section id="philosophy" className="py-32 px-8">
        <div className="max-w-6xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div>
              <p className="text-gold-500 text-sm tracking-[0.3em] uppercase mb-4">Our Philosophy</p>
              <h2 className="font-display text-4xl md:text-5xl text-cream leading-tight mb-8">
                Navigating Wealth
                <br />
                <span className="text-gold-500">Across Borders</span>
              </h2>
              <p className="text-cream/70 leading-relaxed mb-6">
                At Patrimonasia, we bridge the gap between European private banking standards and the immense opportunities within Asian real estate markets. Our approach is rooted in discretion, transparency, and an unwavering commitment to our clients' long-term prosperity.
              </p>
              <p className="text-cream/70 leading-relaxed mb-8">
                We serve as trusted advisors to family offices and independent wealth managers, providing access to curated Thai property investments that meet the rigorous standards of European institutional portfolios.
              </p>
              <div className="flex gap-8">
                <div>
                  <p className="font-display text-4xl text-gold-500">€2.4B</p>
                  <p className="text-cream/50 text-sm">Assets Advised</p>
                </div>
                <div>
                  <p className="font-display text-4xl text-gold-500">180+</p>
                  <p className="text-cream/50 text-sm">Family Offices</p>
                </div>
                <div>
                  <p className="font-display text-4xl text-gold-500">15</p>
                  <p className="text-cream/50 text-sm">Years Asia Focus</p>
                </div>
              </div>
            </div>
            <div className="relative">
              <div className="aspect-[4/5] bg-gradient-to-br from-navy-800 to-navy-700 rounded-sm border border-gold-500/20 p-8 flex items-center justify-center">
                <div className="text-center">
                  <div className="w-24 h-24 mx-auto mb-6 border-2 border-gold-500/30 rounded-full flex items-center justify-center">
                    <div className="w-16 h-16 border border-gold-500/50 rounded-full flex items-center justify-center">
                      <span className="text-gold-500 font-display text-2xl">P</span>
                    </div>
                  </div>
                  <p className="font-display text-xl text-cream mb-2">Est. 2009</p>
                  <p className="text-cream/50 text-sm">Singapore · Bangkok · Geneva</p>
                </div>
              </div>
              {/* Decorative Elements */}
              <div className="absolute -top-4 -right-4 w-32 h-32 border border-gold-500/20" />
              <div className="absolute -bottom-4 -left-4 w-32 h-32 border border-gold-500/20" />
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section id="services" className="py-32 px-8 bg-navy-800/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-20">
            <p className="text-gold-500 text-sm tracking-[0.3em] uppercase mb-4">Advisory Services</p>
            <h2 className="font-display text-4xl md:text-5xl text-cream">
              Bespoke Wealth Solutions
            </h2>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="card-premium">
              <div className="w-12 h-12 border border-gold-500/30 flex items-center justify-center mb-6">
                <svg className="w-6 h-6 text-gold-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
              </div>
              <h3 className="font-display text-xl text-cream mb-4">Portfolio Integration</h3>
              <p className="text-cream/60 text-sm leading-relaxed">
                Seamless integration of Thai real estate assets into existing European portfolios, ensuring regulatory compliance and optimal diversification.
              </p>
            </div>

            <div className="card-premium">
              <div className="w-12 h-12 border border-gold-500/30 flex items-center justify-center mb-6">
                <svg className="w-6 h-6 text-gold-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="font-display text-xl text-cream mb-4">Due Diligence</h3>
              <p className="text-cream/60 text-sm leading-relaxed">
                Rigorous vetting of developers, properties, and legal structures. Our institutional-grade analysis protects your clients' interests.
              </p>
            </div>

            <div className="card-premium">
              <div className="w-12 h-12 border border-gold-500/30 flex items-center justify-center mb-6">
                <svg className="w-6 h-6 text-gold-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 className="font-display text-xl text-cream mb-4">CGP Partnerships</h3>
              <p className="text-cream/60 text-sm leading-relaxed">
                Specialized advisory for Connected Wealth Professionals seeking exclusive off-market opportunities and priority access to premium developments.
              </p>
            </div>

            <div className="card-premium">
              <div className="w-12 h-12 border border-gold-500/30 flex items-center justify-center mb-6">
                <svg className="w-6 h-6 text-gold-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <h3 className="font-display text-xl text-cream mb-4">Developer Selection</h3>
              <p className="text-cream/60 text-sm leading-relaxed">
                Curated network of Thailand's most reputable developers, ensuring quality construction, transparent pricing, and reliable delivery.
              </p>
            </div>

            <div className="card-premium">
              <div className="w-12 h-12 border border-gold-500/30 flex items-center justify-center mb-6">
                <svg className="w-6 h-6 text-gold-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                </svg>
              </div>
              <h3 className="font-display text-xl text-cream mb-4">Legal Framework</h3>
              <p className="text-cream/60 text-sm leading-relaxed">
                Comprehensive legal guidance on Thai property ownership structures, foreign exchange regulations, and international tax planning.
              </p>
            </div>

            <div className="card-premium">
              <div className="w-12 h-12 border border-gold-500/30 flex items-center justify-center mb-6">
                <svg className="w-6 h-6 text-gold-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="font-display text-xl text-cream mb-4">Estate Planning</h3>
              <p className="text-cream/60 text-sm leading-relaxed">
                Multi-generational wealth transfer strategies incorporating Thai assets within compliant European estate frameworks.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Asia Focus Section */}
      <section id="asia" className="py-32 px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-20">
            <p className="text-gold-500 text-sm tracking-[0.3em] uppercase mb-4">Why Thailand</p>
            <h2 className="font-display text-4xl md:text-5xl text-cream mb-6">
              The Asian Opportunity
            </h2>
            <p className="text-cream/60 max-w-2xl mx-auto">
              Thailand represents one of Southeast Asia's most compelling markets for European investors seeking stable returns, cultural appeal, and strategic diversification.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
            <div className="text-center">
              <div className="font-display text-5xl text-gold-500 mb-4">8.5%</div>
              <p className="text-cream/80 text-sm">Tourism Growth (2024)</p>
              <p className="text-cream/40 text-xs mt-1">Resilient recovery</p>
            </div>
            <div className="text-center">
              <div className="font-display text-5xl text-gold-500 mb-4">69M</div>
              <p className="text-cream/80 text-sm">International Visitors</p>
              <p className="text-cream/40 text-xs mt-1">Record arrivals</p>
            </div>
            <div className="text-center">
              <div className="font-display text-5xl text-gold-500 mb-4">3.5%</div>
              <p className="text-cream/80 text-sm">GDP Growth</p>
              <p className="text-cream/40 text-xs mt-1">Stable trajectory</p>
            </div>
            <div className="text-center">
              <div className="font-display text-5xl text-gold-500 mb-4">$150K</div>
              <p className="text-cream/80 text-sm">Average Villa Price</p>
              <p className="text-cream/40 text-xs mt-1">Premium segment</p>
            </div>
          </div>

          <div className="grid lg:grid-cols-3 gap-6">
            <div className="bg-navy-800/50 border border-gold-500/10 rounded-sm p-8">
              <h3 className="font-display text-xl text-gold-500 mb-4">Bangkok</h3>
              <p className="text-cream/60 text-sm mb-4">
                Prime condominiums and commercial properties in the city's most prestigious addresses, with strong rental yields and capital appreciation.
              </p>
              <p className="text-gold-500/70 text-xs">Core · Liquid · 5-7% Net Yield</p>
            </div>
            <div className="bg-navy-800/50 border border-gold-500/10 rounded-sm p-8">
              <h3 className="font-display text-xl text-gold-500 mb-4">Phuket</h3>
              <p className="text-cream/60 text-sm mb-4">
                Exclusive beachfront villas and boutique resorts catering to the ultra-high-net-worth segment seeking luxury lifestyle assets.
              </p>
              <p className="text-gold-500/70 text-xs">Luxury · Tourism · 6-8% Net Yield</p>
            </div>
            <div className="bg-navy-800/50 border border-gold-500/10 rounded-sm p-8">
              <h3 className="font-display text-xl text-gold-500 mb-4">Koh Samui</h3>
              <p className="text-cream/60 text-sm mb-4">
                Private island retreats and wellness estates for discerning buyers seeking unique lifestyle investments.
              </p>
              <p className="text-gold-500/70 text-xs">Lifestyle · Niche · 7-10% Net Yield</p>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Section */}
      <section className="py-32 px-8 bg-navy-800/30">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-4 mb-8">
            <div className="w-16 h-px bg-gradient-to-r from-transparent to-gold-500/50" />
            <p className="text-gold-500 text-sm tracking-[0.3em] uppercase">Institutional Standards</p>
            <div className="w-16 h-px bg-gradient-to-l from-transparent to-gold-500/50" />
          </div>

          <h2 className="font-display text-3xl md:text-4xl text-cream mb-8">
            Trusted by Europe's Most Selective Wealth Managers
          </h2>

          <p className="text-cream/60 mb-12 max-w-2xl mx-auto">
            We maintain the same standards expected by Swiss private banks and Monaco family offices, adapted for the unique opportunities in Asian real estate markets.
          </p>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-12">
            <div className="flex flex-col items-center gap-2">
              <div className="w-12 h-12 border border-gold-500/30 flex items-center justify-center">
                <svg className="w-6 h-6 text-gold-500/70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <p className="text-cream/50 text-xs">Licensed</p>
            </div>
            <div className="flex flex-col items-center gap-2">
              <div className="w-12 h-12 border border-gold-500/30 flex items-center justify-center">
                <svg className="w-6 h-6 text-gold-500/70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <p className="text-cream/50 text-xs">Encrypted</p>
            </div>
            <div className="flex flex-col items-center gap-2">
              <div className="w-12 h-12 border border-gold-500/30 flex items-center justify-center">
                <svg className="w-6 h-6 text-gold-500/70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <p className="text-cream/50 text-xs">Audited</p>
            </div>
            <div className="flex flex-col items-center gap-2">
              <div className="w-12 h-12 border border-gold-500/30 flex items-center justify-center">
                <svg className="w-6 h-6 text-gold-500/70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <p className="text-cream/50 text-xs">Independent</p>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-32 px-8">
        <div className="max-w-6xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-16">
            <div>
              <p className="text-gold-500 text-sm tracking-[0.3em] uppercase mb-4">Private Access</p>
              <h2 className="font-display text-4xl md:text-5xl text-cream leading-tight mb-8">
                Begin Your
                <br />
                <span className="text-gold-500">Advisory Journey</span>
              </h2>
              <p className="text-cream/60 mb-8">
                Our advisory process begins with a confidential consultation. We invite qualified family offices and CGP to discuss how Asian real estate can complement your portfolio strategy.
              </p>

              <div className="space-y-6">
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 border border-gold-500/20 flex items-center justify-center flex-shrink-0 mt-1">
                    <svg className="w-5 h-5 text-gold-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-cream/40 text-xs uppercase tracking-wider mb-1">Direct Line</p>
                    <p className="text-cream">advisory@patrimonasia.com</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 border border-gold-500/20 flex items-center justify-center flex-shrink-0 mt-1">
                    <svg className="w-5 h-5 text-gold-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-cream/40 text-xs uppercase tracking-wider mb-1">Bangkok Office</p>
                    <p className="text-cream">+66 2 XXX XXXX</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 border border-gold-500/20 flex items-center justify-center flex-shrink-0 mt-1">
                    <svg className="w-5 h-5 text-gold-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-cream/40 text-xs uppercase tracking-wider mb-1">Headquarters</p>
                    <p className="text-cream">Bangkok · Singapore · Geneva</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-navy-800/50 border border-gold-500/20 p-8 rounded-sm">
              <h3 className="font-display text-xl text-cream mb-6">Request Private Briefing</h3>
              <form className="space-y-6">
                <div>
                  <label className="block text-cream/40 text-xs uppercase tracking-wider mb-2">Full Name</label>
                  <input
                    type="text"
                    className="w-full bg-navy-900/50 border border-gold-500/20 px-4 py-3 text-cream focus:border-gold-500 focus:outline-none transition-colors"
                    placeholder="Your name"
                  />
                </div>
                <div>
                  <label className="block text-cream/40 text-xs uppercase tracking-wider mb-2">Organization</label>
                  <input
                    type="text"
                    className="w-full bg-navy-900/50 border border-gold-500/20 px-4 py-3 text-cream focus:border-gold-500 focus:outline-none transition-colors"
                    placeholder="Family office or firm"
                  />
                </div>
                <div>
                  <label className="block text-cream/40 text-xs uppercase tracking-wider mb-2">Email</label>
                  <input
                    type="email"
                    className="w-full bg-navy-900/50 border border-gold-500/20 px-4 py-3 text-cream focus:border-gold-500 focus:outline-none transition-colors"
                    placeholder="your@email.com"
                  />
                </div>
                <div>
                  <label className="block text-cream/40 text-xs uppercase tracking-wider mb-2">Area of Interest</label>
                  <select className="w-full bg-navy-900/50 border border-gold-500/20 px-4 py-3 text-cream/70 focus:border-gold-500 focus:outline-none transition-colors">
                    <option value="">Select focus area</option>
                    <option value="bangkok">Bangkok Condominiums</option>
                    <option value="phuket">Phuket Beachfront</option>
                    <option value="samui">Koh Samui Estate</option>
                    <option value="portfolio">Portfolio Integration</option>
                    <option value="cgp">CGP Partnership</option>
                  </select>
                </div>
                <button type="submit" className="btn-gold w-full text-sm tracking-wider uppercase">
                  Request Briefing
                </button>
              </form>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-8 border-t border-gold-500/10">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 border border-gold-500/50 flex items-center justify-center">
                <span className="font-display text-gold-500 text-sm font-semibold">P</span>
              </div>
              <span className="font-display text-lg text-cream tracking-wider">PATRIMONASIA</span>
            </div>
            <div className="flex items-center gap-8">
              <a href="#" className="text-cream/40 text-xs hover:text-gold-500 transition-colors">Privacy</a>
              <a href="#" className="text-cream/40 text-xs hover:text-gold-500 transition-colors">Terms</a>
              <a href="#" className="text-cream/40 text-xs hover:text-gold-500 transition-colors">Regulatory</a>
              <a href="#" className="text-cream/40 text-xs hover:text-gold-500 transition-colors">Careers</a>
            </div>
            <p className="text-cream/30 text-xs">
              © 2024 Patrimonasia. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </main>
  );
}