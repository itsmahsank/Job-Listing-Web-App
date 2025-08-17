import React, { useState, useEffect, useCallback } from 'react';
import Header from './components/Header';
import FilterBar from './components/FilterBar';
import JobList from './components/JobList';
import JobForm from './components/JobForm';
import { jobAPI, handleAPIError } from './api';
import './App.css';

function App() {
  // Simple state variables - no complex objects
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  // Note: error state is not currently used but kept for future error handling
  const [error] = useState(null);
  
  // Simple filter state
  const [searchText, setSearchText] = useState('');
  const [jobTypeFilter, setJobTypeFilter] = useState('All');
  const [locationFilter, setLocationFilter] = useState('All');
  const [tagsFilter, setTagsFilter] = useState('All');
  const [sortBy, setSortBy] = useState('posting_date_desc');
  
  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [totalJobs, setTotalJobs] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [hasNextPage, setHasNextPage] = useState(false);
  const [hasPrevPage, setHasPrevPage] = useState(false);
  
  // Form state
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingJob, setEditingJob] = useState(null);
  const [message, setMessage] = useState(null);

  // Simple function to load jobs
  const loadJobs = useCallback(async () => {
    try {
      setLoading(true);
      
      // Make API call to get jobs
      const response = await jobAPI.getJobs({ 
        page: currentPage,
        per_page: 5,
        search: searchText,
        job_type: jobTypeFilter,
        location: locationFilter,
        tags: tagsFilter,
        sort: sortBy
      });
      
      // Update state with response data
      setJobs(response.jobs || []);
      setTotalJobs(response.total || 0);
      setTotalPages(response.pages || 0);
      setHasNextPage(response.has_next || false);
      setHasPrevPage(response.has_prev || false);
      
      setLoading(false);
      
      // Log for debugging
      console.log('Loaded jobs:', response.jobs?.length, 'out of', response.total);
      
    } catch (error) {
      console.error('Error loading jobs:', error);
      setMessage({ text: 'Failed to load jobs', type: 'error' });
      setLoading(false);
    }
  }, [currentPage, searchText, jobTypeFilter, locationFilter, tagsFilter, sortBy]);

  // Load jobs when filters change or component mounts
  useEffect(() => {
    loadJobs();
  }, [loadJobs]);

  // Handle filter changes
  const handleSearchChange = (newSearch) => {
    setSearchText(newSearch);
    setCurrentPage(1); // Go back to first page
  };

  const handleJobTypeChange = (newJobType) => {
    setJobTypeFilter(newJobType);
    setCurrentPage(1);
  };

  const handleLocationChange = (newLocation) => {
    setLocationFilter(newLocation);
    setCurrentPage(1);
  };

  const handleTagsChange = (newTags) => {
    setTagsFilter(newTags);
    setCurrentPage(1);
  };

  const handleSortChange = (newSort) => {
    setSortBy(newSort);
    setCurrentPage(1);
  };

  // Clear all filters
  const clearAllFilters = () => {
    setSearchText('');
    setJobTypeFilter('All');
    setLocationFilter('All');
    setTagsFilter('All');
    setSortBy('posting_date_desc');
    setCurrentPage(1);
  };

  // Handle page change
  const handlePageChange = (newPage) => {
    console.log('Changing to page:', newPage);
    setCurrentPage(newPage);
  };

  // Handle add job button click
  const handleAddJobClick = () => {
    setEditingJob(null);
    setShowAddForm(true);
  };

  // Handle edit job
  const handleEditJob = (job) => {
    setEditingJob(job);
    setShowAddForm(true);
  };

  // Handle delete job
  const handleDeleteJob = async (jobId) => {
    try {
      await jobAPI.deleteJob(jobId);
      showMessage('Job deleted successfully!', 'delete');
      loadJobs(); // Reload the list
    } catch (err) {
      const errorMessage = handleAPIError(err);
      showMessage(errorMessage, 'error');
    }
  };

  // Handle form submit
  const handleFormSubmit = async (jobData) => {
    try {
      if (editingJob) {
        // Update existing job
        await jobAPI.updateJob(editingJob.id, jobData);
        showMessage('Job updated successfully!', 'success');
      } else {
        // Create new job
        await jobAPI.createJob(jobData);
        showMessage('Job added successfully!', 'success');
      }
      
      setShowAddForm(false);
      setEditingJob(null);
      loadJobs(); // Reload the list
      
    } catch (err) {
      const errorMessage = handleAPIError(err);
      showMessage(errorMessage, 'error');
      throw err; // Let form handle the error
    }
  };

  // Handle form cancel
  const handleFormCancel = () => {
    setShowAddForm(false);
    setEditingJob(null);
  };

  // Show message to user
  const showMessage = (text, type = 'info') => {
    setMessage({ text, type });
    // Hide message after 5 seconds
    setTimeout(() => setMessage(null), 5000);
  };

  // Create filters object for FilterBar
  const filters = {
    search: searchText,
    job_type: jobTypeFilter,
    location: locationFilter,
    tags: tagsFilter,
    sort: sortBy
  };

  // Create pagination object for JobList
  const pagination = {
    currentPage: currentPage,
    totalPages: totalPages,
    totalJobs: totalJobs,
    hasNext: hasNextPage,
    hasPrev: hasPrevPage,
    perPage: 5
  };

  return (
    <div className="App">
      {/* Header with add job button */}
      <Header onAddJobClick={handleAddJobClick} />
      
      <main className="main-content">
        {/* Filter bar for searching and filtering jobs */}
        <FilterBar
          filters={filters}
          onSearchChange={handleSearchChange}
          onJobTypeChange={handleJobTypeChange}
          onLocationChange={handleLocationChange}
          onTagsChange={handleTagsChange}
          onSortChange={handleSortChange}
          onClearFilters={clearAllFilters}
        />
        
        {/* List of jobs with pagination */}
        <JobList
          jobs={jobs}
          loading={loading}
          error={error}
          onEdit={handleEditJob}
          onDelete={handleDeleteJob}
          pagination={pagination}
          onPageChange={handlePageChange}
        />
      </main>

      {/* Add/Edit job form */}
      {showAddForm && (
        <JobForm
          job={editingJob}
          onSubmit={handleFormSubmit}
          onCancel={handleFormCancel}
          isEditing={!!editingJob}
        />
      )}

      {/* Success/Error message */}
      {message && (
        <div className={`message ${message.type}`}>
          <span className="message-text">{message.text}</span>
          <button 
            className="message-close"
            onClick={() => setMessage(null)}
          >
            ×
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
