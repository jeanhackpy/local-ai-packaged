<?php
/**
 * REcall Agency Child Theme — functions.php v3
 * Business Plan 2026 — Intelligence Layer for Real Estate
 *
 * @package Recall_Agency
 */

define( 'RECALL_THEME_VERSION', '3.0.0' );

/* ─────────────────────────────────────────
   1. ENQUEUE ASSETS
───────────────────────────────────────── */
function recall_enqueue_assets(): void {
    // Parent theme
    wp_enqueue_style(
        'astra-theme-css',
        get_template_directory_uri() . '/style.css',
        [],
        RECALL_THEME_VERSION
    );

    // Child theme
    wp_enqueue_style(
        'recall-child-css',
        get_stylesheet_directory_uri() . '/style.css',
        [ 'astra-theme-css' ],
        RECALL_THEME_VERSION
    );

    // Google Fonts: Space Grotesk + Inter + JetBrains Mono
    wp_enqueue_style(
        'recall-fonts',
        'https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500&family=JetBrains+Mono:wght@400;500&display=swap',
        [],
        null
    );

    // GSAP + ScrollTrigger (footer load for performance)
    wp_enqueue_script(
        'gsap',
        'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js',
        [],
        '3.12.5',
        true
    );
    wp_enqueue_script(
        'gsap-st',
        'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js',
        [ 'gsap' ],
        '3.12.5',
        true
    );

    // Custom JS
    wp_enqueue_script(
        'recall-main',
        get_stylesheet_directory_uri() . '/customscript.js',
        [ 'gsap-st' ],
        RECALL_THEME_VERSION,
        true
    );
}
add_action( 'wp_enqueue_scripts', 'recall_enqueue_assets', 15 );


/* ─────────────────────────────────────────
   2. STRIP ELEMENTOR ON FRONT PAGE
───────────────────────────────────────── */
function recall_dequeue_elementor_on_front(): void {
    if ( ! is_front_page() ) {
        return;
    }

    $scripts_to_remove = [
        'elementor-frontend',
        'elementor-frontend-modules',
        'elementor-waypoints',
        'elementor-pro-frontend',
    ];
    foreach ( $scripts_to_remove as $handle ) {
        wp_dequeue_script( $handle );
        wp_deregister_script( $handle );
    }

    $styles_to_remove = [
        'elementor-frontend',
        'elementor-global',
        'elementor-post-9',
        'elementor-icons',
        'elementor-animations',
        'elementor-pro',
    ];
    foreach ( $styles_to_remove as $handle ) {
        wp_dequeue_style( $handle );
    }
}
add_action( 'wp_enqueue_scripts', 'recall_dequeue_elementor_on_front', 999 );


