from django.urls import path
from .views import TeamView, life_at_mn_solutions, diversity_equity_inclusion

urlpatterns = [
    path('company/', TeamView.as_view(), name='about-us'),
    path('about/life-at-xveralabs/', life_at_mn_solutions, name='life_at_mn_solutions'),
    path('about/diversity-equity-inclusion/', diversity_equity_inclusion, name='diversity_equity_inclusion'),
]