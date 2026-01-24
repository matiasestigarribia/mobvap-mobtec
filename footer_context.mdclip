
# System Prompt: MOBVAP Frontend Architect

## 1. Identity & Role

You are the **Lead Frontend Architect** for the MOBVAP-MOBTEC platform. You are an expert in **Django Template Language (DTL)**, **Tailwind CSS**, and **Alpine.js**.

**YOUR PRIME DIRECTIVE:** You are responsible **ONLY** for the Visual Layer (HTML/CSS/JS).
**⛔ STRICT PROHIBITION:** You must **NEVER** modify backend logic.

* Do NOT touch `views.py`, `models.py`, `urls.py`, `serializers.py`, or `admin.py`.
* Do NOT change variable names passed from the context.
* Do NOT alter business logic inside `{% if %}` or `{% for %}` tags (only style them).

If a task requires backend changes, you must explicitly state: *"I cannot fulfill this request as it requires backend logic modification. I strictly operate on the frontend layer."*

## 2. Design Philosophy (The "Vibe")

The MOBVAP platform represents a strategic partnership between **UNIP**, **CIEBP**, and the **State Education Department**. The design must reflect:

* **Professionalism:** Clean, academic, and trustworthy.
* **Innovation:** Modern UI patterns, subtle gradients, and smooth transitions.
* **Accessibility:** High contrast, readable typography, and semantic HTML.
* **Mobile-First:** The site must look perfect on smartphones (students' primary device).

## 3. Tech Stack & Tools

* **Templating:** Django Template Language (DTL) - *Mastery required.*
* **Styling:** Tailwind CSS (v3.0+). Use utility classes for everything.
* **Interactivity:** Alpine.js (for dropdowns, mobile menus, modals). **No React/Vue.**
* **Icons:** Heroicons (SVG inline).

## 4. Visual Guidelines (Design System)

### Color Palette (Tailwind Mapping)

* **Primary (Brand):** `blue-700` to `indigo-900` (Official/Academic).
* **Secondary (Accent):** `emerald-500` (Success/Growth) and `amber-500` (Warning/Attention).
* **Backgrounds:** `slate-50` (Light mode base), `white` (Cards).
* **Text:** `slate-900` (Headings), `slate-600` (Body), `slate-400` (Muted).

### Component Patterns

**1. Cards (Projects/News)**

```html
<div class="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300 border border-slate-200 overflow-hidden">
    </div>

```

**2. Primary Button**

```html
<button class="px-6 py-2.5 bg-blue-700 hover:bg-blue-800 text-white font-medium rounded-lg transition-colors focus:ring-4 focus:ring-blue-300">
    Action
</button>

```

**3. Form Inputs**

```html
<input type="text" class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">

```

## 5. Workflow & Rules

### Rule #1: Preserve Context

When refactoring a file (e.g., `list_projects.html`), you must **KEEP** all existing Django Tags (`{% url %}`, `{{ variable }}`). You are applying a "skin" over the existing skeleton. Do not break the skeleton.

### Rule #2: Semantic Structure

* Use `<header>`, `<main>`, `<section>`, `<footer>`.
* Use `<h1 class="text-3xl font-bold text-slate-900">` for page titles.

### Rule #3: Tailwind Best Practices

* Don't use `@apply` in CSS files unless strictly necessary. Keep utility classes in HTML.
* Use `flex` and `grid` for layouts. Avoid fixed widths (`w-500px`).

### Rule #4: Documentation First

Before starting a task, always read the `PRD.md` and `TASKS.md` files in the root directory to understand the specific requirements for that component.

## 6. Interaction Protocol

When you receive a task (e.g., *"Refactor the Navbar"*):

1. **Analyze:** Read the current HTML code. Identify the Django context variables used.
2. **Plan:** Decide which Tailwind classes apply to the new design.
3. **Execute:** Rewrite the HTML structure applying the new classes, **embedding Alpine.js** if interactivity is needed (e.g., for the hamburger menu).
4. **Verify:** Check if all Django tags (`{% if user.is_authenticated %}`) are still present and in the correct logical place.

---

### Example of Good Refactoring

**Input (Old HTML):**

```html
<div class="menu">
    <ul>
        <li><a href="{% url 'home' %}">Home</a></li>
        {% if user.is_authenticated %}
            <li>Logout</li>
        {% endif %}
    </ul>
</div>

```

**Output (Your Work):**

```html
<nav class="bg-white shadow-sm border-b border-slate-200" x-data="{ open: false }">
    <div class="container mx-auto px-4">
        <div class="flex justify-between items-center h-16">
            <a href="{% url 'home' %}" class="text-xl font-bold text-blue-900">MOBVAP</a>
            
            <div class="hidden md:flex space-x-8">
                <a href="{% url 'home' %}" class="text-slate-600 hover:text-blue-700 transition-colors">Home</a>
                {% if user.is_authenticated %}
                    <a href="{% url 'logout' %}" class="px-4 py-2 text-red-600 border border-red-200 rounded-lg hover:bg-red-50">Logout</a>
                {% endif %}
            </div>
        </div>
    </div>
</nav>

```# Refactoring Roadmap: Visual Upgrade

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
- [ ] **4.2. Console Check:** Verify zero Alpine.js errors in DevTools.{% load static %}

<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@400;500;700&display=swap" rel="stylesheet"/>

    <link href="{% static 'css/output.css' %}" rel="stylesheet">
    
    <title>{% block title %}MOBVAP-MOBTEC{% endblock title %}</title>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body class="bg-slate-50 flex flex-col min-h-screen">
    
    <header class="sticky top-0 z-50 w-full">
        {% include 'components/navbar.html' %}
    </header>
    {% if messages %}
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 mt-4">
            {% for message in messages %}
                <div x-data="{ show: true }" x-show="show"
                class="flex justify-between items-center p-4 rounded-md mb-4
                {% if message.tags == 'success' %} bg-green-100 border border-green-400 text-green-700 {% endif %}
                {% if message.tags == 'error' %} bg-red-100 border border-red-400 text-red-700 {% endif %}">
        
        <span>{{ message }}</span>
        
        <button @click="show = false" class="ml-4 text-xl font-bold">&times;</button>
    </div>
    {% endfor %}
</div>
{% endif %}

    <main class="flex-grow mt-20">
    {% block content %}
    {% endblock content %}
    </main>
 
    {% include 'components/footer.html' %}
    
    <script src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
</body>
</html>
{% load static %}
<footer class="bg-blue-600 text-white py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">

        <div class="mb-12 text-center">
            <h3 class="text-2xl font-bold mb-8">Realização</h3>
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-8 items-center justify-center">
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/realizacao/logo_secretaria_da_educacao.png' %}" alt="Logo Secretaria da Educação" class="h-16 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/realizacao/logo_ure_sjc.png' %}" alt="Logo Ure SJC" class="h-16 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/realizacao/logo_ciebp.png' %}" alt="Logo Centro de Inovação da Educação Básica Paulista" class="h-16 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/realizacao/logo_unip.png' %}" alt="Logo Universidade Paulista " class="h-16 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/realizacao/logo_jc.png' %}" alt="Logo E. E. João Cursino" class="h-16 object-contain">
                </div>
            </div>
        </div>
        
        <div class="text-center">
            <h3 class="text-2xl font-bold mb-8">Apoio</h3>
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-8 items-center">
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_marinha_do_brasil.png' %}" alt="Logo Marina do Brasil" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_dcta.png' %}" alt="Logo DCTA" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_galileo_galilei.png' %}" alt="Logo Instituto Galileo Galilei" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_parque_tecnologico_santos.png' %}" alt="Logo Parque Tecnológico Santos" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_prefeitura_santos.png' %}" alt="Logo Prefeitura Santos" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_cultivotech.png' %}" alt="Logo  Cultivotech" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_nunes.png' %}" alt="Logo Nunes Projetos Incentivados" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_mf.png' %}" alt="Logo Mf Náutica" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_troglio_sports.png' %}" alt="Logo Troglio Sports" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_bse.png' %}" alt="Logo Grupo Bse" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_modirum.png' %}" alt="Logo Modirum Gespi" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_thermas_do_vale.png' %}" alt="Logo Thermas do Vale" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_robo.png' %}" alt="Logo Tesla Robótica Educacional" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_quero_aprender.png' %}" alt="Logo Canal Quero Aprender" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_va.png' %}" alt="Logo VA" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_thiago_gama.png' %}" alt="Logo Thiago Gama Especializações" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_teatro_sergio.png' %}" alt="Logo Teatro Sergio Mamberti" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_instituto_digital.png' %}" alt="Logo Instituto Digital" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_dsa.png' %}" alt="Logo DSA" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_sao_francisco.png' %}" alt="Logo Mercadinho São Francisco" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_sirvase_bem.png' %}" alt="Logo Sirva-se Bem 2" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_mg_acai.png' %}" alt="Logo Mh, Açaí e frutas congeladas" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_kamila_dias.png' %}" alt="Logo Kamila Dias" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_silvio_del_duca.png' %}" alt="Logo Silvio Del Duca Imagens" class="h-14 object-contain">
                </div>
                <div class="flex justify-center">
                    <img src="{% static 'images/logos/apoio/logo_vincula_martech.png' %}" alt="Logo Vínculo Martech" class="h-14 object-contain">
                </div>
            </div>
        </div>

    </div>
    
    <div class="border-t border-blue-400 mt-12 pt-8 text-center text-sm">
        <p>&copy; 2025 MOBVAP-MOBTEC. All Rights Reserved.</p>
        <p>Developed and Designed by Matias Pedro Estigarribia</p>
    </div>
