
# Doc-Chat

Doc-Chat is an AI-powered document chat platform that allows users to upload, search, and interact with documents using natural language. It leverages modern LLMs and vector databases for semantic search and contextual conversation.

## Quick Start

**Default Configuration:** The application is configured for easy deployment using free services with synchronous task processing. No Redis or background workers required.

For production deployments, simply:
1. Push to GitHub and connect to Render
2. Set environment variables: `SECRET_KEY`, `OPENAI_API_KEY`, `UPLOAD_URL`
3. Deploy using the included `render.yaml` configuration

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
2. Copy environment configuration:
	```sh
	cp .env.example .env
	# Edit .env with your actual values (OpenAI API key, etc.)
	```
3. Initialize the database:
	```sh
	flask --app app.web init-db
	```
4. Start the web server:
	```sh
	inv dev
	```

### Worker Configuration Options

The application supports two execution modes controlled by the `USE_WORKERS` environment variable:

**Option 1: Sync Mode (Default - Simpler)**
- Set `USE_WORKERS=false` in your `.env` file
- Tasks run synchronously within the web process
- No Redis or separate worker process required
- Good for development and low-traffic deployments

**Option 2: Async Mode (Advanced)**
- Set `USE_WORKERS=true` in your `.env` file
- Requires Redis server:
	```sh
	redis-server
	```
- Start a separate worker process:
	```sh
	inv devworker
	```
- Better for high-traffic production environments

**Default Configuration:** The `.env.example` file sets `USE_WORKERS=true` for development, but production deployment defaults to `USE_WORKERS=false` to minimize costs.

## Deployment on Render

### Default Deployment (Free Tier - Recommended)
The application is configured by default for cost-effective deployment using only free Render services:
- **PostgreSQL database** (free tier)
- **Web service** with synchronous task processing (`USE_WORKERS=false`)
- **No Redis or background workers** required

Setup steps:
1. Push your code to GitHub and connect the repo to Render
2. Render will automatically use the `render.yaml` configuration
3. Add these environment variables in the Render dashboard:
   - `SECRET_KEY` (generate a secure random string)
   - `OPENAI_API_KEY` (your OpenAI API key)
   - `UPLOAD_URL` (your Render app URL, e.g., `https://your-app.onrender.com`)

The database will be automatically initialized on first deployment. No manual setup required!

### Database Management
- **Safe initialization**: `flask --app app.web init-db` (checks if tables exist, creates only if needed)
- **Reset database**: `flask --app app.web reset-db` (destructive - recreates all tables)
- **Production**: Database tables persist across deployments automatically

### Advanced Deployment (With Background Workers - Optional)
For high-traffic production environments, you can enable asynchronous background workers:

**⚠️ Note: This requires paid Render services for Redis and worker instances**

1. In `render.yaml`, uncomment the Redis and worker services sections
2. In the web service environment variables, change `USE_WORKERS` from `false` to `true`
3. Deploy with the updated configuration

### Environment Variables Reference
**Required for all deployments:**
- `SECRET_KEY` — Secure random string for sessions
- `OPENAI_API_KEY` — Your OpenAI API key  
- `UPLOAD_URL` — Base URL for your application
- `USE_WORKERS` — **Default: `false`** (sync mode), set to `true` for async mode
- `SQLALCHEMY_DATABASE_URI` — Automatically configured by Render PostgreSQL
- `CHROMA_DB_PATH` — Set to `./chroma_db`

**Only required for advanced deployment (USE_WORKERS=true):**
- `REDIS_URI` — Automatically configured by Render Redis service

## Project Structure

- `app/` — Python backend (Flask, Celery, API, models, tasks)
- `client/` — Svelte frontend
- `chroma_db/` — Vector store data
- `uploads/` — User-uploaded files
- `render.yaml` — Render deployment configuration
- `requirements.txt`, `Pipfile` — Python dependencies

## License

MIT
