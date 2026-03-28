# Deployment Guide

## Backend Deployment (Python/FastAPI)

### Option 1: Railway.app (Recommended)
1. Go to https://railway.app
2. Connect your GitHub repo
3. Add PostgreSQL + MongoDB Atlas services
4. Set start command: `uvicorn main:app --host 0.0.0.0`
5. Deploy

### Option 2: Render.com
1. Go to https://render.com
2. Create new Web Service
3. Connect GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn main:app --host 0.0.0.0`
6. Deploy

### Option 3: Heroku (Free tier no longer available)
```bash
heroku login
heroku create your-app-name
git push heroku main
```

## Frontend Deployment (GitHub Pages)

1. Move `index.html` to `docs/` folder
2. Update `API` variable in index.html with your backend URL
3. Go to GitHub repo Settings → Pages
4. Select `docs` as source
5. Site will be live at `https://username.github.io/repo`

## Local Testing

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start MongoDB (Local)
```bash
mongod
```

### 3. Start PostgreSQL (Local)
```bash
createdb shopease
```

### 4. Create .env File
```bash
copy .env.example .env
```

Edit `.env`:
```
PORT=8000
PG_HOST=localhost
PG_USER=postgres
PG_PASSWORD=yourpass
PG_DATABASE=shopease
MONGO_URI=mongodb://localhost:27017/shopease
```

### 5. Run Development Server
```bash
uvicorn main:app --reload
```

Visit API at: `http://localhost:8000/docs` (Swagger UI)
Visit API at: `http://localhost:8000/`

Visit frontend at: `http://localhost:8000` (after moving index.html)

## Environment Variables

**For Backend (.env):**
```
PORT=8000
PG_HOST=your-postgres-host
PG_USER=your-user
PG_PASSWORD=your-password
PG_DATABASE=shopease
MONGO_URI=mongodb+srv://...
```

**For Frontend:**
Update API URL in `index.html`:
```javascript
const API = "https://your-railway-app.railway.app/api";
```

## Database Setup

### PostgreSQL Setup (Railway)
1. Add PostgreSQL to your Railway project
2. Get connection string from variables
3. Update `.env` file with credentials

### MongoDB Atlas (Cloud)
1. Go to https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Create database user
4. Get connection string
5. Update MONGO_URI in `.env`

## Production Checklist

- [ ] PostgreSQL database created and connected
- [ ] MongoDB Atlas cluster created and connected
- [ ] Backend deployed to Railway/Render
- [ ] Frontend repo created on GitHub
- [ ] index.html moved to docs/ folder
- [ ] API URL updated in index.html
- [ ] Frontend deployed to GitHub Pages
- [ ] CORS configured properly (should be `allow_origins=["*"]`)
- [ ] Environment variables set on deployment provider
- [ ] Test API endpoints: `https://your-backend.com/api/categories`
- [ ] Test frontend: `https://username.github.io/repo`

## Testing Endpoints

```bash
# Get categories
curl http://localhost:8000/api/categories

# Get products
curl http://localhost:8000/api/products/Electronics/Laptops

# Get cart
curl http://localhost:8000/api/cart/user123

# Add to cart
curl -X POST http://localhost:8000/api/cart/user123 \
  -H "Content-Type: application/json" \
  -d '{"name":"Dell Inspiron","price":55000,"qty":1}'

# Checkout
curl -X POST http://localhost:8000/api/checkout/user123

# Health check
curl http://localhost:8000/health
```

## Troubleshooting

**"ModuleNotFoundError: No module named 'fastapi'"**
```bash
pip install -r requirements.txt
```

**"ConnectionRefusedError: [Errno 111] Connection refused" (MongoDB)**
- Make sure MongoDB is running or MongoDB Atlas connection string is correct
- Check MONGO_URI in .env

**"psycopg2.OperationalError: could not connect to server"**
- Make sure PostgreSQL is running
- Check PG_HOST, PG_USER, PG_PASSWORD in .env

**CORS errors on frontend**
- Already configured in main.py to allow all origins
- If still not working, update CORS in main.py lines 20-25
