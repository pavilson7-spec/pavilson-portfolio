from __future__ import annotations

from dataclasses import dataclass, field
from textwrap import dedent


QUICK_PROMPTS = [
    "Tell me about Pavilson S.",
    "Explain the MindNest AI Application.",
    "Summarize the internship experience.",
    "How can I contact Pavilson?",
    "What skills does Pavilson bring?",
    "Help me download the resume.",
]


@dataclass(frozen=True)
class ChatAction:
    label: str
    kind: str
    value: str

    def as_dict(self) -> dict:
        return {"label": self.label, "kind": self.kind, "value": self.value}


@dataclass(frozen=True)
class ChatReply:
    response: str
    actions: tuple[ChatAction, ...] = field(default_factory=tuple)
    suggested_prompts: tuple[str, ...] = field(default_factory=tuple)

    def as_dict(self) -> dict:
        return {
            "response": self.response.strip(),
            "actions": [action.as_dict() for action in self.actions],
            "suggested_prompts": list(self.suggested_prompts),
        }


PROJECT_RESPONSES = {
    "mindnest": dedent(
        """
        MindNest AI Application is one of Pavilson's strongest AI-product style projects because it combines backend structure with intelligent user interaction.

        The project is positioned around contextual assistance, API-backed application logic, and an AI-first user experience. It reflects how Pavilson thinks about building modern software, not just isolated models. Instead of treating AI as a separate experiment, the project shows how language-model workflows can be embedded into a usable product experience.

        From a recruiter perspective, MindNest is valuable because it demonstrates product thinking, backend integration, and the ability to explain AI in a practical way.
        """
    ).strip(),
    "tumor": dedent(
        """
        Brain Tumor Detection highlights Pavilson's applied machine-learning mindset in a healthcare-related use case.

        The work focuses on image preprocessing, model inference, and structured classification flow. It shows that he can move beyond standard web development and apply AI techniques to meaningful real-world problem statements. Projects like this are especially useful in interviews because they show both technical curiosity and domain awareness.

        Recruiters usually see this project as evidence of practical AI exposure, image-based model handling, and a willingness to work on impactful problem spaces.
        """
    ).strip(),
    "drowsiness": dedent(
        """
        Driver Drowsiness Detection is a real-time safety-oriented AI project built around alertness monitoring.

        It reflects Pavilson's interest in computer vision and intelligent monitoring systems. The project is useful in recruiter conversations because it shows real-time thinking, applied model usage, and a focus on systems that need timely decision support instead of only offline analysis.

        Overall, it strengthens his profile as someone who can connect AI with practical product-style outcomes.
        """
    ).strip(),
    "ration": dedent(
        """
        E-Ration System is a strong example of full stack and workflow-oriented software thinking.

        The project is designed around secure access, beneficiary management, and structured administrative operations. It demonstrates backend logic, data handling, and a real-world service use case where clean user roles and reliable process flow matter. For recruiters, this project helps show that Pavilson can work on practical business systems and not only AI experimentation.

        It is especially useful when discussing problem solving, architecture, and public-service style digital transformation.
        """
    ).strip(),
    "curio": dedent(
        """
        Curio Mind Learning Platform represents Pavilson's interest in combining education, personalization, and AI-enhanced product design.

        The idea is centered on adaptive learning flow, user-focused recommendations, and a scalable application structure. It helps present him as a developer who thinks about the full user journey, not just isolated features. In recruiter discussions, this project shows a blend of full stack thinking, product creativity, and intelligent workflow design.

        It is a helpful example when the conversation moves toward software that creates meaningful user impact.
        """
    ).strip(),
}


def normalize(message: str) -> str:
    return " ".join(message.lower().strip().split())


def has_any(message: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in message for keyword in keywords)


def reply(text: str, actions: tuple[ChatAction, ...] = (), prompts: tuple[str, ...] = ()) -> dict:
    return ChatReply(text, actions, prompts).as_dict()


