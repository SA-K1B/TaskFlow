
# 🚀 TaskFlow

Designed for university-level projects, Taskflow is a project tracking system developed using Django.
<!-- 
# Project Description
Introducing Taskflow, a web application designed to streamline project management for university students. Using Taskflow, students can effectively track their projects, collaborate seamlessly, and divide tasks efficiently among team members. The intuitive dashboard keeps everyone updated on the project's current status, ensuring transparency and accountability. Additionally, teachers can easily assess student performance by reviewing detailed reports on the tasks for each project, making Taskflow an essential tool for both students and educators in managing and assessing project progress. -->

## 📌 Key Features

- **Collaborative Environment:**

  - Team leaders can create project-specific rooms, allowing team members to join and work     collaboratively.

- **Task Management:**

    - Team leaders can divide tasks and assign them to specific team members.
    - Team members can update task statuses upon completion, ensuring real-time progress          tracking.
- **Intuitive Dashboard:**

    - Visual representation of task statuses for better understanding and project     monitoring.
- **Academic Workflows for Teachers and Students:**

    - Teachers can create assignments or lab activities, providing a structured way for students to submit reports.
    - Students can upload their work directly through the platform.
    - Teachers can review the submissions and provide feedback seamlessly.

### 🔧 Tech Stack

* [![Django][Django.img]][Django-url]
* [![PostgreSQL][PostgreSQL.img]][PostgreSQL-url]
* [![Redis][Redis.img]][Redis-url]
* [![Celery][Celery.img]][Celery-url]
* [![HTML][HTML.img]][HTML-url]
* [![CSS][CSS.img]][CSS-url]
* [![Docker][Docker.img]][Docker-url]

## 🛠️ Tech Stack Details

- **Django:**
    Powers the backend, providing a robust framework to manage  user authentication,task assignments, and collaborative workflows.

- **PostgreSQL:**
Serves as the primary database to securely store project details, user data, task statuses, and feedback from teachers.

- **Redis:**
Used for caching and improving the performance of real-time updates, such as task status changes on the dashboard.

- **Celery:**
Handles background task processing, including sending notifications or reminders about pending tasks and deadlines.

- **Docker:**
Simplifies deployment by containerizing the application, ensuring consistency across development and production environments.

### ⚙️ Installation with Docker


1. Clone the Repository
    ```bash
    git clone https://github.com/SA-K1B/TaskFlow.git
    ```
2. Navigate to the project directory
    ```sh
    cd TaskFlow
    ```
3. Build Image 
   ```sh
   docker compose build
   ```
4. Start the app
   ```sh
   docker compose up -d
   ```
Now, the app will be available at https://localhost:8000

[Django-url]: https://www.djangoproject.com/
[Django.img]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white

[PostgreSQL-url]: https://www.postgresql.org/
[PostgreSQL.img]: https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white

[Redis-url]: https://redis.io/
[Redis.img]: https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white

[Celery-url]: https://docs.celeryproject.org/en/stable/
[Celery.img]: https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white

[HTML-url]: https://html.spec.whatwg.org/
[HTML.img]: https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white

[CSS-url]: https://www.w3.org/Style/CSS/Overview.en.html
[CSS.img]: https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white

[Docker-url]: https://www.docker.com/
[Docker.img]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
