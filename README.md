# MOBVAP-MOBTEC Official Website

This is the official web application for the MOBVAP-MOBTEC science fair, a real-world project built for the event organizers. The platform serves as a central hub for information, event scheduling, photo/video galleries, and community interaction.



---
## Key Features

* **Fully Responsive Design:** A clean, mobile-first interface built with Tailwind CSS.
* **Dynamic Content Management:** All page content is managed through the Django admin panel.
* **Edition Archives:** A gallery system to showcase photos and videos from past events, with pagination.
* **Automated Media Pipeline:**
    * User-uploaded images and videos are stored in a cloud object storage bucket (Google Cloud Storage).
    * Video files are automatically generate thumbnails.
    * Thumbnails for both images and videos are processed with `django-imagekit` for uniform, high-quality previews.
* **Interactive Comment Wall:** A public comment section with a loading spinner on submission and success messages.
* **AI-Powered Content Moderation:** User-submitted comments are automatically analyzed by **Azure AI Content Safety**, and only approved comments are displayed.
* **RESTful API:** A complete API built with Django Rest Framework for programmatic access to all public data (editions, photos, videos, comments). Includes nested routes for edition-specific content.

---
## Tech Stack

* **Backend:** Django, Gunicorn
* **Frontend:** Tailwind CSS, Alpine.js
* **Database:** PostgreSQL
* **API:** Django Rest Framework (DRF)
* **Deployment:** Docker, Docker Compose, Nginx (as a reverse proxy)
* **Cloud Services:**
    * Google Cloud Platform (for hosting and storage)
    * Microsoft Azure AI (for content moderation)
* **Media Processing:** FFmpeg, `django-imagekit`

---
## 🚀 Getting Started (Local Development)

You can run this project locally in two ways: **Native (Fast)** or **Docker (Production Parity)**.

### Option 1: Native Setup (Recommended for Development)
The fastest way to start coding. Uses SQLite and local file storage automatically.

1.  **Clone the repository:**
    ```bash
    git clone [your-repo-url]
    cd [your-project-folder]
    ```

2.  **Create and activate a Virtual Environment:**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Migrations (Setup Database):**
    ```bash
    python manage.py migrate
    ```

5.  **Run the Server:**
    ```bash
    python manage.py runserver
    ```
    Access at `http://localhost:8000`.
    *Note: By default, the project runs in `dev` mode. To enable detailed error pages, create a `.env` file with `DEBUG=True`.*

---

### Option 2: Docker Setup (Simulating Production)
Use this to test the production stack (PostgreSQL, Nginx, Gunicorn) or if you don't want to install Python locally.

1.  **Create your `.env` file:**
    Copy the example file and adjust if necessary (Docker requires the DB credentials).
    ```bash
    cp .env.example .env
    ```

2.  **Build and run:**
    ```bash
    docker-compose up --build -d
    ```

3.  **Setup (First run only):**
    ```bash
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    ```

The application will be available at `http://localhost`.

---

## ⚙️ Configuration & Environments

The project switches behavior based on the `DJANGO_ENV` environment variable in `settings.py`.

| Feature | Development (`dev`) | Production (`prd`) |
| :--- | :--- | :--- |
| **Database** | SQLite (local file) | PostgreSQL |
| **Storage** | Local File System (`/media`) | Google Cloud Storage |
| **Security** | Relaxed (HTTP allowed) | Strict (HTTPS enforced, Secure Cookies) |
| **Static Files** | Served by Django | Served by GCS / Nginx |

To simulate production behavior locally (e.g., to test strict security or GCS upload):
1.  Set `DJANGO_ENV=prd` in your `.env`.
2.  Set `DEBUG=False`.
3.  Use Docker recommended.