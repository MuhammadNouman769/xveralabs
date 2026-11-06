from django.core.management.base import BaseCommand

from apps.services_pages.catalog import (
    AI_CATEGORIES,
    INDUSTRY_CATEGORIES,
    SERVICE_CATEGORIES,
    SOLUTION_CATEGORIES,
    build_ai_pages,
    build_catalog_pages,
    build_domain_pages,
)
from apps.services_pages.models import BlockKind as K
from apps.services_pages.models import ServiceBlock, ServiceGroup, ServicePage


def additional_faqs(title, group_name):
    return [
        (
            "What information should we bring to the first discussion?",
            "A short description of the goal, the people involved, relevant systems and any known constraints is enough to begin.",
        ),
        (
            "Can this work with our existing systems and processes?",
            "We review your current environment during discovery and shape the scope around relevant systems, workflows and constraints.",
        ),
        (
            "How do you agree on scope and priorities?",
            "We clarify the desired outcome, compare options and confirm priorities and boundaries with your team before delivery.",
        ),
        (
            "Can the work be delivered in phases?",
            "Yes. Where appropriate, we can break the work into reviewable stages and agree the next stage based on what is learned.",
        ),
        (
            "How will progress be reviewed?",
            "The team agrees on checkpoints and reviewable outputs so decisions, risks and progress stay visible.",
        ),
        (
            "How do you approach security and privacy?",
            "Security and privacy needs are considered during discovery and solution design, based on the data, users and requirements involved.",
        ),
        (
            "What will our team receive at the end?",
            "The outputs depend on the agreed scope and can include documented decisions, implementation work and recommended next steps.",
        ),
        (
            "Can you coordinate with our internal team?",
            "We agree responsibilities and communication with your team before work begins, and coordinate around the existing delivery process.",
        ),
        (
            "What support is available after delivery?",
            "Any follow-up, handover or ongoing support is discussed as part of the scope so expectations are clear before delivery.",
        ),
        (
            "How do we get started?",
            f"Contact us with a brief description of your {title.lower()} needs. We can discuss your goals and identify a sensible next step.",
        ),
        (
            f"How is success measured for {title.lower()}?",
            "We agree practical outcomes and review criteria with your team before delivery, so the result can be assessed against the original need.",
        ),
        (
            f"Who is involved in work on {title.lower()}?",
            f"The right participants depend on the scope. We identify the relevant {group_name.lower()} stakeholders and subject-matter experts during discovery.",
        ),
    ]


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

