<?php
/**
 * Recall Agency Child Theme — functions.php
 *
 * @package Recall_Agency
 * @since 2.0.0
 */

define( 'RECALL_THEME_VERSION', '2.0.0' );

/**
 * Enqueue all styles and scripts.
 */
function recall_enqueue_assets() {
    // 1. Parent theme
    wp_enqueue_style( 'astra-theme-css', get_template_directory_uri() . '/style.css', array(), RECALL_THEME_VERSION );

    // 2. Child theme
    wp_enqueue_style( 'recall-child-css', get_stylesheet_directory_uri() . '/style.css', array( 'astra-theme-css' ), RECALL_THEME_VERSION );

    // 3. Fonts — Fraunces (Display) + Space Grotesk (Body)
    wp_enqueue_style( 'recall-fonts', 'https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;400;600;700&family=Space+Grotesk:wght@300;400;500;700&display=swap', array(), null );

    // 4. GSAP + ScrollTrigger
    wp_enqueue_script( 'gsap', 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js', array(), '3.12.5', true );
    wp_enqueue_script( 'gsap-st', 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js', array( 'gsap' ), '3.12.5', true );

    // 5. Three.js
    wp_enqueue_script( 'three-js', 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js', array(), 'r134', true );

    // 6. Custom 3D scene
    wp_enqueue_script( 'recall-three', get_stylesheet_directory_uri() . '/js/three-app.js', array( 'three-js', 'gsap-st' ), RECALL_THEME_VERSION, true );
}
add_action( 'wp_enqueue_scripts', 'recall_enqueue_assets', 15 );

/**
 * Remove Elementor frontend rendering on the front page
 * so only our custom template + Three.js scene runs.
 */
function recall_dequeue_elementor_on_front() {
    if ( is_front_page() ) {
        // Remove Elementor frontend JS
        wp_dequeue_script( 'elementor-frontend' );
        wp_deregister_script( 'elementor-frontend' );
        wp_dequeue_script( 'elementor-frontend-modules' );
        wp_deregister_script( 'elementor-frontend-modules' );
        wp_dequeue_script( 'elementor-waypoints' );
        wp_dequeue_script( 'elementor-pro-frontend' );
        wp_deregister_script( 'elementor-pro-frontend' );

        // Remove Elementor CSS
        wp_dequeue_style( 'elementor-frontend' );
        wp_dequeue_style( 'elementor-global' );
        wp_dequeue_style( 'elementor-post-9' );
        wp_dequeue_style( 'elementor-icons' );
        wp_dequeue_style( 'elementor-animations' );
        wp_dequeue_style( 'elementor-pro' );
    }
}
add_action( 'wp_enqueue_scripts', 'recall_dequeue_elementor_on_front', 999 );