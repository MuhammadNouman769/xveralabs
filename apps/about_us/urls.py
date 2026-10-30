from django.urls import path
from . import views
from .views import (
    CompanyView,
    why_choose_us,
    careeers,
    life_at_xvera_labs,
    PeopleView,
    PeopleAnchorRedirect,
    campus_ambassador_program
)       
urlpatterns = [
    # company url
    path('company/', CompanyView.as_view(), name='about-us'),
    # why choose us
    path('why-choose-us/',why_choose_us, name='why_choose_us'),
    # join xvera labs    
    path('join-xvera-labs/careeers/',careeers, name="careeers"), 
    path('join-xvera-labs/life-at-xveralabs/', life_at_xvera_labs, name='life_at_xvera_labs'),
   
    path("people/", views.PeopleView.as_view(), name="people"),

    # the three old names keep working (menu links, footer, bookmarks):
    path("employee-success/",           views.PeopleAnchorRedirect.as_view(anchor="success"),   name="employee_success"),
    path("benefits/",                   views.PeopleAnchorRedirect.as_view(anchor="benefits"),  name="benefits"),
    path("diversity-equity-inclusion/", views.PeopleAnchorRedirect.as_view(anchor="inclusion"), name="diversity-equity-inclusion"),


    path('join-xvera-labs/campus-ambassador-program/',campus_ambassador_program, name="campus_ambassador_program"),
    
]