# Architecture Notes

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (React App)                       │
│                    Port: localhost:5173                       │
│  ┌──────────────┬──────────────┬──────────────────────────┐  │
│  │ Auth Layer   │ API Client   │ State Management         │  │
│  │ (JWT Token)  │ (Axios)      │ (React Query)            │  │
│  └──────────────┴──────────────┴──────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ Pages: Login, Dashboard, Editor                          │ │
│  │ Components: Navbar, Sidebar, Editor, Modal, Toast        │ │
│  │ Hooks: useAuth, useDocuments, useDocument, etc.          │ │
│  └──────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/REST (CORS enabled)
┌──────────────────────────┴──────────────────────────────────┐
│              Django REST API (port 8000)                     │
│                 http://localhost:8000/api                     │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ Routes:                                                  ││
│  │ /auth/login                                              ││
│  │ /documents (CRUD + share + import)                      ││
│  └──────────────────────────────────────────────────────────┘│
│  ┌──────────────────────────────────────────────────────────┐│
│  │ Middleware:                                              ││
│  │ - CORS (allows localhost:5173)                          ││
│  │ - JWT Authentication                                     ││
│  │ - Error Handling                                         ││
│  └──────────────────────────────────────────────────────────┘│
│  ┌──────────────────────────────────────────────────────────┐│
│  │ Function-Based Views (FBV) with @api_view decorator     ││
│  │ - @api_view(['GET', 'POST'])                             ││
│  │ - @permission_classes([IsAuthenticated])                 ││
│  │ - Proper status codes                                    ││
│  │ - Error validation                                       ││
│  └──────────────────────────────────────────────────────────┘│
│  ┌──────────────────────────────────────────────────────────┐│
│  │ Service Layer:                                           ││
│  │ - FileImportService (text → Tiptap conversion)          ││
│  │ - DocumentService (utility functions)                    ││
│  └──────────────────────────────────────────────────────────┘│
│  ┌──────────────────────────────────────────────────────────┐│
│  │ Serializers:                                             ││
│  │ - UserSerializer                                         ││
│  │ - DocumentSerializer (with shared_with field)           ││
│  │ - DocumentShareSerializer                                ││
│  └──────────────────────────────────────────────────────────┘│
└──────────────────────────┬──────────────────────────────────┘
                           │ ORM
┌──────────────────────────┴──────────────────────────────────┐
│           SQLite Database (db.sqlite3)                       │
│  ┌────────────┬────────────┬────────────────────────────────┐│
│  │ auth_user  │ documents_ │ documents_                     ││
│  │            │ document   │ documentshare                  ││
│  └────────────┴────────────┴────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘
```

## Frontend Architecture

### Authentication Flow
1. User enters credentials on LoginPage
2. `authAPI.login()` sends POST to `/api/auth/login/`
3. Server returns JWT tokens + user data
4. `AuthContext.login()` stores tokens and user in localStorage
5. API client interceptor adds `Authorization: Bearer {token}` to all requests
6. `ProtectedRoute` component checks `AuthContext.isAuthenticated`

### State Management
- **localStorage**: Stores JWT tokens and user info
- **React Query**: Caches API responses and manages side effects
- **React Context**: Global auth state across app
- **Component State**: Local UI state (modals, inputs, etc.)

### Data Flow (Document Editor)
1. User navigates to `/documents/{id}`
2. `EditorPage` calls `useDocument(id)` hook
3. React Query fetches document from API (or cache)
4. Content displayed in Tiptap editor
5. User edits → `handleContentChange` updates state
6. Auto-save timer triggers after 30 seconds
7. `updateDocument` mutation sends PUT request
8. Success → toast notification + `lastSaved` update

### Component Hierarchy
```
App
├── AuthProvider (provides AuthContext)
├── QueryClientProvider (provides React Query)
└── BrowserRouter
    └── Routes
        ├── /login → LoginPage
        ├── /dashboard → ProtectedRoute → Layout → DashboardPage
        └── /documents/:id → ProtectedRoute → Layout → EditorPage
