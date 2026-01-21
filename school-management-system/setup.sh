#!/bin/bash

# School Management System - Setup Script

echo "🎓 School Management System - Installation Script"
echo "=================================================="

# Check Python version
echo "✓ Checking Python version..."
python --version

# Check Node version
echo "✓ Checking Node.js version..."
node --version
npm --version

# Backend Setup
echo ""
echo "📦 Setting up Backend..."
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
read -p "Create superuser now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

echo "✓ Backend setup complete!"
echo "  Run: cd backend && source venv/bin/activate && python manage.py runserver"

# Frontend Setup
echo ""
echo "🎨 Setting up Frontend..."
cd ../frontend

# Install dependencies
npm install

echo "✓ Frontend setup complete!"
echo "  Run: cd frontend && npm start"

echo ""
echo "=================================================="
echo "✅ Installation Complete!"
echo ""
echo "Next steps:"
echo "1. Backend:  cd backend && source venv/bin/activate && python manage.py runserver"
echo "2. Frontend: cd frontend && npm start"
echo "3. Visit:    http://localhost:3000"
echo "4. Admin:    http://localhost:8000/admin"
echo "5. API:      http://localhost:8000/api"
echo ""
