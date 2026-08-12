import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')
django.setup()

from accounts.models import User
from courses.models import Course, Chapter, Lesson
from progress.models import CourseAssignment

def seed_database():
    print("--- Seeding LMS Database ---")

    # 1. Create Quick Accounts
    admin_user, _ = User.objects.get_or_create(username="admin", defaults={"role": "ADMIN", "is_staff": True, "is_superuser": True})
    admin_user.set_password("admin123")
    admin_user.role = "ADMIN"
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.is_active = True
    admin_user.save()

    mentor_user, _ = User.objects.get_or_create(username="mentor1", defaults={"role": "MENTOR"})
    mentor_user.set_password("pass123")
    mentor_user.role = "MENTOR"
    mentor_user.is_active = True
    mentor_user.save()

    student_user, _ = User.objects.get_or_create(username="student1", defaults={"role": "STUDENT"})
    student_user.set_password("pass123")
    student_user.role = "STUDENT"
    student_user.is_active = True
    student_user.save()

    print("Quick Accounts (admin, mentor1, student1) populated successfully.")

    # 2. Top 15 Courses
    top_courses = [
        {
            "id": 101,
            "title": "Full-Stack Web Development with React & Django",
            "description": "Master modern full-stack development. Build scalable web applications combining Django REST API and React frontend.",
            "chapters": [
                {
                    "title": "1. Django Backend Core",
                    "lessons": [
                        {"title": "Introduction to Django Models & ORM", "content": "Learn how Django maps Python objects to database tables.", "video_url": "https://www.youtube.com/watch?v=F5mRW0jo-U4"},
                        {"title": "Building REST APIs with DRF", "content": "Understand API views, serializers, and JWT token authentication.", "video_url": "https://www.youtube.com/watch?v=c708Nf0cHMS"}
                    ]
                },
                {
                    "title": "2. React & Modern UI",
                    "lessons": [
                        {"title": "React Component Architecture", "content": "Build reusable, responsive React components with Tailwind CSS.", "video_url": "https://www.youtube.com/watch?v=w7ejDZ8SWv8"}
                    ]
                }
            ]
        },
        {
            "id": 102,
            "title": "Data Science & Machine Learning with Python",
            "description": "Unlock machine learning algorithms, NumPy, Pandas, Scikit-learn, and deep learning neural networks.",
            "chapters": [
                {
                    "title": "1. Python for Data Analysis",
                    "lessons": [
                        {"title": "Pandas DataFrames & Data Cleaning", "content": "Learn data wrangling, missing data imputation, and aggregation techniques.", "video_url": "https://www.youtube.com/watch?v=vmEHCJofslg"}
                    ]
                }
            ]
        },
        {
            "id": 103,
            "title": "Master Python Programming: Zero to Hero",
            "description": "Complete Python bootcamp covering syntax, OOP, concurrency, file I/O, and production best practices.",
            "chapters": [
                {
                    "title": "1. Python Fundamentals",
                    "lessons": [
                        {"title": "Control Flow & Functions", "content": "Master conditional branching, loops, lambda functions, and scope.", "video_url": "https://www.youtube.com/watch?v=_uQrJ0TkZlc"}
                    ]
                }
            ]
        },
        {
            "id": 104,
            "title": "React 19 & Next.js Enterprise Architecture",
            "description": "Build high-performance web applications using Next.js App Router, Server Components, and SSR.",
            "chapters": [
                {
                    "title": "1. Next.js Essentials",
                    "lessons": [
                        {"title": "Server Components & Server Actions", "content": "Leverage React 19 server features for zero-bundle-size rendering.", "video_url": "https://www.youtube.com/watch?v=wm5gMKCORL4"}
                    ]
                }
            ]
        },
        {
            "id": 105,
            "title": "Cloud Computing & DevOps with AWS & Docker",
            "description": "Master containerization with Docker, Kubernetes orchestration, and deployment pipelines on AWS Cloud.",
            "chapters": [
                {
                    "title": "1. Docker & Containerization",
                    "lessons": [
                        {"title": "Dockerizing Web Applications", "content": "Write multi-stage Dockerfiles and compose microservices environments.", "video_url": "https://www.youtube.com/watch?v=3c-iBn73dDE"}
                    ]
                }
            ]
        },
        {
            "id": 106,
            "title": "Cybersecurity & Ethical Hacking Fundamentals",
            "description": "Learn network security, penetration testing, vulnerability assessment, and defensive engineering.",
            "chapters": [
                {
                    "title": "1. Network Security Basics",
                    "lessons": [
                        {"title": "Packet Inspection & Protocol Security", "content": "Understand TCP/IP security, firewalls, and encryption protocols.", "video_url": "https://www.youtube.com/watch?v=inWWhr5tnEA"}
                    ]
                }
            ]
        },
        {
            "id": 107,
            "title": "Microservices & API Design with Go & gRPC",
            "description": "Build blazingly fast, concurrent backend microservices using Golang, protocol buffers, and gRPC.",
            "chapters": [
                {
                    "title": "1. Go Concurrency",
                    "lessons": [
                        {"title": "Goroutines & Channels", "content": "Master concurrent programming with Go channels and sync primitives.", "video_url": "https://www.youtube.com/watch?v=yyUHQIec83I"}
                    ]
                }
            ]
        },
        {
            "id": 108,
            "title": "Mobile App Development with React Native & Expo",
            "description": "Build cross-platform iOS and Android mobile apps using React Native, native modules, and Expo API.",
            "chapters": [
                {
                    "title": "1. React Native Components",
                    "lessons": [
                        {"title": "Layouts & Flexbox in Mobile UI", "content": "Design fluid touch layouts for smartphones and tablets.", "video_url": "https://www.youtube.com/watch?v=0-S5a0eXPoc"}
                    ]
                }
            ]
        },
        {
            "id": 109,
            "title": "UI/UX Design Systems & Figma Masterclass",
            "description": "Design modern user experiences. Create interactive prototypes, design tokens, and glassmorphic interfaces.",
            "chapters": [
                {
                    "title": "1. Design Tokens & Typography",
                    "lessons": [
                        {"title": "Color Systems & Responsive Grids", "content": "Construct scalable UI kits and design tokens in Figma.", "video_url": "https://www.youtube.com/watch?v=c9Wg6Cb_YlU"}
                    ]
                }
            ]
        },
        {
            "id": 110,
            "title": "Data Structures, Algorithms & System Design",
            "description": "Ace technical interviews. Master dynamic programming, graph algorithms, memory optimization, and distributed systems.",
            "chapters": [
                {
                    "title": "1. Data Structures Foundation",
                    "lessons": [
                        {"title": "Trees, Graphs & Heaps", "content": "Implement binary search trees, graph traversals, and priority queues.", "video_url": "https://www.youtube.com/watch?v=8hly31xKLI0"}
                    ]
                }
            ]
        },
        {
            "id": 111,
            "title": "Generative AI & Prompt Engineering with Gemini",
            "description": "Harness Large Language Models, embeddings, RAG pipelines, and autonomous AI agents in production.",
            "chapters": [
                {
                    "title": "1. LLM Integration",
                    "lessons": [
                        {"title": "Building RAG Applications", "content": "Connect vector databases with Gemini API for contextual AI search.", "video_url": "https://www.youtube.com/watch?v=tcqEUSFiVCA"}
                    ]
                }
            ]
        },
        {
            "id": 112,
            "title": "Microsoft SQL Server Database Administration",
            "description": "In-depth T-SQL programming, index optimization, query execution plan analysis, and high-availability backup.",
            "chapters": [
                {
                    "title": "1. T-SQL & Indexing",
                    "lessons": [
                        {"title": "Clustered & Non-Clustered Index Tuning", "content": "Optimize query execution speed and eliminate database bottlenecks.", "video_url": "https://www.youtube.com/watch?v=7S_tz1z_5bA"}
                    ]
                }
            ]
        },
        {
            "id": 113,
            "title": "Blockchain & Smart Contract Engineering",
            "description": "Develop decentralized applications (dApps), Solidity smart contracts, Web3 tokenomics, and security audits.",
            "chapters": [
                {
                    "title": "1. Solidity Basics",
                    "lessons": [
                        {"title": "Writing Safe Smart Contracts", "content": "Implement ERC-20 tokens and security patterns against reentrancy attacks.", "video_url": "https://www.youtube.com/watch?v=gyMwXuJrbJQ"}
                    ]
                }
            ]
        },
        {
            "id": 114,
            "title": "Modern C++ & High-Performance Computing",
            "description": "Master C++20 standard features, memory management, pointers, RAII, multithreading, and low-latency systems.",
            "chapters": [
                {
                    "title": "1. Modern C++ Core",
                    "lessons": [
                        {"title": "Smart Pointers & RAII Pattern", "content": "Manage dynamic heap allocations safely with unique_ptr and shared_ptr.", "video_url": "https://www.youtube.com/watch?v=vLnPwxZdW4Y"}
                    ]
                }
            ]
        },
        {
            "id": 115,
            "title": "Kubernetes & Cloud Native Infrastructure",
            "description": "Deploy, scale, and manage automated container orchestrations using Helm, Ingress controllers, and Prometheus.",
            "chapters": [
                {
                    "title": "1. Kubernetes Pods & Deployments",
                    "lessons": [
                        {"title": "Declarative YAML Manifests", "content": "Deploy scalable microservices clusters using Kubernetes deployments and services.", "video_url": "https://www.youtube.com/watch?v=X48VuDVv0do"}
                    ]
                }
            ]
        }
    ]

    for cdata in top_courses:
        course, created = Course.objects.get_or_create(
            id=cdata["id"],
            defaults={
                "title": cdata["title"],
                "description": cdata["description"],
                "mentor": mentor_user
            }
        )
        if not created:
            course.title = cdata["title"]
            course.description = cdata["description"]
            course.mentor = mentor_user
            course.save()

        if cdata["id"] in [101, 102]:
            CourseAssignment.objects.get_or_create(student=student_user, course=course)

        for ch_idx, chdata in enumerate(cdata["chapters"]):
            chapter, _ = Chapter.objects.get_or_create(
                course=course,
                title=chdata["title"]
            )
            for l_idx, ldata in enumerate(chdata["lessons"]):
                Lesson.objects.get_or_create(
                    chapter=chapter,
                    title=ldata["title"],
                    defaults={
                        "content": ldata["content"],
                        "video_url": ldata["video_url"],
                        "order": l_idx + 1
                    }
                )

    print(f"Successfully populated {len(top_courses)} Top Courses with syllabus into database!")

if __name__ == "__main__":
    seed_database()
