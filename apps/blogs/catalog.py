"""Editorial resource content for the public Resources hub."""

RESOURCES = [
    {
        "slug": "responsible-ai-in-healthcare",
        "title": "Responsible AI in Healthcare: A Practical Starting Point",
        "category": "Healthcare",
        "topic": "technology",
        "kind": "article",
        "read_time": "7 min read",
        "excerpt": "A practical way to explore clinical and operational AI without losing sight of privacy, safety, and human judgment.",
        "image": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1200&q=85",
        "image_alt": "Healthcare professional reviewing patient information on a tablet",
        "sections": [
            {
                "heading": "Start with a workflow, not a model",
                "paragraphs": [
                    "Healthcare teams can find opportunities for AI in documentation, scheduling, information retrieval, and decision support. The useful starting point is a clearly bounded workflow and the people who rely on it.",
                    "Map where information enters, who reviews it, and what happens when the system is uncertain. This reveals whether automation can reduce friction without creating a new source of risk.",
                ],
                "bullets": [
                    "Define the intended user and decision.",
                    "Separate administrative assistance from clinical recommendations.",
                    "Document escalation and correction paths before a pilot.",
                ],
            },
            {
                "heading": "Treat data handling as part of product design",
                "paragraphs": [
                    "Sensitive data should not be collected simply because it is available. Decide what information is necessary, where it may be processed, who can access it, and how long it should be retained.",
                    "A data-flow map helps teams review permissions, vendor boundaries, audit needs, and de-identification options before implementation choices become difficult to change.",
                ],
                "bullets": [
                    "Use the minimum data needed for the defined task.",
                    "Keep access tied to a clear role and purpose.",
                    "Plan retention, deletion, and audit review.",
                ],
            },
            {
                "heading": "Evaluate with people in the loop",
                "paragraphs": [
                    "A promising demonstration does not prove that a system is reliable in everyday care. Evaluate representative cases, including incomplete, unusual, and ambiguous inputs, and make it easy for qualified staff to correct outputs.",
                    "Agree on measurable acceptance criteria with clinical, operational, security, and product stakeholders. Expand only when the evidence supports the intended use.",
                ],
                "bullets": [
                    "Compare outputs against a reviewed reference set.",
                    "Track errors and near misses, not just average quality.",
                    "Reassess performance when workflows or data change.",
                ],
            },
        ],
    },
    {
        "slug": "enterprise-ai-readiness-checklist",
        "title": "An Enterprise AI Readiness Checklist",
        "category": "Artificial Intelligence",
        "topic": "business",
        "kind": "guide",
        "read_time": "8 min read",
        "excerpt": "Use these questions to assess whether a team, process, and data set are ready for a useful AI pilot.",
        "image": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1200&q=85",
        "image_alt": "Team planning an initiative around a table",
        "sections": [
            {
                "heading": "Business purpose",
                "paragraphs": [
                    "Readiness starts with a problem statement that is specific enough to evaluate. Name the user, the task, the current friction, and the outcome that would make a change worthwhile.",
                ],
                "bullets": [
                    "Is the task frequent, costly, slow, or difficult to scale?",
                    "Can the team describe a successful result in observable terms?",
                    "Is AI preferable to a simpler workflow or rules-based improvement?",
                ],
            },
            {
                "heading": "Data and operating conditions",
                "paragraphs": [
                    "A pilot depends on more than model access. Teams need appropriate data permissions, a clear owner, and an understanding of how the system will fit into existing tools.",
                ],
                "bullets": [
                    "Are data sources documented and authorized for this purpose?",
                    "Can sensitive information be minimized or protected?",
                    "Who will support, monitor, and maintain the pilot?",
                ],
            },
            {
                "heading": "Risk and evaluation",
                "paragraphs": [
                    "Set boundaries before a system is placed in front of users. Define which decisions remain human-owned, how a user can question an output, and what evidence is required to proceed.",
                ],
                "bullets": [
                    "Have failure modes and fallback behavior been reviewed?",
                    "Is there a representative evaluation set and a named reviewer?",
                    "Are launch, pause, and rollback criteria agreed?",
                ],
            },
        ],
    },
    {
        "slug": "cloud-cost-controls-without-slowing-delivery",
        "title": "Cloud Cost Controls Without Slowing Delivery",
        "category": "Cloud",
        "topic": "technology",
        "kind": "article",
        "read_time": "6 min read",
        "excerpt": "A lightweight operating model for understanding cloud spend and making cost ownership part of engineering work.",
        "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=85",
        "image_alt": "Connected digital network representing cloud infrastructure",
        "sections": [
            {
                "heading": "Make spend understandable",
                "paragraphs": [
                    "A monthly cloud invoice rarely explains which product decision caused a change. Organize accounts, tags, and reporting around teams or workloads so engineers and product owners can connect usage to the services they operate.",
                    "Start with a small number of consistent dimensions. Naming and ownership conventions are more valuable than an elaborate dashboard that teams cannot maintain.",
                ],
                "bullets": [
                    "Assign an owner to each production workload.",
                    "Separate shared platform costs from team-owned services.",
                    "Review trends and unusual changes on a regular cadence.",
                ],
            },
            {
                "heading": "Prioritize reversible improvements",
                "paragraphs": [
                    "Rightsizing, storage lifecycle policies, and removing idle resources can often be tested safely. Changes to reliability or performance assumptions need more careful review.",
                    "Pair cost observations with service-level indicators so savings do not come at the expense of availability or user experience.",
                ],
                "bullets": [
                    "Use observed demand rather than peak guesses.",
                    "Test changes in a representative environment.",
                    "Keep a clear rollback path for production changes.",
                ],
            },
            {
                "heading": "Build cost awareness into delivery",
                "paragraphs": [
                    "Cost review works best as part of normal engineering decisions, not as a last-minute finance exercise. Teams can include likely operating costs in architecture reviews and revisit them as usage changes.",
                ],
                "bullets": [
                    "Discuss expected traffic and growth assumptions.",
                    "Include cost signals in service dashboards.",
                    "Treat efficiency as an ongoing reliability practice.",
                ],
            },
        ],
    },
    {
        "slug": "data-governance-for-trusted-analytics",
        "title": "Data Governance for Analytics People Can Trust",
        "category": "Data",
        "topic": "technology",
        "kind": "article",
        "read_time": "7 min read",
        "excerpt": "Practical governance habits that help teams understand where metrics come from and when they are safe to use.",
        "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=85",
        "image_alt": "Analytics dashboard with charts on a computer screen",
        "sections": [
            {
                "heading": "Give important data a clear owner",
                "paragraphs": [
                    "When a report is questioned, teams need to know who can explain the source, definition, and limitations of its data. Ownership does not mean one person manages every dataset; it means responsibilities are visible.",
                ],
                "bullets": [
                    "Name a business steward for high-value datasets.",
                    "Document source systems and refresh expectations.",
                    "Create a route for reporting quality concerns.",
                ],
            },
            {
                "heading": "Define metrics once and explain them",
                "paragraphs": [
                    "Two dashboards can show different answers because teams use the same label for different calculations. A shared metric definition should explain its purpose, calculation, time window, and exclusions.",
                    "Definitions should be understandable to the people making decisions, not only to the team that built the pipeline.",
                ],
                "bullets": [
                    "Maintain a plain-language data dictionary.",
                    "Show when data was last refreshed.",
                    "Make known limitations visible beside the metric.",
                ],
            },
            {
                "heading": "Apply access according to purpose",
                "paragraphs": [
                    "Reliable analytics also requires appropriate access. Classify data according to sensitivity and make permissions reflect the work a user needs to do.",
                ],
                "bullets": [
                    "Review access as roles and projects change.",
                    "Use aggregated or masked information where possible.",
                    "Keep a record of important access and quality decisions.",
                ],
            },
        ],
    },
    {
        "slug": "secure-digital-banking-product-design",
        "title": "Security Considerations for Digital Banking Products",
        "category": "Finance & Banking",
        "topic": "industry",
        "kind": "article",
        "read_time": "7 min read",
        "excerpt": "A product-focused look at identity, transaction journeys, operational controls, and safe change in financial services.",
        "image": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=1200&q=85",
        "image_alt": "Secure online banking displayed on a laptop",
        "sections": [
            {
                "heading": "Design identity around real user journeys",
                "paragraphs": [
                    "Authentication and recovery are part of the product experience. Teams should understand how users enroll, change devices, recover access, and receive help when something looks wrong.",
                    "Controls should be proportionate to the action and risk, while remaining accessible to legitimate users.",
                ],
                "bullets": [
                    "Map enrollment, login, recovery, and high-risk actions.",
                    "Make unusual activity and next steps understandable.",
                    "Test recovery flows as carefully as sign-in.",
                ],
            },
            {
                "heading": "Protect the transaction lifecycle",
                "paragraphs": [
                    "A transaction involves more than a submit button. Review how intent is confirmed, how status is communicated, and how the product handles retries, timeouts, and duplicate requests.",
                ],
                "bullets": [
                    "Show clear confirmation and transaction status.",
                    "Design for interrupted or repeated requests.",
                    "Keep operational logs useful without exposing unnecessary sensitive data.",
                ],
            },
            {
                "heading": "Plan for change and response",
                "paragraphs": [
                    "Dependencies, fraud patterns, and user expectations evolve. A secure product needs an accountable process for updates, incident triage, and communication with affected users.",
                ],
                "bullets": [
                    "Assign owners for critical components and vendors.",
                    "Test backup, recovery, and incident procedures.",
                    "Review security findings and remediation progress regularly.",
                ],
            },
        ],
    },
    {
        "slug": "modernization-roadmap-guide",
        "title": "A Practical Guide to Planning Platform Modernization",
        "category": "Modernization",
        "topic": "business",
        "kind": "guide",
        "read_time": "9 min read",
        "excerpt": "Plan modernization around user impact, operational constraints, and manageable increments rather than a full rewrite by default.",
        "image": "https://images.unsplash.com/photo-1497366811353-6870744d04b2?auto=format&fit=crop&w=1200&q=85",
        "image_alt": "Modern workspace with a team collaborating",
        "sections": [
            {
                "heading": "Understand the current system",
                "paragraphs": [
                    "Before choosing a target architecture, identify the capabilities the system supports, its dependencies, and the reasons it has become difficult to change.",
                    "Combine technical discovery with input from users and operators. A diagram alone cannot reveal which delays or workarounds matter most.",
                ],
                "bullets": [
                    "Map users, critical journeys, data, and integrations.",
                    "Identify operational risks and recurring maintenance work.",
                    "Separate urgent problems from assumptions about old technology.",
                ],
            },
            {
                "heading": "Compare pathways before committing",
                "paragraphs": [
                    "Modernization may involve simplifying, replacing, rehosting, replatforming, or incrementally extracting capabilities. Compare options against business outcomes, delivery risk, and the team's ability to operate the result.",
                ],
                "bullets": [
                    "Estimate migration and parallel-running effort.",
                    "Check compatibility and data transition needs.",
                    "Consider whether a smaller intervention solves the primary pain.",
                ],
            },
            {
                "heading": "Deliver in verifiable stages",
                "paragraphs": [
                    "A phased plan keeps learning close to implementation. Select a first slice that is valuable, bounded, and reversible enough to validate the architecture and delivery assumptions.",
                ],
                "bullets": [
                    "Define acceptance criteria and rollback conditions.",
                    "Measure user and operational impact after each release.",
                    "Update the roadmap as evidence replaces estimates.",
                ],
            },
        ],
    },
    {
        "slug": "ecommerce-personalization-with-care",
        "title": "E-Commerce Personalization That Respects the Customer",
        "category": "E-Commerce",
        "topic": "industry",
        "kind": "article",
        "read_time": "6 min read",
        "excerpt": "Use customer context to improve product discovery without making shopping feel intrusive or unpredictable.",
        "image": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=1200&q=85",
        "image_alt": "Customer making an online retail purchase",
        "sections": [
            {
                "heading": "Make the benefit obvious",
                "paragraphs": [
                    "Personalization is useful when it helps a customer find a relevant product, compare options, or continue a task. It becomes distracting when recommendations feel unrelated or obscure the basics of browsing.",
                ],
                "bullets": [
                    "Keep search, filters, and categories easy to use.",
                    "Explain why an item is being recommended when helpful.",
                    "Offer a clear way to dismiss or adjust preferences.",
                ],
            },
            {
                "heading": "Use signals carefully",
                "paragraphs": [
                    "Teams should understand which events and attributes inform recommendations, whether the data is appropriate for the purpose, and how long it remains useful.",
                    "Begin with low-risk signals and review the experience across new, returning, and signed-out shoppers.",
                ],
                "bullets": [
                    "Collect only signals needed for a clear experience.",
                    "Avoid sensitive inferences that customers do not expect.",
                    "Set retention and access rules for personalization data.",
                ],
            },
            {
                "heading": "Measure the full experience",
                "paragraphs": [
                    "Click-through alone can reward noisy recommendations. Review whether customers complete their task, discover appropriate alternatives, and remain able to control the journey.",
                ],
                "bullets": [
                    "Use controlled tests with clear success measures.",
                    "Monitor returns, complaints, and recommendation diversity.",
                    "Keep a straightforward fallback when personalization is unavailable.",
                ],
            },
        ],
    },
    {
        "slug": "ai-governance-operating-guide",
        "title": "A Small-Team Operating Guide to AI Governance",
        "category": "Artificial Intelligence",
        "topic": "business",
        "kind": "guide",
        "read_time": "8 min read",
        "excerpt": "A proportionate governance model for teams that need clear ownership, review, and escalation without unnecessary process.",
        "image": "https://images.unsplash.com/photo-1521737711867-e3b97375f902?auto=format&fit=crop&w=1200&q=85",
        "image_alt": "Colleagues reviewing a project together",
        "sections": [
            {
                "heading": "Create a shared inventory",
                "paragraphs": [
                    "A lightweight inventory helps an organization see where AI is being considered or used. Record the purpose, owner, users, data types, vendors, and status of each initiative.",
                ],
                "bullets": [
                    "Include prototypes as well as launched systems.",
                    "Name a business owner and a technical contact.",
                    "Record when an initiative should be reviewed again.",
                ],
            },
            {
                "heading": "Set minimum review questions",
                "paragraphs": [
                    "Not every use case needs the same approval path. A consistent first review can identify sensitive data, consequential decisions, external dependencies, and the need for human oversight.",
                ],
                "bullets": [
                    "What is the intended use and what is out of scope?",
                    "What evidence supports quality for the intended users?",
                    "How can a user report, correct, or escalate an issue?",
                ],
            },
            {
                "heading": "Keep governance active",
                "paragraphs": [
                    "Governance continues after launch. Changes to models, data, prompts, integrations, and user groups can alter the system's behavior and risk profile.",
                ],
                "bullets": [
                    "Set a review cadence based on use and risk.",
                    "Log meaningful changes and evaluation results.",
                    "Define who can pause or retire a system.",
                ],
            },
        ],
    },
    {
        "slug": "digital-health-platform-design",
        "title": "Designing Digital Health Platforms Around Care Teams",
        "category": "Healthcare",
        "topic": "industry",
        "kind": "article",
        "read_time": "6 min read",
        "excerpt": "Bring patient needs, staff workflows, interoperability, and service continuity into the same product conversation.",
        "image": "https://images.unsplash.com/photo-1584982751601-97dcc096659c?auto=format&fit=crop&w=1200&q=85",
        "image_alt": "Clinician using digital tools in a care environment",
        "sections": [
            {
                "heading": "Follow work across roles",
                "paragraphs": [
                    "A digital health journey often crosses patients, clinicians, operations, and support staff. Map how each role receives information, completes a task, and hands work to the next person.",
                ],
                "bullets": [
                    "Include users with different levels of digital confidence.",
                    "Observe workarounds as signals of unmet needs.",
                    "Design clear ownership when tasks move between teams.",
                ],
            },
            {
                "heading": "Design for continuity",
                "paragraphs": [
                    "Health services need predictable behavior during delays, outages, and handoffs. Teams should understand which functions are essential and how users can continue safely when a digital service is unavailable.",
                ],
                "bullets": [
                    "Identify critical journeys and service dependencies.",
                    "Make system status and next actions clear.",
                    "Test recovery and support processes with the team.",
                ],
            },
            {
                "heading": "Plan interoperability early",
                "paragraphs": [
                    "Integration requirements can shape the user experience and delivery plan. Confirm data ownership, exchange formats, access, and operational responsibilities with relevant partners early.",
                ],
                "bullets": [
                    "Document source-of-truth decisions.",
                    "Agree error handling and reconciliation workflows.",
                    "Validate security and privacy expectations across boundaries.",
                ],
            },
        ],
    },
    {
        "slug": "secure-product-delivery-checklist",
        "title": "Secure Product Delivery: A Practical Team Checklist",
        "category": "Cyber Security",
        "topic": "technology",
        "kind": "guide",
        "read_time": "7 min read",
        "excerpt": "Bring security checks into discovery, design, development, and operations with clear responsibilities at each stage.",
        "image": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=85",
        "image_alt": "Digital security visualization on a monitor",
        "sections": [
            {
                "heading": "At discovery and design",
                "paragraphs": [
                    "Security is easier to address when teams know what they are protecting and how the product will be used. Capture data sensitivity, user roles, external dependencies, and likely misuse cases.",
                ],
                "bullets": [
                    "Identify assets, trust boundaries, and privileged actions.",
                    "Review authentication, authorization, and recovery needs.",
                    "Record security assumptions and unresolved questions.",
                ],
            },
            {
                "heading": "During implementation",
                "paragraphs": [
                    "Build repeatable checks into the development workflow. Keep credentials out of source control, review dependencies, and make security-relevant changes visible to the team.",
                ],
                "bullets": [
                    "Use peer review and automated checks appropriate to the stack.",
                    "Keep dependencies and secrets under controlled processes.",
                    "Validate access rules at the server boundary.",
                ],
            },
            {
                "heading": "Before and after release",
                "paragraphs": [
                    "A release plan should state what has been tested, what remains accepted risk, and how the team will respond to a problem. Operational visibility is part of the security control set.",
                ],
                "bullets": [
                    "Test critical flows and permission boundaries.",
                    "Define incident ownership and escalation.",
                    "Review findings and patch progress after release.",
                ],
            },
        ],
    },
    {
        "slug": "data-platform-modernization-report",
        "title": "Data Platform Modernization: Questions for the Roadmap",
        "category": "Data",
        "topic": "reports",
        "kind": "report",
        "read_time": "10 min read",
        "excerpt": "A decision framework for teams weighing analytics reliability, governance, migration effort, and future needs.",
        "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=85",
        "image_alt": "Business analytics dashboard with charts and figures",
        "sections": [
            {
                "heading": "What is limiting the current platform?",
                "paragraphs": [
                    "A modernization case should describe the friction users experience and the operational cost of the current approach. Examples include delayed reporting, duplicated transformations, unclear data ownership, or a growing maintenance burden.",
                ],
                "bullets": [
                    "Which decisions are delayed or difficult to trust?",
                    "Where do teams repeatedly repair or reconcile data?",
                    "Which capabilities are needed that the current platform cannot support?",
                ],
            },
            {
                "heading": "What should the target enable?",
                "paragraphs": [
                    "Define target capabilities before selecting products. Teams may need reliable ingestion, shared definitions, self-service exploration, or stronger lineage and access controls.",
                ],
                "bullets": [
                    "Describe user-facing and operational outcomes.",
                    "Clarify governance and data protection requirements.",
                    "Separate essential capabilities from optional features.",
                ],
            },
            {
                "heading": "How can change be staged?",
                "paragraphs": [
                    "A staged roadmap reduces the risk of replacing too much at once. Choose a representative use case, migrate it with validation, and use the findings to refine the next stage.",
                ],
                "bullets": [
                    "Plan parallel checks for critical outputs.",
                    "Identify ownership for data contracts and quality.",
                    "Set explicit migration and retirement criteria.",
                ],
            },
        ],
    },
    {
        "slug": "product-roadmap-from-user-evidence",
        "title": "Turning User Evidence into a Product Roadmap",
        "category": "Product Strategy",
        "topic": "business",
        "kind": "article",
        "read_time": "6 min read",
        "excerpt": "Connect customer feedback, business objectives, and delivery capacity to a roadmap teams can explain and adapt.",
        "image": "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1200&q=85",
        "image_alt": "Product team collaborating around a planning board",
        "sections": [
            {
                "heading": "Separate observations from solutions",
                "paragraphs": [
                    "A request describes one person's proposed answer. The underlying observation explains the task, context, and obstacle that led to the request. Keeping those separate opens up more useful options.",
                ],
                "bullets": [
                    "Record who is affected and in what situation.",
                    "Look for repeated patterns across support and research.",
                    "Keep assumptions visible until they are tested.",
                ],
            },
            {
                "heading": "Prioritize with explicit trade-offs",
                "paragraphs": [
                    "A roadmap is a set of choices under constraints. Teams can compare customer impact, strategic fit, effort, dependencies, and uncertainty without pretending every estimate is exact.",
                ],
                "bullets": [
                    "Use a small set of criteria consistently.",
                    "Identify dependencies and opportunity costs.",
                    "Explain why a promising idea is not scheduled yet.",
                ],
            },
            {
                "heading": "Keep the roadmap revisable",
                "paragraphs": [
                    "Communicate near-term commitments separately from longer-term direction. Revisit priorities when evidence, capacity, or business conditions change.",
                ],
                "bullets": [
                    "Review outcomes after releases.",
                    "Retire assumptions that no longer hold.",
                    "Share changes with the people affected by them.",
                ],
            },
        ],
    },
]

RESOURCE_TOPICS = [
    ("all", "All"),
    ("technology", "Technology"),
    ("business", "Business"),
    ("industry", "Industries"),
    ("guides", "Guides"),
    ("reports", "Reports"),
]


def get_resource(slug):
    return next((resource for resource in RESOURCES if resource["slug"] == slug), None)
