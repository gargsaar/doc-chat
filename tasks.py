import os
from invoke import task


@task
def dev(ctx):
    ctx.run(
        "flask --app app.web run --debug --port 8000",
        pty=os.name != "nt",
        env={"APP_ENV": "development"},
    )


@task
def devworker(ctx):
    ctx.run(
        "watchmedo auto-restart --directory=./app --pattern=*.py --recursive -- celery -A app.celery.worker worker --concurrency=1 --loglevel=INFO --pool=solo",
        pty=os.name != "nt",
        env={"APP_ENV": "development"},
    )


@task
def prod(ctx):
    port = os.environ.get("PORT", "10000")
    ctx.run(
        f"gunicorn 'app.web:create_app()' --bind 0.0.0.0:{port} --workers 2",
        pty=os.name != "nt",
        env={"APP_ENV": "production"},
    )


@task
def prodworker(ctx):
    ctx.run(
        "celery -A app.celery.worker worker --concurrency=2 --loglevel=INFO",
        pty=os.name != "nt",
        env={"APP_ENV": "production"},
    )
