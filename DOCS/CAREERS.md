CAREERS: setup
1) Copy backend/apps/careers/ into your project's apps/ folder.
2) settings.py
     INSTALLED_APPS += ["apps.careers"]
     CAREERS_NOTIFY_EMAIL = "xveralabs@gmail.com"     # HR gets an email for every application
   (EMAIL_* and DEFAULT_FROM_EMAIL are the same ones you already set for the contact app)
3) Root urls.py:  path("", include("apps.careers.urls"))
   Remove your OLD careers route/view (in about_us) so the URL name 'careeers' exists only once.
4) Templates: copy templates/careers/*.html to your templates/careers/ folder
   (change template_name in views.py if your path differs).
   Static: static/careers.css -> static/css/pages/careers.css ; static/careers-1.js -> static/js/pages/careers-1.js
   Delete the old about-careers.css, about-careers-1.js and the old careers template.
5) CVs are saved OUTSIDE the public media folder: BASE_DIR/private_media/
   Add  private_media/  to .gitignore, and never serve that folder from nginx or whitenoise.
   Staff download CVs from the dashboard (Career applications > Download CV).
6) python manage.py makemigrations careers && python manage.py migrate
7) Sample data (optional, for testing): python manage.py seed_careers
   They are SAMPLE roles. Edit, close or delete them in the dashboard and keep only the roles you really hire for.
8) Dashboard: Career positions (add a role, tick "Is open", pick type "Internship" for internships)
              Career applications (status, notes, CSV export)
9) Replace header/header.html (a new "Internships" link was added under Careers).