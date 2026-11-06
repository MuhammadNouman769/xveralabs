"""Starter catalog for the service links that were placeholders in the menu."""

import re

SERVICE_CATEGORIES = [
    {
        "slug": "cloud-services",
        "name": "Cloud Services",
        "order": 2,
        "focus": "cloud platforms, infrastructure and operating costs",
        "design": "cloud",
        "items": [
            "Cloud",
            "Managed Cloud and FinOps",
            "Cloud-Native Engineering",
            "AWS, Azure, GCP & Oracle",
            "Cloud Modernization & Migration",
        ],
    },
    {
        "slug": "ai-solutions-engineering",
        "name": "AI Solutions & Engineering",
        "order": 3,
        "focus": "AI products, machine learning and responsible integration",
        "design": "intelligence",
        "items": [
            "AI Solutions & Engineering",
            "AI Product Development",
            "Generative AI Applications",
            "Agentic AI Systems",
            "AI Platforms & Machine Learning",
        ],
    },
    {
        "slug": "innovation",
        "name": "Innovation",
        "order": 4,
        "focus": "validating ideas and turning useful concepts into products",
        "design": "workshop",
        "items": [
            "Innovation",
            "Design Thinking",
            "MVP Development",
            "Agile Development",
        ],
    },
    {
        "slug": "quality-assurance",
        "name": "Quality Assurance",
        "order": 5,
        "focus": "software quality, testing and release confidence",
        "design": "quality",
        "items": [
            "Quality Assurance",
            "Functional Testing",
            "Integration Testing",
            "Self-Healing Test Automation",
            "Automation Testing",
        ],
    },
    {
        "slug": "ai-strategy-governance",
        "name": "AI Strategy & Governance",
        "order": 6,
        "focus": "AI readiness, adoption, risk management and governance",
        "design": "governance",
        "items": [
            "AI Strategy, Enablement & Governance",
            "AI Strategy & Readiness Assessment",
            "AI Use Case Discovery Workshops",
            "AI Enablement & Executive Training",
            "AI Security, Risk & Governance",
        ],
    },
    {
        "slug": "digital-implementation",
        "name": "Digital Implementation",
        "order": 7,
        "focus": "delivery leadership, product engineering and business workflows",
        "design": "delivery",
        "items": [
            "Digital Implementation & Delivery",
            "Program Management",
            "Product Engineering",
            "Managed Services",
            "Business Process Orchestration",
        ],
    },
    {
        "slug": "modernization",
        "name": "Modernization",
        "order": 8,
        "focus": "improving established platforms, architecture and experiences",
        "design": "blueprint",
        "items": [
            "Modernization",
            "Platform Refactoring",
            "Technology Assessment",
            "User Experience",
            "Enterprise Application Architecture",
        ],
    },
    {
        "slug": "software-development",
        "name": "Software Development",
        "order": 9,
        "focus": "building, extending and supporting software products",
        "design": "engineering",
        "items": [
            "Software Development",
            "Nearshore Development",
            "Offshore Development",
            "Staff Augmentation",
            "Web App Development",
            "Mobile App Development",
            "eCommerce Solutions",
        ],
    },
    {
        "slug": "data-analytics",
        "name": "Data & Analytics",
        "order": 10,
        "focus": "data platforms, governance, analytics and decision support",
        "design": "data",
        "items": [
            "Data & Analytics",
            "Data Engineering",
            "Data Management & Governance",
            "Analytics & Platform Implementation",
            "Data Science",
        ],
    },
    {
        "slug": "privacy-security",
        "name": "Privacy & Security",
        "order": 11,
        "focus": "privacy, security controls, compliance and risk reduction",
        "design": "trust",
        "items": [
            "Privacy & Security",
            "Governance, Risk & Compliance",
            "Cyber Security",
            "Security Services",
            "Penetration Testing",
        ],
    },
]

