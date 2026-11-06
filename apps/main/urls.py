from django.urls import path
from . import views
from apps.blogs import views as blog_views

urlpatterns = [
    path('', views.home, name='home'),
   # path('about-us/', views.about_us, name='about_us'),
    path('services/', views.services, name='services'),
    path('projects/', views.projects, name='projects'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('blogs/', views.blogs, name='blogs'),
    path('resources/', blog_views.resource_index, name='resources'),
    path('resources/<slug:slug>/', blog_views.resource_detail, name='resource_detail'),
    path('blog-single/', views.blog_single, name='blog_single'),
    path('case-studies/', views.case_studies, name='case_studies'),
    path('case-studies/<slug:slug>/', views.industry_case_study, name='case_study_detail'),
    path('faqs/', views.faqs, name='faqs'),
    path('terms-conditions/', views.term_condition, name='term_condition'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('site-map/', views.site_map, name='site_map'),
    path('sqa/', views.sqa, name='sqa'),
    path('web-development/', views.web_dev, name='web_dev'),
    path('product-development/', views.product_dev, name='product_dev'),
    path('dev-ops/', views.devops, name='dev_ops'),
    path('staff-augmentation/', views.staff_aug, name='staff_aug'),
   # path('about/leadership-&-team/', views.leadship, name='leadership-&-team'),
    path('coming-soon/', views.coming, name='coming'),
    path('art/', views.articial_detail, name="art"),
    
]