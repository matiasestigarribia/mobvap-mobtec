# AUDIT INSTRUCTION: Visual Design Review

## Objective
Do NOT write any code yet. Your goal is to act as a **Design Consultant**. You must analyze the current project structure and HTML templates provided in the context to identify visual weaknesses, inconsistencies, and opportunities for modernization based on the "High-End Science Fair" aesthetic defined in `agent_frontend.md`.

## Input Analysis
1.  **Navbar:** Analyze the current implementation. Is the Alpine.js state logic clean? Are the mobile transitions smooth? Does it match the new color palette?
2.  **Typography:** Look for consistency in headings (`h1`, `h2`) and body text.
3.  **Spacing:** Check for inconsistent margins/paddings (e.g., mixing `p-4` with `p-10`).
4.  **Color Usage:** Identify hardcoded colors or deviation from the new Slate/Blue theme.
5.  **UX Patterns:** Analyze buttons and cards. Are they clickable? Do they have hover states?

## Output Requirement
Generate a file named `PROPOSED_TASKS.md` containing a prioritized list of refactoring tasks.
Each task must have:
- **Priority:** [High/Medium/Low]
- **Current State:** A brief description of what you see now.
- **Proposed Change:** What specific Tailwind classes or components should be used.
- **Rationale:** Why this change improves the project (e.g., "Improves readability", "Standardizes branding").

## Example Output Format
### 1. Navbar Modernization
- **Priority:** High
- **Current State:** Basic blue background with standard links. Hamburger menu exists but uses old toggle logic.
- **Proposed Change:** Switch to `bg-slate-900` with a blur effect (`backdrop-blur`). Update Alpine.js to use `x-transition`.
- **Rationale:** Matches the new "Premium" look and feels smoother on mobile.