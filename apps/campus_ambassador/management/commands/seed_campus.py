from django.core.management.base import BaseCommand

from apps.campus_ambassador.models import Cohort, ItemKind, ProgramItem

# SAMPLE content so you can see the page working. Edit everything in the dashboard
# (Campus Ambassador > Program items) and keep only points that are TRUE for your program.
ITEMS = [
    (ItemKind.BENEFIT, "Certificate of participation", "Receive a certificate when you complete the program term."),
    (ItemKind.BENEFIT, "Skill workshops", "Short sessions on communication, event planning and marketing."),
    (ItemKind.BENEFIT, "Mentorship", "Guidance from the Xvera Labs team while you run your activities."),
    (ItemKind.BENEFIT, "Networking", "Meet student leaders from other campuses in the same program."),
    (ItemKind.BENEFIT, "Internship consideration", "Strong performers may be considered for internships at Xvera Labs."),
    (ItemKind.BENEFIT, "Recognition", "A reference from our team for ambassadors who complete the term well."),
    (ItemKind.STEP, "Apply online", "Fill in the short application form and tell us why you would be a great fit."),
    (ItemKind.STEP, "We review", "Our team reads every application and may invite you to a short call."),
    (ItemKind.STEP, "Onboarding", "Selected ambassadors get an orientation and a clear plan for the term."),
    (ItemKind.STEP, "Lead and grow", "Run campus activities, share what you learn and get regular feedback."),
    (ItemKind.RESPONSIBILITY, "Represent Xvera Labs", "Be the friendly contact for students on your campus who want to learn about us."),
    (ItemKind.RESPONSIBILITY, "Organise activities", "Help run meetups, workshops or sessions with support from our team."),
    (ItemKind.RESPONSIBILITY, "Share content", "Post about the program and your experience on your own channels."),
    (ItemKind.RESPONSIBILITY, "Share feedback", "Tell us what students on your campus need and want."),
    (ItemKind.FAQ, "Who can apply?", "Any student currently enrolled at a university or college. All degree programs and years are welcome."),
    (ItemKind.FAQ, "Is there a fee to apply?", "No. Applying and taking part are free."),
    (ItemKind.FAQ, "How much time does it take?", "It depends on the term. The time commitment is shown at the top of this page."),
    (ItemKind.FAQ, "Is this a paid role?", "It is a volunteer program for students. See the benefits above for what ambassadors receive."),
    (ItemKind.FAQ, "Can first-year students apply?", "Yes. Students from any year can apply."),
]


class Command(BaseCommand):
    help = "Create a sample cohort and sample page content (edit or delete them in the dashboard)."

    def handle(self, *args, **opts):
        cohort, c_new = Cohort.objects.get_or_create(
            name="Current cohort",
            defaults=dict(term_months=3, hours_per_week="4 to 6 hours",
                          eligibility="Currently enrolled at a university or college\nAny degree program and any year\nComfortable talking to people and organising small activities"))
        made = 0
        for i, (kind, title, text) in enumerate(ITEMS):
            _, new = ProgramItem.objects.get_or_create(kind=kind, title=title, defaults=dict(text=text, order=i))
            made += int(new)
        self.stdout.write(self.style.SUCCESS(f"Cohort {'created' if c_new else 'already existed'}, {made} items created."))