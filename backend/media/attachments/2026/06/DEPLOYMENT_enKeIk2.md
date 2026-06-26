# Deployment Guide

## Overview
DocEdit is ready to deploy to Render.com for free. This guide covers the deployment process.

## Prerequisites
- GitHub account with the repository pushed
- Render.com account (free tier)
- PostgreSQL database (included in Render free tier)

## Deployment Steps

### Option 1: Deploy with render.yaml (Recommended)

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Connect to Render**
   - Go to https://render.com
   - Sign in/Create account
   - Click "New +" → "Blue Stack"
   - Select the GitHub repository
   - Render will detect `render.yaml` automatically

3. **Configure Environment Variables**
   - `DEBUG`: `false`
   - `SECRET_KEY`: Auto-generated (leave as is or set custom)
   - `ALLOWED_HOSTS`: `.onrender.com`
   - `DATABASE_URL`: Auto-populated by PostgreSQL service

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete (~5-10 minutes)
   - Services will be available at:
     - Backend: `https://docedit-backend.onrender.com`
     - Frontend: `https://docedit-frontend.onrender.com`

### Option 2: Manual Deployment

#### Deploy Backend

1. Create a new Web Service on Render
   - Runtime: Python 3.11
   - Build Command: 
     ```bash
     pip install -r backend/requirements.txt && cd backend && python manage.py migrate
     ```
   - Start Command:
     ```bash
     cd backend && gunicorn config.wsgi:application
     ```

2. Create PostgreSQL Database
   - New → PostgreSQL Database
   - Free tier, single region
   - Note the database URL

3. Set Environment Variables
   - `DEBUG`: `false`
   - `SECRET_KEY`: Generate strong key
   - `ALLOWED_HOSTS`: `.onrender.com`
   - `DATABASE_URL`: Copy from PostgreSQL service
   - `CORS_ORIGINS`: `https://docedit-frontend.onrender.com`

#### Deploy Frontend

1. Create a new Web Service on Render
   - Runtime: Node 18
   - Build Command: `cd frontend && npm install && npm run build`
   - Start Command: `cd frontend && npm run preview`
   - Environment Variables:
     - `VITE_API_BASE_URL`: `https://docedit-backend.onrender.com/api`

### Option 3: Deploy to Heroku

1. **Install Heroku CLI**
   ```bash
   npm install -g heroku
   heroku login
   ```

2. **Create Heroku apps**
   ```bash
   heroku create docedit-backend
   heroku create docedit-frontend
   ```

3. **Configure Procfile**
   - Already included in repository
   - Heroku will automatically use it

4. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=<strong-key> -a docedit-backend
   heroku config:set DEBUG=false -a docedit-backend
   ```

5. **Deploy**
   ```bash
   git push heroku main -a docedit-backend
   git push heroku main -a docedit-frontend
   ```

## Database Migrations

After deployment, run migrations:

```bash
# Via Render dashboard
# Go to backend service → Shell
python manage.py migrate

# Via Heroku
heroku run python manage.py migrate -a docedit-backend
```

## Seed Test Users

```bash
# Via Render
# Go to backend service → Shell
python manage.py seed_users

# Via Heroku
heroku run python manage.py seed_users -a docedit-backend
```

## Verify Deployment

1. Visit frontend URL
2. Login with test credentials:
   - Email: `owner@test.com`
   - Password: `Password123`
3. Create a test document
4. Share it with `collaborator@test.com`
5. Test all features

## Troubleshooting

### Database connection errors
- Check DATABASE_URL is set correctly
- Verify PostgreSQL database is running
- Run migrations: `python manage.py migrate`

### CORS errors
- Verify `CORS_ORIGINS` includes frontend URL
- Include protocol (https://)
- Rebuild backend after changing environment variables

### Static files not loading
- Django collects static files automatically
- WhiteNoise middleware handles serving
- Check Django logs for errors

### Frontend can't connect to backend
- Verify `VITE_API_BASE_URL` is set correctly
- Include `/api` in the URL
- Use https:// in production
- Check CORS_ORIGINS on backend

### "Cannot find module" errors
- Install dependencies: `npm install` or `pip install -r requirements.txt`
- Check Node/Python versions match requirements
- Clear build cache and rebuild

## Monitoring

### View Logs
- Render: Service dashboard → Logs tab
- Heroku: `heroku logs -t -a app-name`

### Check Health
- Backend: `https://backend-url/api/auth/login/` (should return 400 if down)
- Frontend: Visit URL in browser

## Production Considerations

### Performance
- Enable caching headers
- Minimize frontend bundle size
- Consider CDN for static files
- Use database connection pooling

### Security
- Keep dependencies updated
- Monitor for security vulnerabilities
- Use strong SECRET_KEY
- Enable HTTPS (automatic on Render/Heroku)

### Scaling
- For production load, upgrade from free tier
- Use managed PostgreSQL instead of free tier
- Consider adding Redis for caching
- Implement rate limiting

## Rollback

If deployment fails:

1. **Render**: Automatic rollback to previous deployment
2. **Heroku**: `git push heroku previous-commit:main`

## Auto-deployment

Both Render and Heroku support auto-deployment:
1. Connect GitHub repository
2. Enable auto-deploy from main branch
3. Every git push will trigger deployment

## Environment Configuration

### Development
```
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CORS_ORIGINS=http://localhost:5173
```

### Production
```
DEBUG=False
ALLOWED_HOSTS=*.onrender.com
DATABASE_URL=postgresql://...
CORS_ORIGINS=https://docedit-frontend.onrender.com
```

## Next Steps

1. Choose deployment platform (Render recommended)
2. Follow deployment option 1 or 2
3. Verify with test scenarios
4. Share live URL for review
5. Monitor logs for issues