/* ─────────────────────────────────────────
   3. SCHEMA MARKUP — Organization + Service
───────────────────────────────────────── */
function recall_schema_markup(): void {
    if ( is_front_page() || is_home() ) {
        $org_schema = [
            '@context'    => 'https://schema.org',
            '@type'       => 'Organization',
            'name'        => 'REcall Agency',
            'url'         => 'https://recall-agency.com',
            'logo'        => 'https://recall-agency.com/wp-content/uploads/recall-logo.png',
            'description' => 'REcall Agency builds AI-powered intelligence systems for real estate firms in Thailand and Southeast Asia — data sovereignty, operational automation, and market analytics.',
            'areaServed'  => [ 'Thailand', 'Southeast Asia' ],
            'knowsAbout'  => [ 'AI', 'Real Estate', 'Data Infrastructure', 'Cybersecurity', 'PropTech', 'Automation' ],
            'sameAs'      => [
                'https://linkedin.com/company/recall-agency',
            ],
            'contactPoint' => [
                '@type'       => 'ContactPoint',
                'contactType' => 'sales',
                'email'       => 'hello@recall-agency.com',
                'areaServed'  => 'TH',
            ],
        ];

        $service_schema = [
            '@context'    => 'https://schema.org',
            '@type'       => 'Service',
            'name'        => 'AI Real Estate Intelligence Services',
            'provider'    => [
                '@type' => 'Organization',
                'name'  => 'REcall Agency',
            ],
            'serviceType' => 'AI-Powered Real Estate Technology Consulting',
            'areaServed'  => 'Thailand',
            'description' => 'We build AI analytics, PropTech infrastructure, cybersecurity systems, and automation pipelines for real estate developers, investors, and operators in Thailand.',
            'hasOfferCatalog' => [
                '@type' => 'OfferCatalog',
                'name'  => 'REcall Services',
                'itemListElement' => [
                    [ '@type' => 'Offer', 'itemOffered' => [ '@type' => 'Service', 'name' => 'AI Market Analytics' ] ],
                    [ '@type' => 'Offer', 'itemOffered' => [ '@type' => 'Service', 'name' => 'PropTech Infrastructure' ] ],
                    [ '@type' => 'Offer', 'itemOffered' => [ '@type' => 'Service', 'name' => 'Cybersecurity & OSINT' ] ],
                    [ '@type' => 'Offer', 'itemOffered' => [ '@type' => 'Service', 'name' => 'Automation Pipelines' ] ],
                ],
            ],
        ];

        echo '<script type="application/ld+json">' . wp_json_encode( $org_schema, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
        echo '<script type="application/ld+json">' . wp_json_encode( $service_schema, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
    }

    if ( is_singular('post') ) {
        global $post;
        $article_schema = [
            '@context'        => 'https://schema.org',
            '@type'           => 'Article',
            'headline'        => get_the_title(),
            'datePublished'   => get_the_date( 'c' ),
            'dateModified'    => get_the_modified_date( 'c' ),
            'author'          => [
                '@type' => 'Organization',
                'name'  => 'REcall Agency',
            ],
            'publisher'       => [
                '@type' => 'Organization',
                'name'  => 'REcall Agency',
                'logo'  => [ '@type' => 'ImageObject', 'url' => 'https://recall-agency.com/wp-content/uploads/recall-logo.png' ],
            ],
            'mainEntityOfPage' => [ '@type' => 'WebPage', '@id' => get_permalink() ],
        ];
        echo '<script type="application/ld+json">' . wp_json_encode( $article_schema, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
    }
}
add_action( 'wp_head', 'recall_schema_markup' );


/* ─────────────────────────────────────────
   4. SEO META TAGS (fallback for Rank Math)
───────────────────────────────────────── */
function recall_seo_meta(): void {
    // Only output if Rank Math is NOT active
    if ( function_exists( 'rank_math' ) || function_exists( 'yoast_breadcrumb' ) ) {
        return;
    }

    if ( is_front_page() ) {
        echo '<meta name="description" content="REcall Agency builds AI-powered intelligence systems for real estate firms in Thailand and Southeast Asia. AI analytics, PropTech, cybersecurity, and automation pipelines.">' . "\n";
        echo '<meta property="og:title" content="REcall Agency — AI Intelligence for Real Estate in Thailand">' . "\n";
        echo '<meta property="og:description" content="We build systems that turn data, infrastructure, and real-world assets into strategic dominance for Thai real estate firms.">' . "\n";
        echo '<meta property="og:type" content="website">' . "\n";
        echo '<meta property="og:url" content="' . esc_url( home_url('/') ) . '">' . "\n";
    }
}
add_action( 'wp_head', 'recall_seo_meta', 5 );


/* ─────────────────────────────────────────
   5. SECURITY HEADERS (via wp_head)
───────────────────────────────────────── */
function recall_security_headers(): void {
    if ( ! headers_sent() ) {
        header( 'X-Content-Type-Options: nosniff' );
        header( 'X-Frame-Options: SAMEORIGIN' );
        header( 'Referrer-Policy: strict-origin-when-cross-origin' );
        header( 'Permissions-Policy: geolocation=(), microphone=(), camera=()' );
    }
}
add_action( 'send_headers', 'recall_security_headers' );


/* ─────────────────────────────────────────
   6. AI CRAWLER PERMISSIONS (llms.txt route)
───────────────────────────────────────── */
function recall_llms_txt_rewrite(): void {
    add_rewrite_rule( '^llms\.txt$', 'index.php?recall_llms_txt=1', 'top' );
}
add_action( 'init', 'recall_llms_txt_rewrite' );

function recall_llms_txt_query_var( array $vars ): array {
    $vars[] = 'recall_llms_txt';
    return $vars;
}
add_filter( 'query_vars', 'recall_llms_txt_query_var' );

function recall_llms_txt_output(): void {
    if ( ! get_query_var( 'recall_llms_txt' ) ) {
        return;
    }
    header( 'Content-Type: text/plain; charset=utf-8' );
    echo "# REcall Agency\n";
    echo "> The intelligence layer for real estate in Thailand and Southeast Asia.\n\n";
    echo "## About\n";
    echo "REcall Agency builds AI-powered systems — market analytics, PropTech infrastructure, cybersecurity, and automation pipelines — for real estate firms in Thailand and SEA.\n\n";
    echo "## Key Pages\n";
    echo "- Homepage: https://recall-agency.com/\n";
    echo "- Services: https://recall-agency.com/services/\n";
    echo "- Blog/Insights: https://recall-agency.com/blog/\n";
    echo "- Contact: https://recall-agency.com/contact/\n\n";
    echo "## AI Crawlers\n";
    echo "ClaudeBot, GPTBot, PerplexityBot, Google-Extended: allowed\n";
    exit;
}
add_action( 'template_redirect', 'recall_llms_txt_output' );


/* ─────────────────────────────────────────
   7. DISABLE XML-RPC (security)
───────────────────────────────────────── */
add_filter( 'xmlrpc_enabled', '__return_false' );


/* ─────────────────────────────────────────
   8. REMOVE WORDPRESS VERSION (security)
───────────────────────────────────────── */
remove_action( 'wp_head', 'wp_generator' );


/* ─────────────────────────────────────────
   9. THEME SUPPORT
───────────────────────────────────────── */
function recall_theme_setup(): void {
    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support( 'html5', [ 'search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'style', 'script' ] );
    add_theme_support( 'custom-logo' );
}
add_action( 'after_setup_theme', 'recall_theme_setup' );
