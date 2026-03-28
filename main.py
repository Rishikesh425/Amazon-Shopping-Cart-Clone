from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
from dotenv import load_dotenv
import asyncio

# ========== Database Imports ==========
from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

load_dotenv()

# ========== Initialize FastAPI ==========
app = FastAPI(title="ShopEasy API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== PostgreSQL Setup ==========
try:
    PG_URL = f"postgresql://{os.getenv('PG_USER', 'postgres')}:{os.getenv('PG_PASSWORD', 'password')}@{os.getenv('PG_HOST', 'localhost')}:{os.getenv('PG_PORT', 5432)}/{os.getenv('PG_DATABASE', 'shopease')}"
    engine = create_engine(PG_URL, echo=False, pool_pre_ping=True)
    SessionLocal = sessionmaker(bind=engine)
    Base = declarative_base()
    
    # PostgreSQL Models
    class Category(Base):
        __tablename__ = "categories"
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)

    class Product(Base):
        __tablename__ = "products"
        id = Column(Integer, primary_key=True)
        name = Column(String)
        price = Column(Integer)
        specs = Column(Text)
        stock = Column(Integer, default=10)
        category = Column(String)
        subcategory = Column(String)

    # Create tables (non-blocking)
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ PostgreSQL connected")
    except:
        print("⚠ PostgreSQL not available - will connect on deployment")
        engine = None
except Exception as e:
    print(f"⚠ PostgreSQL setup warning: {e}")
    engine = None

# ========== MongoDB Setup ==========
try:
    MONGO_CLIENT = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/shopease"), serverSelectionTimeoutMS=5000)
    MONGO_CLIENT.admin.command('ping')
    MONGO_DB = MONGO_CLIENT.get_database(os.getenv("MONGO_DB", "shopease"))
    CARTS = MONGO_DB["carts"]
    print("✓ MongoDB connected")
except (ServerSelectionTimeoutError, Exception) as e:
    print(f"⚠ MongoDB not available: {e}")
    MONGO_DB = None
    CARTS = None

# ========== Pydantic Models ==========
class CartItem(BaseModel):
    productId: Optional[str] = None
    name: str
    price: int
    qty: int

class Cart(BaseModel):
    userId: str
    items: List[CartItem] = []

