"""Industry case-study landing page content."""

INDUSTRY_CASE_STUDIES = [
    {
        "slug": "healthcare",
        "name": "Healthcare",
        "eyebrow": "Care delivery",
        "title": "Digital experiences that give care teams more room to care",
        "summary": "Explore practical ways to connect patient journeys, clinical workflows, and healthcare operations through secure, usable digital products.",
        "image": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1400&q=85",
        "image_alt": "Healthcare professional reviewing patient information on a tablet",
        "challenge": "Healthcare services often rely on disconnected systems, manual coordination, and repeated data entry. These gaps can make it harder for patients to navigate care and for teams to see the information they need.",
        "approach": "Begin with the people and hand-offs in a care journey. Map where information is created, reviewed, and acted on, then prioritize improvements with clinical, operations, privacy, and technology stakeholders.",
        "capabilities": [
            ("Patient access", "Appointment, intake, and follow-up experiences designed around clear next steps."),
            ("Care-team workflows", "Tools that support coordination, task visibility, and less repetitive administration."),
            ("Connected information", "Interoperability planning that respects source systems, permissions, and data quality."),
            ("Responsible AI", "Bounded assistance with human review, evaluation, and safeguards appropriate to the use."),
        ],
        "considerations": [
            "Protect sensitive information and limit access to the intended purpose.",
            "Design accessible experiences for different devices and levels of digital confidence.",
            "Keep clinical decisions with qualified professionals unless a specific approved use says otherwise.",
        ],
    },
    {
        "slug": "fintech",
        "name": "FinTech",
        "eyebrow": "Financial services",
        "title": "Build financial products around trust at every interaction",
        "summary": "Design secure digital banking, payments, and financial operations with clear user journeys and resilient systems.",
        "image": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=1400&q=85",
        "image_alt": "Secure digital banking displayed on a laptop",
        "challenge": "Financial products must balance low-friction experiences with strong identity, transaction integrity, privacy, and operational controls. Fragmented journeys can create confusion for users and additional support work.",
        "approach": "Trace key paths such as onboarding, authentication, payment, account recovery, and support. Review risk boundaries and dependencies while prototyping the experience, then validate error handling and operational readiness.",
        "capabilities": [
            ("Digital banking", "Account and service experiences with understandable status and next actions."),
            ("Payments and integrations", "Transaction journeys designed for retries, reconciliation, and clear confirmation."),
            ("Identity and access", "Authentication, permissions, and recovery planned around user needs and risk."),
            ("Operational visibility", "Monitoring and support workflows that help teams respond to service issues."),
        ],
        "considerations": [
            "Treat security and privacy as product requirements from discovery through operations.",
            "Make fees, transaction states, and recovery choices easy to understand.",
            "Review applicable regulatory and compliance requirements with qualified specialists.",
        ],
    },
    {
        "slug": "e-commerce",
        "name": "E-Commerce",
        "eyebrow": "Digital commerce",
        "title": "Create shopping journeys that work from discovery to delivery",
        "summary": "Connect storefronts, catalog, checkout, inventory, and customer support into a coherent commerce experience.",
        "image": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=1400&q=85",
        "image_alt": "Customer making an online retail purchase",
        "challenge": "Commerce teams can lose customers when product information is inconsistent, checkout is difficult, inventory is unclear, or service teams cannot see order context. Adding features without fixing those hand-offs can add complexity.",
        "approach": "Map the complete shopping and fulfillment journey, including catalog ownership, stock updates, payment, delivery, returns, and customer support. Prioritize improvements that remove friction and remain manageable for the operating team.",
        "capabilities": [
            ("Storefronts and marketplaces", "Responsive shopping experiences supported by clear catalog structures."),
            ("Checkout and payments", "Focused checkout flows with understandable validation and order confirmation."),
            ("Inventory and fulfillment", "Integration planning for stock, delivery, order status, and returns."),
            ("Personalization", "Relevant discovery features with customer choice and thoughtful data use."),
        ],
        "considerations": [
            "Keep browsing and checkout usable on mobile devices and assistive technology.",
            "Plan for payment failures, unavailable items, returns, and interrupted sessions.",
            "Use customer data transparently and only where it supports a clear purpose.",
        ],
    },
    {
        "slug": "education",
        "name": "Education",
        "eyebrow": "Learning experiences",
        "title": "Make learning platforms easier to use for every participant",
        "summary": "Support learners, educators, and administrators with connected digital learning and education operations.",
        "image": "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=1400&q=85",
        "image_alt": "Educators collaborating around a learning plan",
        "challenge": "Learning can be spread across platforms for course delivery, communication, assessment, and administration. Inconsistent access and duplicated workflows make it harder for learners and educators to focus on progress.",
        "approach": "Understand the needs of learners, instructors, administrators, and support teams. Map the learning lifecycle and existing systems, then design a focused experience with clear access, feedback, and reporting.",
        "capabilities": [
            ("Learning platforms", "Course discovery, learning paths, and content experiences across devices."),
            ("Virtual classrooms", "Tools for sessions, participation, collaboration, and follow-up."),
            ("Assessment and feedback", "Clear workflows for assignments, review, progress, and communication."),
            ("Education operations", "Administrative tools and integrations that reduce repeated coordination."),
        ],
        "considerations": [
            "Make learning content and navigation accessible to a broad range of users.",
            "Protect learner information and clarify who can access records.",
            "Design for varied connectivity, devices, schedules, and support needs.",
        ],
    },
    {
        "slug": "logistics",
        "name": "Logistics",
        "eyebrow": "Connected operations",
        "title": "Give logistics teams a clearer view from dispatch to delivery",
        "summary": "Connect planning, fleet, warehouse, and customer updates around reliable operational information.",
        "image": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=1400&q=85",
        "image_alt": "Logistics operations and supply chain coordination",
        "challenge": "Logistics work depends on timely coordination across vehicles, warehouses, partners, and customers. Delayed or inconsistent updates make it difficult to respond to exceptions and communicate realistic delivery information.",
        "approach": "Trace how an order or shipment moves through planning, dispatch, hand-offs, and delivery. Identify the systems and people responsible for each update, then design integration and exception workflows around real operating conditions.",
        "capabilities": [
            ("Shipment visibility", "Status experiences that bring events and next actions into one place."),
            ("Fleet and dispatch", "Operational tools for assignments, schedules, and exception handling."),
            ("Warehouse coordination", "Inventory and fulfillment workflows connected to upstream and downstream systems."),
            ("Partner integrations", "Data exchange planning for carriers, suppliers, customers, and internal platforms."),
        ],
        "considerations": [
            "Design for changing network conditions and delayed or duplicated events.",
            "Make exceptions actionable, with clear ownership and escalation.",
            "Protect location, customer, and commercial data with appropriate access controls.",
        ],
    },
]


def get_industry_case_study(slug):
    return next(
        (study for study in INDUSTRY_CASE_STUDIES if study["slug"] == slug),
        None,
    )
