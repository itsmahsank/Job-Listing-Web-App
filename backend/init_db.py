#!/usr/bin/env python3
"""
Database Initialization Script
This script creates the database and tables for the Job Listing Web App
"""

import os
import sys

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

def init_database():
    """
    Initialize the database and create all tables
    """
    try:
        # Import the database functions
        from db import init_database
        from app import create_app
        
        # Create the Flask app
        app = create_app()
        
        # Initialize the database
        with app.app_context():
            success = init_database(app)
            if success:
                print("Database tables created successfully!")
            else:
                print("Failed to create database tables")
                return False
        
        print("\nDatabase initialization completed!")
        print("You can now run the main application with: python app.py")
        return True
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

if __name__ == "__main__":
    try:
        init_database()
    except Exception as e:
        print(f"Import error: {e}")
        print("Make sure you're running this script from the backend directory")