# ========== Product Data ==========
PRODUCTS = {
    "Electronics": {
        "Laptops": [
            {"brand": "Dell", "model": "Inspiron 15", "specs": "i5, 8GB RAM, 512GB SSD, 15.6\", Silver", "price": 55000},
            {"brand": "Dell", "model": "XPS 13", "specs": "i7, 16GB RAM, 1TB SSD, 13\", Platinum", "price": 120000},
            {"brand": "HP", "model": "Pavilion", "specs": "i7, 16GB RAM, 1TB SSD, 14\", Blue", "price": 75000},
            {"brand": "HP", "model": "Omen", "specs": "Ryzen 7, 16GB RAM, RTX 4060, 15.6\", Black", "price": 95000},
            {"brand": "Lenovo", "model": "ThinkPad X1", "specs": "i7, 16GB RAM, 512GB SSD, 14\", Carbon Black", "price": 110000},
            {"brand": "Asus", "model": "TUF Gaming F15", "specs": "i5, RTX 3050, 16GB RAM, 512GB SSD, 15.6\"", "price": 85000},
        ],
        "Phones": [
            {"brand": "Apple", "model": "iPhone 14", "specs": "128GB, A15 Bionic, Blue/Black/Purple", "price": 80000},
            {"brand": "Apple", "model": "iPhone 15 Pro", "specs": "256GB, A17 Pro, Titanium", "price": 140000},
            {"brand": "Samsung", "model": "Galaxy S23", "specs": "256GB, Snapdragon 8 Gen 2, Green/Lavender", "price": 72000},
            {"brand": "Samsung", "model": "Galaxy Z Fold 5", "specs": "512GB, Snapdragon 8 Gen 2, Phantom Black", "price": 145000},
            {"brand": "OnePlus", "model": "11R", "specs": "256GB, Snapdragon 8+ Gen 1, Sonic Black/Silver", "price": 45000},
            {"brand": "Xiaomi", "model": "13 Pro", "specs": "512GB, Snapdragon 8 Gen 2, Ceramic White", "price": 78000},
        ],
        "Headphones": [
            {"brand": "Sony", "model": "WH-1000XM5", "specs": "Wireless, Noise Cancelling, Black", "price": 29990},
            {"brand": "Sony", "model": "WF-C700N", "specs": "Bluetooth, ANC, White", "price": 8990},
            {"brand": "Boat", "model": "Rockerz 450", "specs": "Bluetooth, 15H Playtime, Blue/Red", "price": 1499},
            {"brand": "JBL", "model": "Tune 510BT", "specs": "Wireless, 40mm Drivers, Black", "price": 2999},
        ],
        "Watches": [
            {"brand": "Apple", "model": "Watch Series 9", "specs": "GPS + Cellular, 45mm, Pink Aluminum", "price": 45000},
            {"brand": "Samsung", "model": "Galaxy Watch 6", "specs": "Bluetooth, 44mm, Graphite", "price": 34000},
            {"brand": "Noise", "model": "ColorFit Pro 4", "specs": "1.8\" Display, Heart Rate, Blue", "price": 3500},
        ],
    },
    "Clothes": {
        "Men": [
            {"brand": "Allen Solly", "model": "Slim Fit Shirt", "specs": "Cotton, Sizes: S–XL, Blue/White", "price": 2000},
            {"brand": "Peter England", "model": "Formal Shirt", "specs": "Cotton, Sizes: 38–44, White/Grey", "price": 1800},
            {"brand": "Van Heusen", "model": "Checked Shirt", "specs": "Slim Fit, Sizes: M–XL, Navy/Red", "price": 2200},
            {"brand": "Levis", "model": "Slim Fit Jeans", "specs": "Denim, Waist: 30–38, Blue", "price": 3500},
            {"brand": "Wrangler", "model": "Regular Fit", "specs": "Stretch Denim, Waist: 32–42, Black", "price": 2800},
            {"brand": "Pepe Jeans", "model": "Skinny Fit", "specs": "Cotton Blend, Waist: 30–38, Grey", "price": 3000},
            {"brand": "Puma", "model": "Graphic Tee", "specs": "Cotton, Sizes: S–XL, Black/Red", "price": 1500},
            {"brand": "Adidas", "model": "Sports Tee", "specs": "Polyester, Sizes: S–XXL, Blue/White", "price": 1700},
            {"brand": "Jack & Jones", "model": "Plain Tee", "specs": "Organic Cotton, Sizes: S–XL", "price": 1200},
            {"brand": "Raymond", "model": "Blazer", "specs": "Wool Blend, Sizes: 38–44, Grey", "price": 6500},
            {"brand": "Arrow", "model": "Trousers", "specs": "Slim Fit, Sizes: 30–38, Black", "price": 2800},
        ],
        "Women": [
            {"brand": "FabIndia", "model": "Silk Saree", "specs": "6.3m, Handloom, Maroon/Green", "price": 5000},
            {"brand": "Biba", "model": "Cotton Saree", "specs": "6m, Printed, Yellow/Blue", "price": 3500},
            {"brand": "Zara", "model": "Casual Dress", "specs": "Sizes: XS–L, Cotton, Beige/Black", "price": 4500},
            {"brand": "H&M", "model": "Evening Dress", "specs": "Sizes: S–XL, Velvet, Red/Navy", "price": 6000},
            {"brand": "Only", "model": "Formal Top", "specs": "Polyester, Sizes: S–L, White/Peach", "price": 1600},
            {"brand": "Forever 21", "model": "Floral Top", "specs": "Rayon, Sizes: XS–L, Pink/Yellow", "price": 1800},
            {"brand": "Global Desi", "model": "Anarkali", "specs": "Silk Blend, Sizes: M–XL, Purple/Teal", "price": 4200},
            {"brand": "W for Woman", "model": "Kurti Set", "specs": "Cotton, Sizes: S–XL, Blue/Maroon", "price": 2800},
        ],
    },
    "Shoes": {
        "Sports": [
            {"brand": "Nike", "model": "Air Zoom", "specs": "Running Shoes, Sizes: 7–12, Black/Grey", "price": 6000},
            {"brand": "Nike", "model": "Metcon 8", "specs": "Training, Sizes: 6–11, Blue/Red", "price": 8500},
            {"brand": "Adidas", "model": "Ultraboost", "specs": "Running, Sizes: 6–12, White/Grey", "price": 7000},
            {"brand": "Adidas", "model": "Predator", "specs": "Football, Sizes: 7–11, Black/Yellow", "price": 9000},
        ],
        "Casual": [
            {"brand": "Puma", "model": "Sneakers", "specs": "Sizes: 6–11, Black/Navy", "price": 4000},
            {"brand": "Puma", "model": "Slides", "specs": "Sizes: 7–12, Blue/Grey", "price": 1500},
            {"brand": "Bata", "model": "Loafers", "specs": "Sizes: 7–11, Tan/Brown", "price": 2500},
            {"brand": "Bata", "model": "Canvas", "specs": "Sizes: 6–10, Blue/White", "price": 1800},
        ],
        "Formal": [
            {"brand": "Hush Puppies", "model": "Oxford", "specs": "Leather, Sizes: 7–11, Brown/Black", "price": 5500},
            {"brand": "Red Tape", "model": "Derby", "specs": "PU Leather, Sizes: 6–12, Tan", "price": 4200},
        ],
    },
    "Daily Essentials": {
        "Grocery": [
            {"brand": "Aashirvaad", "model": "Atta", "specs": "10kg Pack, Whole Wheat", "price": 500},
            {"brand": "Tata", "model": "Salt", "specs": "1kg, Iodized", "price": 25},
            {"brand": "India Gate", "model": "Basmati Rice", "specs": "5kg, Premium Quality", "price": 700},
            {"brand": "Fortune", "model": "Sunflower Oil", "specs": "5L Jar", "price": 780},
        ],
        "Toiletries": [
            {"brand": "Colgate", "model": "Toothpaste", "specs": "150g, Mint Flavor", "price": 90},
            {"brand": "Dove", "model": "Shampoo", "specs": "500ml, Hair Fall Rescue", "price": 350},
            {"brand": "Lifebuoy", "model": "Soap", "specs": "Pack of 4, 125g each", "price": 120},
            {"brand": "Nivea", "model": "Body Lotion", "specs": "400ml, Aloe Hydration", "price": 260},
        ],
        "Cleaning": [
            {"brand": "Surf Excel", "model": "Detergent", "specs": "4kg Pack", "price": 480},
            {"brand": "Vim", "model": "Dishwash Gel", "specs": "1L Bottle, Lemon", "price": 180},
            {"brand": "Lizol", "model": "Floor Cleaner", "specs": "2L Lavender", "price": 220},
        ],
        "Stationery": [
            {"brand": "Classmate", "model": "Notebook", "specs": "200 Pages, A4 Size", "price": 60},
            {"brand": "Reynolds", "model": "Pen Pack", "specs": "10 Blue Ink Pens", "price": 90},
        ],
    },
    "Protein & Supplements": {
        "Whey Protein": [
            {"brand": "Optimum Nutrition", "model": "Gold Standard", "specs": "2kg, Double Rich Chocolate", "price": 6000},
            {"brand": "MuscleBlaze", "model": "Biozyme Whey", "specs": "2kg, Café Mocha", "price": 5200},
            {"brand": "Dymatize", "model": "ISO 100", "specs": "2kg, Gourmet Vanilla", "price": 7500},
            {"brand": "MyProtein", "model": "Impact Whey", "specs": "1kg, Chocolate Smooth", "price": 3300},
        ],
        "Creatine": [
            {"brand": "Ultimate Nutrition", "model": "Creatine Monohydrate", "specs": "300g, Micronized", "price": 1200},
            {"brand": "HealthKart", "model": "Creatine", "specs": "250g, Unflavored", "price": 900},
            {"brand": "MyProtein", "model": "Creatine", "specs": "500g, Lemon Flavor", "price": 2000},
        ],
        "Multivitamins": [
            {"brand": "GNC", "model": "Mega Men", "specs": "60 Tablets, Energy + Immunity", "price": 1200},
            {"brand": "HealthKart", "model": "Daily Multivitamin", "specs": "90 Tablets, General Wellness", "price": 800},
            {"brand": "Revital", "model": "H Multivitamin", "specs": "60 Capsules, With Ginseng", "price": 1000},
        ],
        "Pre-Workout": [
            {"brand": "C4", "model": "Original", "specs": "300g, Fruit Punch Flavor", "price": 2500},
            {"brand": "BigMuscles", "model": "Nitric Shock", "specs": "250g, Orange Flavor", "price": 1800},
        ],
    }
}

