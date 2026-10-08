# 🌿 eco_libra — Forum & Social Platform built on Django

> **Developed by [@x90q](https://github.com/x90q)**

### 📌 About The Project

**eco_libra** is an ongoing personal project aimed at building a full-featured forum and social platform from the ground up.

At this moment I am developing the entire application independently - writing the backend logic in Python/Django and building the frontend layout with HTML/CSS from scratch. This repository tracks the real-time development process step-by-step as the platform evolves from a clean slate into a complete social forum.

It serves as a transparent build log showcasing a hands-on, full-stack approach to web development and the step-by-step evolution of both myself and the project.

---
### Preview
<p align="center">
<img width="1427" height="723" alt="Снимок экрана 2026-09-30 в 21 07 59" src="https://github.com/user-attachments/assets/6efd8492-8680-46ad-817e-ab26c66151f9" />

<img width="1423" height="727" alt="Снимок экрана 2026-09-30 в 20 54 16" src="https://github.com/user-attachments/assets/4386d425-95b2-4a37-b08f-1587404e89b2" />

<img width="1427" height="723" alt="Снимок экрана 2026-09-30 в 20 54 53" src="https://github.com/user-attachments/assets/fde2c8cb-4e1f-4e56-afe4-60f5d08d1627" />
</p>

---

### 🛠 Tech Stack & Dependencies

* **Core Framework & Language:**
  * **Python 3.11+** & **Django 6.1+** - Main full-stack framework powering backend logic, ORM, views, and DTL templates.

* **Authentication & Social Auth:**
  * **Email & Google OAuth2 Integration** - Dual authentication flow via native Django auth and Google API over HTTPS.
  * `django-extensions` & `Werkzeug` - Advanced development server tools for HTTPS local debugging (`runserver_plus`).

* **Database & Search:**
  * **PostgreSQL** - Required relational database powering full-text search and trigram similarity support.
  * `psycopg` (v3) / `psycopg2-binary` - High-performance database adapters connecting Django to PostgreSQL.

* **Content & Features:**
  * `django-taggit` - Flexible tagging framework for organizing forum posts, categories, and tag-based recommendations.
  * `django.contrib.sitemaps` & `django.contrib.sites` - Sitemap generation and domain site management for OAuth callbacks.
  * `Pillow` - Image handling for user avatars.

* **Configuration & Security:**
  * `python-decouple` - Environment variable manager for secure decoupling of credentials (`SECRET_KEY`, OAuth keys, DB configs, SMTP).

* **Frontend:**
  * **HTML5 & CSS3** - Custom, hand-crafted responsive templates and styles built from scratch.

* **Tooling & Environment:**
  * **Git & GitHub** - Version control and project evolution tracking.
  * **Virtualenv (`venv`)** & `pip` - Isolated environment management and dependency tracking (`requirements.txt`).

---

### Key Features

* **Multi-Method Authentication:** Authentication via email address alongside social sign-in via **Google OAuth2**.
* **Strict Email Uniqueness:** Validation preventing users from registering or changing their profile email to an address already registered on the platform.
* **User Profile Statistics:** Profile pages displaying active post and comment counters with clickable links to inspect all posts or comments written by a specific user.
* **User-Generated Post Creation:** Initial draft implementation allowing registered users to create and publish posts directly on the site.
* **User Avatars:** Custom user avatar upload and media handling.
* **Post Sharing via Email:** Integrated SMTP configuration allowing users to share posts/content via email directly from the platform.
* **Comment System:** Interactive commenting functionality for discussion threads with text wrapping protections.
* **Advanced PostgreSQL Search:** Powered by PostgreSQL full-text search with **trigram similarity** for accurate and fuzzy content discovery.
* **Categorization & Tagging:** Organized content hierarchy using categories alongside `django-taggit` for tagging.
* **Similar Content Recommendations:** Dynamic post recommendations based on shared tags and overlapping topics.
* **Post Analytics:** Built-in view count tracking system for monitoring post popularity.
* **SEO Optimization:** Dynamic XML sitemap generation built with `django.contrib.sitemaps`.

---

### Roadmap

- [x] **Authentication & Profiles:** User registration, login, email uniqueness validation, and profile pages.
- [x] **User-Generated Content:** Post creation and management for registered users.
- [x] **OAuth Integration:** Social authentication support (Sign in with Google).
- [x] **Avatars & Profile Analytics:** User avatar handling and clickable post/comment statistics.
- [ ] **UI/UX Enhancement & Polishing:** Completing CSS styling for newly added UI elements, responsive layout refinements, and micro-interactions.
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
5. **Database Setup (PostgreSQL):**
   
   Create a local PostgreSQL database and enable the *pg_trgm* extension required for fuzzy/trigram search:
   ```bash
   CREATE DATABASE eco_libra_db;
   ```
6. **Configure environment variables:**

   Copy .env_example to .env and add your DB data:
   ```bash
   cp .env_example .env
   ```
   Make sure to include your GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET in .env if testing Google Login.
7. **Apply migrations & create superuser:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

8. **Django Sites Framework Setup (Admin Panel):**
   1. Log into Django Admin (`/admin/`).
   2. Go to Sites (`/admin/sites/site/`) and set the *Domain Name* to match your local setup for OAuth callbacks to work properly.

9. **Run development server:**
   For Google OAuth testing over local SSL:
   ```bash
   python manage.py runserver_plus --cert-file cert.crt
   ```
   (Or standard server without HTTPS):
   ```bash
   python manage.py runserver
   ```
10. **Access the Application & Admin Panel:**
   * **Main Blog/Platform:** *Open [https://127.0.0.1:8000/feed/](https://127.0.0.1:8000/feed/) in your browser to view the forum interface.*
   * **Admin Panel:** *Go to [https://127.0.0.1:8000/admin/](https://127.0.0.1:8000/admin/), log in using the superuser credentials created in Step 7, and add initial Categories and Posts to populate the site with test content.*