TECHNOLOGY_PAGES = [
 dict(slug="advanced-technology", title="Advanced Technology", short="Overview", order=0,
  tagline="Explore practical technologies that can improve operations, connect devices and create more useful digital experiences.",
  intro="""Advanced technology is most valuable when it solves a real problem. We help teams assess opportunities, choose an appropriate approach and plan a responsible implementation.

This page introduces our technology services. Explore the focused capabilities below to learn where automation, connected devices, distributed records or immersive interfaces may fit your goals.""",
  features=[("Robotic Process Automation","Identify repetitive, rules-based work that could be handled by software automation."),
   ("Internet of Things","Connect devices and systems to collect useful operational data."),
   ("Blockchain","Assess whether a shared, tamper-evident ledger is appropriate for a business process."),
   ("AR/VR experiences","Explore immersive interfaces for training, visualization or customer experiences.")],
  steps=[("Understand the need","Clarify the users, process and outcome behind the technology idea."),
   ("Assess options","Compare technical fit, integration needs, risks and ongoing ownership."),
   ("Prototype and plan","Test the important assumptions and define a practical delivery plan.")],
  deliverables=["A documented problem and opportunity assessment","A comparison of suitable technology options","A prototype or proof-of-concept plan","A phased implementation roadmap"],
  audience=["Teams exploring a new technology for a known business need","Operations leaders looking to reduce repetitive work","Product teams considering connected or immersive experiences"],
  sections=[("Start with the problem","""A technology choice should follow a clear need, not the other way around.

## What we consider
- The people who will use or maintain the solution.
- Existing systems, data and integration requirements.
- Security, privacy, accessibility and operational risks.
- The simplest way to test whether the idea is useful.""")],
  faqs=[("Do all projects need a proof of concept?","No. We recommend a prototype when an important assumption needs to be tested before a larger investment."),
   ("Can you help implement the selected solution?","Yes. After agreeing on scope, our team can help with design, engineering and integration.")]),

 dict(slug="robotic-process-automation", title="Robotic Process Automation (RPA)", short="RPA", order=1,
  tagline="Reduce repetitive, rule-based work with software automation designed around your existing processes.",
  intro="""Many teams spend time moving information between systems, checking forms or repeating predictable steps. Robotic Process Automation can handle some of this work when the process is stable and rules are clear.

We help map the workflow, check where automation is appropriate and design a solution with monitoring and human review for exceptions.""",
  features=[("Workflow assessment","Map the current steps and identify repetitive tasks suitable for automation."),
   ("Automation design","Define triggers, rules, exception handling and approvals."),
   ("System integration","Connect automation to the applications and data sources a workflow uses.")],
  steps=[("Map the workflow","Document the existing process and its exceptions."),
   ("Choose a pilot","Select a bounded, repeatable task and agree how to evaluate it."),
   ("Build and review","Implement the automation, test edge cases and plan ongoing monitoring.")],
  deliverables=["A workflow map and automation suitability review","A prioritized automation backlog","A pilot scope with exception handling","Documentation for operating and reviewing the automation"],
  audience=["Operations teams handling repeated data-entry tasks","Businesses moving information across multiple applications","Teams seeking to improve consistency in stable workflows"],
  sections=[("Choose automation carefully","""Automation works best when the process is understood and reasonably consistent.

## Before automating
- Simplify unnecessary steps first.
- Identify sensitive decisions that need human review.
- Plan for application changes, errors and audit requirements.""")],
  faqs=[("Can RPA work with our existing applications?","It can often interact with existing applications, but the best approach depends on available APIs, system stability and access controls."),
   ("Should every manual task be automated?","No. Tasks that require judgment or change frequently may be better improved through process redesign or direct system integration.")]),

 dict(slug="internet-of-things", title="Internet of Things (IoT)", short="IoT", order=2,
  tagline="Connect devices and operational systems to collect, understand and act on useful real-world data.",
  intro="""Connected devices can provide timely information about equipment, environments and operations. A successful IoT solution needs more than sensors: it also needs reliable connectivity, secure data handling and a clear plan for what happens when readings change.

We help teams define the use case, evaluate device and platform options, and plan an architecture that fits the environment.""",
  features=[("Use-case discovery","Define what should be observed and how the information will support a decision."),
   ("Device and platform planning","Compare sensors, connectivity and data platforms for the deployment context."),
   ("Data and alert workflows","Plan dashboards, event processing and the right response to important readings.")],
  steps=[("Define the signal","Choose the measurements and decisions that matter."),
   ("Plan the system","Review devices, connectivity, security and integrations."),
   ("Pilot in context","Test a small deployment and refine the operating model.")],
  deliverables=["An IoT use-case and requirements brief","A device, connectivity and platform comparison","A data-flow and integration plan","A pilot and rollout checklist"],
  audience=["Organizations monitoring equipment or facilities","Teams collecting data from distributed locations","Product teams building connected-device features"],
  sections=[("Design for the operating environment","""Device constraints and connectivity conditions shape the architecture.

## Plan for the full lifecycle
- Secure device identity and communications.
- Handle intermittent or unavailable connectivity.
- Track device health, updates and data quality.
- Define who responds to alerts and how.""")],
  faqs=[("Do we need to choose hardware before planning?","Not always. Starting with the required measurements and environment helps narrow hardware options."),
   ("Can an IoT project work with our existing software?","Often, through APIs or data integrations. The available interfaces and data requirements determine the approach.")]),

 dict(slug="blockchain", title="Blockchain", short="Blockchain", order=3,
  tagline="Evaluate distributed-ledger approaches for processes that need shared records, traceability or verifiable transactions.",
  intro="""Blockchain is useful only for a limited set of problems. It may be worth evaluating when multiple parties need to share a consistent record and ordinary databases or existing platforms do not meet the trust requirements.

We help compare the trade-offs, clarify governance and identify a small way to validate the concept before committing to a larger build.""",
  features=[("Use-case evaluation","Check whether a distributed ledger addresses a real coordination or trust need."),
   ("Architecture planning","Compare permissioned and public approaches, integrations and data boundaries."),
   ("Prototype design","Test a focused workflow and define how participants would operate it.")],
  steps=[("Review the participants","Understand who writes, reads and governs shared records."),
   ("Compare alternatives","Assess conventional databases and existing services alongside ledger options."),
   ("Validate a workflow","Prototype the smallest useful transaction and review its constraints.")],
  deliverables=["A technology suitability assessment","A comparison of architecture options","A governance and integration outline","A bounded prototype brief"],
  audience=["Organizations coordinating records across independent parties","Teams evaluating transaction traceability requirements","Product owners considering verifiable digital workflows"],
  sections=[("Compare the simpler alternatives","""A shared database or established service may be more appropriate than a blockchain.

## Important trade-offs
- Governance and participant responsibilities.
- Privacy and the handling of sensitive information.
- Performance, operating costs and long-term support.
- Integration with existing systems and legal requirements.""")],
  faqs=[("Should we put sensitive data on a blockchain?","Sensitive information needs careful protection. A design should evaluate data minimization, access, retention and legal requirements before implementation."),
   ("Can you help us decide if blockchain is necessary?","Yes. An initial assessment can compare the use case with conventional databases and other available approaches.")]),

 dict(slug="ar-vr", title="AR/VR", short="AR/VR", order=4,
  tagline="Design augmented and virtual reality experiences for training, visualization and interactive product use cases.",
  intro="""Augmented and Virtual Reality can make spatial information and simulated experiences easier to understand. The right format depends on the audience, environment, devices and task.

We help define the experience, assess device and accessibility needs, and prototype the important interactions before planning a full implementation.""",
  features=[("Experience discovery","Choose the user task and decide whether AR, VR or a simpler interface fits."),
   ("Interaction prototyping","Test navigation, controls and content with representative users."),
   ("Application integration","Plan how the experience connects to existing products, content and workflows.")],
  steps=[("Define the audience","Clarify users, setting, devices and accessibility needs."),
   ("Prototype key interactions","Test the experience with a small, focused scenario."),
   ("Plan delivery","Document content, integration, device support and maintenance needs.")],
  deliverables=["An experience concept and user-flow outline","A device and platform assessment","A prototype plan for key interactions","A content and implementation roadmap"],
  audience=["Teams developing interactive product experiences","Organizations exploring simulated training","Businesses visualizing spatial or product information"],
  sections=[("Make the experience useful and comfortable","""Immersive features should support a task rather than distract from it.

## Design considerations
- Keep interactions clear and comfortable for the intended session length.
- Provide alternatives for different devices and accessibility needs.
- Plan content updates, privacy and support from the beginning.""")],
  faqs=[("Do users need a headset?","Not always. Some augmented-reality experiences can use mobile devices, while virtual reality generally uses a headset."),
   ("Can we test an idea before building the full experience?","Yes. A small interactive prototype can help validate the task, device and interaction model.")]),
]


