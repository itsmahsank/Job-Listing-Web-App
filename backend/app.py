from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Import our database functions
from db import init_database, test_database_connection

# Import our routes (API endpoints)
from routes.job_routes import job_bp

# Load environment variables from .env file
load_dotenv()

def create_app():
    """
    Create and configure the Flask application
    This is the main function that sets up our app
    """
    app = Flask(__name__)
    
    # Enable CORS to allow frontend to communicate with backend
    CORS(app)
    
    # Configure the database connection
    # Use DATABASE_URL from environment variables (PostgreSQL)
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        app.config['DATABASE_URL'] = database_url
        print(f"Using database from environment: {database_url}")
    else:
        # Fallback to SQLite if no DATABASE_URL is provided
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = os.path.join(backend_dir, 'jobs.db')
        app.config['DATABASE_URL'] = f'sqlite:///{database_path}'
        print(f"Using SQLite database: {database_path}")
    
    # Initialize the database with our app
    init_database(app)
    
    # Import and register our job routes
    from routes.job_routes import job_bp
    app.register_blueprint(job_bp)
    
    # Health check endpoint to test if the server is running
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'Job Listing API is running'})
    
    # Test database connection on startup
    try:
        test_database_connection()
        print("Database connection test successful!")
    except Exception as e:
        print(f"Warning: Database connection test failed: {e}")
        print("App will continue to run, but database operations may fail")
    
    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    print("Starting Job Listing Web App...")
    print("Backend server will be available at: http://localhost:5000")
    print("API endpoints will be available at: http://localhost:5000/api/")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
