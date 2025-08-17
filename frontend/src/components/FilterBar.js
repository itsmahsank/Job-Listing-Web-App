import React, { useState, useEffect } from 'react';
import { jobAPI } from '../api';
import './FilterBar.css';

const FilterBar = ({ 
  filters, 
  onSearchChange, 
  onJobTypeChange, 
  onLocationChange, 
  onTagsChange, 
  onSortChange, 
  onClearFilters 
}) => {
  // State for filter options
  const [jobTypes, setJobTypes] = useState([]);
  const [locations, setLocations] = useState([]);
  const [tags, setTags] = useState([]);

  // Load filter options when component loads
  useEffect(() => {
    loadFilterOptions();
  }, []);

  // Function to load filter options from API
  const loadFilterOptions = async () => {
    try {
      // Get filter options from backend
      const data = await jobAPI.getFilters();
      
      // Update state with the options
      setJobTypes(data.job_types || []);
      setLocations(data.locations || []);
      setTags(data.tags || []);
      
    } catch (error) {
      console.error('Error loading filter options:', error);
    }
  };

  // Check if any filters are active
  const hasActiveFilters = () => {
    return filters.search || 
           filters.job_type !== 'All' || 
           filters.location !== 'All' || 
           filters.tags !== 'All';
  };
  
  // Get active filter count
  const getActiveFilterCount = () => {
    let count = 0;
    if (filters.search) count++;
    if (filters.job_type !== 'All') count++;
    if (filters.location !== 'All') count++;
    if (filters.tags !== 'All') count++;
    return count;
  };
  
  // Get active filter count badge
  const activeFilterCount = getActiveFilterCount();

  return (
    <div className="filter-bar">
      <div className="filter-header">
        <h3 className="filter-title">Filter Jobs</h3>
        {activeFilterCount > 0 && (
          <div className="active-filter-badge">
            {activeFilterCount}
          </div>
        )}
      </div>
      
      <div className="filter-container">
        
        {/* Search input */}
        <div className="filter-section">
          <label htmlFor="search" className="filter-label">Search</label>
          <div className="search-input-container">
            <input
              type="text"
              id="search"
              className="filter-input"
              placeholder="Search jobs, companies..."
              value={filters.search || ''}
              onChange={(e) => onSearchChange(e.target.value)}
            />
            {filters.search && (
              <button 
                className="search-clear-btn" 
                onClick={() => onSearchChange('')}
                aria-label="Clear search"
              >
                ×
              </button>
            )}
            <span className="search-icon"></span>
          </div>
        </div>

        {/* Job Type dropdown */}
        <div className="filter-section">
          <label htmlFor="job_type" className="filter-label">Job Type</label>
          <select
            id="job_type"
            className={`filter-select ${filters.job_type !== 'All' ? 'active-filter' : ''}`}
            value={filters.job_type || 'All'}
            onChange={(e) => onJobTypeChange(e.target.value)}
          >
            <option value="All">All Types</option>
            {jobTypes.map((type, index) => (
              <option key={index} value={type}>{type}</option>
            ))}
          </select>
        </div>

        {/* Location dropdown */}
        <div className="filter-section">
          <label htmlFor="location" className="filter-label">Location</label>
          <select
            id="location"
            className={`filter-select ${filters.location !== 'All' ? 'active-filter' : ''}`}
            value={filters.location || 'All'}
            onChange={(e) => onLocationChange(e.target.value)}
          >
            <option value="All">All Locations</option>
            {locations.map((location, index) => (
              <option key={index} value={location}>{location}</option>
            ))}
          </select>
        </div>

        {/* Tags dropdown */}
        <div className="filter-section">
          <label htmlFor="tags" className="filter-label">Tags</label>
          <select
            id="tags"
            className={`filter-select ${filters.tags !== 'All' ? 'active-filter' : ''}`}
            value={filters.tags || 'All'}
            onChange={(e) => onTagsChange(e.target.value)}
          >
            <option value="All">All Tags</option>
            {tags.map((tag, index) => (
              <option key={index} value={tag}>{tag}</option>
            ))}
          </select>
        </div>

        {/* Sort dropdown */}
        <div className="filter-section">
          <label htmlFor="sort" className="filter-label">Sort By</label>
          <select
            id="sort"
            className={`filter-select sort-select ${filters.sort !== 'posting_date_desc' ? 'active-filter' : ''}`}
            value={filters.sort || 'posting_date_desc'}
            onChange={(e) => onSortChange(e.target.value)}
          >
            <option value="posting_date_desc">Date Posted: Newest First</option>
            <option value="posting_date_asc">Date Posted: Oldest First</option>
            <option value="title_asc">Title A-Z</option>
            <option value="title_desc">Title Z-A</option>
            <option value="company_asc">Company A-Z</option>
            <option value="company_desc">Company Z-A</option>
          </select>
        </div>

        {/* Clear filters button */}
        <div className="filter-section clear-filters-section">
          <button
            className={`clear-filters-btn ${!hasActiveFilters() ? 'disabled' : ''}`}
            onClick={onClearFilters}
            disabled={!hasActiveFilters()}
          >
            <span className="clear-icon"></span>
            Clear All Filters
          </button>
        </div>

      </div>
    </div>
  );
};

export default FilterBar;
