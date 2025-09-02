import click
import os
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

db = SQLAlchemy()


@click.command("init-db")
def init_db_command():
    """Initialize the database with all tables."""
    with current_app.app_context():
        try:
            os.makedirs(current_app.instance_path)
        except OSError:
            pass
        
        # Drop all existing tables and create new ones
        db.drop_all()
        db.create_all()
        
        # Verify tables were created
        try:
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            click.echo(f"Database initialized with tables: {', '.join(tables)}")
        except Exception as e:
            click.echo(f"Database initialized (verification failed: {e})")
    
    click.echo("Database initialization completed.")
