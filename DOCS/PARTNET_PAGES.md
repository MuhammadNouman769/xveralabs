PARTNER PAGES: setup
1) Copy backend/apps/partners/ over your apps/partners/ (models, forms, views, urls, admin, content.py, apps.py).
2) Copy templates/partners/*.html to your templates/partners/ folder (change template_name in views.py if your path differs).
3) Copy static/partners.css -> static/css/pages/partners.css  and  static/partners-1.js -> static/js/pages/partners-1.js
   Delete the old partners.css, partners-investors.css, partners-apply.css and partners-1.js, partners-investors-1.js, partners-apply-1.js.
4) settings.py: 'apps.partners' in INSTALLED_APPS, and for emails:
     PARTNER_NOTIFY_EMAIL = "xveralabs@gmail.com"
     (EMAIL_* and DEFAULT_FROM_EMAIL are the same ones you set for the contact app)
5) python manage.py makemigrations partners && python manage.py migrate
   If the migrate complains about existing rows, tell me the error.
6) Replace header/header.html and footer/footer.html (Partners menu now follows the page order).
7) Numbers shown on the site (5% commission, 5% profit share) are in PARTNER_TERMS at the top of views.py.