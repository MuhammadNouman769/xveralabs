1) Copy backend/apps/contact_us/ into your project's apps/ folder.

2) settings.py
   INSTALLED_APPS += ["apps.contact_us"]

   # Email alert on every new inquiry (Gmail needs an App Password, not your normal password)
   EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
   EMAIL_HOST = "smtp.gmail.com"
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
   EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
   DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
   CONTACT_RECEIVER_EMAIL = "xveralabs@gmail.com"
   # In development use: EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

   TEMPLATES[0]["OPTIONS"]["context_processors"] += ["apps.contact_us.context_processors.chat_form"]
   (this gives the chat sidebar in base.html the same dropdown data as the contact page)

3) Root urls.py
   urlpatterns += [path("", include("apps.contact_us.urls"))]
   Remove your OLD contact_us path/view so the name 'contact_us' exists only once.

4) python manage.py makemigrations contact_us
   python manage.py migrate

5) Put home-contact-us.html and home-contact-us.css where the old ones were.
   If your template path differs, change template_name in views.py.

6) The chat sidebar posts to the URL name 'contact_chat' (JSON). base.html already uses it.
   After pulling these files run makemigrations/migrate again (new fields: budget, source, page_url).