</footer>
    {% extends "base.html" %}
{% load static %}


{% block title %}
    
        {{ home_content.home_title }} - MOBVAP-MOBTEC 
    
{% endblock title %}

{% block content %}

    <section class="flex flex-col items-center justify-center pt-2 pb-12 px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center w-full max-w-4xl mx-auto">
            <img src="{% static 'images/general/mobvap-logo1.png' %}" alt="MOBVAP Logo" class="h-32 w-32 object-contain">
            <h1 class="text-4xl sm:text-5xl font-bold text-[var(--dark-navy)] mb-6 text-center">{{ home_content.home_title }}</h1>
            <img src="{% static 'images/general/mobtec-logo1.png' %}" alt="MOBTEC Logo" class="h-32 w-32 object-contain">
        </div>
        <div class="w-full max-w-4xl mx-auto border-4 border-blue-300 rounded-lg overflow-hidden shadow-lg">
        <div class="aspect-video">
            <iframe class="w-full h-full" 
                    src="{{ home_content.youtube_url }}" 
                    title="YouTube video player" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                    allowfullscreen
                    referrerpolicy="strict-origin-when-cross-origin">
            </iframe>
        </div>
</div>
    </section>

    <section class="py-12 px-4 sm:px-6 lg:px-8 bg-blue-50">
    <div class="max-w-4xl mx-auto text-center">
        <h2 class="text-3xl font-bold text-[var(--dark-navy)] mb-4">{{ home_content.block_content1_title }}</h2>
        
        <p class="text-lg text-[var(--dark-navy)] leading-relaxed font-['Inter']">{{ home_content.block_content1_text }}</p>
    </div>
    </section>

    <section class="py-16 px-4 sm:px-6 lg:px-8">
        <div class="max-w-4xl mx-auto">
            <h2 class="text-3xl font-bold text-center text-[var(--dark-navy)] mb-8">{{ home_content.block_content2_title }}</h2>
            <p class="text-lg text-[var(--dark-navy)] leading-relaxed font-['Inter']">{{ home_content.block_content2_text }}</p>
        </div>
    </section>

    <section>
        <div class="max-w-4xl mx-auto">
            <h2 class="text-3xl font-bold text-center text-[var(--dark-navy)] mb-8" >{{ home_content.schedule_table_title }} </h2>
             <div class="overflow-x-auto rounded-lg shadow-md ">
                {{ home_content.schedule_table_html|safe }}
        </div>
        </div>
    </section>

    <section class="py-12 px-4 sm:px-6 lg:px-8 bg-blue-50">
        <div class="max-w-4xl mx-auto">
            <h2 class="text-3xl font-bold text-center text-[var(--dark-navy)] mb-8">{{ home_content.block_content3_title }}</h2>
            <p class="text-lg text-[var(--dark-navy)] leading-relaxed font-['Inter']">{{ home_content.block_content3_text|safe }}</p>
        

        </div>
    </section>

    <section class="py-16 px-4 sm:px-6 lg:px-8">
        <div class="max-w-4xl mx-auto">
            <h2 class="text-3xl font-bold text-center text-[var(--dark-navy)] mb-8">{{ home_content.block_content4_title }}</h2>
            <p class="text-lg text-[var(--dark-navy)] leading-relaxed font-['Inter']">{{ home_content.block_content4_text|safe }}</p>
           
        </div>
    </section>

{% endblock content %}
const { fontFamily } = require('tailwindcss/defaultTheme')

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      './**/*.html'
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Inter"', ...fontFamily.sans],
        headings: ['"Poppins"', ...fontFamily.sans],
      },
      colors: {
        slate: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
        blue: {
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        indigo: {
          900: '#312e81',
        },
        emerald: {
          500: '#10b981',
        },
        amber: {
          500: '#f59e0b',
        },
      }
    },
  },
  plugins: [],
}