AI_CATEGORIES = [
    {
        "slug": "ai-consulting-strategy",
        "name": "AI Consulting & Strategy",
        "order": 20,
        "focus": "AI readiness, product opportunities, and an adoption roadmap",
        "items": [
            "AI Strategy Consulting",
            "AI Readiness Assessment",
            "AI Product Development",
            "AI Adoption Roadmap",
        ],
    },
    {
        "slug": "ai-development-engineering",
        "name": "AI Development & Engineering",
        "order": 21,
        "focus": "machine learning, computer vision, and AI-enabled software",
        "items": [
            "Custom AI Development",
            "Machine Learning Development",
            "Computer Vision Solutions",
            "AI Integration Services",
        ],
    },
    {
        "slug": "enterprise-ai-governance",
        "name": "Enterprise AI & Governance",
        "order": 22,
        "focus": "enterprise adoption, responsible AI, security and operations",
        "items": [
            "Enterprise AI Solutions",
            "AI Security, Risk & Compliance",
            "Responsible AI & Governance",
            "MLOps & AI Platforms",
        ],
    },
    {
        "slug": "ai-training-enablement",
        "name": "AI Training & Enablement",
        "order": 23,
        "focus": "practical AI skills, leadership and team adoption",
        "items": [
            "Executive AI Leadership Program",
            "AI Workshops for Enterprises",
            "AI Use Case Discovery",
            "AI Enablement Workshops",
        ],
    },
    {
        "slug": "generative-ai-development",
        "name": "Generative AI Development",
        "order": 24,
        "focus": "large language model applications and generative experiences",
        "items": [
            "LLM Application Development",
            "Custom Chatbot Development",
            "AI Content Generation",
            "Fine-Tuning & Model Customization",
        ],
    },
    {
        "slug": "rag-knowledge-systems",
        "name": "RAG & Knowledge Systems",
        "order": 25,
        "focus": "retrieval, organizational knowledge and document intelligence",
        "items": [
            "RAG Solutions",
            "Enterprise Knowledge Assistants",
            "AI Document Intelligence",
            "Vector Database Integration",
        ],
    },
    {
        "slug": "agentic-ai",
        "name": "Agentic AI",
        "order": 26,
        "focus": "AI agents, workflow orchestration and conversational interfaces",
        "items": [
            "AI Agent Development",
            "Multi-Agent Workflows",
            "AI Workflow Automation",
            "Voice & Conversational Agents",
        ],
    },
    {
        "slug": "genai-integration-services",
        "name": "GenAI Integration & Services",
        "order": 27,
        "focus": "connecting generative AI models and assistants to business systems",
        "items": [
            "OpenAI / Claude / Gemini Integration",
            "Prompt Engineering Services",
            "AI Copilots for Business",
            "GenAI MVP Development",
        ],
    },
]

SOLUTION_CATEGORIES = [
    {
        "slug": "data-solutions",
        "name": "Data Solutions",
        "order": 30,
        "focus": "turning scattered data into reliable information for decisions",
        "design": "data",
        "items": [
            "BI & Data Analytics",
            "Data Governance & Security",
            "Data Migration",
            "Data Scraping",
            "Data Warehousing",
        ],
    },
    {
        "slug": "e-commerce-solutions",
        "name": "E-Commerce",
        "order": 31,
        "focus": "helping commerce teams improve discovery, purchasing and service",
        "design": "commerce",
        "items": [
            "AI Chatbots & Support",
            "eCommerce Development",
            "Marketplace Solutions",
            "Voice Commerce",
            "Customer Segmentation",
            "Recommendation Engines",
        ],
    },
    {
        "slug": "applied-ai-solutions",
        "name": "Applied AI",
        "order": 32,
        "focus": "using data and AI methods to answer practical business questions",
        "design": "applied-ai",
        "items": [
            "Deep Learning",
            "Predictive Analytics",
            "Sentiment Analysis",
            "AI Consulting",
        ],
    },
]

INDUSTRY_CATEGORIES = [
    {
        "slug": "core-industries",
        "name": "Core Industries",
        "order": 40,
        "focus": "digital experiences for essential, people-facing sectors",
        "design": "core-industry",
        "items": [
            "Healthcare",
            "Education",
            "Finance & Banking",
            "E-Commerce",
            "Retail",
            "Real Estate",
        ],
    },
    {
        "slug": "digital-economy-industries",
        "name": "Digital Economy",
        "order": 41,
        "focus": "connected services across travel, logistics, food, media and sport",
        "design": "digital-industry",
        "items": [
            "Travel & Tourism",
            "Logistics & Supply Chain",
            "Food & Restaurants",
            "Media & Entertainment",
            "Sports Tech",
        ],
    },
    {
        "slug": "special-domains-industries",
        "name": "Special Domains",
        "order": 42,
        "focus": "technology shaped around specialized needs and responsibilities",
        "design": "special-industry",
        "items": [
            "Artificial Intelligence",
            "Government Projects",
            "Non-Profit / NGO",
            "Religious Platforms",
        ],
    },
]

