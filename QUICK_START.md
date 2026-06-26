# Quick Start Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- npm

## Installation & Running

### Option 1: Manual Start (2 terminals)

#### Terminal 1 - Backend
```bash
cd backend

# Activate virtual environment (Windows)
..\venv\Scripts\activate
# macOS/Linux
source ../venv/bin/activate

# Run server
python manage.py runserver
# Backend: http://localhost:8000
```

#### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
# Frontend: http://localhost:5173
```

### Option 2: One-time Setup
```bash
# Install backend dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies
cd frontend && npm install && cd ..

# Setup database
cd backend
python manage.py migrate
python manage.py seed_users
cd ..

# Start both servers (in separate terminals as above)
```

## Access the App

1. Open browser: http://localhost:5173
2. Login with credentials:
   - Email: `owner@test.com`
   - Password: `Password123`

## Features Quick Demo

### 1. Create Document
- Click "New Document" in sidebar
- Enter document title
- Start typing in editor

### 2. Edit Document
- Use formatting toolbar (Bold, Italic, etc.)
- Create headings, lists
- Changes auto-save every 30 seconds

### 3. Share Document
- Click "Share" button
- Enter collaborator's email
- Collaborator can now view and edit

### 4. Import Document
- Click "Import File" in sidebar
- Select .txt or .md file
- Document created with file content

### 5. Switch Users
- Click "Logout"
- Login with: `collaborator@test.com` / `Password123`
- See shared documents in "My Documents"

## Test Scenarios

### Scenario 1: Basic CRUD
1. Login as owner
2. Create "Meeting Notes"
3. Add content with formatting
4. Go to dashboard
5. Delete the document

### Scenario 2: Sharing
1. Login as owner
2. Create "Project Plan"
3. Click Share → Enter collaborator@test.com
4. Open another browser (or incognito)
5. Login as collaborator
6. See document in "Shared With Me"
7. Edit and verify changes

### Scenario 3: File Import
1. Create test.txt with content
2. Go to app → Click "Import File"
3. Select test.txt
4. Verify content in editor

## Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process using port
taskkill /PID <PID> /F

# Clear migrations and restart
python manage.py migrate
```

### Frontend won't start
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Try different port
npm run dev -- --port 3000
```

### Seed users not created
```bash
cd backend
python manage.py seed_users
```

### CORS errors
- Ensure backend is running on port 8000
- Check Django CORS settings in config/settings.py
- Frontend must be on localhost:5173

### Can't login
- Verify seed users exist: `python manage.py seed_users`
- Check credentials: owner@test.com / Password123
- Clear localStorage: F12 → Application → Storage → Clear All

## Database

View database using Django admin:
```bash
cd backend
python manage.py createsuperuser
python manage.py runserver
# Go to http://localhost:8000/admin
# Login with superuser credentials
```

## Testing

Run backend tests:
```bash
cd backend
python manage.py test documents.tests.DocumentCreationTest -v 2
```

Expected output:
```
test_document_creation_flow ... ok
Ran 1 test in 1.2s
OK
```

## Common Workflows

### Login → Create → Edit → Share
1. Open http://localhost:5173
2. Login (owner@test.com)
3. Click "New Document"
4. Type title "Shared Project"
5. Add content with **bold** and headings
6. Click "Share"
7. Type "collaborator@test.com"
8. Click "Share"
9. Open new browser, login as collaborator
10. See document in "Shared With Me"
11. Edit document
12. See changes auto-saved

### Import Markdown File
1. Create file: `test.md`
   ```markdown
   # Heading 1
   This is content
   - List item 1
   - List item 2
   ```
2. Login to app
3. Click "Import File"
4. Select test.md
5. Verify formatting preserved

### View Shared Documents
1. Login as owner
2. Create document "Collaboration"
3. Share with collaborator@test.com
4. Logout
5. Login as collaborator@test.com
6. Click sidebar "My Documents" (if not visible)
7. See "Collaboration" in Shared With Me section

## Performance Tips

- First load: May take 10-15s (Vite bundle)
- Auto-save: Every 30 seconds
- Queries: Optimized, no N+1
- Storage: About 1MB for demo data

## Need Help?

Check these files:
- `README.md` - Full documentation
- `ARCHITECTURE.md` - Technical details
- `AI_WORKFLOW.md` - Development process
- `PROJECT_SUMMARY.md` - Completion summary

## Next Steps

1. ✅ Start both servers
2. ✅ Login and explore
3. ✅ Create and share documents
4. ✅ Test all features
5. ✅ Read documentation
6. ✅ Review code structure

## Useful Commands

```bash
# Backend commands
python manage.py runserver          # Start server
python manage.py makemigrations     # Create migrations
python manage.py migrate            # Apply migrations
python manage.py seed_users         # Create test users
python manage.py createsuperuser    # Create admin user
python manage.py test               # Run tests

# Frontend commands
npm run dev                         # Start dev server
npm run build                       # Production build
npm run preview                     # Preview build
npm install <package>              # Install package
npm list                            # List installed packages
```

## Browser DevTools Tips

**Check Network Requests:**
- F12 → Network tab
- Create/edit/share document
- See API calls to backend

**Check Local Storage:**
- F12 → Application → Local Storage
- See stored JWT tokens and user data

**Check Redux (React Query):**
- Install React Query DevTools extension
- See cached data and query states

## Mobile Responsive

App works on mobile browsers:
- Sidebar collapses on small screens
- Touch-friendly buttons
- Responsive typography
- Works on tablets

Try on mobile: http://localhost:5173

---

Happy documenting! 🚀
