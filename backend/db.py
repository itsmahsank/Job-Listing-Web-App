from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os

# Create a SQLAlchemy instance
db = SQLAlchemy()

def init_database(app):
    """
    Initialize the database with the Flask app
    This sets up the database connection and creates tables
    """
    try:
        # Check for forced database URL first (used by scraper)
        force_database_url = os.environ.get('FORCE_DATABASE_URL')
        if force_database_url:
            database_url = force_database_url
            print(f"Using forced database URL: {database_url}")
        else:
            # Configure the database URL from app config
            database_url = app.config.get('DATABASE_URL')
            if not database_url:
                # Default to SQLite if no database URL is provided
                database_url = 'sqlite:///jobs.db'
                print("No DATABASE_URL found, using default SQLite database")
        
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Initialize the database with the app
        db.init_app(app)
        
        # Create all tables
        with app.app_context():
            db.create_all()
            print("Database initialized successfully!")
            print("All tables created!")
        
        return True
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

def test_database_connection():
    """
    Test if we can connect to the database
    This helps verify the database is working
    """
    try:
        # Try to execute a simple query
        result = db.session.execute(text('SELECT 1'))
        result.fetchone()
        print("Database connection test successful!")
        return True
        
    except Exception as e:
        print(f"Database connection test failed: {e}")
        return False
