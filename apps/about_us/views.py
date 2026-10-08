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

def diversity_equity_inclusion(request):
    return render(request, 'about/join-xvera-labs/diversity-equity-inclusion.html')

def employee_success(request):
    return render(request, 'about/join-xvera-labs/employee-success.html')

def benefits(request):
    return render(request, 'about/join-xvera-labs/benefits.html')
