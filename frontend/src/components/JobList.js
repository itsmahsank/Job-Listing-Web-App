import React from 'react';
import JobCard from './JobCard';
import './JobList.css';

// Job list component - shows jobs with pagination
const JobList = ({ 
  jobs, 
  loading, 
  error, 
  onEdit, 
  onDelete, 
  pagination, 
  onPageChange 
}) => {
  
  // Show loading spinner
  if (loading) {
    return (
      <div className="job-list">
        <div className="loading-container">
          <p>Loading</p>
        </div>
      </div>
    );
  }

  // Show error if something went wrong
  if (error) {
    return (
      <div className="job-list">
        <div className="error-container">
          <div className="error-icon">!</div>
          <h3>Error Loading Jobs</h3>
          <p>{error}</p>
          <button 
            className="retry-btn"
            onClick={() => window.location.reload()}
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  // Show message if no jobs
  if (!jobs || jobs.length === 0) {
    return (
      <div className="job-list">
        <div className="empty-container">
          <div className="empty-icon">📄</div>
          <h3>No jobs found</h3>
          <p>Try adjusting your filters or search terms</p>
        </div>
      </div>
    );
  }

  // Calculate job numbers for display
  const jobsPerPage = pagination.perPage;
  const currentPage = pagination.currentPage;
  const totalJobs = pagination.totalJobs;
  
  const firstJob = (currentPage - 1) * jobsPerPage + 1;
  const lastJob = Math.min(currentPage * jobsPerPage, totalJobs);

  return (
    <div className="job-list">
      
      {/* Job cards */}
      <div className="job-cards">
        {jobs.map((job) => (
          <JobCard
            key={job.id}
            job={job}
            onEdit={onEdit}
            onDelete={onDelete}
          />
        ))}
      </div>

      {/* Pagination */}
      {pagination.totalPages > 1 && (
        <div className="pagination">
          
          <button
            className="pagination-btn"
            onClick={() => onPageChange(currentPage - 1)}
            disabled={!pagination.hasPrev}
          >
            ← Previous
          </button>
          
          <div className="page-numbers">
            {Array.from({ length: pagination.totalPages }, (_, i) => i + 1)
              .map((pageNumber) => (
                <button
                  key={pageNumber}
                  className={`page-btn ${pageNumber === currentPage ? 'active' : ''}`}
                  onClick={() => onPageChange(pageNumber)}
                >
                  {pageNumber}
                </button>
              ))}
          </div>
          
          <button
            className="pagination-btn"
            onClick={() => onPageChange(currentPage + 1)}
            disabled={!pagination.hasNext}
          >
            Next →
          </button>
        </div>
      )}

      {/* Job count at bottom */}
      <div className="job-list-footer">
        <div className="job-count">
          Showing {firstJob}-{lastJob} of {totalJobs} jobs
        </div>
        
        {pagination.totalPages > 1 && (
          <div className="pagination-info">
            Page {currentPage} of {pagination.totalPages}
          </div>
        )}
      </div>
    </div>
  );
};

export default JobList;
