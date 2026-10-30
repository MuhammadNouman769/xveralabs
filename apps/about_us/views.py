from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import render
from .models import Team

""" =============== Company View ================ """

class CompanyView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'about/company/company.html'

    def get(self, request):
        teams = Team.objects.filter(
            is_active=True
        ).order_by("display_order")
        
        return Response({
            'teams': teams
        })


""" =============== Why Choose Us View ================ """


def why_choose_us(request):
    return render(request, 'about/why-choose-us/why-choose-us.html')

""" =============== Join Xvera labs View ================ """

def careeers(request):
    return render(request, 'about/join-xvera-labs/careers.html')

def life_at_xvera_labs(request):
    return render(request, 'about/join-xvera-labs/life-at-xvera-labs.html')       


"""
ONE PAGE for Employee Success + Benefits + Diversity, Equity & Inclusion.

1) Put these in your app's views.py
2) Put the url patterns in your app's urls.py. KEEP the same path strings you already use for the
   three old pages (so old links and bookmarks still work); only the view changes.
3) Delete the three old views/templates once you have checked the new page.
"""
# ---------------- views.py ----------------
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView


class PeopleView(TemplateView):
    template_name = "about/join-xvera-labs/people.html"          # <- where you put people.html


class PeopleAnchorRedirect(RedirectView):
    """Old page -> the matching section of the new page."""

    permanent = True
    anchor = ""

    def get_redirect_url(self, *args, **kwargs):
        return reverse("people") + (f"#{self.anchor}" if self.anchor else "")


def campus_ambassador_program(request):
    return render(request, 'about/join-xvera-labs/campus-ambassador-program.html')    
