from flask import Blueprint, request, jsonify
from sqlalchemy import or_, desc, asc
from datetime import datetime
from models.job import Job
from db import db

# Create a blueprint for all our job-related routes
# A blueprint is like a container for related routes
job_bp = Blueprint('jobs', __name__)

@job_bp.route('/api/jobs', methods=['GET'])
def get_jobs():
    """
    Get all jobs with optional filtering and sorting
    This is the main endpoint that the frontend calls to get job listings
    """
    try:
        # Get all the parameters from the URL query string
        # These are sent by the frontend when making requests
        page = request.args.get('page', 1, type=int)  # Which page to show
        per_page = request.args.get('per_page', 5, type=int)  # How many jobs per page
        job_type = request.args.get('job_type')  # Filter by job type
        location = request.args.get('location')  # Filter by location
        tags = request.args.get('tags')  # Filter by tags
        search = request.args.get('search')  # Search text
        sort_by = request.args.get('sort', 'posting_date_desc')  # How to sort
        
        # Start with a basic query to get all jobs
        query = Job.query
        
        # Apply filters one by one
        # Only apply a filter if the user actually selected something
        
        # Filter by job type (e.g., Full-time, Part-time)
        if job_type and job_type.lower() != 'all':
            query = query.filter(Job.job_type.ilike(f'%{job_type}%'))
        
        # Filter by location (e.g., New York, Remote)
        if location and location.lower() != 'all':
            query = query.filter(Job.location.ilike(f'%{location}%'))
        
        # Filter by tags (e.g., Life, Health, Pricing)
        if tags and tags.lower() != 'all':
            # Split tags by comma and search for each one
            tag_list = [tag.strip() for tag in tags.split(',')]
            for tag in tag_list:
                query = query.filter(Job.tags.ilike(f'%{tag}%'))
        
        # Search in title, company, and description
        if search:
            # Use OR to search in multiple fields
            search_filter = or_(
                Job.title.ilike(f'%{search}%'),
                Job.company.ilike(f'%{search}%'),
                Job.description.ilike(f'%{search}%')
            )
            query = query.filter(search_filter)
        
        # Apply sorting based on what the user selected
        if sort_by == 'posting_date_desc':
            # Newest jobs first
            query = query.order_by(desc(Job.posting_date))
        elif sort_by == 'posting_date_asc':
            # Oldest jobs first
            query = query.order_by(asc(Job.posting_date))
        elif sort_by == 'title_asc':
            # Job titles A-Z
            query = query.order_by(asc(Job.title))
        elif sort_by == 'title_desc':
            # Job titles Z-A
            query = query.order_by(desc(Job.title))
        elif sort_by == 'company_asc':
            # Company names A-Z
            query = query.order_by(asc(Job.company))
        elif sort_by == 'company_desc':
            # Company names Z-A
            query = query.order_by(desc(Job.company))
        else:
            # Default sorting: newest jobs first
            query = query.order_by(desc(Job.posting_date))
        
        # Count total jobs before pagination (for debugging)
        total_count = query.count()
        print(f"Total jobs found: {total_count}")
        
        # Apply pagination to the query
        # This splits the results into pages
        offset = (page - 1) * per_page
        jobs = query.offset(offset).limit(per_page).all()
        
        # Calculate pagination info
        total_pages = (total_count + per_page - 1) // per_page
        has_next = page < total_pages
        has_prev = page > 1
        
        # Convert job objects to dictionaries for JSON response
        jobs_dict = [job.to_dict() for job in jobs]
        print(f"Returning {len(jobs_dict)} jobs for page {page} (per_page: {per_page})")
        
        # Return the response with all the pagination info
        return jsonify({
            'jobs': jobs_dict,
            'total': total_count,
            'pages': total_pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': has_next,
            'has_prev': has_prev
        }), 200
        
    except Exception as e:
        print(f"Error getting jobs: {e}")
        return jsonify({'error': 'Failed to get jobs'}), 500

@job_bp.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """
    Get a specific job by its ID
    This is used when the frontend wants to show details of one specific job
    """
    try:
        # Try to find the job with the given ID
        job = Job.query.get_or_404(job_id)
        
        # Convert to dictionary and return
        return jsonify(job.to_dict()), 200
        
    except Exception as e:
        print(f"Error getting job {job_id}: {e}")
        return jsonify({'error': str(e)}), 500

