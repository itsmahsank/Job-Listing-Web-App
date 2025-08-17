# Job Listing Web App

A full-stack web application built as a learning project to demonstrate modern web development skills. This project showcases my journey in mastering React, Flask, and web scraping technologies.


## 🚀 Key Features Implemented

### Frontend (React)
- **Modern React Hooks** - useState, useEffect, useCallback for state management
- **Component Architecture** - Modular, reusable components
- **Advanced Filtering System** - Real-time search, job type, location, and tag filters
- **Responsive Design** - Mobile-first approach with CSS Grid and Flexbox
- **Professional UI/UX** - Clean design with smooth animations and transitions
- **Form Validation** - Client-side validation with error handling
- **Custom Modal System** - Red-themed delete confirmations for better UX

### Backend (Flask)
- **RESTful API Design** - Clean, intuitive endpoints following REST principles
- **Database Integration** - PostgreSQL with SQLAlchemy ORM
- **Advanced Querying** - Complex filtering, sorting, and pagination
- **Error Handling** - Comprehensive error responses and logging
- **CORS Configuration** - Secure cross-origin request handling
- **Environment Management** - Secure configuration with environment variables

### Web Scraping (Selenium)
- **Automated Data Collection** - Scraping from ActuaryList.com
- **Intelligent Data Processing** - Removing emojis, cleaning location data
- **Duplicate Prevention** - Smart duplicate detection and handling
- **Error Resilience** - Robust error handling and retry mechanisms
- **Configurable Limits** - Adjustable page limits and data extraction

## 🛠️ Technology Stack

### Frontend
- **React 18** - Modern React with hooks and functional components
- **CSS3** - Custom styling with Grid, Flexbox, and animations
- **Axios** - HTTP client for API communication

### Backend
- **Flask** - Lightweight Python web framework
- **SQLAlchemy** - Python SQL toolkit and ORM
- **PostgreSQL** - Robust relational database
- **Python-dotenv** - Environment variable management

### Web Scraping
- **Selenium** - Web browser automation
- **Chrome WebDriver** - Headless browser for scraping
- **Beautiful Soup** - HTML parsing and data extraction

### Development Tools
- **Git** - Version control
- **GitHub** - Code repository and collaboration
- **VS Code** - Development environment

## 📋 Learning Objectives Achieved

### Full-Stack Development
- ✅ **Frontend-Backend Integration** - Seamless communication between React and Flask
- ✅ **Database Design** - Proper schema design and relationships
- ✅ **API Development** - RESTful API with proper HTTP methods
- ✅ **State Management** - Efficient state handling across components

### Modern Web Technologies
- ✅ **React Hooks** - Functional components with state and effects
- ✅ **Async/Await** - Modern JavaScript for API calls
- ✅ **CSS Grid & Flexbox** - Modern layout techniques
- ✅ **Responsive Design** - Mobile-first responsive layouts

### Data Processing
- ✅ **Web Scraping** - Automated data collection from websites
- ✅ **Data Cleaning** - Removing unwanted characters and formatting
- ✅ **Duplicate Detection** - Smart duplicate prevention algorithms
- ✅ **Data Validation** - Input validation and sanitization

### Professional Development
- ✅ **Code Organization** - Clean, maintainable code structure
- ✅ **Error Handling** - Comprehensive error management
- ✅ **Documentation** - Clear code comments and README
- ✅ **Version Control** - Proper Git workflow and commits

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL database
- Chrome browser (for web scraping)

### 1. Clone the Repository
```bash
git clone https://github.com/itsmahsank/Job-Listing-Web-App.git
cd Job-Listing-Web-App
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the backend directory:
```env
DATABASE_URL="your_postgresql_connection_string"
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Database Setup
```bash
cd backend
python init_db.py
```

### 5. Run the Application

**Backend:**
```bash
cd backend
python app.py
```