# ========== Routes ==========

@app.get("/")
def home():
    return {"message": "ShopEasy API", "version": "1.0.0"}

@app.get("/api/categories")
def get_categories():
    """Get all categories"""
    return list(PRODUCTS.keys())

@app.get("/api/categories/{category}")
def get_subcategories(category: str):
    """Get subcategories for a category"""
    if category not in PRODUCTS:
        raise HTTPException(status_code=404, detail="Category not found")
    return list(PRODUCTS[category].keys())

@app.get("/api/products/{category}/{subcategory}")
def get_products(category: str, subcategory: str):
    """Get products for a subcategory"""
    if category not in PRODUCTS or subcategory not in PRODUCTS[category]:
        raise HTTPException(status_code=404, detail="Category or subcategory not found")
    return PRODUCTS[category][subcategory]

@app.get("/api/cart/{user_id}")
def get_cart(user_id: str):
    """Get user's cart from MongoDB"""
    if not CARTS:
        raise HTTPException(status_code=500, detail="MongoDB not available")
    cart = CARTS.find_one({"userId": user_id})
    if not cart:
        return {"userId": user_id, "items": []}
    cart.pop("_id", None)
    return cart

@app.post("/api/cart/{user_id}")
def add_to_cart(user_id: str, item: CartItem):
    """Add item to cart (MongoDB)"""
    if not CARTS:
        raise HTTPException(status_code=500, detail="MongoDB not available")
    
    cart = CARTS.find_one({"userId": user_id})
    if not cart:
        CARTS.insert_one({"userId": user_id, "items": [item.dict()], "createdAt": datetime.now()})
    else:
        existing = next((i for i in cart["items"] if i["name"] == item.name), None)
        if existing:
            existing["qty"] += item.qty
            CARTS.update_one({"userId": user_id}, {"$set": {"items": cart["items"]}})
        else:
            CARTS.update_one({"userId": user_id}, {"$push": {"items": item.dict()}})
    
    cart = CARTS.find_one({"userId": user_id})
    cart.pop("_id", None)
    return cart

@app.put("/api/cart/{user_id}/{idx}")
def update_cart_item(user_id: str, idx: int, qty: int):
    """Update cart item quantity"""
    if not CARTS:
        raise HTTPException(status_code=500, detail="MongoDB not available")
    
    cart = CARTS.find_one({"userId": user_id})
    if not cart or idx >= len(cart["items"]):
        raise HTTPException(status_code=404, detail="Item not found")
    
    if qty > 0:
        cart["items"][idx]["qty"] = qty
    else:
        cart["items"].pop(idx)
    
    CARTS.update_one({"userId": user_id}, {"$set": {"items": cart["items"]}})
    cart.pop("_id", None)
    return cart

@app.delete("/api/cart/{user_id}")
def clear_cart(user_id: str):
    """Clear user's cart"""
    if not CARTS:
        raise HTTPException(status_code=500, detail="MongoDB not available")
    CARTS.delete_one({"userId": user_id})
    return {"success": True}

@app.post("/api/checkout/{user_id}")
def checkout(user_id: str):
    """Checkout and clear cart"""
    if not CARTS:
        raise HTTPException(status_code=500, detail="MongoDB not available")
    CARTS.delete_one({"userId": user_id})
    return {"success": True, "message": "Order placed!"}

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}