@job_bp.route('/api/jobs', methods=['POST'])
def create_job():
    """
    Create a new job
    This is called when the user submits the add job form
    """
    try:
        # Get the job data from the request
        data = request.get_json()
        
        # Check if required fields are present
        if not data or not data.get('title') or not data.get('company') or not data.get('location'):
            return jsonify({'error': 'Title, company, and location are required'}), 400
        
        # Create a new job object
        new_job = Job(
            title=data.get('title'),
            company=data.get('company'),
            location=data.get('location'),
            job_type=data.get('job_type', 'Full-time'),
            experience_level=data.get('experience_level', 'Entry Level'),
            salary_range=data.get('salary_range', 'Not specified'),
            description=data.get('description', ''),
            tags=data.get('tags', ''),
            posting_date=datetime.now()
        )
        
        # Add the job to the database
        db.session.add(new_job)
        db.session.commit()
        
        print(f"Created new job: {new_job.title} at {new_job.company}")
        
        # Return the created job
        return jsonify({
            'message': 'Job created successfully',
            'job': new_job.to_dict()
        }), 201
        
    except Exception as e:
        # Rollback on error
        db.session.rollback()
        print(f"Error creating job: {e}")
        return jsonify({'error': 'Failed to create job'}), 500

@job_bp.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    """
    Update an existing job
    This is called when the user submits the edit job form
    """
    try:
        # Find the job to update
        job = Job.query.get_or_404(job_id)
        
        # Get the updated data from the request
        data = request.get_json()
        
        # Check if required fields are present
        if not data or not data.get('title') or not data.get('company') or not data.get('location'):
            return jsonify({'error': 'Title, company, and location are required'}), 400
        
        # Update the job fields
        job.title = data.get('title')
        job.company = data.get('company')
        job.location = data.get('location')
        job.job_type = data.get('job_type', job.job_type)
        job.experience_level = data.get('experience_level', job.experience_level)
        job.salary_range = data.get('salary_range', job.salary_range)
        job.description = data.get('description', job.description)
        job.tags = data.get('tags', job.tags)
        
        # Save the changes
        db.session.commit()
        
        print(f"Updated job {job_id}: {job.title}")
        
        # Return success message
        return jsonify({
            'message': 'Job updated successfully',
            'job': job.to_dict()
        }), 200
        
    except Exception as e:
        # Rollback on error
        db.session.rollback()
        print(f"Error updating job {job_id}: {e}")
        return jsonify({'error': str(e)}), 500

@job_bp.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """
    Delete a job
    This is called when the user clicks the delete button
    """
    try:
        # Find the job to delete
        job = Job.query.get_or_404(job_id)
        
        # Delete it from the database
        db.session.delete(job)
        db.session.commit()
        
        print(f"Deleted job {job_id}: {job.title}")
        
        # Return success message
        return jsonify({'message': 'Job deleted successfully'}), 200
        
    except Exception as e:
        # Rollback on error
        db.session.rollback()
        print(f"Error deleting job {job_id}: {e}")
        return jsonify({'error': str(e)}), 500

@job_bp.route('/api/jobs/filters', methods=['GET'])
def get_filters():
    """
    Get all the available filter options
    This helps the frontend populate the filter dropdowns
    """
    try:
        # Provide comprehensive job types instead of just what's in the database
        # This ensures users can filter by all possible job types
        comprehensive_job_types = [
            'Full-time',
            'Part-time',
            'Contract',
            'Internship',
            'Temporary',
            'Freelance',
            'Remote',
            'Hybrid',
            'On-site'
        ]
        
        # Get all unique job types from the database (for existing jobs)
        db_job_types = db.session.query(Job.job_type).distinct().all()
        db_job_types = [job_type[0] for job_type in db_job_types if job_type[0]]
        
        # Combine comprehensive list with database job types
        all_job_types = list(set(comprehensive_job_types + db_job_types))
        all_job_types.sort()  # Sort alphabetically
        
        # Get all unique locations
        locations = db.session.query(Job.location).distinct().all()
        locations = [location[0] for location in locations if location[0]]
        
        # Get all unique tags
        all_tags = []
        jobs = Job.query.all()
        for job in jobs:
            if job.tags:
                # Split tags by comma and add each one
                tags = [tag.strip() for tag in job.tags.split(',')]
                all_tags.extend(tags)
        
        # Remove duplicates and sort
        unique_tags = sorted(list(set(all_tags)))
        
        print(f"Filter options - Job types: {len(all_job_types)}, Locations: {len(locations)}, Tags: {len(unique_tags)}")
        print(f"Available job types: {all_job_types}")
        
        # Return all the filter options
        return jsonify({
            'job_types': all_job_types,
            'locations': locations,
            'tags': unique_tags
        }), 200
        
    except Exception as e:
        print(f"Error getting filters: {e}")
        return jsonify({'error': str(e)}), 500

# Error handlers for common HTTP errors
@job_bp.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors (resource not found)
    """
    return jsonify({'error': 'Resource not found'}), 404

@job_bp.errorhandler(400)
def bad_request(error):
    """
    Handle 400 errors (bad request - invalid data)
    """
    return jsonify({'error': 'Bad request'}), 400

@job_bp.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors (internal server error)
    """
    return jsonify({'error': 'Internal server error'}), 500
