# MOBVAP-MOBTEC Official Website

This is the official web application for the MOBVAP-MOBTEC science fair, a real-world project built for the event organizers. The platform serves as a central hub for information, event scheduling, photo/video galleries, and community interaction.



---
## Key Features

* **Fully Responsive Design:** A clean, mobile-first interface built with Tailwind CSS.
* **Dynamic Content Management:** All page content is managed through the Django admin panel.
* **Edition Archives:** A gallery system to showcase photos and videos from past events, with pagination.
* **Automated Media Pipeline:**
    * User-uploaded images and videos are stored in a cloud object storage bucket (Google Cloud Storage).
    * Video files are automatically processed with FFmpeg to create optimized versions and generate thumbnails.
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
## Local Setup & Installation

This project is fully containerized with Docker.

1.  **Clone the repository:**
    ```bash
    git clone [your-repo-url]
    cd [your-project-folder]
    ```
2.  **Create your `.env` file:**
    * Create a `.env` file in the root directory.
    * Add your `SECRET_KEY`, database credentials, and cloud service keys.

3.  **Build and run the containers:**
    ```bash
    docker-compose up --build -d
    ```
4.  **Run database migrations:**
    ```bash
    docker-compose exec web python manage.py migrate
    ```
5.  **Create a superuser:**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
6.  The application will be available at `http://localhost`.
