from __future__ import annotations

import os
from datetime import date
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, send_file, send_from_directory, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
RESUME_DIR = BASE_DIR / "resume"
GOOGLE_VERIFICATION_FILENAME = "google06484969bd287b9c.html"
REQUIRED_DIRECTORIES = (
    TEMPLATES_DIR,
    STATIC_DIR,
    STATIC_DIR / "css",
    STATIC_DIR / "js",
    STATIC_DIR / "images",
    RESUME_DIR,
)


CONTACT = {
    "name": "Pavilson S",
    "headline": "AI-Powered Software Developer",
    "phone": "+91 8667840473",
    "phone_link": "tel:+918667840473",
    "email": "pavilson7@gmail.com",
    "email_link": "mailto:pavilson7@gmail.com",
    "country": "India",
    "linkedin": "https://www.linkedin.com/in/pavilson-s-b86500326/",
}

QUICK_PROMPTS = [
    "Tell me about Pavilson S.",
    "Explain the MindNest AI Application.",
    "Summarize the internship experience.",
    "How can I contact Pavilson?",
    "What skills does Pavilson bring?",
    "Help me download the resume.",
]

RESUME_FILENAME = "Pavilson_Software_Developer_Resume.pdf"
CERTIFICATE_FILENAME = "images/Pavilson_Canza_Internship_Certificate.jpg"
PROFILE_FILENAME = "images/pavilson-profile.png"

NAV_ITEMS = [
    {"id": "about", "label": "About"},
    {"id": "skills", "label": "Skills"},
    {"id": "experience", "label": "Experience"},
    {"id": "projects", "label": "Projects"},
    {"id": "certifications", "label": "Certifications"},
    {"id": "assistant", "label": "AI Assistant"},
    {"id": "contact", "label": "Contact"},
    {"id": "resume", "label": "Resume"},
]

HERO_STATS = [
    {"value": "Python + AI", "label": "Backend-first engineering with intelligent product thinking"},
    {"value": "Intern Ready", "label": "Positioned for recruiter conversations, interviews, and fast onboarding"},
    {"value": "Flask Deployed", "label": "Architecture prepared for production hosting and static asset delivery"},
]

ABOUT_PANELS = [
    {
        "title": "Software systems",
        "copy": "Pavilson builds structured backend systems, recruiter-friendly product experiences, and scalable web apps with a strong Python foundation.",
    },
    {
        "title": "AI integration",
        "copy": "His portfolio direction blends machine learning, NLP, LLM workflows, and practical software delivery into one modern developer identity.",
    },
    {
        "title": "Career focus",
        "copy": "He is actively targeting software developer, backend engineer, full stack, and AI-focused roles where he can grow through real product execution.",
    },
]

SKILL_GROUPS = [
    {
        "label": "Programming",
        "title": "Python-first engineering core",
        "copy": "Comfortable shipping full applications with Python while using JavaScript and SQL to complete product workflows end to end.",
        "skills": ["Python", "JavaScript", "SQL", "Data Structures", "Problem Solving"],
    },
    {
        "label": "Backend",
        "title": "API and application architecture",
        "copy": "Focused on clean routes, maintainable backend logic, authentication, request handling, and deployment-minded Flask services.",
        "skills": ["Flask", "Django", "FastAPI", "REST APIs", "Authentication", "JSON APIs"],
    },
    {
        "label": "Frontend",
        "title": "Modern responsive interfaces",
        "copy": "Builds polished web experiences with clear interaction design, smooth motion, and structured UI delivery.",
        "skills": ["HTML", "CSS", "JavaScript", "Responsive Design", "UI Animation"],
    },
    {
        "label": "AI / ML",
        "title": "Intelligent application workflows",
        "copy": "Applies NLP, model inference, LLM-enabled assistance, and computer vision thinking to real use cases.",
        "skills": ["NLP", "Machine Learning", "LLM Integration", "Computer Vision", "Model Deployment"],
    },
    {
        "label": "Data",
        "title": "Reliable storage and performance",
        "copy": "Works comfortably with relational data structures, schema thinking, and query optimization fundamentals.",
        "skills": ["MySQL", "Query Optimization", "Data Modeling", "CRUD Workflows", "Database Integration"],
    },
    {
        "label": "Delivery",
        "title": "Hosting and collaboration readiness",
        "copy": "Prepared for production deployment, recruiter review, static asset routing, and collaborative team workflows.",
        "skills": ["Git", "GitHub Workflow", "Render", "Railway", "Vercel", "Production Debugging"],
    },
]

