# Product Requirements Document (PRD) - Visual Overhaul

## 1. Objective
Refactor the frontend visual layer of the MOBVAP-MOBTEC platform to achieve a "High-End Science Fair" aesthetic. The goal is to transition from a basic functional look to a modern, impactful, and responsive design without altering the backend logic (Django Views/URLs).

## 2. Tech Stack Constraints
- **Core:** Django Templates (HTML).
- **Styling:** Tailwind CSS (Utility-first).
- **Interactivity:** Alpine.js (Lightweight JS).
- **Icons:** Heroicons or FontAwesome (via CDN/SVG).
- **NO New Frameworks:** Do NOT introduce React, Vue, or heavy npm dependencies.

## 3. Design Guidelines (The "Vibe")
- **Theme:** Professional, Academic yet Innovative, Clean.
- **Color Palette:** Use the existing brand colors but refine typography and spacing.
- **Components:**
  - Cards should have subtle shadows and hover effects (`hover:scale-105`).
  - Inputs should use modern borders and focus rings (`ring-2`).
  - Buttons should be consistent (Primary, Secondary, Ghost).
- **Typography:** Ensure readability with good line-height (`leading-relaxed`) and hierarchy.

## 4. Scope of Work
1. **Global Layout:** Improve the base template (Navbar, Footer, Container widths).
2. **Landing Page:** Make the "Hero Section" impactful (large images, clear CTA).
3. **Gallery:** Improve the grid system for photos/videos.
4. **Forms:** Style standard Django forms with Tailwind classes (remove default browser look).

## 5. Success Metrics
- Mobile responsiveness is perfect.
- Lighthouse Accessibility score > 90.
- "Wow Factor" increased on the Home Page.