def build_catalog_pages():
    """Build editable CMS starter records from the service-menu catalog."""
    pages = []
    for category in SERVICE_CATEGORIES:
        for order, title in enumerate(category["items"]):
            slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
            if slug == "aws-azure-gcp-oracle":
                slug = "aws-azure-gcp-oracle-cloud"
            if slug == "self-healing-test-automation":
                slug = "self-healing-test-automation"

            focus = category["focus"]
            pages.append(
                {
                    "group_slug": category["slug"],
                    "group_name": category["name"],
                    "group_order": category["order"],
                    "slug": slug,
                    "title": title,
                    "short": title[:40],
                    "order": order,
                    "design": category["design"],
                    "tagline": (
                        f"Make {title.lower()} work for your goals with a practical "
                        f"approach to {focus}."
                    ),
                    "intro": (
                        f"{title} should support a clear business or product outcome. "
                        f"Our team helps you understand the need, shape an approach and "
                        f"plan delivery around your people, systems and constraints.\n\n"
                        f"For {focus}, we focus on useful decisions and maintainable "
                        "solutions rather than adding complexity for its own sake. "
                        "The scope is shaped with your team before implementation begins."
                    ),
                    "features": [
                        (
                            "Discovery and priorities",
                            f"Clarify the outcomes, users and constraints that matter for {title.lower()}.",
                        ),
                        (
                            "Solution design",
                            f"Compare suitable options for {focus}, including integration, ownership and trade-offs.",
                        ),
                        (
                            "Delivery support",
                            f"Turn the agreed direction for {title.lower()} into manageable work that can be reviewed and improved.",
                        ),
                    ],
                    "steps": [
                        ("Understand", "Align on the current situation, desired outcome and practical constraints."),
                        ("Shape", f"Define a suitable approach to {title.lower()} and agree what is in scope."),
                        ("Deliver", "Build or configure the agreed solution in reviewable stages."),
                        ("Improve", "Review how the result works in practice and identify the next useful step."),
                    ],
                    "deliverables": [
                        f"An agreed scope and success criteria for {title.lower()}",
                        f"A solution outline covering {focus}",
                        "A prioritized delivery plan with dependencies and decisions",
                        "Implementation notes and recommended next steps",
                    ],
                    "audience": [
                        "Teams planning a new digital initiative",
                        "Organizations improving an existing product or process",
                        "Leaders who need a clear technical delivery plan",
                    ],
                    "sections": [
                        (
                            f"A practical approach to {title.lower()}",
                            f"""The right solution depends on the context around {title.lower()}. We start by understanding the people, workflows and systems involved.

## What we consider
- The result your users and business need.
- Existing tools, integrations and team capabilities.
- Security, privacy, accessibility and ongoing support.
- A phased way to validate decisions and manage change.""",
                        ),
                        (
                            f"Choosing the right scope for {title.lower()}",
                            f"""A useful scope for {title.lower()} starts with the work that matters most, not a feature list built without context.

## Decisions to make early
- Which users and workflows should the first release support?
- Which existing tools should be connected, retained or replaced?
- What should stay manual until the team has more evidence?
- Who will own the solution after the initial delivery?""",
                        ),
                        (
                            f"Reviewing progress on {title.lower()}",
                            f"""Teams can keep {title.lower()} on track by connecting delivery checkpoints to observable outcomes and operational readiness.

## A practical review
- Confirm that agreed user journeys work end to end.
- Review open dependencies, risks and decisions with their owners.
- Check support, access and documentation before handover.
- Use feedback to prioritize the next improvement.""",
                        ),
                    ],
                    "faqs": [
                        (
                            f"How do we start with {title.lower()}?",
                            "We begin with a conversation about the goal, current systems and constraints. From there, we recommend a focused next step.",
                        ),
                        (
                            "Can you work with our existing team and tools?",
                            "Yes. We plan around your current environment and agree responsibilities with your team before work begins.",
                        ),
                    ],
                }
            )
    return pages