EXPERIENCE = {
    "title": "Software Development Intern",
    "company": "CANZA Technology Consultants",
    "summary": (
        "Hands-on exposure to backend engineering, API architecture, authentication, database operations, "
        "AI-oriented workflows, and production-style software delivery."
    ),
    "points": [
        "Built and improved REST API workflows using Flask, Django, and FastAPI in structured application environments.",
        "Worked on authentication, authorization, and secure backend logic for real multi-user product scenarios.",
        "Contributed to AI-oriented workflows involving NLP thinking, LLM integration patterns, and intelligent feature delivery.",
        "Supported MySQL operations and query optimization to improve application responsiveness and reliability.",
        "Strengthened understanding of debugging, maintainable code structure, deployment flow, and team collaboration.",
        "Gained confidence translating academic learning into recruiter-ready software engineering outcomes.",
    ],
    "stack": ["Flask", "Django", "FastAPI", "REST APIs", "Role-Based Auth", "NLP", "LLM Workflows", "MySQL", "Deployment"],
}

PROJECTS = [
    {
        "slug": "mindnest",
        "name": "MindNest AI Application",
        "tag": "AI Product Experience",
        "summary": "An AI-assisted application experience focused on contextual guidance, product-grade backend logic, and conversational workflows.",
        "details": [
            "Combines structured APIs with intelligent assistant behavior for a polished software experience.",
            "Reflects Pavilson's interest in merging backend engineering with practical AI product thinking.",
            "Shows how recruiter-facing demos can explain architecture, user flow, and business value together.",
        ],
        "stack": ["Python", "FastAPI", "LLM Workflow", "NLP", "MySQL"],
        "shot_class": "shot-mindnest",
        "shot_title": "AI workflow console",
        "shot_lines": ["92%", "80%", "68%"],
        "shot_metrics": [
            {"value": "LLM", "label": "guided flows"},
            {"value": "API", "label": "modular services"},
        ],
        "repo_prompt": "Explain the architecture of MindNest AI Application.",
        "demo_prompt": "Give me a recruiter demo walkthrough of MindNest AI Application.",
    },
    {
        "slug": "brain-tumor",
        "name": "Brain Tumor Detection",
        "tag": "AI for Healthcare",
        "summary": "A machine-learning project centered on image analysis, classification flow, and assistive decision support for medical imaging scenarios.",
        "details": [
            "Built around preprocessing, model inference, and result interpretation for image-based predictions.",
            "Demonstrates applied AI thinking in a meaningful healthcare-related problem space.",
            "Highlights the ability to connect technical experimentation with real-world impact narratives.",
        ],
        "stack": ["Python", "Deep Learning", "Computer Vision", "Image Processing", "Model Inference"],
        "shot_class": "shot-tumor",
        "shot_title": "scan classification preview",
        "shot_lines": ["88%", "74%", "56%"],
        "shot_metrics": [
            {"value": "CV", "label": "image pipeline"},
            {"value": "ML", "label": "assistive output"},
        ],
        "repo_prompt": "Explain the Brain Tumor Detection project in interview style.",
        "demo_prompt": "Give me a recruiter walkthrough of Brain Tumor Detection.",
    },
    {
        "slug": "drowsiness",
        "name": "Driver Drowsiness Detection",
        "tag": "Real-Time Safety AI",
        "summary": "A safety-oriented intelligent system designed to detect fatigue signals and support timely alert-based intervention.",
        "details": [
            "Explores computer vision in a real-time inference setting with practical safety relevance.",
            "Shows product thinking around monitoring, alerting, and usable AI system behavior.",
            "Strengthens Pavilson's software profile beyond standard CRUD applications.",
        ],
        "stack": ["Python", "Computer Vision", "Real-Time Detection", "Machine Learning"],
        "shot_class": "shot-drowsy",
        "shot_title": "fatigue alert monitor",
        "shot_lines": ["84%", "72%", "52%"],
        "shot_metrics": [
            {"value": "RT", "label": "vision checks"},
            {"value": "Safe", "label": "alert logic"},
        ],
        "repo_prompt": "Explain the Driver Drowsiness Detection project.",
        "demo_prompt": "Give me a recruiter demo walkthrough of Driver Drowsiness Detection.",
    },
    {
        "slug": "eration",
        "name": "E-Ration System",
        "tag": "Full Stack Public Service Flow",
        "summary": "A structured digital system for managing beneficiary workflows, secure access, and operational administration in a real-world service model.",
        "details": [
            "Focuses on role-based workflows, data handling, and secure administrative operations.",
            "Represents strong full stack thinking for an organized and practical software use case.",
            "Shows backend and data-design discipline in a meaningful public-service scenario.",
        ],
        "stack": ["Python", "Flask", "MySQL", "Role-Based Auth", "Full Stack"],
        "shot_class": "shot-ration",
        "shot_title": "beneficiary ops dashboard",
        "shot_lines": ["90%", "78%", "60%"],
        "shot_metrics": [
            {"value": "RBAC", "label": "secure flows"},
            {"value": "Data", "label": "records and access"},
        ],
        "repo_prompt": "Explain the E-Ration System project in a recruiter-friendly way.",
        "demo_prompt": "Give me a recruiter demo walkthrough of the E-Ration System.",
    },
    {
        "slug": "curio-mind",
        "name": "Curio Mind Learning Platform",
        "tag": "AI-Enhanced EdTech",
        "summary": "A personalized learning platform concept that blends web development, adaptive user flow, and intelligent recommendations.",
        "details": [
            "Designed around learner-centered experience, structured content flow, and smart personalization.",
            "Shows interest in products where software design and AI-enhanced decision support work together.",
            "Positions Pavilson as a developer who can think beyond backend tasks into user impact and product direction.",
        ],
        "stack": ["Python", "JavaScript", "Flask", "MySQL", "AI Personalization"],
        "shot_class": "shot-curio",
        "shot_title": "adaptive learning stream",
        "shot_lines": ["86%", "70%", "58%"],
        "shot_metrics": [
            {"value": "UX", "label": "learner flow"},
            {"value": "AI", "label": "smart recommendations"},
        ],
        "repo_prompt": "Explain the Curio Mind Learning Platform.",
        "demo_prompt": "Give me a recruiter walkthrough of Curio Mind Learning Platform.",
    },
]

