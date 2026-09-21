from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home/index.html')

def why_choose_us(request):
    return render(request, 'about/why-choose-us.html')

def contact(request):
    return render(request, 'home/contact-us.html')

def services(request):
    return render(request, 'home/services.html')

def projects(request):
    return render(request, 'home/projects.html')

def signin(request):
    return render(request, 'home/signin.html')

def signup(request):
    return render(request, 'home/signup.html')

def blogs(request):
    return render(request, 'blogs/blog-grid.html')

def blog_single(request):
    return render(request, 'home/blog-single.html')

def case_studies(request):
    return render(request, 'home/case-studies.html')

def faqs(request):
    return render(request, 'faqs/faqs.html')

def term_condition(request):
    return render(request, 'faqs/term_condition.html')

def privacy_policy(request):
    return render(request, 'faqs/privacy_policy.html')

def sqa(request):
    return render(request, 'services/sqa.html')

def web_dev(request):
    return render(request, 'services/web_development.html')

def product_dev(request):
    return render(request, 'services/product_dev.html')    

def devops(request):
    return render(request, 'services/devops.html')

def staff_aug(request):
    return render(request, 'services/staff-aug.html')


def coming(request):
    return render(request, 'coming-soon.html')

def careeer(request):
    return render(request, 'about/careers.html')

def articial_detail(request):
    return render(request, 'artificial_intelligence/ariticial_itelligence_detail.html')