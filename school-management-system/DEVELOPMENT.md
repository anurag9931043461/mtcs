# School Management System - Development Guide

## Getting Started with Development

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn
- Git

### Quick Start

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## Database Schema Overview

### Key Design Decisions

1. **UUID Primary Keys**: All models use UUID instead of auto-incrementing integers for enhanced security and better distributed system support.

2. **Soft Delete Pattern**: (Optional) Consider adding soft deletes for audit compliance.

3. **Historical Records**: Audit logs capture all changes for compliance.

### Model Relationships

```
User (1) ──→ Student (1)
User (1) ──→ Parent (1)
User (1) ──→ Staff (1)

Student (M) ──→ Class (1)
Student (M) ──→ Parent (M) [through StudentParent]

Class (1) ──→ Subject (M) [through ClassSubject]
Class (1) ──→ Teacher [User]

AttendanceRecord (M) ──→ Student (1)
Mark (M) ──→ Student (1)
Mark (M) ──→ ExamSchedule (1)

FeePayment (M) ──→ Student (1)
FeePayment (M) ──→ FeeStructure (1)

TransportRoute (1) ──→ Student (M) [through StudentTransport]
Vehicle (M) ──→ TransportRoute (1)
Driver (1) ──→ User (1)
```

## API Implementation Guide

### ViewSet Pattern

Each model has a ViewSet that provides:
- List (GET /resource/)
- Create (POST /resource/)
- Retrieve (GET /resource/{id}/)
- Update (PUT /resource/{id}/)
- Partial Update (PATCH /resource/{id}/)
- Delete (DELETE /resource/{id}/)

### Custom Actions

Custom actions are implemented using `@action` decorator:
```python
@action(detail=False, methods=['get'])
def bulk_mark(self, request):
    # Custom logic
    return Response(data)
```

### Filtering and Search

All ViewSets support:
- Filter by fields: `?field=value`
- Search: `?search=query`
- Ordering: `?ordering=-created_at`
- Pagination: `?page=1`

## Frontend Component Structure

### Core Components
- `UI.js`: Reusable UI components (Button, Input, Card, etc.)
- `Layout.js`: Navigation and sidebar layouts

### Pages
- `LoginPage.js`: Authentication
- `Dashboard.js`: Main dashboard
- `StudentsList.js`: Student management (template)

### Services
- `api.js`: Centralized API client with Axios

### Context
- `AuthContext.js`: Authentication state management

## Common Development Tasks

### Adding a New Model

1. Create model in `backend/school_management/core/models.py`
2. Register in `backend/school_management/core/admin.py`
3. Create serializer in `backend/school_management/api/serializers.py`
4. Create ViewSet in `backend/school_management/api/views.py`
5. Register in `backend/school_management/api/urls.py`
6. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Adding a New Page

1. Create component in `frontend/src/pages/`
2. Import and add route in `frontend/src/App.js`
3. Add menu item in `frontend/src/components/Layout.js` (Sidebar)

### Styling

The project uses Tailwind CSS. Add classes directly to elements:
```jsx
<div className="bg-blue-600 text-white p-4 rounded-lg">
  Content
</div>
```

## Testing

### Backend Testing
```bash
python manage.py test
```

### Frontend Testing
```bash
npm test
```

## Best Practices

### Backend
1. Use DRY principle - avoid code duplication
2. Validate data at serializer level
3. Use select_related() and prefetch_related() for performance
4. Document API responses
5. Use pagination for large datasets
6. Implement proper error handling

### Frontend
1. Use hooks for state management
2. Memoize expensive computations
3. Implement proper loading and error states
4. Use semantic HTML
5. Follow accessibility guidelines (WCAG)

## Debugging

### Backend
```bash
# Enable debug toolbar
pip install django-debug-toolbar

# In settings.py
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

### Frontend
- Use React DevTools browser extension
- Console logs and debugger statements
- Network tab for API debugging

## Performance Optimization

### Database
- Add indexes on frequently queried fields
- Use database query optimization
- Implement caching strategies

### API
- Implement field selection
- Pagination
- Result limiting
- Response compression

### Frontend
- Code splitting with React.lazy()
- Image optimization
- Memoization of components
- Lazy loading

## Deployment

### Backend Deployment
```bash
# Using Gunicorn
pip install gunicorn
gunicorn school_management.wsgi:application --bind 0.0.0.0:8000

# Using Docker
docker build -t school-ms-backend .
docker run -p 8000:8000 school-ms-backend
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Serve with production server
npm install -g serve
serve -s build
```

## Troubleshooting

### Common Issues

**CORS Errors**
- Check CORS_ALLOWED_ORIGINS in settings.py
- Ensure frontend and backend URLs match

**Database Migration Issues**
```bash
python manage.py showmigrations
python manage.py migrate [app_name] [migration_name]
```

**API Not Returning Data**
- Check serializer fields
- Verify query parameters
- Check authentication token
- Review database constraints

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Axios Documentation](https://axios-http.com/)

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Create a pull request with clear description

## Version History

- **v0.1.0** - Initial release with core models and API