def get_response(message: str) -> dict:
    normalized = normalize(message)

    if not normalized:
        return default_reply()

    if has_any(normalized, ("mindnest", "mind nest")):
        return reply(
            PROJECT_RESPONSES["mindnest"],
            actions=(
                ChatAction("Open projects", "navigate", "projects"),
                ChatAction("Contact Pavilson", "navigate", "contact"),
            ),
            prompts=("Summarize the internship experience.", "What skills does Pavilson bring?"),
        )

    if has_any(normalized, ("brain tumor", "tumor detection", "brain tumour")):
        return reply(
            PROJECT_RESPONSES["tumor"],
            actions=(ChatAction("View project section", "navigate", "projects"),),
            prompts=("Tell me about Pavilson S.", "What AI skills does Pavilson use?"),
        )

    if has_any(normalized, ("drowsiness", "driver", "fatigue detection")):
        return reply(
            PROJECT_RESPONSES["drowsiness"],
            actions=(ChatAction("Open projects", "navigate", "projects"),),
            prompts=("Summarize the internship experience.", "What skills does Pavilson bring?"),
        )

    if has_any(normalized, ("e-ration", "ration system", "eration")):
        return reply(
            PROJECT_RESPONSES["ration"],
            actions=(ChatAction("Open projects", "navigate", "projects"),),
            prompts=("Why should we hire Pavilson?", "How can I contact Pavilson?"),
        )

    if has_any(normalized, ("curio", "learning platform", "personalized learning")):
        return reply(
            PROJECT_RESPONSES["curio"],
            actions=(ChatAction("Open projects", "navigate", "projects"),),
            prompts=("Tell me about Pavilson S.", "What skills does Pavilson bring?"),
        )

    if has_any(normalized, ("tell me about yourself", "introduce yourself", "about pavilson", "who is pavilson")):
        return reply(
            dedent(
                """
                My name is Pavilson S, and I recently completed my B.Sc. in Computer Science with specialization in Artificial Intelligence and Data Science.

                I am strongly interested in software development, backend engineering, full stack application building, and AI-enabled products. My hands-on work includes Python development with Flask, Django, and FastAPI, along with experience in REST APIs, MySQL, authentication workflows, and intelligent application features.

                I also completed a software development internship at CANZA Technology Consultants, where I gained practical exposure to professional backend workflows, API development, database operations, and AI-oriented product thinking.

                I am now looking for opportunities where I can contribute as a software developer, Python developer, backend engineer, full stack developer, or AI-focused engineer while continuing to grow through real-world product work.
                """
            ),
            actions=(
                ChatAction("View experience", "navigate", "experience"),
                ChatAction("Open resume", "navigate", "resume"),
            ),
            prompts=("Why should we hire Pavilson?", "What skills does Pavilson bring?"),
        )

    if has_any(normalized, ("why should we hire", "hire you", "hire pavilson")):
        return reply(
            dedent(
                """
                You should hire me because I bring a strong Python foundation, practical backend exposure, and a clear growth mindset.

                I already have hands-on experience with Flask, Django, FastAPI, REST APIs, MySQL, frontend integration, and AI-oriented workflows. I have applied these skills in projects as well as during my internship, so I understand both the technical side and the importance of building usable, maintainable software.

                I am also adaptable, sincere, and coachable. I learn quickly, accept feedback well, and stay committed to improving the quality of my work. That combination makes me a strong early-career developer who can contribute immediately while growing fast in a professional team.
                """
            ),
            actions=(
                ChatAction("See projects", "navigate", "projects"),
                ChatAction("Contact Pavilson", "navigate", "contact"),
            ),
            prompts=("Summarize the internship experience.", "Help me download the resume."),
        )

    if has_any(normalized, ("strength", "strengths", "strong points")):
        return reply(
            dedent(
                """
                My main strengths are structured problem solving, adaptability, consistency, and a strong willingness to learn.

                I like to understand a problem clearly before solving it, which helps me build cleaner backend logic and more reliable workflows. I am also comfortable adapting across Flask, Django, FastAPI, JavaScript, MySQL, and AI-oriented technologies based on project needs.

                Another strength is persistence. When I face a difficult issue, I keep working through it step by step until I find a practical solution. That discipline helps me improve steadily and contribute with reliability.
                """
            ),
            actions=(ChatAction("Open skills", "navigate", "skills"),),
            prompts=("What is Pavilson's internship experience?", "Why should we hire Pavilson?"),
        )

    if has_any(normalized, ("weakness", "weaknesses", "improve area")):
        return reply(
            dedent(
                """
                One area I continue to improve is that I sometimes spend extra time refining my work because I care about clean and well-structured output.

                Earlier, that could slow me down more than necessary. Over time, I have been improving my ability to balance quality with delivery speed by prioritizing better, shipping in smaller iterations, and refining after the core result is working well.

                I see it as a growth area that comes from responsibility toward the work, and I am already becoming more practical and efficient.
                """
            ),
            prompts=("Tell me about Pavilson S.", "Why should we hire Pavilson?"),
        )

    if has_any(normalized, ("internship", "experience", "canza")):
        return reply(
            dedent(
                """
                Pavilson completed his internship with CANZA Technology Consultants as a Software Development Intern.

                During that experience, he worked with Flask, Django, and FastAPI while gaining exposure to REST API development, authentication and authorization, database handling, debugging, and deployment-minded backend logic. He also gained insight into NLP and LLM-related workflows, which aligns well with his AI-focused learning direction.

                The internship is important because it moved his skills from academic knowledge into practical software delivery. It gave him confidence in team-style engineering and helped him understand how modern backend systems are built and maintained.
                """
            ),
            actions=(
                ChatAction("Open experience", "navigate", "experience"),
                ChatAction("View certificate", "navigate", "certifications"),
            ),
            prompts=("What skills does Pavilson bring?", "How can I contact Pavilson?"),
        )

    if has_any(normalized, ("skills", "tech stack", "technical skills", "what skills")):
        return reply(
            dedent(
                """
                Pavilson's skill set is centered around Python-based software development, backend engineering, full stack delivery, and AI-enabled application building.

                His main strengths include Python, Flask, Django, FastAPI, JavaScript, SQL, REST APIs, MySQL, authentication workflows, and responsive frontend development. On the AI side, he has worked with NLP ideas, LLM-oriented integrations, machine learning workflows, and computer-vision style projects.

                That combination makes him especially relevant for software developer, backend, Python, full stack, and AI-focused roles.
                """
            ),
            actions=(
                ChatAction("Open skills", "navigate", "skills"),
                ChatAction("See projects", "navigate", "projects"),
            ),
            prompts=("Explain the MindNest AI Application.", "Summarize the internship experience."),
        )

    if has_any(normalized, ("project", "projects", "portfolio work")):
        return reply(
            dedent(
                """
                The portfolio highlights five recruiter-friendly projects:

                - MindNest AI Application
                - Brain Tumor Detection
                - Driver Drowsiness Detection
                - E-Ration System
                - Curio Mind Learning Platform

                Together, these projects show a mix of backend engineering, full stack application building, AI experimentation, and product-style thinking. If you want, I can explain any one of them in detail.
                """
            ),
            actions=(ChatAction("Open projects", "navigate", "projects"),),
            prompts=(
                "Explain the MindNest AI Application.",
                "Explain the Brain Tumor Detection project in interview style.",
            ),
        )

    if has_any(normalized, ("certificate", "certification", "certifications")):
        return reply(
            dedent(
                """
                Pavilson currently showcases his Software Development Internship Certificate from CANZA Technology Consultants.

                This certificate supports the internship experience presented in the portfolio and helps recruiters verify his practical exposure to backend and AI-oriented software development.
                """
            ),
            actions=(
                ChatAction("Open certifications", "navigate", "certifications"),
                ChatAction("Open experience", "navigate", "experience"),
            ),
            prompts=("Help me download the resume.", "How can I contact Pavilson?"),
        )

    if has_any(normalized, ("contact", "email", "phone", "number", "linkedin", "reach")):
        return reply(
            dedent(
                """
                You can reach Pavilson S through the following details:

                Phone: +91 8667840473
                Email: pavilson7@gmail.com
                LinkedIn: https://www.linkedin.com/in/pavilson-s-b86500326/
                Country: India

                Email is ideal for interview scheduling and recruiter follow-up, while LinkedIn works well for professional networking and opportunity discussions.
                """
            ),
            actions=(
                ChatAction("Email Pavilson", "contact", "email"),
                ChatAction("Open LinkedIn", "contact", "linkedin"),
                ChatAction("Call Pavilson", "contact", "phone"),
            ),
            prompts=("Help me download the resume.", "Tell me about Pavilson S."),
        )

    if has_any(normalized, ("resume", "cv", "download")):
        return reply(
            dedent(
                """
                The portfolio includes a recruiter-ready resume section with both preview and direct download support.

                If you want the fastest route, use the resume action below. You can also scroll to the resume section to review the document context before downloading it.
                """
            ),
            actions=(
                ChatAction("Go to resume", "navigate", "resume"),
                ChatAction("Download resume", "download", "resume"),
            ),
            prompts=("How can I contact Pavilson?", "Summarize the internship experience."),
        )

    if has_any(normalized, ("navigate", "go to", "open", "take me")):
        for section, label in (
            ("about", "About"),
            ("skills", "Skills"),
            ("experience", "Experience"),
            ("projects", "Projects"),
            ("certifications", "Certifications"),
            ("assistant", "AI Assistant"),
            ("contact", "Contact"),
            ("resume", "Resume"),
        ):
            if section in normalized or label.lower() in normalized:
                return reply(
                    f"I can guide you there right away. Use the action below to jump to the {label} section.",
                    actions=(ChatAction(f"Open {label}", "navigate", section),),
                    prompts=("Tell me about Pavilson S.", "How can I contact Pavilson?"),
                )

    if has_any(normalized, ("recruiter", "hiring manager", "interviewer")):
        return reply(
            dedent(
                """
                For recruiters and hiring managers, the fastest way to review this portfolio is:

                1. Open the projects section to understand Pavilson's AI and software range.
                2. Review the internship and certification sections for practical credibility.
                3. Download the resume for structured screening.
                4. Use contact details for interview coordination.

                I can help you jump to any of those sections instantly.
                """
            ),
            actions=(
                ChatAction("Open projects", "navigate", "projects"),
                ChatAction("Open resume", "navigate", "resume"),
                ChatAction("Contact Pavilson", "navigate", "contact"),
            ),
            prompts=("Tell me about Pavilson S.", "Summarize the internship experience."),
        )

    if has_any(normalized, ("hi", "hello", "hey")):
        return reply(
            dedent(
                """
                Hello, I am Pavilson Is Here.

                I can guide you through interview answers, projects, internship experience, resume access, certifications, or direct contact details. Ask me naturally, and I will respond like a smart recruiter assistant.
                """
            ),
            actions=(ChatAction("Open projects", "navigate", "projects"),),
            prompts=tuple(QUICK_PROMPTS[:4]),
        )

    return default_reply()


def default_reply() -> dict:
    return reply(
        dedent(
            """
            I can help you with recruiter-style portfolio guidance, including:

            - interview answers such as tell me about yourself or why should we hire you
            - project explanations for MindNest, Brain Tumor Detection, Driver Drowsiness Detection, E-Ration System, and Curio Mind
            - internship and certification details
            - resume download and contact information
            - section navigation across the portfolio

            Ask me in a natural sentence, and I will guide you.
            """
        ),
        actions=(
            ChatAction("Open projects", "navigate", "projects"),
            ChatAction("Open resume", "navigate", "resume"),
        ),
        prompts=tuple(QUICK_PROMPTS[:4]),
    )
