# Quick Start Guide - Job Listing Web App

This guide will help you get the Job Listing Web App up and running quickly.

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- A database (PostgreSQL, MySQL, or SQLite)

## Quick Setup

### 1. Clone and Navigate

```bash
git clone <your-repo-url>
cd "Job Listing Web App"
```

### 2. Run the Setup Script

```bash
python setup.py
```

This script will:
- Check your Python and Node.js versions
- Set up the Python backend with virtual environment
- Install all Python dependencies
- Set up the React frontend
- Install all Node.js dependencies
- Create a sample environment file

### 3. Configure Database

Edit `backend/.env` file with your database settings:

```env
DATABASE_URL=postgresql://username:password@localhost/jobdb
```

Or use SQLite for development:
```env
DATABASE_URL=sqlite:///jobs.db
```

### 4. Start the Backend

```bash
cd backend
python app.py
```

The Flask server will start at `http://localhost:5000`

### 5. Start the Frontend

In a new terminal:

```bash
cd frontend
npm start
```

The React app will open at `http://localhost:3000`

### 6. Add Sample Data (Optional)

```bash
cd backend
python sample_data.py
```

## Manual Setup (Alternative)

If you prefer to set up manually:

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Change ports in `app.py` (backend) or `package.json` (frontend)
2. **Database connection failed**: Check your `.env` file and database status
3. **Dependencies not found**: Make sure virtual environment is activated (backend) or `node_modules` exists (frontend)

### Database Issues

- **PostgreSQL**: Make sure the service is running
- **MySQL**: Check if MySQL server is active
- **SQLite**: No setup required, file will be created automatically

## Next Steps

1. Explore the API endpoints at `http://localhost:5000/api/`
2. Test the frontend features (add, edit, delete jobs)
3. Run the web scraper to get real job data
4. Customize the styling and functionality

## Support

If you encounter issues:
1. Check the console for error messages
2. Verify all dependencies are installed
3. Ensure database is accessible
4. Check that both backend and frontend are running

Happy coding!