def build_domain_pages(categories, domain):
    """Build starter CMS content for solution or industry navigation pages."""
    pages = []
    for category in categories:
        for order, title in enumerate(category["items"]):
            slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
            if domain == "solution" and slug in {"bi-data-analytics"}:
                pass
            elif domain == "solution" and slug == "ai-consulting":
                pass
            elif domain == "industry" and slug == "e-commerce":
                slug = "e-commerce-industry"
            pages.append(
                {
                    "group_slug": category["slug"],
                    "group_name": category["name"],
                    "group_order": category["order"],
                    "slug": slug,
                    "title": title,
                    "short": title[:40],
                    "order": order,
                    "design": category["design"],
                    "domain": domain,
                    "tagline": (
                        f"Practical {domain} technology for the needs and day-to-day "
                        f"work of {title.lower()}."
                    ),
                    "intro": (
                        f"{title} teams work with specific users, processes and "
                        "operational constraints. Digital tools should fit that context "
                        "and make important tasks easier to complete.\n\n"
                        f"Our {domain} work starts by understanding those needs. We "
                        f"then shape software and data solutions around {category['focus']}, "
                        "with a clear scope and room to adapt as requirements become clearer."
                    ),
                    "features": [
                        (
                            "Understand the context",
                            f"Map the users, workflows and priorities that shape {title.lower()}.",
                        ),
                        (
                            "Design around real needs",
                            f"Plan practical capabilities for {category['focus']}.",
                        ),
                        (
                            "Connect the experience",
                            "Consider data, integrations, accessibility and ongoing support from the start.",
                        ),
                    ],
                    "steps": [
                        ("Listen", f"Learn how people currently work in {title.lower()}."),
                        ("Define", "Agree the user needs, boundaries and measures of success."),
                        ("Design", "Shape the experience and technical plan with the people involved."),
                        ("Deliver", "Build, review and improve the solution in manageable stages."),
                    ],
                    "deliverables": [
                        f"A needs and workflow brief for {title.lower()}",
                        "A prioritized feature and integration outline",
                        "A phased delivery plan",
                        "Recommendations for support and future improvements",
                    ],
                    "audience": [
                        f"Organizations serving users in {title.lower()}",
                        "Teams improving an existing digital service",
                        "Leaders planning a new digital initiative",
                    ],
                    "sections": [
                        (
                            f"Designed for {title.lower()}",
                            f"""Useful technology starts with a clear picture of the work and the people it supports.

## What we consider
- The needs of customers, staff and other stakeholders.
- Existing processes, systems and data.
- Privacy, security, accessibility and operational continuity.
- A practical way to validate the solution before expanding it.""",
                        ),
                        (
                            f"Account for day-to-day work in {title.lower()}",
                            f"""A digital experience for {title.lower()} needs to fit the responsibilities and conditions of the people who use and support it.

## Operating details to explore
- Different user roles, permissions and accessibility needs.
- Busy periods, hand-offs, exceptions and offline constraints.
- Existing records, integrations and sources of truth.
- Training and support for people adopting a changed process.""",
                        ),
                        (
                            f"Validate outcomes with {title.lower()} users",
                            f"""Before broad rollout, involve representative {title.lower()} users in a realistic review of the proposed experience. Their feedback can reveal missing steps and unclear terminology early.

## Useful validation activities
- Walk through common and exception scenarios.
- Check that information is understandable and actionable.
- Review privacy, security and accessibility needs.
- Capture feedback and agree what changes before expansion.""",
                        ),
                    ],
                    "faqs": [
                        (
                            f"Can the solution fit our {title.lower()} workflow?",
                            "Yes. Discovery focuses on your actual users and workflow so the proposed scope fits your operating context.",
                        ),
                        (
                            "Can you work with our current systems?",
                            "We review available integrations and constraints early, then plan a suitable approach with your team.",
                        ),
                    ],
                }
            )
    return pages


