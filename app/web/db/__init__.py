import click
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

db = SQLAlchemy()


@click.command("init-db")
def init_db_command():
    """Initialize database tables if they don't exist (production-safe)."""
    with current_app.app_context():
        # Check if tables already exist
        inspector = db.inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        if existing_tables:
            click.echo(f"Database tables already exist: {', '.join(existing_tables)}")
            click.echo("Skipping initialization to preserve existing data.")
            click.echo("Use 'flask --app app.web reset-db' if you need to recreate tables.")
        else:
            click.echo("No tables found. Creating database tables...")
            db.create_all()
            
            # Verify tables were created
            tables = db.inspect(db.engine).get_table_names()
            click.echo(f"Database initialized with tables: {', '.join(tables)}")
    
    click.echo("Database initialization completed.")


@click.command("reset-db")
def reset_db_command():
    """Reset database by dropping and recreating all tables (DESTRUCTIVE)."""
    with current_app.app_context():
        click.echo("⚠️  WARNING: This will delete all existing data!")
        
        # Drop all existing tables and create new ones
        db.drop_all()
        db.create_all()
        
        # Verify tables were created
        tables = db.inspect(db.engine).get_table_names()
        click.echo(f"Database reset with tables: {', '.join(tables)}")
    
    click.echo("Database reset completed.")
