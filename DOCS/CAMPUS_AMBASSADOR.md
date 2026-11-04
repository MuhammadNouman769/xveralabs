CAMPUS AMBASSADOR: setup
1) Copy backend/apps/campus_ambassador/ into your project's apps/ folder.
2) settings.py
     INSTALLED_APPS += ["apps.campus_ambassador"]
     CAMPUS_NOTIFY_EMAIL = "xveralabs@gmail.com"      # optional; falls back to PARTNER_NOTIFY_EMAIL
3) Root urls.py:  path("", include("apps.campus_ambassador.urls"))
   Remove your OLD campus ambassador route/view (in about_us) so the name 'campus_ambassador_program' exists only once.
4) Template: templates/campus/campus-ambassador-program.html (change template_name in views.py if your path differs)
   Static: static/campus-ambassador-program.css -> static/css/pages/campus-ambassador-program.css
           static/campus-ambassador-program-1.js -> static/js/pages/campus-ambassador-program-1.js
5) python manage.py makemigrations campus_ambassador && python manage.py migrate
6) Sample content (optional): python manage.py seed_campus
   It creates a cohort and sample benefits, steps, responsibilities and FAQs. Edit them in the admin.
7) Admin: Campus Ambassador > Cohorts (open/close applications, dates, term, hours)
          Campus Ambassador > Program items (benefits, steps, responsibilities, FAQs)
          Campus Ambassador > Stories (add REAL quotes later; the section appears only when one is published)
          Campus Ambassador > Ambassador applications (status, notes, CSV export)