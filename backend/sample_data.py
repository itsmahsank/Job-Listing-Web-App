#!/usr/bin/env python3
"""
Sample Data Creator for Job Listing Web App
This script populates the database with sample job listings
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

def create_sample_jobs():
    """
    Create sample job data for testing and demonstration
    """
    try:
        # Import the database and models
        from db import db
        from models.job import Job
        from app import create_app
        
        # Create the Flask app
        app = create_app()
        
        with app.app_context():
            # Check if jobs already exist
            existing_jobs = Job.query.count()
            if existing_jobs > 0:
                print(f"Database already contains {existing_jobs} jobs")
                print("Skipping sample data creation")
                return
            
            print("Starting to add sample jobs to the database...")
            
            # Sample job data
            sample_jobs = [
                {
                    'title': 'Senior Actuarial Analyst',
                    'company': 'MetLife',
                    'location': 'New York, NY',
                    'description': 'We are seeking a Senior Actuarial Analyst to join our team. The ideal candidate will have strong analytical skills and experience in life insurance pricing.',
                    'job_type': 'Full-time',
                    'salary_range': '$80,000 - $120,000',
                    'experience_level': '3-5 years',
                    'tags': 'Life, Pricing, Analysis',
                    'posting_date': datetime.now() - timedelta(days=5)
                },
                {
                    'title': 'Actuarial Intern',
                    'company': 'Prudential',
                    'location': 'Newark, NJ',
                    'description': 'Summer internship opportunity for actuarial students. Gain hands-on experience in insurance mathematics and risk assessment.',
                    'job_type': 'Internship',
                    'salary_range': '$25 - $30 per hour',
                    'experience_level': 'Student',
                    'tags': 'Internship, Life, Health',
                    'posting_date': datetime.now() - timedelta(days=3)
                },
                {
                    'title': 'Pricing Actuary',
                    'company': 'AIG',
                    'location': 'Houston, TX',
                    'description': 'Join our pricing team to develop and maintain pricing models for property and casualty insurance products.',
                    'job_type': 'Full-time',
                    'salary_range': '$90,000 - $130,000',
                    'experience_level': '5-7 years',
                    'tags': 'Pricing, P&C, Modeling',
                    'posting_date': datetime.now() - timedelta(days=7)
                },
                {
                    'title': 'Actuarial Consultant',
                    'company': 'Deloitte',
                    'location': 'Chicago, IL',
                    'description': 'Provide actuarial consulting services to clients in the insurance and financial services industries.',
                    'job_type': 'Full-time',
                    'salary_range': '$100,000 - $150,000',
                    'experience_level': '7-10 years',
                    'tags': 'Consulting, Life, Health, P&C',
                    'posting_date': datetime.now() - timedelta(days=2)
                },
                {
                    'title': 'Reserving Actuary',
                    'company': 'Travelers',
                    'location': 'Hartford, CT',
                    'description': 'Responsible for estimating insurance reserves and providing actuarial support for financial reporting.',
                    'job_type': 'Full-time',
                    'salary_range': '$85,000 - $125,000',
                    'experience_level': '4-6 years',
                    'tags': 'Reserving, Financial Reporting, P&C',
                    'posting_date': datetime.now() - timedelta(days=1)
                }
            ]
            
            # Add jobs to database
            jobs_added = 0
            for i, job_data in enumerate(sample_jobs, 1):
                try:
                    job = Job(**job_data)
                    db.session.add(job)
                    db.session.commit()
                    print(f"Added job {i}: {job_data['title']} at {job_data['company']}")
                    jobs_added += 1
                except Exception as e:
                    print(f"Error adding job {i}: {e}")
                    db.session.rollback()
            
            print(f"Sample data creation complete!")
            print(f"Total jobs added: {jobs_added}")
            
    except Exception as e:
        print(f"Error creating sample jobs: {e}")

def main():
    """
    Main function to run the sample data creator
    """
    print("Job Listing Web App - Sample Data Creator")
    print("=" * 50)
    
    try:
        # Test database connection first
        from db import test_database_connection
        if test_database_connection():
            print("Database connection successful!")
            create_sample_jobs()
        else:
            print("Database connection failed!")
            print("Please check your database configuration")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you're running this script from the backend directory")

if __name__ == "__main__":
    main()
