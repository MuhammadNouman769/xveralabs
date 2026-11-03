from django.core.management.base import BaseCommand

from apps.careers.models import JobPosition

# SAMPLE roles so you can see the pages working. Edit or close them in the admin,
# and keep only the roles you really want to hire for.
SAMPLES = [
    dict(title="Python / Django Backend Engineer", department="engineering", job_type="full_time", work_mode="hybrid", level="mid",
         summary="Build and maintain APIs and web back-ends for client products using Python, Django and PostgreSQL.",
         description="You will design and build back-end features for client projects, from database design to APIs, and work closely with front-end engineers and designers.",
         responsibilities="Build and maintain Django and DRF APIs\nDesign database models and write migrations\nWrite clean, tested code and take part in code reviews\nHelp deploy and monitor the services you build",
         requirements="Solid experience with Python and Django\nGood knowledge of PostgreSQL and REST APIs\nComfortable with Git and code review\nClear communication in English",
         nice_to_have="Celery, Redis or Docker\nExperience with AI APIs"),
    dict(title="Frontend Engineer (React)", department="engineering", job_type="full_time", work_mode="remote", level="mid",
         summary="Turn designs into fast, accessible web interfaces using React and modern CSS.",
         description="You will build user interfaces for web applications and dashboards, working from designs and agreed APIs.",
         responsibilities="Build reusable React components\nIntegrate REST APIs\nMake interfaces responsive and accessible\nReview code and share ideas with the team",
         requirements="Strong HTML, CSS and JavaScript\nExperience with React\nAttention to detail and design sense"),
    dict(title="DevOps Engineer", department="devops", job_type="full_time", work_mode="remote", level="mid",
         summary="Automate deployments and keep our client platforms reliable on the cloud.",
         description="You will own build and release pipelines, manage cloud infrastructure and improve monitoring across our projects.",
         responsibilities="Build and maintain CI/CD pipelines\nManage cloud infrastructure\nContainerise applications with Docker\nSet up monitoring and alerts",
         requirements="Experience with Linux, Docker and CI/CD\nWorking knowledge of AWS, Azure or GCP\nScripting skills (Bash or Python)"),
    dict(title="UI / UX Designer", department="design", job_type="full_time", work_mode="hybrid", level="mid",
         summary="Design clear, modern interfaces for web and mobile products.",
         description="You will take ideas from sketches to polished designs and prototypes, and work with engineers to see them built well.",
         responsibilities="Create wireframes, prototypes and final designs\nBuild and maintain a design system\nTest ideas with users and the team",
         requirements="A portfolio with web or mobile work\nExperience with Figma\nGood sense of layout and typography"),
    dict(title="Backend Development Intern (Python / Django)", department="engineering", job_type="internship", work_mode="hybrid", level="intern", duration="3 months",
         summary="Learn professional Django development by working on real tasks with a mentor.",
         description="This internship is for students and fresh graduates who want to start a career in back-end development.",
         responsibilities="Work on small features and bug fixes\nLearn Git, code review and testing\nPresent your work to the team",
         requirements="Basic Python knowledge\nUnderstanding of HTML and databases\nEagerness to learn and ask questions"),
    dict(title="Frontend Development Intern", department="engineering", job_type="internship", work_mode="hybrid", level="intern", duration="3 months",
         summary="Build real interface components with HTML, CSS and JavaScript under a mentor's guidance.",
         description="A learning-focused internship for people who enjoy building what users see.",
         responsibilities="Build and polish page sections\nFix layout and responsiveness issues\nLearn component-based development",
         requirements="Good HTML and CSS basics\nBasic JavaScript\nA small project or portfolio you can show"),
    dict(title="UI / UX Design Intern", department="design", job_type="internship", work_mode="hybrid", level="intern", duration="3 months",
         summary="Practise real product design with feedback from experienced designers.",
         description="You will help the design team with research, wireframes and visual design for client projects.",
         responsibilities="Support wireframing and prototyping\nCreate visual assets\nTake part in design reviews",
         requirements="Basic Figma skills\nA few design samples\nWillingness to take feedback"),
    dict(title="QA / Testing Intern", department="qa", job_type="internship", work_mode="onsite", level="intern", duration="3 months",
         summary="Learn how to test web and mobile products and report issues clearly.",
         description="You will test features before release and learn manual and basic automated testing.",
         responsibilities="Run test cases and report bugs\nWrite simple test scenarios\nRe-test fixes before release",
         requirements="Attention to detail\nClear written communication\nInterest in software quality"),
]


class Command(BaseCommand):
    help = "Create sample open positions and internships (they are only samples: edit or close them in the admin)."

    def handle(self, *args, **opts):
        made = 0
        for data in SAMPLES:
            _, created = JobPosition.objects.get_or_create(title=data["title"], defaults=data)
            made += int(created)
        self.stdout.write(self.style.SUCCESS(f"{made} sample positions created ({len(SAMPLES) - made} already existed)."))