# 🌿 eco_libra — Forum & Social Platform built on Django

> **Developed by [@x90q](https://github.com/x90q)**

### 📌 About The Project

**eco_libra** is an ongoing personal project aimed at building a full-featured forum and social platform from the ground up.

At this moment I am developing the entire application independently - writing the backend logic in Python/Django and building the frontend layout with HTML/CSS from scratch. This repository tracks the real-time development process step-by-step as the platform evolves from a clean slate into a complete social forum.

It serves as a transparent build log showcasing a hands-on, full-stack approach to web development and the step-by-step evolution of both myself and the project.

---
### Preview
<p align="center">

<img width="1920" height="965" alt="1" src="https://github.com/user-attachments/assets/3ae91cc8-1f47-4a92-962b-3375b5fddd01" />

<img width="1920" height="967" alt="2" src="https://github.com/user-attachments/assets/8b6254d7-42f2-4c53-8e8b-db5e9868ed6d" />

<img width="1920" height="966" alt="3" src="https://github.com/user-attachments/assets/16fa109c-0299-4342-9487-94f9d2fd083a" />

<img width="1920" height="968" alt="5" src="https://github.com/user-attachments/assets/53ad0a25-58b0-4068-bf6d-2395d7f218a6" />

<img width="1920" height="966" alt="7" src="https://github.com/user-attachments/assets/7c30a395-ca73-4e1e-a1b3-9baca1e8d072" />

<img width="1920" height="966" alt="8" src="https://github.com/user-attachments/assets/9dcf28bd-0bb0-4f65-bab9-966772060971" />

</p>

---

### 🛠 Tech Stack & Dependencies

- **Core Framework & Language:**
  * **Python 3.11+** & **Django 6.1+** — Main full-stack framework powering backend logic, ORM, views, and DTL templates.

- **Authentication & Social Auth:**
  * **`django-allauth`** — Robust authentication suite handling user registration, login, and security flows.
  * **Google OAuth2 Integration** — Social sign-in via Google API over HTTPS.
  * `django-extensions` & `Werkzeug` — Advanced development server tools for HTTPS local debugging (`runserver_plus`).

- **Frontend & Styling:**
  * **Tailwind CSS** (`django-tailwind` & `pytailwindcss`) — Modern utility-first CSS framework powering the complete UI design.
  * `django-widget-tweaks` — Helper library for fine-tuning HTML form rendering.

- **Database & Search:**
  * **PostgreSQL** — Relational database powering full-text search and trigram similarity support.
  * `psycopg` (v3) / `psycopg-binary` — High-performance database adapters connecting Django to PostgreSQL.

- **Content & Features:**
  * `django-taggit` — Flexible tagging framework for organizing forum posts, categories, and tag-based recommendations.
  * `django.contrib.sitemaps` & `django.contrib.sites` — Sitemap generation and domain site management for OAuth callbacks.
  * `Pillow` — Image handling for user avatars.

- **Configuration & Security:**
  * `python-decouple` — Environment variable manager for secure decoupling of credentials (`SECRET_KEY`, OAuth keys, DB configs, SMTP).

- **Tooling & Environment:**
  * **Git & GitHub** — Version control and project evolution tracking.
  * **Virtualenv (`venv`)** & `pip` — Isolated environment management and dependency tracking (`requirements.txt`).
  
---
### Key Features

- **Multi-Method Authentication:** Secure authentication via email and social sign-in via **Google OAuth2** powered by `django-allauth`.
- **One-Time Code (OTP) Login:** Secure login option utilizing one-time verification codes for enhanced user access.
- **Customized `django-allauth` Templates:** Fully tailored authentication views and forms styled with Tailwind CSS, bypassing default component tags for complete layout and design control.
- **Email Verification & Security:** Mandatory or managed email address verification upon registration and robust account creation safeguards.
- **Secure Email Management & Uniqueness:** Protected email change workflow with confirmation steps and strict uniqueness validation preventing duplicate addresses across profiles.
- **Modern Tailwind UI:** Fully redesigned responsive interface utilizing Tailwind CSS utility classes and custom components.
- **User Profile Statistics:** Profile pages displaying active post and comment counters with clickable links to inspect all posts or comments written by a specific user.
- **User-Generated Post Creation:** Initial draft implementation allowing registered users to create and publish posts directly on the site.
- **User Avatars:** Custom user avatar upload and media handling.
- **Comment System:** Interactive commenting functionality for discussion threads with text wrapping protections.
- **Advanced PostgreSQL Search:** Powered by PostgreSQL full-text search with **trigram similarity** for accurate and fuzzy content discovery.
- **Categorization & Tagging:** Organized content hierarchy using categories alongside `django-taggit` for tagging.
- **Similar Content Recommendations:** Dynamic post recommendations based on shared tags and overlapping topics.
- **Post Analytics:** Built-in view count tracking system for monitoring post popularity.
- **SEO Optimization:** Dynamic XML sitemap generation built with `django.contrib.sitemaps`.

---

### Roadmap

- [x] **Authentication & Profiles:** User registration, login, email uniqueness validation, and profile pages via `django-allauth`.
- [x] **User-Generated Content:** Post creation and management for registered users.
- [x] **OAuth Integration:** Social authentication support (Sign in with Google).
- [x] **UI/UX Overhaul & Tailwind CSS:** Full migration to Tailwind CSS with responsive design and modern layouts.
- [x] **Avatars & Profile Analytics:** User avatar handling and clickable post/comment statistics.
- [ ] **Gamification & Reputation:** User rating and reputation system.
- [ ] **Security Hardening:** Implementing protection against common web threats and hardening Django settings for production.

---

### ⚙️ Local Setup Instructions

1. **Prerequisites:**
   * **Python 3.11+** installed on your system.
   * **PostgreSQL 13+** *(Required: The project strictly relies on native PostgreSQL Full-Text Search and Trigram Similarity extensions)*.

2. **Clone the repository:**
   ```bash
   git clone https://github.com/x90q/eco_libra.git
   cd eco_libra
   ```
3. **Set up virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
5. **Install Tailwind CSS & Node packages:**
   ```bash
   python manage.py tailwind install
   ```
   (This command automatically downloads and installs the required Node.js modules for the Tailwind theme).
   
6. **Database Setup (PostgreSQL):**
   
   Create a local PostgreSQL database and enable the *pg_trgm* extension required for fuzzy/trigram search:
   ```bash
   CREATE DATABASE eco_libra_db;
   ```
7. **Configure environment variables:**

   Copy .env_example to .env and add your DB data:
   ```bash
   cp .env_example .env
   ```
   Make sure to include your GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET in .env if testing Google Login.

8. **Apply migrations & create superuser:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

9. **Django Sites Framework Setup (Admin Panel):**
    
   * Log into Django Admin (`/admin/`).
   
   * Go to Sites (`/admin/sites/site/`) and set the *Domain Name* to match your local setup (`127.0.0.1:8000`) for OAuth callbacks to work properly.
      
10. **Run development server:**
    
    Terminal 1 (Tailwind CSS Watcher):
    ```bash
    python manage.py tailwind start
    ```
    Terminal 2 (Django Development Server with HTTPS support for Google OAuth):
    ```bash
    python manage.py runserver_plus --cert-file cert.crt
    ```
    (Or standard server without HTTPS: (`python manage.py runserver`)
    
11. **Access the Application & Admin Panel:**
   * **Main Blog/Platform:** *Open [https://127.0.0.1:8000/feed/](https://127.0.0.1:8000/feed/) in your browser to view the forum interface.*
   * **Admin Panel:** *Go to [https://127.0.0.1:8000/admin/](https://127.0.0.1:8000/admin/), log in using the superuser credentials created in Step 7, and add initial Categories and Posts to populate the site with test content.*
