import React, { useState } from 'react';
import './JobCard.css';

const JobCard = ({ job, onEdit, onDelete }) => {
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  // Format date function with error handling
  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) {
        return 'Date not available';
      }
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    } catch (error) {
      return 'Date not available';
    }
  };

  // Handle delete button click - show modal
  const handleDeleteClick = () => {
    setShowDeleteModal(true);
  };

  // Handle delete confirmation
  const handleDeleteConfirm = () => {
    onDelete(job.id);
    setShowDeleteModal(false);
  };

  // Handle delete cancellation
  const handleDeleteCancel = () => {
    setShowDeleteModal(false);
  };
  
  // Parse tags from string to array
  const parseTags = (tagsString) => {
    if (!tagsString) return [];
    return tagsString.split(',').map(tag => tag.trim()).filter(tag => tag);
  };
  
  // Get tags array
  const tagsList = typeof job.tags === 'string' ? parseTags(job.tags) : job.tags || [];

  return (
    <>
      <div className="job-card">
        {/* Header with title, company, and action buttons */}
        <div className="job-card-header">
          <div className="job-title-section">
            <h3 className="job-title">{job.title}</h3>
            <p className="job-company">{job.company}</p>
          </div>
          
          <div className="job-actions">
            <button 
              className="action-btn edit-btn"
              onClick={() => onEdit(job)}
              title="Edit this job"
            >
              Edit
            </button>
            <button 
              className="action-btn delete-btn"
              onClick={handleDeleteClick}
              title="Delete this job"
            >
              Delete
            </button>
          </div>
        </div>

        {/* Job subtitle section with location, job type, experience level, and salary */}
        <div className="job-subtitle">
          <div className="job-location">
            {job.location || 'Remote'}
          </div>
          <div className="job-type-badge">
            {job.job_type}
          </div>
          {job.experience_level && job.experience_level !== 'Not Specified' && (
            <div className="job-experience-badge">
              {job.experience_level}
            </div>
          )}
        </div>
        
        {/* Salary range if available */}
        {job.salary_range && job.salary_range !== 'Not Specified' && (
          <div className="job-salary">
            {job.salary_range}
          </div>
        )}

        {/* Job tags */}
        {tagsList.length > 0 && (
          <div className="job-tags">
            {tagsList.map((tag, index) => (
              <span key={index} className="job-tag">
                {tag}
              </span>
            ))}
          </div>
        )}

        {/* No job details section as per requirements */}

        {/* Footer with posting date */}
        <div className="job-footer">
          <span className="job-date">
            Posted: {formatDate(job.posting_date || job.created_at)}
          </span>
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="delete-modal-overlay">
          <div className="delete-modal">
            <div className="delete-modal-header">
              <h3>⚠️ Delete Job</h3>
            </div>
            <div className="delete-modal-content">
              <p>Are you sure you want to delete this job?</p>
              <div className="job-preview">
                <strong>{job.title}</strong>
                <br />
                <span>{job.company}</span>
              </div>
              <p className="delete-warning">This action cannot be undone.</p>
            </div>
            <div className="delete-modal-actions">
              <button 
                className="delete-modal-btn cancel-btn"
                onClick={handleDeleteCancel}
              >
                Cancel
              </button>
              <button 
                className="delete-modal-btn confirm-btn"
                onClick={handleDeleteConfirm}
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default JobCard;
