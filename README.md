<div align="center">

<h1>🛒 ShopEasy</h1>

**Amazon-Inspired E-Commerce Platform**

A full-stack shopping cart clone with a Python FastAPI backend, dual-database architecture, and a vanilla HTML/CSS/JS frontend.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat-square&logo=mongodb&logoColor=white)

🌐 **Live Demo**: [amazon-shopping-cart-clone.vercel.app](https://amazon-shopping-cart-clone.vercel.app)

</div>

---

## Features

✅ RESTful API built with FastAPI — lightweight and async-ready  
✅ PostgreSQL for structured product and category data  
✅ MongoDB for flexible, real-time cart storage  
✅ 5 product categories — Electronics, Clothes, Shoes, Groceries, Supplements  
✅ Real-time cart management — add, update, clear, and checkout  
✅ CORS-enabled for seamless frontend integration  
✅ Ready for production deployment on Railway + Vercel  
✅ 70% less code than the original Flask version  

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Rishikesh425/Amazon-Shopping-Cart-Clone.git
cd Amazon-Shopping-Cart-Clone
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup databases

**MongoDB Atlas** (Free):
- Go to https://www.mongodb.com/cloud/atlas
- Create a free cluster and copy your connection string

**PostgreSQL** (Local):
```bash
createdb shopease
```

### 4. Configure environment

```bash
cp .env.example .env
# Edit .env with your credentials
```

```env
# PostgreSQL
PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=shopease
PG_USER=your_pg_username
PG_PASSWORD=your_pg_password

# MongoDB
MONGO_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/shopease
MONGO_DB=shopease
```

### 5. Run locally

```bash
uvicorn main:app --reload
```

API available at: `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API health and version info |
| GET | `/api/categories` | Get all product categories |
| GET | `/api/categories/{category}` | Get subcategories for a category |
| GET | `/api/products/{category}/{subcategory}` | Get products in a subcategory |
| GET | `/api/cart/{userId}` | Get a user's cart |
| POST | `/api/cart/{userId}` | Add an item to the cart |
| PUT | `/api/cart/{userId}/{idx}` | Update quantity of a cart item |
| DELETE | `/api/cart/{userId}` | Clear a user's cart |
| POST | `/api/checkout/{userId}` | Checkout and place order |
| GET | `/health` | Health check |

---

## Product Catalog

| Category | Subcategories |
|----------|--------------|
| Electronics | Laptops, Phones, Headphones, Watches |
| Clothes | Men, Women |
| Shoes | Sports, Casual, Formal |
| Daily Essentials | Grocery, Toiletries, Cleaning, Stationery |
| Protein & Supplements | Whey Protein, Creatine, Multivitamins, Pre-Workout |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, FastAPI |
| **Relational DB** | PostgreSQL (products, categories) |
| **Document DB** | MongoDB Atlas (cart storage) |
| **ORM** | SQLAlchemy + Pydantic |
| **Frontend** | HTML, CSS, JavaScript (Vanilla) |
| **Deployment** | Railway (backend), Vercel (frontend) |

---

## File Structure

```
├── main.py             # FastAPI app — all routes and DB logic
├── app.py              # App entry / alternate runner
├── AmazonCart2.py      # Legacy version reference
├── server.js           # Node server (frontend serving)
├── index.html          # Homepage
├── shop.html           # Product browsing page
├── study_sheet.html    # Dev reference sheet
├── templates/          # HTML templates
├── requirements.txt    # Python dependencies
├── package.json        # Node dependencies
├── DEPLOYMENT.md       # Step-by-step deployment guide
└── README.md           # This file
```

---

## vs Flask (Original)

| Feature | Flask Version | FastAPI Version |
|---------|--------------|-----------------|
| Lines of Code | ~500 | ~230 |
| Setup Time | 15 min | 3 min |
| Async Support | ✗ | ✓ |
| Auto API Docs | ✗ | ✓ (Swagger + ReDoc) |
| Speed | Slow | Very Fast |
| Deployment | Heroku | Railway |

---

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for full step-by-step instructions.

**Recommended stack:**

- **Backend**: [Railway.app](https://railway.app) — supports Python + PostgreSQL natively
- **Frontend**: [Vercel](https://vercel.com) — zero-config static deployment
- **Database**: Railway PostgreSQL + MongoDB Atlas (free tier)

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## Author

<div align="center">

**Rishikesh Paladugu**

[![GitHub](https://img.shields.io/badge/GitHub-Rishikesh425-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Rishikesh425)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rishikesh-paladugu-23596b301)

⭐ If this project helped or inspired you, give it a star!

</div>

---

## License

MIT