**Frontend:**
```bash
cd frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## 🔧 Web Scraping

To populate the database with real job data:

```bash
cd scraper
pip install -r requirements.txt
python scrape_simple_fast.py
```

**Features:**
- Scrapes from ActuaryList.com
- Extracts job titles, companies, locations, salaries
- Prevents duplicates automatically
- Cleans location data (removes emojis, salary info)
- Configurable page limits

## 📊 API Endpoints

### Jobs
- `GET /api/jobs` - List all jobs with filtering and pagination
- `POST /api/jobs` - Create a new job
- `PUT /api/jobs/<id>` - Update an existing job
- `DELETE /api/jobs/<id>` - Delete a job
- `GET /api/jobs/filters` - Get available filter options

### Query Parameters
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 5)
- `search` - Search text
- `job_type` - Filter by job type
- `location` - Filter by location
- `tags` - Filter by tags
- `sort` - Sort order

## 🎨 UI Features

### Filtering System
- **Search Bar** - Real-time text search
- **Job Type Filter** - Full-time, Part-time, Contract, etc.
- **Location Filter** - Clean location options (no emojis)
- **Tags Filter** - Skill-based filtering
- **Sort Options** - Date, title, company sorting

### Job Management
- **Add Jobs** - Comprehensive job form
- **Edit Jobs** - In-place editing
- **Delete Jobs** - Red-themed confirmation modal
- **Job Cards** - Professional display with all details

### Responsive Design
- **Mobile-friendly** layout
- **Clean typography** and spacing
- **Professional color scheme**
- **Smooth animations**

## 🗄️ Database Schema

### Jobs Table
- `id` - Primary key
- `title` - Job title
- `company` - Company name
- `location` - Job location (cleaned)
- `job_type` - Employment type
- `salary_range` - Salary information
- `experience_level` - Required experience
- `tags` - Skills and keywords
- `description` - Job description
- `posting_date` - When posted
- `created_at` - Record creation time
- `updated_at` - Last update time

## 🔒 Security Features

- **Input Validation** on all forms
- **SQL Injection Prevention** with parameterized queries
- **CORS Configuration** for secure cross-origin requests
- **Environment Variables** for sensitive data

## 📈 Performance Features

- **Pagination** for large datasets
- **Efficient Database Queries** with proper indexing
- **Optimized Frontend** with React best practices
- **Caching** for filter options

## 🧪 Testing & Quality

The application includes:
- **Error Handling** throughout the stack
- **Input Validation** on all forms
- **API Response Validation**
- **Database Integrity** checks

## 🎓 Skills Demonstrated

### Technical Skills
- **Full-Stack Development** - React + Flask + PostgreSQL
- **API Design** - RESTful API with proper HTTP methods
- **Database Management** - Schema design and query optimization
- **Web Scraping** - Automated data collection and processing
- **Responsive Design** - Mobile-first CSS with modern techniques
- **State Management** - Efficient React state handling
- **Error Handling** - Comprehensive error management

### Soft Skills
- **Problem Solving** - Tackling complex technical challenges
- **Learning Ability** - Mastering new technologies quickly
- **Attention to Detail** - Clean code and professional UI
- **Documentation** - Clear project documentation
- **Version Control** - Proper Git workflow

## 🚀 Future Enhancements

As I continue learning, I plan to add:
- **Authentication System** - User login and registration
- **Real-time Updates** - WebSocket integration
- **Advanced Analytics** - Job market insights
- **Mobile App** - React Native version
- **Deployment** - Cloud deployment (AWS/Azure)
- **Testing** - Unit and integration tests
- **CI/CD Pipeline** - Automated testing and deployment

## 📝 Project Journey

This project represents my learning journey in web development:

1. **Started with basics** - HTML, CSS, JavaScript
2. **Learned React** - Modern frontend development
3. **Explored backend** - Flask and Python
4. **Database integration** - PostgreSQL and SQLAlchemy
5. **Web scraping** - Data collection and processing
6. **Advanced features** - Filtering, search, pagination
7. **Professional touches** - Error handling, documentation

## 🤝 Contributing

As a learning project, I welcome feedback and suggestions:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

##  Contact

- **GitHub:** [@itsmahsank](https://github.com/itsmahsank)
- **LinkedIn:** https://www.linkedin.com/in/itsahsank/ 
- **Email:** itsmahsank@gmail.com

## 📝 License

This project  demonstrates my full-stack development skills.

---