CERTIFICATIONS = [
    {
        "title": "Software Development Internship Certificate",
        "issuer": "CANZA Technology Consultants",
        "summary": "Verified internship recognition covering practical backend, API, and AI-oriented development exposure.",
        "badge": "Verified certificate",
    }
]

ASSISTANT_FEATURES = [
    "Answers interview-style questions in polished natural language",
    "Explains projects, internship experience, certifications, and technical stack",
    "Guides recruiters to resume, contact, and relevant sections instantly",
    "Acts as a smart portfolio concierge called Pavilson Is Here",
]


def get_response(user_message: str) -> dict:
    normalized = user_message.casefold()

    if "mindnest" in normalized:
        return {
            "response": (
                "MindNest AI Application highlights product-minded AI development. "
                "It combines backend structure, API workflows, and intelligent interaction in a recruiter-friendly way."
            ),
            "actions": [
                {"kind": "navigate", "value": "projects", "label": "View projects"},
                {"kind": "navigate", "value": "assistant", "label": "Open assistant"},
            ],
            "suggested_prompts": QUICK_PROMPTS[:4],
        }

    if "internship" in normalized or "experience" in normalized:
        return {
            "response": (
                "Pavilson completed a Software Development Internship at CANZA Technology Consultants, "
                "working across Flask, Django, FastAPI, backend logic, authentication, MySQL, and AI-oriented workflows."
            ),
            "actions": [
                {"kind": "navigate", "value": "experience", "label": "Open experience"},
                {"kind": "navigate", "value": "certifications", "label": "View certificate"},
            ],
            "suggested_prompts": QUICK_PROMPTS[:4],
        }

    if "contact" in normalized or "email" in normalized or "phone" in normalized or "linkedin" in normalized:
        return {
            "response": (
                "You can contact Pavilson at pavilson7@gmail.com, call +91 8667840473, "
                "or connect on LinkedIn at https://www.linkedin.com/in/pavilson-s-b86500326/."
            ),
            "actions": [
                {"kind": "contact", "value": "email", "label": "Email"},
                {"kind": "contact", "value": "linkedin", "label": "LinkedIn"},
            ],
            "suggested_prompts": QUICK_PROMPTS[:4],
        }

    if "skill" in normalized or "stack" in normalized:
        return {
            "response": (
                "Pavilson's stack centers on Python, Flask, Django, FastAPI, JavaScript, SQL, MySQL, REST APIs, "
                "responsive frontend work, and AI-focused workflows including NLP and LLM integration."
            ),
            "actions": [
                {"kind": "navigate", "value": "skills", "label": "Open skills"},
                {"kind": "navigate", "value": "projects", "label": "View projects"},
            ],
            "suggested_prompts": QUICK_PROMPTS[:4],
        }

    if "resume" in normalized or "cv" in normalized:
        return {
            "response": "The resume is available for preview or download from the resume section.",
            "actions": [
                {"kind": "navigate", "value": "resume", "label": "Open resume"},
                {"kind": "download", "value": "resume", "label": "Preview resume"},
            ],
            "suggested_prompts": QUICK_PROMPTS[:4],
        }

    return {
        "response": (
            "I can help with projects, internship experience, technical skills, contact details, or resume access."
        ),
        "actions": [
            {"kind": "navigate", "value": "projects", "label": "View projects"},
            {"kind": "navigate", "value": "contact", "label": "Open contact"},
        ],
        "suggested_prompts": QUICK_PROMPTS[:4],
    }


