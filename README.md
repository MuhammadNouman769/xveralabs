
# XVERA — Excellence in Versatile Technology & AI

Xvera Labs is a Django-based corporate website designed for a technology and consulting company. The project includes the main landing page, about section, services, projects, blogs, contact page, FAQ pages, and a modular app structure for future expansion.

## Features

- Home page and marketing landing page
- About Us section with company, culture, diversity, and career pages
- Service pages for consulting and advanced technology offerings
- Project and portfolio showcase pages
- Blog and case study pages
- FAQ, privacy policy, and terms pages
- Contact us page
- User authentication pages for sign in and sign up
- Django admin for content management
- Responsive template-based frontend with static media support

## Tech Stack

- Python 3.10+
- Django 6.0.6
- Django REST Framework
- SQLite (development database)
- Pillow for image handling
- HTML, CSS, and JavaScript templates

## Project Structure

```bash
xveralabs/
├── apps/
│   ├── about_us/
│   ├── blogs/
│   ├── contact/
│   ├── main/
│   ├── portfolio/
│   ├── projects/
│   ├── services/
│   ├── team/
│   ├── utils/
│   └── __init__.py
├── core/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── media/
├── static/
├── templates/
├── db.sqlite3
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Apps Overview

- apps.main: homepage and primary public pages
- apps.about_us: company history, culture, diversity, and team-related pages
- apps.services: consulting and technology service categories
- apps.projects: project or portfolio-related app structure
- apps.portfolio: portfolio data and views
- apps.contact: contact-related app
- apps.blogs: blog content area
- apps.utils: shared utility app
- apps.team: team-specific logic and models

## Website Pages / Routes

This project contains the following pages from the actual templates and URL configuration.

### Home / Main Pages

- / — Home page
- /contact-us/ — Contact page
- /services/ — Services overview
- /projects/ — Projects overview
- /signin/ — Sign in page
- /signup/ — Sign up page
- /blogs/ — Blog listing page
- /blog-single/ — Single blog page
- /case-studies/ — Case studies page
- /faqs/ — FAQ page
- /terms-conditions/ — Terms and conditions page
- /privacy-policy/ — Privacy policy page
- /coming-soon/ — Coming soon page

### About Pages

- /about-us/company/ — Company profile page
- /about-us/about/life-at-mn-solutions/ — Life at MN Solutions page
- /about-us/about/diversity-equity-inclusion/ — DEI page
- /about-us/why-choose-us/ — Why choose us page
- /about/careeer/ — Careers page

### Service Pages

#### Strategy & Consulting

- /services/strategy-and-consulting/
- /services/strategy_&_consulting/business-optimization-consulting/
- /services/strategy_&_consulting/product-strategy/
- /services/strategy_&_consulting/technology-strategy/
- /services/strategy_&_consulting/learning-and-development/

#### Advanced Technology

- /services/advanced-technology/
- /services/advanced-technology/robotic-process-automation/
- /services/advanced-technology/internet-of-things/
- /services/advanced-technology/blockchain/
- /services/advanced-technology/ar-vr/

#### Additional service pages

- /sqa/
- /web-development/
- /product-development/
- /dev-ops/
- /staff-augmentation/

### Template Files Included

The project templates include pages such as:

- templates/home/index.html
- templates/home/contact-us.html
- templates/home/services.html
- templates/home/projects.html
- templates/home/signin.html
- templates/home/signup.html
- templates/blogs/blog-grid.html
- templates/blogs/blog-single.html
- templates/home/case-studies.html
- templates/faqs/faqs.html
- templates/faqs/term_condition.html
- templates/faqs/privacy_policy.html
- templates/about/about.html
- templates/about/culture.html
- templates/about/diversity_equity_inclusion.html
- templates/about/why-choose-us.html
- templates/about/careers.html
- templates/services/sqa.html
- templates/services/web_development.html
- templates/services/product_dev.html
- templates/services/devops.html
- templates/services/staff-aug.html
- templates/services/strategy_&_consulting/*.html
- templates/services/advanced_technology/*.html
- templates/coming-soon.html

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/MuhammadNouman769/xveralabs.git

cd  xveralabs
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

For local development, copy `.env.example` to `.env`, generate a `DJANGO_SECRET_KEY`, then set `DJANGO_DEBUG=True`, `DJANGO_SERVE_MEDIA=True`, `DJANGO_DB_ENGINE=sqlite`, and `DJANGO_SECURE_SSL_REDIRECT=False` in `.env`. `DJANGO_SERVE_MEDIA` only enables Django's local media file route when debug is off; leave it disabled in production.

Generate a local secret with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

For deployment, configure the values from `.env.example` in your hosting provider instead of committing `.env`. Set the real domain names and trusted origins, provide the PostgreSQL credentials, and use HTTPS. Enable the proxy SSL header setting only when your trusted reverse proxy overwrites that header.

### 5. Prepare the application

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
```

The included `Procfile` starts the application with Gunicorn on the platform-provided port.

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## Admin Access

After creating the superuser, you can access Django admin here:

```text
http://127.0.0.1:8000/admin/
```

## Configuration Notes

- `.env.example` contains production-shaped settings; adapt it for local development as described above.
- `.env` is loaded automatically and ignored by Git. Never commit production secrets.
- The project uses SQLite by default for local development. Set `DJANGO_DB_ENGINE=postgresql` and the `DJANGO_DB_*` values for PostgreSQL.
- `DJANGO_DEBUG` defaults to `False`; set it to `True` only in your local `.env` when developing.
- Before deployment, configure `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, the database, and HTTPS settings in the hosting provider's environment.
- Run `python manage.py migrate`, `python manage.py collectstatic --noinput`, and `python manage.py check --deploy` during deployment.
- WhiteNoise serves collected static files. User-uploaded media should be stored on persistent/object storage or served by the hosting platform; the local `media/` directory is not durable on many hosts.
- Django's custom 404 and 500 responses use `templates/404.html` and `templates/500.html` when `DEBUG=False`.

## Notes

This project is a template-based Django website for a business/agency brand and is suitable for extension into a production-ready company website with CMS integration, contact form processing, and deployment optimization.

## License

