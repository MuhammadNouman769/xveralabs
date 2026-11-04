from django.core.management.base import BaseCommand

from apps.services_pages.models import BlockKind as K
from apps.services_pages.models import ServiceBlock, ServiceGroup, ServicePage

# Starter content for the Strategy & Consulting pages. It describes HOW we work, with no invented numbers or client claims.
# Review it, edit it in the admin (Service pages) and delete anything that is not true for your company.
PAGES = [
 dict(slug="strategy-and-consulting", title="Strategy & Consulting", short="Overview", order=0,
  tagline="Clear direction for your business, product and technology decisions, from a team that also builds the software.",
  intro="""Good software starts with good decisions. Before a single line of code is written, someone has to decide what to build, for whom, in what order and with which technology.

Our Strategy & Consulting service helps you make those decisions with confidence. We look at your goals, your users and your current systems, and turn them into a plan your team can actually follow.

Because we are also the people who design and build software every day, our advice stays practical. We tell you what is worth doing, what can wait and what it is likely to cost.""",
  features=[("Business optimization","Find the slow, manual and costly parts of how your business runs, and fix them in the right order."),
   ("Product strategy","Decide what to build first, who it is for and how you will know it works."),
   ("Technology strategy","Choose architecture, tools and cloud setup that fit your goals and your budget."),
   ("Learning & development","Raise your team's skills with practical, hands-on training."),
   ("Digital roadmaps","Turn ideas into a prioritised plan with clear phases and estimates."),
   ("Build, buy or integrate","Get an honest view on custom software versus ready-made tools.")],
  steps=[("Listen","We start with your goals, constraints and what you have already tried."),
   ("Assess","We review your processes, product and systems to see where things really stand."),
   ("Recommend","We share options with trade-offs, not a single answer."),
   ("Plan","We turn the chosen option into a phased roadmap with estimates."),
   ("Support","We stay available to help your team, or ours, carry it out.")],
  deliverables=["A short discovery summary of goals and constraints","A current-state assessment in plain language","Recommendations with the pros and cons of each option","A prioritised roadmap with phases and rough estimates","Workshop notes and decisions, so nothing gets lost"],
  audience=["Founders turning an idea into a product","Business owners who want to work with less manual effort","Product and engineering leads planning the next stage","Teams modernising older systems"],
  sections=[("Why consulting from a team that builds software","""Many consultants write reports. We write reports too, but we also have to make the plan work in code.

## What that means for you
- Recommendations are checked against real technical effort, not guesswork.
- We say early when an idea is too big for the first release.
- If you choose to build with us, nothing is lost in translation between advice and delivery.

You are free to take our plan to any team. A good plan should work whoever carries it out."""),
   ("How we can work together","""We keep the ways of working simple, so you can start small.

1. **Workshop:** a focused session to clarify goals and options.
2. **Assessment:** a deeper review of your product, process or technology, with a written report.
3. **Ongoing advisory:** regular time with our team as you build and grow.

The right option depends on your situation. We will suggest one after our first conversation.""")],
  faqs=[("Do I need a consulting engagement before building software?","Not always. If your idea is already clear, we can go straight to building. A short consulting phase helps most when the goals, scope or technology choices are still open."),
   ("How long does a consulting engagement take?","A workshop can be a day or two. An assessment usually takes a few weeks, depending on size. We agree the timeline with you before starting."),
   ("Will you also build what you recommend?","If you want us to, yes. If not, you can take the plan to another team. The advice is meant to stand on its own."),
   ("How do we get started?","Contact us with a short description of your situation. We will arrange a call and suggest the simplest next step.")]),

 dict(slug="business-optimization-consulting", title="Business Optimization Consulting", short="Business Optimization", order=1,
  tagline="Remove manual work, bottlenecks and wasted effort by improving how your business runs and which tools it uses.",
  intro="""Most businesses do not slow down because people work too little. They slow down because work moves through too many hand-offs, spreadsheets and repeated steps.

Our Business Optimization Consulting looks closely at how work really flows through your organisation. We map the process, find where time and money leak, and propose improvements that fit your team.

Some fixes need no software at all. Others are best solved with a small tool, an integration or automation. We tell you which is which.""",
  features=[("Process mapping","We document how work flows today, step by step, with the people who do it."),
   ("Bottleneck analysis","We find the steps where work waits, repeats or gets lost."),
   ("Automation opportunities","We pick the repetitive tasks that are worth automating first."),
   ("Tool and system review","We check overlapping tools and gaps, and recommend what to keep, merge or replace."),
   ("Metrics and reporting","We define a few useful measures so you can see whether things improve."),
   ("Change planning","We plan how to roll improvements out so your team actually adopts them.")],
  steps=[("Map","We sit with your team and map the current process as it really happens."),
   ("Measure","We find where time, cost and errors build up."),
   ("Prioritise","We rank improvements by effort and benefit."),
   ("Improve","We design the new process and, where needed, the tools to support it."),
   ("Review","We check results and adjust.")],
  deliverables=["Current-state process maps","A list of bottlenecks and their causes","A quick-wins list you can start on at once","An automation backlog ranked by value and effort","Suggested measures and a simple reporting layout","A rollout plan for the changes"],
  audience=["Growing businesses whose processes have not kept up","Operations and finance teams working in spreadsheets","Companies using many tools that do not talk to each other","Owners who feel the business depends on a few people"],
  sections=[("Start with the process, then the software","""A new tool placed on top of a confusing process usually makes the confusion faster.

## Our order of work
1. Understand the process and who it serves.
2. Remove steps that add no value.
3. Simplify what remains.
4. Only then automate or build software.

This keeps your spending focused on what really helps.""")],
  faqs=[("Does optimization always mean new software?","No. Often the biggest gains come from simplifying steps or changing responsibilities. We recommend software only when it is the best answer."),
   ("Will this disrupt our team?","We work around your schedule and involve the people who do the work. Changes are introduced in small steps."),
   ("Can you implement the automation too?","Yes. Our engineers can build integrations and automation, or hand over a clear specification to your team."),
   ("How do we know it worked?","We agree a few measures at the start, such as time per task or error rate, and check them after the changes.")]),

 dict(slug="product-strategy", title="Product Strategy", short="Product Strategy", order=2,
  tagline="Decide what to build first, who it is for and how you will know it works, before you spend on development.",
  intro="""The most expensive mistake in software is building the wrong thing well. Product strategy reduces that risk.

We help you describe the problem, understand your users, define a first version worth launching and plan what comes after. The result is a product direction that you, your team and your developers can all follow.

Whether you are launching a new product or improving an existing one, we focus on real user needs and a realistic scope.""",
  features=[("Discovery and research","We talk to users and study the market so decisions rest on evidence."),
   ("Positioning and value","We define who the product is for and why they would choose it."),
   ("MVP scoping","We cut the idea down to a first release that can be built and tested quickly."),
   ("Roadmap and prioritisation","We order features by value and effort, and plan the stages."),
   ("Prototyping","We turn key ideas into clickable prototypes to test before building."),
   ("Success metrics","We define how you will measure whether the product is working.")],
  steps=[("Discover","We learn about your users, market and goals."),
   ("Define","We shape the problem statement, target users and value."),
   ("Scope","We choose the smallest version that tests the idea."),
   ("Prototype","We design and test the key flows with real people."),
   ("Plan","We prepare the roadmap and backlog for development.")],
  deliverables=["A product vision and clear problem statement","User profiles and key journeys","An MVP scope document, with what is in and what is out","A prioritised roadmap and backlog","Clickable prototypes of the main flows","A set of success measures"],
  audience=["Founders with a new product idea","Companies adding a digital product to their business","Product owners with too many ideas and too little clarity","Teams whose product has stalled and needs a fresh direction"],
  sections=[("What a good MVP really is","""An MVP is not a poor-quality product. It is the smallest product that lets you learn something real from real users.

## How we scope it
- Start from the one problem the product must solve.
- List everything users could want, then keep only what proves the core idea.
- Plan the next releases, but do not build them yet.

This lets you launch sooner and spend the next budget on what users actually asked for.""")],
  faqs=[("Do you only advise, or do you design and build too?","Both are possible. Many clients start with product strategy and continue with design and development, but you can also take the outputs to another team."),
   ("What if I only have an idea and no research?","That is a normal starting point. Our discovery step is designed to turn an idea into something tested and specific."),
   ("How long does product strategy take?","It depends on how much is already known. A focused engagement is often a few weeks. We agree the timeline at the start."),
   ("Will I own the documents and designs?","The deliverables are prepared for you to use. We confirm ownership terms in the agreement before work starts.")]),

 dict(slug="technology-strategy", title="Technology Strategy", short="Technology Strategy", order=3,
  tagline="Make confident choices about architecture, cloud, security and tools, so your technology supports growth instead of slowing it.",
  intro="""Technology decisions are hard to undo. The wrong database, hosting model or architecture can quietly cost you for years.

Our Technology Strategy service reviews where you are, where you want to go and what stands in between. We look at architecture, infrastructure, security basics, team skills and cost, and then recommend a clear path.

We are tool-neutral. We recommend what fits your situation, whether that is a simple setup that is cheap to run or a more scalable platform for a growing product.""",
  features=[("Architecture review","We assess how your system is built and where it will struggle as you grow."),
   ("Technology selection","We compare options for languages, frameworks, databases and services."),
   ("Cloud and infrastructure","We plan hosting, environments and cost on AWS, Azure, GCP or simpler options."),
   ("Security and reliability basics","We check access, data protection, backups and monitoring."),
   ("Technical debt planning","We list the shortcuts that cost you most and plan how to pay them down."),
   ("AI readiness","We look at where AI tools could help, and what data and systems you need first.")],
  steps=[("Understand","We review goals, current systems and constraints."),
   ("Review","We examine architecture, code health, infrastructure and security."),
   ("Compare","We weigh realistic options with their costs and risks."),
   ("Recommend","We propose a target setup and the steps to reach it."),
   ("Roadmap","We plan the migration or upgrade in safe stages.")],
  deliverables=["An architecture review report","A recommended target architecture","A technology comparison with trade-offs","A migration or upgrade plan in stages","A risk list with suggested actions","A cost estimate for infrastructure and effort"],
  audience=["Companies whose system is getting slow or hard to change","Teams choosing a stack for a new product","Businesses planning a cloud move","Leaders who want an independent second opinion"],
  sections=[("Build, buy or integrate","""Not every problem needs custom software. Sometimes a ready-made tool is the better choice.

## How we decide with you
- **Build** when the software is part of what makes your business different.
- **Buy** when the problem is common and a good product already exists.
- **Integrate** when two good tools just need to work together.

We compare the total cost over time, not only the first price.""")],
  faqs=[("Do we need to move to the cloud?","Not necessarily. The right answer depends on cost, scale, compliance and your team. We compare cloud and simpler options honestly."),
   ("Can you review a system someone else built?","Yes. A review of an existing system is a common request. We explain findings in plain language and avoid blame."),
   ("Will you recommend only technologies you sell?","No. We recommend what fits your goals. We prefer tools your team can maintain."),
   ("What do you need from us to start?","Access to documentation or a walkthrough of your system, and time with the people who know it best.")]),

 dict(slug="learning-and-development", title="Learning & Development", short="Learning & Development", order=4,
  tagline="Practical, hands-on training that helps your team build better software and use modern tools with confidence.",
  intro="""Technology moves quickly, and a team's skills can fall behind without anyone noticing. Good training closes that gap.

Our Learning & Development service gives your team practical training led by working engineers. Sessions use real examples and exercises, not slides alone, so people can apply what they learn the next day.

We shape each programme around your team's level, your tools and your goals. It can be a single workshop, a series of sessions or a longer structured programme.""",
  features=[("Engineering workshops","Hands-on sessions on topics such as Python and Django, APIs, databases and testing."),
   ("Cloud and DevOps training","Practical training on containers, CI/CD, deployment and monitoring."),
   ("AI tools for teams","How to use modern AI tools safely and effectively in daily work."),
   ("Engineering practices","Code review, version control, testing and clean-code habits."),
   ("Onboarding programmes","A structured start for new hires and interns."),
   ("Mentoring","Regular one-to-one guidance for developers growing into senior roles.")],
  steps=[("Assess","We learn your team's current skills and goals."),
   ("Design","We build a programme that fits your level, tools and schedule."),
   ("Deliver","We run the sessions with real examples and exercises."),
   ("Practise","Participants apply the skills on a real task."),
   ("Review","We check progress and plan what comes next.")],
  deliverables=["A short skills assessment","A learning plan matched to your goals","Workshop materials and exercises","Hands-on labs using your kind of work","A progress review at the end"],
  audience=["Engineering managers upskilling their team","Companies onboarding new developers or interns","Teams adopting new tools or cloud platforms","Organisations that want to reduce their reliance on outside help"],
  sections=[("Learning that sticks","""People remember what they practise. Our programmes are built around doing.

## What a typical session looks like
- A short explanation of the idea and why it matters.
- A guided exercise on a realistic example.
- Time to try it on your own code or case.
- Questions, discussion and a short summary.

We agree format, group size and schedule with you when we scope the programme.""")],
  faqs=[("Can the training be online or on site?","We can agree the format that suits your team. Online sessions are often easier to schedule across locations."),
   ("Can you customise the topics?","Yes. We build each programme around your tools, your level and what your team needs next."),
   ("Is this suitable for beginners?","Yes. We can run programmes for beginners, mixed teams or experienced engineers."),
   ("How do we measure progress?","We agree simple goals at the start, review them at the end and can include a hands-on task.")]),
]


