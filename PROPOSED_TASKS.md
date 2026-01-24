Visual Refactoring Plan 
Executive Summary
The application is functional but lacks a cohesive, premium visual identity. It relies on a basic bright blue palette and standard layouts. The requirement to display numerous partner logos in the footer is currently handled inelegantly, creating a heavy visual bottom. The use of |safe tags for CMS content necessitates the use of the Tailwind Typography plugin to ensure rich text renders beautifully without custom CSS for every element.

Goal: Transform the site into a professional, academic, and modern platform using the Slate/Blue palette, gradients, and sophisticated component patterns, while respecting client constraints.

🏗️ Phase 1: Foundation & Global Elements
1.1. Upgrade Alpine.js & Global Typography
Priority: Critical

Current State: Uses outdated Alpine v2. Fonts (Poppins/Inter) are linked but not correctly applied globally in Tailwind config, leading to generic system fonts.

Proposed Change:

Switch to Alpine.js v3 in <head>.

Configure tailwind.config.js to use Poppins for headings and Inter for body text by default.

Rationale: Essential for modern interactivity (mobile menu animations) and establishing the premium feel instantly across all pages.

1.2. Navbar Modernization
Priority: High

Current State: Solid bright blue bar. Functional but basic.

Proposed Change:

Change background to a deep academic blue (bg-blue-900) or a dark slate for a more official feel.

Implement proper mobile hamburger menu using Alpine v3 transitions.

Ensure navigation links have clear hover states (e.g., lightening the text or a subtle underline).

1.3. The "Wall of Logos" Footer Strategy
Priority: High (Client Requirement)

Current State: A massive, unstructured block of logos manually added to the bottom of pages on a bright blue background. It is visually overwhelming.

Proposed Change:

Structure: Create a dedicated footer.html component included once in base.html.

Design: Change the background to a dark slate (bg-slate-900) to make it recede visually. Use CSS Grid to organize the logos into neat, smaller rows with consistent grayscale styling, perhaps revealing color on hover. Add standard footer links (Contact, Privacy) below the logos.

Rationale: Meets the client requirement without ruining the page aesthetics. Makes maintenance far easier.

1.4. CMS Content Handling (|safe)
Priority: High

Current State: Raw HTML is rendered via |safe, inheriting base styles, which often looks unstyled.

Proposed Change:

Install @tailwindcss/typography plugin.

Wrap all areas using |safe (like on the Homepage or About sections) with a container class: <div class="prose prose-slate max-w-none">...</div>.

Rationale: Automatically makes standard HTML (tables, lists, bold text, paragraphs) look professional without writing custom CSS for dynamic content.

🏠 Phase 2: Landing Page (Home)
2.1. Hero Section Overhaul
Priority: High

Current State: A loose collection of logos and title. No visual impact.

Proposed Change: Implement a full-width Hero section with a professional academic gradient background, clear hierarchy for the title, and the video embedded in a stylish, shadowed container.

📄 Phase 3: Content Pages Refactoring
3.1. Buttons & "Regulamento" Page
Priority: Medium

Current State: Giant, basic blue buttons.

Proposed Change: Replace all generic buttons with the Design System's "Primary Button" pattern (gradient or deep blue, shadow, hover lift effect).

3.2. Editions & Gallery Cards
Priority: Medium

Current State: Basic cards. "Fotos" and "Videos" links are barely visible text.

Proposed Change:

Add depth to cards with subtle borders (border-slate-200) and hover shadows.

Turn the "Fotos/Videos" links into actual secondary buttons or clear icons so they look actionable.

3.3. Photo Gallery Layout
Priority: Medium

Current State: A basic, somewhat dated grid of thumbnails.

Proposed Change: Implement a modern, clean CSS Grid layout with consistent aspect ratios and rounded corners for a more polished look.

3.4. Comments Section styling
Priority: Low

Current State: Wide form fields and flat comment display cards.

Proposed Change: Constrain the form width for better readability. Style form inputs with focus states (blue ring). Give comment cards a slight background color distinction (bg-slate-50) and softer shadows.