```

## Backend Architecture

### Authentication
- JWT tokens issued via `/api/auth/login/`
- Tokens validated via `JWTAuthentication` class
- `@permission_classes([IsAuthenticated])` protects endpoints
- Tokens expire: access (1 hour), refresh (7 days)

### Authorization
- Document endpoints check: `document.owner == request.user`
- Sharing endpoints check: user is owner before sharing
- Read access for: document owner or shared_with users

### API View Structure
```python
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def document_list(request):
    if request.method == 'GET':
        # List documents
    elif request.method == 'POST':
        # Create document
```

### Database Relations
```
User (1) ──→ (n) Document (owns)
       ↓
       └──→ (n) DocumentShare

Document (1) ──→ (n) DocumentShare
         ↓
         └──→ (1) User (shared_with)
```

### Error Handling
- 400: Bad Request (validation errors)
- 401: Unauthorized (invalid token)
- 403: Forbidden (permission denied)
- 404: Not Found
- 201: Created (for POST)
- 204: No Content (for DELETE)

## Content Format: Tiptap JSON

Documents store content as JSON matching Tiptap's schema:

```json
{
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "marks": [{"type": "bold"}],
          "text": "Bold text"
        }
      ]
    },
    {
      "type": "heading",
      "attrs": {"level": 2},
      "content": [{"type": "text", "text": "Heading"}]
    },
    {
      "type": "bulletList",
      "content": [
        {"type": "listItem", "content": [{"type": "paragraph"}]}
      ]
    }
  ]
}
```

## API Client Pattern

```typescript
// 1. Define in API module
export const documentsAPI = {
  get: async (id: number) => {
    const response = await apiClient.get(`/documents/${id}/`);
    return response.data;
  }
};

// 2. Use in custom hook
export const useDocument = (id: number) => {
  return useQuery({
    queryKey: ['document', id],
    queryFn: () => documentsAPI.get(id),
  });
};

// 3. Use in component
const { data: document } = useDocument(docId);
```

## Performance Optimizations

### Frontend
- React Query deduplicates identical requests
- Memoized selectors prevent unnecessary re-renders
- Lazy loading of editor components
- Virtual scrolling for large lists (future enhancement)

### Backend
- Single query per endpoint (no N+1)
- Indexed foreign keys for fast lookups
- Pagination ready (built into DRF)

### Caching
- React Query: 5-minute default stale time
- Browser cache: JWT tokens in localStorage
- Server cache: Django's cache framework ready

## Type Safety

### TypeScript Interfaces
```typescript
interface Document {
  id: number;
  title: string;
  content: Record<string, any>;
  owner: number;
  created_at: string;
  updated_at: string;
  shared_with: Array<{ id: number; email: string; username: string }>;
}
```

### Django Serializers
```python
class DocumentSerializer(serializers.ModelSerializer):
    owner_email = serializers.CharField(source='owner.email', read_only=True)
    shared_with = serializers.SerializerMethodField()
```

## Testing Strategy

### Unit Tests
- Document CRUD operations
- Permission checks
- Serializer validation

### Integration Tests
- Full login → create → share → delete flow
- File import conversion

### E2E Tests (future)
- User journey from login to document editing
- Sharing and collaboration

## Deployment Checklist

- [ ] Set `DEBUG = False` in Django settings
- [ ] Configure `SECRET_KEY` via environment variable
- [ ] Set `ALLOWED_HOSTS` for production domain
- [ ] Enable HTTPS
- [ ] Configure CORS for production domain
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up static files serving
- [ ] Configure logging and error tracking
- [ ] Set up database backups
- [ ] Enable rate limiting on API

## Scaling Considerations

### Horizontal Scaling
- Stateless backend (JWT doesn't require sessions)
- Database can use read replicas
- Frontend can be served from CDN

### Vertical Scaling
- Database indexing on frequently queried fields
- Pagination for large datasets
- Document versioning (future feature)

### Real-time Collaboration (Future)
- WebSocket connection for live editing
- Operational transformation for conflict resolution
- Server-sent events for document changes