class Command(BaseCommand):
    help = "Create starter content for all service pages (edit it in the admin)."

    def handle(self, *args, **opts):
        made = 0
        groups = (
            ("strategy-consulting", "Strategy & Consulting", 0, PAGES),
            ("advanced-technology", "Advanced Technology", 1, TECHNOLOGY_PAGES),
        )
        for categories, catalog_pages in (
            (SERVICE_CATEGORIES, build_catalog_pages()),
            (AI_CATEGORIES, build_ai_pages()),
            (SOLUTION_CATEGORIES, build_domain_pages(SOLUTION_CATEGORIES, "solution")),
            (INDUSTRY_CATEGORIES, build_domain_pages(INDUSTRY_CATEGORIES, "industry")),
        ):
            for category in categories:
                category_pages = [
                    page for page in catalog_pages
                    if page["group_slug"] == category["slug"]
                ]
                groups += (
                    (
                        category["slug"],
                        category["name"],
                        category["order"],
                        category_pages,
                    ),
                )
        total_pages = sum(len(pages) for _, _, _, pages in groups)
        for group_slug, group_name, group_order, pages in groups:
            group, _ = ServiceGroup.objects.get_or_create(
                slug=group_slug,
                defaults={"name": group_name, "order": group_order},
            )
            for d in pages:
                page, created = ServicePage.objects.get_or_create(
                    slug=d["slug"],
                    defaults={
                        "group": group,
                        "title": d["title"],
                        "short_title": d["short"],
                        "tagline": d["tagline"],
                        "intro": d["intro"],
                        "order": d["order"],
                    },
                )
                if created:
                    made += 1
                    rows = []
                    for kind, key in (
                        (K.FEATURE, "features"),
                        (K.STEP, "steps"),
                        (K.SECTION, "sections"),
                        (K.FAQ, "faqs"),
                    ):
                        rows += [(kind, title, text) for title, text in d[key]]  # type: ignore
                    rows += [(K.DELIVERABLE, title, "") for title in d["deliverables"]]  # pyright: ignore[reportGeneralTypeIssues]
                    rows += [(K.AUDIENCE, title, "") for title in d["audience"]]  # type: ignore
                    ServiceBlock.objects.bulk_create(
                        [
                            ServiceBlock(
                                page=page,
                                kind=kind,
                                title=title,
                                text=text or title,
                                order=index,
                            )
                            for index, (kind, title, text) in enumerate(rows)
                        ]
                    )

                faq_blocks = ServiceBlock.objects.filter(
                    page=page, kind=K.FAQ, is_active=True
                )
                faq_titles = {faq.title.casefold() for faq in faq_blocks}
                missing_faqs = []
                faq_count = faq_blocks.count()
                for title, text in additional_faqs(d["title"], group_name):
                    if faq_count + len(missing_faqs) >= 10:
                        break
                    if title.casefold() in faq_titles:
                        continue
                    missing_faqs.append(
                        ServiceBlock(
                            page=page,
                            kind=K.FAQ,
                            title=title,
                            text=text,
                            order=faq_count + len(missing_faqs),
                        )
                    )
                ServiceBlock.objects.bulk_create(missing_faqs)
                section_blocks = ServiceBlock.objects.filter(
                    page=page, kind=K.SECTION, is_active=True
                )
                section_titles = {
                    section.title.casefold() for section in section_blocks
                }
                section_count = section_blocks.count()
                missing_sections = [
                    ServiceBlock(
                        page=page,
                        kind=K.SECTION,
                        title=title,
                        text=text,
                        order=section_count + index,
                    )
                    for index, (title, text) in enumerate(d.get("sections", []))
                    if title.casefold() not in section_titles
                ]
                ServiceBlock.objects.bulk_create(missing_sections)
        self.stdout.write(
            self.style.SUCCESS(
                f"{made} pages created ({total_pages - made} already existed)."
            )
        )