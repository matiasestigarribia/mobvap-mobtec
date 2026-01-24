# Refactoring Roadmap: Visual Upgrade

This document outlines the step-by-step plan to modernize the MOBVAP-MOBTEC frontend. The Agent must strictly follow this order to ensure structural integrity before applying cosmetic polish.

## 🏗️ Phase 1: Foundation (Critical)
*Objective: Establish the Design System, fix dependencies, and modernize global layout elements.*

- [*] **1.1. Alpine.js Upgrade:**
    - Replace Alpine.js v2 CDN with v3 in `base.html` `<head>` (use `defer`).
    - Ensure `viewport` meta tag is correct.
    - Consolidate Google Fonts links (Poppins/Inter).

- [*] **1.2. Global Typography Config:**
    - Update `tailwind.config.js` to set 'Poppins' as the default for headings and 'Inter' for body.
    - Define the new color palette in config (e.g., extend `colors` with `slate` and specific brand blues if needed).

- [*] **1.3. Navbar Modernization:**
    - Refactor `components/navbar.html`.
    - Change background to `bg-blue-900` (Academic Blue) or Dark Slate.
    - Implement a proper mobile hamburger menu using Alpine.js v3 (`x-data`, `x-transition`).
    - Ensure links have clear hover states (e.g., `hover:text-blue-200`).

- [ ] **1.4. Footer Architecture:**
    - Create/Refactor `components/footer.html` to be included *once* in `base.html`.
    - Move the "Wall of Logos" into this component.
    - Style: Use a Dark Slate (`bg-slate-900`) background to reduce visual weight.
    - Layout: Organize logos using CSS Grid (`grid-cols-4 md:grid-cols-8`) with grayscale filtering that reveals color on hover (`grayscale hover:grayscale-0`).

- [ ] **1.5. CMS Rich Text Support:**
    - **Action for User:** Install `@tailwindcss/typography` via npm.
    - **Action for Agent:** Add the plugin to `tailwind.config.js`.
    - Wrap `|safe` content areas in `base.html` or `home.html` with `<div class="prose prose-slate max-w-none">`.

## 🏠 Phase 2: Landing Page (Home)
*Objective: Create a "Wow Factor" first impression.*

- [ ] **2.1. Hero Section:**
    - Refactor the top section of `home.html`.
    - Implement a full-width container with a subtle gradient (`bg-gradient-to-r from-blue-900 to-indigo-900`).
    - Style the Youtube Video container with a "window frame" look and deep shadow (`shadow-2xl`).

- [ ] **2.2. Content Blocks:**
    - Standardize all text sections.
    - Replace hardcoded colors with Tailwind utility classes (`text-slate-800` for headings, `text-slate-600` for body).
    - Ensure tables (Schedule) are wrapped in a rounded container with borders.

## 📄 Phase 3: Content Pages & Polish
*Objective: Standardize internal pages to match the new Home aesthetic.*

- [ ] **3.1. Button Standardization:**
    - Identify all large/blocky buttons (e.g., on "Regulamento" page).
    - Apply the Primary Button pattern: `bg-blue-700 hover:bg-blue-800 text-white shadow-sm rounded-lg`.

- [ ] **3.2. Editions & Cards:**
    - Refactor `editions.html`.
    - Add depth to cards: `border border-slate-200`, `rounded-xl`, `hover:shadow-md`.
    - Style "Fotos" and "Videos" links as distinct secondary buttons (outline style) or clear icons.

- [ ] **3.3. Photo Gallery Grid:**
    - Refactor `photos.html`.
    - Replace basic grid with a responsive Masonry-like layout or clean CSS Grid with consistent aspect ratios.
    - Add hover zoom effects on thumbnails (`group-hover:scale-105`).

- [ ] **3.4. Comments Section:**
    - Refactor the comments form to have a constrained max-width (readability).
    - Style inputs with `focus:ring-2 focus:ring-blue-500`.
    - Style individual comment cards with `bg-slate-50` and soft shadows.

## ✅ Phase 4: QA & Cleanup
- [ ] **4.1. Visual Regression:** Check for broken layouts on Mobile (375px).
- [ ] **4.2. Console Check:** Verify zero Alpine.js errors in DevTools.