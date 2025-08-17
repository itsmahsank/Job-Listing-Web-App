import React, { useState, useEffect } from 'react';
import './JobForm.css';

const JobForm = ({ job, onSubmit, onCancel, isEditing = false }) => {
  // Form data state
  const [formData, setFormData] = useState({
    title: '',
    company: '',
    location: '',
    job_type: 'Full-time',
    tags: '',
    description: '',
    salary_range: '',
    experience_level: ''
  });
  
  // Error state
  const [errors, setErrors] = useState({});
  
  // Loading state
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  // Success message state
  const [successMessage, setSuccessMessage] = useState('');

  // Load job data when editing
  useEffect(() => {
    if (job) {
      // If editing, fill form with existing job data
      setFormData({
        title: job.title || '',
        company: job.company || '',
        location: job.location || '',
        job_type: job.job_type || 'Full-time',
        tags: Array.isArray(job.tags) ? job.tags.join(', ') : job.tags || '',
        description: job.description || '',
        salary_range: job.salary_range || '',
        experience_level: job.experience_level || ''
      });
      
      // Clear any previous errors or success messages
      setErrors({});
      setSuccessMessage('');
    }
  }, [job]);

  // Check if form is valid
  const validateForm = () => {
    const newErrors = {};

    // Check required fields
    if (!formData.title.trim()) {
      newErrors.title = 'Job title is required';
    } else if (formData.title.trim().length < 3) {
      newErrors.title = 'Job title must be at least 3 characters';
    }

    if (!formData.company.trim()) {
      newErrors.company = 'Company name is required';
    } else if (formData.company.trim().length < 2) {
      newErrors.company = 'Company name must be at least 2 characters';
    }

    if (!formData.location.trim()) {
      newErrors.location = 'Location is required';
    }
    
    // Validate tags format if provided
    if (formData.tags && !formData.tags.split(',').every(tag => tag.trim().length > 0)) {
      newErrors.tags = 'Tags must be comma-separated values';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle input changes
  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));

    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: ''
      }));
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Clear previous success message
    setSuccessMessage('');
    
    // Validate form first
    if (!validateForm()) {
      // Scroll to the first error
      const firstErrorField = document.querySelector('.form-input.error');
      if (firstErrorField) {
        firstErrorField.scrollIntoView({ behavior: 'smooth', block: 'center' });
        firstErrorField.focus();
      }
      return;
    }

    setIsSubmitting(true);

    try {
      // Convert tags string to array and clean up
      const jobData = {
        ...formData,
        tags: formData.tags.split(',').map(tag => tag.trim()).filter(tag => tag)
      };

      // Submit the form
      await onSubmit(jobData);
      
      // Show success message
      setSuccessMessage(isEditing ? 'Job updated successfully!' : 'Job added successfully!');
      
      // If not editing (adding new job), reset form after successful submission
      if (!isEditing) {
        setFormData({
          title: '',
          company: '',
          location: '',
          job_type: 'Full-time',
          tags: '',
          description: '',
          salary_range: '',
          experience_level: ''
        });
      }
      
      // Auto-close form after success (optional)
      // setTimeout(() => onCancel(), 2000);
      
    } catch (error) {
      console.error('Error submitting form:', error);
      // Handle API errors
      if (error.response && error.response.data) {
        const apiErrors = error.response.data.errors || {};
        setErrors(prev => ({ ...prev, ...apiErrors }));
      } else {
        setErrors(prev => ({ 
          ...prev, 
          form: 'An error occurred while saving the job. Please try again.'
        }));
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle cancel button
  const handleCancel = () => {
    onCancel();
  };

  return (
    <div className="job-form-overlay">
      <div className="job-form-modal">
        {/* Form header */}
        <div className="job-form-header">
          <h2>{isEditing ? 'Edit Job' : 'Add New Job'}</h2>
          <button 
            className="close-btn"
            onClick={handleCancel}
            type="button"
            aria-label="Close"
          >
            ×
          </button>
        </div>

        {/* Form body */}
        <form onSubmit={handleSubmit} className="job-form">
          {/* Success message */}
          {successMessage && (
            <div className="success-message">
              <span className="success-icon">✓</span> {successMessage}
            </div>
          )}
          
          {/* Form error */}
          {errors.form && (
            <div className="form-error-message">
              <span className="error-icon">!</span> {errors.form}
            </div>
          )}
          {/* Job Title */}
          <div className="form-group">
            <label htmlFor="title" className="form-label">Job Title *</label>
            <input
              type="text"
              id="title"
              className={`form-input ${errors.title ? 'error' : ''}`}
              value={formData.title}
              onChange={(e) => handleInputChange('title', e.target.value)}
              placeholder="Enter job title"
            />
            {errors.title && <span className="error-message">{errors.title}</span>}
          </div>

          {/* Company */}
          <div className="form-group">
            <label htmlFor="company" className="form-label">Company *</label>
            <input
              type="text"
              id="company"
              className={`form-input ${errors.company ? 'error' : ''}`}
              value={formData.company}
              onChange={(e) => handleInputChange('company', e.target.value)}
              placeholder="Enter company name"
            />
            {errors.company && <span className="error-message">{errors.company}</span>}
          </div>

          {/* Location */}
          <div className="form-group">
            <label htmlFor="location" className="form-label">Location *</label>
            <input
              type="text"
              id="location"
              className={`form-input ${errors.location ? 'error' : ''}`}
              value={formData.location}
              onChange={(e) => handleInputChange('location', e.target.value)}
              placeholder="Enter location (city, state, country)"
            />
            {errors.location && <span className="error-message">{errors.location}</span>}
          </div>

          {/* Job Type */}
          <div className="form-group">
            <label htmlFor="job_type" className="form-label">Job Type</label>
            <select
              id="job_type"
              className="form-select"
              value={formData.job_type}
              onChange={(e) => handleInputChange('job_type', e.target.value)}
            >
              <option value="Full-time">Full-time</option>
              <option value="Part-time">Part-time</option>
              <option value="Contract">Contract</option>
              <option value="Internship">Internship</option>
              <option value="Temporary">Temporary</option>
            </select>
          </div>

          {/* Tags */}
          <div className="form-group">
            <label htmlFor="tags" className="form-label">Tags</label>
            <input
              type="text"
              id="tags"
              className="form-input"
              value={formData.tags}
              onChange={(e) => handleInputChange('tags', e.target.value)}
              placeholder="Enter tags separated by commas (e.g., Life, Health, Pricing)"
            />
          </div>

          {/* Description */}
          <div className="form-group">
            <label htmlFor="description" className="form-label">Description</label>
            <textarea
              id="description"
              className="form-textarea"
              value={formData.description}
              onChange={(e) => handleInputChange('description', e.target.value)}
              placeholder="Enter job description"
              rows="4"
            />
          </div>

          {/* Salary Range */}
          <div className="form-group">
            <label htmlFor="salary_range" className="form-label">Salary Range</label>
            <input
              type="text"
              id="salary_range"
              className="form-input"
              value={formData.salary_range}
              onChange={(e) => handleInputChange('salary_range', e.target.value)}
              placeholder="Enter salary range (e.g., $50,000 - $80,000)"
            />
          </div>

          {/* Experience Level */}
          <div className="form-group">
            <label htmlFor="experience_level" className="form-label">Experience Level</label>
            <select
              id="experience_level"
              className="form-select"
              value={formData.experience_level}
              onChange={(e) => handleInputChange('experience_level', e.target.value)}
            >
              <option value="">Select experience level</option>
              <option value="Entry Level">Entry Level</option>
              <option value="Mid Level">Mid Level</option>
              <option value="Senior Level">Senior Level</option>
              <option value="Executive">Executive</option>
            </select>
          </div>

          {/* Form buttons */}
          <div className="form-actions">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={handleCancel}
              disabled={isSubmitting}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <span className="loading-spinner">
                  <span className="spinner-icon"></span>
                  <span className="spinner-text">{isEditing ? 'Updating...' : 'Adding...'}</span>
                </span>
              ) : (
                isEditing ? 'Update Job' : 'Add Job'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default JobForm;
