import os
import django
import sqlite3

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')
django.setup()

from accounts.models import User
from courses.models import Course, Chapter, Lesson
from certificates.models import Certificate
from progress.models import CourseAssignment, LessonProgress

print("Migrating data from db.sqlite3 to SQL Server (lms_db)...")

sqlite_conn = sqlite3.connect('db.sqlite3')
sqlite_conn.row_factory = sqlite3.Row
sqlite_cursor = sqlite_conn.cursor()

# 1. Accounts User
sqlite_cursor.execute("SELECT * FROM accounts_user")
users = sqlite_cursor.fetchall()
print(f"Transferring {len(users)} Users...")
for u in users:
    u_dict = dict(u)
    if not User.objects.filter(id=u_dict['id']).exists():
        User.objects.create(
            id=u_dict['id'],
            password=u_dict['password'],
            last_login=u_dict['last_login'],
            is_superuser=u_dict['is_superuser'],
            username=u_dict['username'],
            first_name=u_dict['first_name'],
            last_name=u_dict['last_name'],
            email=u_dict['email'],
            is_staff=u_dict['is_staff'],
            is_active=u_dict['is_active'],
            date_joined=u_dict['date_joined'],
            role=u_dict['role'],
            is_approved=u_dict['is_approved']
        )

# 2. Courses
sqlite_cursor.execute("SELECT * FROM courses_course")
courses = sqlite_cursor.fetchall()
print(f"Transferring {len(courses)} Courses...")
for c in courses:
    c_dict = dict(c)
    if not Course.objects.filter(id=c_dict['id']).exists():
        Course.objects.create(
            id=c_dict['id'],
            title=c_dict['title'],
            description=c_dict['description'],
            created_at=c_dict['created_at'],
            mentor_id=c_dict['mentor_id']
        )

# 3. Chapters
sqlite_cursor.execute("SELECT * FROM courses_chapter")
chapters = sqlite_cursor.fetchall()
print(f"Transferring {len(chapters)} Chapters...")
for ch in chapters:
    ch_dict = dict(ch)
    if not Chapter.objects.filter(id=ch_dict['id']).exists():
        Chapter.objects.create(
            id=ch_dict['id'],
            title=ch_dict['title'],
            created_at=ch_dict['created_at'],
            course_id=ch_dict['course_id']
        )

# 4. Lessons
sqlite_cursor.execute("SELECT * FROM courses_lesson")
lessons = sqlite_cursor.fetchall()
print(f"Transferring {len(lessons)} Lessons...")
for l in lessons:
    l_dict = dict(l)
    if not Lesson.objects.filter(id=l_dict['id']).exists():
        Lesson.objects.create(
            id=l_dict['id'],
            title=l_dict['title'],
            content=l_dict['content'],
            video_url=l_dict['video_url'],
            order=l_dict['order'],
            created_at=l_dict['created_at'],
            chapter_id=l_dict['chapter_id']
        )

# 5. CourseAssignment
sqlite_cursor.execute("SELECT * FROM progress_courseassignment")
assignments = sqlite_cursor.fetchall()
print(f"Transferring {len(assignments)} Course Assignments...")
for a in assignments:
    a_dict = dict(a)
    if not CourseAssignment.objects.filter(id=a_dict['id']).exists():
        CourseAssignment.objects.create(
            id=a_dict['id'],
            assigned_at=a_dict['assigned_at'],
            course_id=a_dict['course_id'],
            student_id=a_dict['student_id']
        )

# 6. LessonProgress
sqlite_cursor.execute("SELECT * FROM progress_lessonprogress")
lp_list = sqlite_cursor.fetchall()
print(f"Transferring {len(lp_list)} Lesson Progress entries...")
for lp in lp_list:
    lp_dict = dict(lp)
    if not LessonProgress.objects.filter(id=lp_dict['id']).exists():
        LessonProgress.objects.create(
            id=lp_dict['id'],
            completed=lp_dict['completed'],
            lesson_id=lp_dict['lesson_id'],
            student_id=lp_dict['student_id']
        )

# 7. Certificate
sqlite_cursor.execute("SELECT * FROM certificates_certificate")
certs = sqlite_cursor.fetchall()
print(f"Transferring {len(certs)} Certificates...")
for cert in certs:
    cert_dict = dict(cert)
    if not Certificate.objects.filter(id=cert_dict['id']).exists():
        Certificate.objects.create(
            id=cert_dict['id'],
            certificate_id=cert_dict['certificate_id'],
            certificate_file=cert_dict['certificate_file'],
            created_at=cert_dict['created_at'],
            course_id=cert_dict['course_id'],
            student_id=cert_dict['student_id']
        )

sqlite_conn.close()
print("Data migration from SQLite to MS SQL Server completed successfully!")