def build_ai_pages():
    """Build starter CMS content for AI menu pages and their layout details."""
    pages = []
    for category_index, category in enumerate(AI_CATEGORIES):
        for order, title in enumerate(category["items"]):
            slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
            if slug == "ai-product-development":
                slug = "ai-product-development-for-business"
            pages.append(
                {
                    "group_slug": category["slug"],
                    "group_name": category["name"],
                    "group_order": category["order"],
                    "slug": slug,
                    "title": title,
                    "short": title[:40],
                    "order": order,
                    "design": "ai",
                    "ai_layout": category_index * len(category["items"]) + order,
                    "tagline": (
                        f"Make {title.lower()} useful to your organization with a "
                        f"practical approach to {category['focus']}."
                    ),
                    "intro": (
                        f"{title} can help when it addresses a real need and fits the "
                        "way people work. We begin by understanding the intended users, "
                        "data, systems and constraints before recommending an approach.\n\n"
                        f"Our work around {category['focus']} balances useful outcomes "
                        "with reliability, privacy, security and human oversight. "
                        "We shape the scope with your team and validate important "
                        "assumptions before scaling."
                    ),
                    "features": [
                        (
                            "Use-case discovery",
                            f"Clarify where {title.lower()} can assist users and what a useful result looks like.",
                        ),
                        (
                            "Solution design",
                            f"Choose a suitable model, data flow and integration approach for {category['focus']}.",
                        ),
                        (
                            "Evaluation and safeguards",
                            "Plan quality checks, privacy controls, human review and ongoing monitoring.",
                        ),
                    ],
                    "steps": [
                        ("Discover", "Understand users, workflows, data and the outcome to improve."),
                        ("Design", "Compare implementation options and agree boundaries and safeguards."),
                        ("Prototype", f"Test the core {title.lower()} experience with representative examples."),
                        ("Evaluate", "Review quality, risks and operational needs before expanding the scope."),
                    ],
                    "deliverables": [
                        f"A use-case and scope brief for {title.lower()}",
                        "A solution outline covering models, data and integrations",
                        "An evaluation plan with human review and safety checks",
                        "A phased implementation and operations roadmap",
                    ],
                    "audience": [
                        "Teams exploring a practical AI use case",
                        "Product and engineering groups integrating AI into existing work",
                        "Leaders seeking a clear plan for responsible adoption",
                    ],
                    "sections": [
                        (
                            f"Build around the people using {title.lower()}",
                            f"""AI should make a task clearer or more useful, not add another opaque step. We consider the complete experience around {title.lower()}.

## What we plan for
- Data access, quality, privacy and permissions.
- Clear user feedback and appropriate human review.
- Quality evaluation across realistic examples.
- Monitoring, maintenance and a safe path to update the system.""",
                        ),
                        (
                            f"Evaluate {title.lower()} before expanding",
                            f"""Evaluation for {title.lower()} should reflect the task, users, and conditions where the system will operate. A small, reviewed set of representative examples can uncover gaps before a wider pilot.

## Evaluation essentials
- Include routine, ambiguous and out-of-scope examples.
- Review factuality, relevance and failure behavior.
- Decide where human approval or escalation is required.
- Record limitations and criteria for pausing expansion.""",
                        ),
                        (
                            f"Prepare {title.lower()} for ongoing operations",
                            f"""The quality of {title.lower()} can change when models, data, prompts, integrations or users change. Assign ownership for monitoring and a process for reviewing meaningful updates.

## Plan beyond launch
- Track quality and operational issues over time.
- Keep system changes and evaluation results reviewable.
- Make it possible to pause or roll back a release.
- Revisit access, privacy and retention as the use evolves.""",
                        ),
                    ],
                    "faqs": [
                        (
                            f"What is a good first step for {title.lower()}?",
                            "Start with a specific user problem and a small set of examples. A focused discovery or prototype can help test fit before broader investment.",
                        ),
                        (
                            "How do you address AI accuracy and privacy?",
                            "We define evaluation criteria, review data handling and permissions, and identify where people should validate or approve outputs.",
                        ),
                    ],
                }
            )
    return pages
