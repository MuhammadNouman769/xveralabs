from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
   # path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact, name='contact_us'),
    path('services/', views.services, name='services'),
    path('projects/', views.projects, name='projects'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('blogs/', views.blogs, name='blogs'),
    path('blog-single/', views.blog_single, name='blog_single'),
    path('case-studies/', views.case_studies, name='case_studies'),
    path('faqs/', views.faqs, name='faqs'),
    path('terms-conditions/', views.term_condition, name='term_condition'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('sqa/', views.sqa, name='sqa'),
    path('web-development/', views.web_dev, name='web_dev'),
    path('product-development/', views.product_dev, name='product_dev'),
    path('dev-ops/', views.devops, name='dev_ops'),
    path('staff-augmentation/', views.staff_aug, name='staff_aug'),
   # path('about/leadership-&-team/', views.leadship, name='leadership-&-team'),
    path('coming-soon/', views.coming, name='coming'),
    path('about-us/why-choose-us/', views.why_choose_us, name='why_choose_us'),
    path('about/careeer/', views.careeer, name="careeer"),
    path('about/art/', views.articial_detail, name="careeer")
    
]