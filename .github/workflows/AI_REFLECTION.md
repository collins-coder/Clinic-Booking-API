# AI Reflection

## How I Used AI

During this project, I used AI as a development assistant rather than as a code generator. AI helped me understand FastAPI concepts, explain SQLAlchemy behaviour, troubleshoot errors, review implementation choices, and improve documentation. I verified and tested all generated code before integrating it into the project.

---

## Example Where AI Improved My Work

AI helped structure the application using a layered architecture by separating API routes, business logic, and database models. This made the project easier to organize, test, and maintain.

Another significant contribution was helping implement concurrency handling by combining application-level validation with a database unique constraint and proper handling of database integrity errors.

---

## Example Where AI Was Incorrect

At one point, AI suggested changes that introduced an indentation issue in the booking service, which caused runtime errors. By reviewing the traceback, inspecting the code, and running the application locally, I identified the problem and corrected the implementation before proceeding.

This reinforced the importance of validating AI-generated code rather than accepting it without verification.

---

## Decisions I Made Independently

### 1. Database Migration

I decided to migrate the project from MySQL to PostgreSQL to better align with the deployment environment on Render. Although the project initially used MySQL during development, PostgreSQL simplified deployment and matched the managed database service provided by the hosting platform.

### 2. Deployment Strategy

I independently chose to deploy the application on Render using a managed PostgreSQL database and configured the environment variables, migrations, and deployment settings. This ensured the application was production-ready and accessible through a public URL.

---

## Lessons Learned

This project reinforced several software engineering concepts:

- Designing RESTful APIs using FastAPI.
- Applying database constraints to maintain data integrity.
- Separating business logic from API routes.
- Using Alembic for database migrations.
- Writing automated tests with Pytest.
- Deploying production applications with PostgreSQL on Render.
- Treating AI as a productivity tool while validating its output through testing and debugging.

Overall, AI accelerated development and documentation, while my own testing, debugging, and deployment work ensured the correctness and reliability of the final solution.