class Command(BaseCommand):
    help = "Create the Strategy & Consulting group and its five pages with starter content (edit them in the admin)."

    def handle(self, *args, **opts):
        group, _ = ServiceGroup.objects.get_or_create(slug="strategy-consulting", defaults=dict(name="Strategy & Consulting", order=0))
        made = 0
        for d in PAGES:
            page, created = ServicePage.objects.get_or_create(slug=d["slug"], defaults=dict(
                group=group, title=d["title"], short_title=d["short"], tagline=d["tagline"], intro=d["intro"], order=d["order"]))
            if not created:
                continue
            made += 1
            rows = []
            for kind, key in ((K.FEATURE, "features"), (K.STEP, "steps"), (K.SECTION, "sections"), (K.FAQ, "faqs")):
                rows += [(kind, t, x) for t, x in d[key]] # type: ignore
            rows += [(K.DELIVERABLE, t, "") for t in d["deliverables"]] # pyright: ignore[reportGeneralTypeIssues]
            rows += [(K.AUDIENCE, t, "") for t in d["audience"]] # type: ignore
            ServiceBlock.objects.bulk_create([ServiceBlock(page=page, kind=k, title=t, text=x or t, order=i) for i, (k, t, x) in enumerate(rows)])
        self.stdout.write(self.style.SUCCESS(f"{made} pages created ({len(PAGES) - made} already existed)."))