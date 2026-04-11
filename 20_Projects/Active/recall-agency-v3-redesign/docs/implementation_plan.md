# Recall Agency - Frontend Redesign Plan

## 1. Goal Description
The objective is to redesign the `recall-agency.com` staging site (`v2`) with a premium, high-end visual aesthetic focused on Agentic AI and Automation for the Real Estate sector. 

Based on the provided references, the brand will center around a "High-Tech Infrastructure & Data Pipeline" aesthetic (dark mode, glowing green/purple nodes, server racks, datagrids). The hero section will feature a scroll-linked animation to provide an immersive 3D/video experience.

## 2. Technical Approach (WordPress Child Theme)

Because we are building this inside the existing `recall-agency-child-theme` on a live WordPress architecture, the strategy is to implement modern web practices on top of the traditional CMS structure:

*   **CSS Architecture:** We will use modern vanilla CSS with variables (or Tailwind if preferred, but vanilla CSS is faster for pure custom styling without node environments on a live VPS sync). 
*   **Colors & Typography:** Deep blacks, metallic silvers, glowing node greens, and high-tech purples. Clean, wide sans-serif fonts (e.g., Space Grotesk or Inter).
*   **Animations:** 
    *   **GSAP (GreenSock):** For scroll-triggered animations (fade-ins, sliding data nodes).
    *   **GSAP ScrollTrigger:** To link the central 3D infrastructure graphic (either a Spline embed, a lightweight Three.js canvas, or a scroll-bound video/image sequence) directly to the user's scrollbar.

## 3. Proposed Changes

### Local Workspace: `/Users/phil/Documents/Vaults/SystemMac/20_Projects/Active/websites redesign/recall-agency.com/recall-agency-child-theme/`

#### `style.css`
*   Add brand CSS variables (colors, fonts).
*   Add base styling for the new dark-mode layout, glassmorphism elements, and glowing buttons.

#### `functions.php`
*   Enqueue GSAP and ScrollTrigger CDN links safely.
*   Enqueue a new custom JavaScript file for the animation logic.

#### `customscript.js` (or a new `animations.js`)
*   Initialize GSAP ScrollTrigger.
*   Write the timeline logic that animates the hero elements and the data center graphics as the user scrolls down the page.

#### Templates (e.g., `front-page.php` or `header.php`)
*   We will need to inject or override the HTML structure of the hero section so it supports our new 3D/video container and layout requirements. *(Will need to check how the current theme builds the homepage — whether it uses Elementor blocks or pure PHP).*

## 4. User Review Required

> [!IMPORTANT]  
> **Animation Asset:** To achieve the exact look of the images you uploaded (server racks, data grids), the absolute best approach is to use a 3D asset tool like **Spline (spline.design)** or a **Lottie** file. 
> 
> *   Do you already have animated files/videos/Spline URLs for these graphics, or would you like me to try and build a CSS/JS approximation of a glowing data grid? 
> *   The current theme uses Elementor. Do you want me to write pure PHP templates to override the homepage, or do you want to build the structure in Elementor and have me write the custom CSS/JS to animate it?

## 5. Verification Plan
*   Run the custom CSS/JS locally.
*   Use `rsync` to sync the child theme to Hostinger's `v2.recall-agency.com`.
*   Verify the scroll animations trigger correctly on both desktop and mobile devices without performance lag.
