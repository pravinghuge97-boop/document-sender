# Walkthrough Video Script

## Video Overview
- **Duration**: 3-5 minutes
- **Format**: Screen recording with voice narration
- **Platform**: Loom.com (https://www.loom.com)
- **Audience**: Hiring team evaluating product judgment and execution

## Setup
1. Open browser to http://localhost:5174 (or production URL)
2. Have console/terminal visible for showing commands
3. Test both login accounts work before recording
4. Record at 1080p with clear audio

## Scene-by-Scene Breakdown

### Scene 1: Project Overview (0:00-0:20)
**Objective**: Introduce the product and scope

**Script**:
> "This is DocEdit, a lightweight collaborative document editor inspired by Google Docs. Built with Django, React, and SQLite, it focuses on the core document editing, sharing, and file import workflows while intentionally deprioritizing real-time collaboration and complex features."

**Action**:
- Show README.md
- Show ARCHITECTURE.md diagram
- Briefly mention what was intentionally excluded

---

### Scene 2: Login & Authentication (0:20-0:40)
**Objective**: Demonstrate authentication flow

**Script**:
> "Starting with the login page. We have two seeded test accounts: an owner and a collaborator. The authentication uses JWT tokens stored in localStorage. Let me login as the owner."

**Action**:
- Click login page
- Type: `owner@test.com`
- Type password: `Password123`
- Click login
- Show dashboard loading with user's documents

---

### Scene 3: Dashboard Overview (0:40-1:00)
**Objective**: Show document management

**Script**:
> "Here's the dashboard. I can see my documents on the left sidebar. The dashboard is divided into 'My Documents' and 'Shared With Me' sections, making it clear what I own versus what I've been granted access to. Let me create a new document."

**Action**:
- Point to sidebar
- Click "New Document" button
- Show new document modal with title input

---

### Scene 4: Document Creation & Rich Text Editing (1:00-2:00)
**Objective**: Demonstrate editing and formatting

**Script**:
> "I'll create a document called 'Product Roadmap'. The editor is built with Tiptap, providing a familiar rich text editing experience with a formatting toolbar."

**Action**:
- Enter title "Product Roadmap"
- Click create
- Show editor interface
- Type some content: "Q3 2024 Roadmap"
- Demonstrate formatting:
  - Select text and click **Bold** button
  - Type more: "Key Initiatives"
  - Click *Italic* button
- Use keyboard shortcuts:
  - Ctrl+B for bold
  - Ctrl+I for italic
  - Ctrl+U for underline
- Show heading dropdown:
  - Select "Heading 1"
  - Type "H1 Title"
- Create bulleted list:
  - Click bullet list button
  - Type: "Item 1"
  - Press Enter, add "Item 2"
- Show numbered list:
  - Click numbered list button
  - Add numbered items

**Narration**:
> "You can see the formatting toolbar with all the essentials: bold, italic, underline, headings, bullet points, numbered lists, and more. The content is stored as JSON, so formatting is perfectly preserved even after refresh."

---

### Scene 5: Auto-save Functionality (2:00-2:20)
**Objective**: Show persistence and auto-save

**Script**:
> "Notice the 'Unsaved changes' indicator in the top right. The document auto-saves every 30 seconds. Let me make some changes and wait for it to save automatically."

**Action**:
- Make an edit
- Point to "Unsaved changes" status
- Wait 30+ seconds
- Show "Last saved: just now" status
- Refresh the page (F5)
- Show document content is still there
- Point out that formatting was preserved

---

### Scene 6: File Import (2:20-2:50)
**Objective**: Demonstrate file upload

**Script**:
> "The app supports importing .txt and .md files. Let me create a markdown file and import it. I've already prepared a sample file with markdown formatting."

**Action**:
- Click "Import File" button (or show in sidebar)
- Select a .md file with content like:
  ```markdown
  # Meeting Notes
  Date: June 23, 2024
  
  ## Topics Discussed
  - Feature planning
  - Performance improvements
  - User feedback
  
  ## Action Items
  1. Complete Q3 roadmap
  2. Performance optimization
  3. Beta testing
  ```
- Show the import dialog accepts the file
- Show converted document in editor
- Point out:
  - Heading structure preserved
  - Bullet lists converted to Tiptap format
  - Numbered lists preserved
  - Title auto-populated from filename

---

### Scene 7: Document Sharing (2:50-3:30)
**Objective**: Demonstrate sharing workflow

**Script**:
> "One of the key features is document sharing. Let me share this document with the collaborator. I'll click the Share button, enter their email, and grant access."

**Action**:
- Click "Share" button
- Show share modal
- Type: `collaborator@test.com`
- Click "Share"
- Show success message: "Document shared successfully"
- Show shared user in list: "collaborator@test.com"
- Logout (show "Logout" button)

**Continue narration**:
> "Now let me login as the collaborator to show the shared access. Notice I'm using a different browser context."

**Action**:
- Open new incognito/private browser window
- Navigate to http://localhost:5174
- Login with:
  - Email: `collaborator@test.com`
  - Password: `Password123`
- Show dashboard with "Shared With Me" section
- Point to the "Product Roadmap" document
- Click to open it
- Demonstrate that collaborator can edit:
  - Add a comment/edit to the document
  - Show auto-save
  - Log back into owner account
  - Refresh
  - Show the collaborator's changes are visible

---

### Scene 8: Implementation Highlights (3:30-4:00)
**Objective**: Explain key technical decisions

**Script**:
> "Let me highlight some of the implementation decisions. The backend is Django with Django REST Framework, providing a clean REST API. The frontend is React with TypeScript for type safety. We use Tiptap for rich text editing with JSON serialization, ensuring formatting persists perfectly."

**Action**:
- Show backend structure briefly
  - Models for User, Document, DocumentShare
  - Views for CRUD operations
  - Services for file import logic
- Show frontend structure
  - Components organized by feature
  - API client layer with Axios
  - React Query for server state management
- Show tests passing:
  ```bash
  python manage.py test documents.tests -v 2
  ```

---

### Scene 9: What Was Intentionally Deprioritized (4:00-4:20)
**Objective**: Demonstrate product judgment

**Script**:
> "In the interest of shipping a focused MVP, I intentionally excluded several features: Real-time collaboration would require WebSockets and operational complexity. Comments and suggestions add complexity without core value in V1. Version history and export features are useful but not essential for basic document editing and sharing. I chose to focus depth on the core workflows rather than breadth across many features."

**Action**:
- Show ARCHITECTURE.md section on "Intentional Scope Cuts"
- Discuss tradeoffs
- Mention these could be built in future iterations

---

### Scene 10: Deployment & Production Ready (4:20-4:50)
**Objective**: Show production readiness

**Script**:
> "The app is production-ready and deployed on Render. The deployment includes PostgreSQL for production data, environment-based configuration, and proper security headers. I've documented the deployment process, making it easy for others to extend this project."

**Action**:
- Show live deployment URL
- Show render.yaml configuration
- Show DEPLOYMENT.md
- Mention CI/CD pipeline configured
- Show environment variables configured

---

### Scene 11: Code Quality & Testing (4:50-5:00)
**Objective**: Demonstrate engineering quality

**Script**:
> "The codebase demonstrates solid engineering practices: automated tests covering core workflows, clear separation of concerns between frontend and backend, type safety with TypeScript, and comprehensive documentation."

**Action**:
- Show test coverage:
  - test_document_creation_flow passing
  - All tests covering login, create, read, update, delete
- Quick code review:
  - Show API serializers
  - Show React components
  - Highlight clean, readable code
- Show documentation:
  - README.md
  - ARCHITECTURE.md
  - AI_WORKFLOW.md

---

### Final Scene: Summary & Call to Action (5:00-end)
**Objective**: Close with key takeaways

**Script**:
> "To summarize, DocEdit demonstrates:
> - Solid product judgment with intentional scope cuts
> - Full-stack execution across backend, frontend, database, and deployment
> - A polished user experience for document editing and sharing
> - Production-ready code with tests and documentation
> - Practical use of AI tools to accelerate development while maintaining quality
> 
> The app is ready to use. Try it, create documents, share them, and let me know if you have questions!"

**Action**:
- Show both servers running in terminal
- Show live product URL
- Show GitHub repository
- Show all documentation files

---

## Recording Tips

### Audio
- Use headphones to hear system audio
- Speak clearly and at a moderate pace
- Add pauses between major sections
- Don't rush - take time to explain decisions

### Screen Recording
- Maximize browser window for visibility
- Use 1080p or higher resolution
- Keep mouse movements smooth
- Use keyboard shortcuts to show UI flow
- Include both happy path and some edge cases

### Editing (if using Loom)
- Trim intro/outro silence
- Add captions for accessibility
- Highlight important moments
- Use Loom's built-in tools for emphasis

## Upload Instructions

1. Record on Loom.com (https://www.loom.com)
2. Set to "Unlisted" (not public)
3. Get the shareable link
4. Add link to submission folder
5. Add link to this repository's README

## Timing Checklist

- [ ] 0:00-0:20 - Project Overview (20s)
- [ ] 0:20-0:40 - Login (20s)
- [ ] 0:40-1:00 - Dashboard (20s)
- [ ] 1:00-2:00 - Rich Text Editing (60s)
- [ ] 2:00-2:20 - Auto-save (20s)
- [ ] 2:20-2:50 - File Import (30s)
- [ ] 2:50-3:30 - Sharing (40s)
- [ ] 3:30-4:00 - Technical Highlights (30s)
- [ ] 4:00-4:20 - Deprioritized Features (20s)
- [ ] 4:20-4:50 - Deployment (30s)
- [ ] 4:50-5:00 - Code Quality (10s)
- [ ] 5:00+ - Summary (10s+)

**Total target: 3-5 minutes**

## Script Variations

### If running locally (for technical review):
- Show backend logs
- Show database queries
- Show network requests in DevTools
- Demonstrate loading states

### If showing deployment (for production review):
- Show live URL
- Show deployment logs
- Show monitoring dashboard
- Mention uptime and performance

### If emphasizing AI workflow:
- Show before/after code generated
- Explain how AI accelerated development
- Demonstrate verification process
- Discuss tradeoffs made

---

**Ready to record?** Grab coffee ☕ and let's go! 🎬
