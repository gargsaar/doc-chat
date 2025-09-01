
# Doc-Chat

Doc-Chat is an AI-powered document chat platform that allows users to upload, search, and interact with documents using natural language. It leverages modern LLMs and vector databases for semantic search and contextual conversation.

## Features

- **Document Upload & Management**: Securely upload and organize PDFs.
- **Semantic Search**: Find information using natural language queries.
- **Conversational AI**: Chat with your documents and get context-aware answers.
- **User Authentication**: Secure login and access control.
- **Task Queue**: Background processing with Celery.
- **Vector Store Integration**: Fast, scalable semantic search using ChromaDB.
- **REST API**: Interact programmatically with your documents.

## Local Development Setup

1. Install dependencies:
	```sh
	uv venv .venv
	source .venv/bin/activate
	uv pip install -r requirements.txt
	```
2. Start Redis locally (or use a managed service):
	```sh
	redis-server
	```
3. Initialize the database:
	```sh
	flask --app app.web init-db
	```
4. Start the web server:
	```sh
	inv dev
	```
5. Start the worker:
	```sh
	inv devworker
	```

## Deployment on Render

1. Push your code to GitHub and connect the repo to Render.
2. Add environment variables in the Render dashboard:
	- `SECRET_KEY`
	- `SQLALCHEMY_DATABASE_URI`
	- `REDIS_URI` (from managed Redis service)
3. Render will build and start your web and worker services using `render.yaml`:
	- Web service: `inv prod` (uses Gunicorn for production)
	- Worker service: `inv devworker`
	- Redis: managed by Render
4. To reset the database, use the Render shell:
	```sh
	flask --app app.web init-db
	```

## Project Structure

- `app/` — Python backend (Flask, Celery, API, models, tasks)
- `client/` — Svelte frontend
- `chroma_db/` — Vector store data
- `uploads/` — User-uploaded files
- `render.yaml` — Render deployment configuration
- `requirements.txt`, `Pipfile` — Python dependencies

## License

MIT
