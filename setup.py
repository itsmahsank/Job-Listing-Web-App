#!/usr/bin/env python3
"""
Setup Script for Job Listing Web App
This script helps you set up the project for the first time
"""

import os
import sys
import subprocess
import platform

def print_header():
    """Print a nice header for the setup script"""
    print("=" * 60)
    print("Job Listing Web App - Setup Script")
    print("=" * 60)
    print("This script will help you set up the project step by step")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("Python 3.8 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_nodejs():
    """Check if Node.js is installed"""
    print("\nChecking Node.js...")
    
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Node.js version: {result.stdout.strip()}")
            return True
        else:
            print("Node.js not found or not working")
            return False
    except FileNotFoundError:
        print("Node.js not installed")
        print("   Please install Node.js from: https://nodejs.org/")
        return False

def check_npm():
    """Check if npm is installed"""
    print("\nChecking npm...")
    
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"npm version: {result.stdout.strip()}")
            return True
        else:
            print("npm not found or not working")
            return False
    except FileNotFoundError:
        print("npm not installed")
        print("   Please install npm (usually comes with Node.js)")
        return False

def setup_backend():
    """Set up the Python backend"""
    print("\nSetting up Python backend...")
    
    backend_dir = "backend"
    if not os.path.exists(backend_dir):
        print("Backend directory not found!")
        return False
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Check if virtual environment exists
    venv_dir = "venv"
    if os.path.exists(venv_dir):
        print("Virtual environment already exists")
    else:
        print("Creating virtual environment...")
        try:
            subprocess.run([sys.executable, '-m', 'venv', venv_dir], check=True)
            print("Virtual environment created!")
        except subprocess.CalledProcessError:
            print("Failed to create virtual environment")
            return False
    
    # Activate virtual environment and install requirements
    if platform.system() == "Windows":
        activate_script = os.path.join(venv_dir, "Scripts", "activate")
        pip_path = os.path.join(venv_dir, "Scripts", "pip")
    else:
        activate_script = os.path.join(venv_dir, "bin", "activate")
        pip_path = os.path.join(venv_dir, "bin", "pip")
    
    print("Installing Python packages...")
    try:
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("Python packages installed!")
    except subprocess.CalledProcessError:
        print("Failed to install Python packages")
        return False
    
    # Go back to root directory
    os.chdir("..")
    return True

def setup_frontend():
    """Set up the React frontend"""
    print("\nSetting up React frontend...")
    
    frontend_dir = "frontend"
    if not os.path.exists(frontend_dir):
        print("Frontend directory not found!")
        return False
    
    # Change to frontend directory
    os.chdir(frontend_dir)
    
    print("Installing Node.js packages...")
    try:
        subprocess.run(['npm', 'install'], check=True)
        print("Node.js packages installed!")
    except subprocess.CalledProcessError:
        print("Failed to install Node.js packages")
        return False
    
    # Go back to root directory
    os.chdir("..")
    return True

def create_env_file():
    """Create a sample .env file"""
    print("\nCreating environment file...")
    
    env_file = "backend/.env"
    if os.path.exists(env_file):
        print(".env file already exists")
        return True
    
    # Sample .env content
    env_content = """# Database Configuration
# Replace this with your actual database connection string
DATABASE_URL=postgresql://username:password@localhost/jobdb

# Or use SQLite for development (easier to set up)
# DATABASE_URL=sqlite:///jobs.db

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here-change-this-in-production
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(".env file created!")
        print("Please edit backend/.env with your actual database settings")
    except Exception as e:
        print(f"Failed to create .env file: {e}")
        return False
    
    return True

def print_next_steps():
    """Print instructions for next steps"""
    print("\n" + "=" * 60)
    print("Setup Complete! Here's what to do next:")
    print("=" * 60)
    print("1. Edit backend/.env file with your database settings")
    print("2. Make sure your database is running")
    print("3. Start the backend: cd backend && python app.py")
    print("4. Start the frontend: cd frontend && npm start")
    print("5. Add sample data: cd backend && python sample_data.py")
    print("=" * 60)
    print("For more help, check the README.md file")
    print("=" * 60)

def main():
    """Main setup function"""
    print_header()
    
    # Check prerequisites
    if not check_python_version():
        return 1
    
    if not check_nodejs():
        return 1
    
    if not check_npm():
        return 1
    
    # Set up backend
    if not setup_backend():
        print("Backend setup failed!")
        return 1
    
    # Set up frontend
    if not setup_frontend():
        print("Frontend setup failed!")
        return 1
    
    # Create environment file
    if not create_env_file():
        print("Environment file creation failed!")
        return 1
    
    # Print next steps
    print_next_steps()
    
    return 0

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
