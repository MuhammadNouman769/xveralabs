from django.shortcuts import get_object_or_404, redirect, render

from .models import IndustryCaseStudy, IndustryCaseStudyBlock

# Create your views here.

def home(request):
    return render(request, 'home/index.html')


def services(request):
    return redirect("software_development", permanent=True)

def projects(request):
    return redirect("case_studies", permanent=True)

def signin(request):
    return redirect("home", permanent=True)

def signup(request):
    return redirect("home", permanent=True)

def blogs(request):
    query = request.GET.urlencode()
    destination = f"/resources/?{query}" if query else "/resources/"
    return redirect(destination, permanent=True)

def blog_single(request):
    return redirect("resources", permanent=True)

def case_studies(request):
    case_studies = IndustryCaseStudy.objects.filter(
        is_active=True, is_published=True
    )
    return render(
        request,
        "home/case-studies.html",
        {"case_studies": case_studies},
    )


def industry_case_study(request, slug):
    case_study = get_object_or_404(
        IndustryCaseStudy.objects.prefetch_related("blocks"),
        slug=slug,
        is_active=True,
        is_published=True,
    )
    return render(
        request,
        "home/industry-case-study.html",
        {
            "case_study": case_study,
            "capabilities": case_study.blocks.filter(
                kind=IndustryCaseStudyBlock.Kind.CAPABILITY,
                is_active=True,
            ),
            "considerations": case_study.blocks.filter(
                kind=IndustryCaseStudyBlock.Kind.CONSIDERATION,
                is_active=True,
            ),
            "related_case_studies": IndustryCaseStudy.objects.filter(
                is_active=True, is_published=True
            ).exclude(pk=case_study.pk)[:4],
        },
    )

def faqs(request):
    return render(request, 'faqs/faqs.html')

def term_condition(request):
    return render(request, 'faqs/term_condition.html')

def privacy_policy(request):
    return render(request, 'faqs/privacy_policy.html')

def sqa(request):
    return redirect("quality_assurance", permanent=True)

def web_dev(request):
    return redirect("web_app_development", permanent=True)

def product_dev(request):
    return redirect("product_engineering", permanent=True)

def devops(request):
    return redirect("cloud_native_engineering", permanent=True)

def staff_aug(request):
    return redirect("staff_augmentation", permanent=True)


def coming(request):
    return render(request, 'coming-soon.html')


def articial_detail(request):
    return redirect("ai_solutions_engineering", permanent=True)
