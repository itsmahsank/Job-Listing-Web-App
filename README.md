# Job Listing Web App

A full-stack web application for managing and displaying job listings with advanced filtering, search capabilities, and web scraping functionality.

## 🚀 Features

### Frontend (React)
- **Modern UI/UX** with clean, responsive design
- **Advanced Filtering** by job type, location, tags, and search terms
- **Real-time Search** with instant results
- **Pagination** for large datasets
- **Job Management** - Add, edit, and delete jobs
- **Professional Styling** with custom CSS
- **Red-themed Delete Confirmations** for better UX

### Backend (Flask)
- **RESTful API** with comprehensive endpoints
- **PostgreSQL Database** with SQLAlchemy ORM
- **Advanced Filtering** and sorting capabilities
- **Pagination Support** for efficient data loading
- **Error Handling** and validation
- **CORS Support** for cross-origin requests

### Web Scraping (Selenium)
- **Automated Job Scraping** from ActuaryList
- **Intelligent Data Extraction** with duplicate prevention
- **Clean Data Processing** (removes emojis, salary info from locations)
- **Configurable Page Limits** (default: 10 pages)
- **Professional Data Quality** with filtering of invalid content

## 🛠️ Technology Stack

- **Frontend:** React, CSS3, Axios
- **Backend:** Flask, SQLAlchemy, PostgreSQL
- **Web Scraping:** Selenium, Python
- **Database:** PostgreSQL (Supabase)
- **Deployment:** Ready for deployment

## 📋 Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL database
- Chrome browser (for web scraping)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd job-listing-web-app
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

## 🚀 Deployment Ready

The application is structured for easy deployment:

### Backend Deployment
- Flask application ready for WSGI servers
- Environment variable configuration
- Database connection handling

### Frontend Deployment
- React build process
- Static file serving
- API proxy configuration

## 📈 Performance Features

- **Pagination** for large datasets
- **Efficient Database Queries** with proper indexing
- **Optimized Frontend** with React best practices
- **Caching** for filter options

## 🧪 Testing

The application includes:
- **Error Handling** throughout the stack
- **Input Validation** on all forms
- **API Response Validation**
- **Database Integrity** checks

## 📝 License

This project is for educational purposes and demonstrates full-stack development skills.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For questions or issues, please open an issue in the GitHub repository.

---

**Built with ❤️ using modern web technologies**
