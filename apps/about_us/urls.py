from django.urls import path
from .views import (
    CompanyView,
    why_choose_us,
    careeers,
    life_at_xvera_labs,
    diversity_equity_inclusion,
    employee_success,
    benefits
)       
urlpatterns = [
    # company url
    path('company/', CompanyView.as_view(), name='about-us'),
    # why choose us
    path('why-choose-us/',why_choose_us, name='why_choose_us'),
    # join xvera labs    
    path('join-xvera-labs/careeers/',careeers, name="careeers"), 
    path('join-xvera-labs/life-at-xveralabs/', life_at_xvera_labs, name='life_at_xvera_labs'),
    path('join-xvera-labs/diversity-equity-inclusion/', diversity_equity_inclusion, name='diversity-equity-inclusion'),
    path('join-xvera-labs/employee-success/',employee_success, name="employee_success"),
    path('join-xvera-labs/benefits/',benefits, name="benefits"),
    
]