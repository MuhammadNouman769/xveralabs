
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

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

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

- The project currently uses SQLite for local development.
- DEBUG is enabled in settings for local development.
- For production, update the following before deployment:
  - SECRET_KEY
  - DEBUG
  - ALLOWED_HOSTS
  - database configuration
  - static/media deployment settings

## Notes

This project is a template-based Django website for a business/agency brand and is suitable for extension into a production-ready company website with CMS integration, contact form processing, and deployment optimization.

## License

