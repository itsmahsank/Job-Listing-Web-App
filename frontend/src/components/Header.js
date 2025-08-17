import React from 'react';
import './Header.css';

const Header = ({ onAddJobClick }) => {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo-container">
          <a href="/" className="logo">
            <span className="logo-text">Job Finder</span>
          </a>
          <span className="logo-tagline">Find your dream job</span>
        </div>
        
        <button 
          className="add-job-btn"
          onClick={onAddJobClick}
          aria-label="Add new job listing"
        >
          <span className="add-icon">+</span>
          <span className="btn-text">Add Job</span>
        </button>
      </div>
    </header>
  );
};

export default Header;
