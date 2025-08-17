from sqlalchemy import Column, Integer, String, Text, DateTime, Date
from datetime import datetime
from db import db

# Use Flask-SQLAlchemy's db.Model
class Job(db.Model):
    """
    This is the Job model - it represents a table in our database
    Each job posting will be stored as a row in this table
    """
    
    # Tell SQLAlchemy what table name to use
    __tablename__ = 'jobs'
    
    # Define all the columns in our jobs table
    # Each column stores a different piece of information about a job
    
    # Primary key - unique identifier for each job
    id = Column(Integer, primary_key=True)
    
    # Job title (e.g., "Senior Actuary", "Actuarial Analyst")
    title = Column(String(200), nullable=False)
    
    # Company name (e.g., "ABC Insurance", "XYZ Corp")
    company = Column(String(100), nullable=False)
    
    # Job location (e.g., "New York, NY", "Remote", "London, UK")
    location = Column(String(100), nullable=False)
    
    # When the job was posted (date)
    posting_date = Column(DateTime, nullable=False)
    
    # Type of job (e.g., "Full-time", "Part-time", "Contract")
    job_type = Column(String(50), default='Full-time')
    
    # Tags/keywords for the job (e.g., "Life", "Health", "Pricing")
    # Store as comma-separated string for simplicity
    tags = Column(Text)
    
    # Detailed job description
    description = Column(Text)
    
    # Salary information (e.g., "$80,000 - $120,000")
    salary_range = Column(String(100))
    
    # Experience level required (e.g., "Entry Level", "Senior")
    experience_level = Column(String(50))
    
    # When this record was created in our database
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # When this record was last updated
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    """
    This is the Job model - it represents a table in our database
    Each job posting will be stored as a row in this table
    """
    
    # Tell SQLAlchemy what table name to use
    __tablename__ = 'jobs'
    
    # Define all the columns in our jobs table
    # Each column stores a different piece of information about a job
    
    # Primary key - unique identifier for each job
    id = Column(Integer, primary_key=True)
    
    # Job title (e.g., "Senior Actuary", "Actuarial Analyst")
    title = Column(String(200), nullable=False)
    
    # Company name (e.g., "ABC Insurance", "XYZ Corp")
    company = Column(String(100), nullable=False)
    
    # Job location (e.g., "New York, NY", "Remote", "London, UK")
    location = Column(String(100), nullable=False)
    
    # When the job was posted (date)
    posting_date = Column(DateTime, nullable=False)
    
    # Type of job (e.g., "Full-time", "Part-time", "Contract")
    job_type = Column(String(50), default='Full-time')
    
    # Tags/keywords for the job (e.g., "Life", "Health", "Pricing")
    # Store as comma-separated string for simplicity
    tags = Column(Text)
    
    # Detailed job description
    description = Column(Text)
    
    # Salary information (e.g., "$80,000 - $120,000")
    salary_range = Column(String(100))
    
    # Experience level required (e.g., "Entry Level", "Senior")
    experience_level = Column(String(50))
    
    # When this record was created in our database
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # When this record was last updated
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """
        Convert the job object to a dictionary
        This makes it easy to send job data to the frontend as JSON
        """
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'posting_date': self.posting_date.isoformat() if self.posting_date else None,
            'job_type': self.job_type,
            'tags': self.tags.split(', ') if self.tags else [],
            'description': self.description,
            'salary_range': self.salary_range,
            'experience_level': self.experience_level,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a new Job object from a dictionary
        This is useful when the frontend sends us job data to create/update
        """
        # Handle the posting_date field specially
        posting_date = data.get('posting_date')
        if isinstance(posting_date, str):
            try:
                # Try to parse the date string
                posting_date = datetime.fromisoformat(posting_date.replace('Z', '+00:00'))
            except ValueError:
                # If we can't parse it, use current time
                posting_date = datetime.utcnow()
        elif not posting_date:
            # If no date provided, use current time
            posting_date = datetime.utcnow()
        
        # Handle tags field - convert list to comma-separated string
        tags = data.get('tags')
        if isinstance(tags, list):
            tags = ', '.join(tags)
        
        # Create and return the new Job object
        return cls(
            title=data.get('title', ''),
            company=data.get('company', ''),
            location=data.get('location', ''),
            posting_date=posting_date,
            job_type=data.get('job_type', 'Full-time'),
            tags=tags,
            description=data.get('description', ''),
            salary_range=data.get('salary_range', ''),
            experience_level=data.get('experience_level', '')
        )

    def __repr__(self):
        """
        This is what you see when you print a Job object
        Useful for debugging
        """
        return f"<Job(id={self.id}, title='{self.title}', company='{self.company}')>"