def build_template_context() -> dict:
    resume_url = url_for("resume_file", filename=RESUME_FILENAME)
    certificate_url = url_for("static", filename=CERTIFICATE_FILENAME)
    profile_url = url_for("static", filename=PROFILE_FILENAME)

    return {
        "contact": CONTACT,
        "nav_items": NAV_ITEMS,
        "hero_stats": HERO_STATS,
        "about_panels": ABOUT_PANELS,
        "skill_groups": SKILL_GROUPS,
        "experience": EXPERIENCE,
        "projects": PROJECTS,
        "certifications": CERTIFICATIONS,
        "assistant_features": ASSISTANT_FEATURES,
        "assistant_name": "Pavilson Is Here",
        "assistant_intro": (
            "I am Pavilson Is Here, your recruiter-ready portfolio assistant. "
            "Ask me about projects, internship experience, contact details, interview answers, or where to navigate next."
        ),
        "assistant_prompts": QUICK_PROMPTS,
        "resume_url": resume_url,
        "resume_filename": "Pavilson_Software_Developer_Resume.pdf",
        "certificate_url": certificate_url,
        "certificate_filename": "Pavilson_Canza_Internship_Certificate.jpg",
        "profile_url": profile_url,
        "favicon_url": url_for("favicon"),
        "current_year": date.today().year,
    }


def ensure_project_structure() -> None:
    for directory in REQUIRED_DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)


def create_app() -> Flask:
    ensure_project_structure()

    app = Flask(
        __name__,
        static_folder=str(STATIC_DIR),
        template_folder=str(TEMPLATES_DIR),
    )
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
    app.config["JSON_SORT_KEYS"] = False

    @app.get("/")
    def home():
        return render_template("index.html", **build_template_context())

    @app.get("/favicon.ico")
    def favicon():
        favicon_path = STATIC_DIR / "favicon.ico"
        if favicon_path.is_file():
            return send_file(favicon_path, mimetype="image/x-icon", max_age=86400)

        return redirect(url_for("static", filename=PROFILE_FILENAME), code=307)

    @app.get(f"/{GOOGLE_VERIFICATION_FILENAME}")
    def google_verification():
        return send_from_directory(STATIC_DIR, GOOGLE_VERIFICATION_FILENAME, mimetype="text/html")

    @app.get("/resume/<path:filename>")
    def resume_file(filename: str):
        return send_from_directory(RESUME_DIR, filename)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "service": "portfolio"})

    @app.post("/chat")
    def chat():
        payload = request.get_json(silent=True) or {}
        user_message = str(payload.get("message", "")).strip()

        if not user_message:
            return (
                jsonify(
                    {
                        "response": "Please enter a message so I can help you with projects, experience, resume access, or interview answers.",
                        "actions": [
                            {"kind": "navigate", "value": "assistant", "label": "Open assistant section"},
                            {"kind": "navigate", "value": "projects", "label": "View projects"},
                        ],
                        "suggested_prompts": QUICK_PROMPTS[:4],
                    }
                ),
                400,
            )

        return jsonify(get_response(user_message))

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "").strip() == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
