# DocEdit - Collaborative Document Editor

A production-ready MVP inspired by Google Docs, built with Django REST Framework and React.

## Features

- ✅ User Authentication (JWT)
- ✅ Create, Read, Update, Delete Documents
- ✅ Rich Text Editing (Tiptap)
- ✅ Auto-save with Status Indicator
- ✅ Document Sharing
- ✅ File Import (.txt, .md)
- ✅ Responsive UI
- ✅ Toast Notifications

## Tech Stack

### Backend
- Django 4.2
- Django REST Framework
- SimpleJWT Authentication
- SQLite Database

### Frontend
- React 18
- TypeScript
- Vite
- TailwindCSS
- Tiptap Editor
- React Query
- Axios

## Quick Start

### Backend Setup

```bash
cd backend

# Activate virtual environment
../venv/Scripts/activate  # Windows
source ../venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed test users
python manage.py seed_users

# Start server
python manage.py runserver
```

Backend will run on `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on `http://localhost:5173`

## Test Credentials

### Owner Account
- Email: `owner@test.com`
- Password: `Password123`

### Collaborator Account
- Email: `collaborator@test.com`
- Password: `Password123`

## API Endpoints

### Authentication
- `POST /api/auth/login/` - Login with email and password

### Documents
- `GET /api/documents/` - Get all documents (owned and shared)
- `POST /api/documents/` - Create new document
- `GET /api/documents/{id}/` - Get specific document
- `PUT /api/documents/{id}/` - Update document
- `DELETE /api/documents/{id}/` - Delete document
- `POST /api/documents/{id}/share/` - Share document with user
- `POST /api/documents/import/` - Import .txt or .md file

## Project Structure

```
pdf-editior/
├── backend/
│   ├── auth_app/
│   │   ├── views.py
│   │   └── urls.py
│   ├── documents/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   ├── tests.py
│   │   └── management/
│   │       └── commands/
│   │           └── seed_users.py
│   ├── config/
│   │   ├── settings.py
│   │   └── urls.py
│   └── manage.py
│
└── frontend/
    ├── src/
    │   ├── api/
    │   │   ├── client.ts
    │   │   ├── auth.ts
    │   │   └── documents.ts
    │   ├── components/
    │   │   ├── layout/
    │   │   ├── editor/
    │   │   ├── shared/
    │   │   └── modals/
    │   ├── pages/
    │   │   ├── LoginPage.tsx
    │   │   ├── DashboardPage.tsx
    │   │   └── EditorPage.tsx
    │   ├── hooks/
    │   │   ├── useAuth.ts
    │   │   └── useDocuments.ts
    │   ├── context/
    │   │   └── AuthContext.tsx
    │   ├── types/
    │   │   └── index.ts
    │   ├── utils/
    │   │   └── helpers.ts
    │   └── App.tsx
    └── package.json
```

## Testing

### Run Backend Tests

```bash
cd backend
python manage.py test documents.tests.DocumentCreationTest -v 2
```

Tests cover:
- User login
- Document creation
- Document retrieval
- Document updates
- Document listing
- Document deletion

## Key Features Explained

### Auto-save
Documents auto-save every 30 seconds when there are unsaved changes. The UI shows a "Unsaved changes" indicator.

### Document Sharing
- Owner can share documents by email
- Shared users can view and edit documents
- Prevents duplicate shares and self-sharing

### File Import
- Supports .txt, .md, and .docx files
- Automatically converts to Tiptap JSON format
- Shows validation errors for unsupported files

### Rich Text Editor
- Bold, Italic, Underline
- Headings (H1, H2, H3)
- Bullet lists and numbered lists
- Content stored as JSON

## Database Schema

### User
- id (Integer, Primary Key)
- username (String, Unique)
- email (String)
- password (String, hashed)

### Document
- id (Integer, Primary Key)
- title (String)
- content (JSON)
- owner (ForeignKey → User)
- created_at (DateTime)
- updated_at (DateTime)

### DocumentShare
- id (Integer, Primary Key)
- document (ForeignKey → Document)
- shared_with (ForeignKey → User)
- created_at (DateTime)
- Unique: (document, shared_with)

## Error Handling

- Proper HTTP status codes
- User-friendly error messages
- Toast notifications for feedback
- Unauthorized access protection
- Validation errors

## Performance Optimizations

- React Query for caching and deduplication
- Lazy loading of documents
- Optimized re-renders
- Debounced auto-save
- JWT token caching

## Production Considerations

For production deployment:

1. **Django Settings**
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use environment variables for secrets

2. **Frontend**
   - Build: `npm run build`
   - Serve built files from static server

3. **Database**
   - Use PostgreSQL instead of SQLite
   - Run migrations on deployment

4. **Security**
   - Enable HTTPS
   - Configure CORS properly
   - Use secure cookies
   - Implement rate limiting

## Development Notes

- Components are built with composition in mind
- Services handle business logic
- API client layer abstracts HTTP details
- Context provides app-wide state
- Custom hooks encapsulate complex logic

## Architecture & Prioritization Note

### What Was Prioritized and Why

In building this lightweight collaborative editor within a constrained timebox, the architectural focus was placed heavily on **shipping a robust, usable, single-player editing experience with asynchronous collaboration** rather than attempting to build a brittle real-time WebSockets synchronization engine. 

1.  **Persistence over Real-time:** Real-time sync (e.g., via WebSockets and Yjs) introduces significant complexity regarding conflict resolution, offline states, and backend infrastructure (Redis, Daphne, Channels). Given the constraints, I prioritized a highly reliable Auto-Save REST integration (saving every 5 seconds) against a standard SQLite/Django backend. This guarantees data persistence, allows users to pick up exactly where they left off after a refresh, and cleanly handles concurrent last-write-wins without infrastructure overhead.
2.  **Extensible Editor Foundation:** Tiptap was chosen over Slate or Quill because it natively stores data as structured JSON (rather than HTML or complex deltas), making it inherently ready for future real-time CRDT (Conflict-free Replicated Data Type) upgrades. It also provides headless rendering, allowing for the precise "Deep Work" UI styling requested.
3.  **UI/UX Fidelity:** Significant time was invested in the visual layout, floating toolbar, and visual feedback (e.g., "Saved", "Saving" indicators, Share Modal, "Owned" vs "Shared" badges). A collaborative tool lives or dies by its UX; users need explicit visual cues regarding their document state and permissions.
4.  **Security and Access Control:** The backend handles document authorization securely. The `share_document` endpoints, `DocumentShare` models, and view filtering guarantee that users can only see and modify documents they own or have been explicitly granted access to.

## Deployment Notes

Reviewers can access the local deployment by following the Quick Start guide. For a production deployment, the architecture is designed to map cleanly to a standard PaaS provider (e.g., Heroku, Render, AWS App Runner):
- **Frontend:** Built via Vite (`npm run build`) and served statically via Vercel or Netlify.
- **Backend:** Gunicorn serving the Django WSGI application, connected to a managed PostgreSQL instance.
- **Media/Static:** Django's WhiteNoise middleware handles static files efficiently for a lightweight PaaS footprint without needing S3 immediately.

## Common Issues

**CORS Errors**: Ensure Django CORS middleware is installed and configured correctly.

**Token Expiration**: Frontend automatically logs out on 401 responses.

**Unsaved Changes**: Check network tab for save requests in browser dev tools.

## License

MIT
