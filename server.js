import express from "express";
import cors from "cors";
import { Sequelize, DataTypes } from "sequelize";
import mongoose from "mongoose";
import dotenv from "dotenv";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

// ========== PostgreSQL Setup ==========
const sequelize = new Sequelize(
  process.env.PG_DATABASE || "shopease",
  process.env.PG_USER || "postgres",
  process.env.PG_PASSWORD || "password",
  {
    host: process.env.PG_HOST || "localhost",
    port: process.env.PG_PORT || 5432,
    dialect: "postgres",
  }
);

// Models
const Category = sequelize.define("Category", {
  name: DataTypes.STRING,
});

const Product = sequelize.define("Product", {
  name: DataTypes.STRING,
  price: DataTypes.INTEGER,
  specs: DataTypes.TEXT,
  stock: { type: DataTypes.INTEGER, defaultValue: 10 },
  category: DataTypes.STRING,
  subcategory: DataTypes.STRING,
});

Product.belongsTo(Category);
Category.hasMany(Product);

// ========== MongoDB Setup ==========
mongoose.connect(process.env.MONGO_URI || "mongodb://localhost/shopease");

const CartSchema = new mongoose.Schema({
  userId: String,
  items: [{ productId: String, name: String, price: Number, qty: Number }],
  createdAt: { type: Date, default: Date.now },
});

const Cart = mongoose.model("Cart", CartSchema);

// ========== Product Data Seed ==========
const PRODUCTS = {
  Electronics: {
    Laptops: [
      { brand: "Dell", model: "Inspiron 15", specs: "i5, 8GB RAM, 512GB SSD, 15.6\", Silver", price: 55000 },
      { brand: "HP", model: "Pavilion", specs: "i7, 16GB RAM, 1TB SSD, 14\", Blue", price: 75000 },
    ],
    Phones: [
      { brand: "Apple", model: "iPhone 14", specs: "128GB, A15 Bionic", price: 80000 },
      { brand: "Samsung", model: "Galaxy S23", specs: "256GB, Snapdragon 8 Gen 2", price: 72000 },
    ],
  },
  Clothes: {
    Mens: [
      { brand: "Peter England", model: "Formal Shirt", specs: "Cotton, Sizes: 38–44", price: 1800 },
      { brand: "Levis", model: "Slim Fit Jeans", specs: "Denim, Waist: 30–38", price: 3500 },
    ],
    Womens: [
      { brand: "Zara", model: "Casual Dress", specs: "Sizes: XS–L, Cotton", price: 4500 },
      { brand: "H&M", model: "Evening Dress", specs: "Sizes: S–XL, Velvet", price: 6000 },
    ],
  },
};

// ========== Routes ==========

// Get all categories
app.get("/api/categories", async (req, res) => {
  const categories = Object.keys(PRODUCTS);
  res.json(categories);
});

// Get subcategories
app.get("/api/categories/:cat", (req, res) => {
  const subs = Object.keys(PRODUCTS[req.params.cat] || {});
  res.json(subs);
});

// Get products
app.get("/api/products/:cat/:sub", (req, res) => {
  const { cat, sub } = req.params;
  const items = PRODUCTS[cat]?.[sub] || [];
  res.json(items);
});

// Get cart
app.get("/api/cart/:userId", async (req, res) => {
  const cart = await Cart.findOne({ userId: req.params.userId });
  res.json(cart || { items: [] });
});

// Add to cart
app.post("/api/cart/:userId", async (req, res) => {
  const { userId } = req.params;
  const { item } = req.body;

  let cart = await Cart.findOne({ userId });
  if (!cart) cart = new Cart({ userId, items: [] });

  const existing = cart.items.find((i) => i.name === item.name);
  if (existing) {
    existing.qty += item.qty;
  } else {
    cart.items.push(item);
  }

  await cart.save();
  res.json(cart);
});

// Update cart
app.put("/api/cart/:userId/:idx", async (req, res) => {
  const { userId, idx } = req.params;
  const { qty } = req.body;

  const cart = await Cart.findOne({ userId });
  if (cart && cart.items[idx]) {
    if (qty > 0) {
      cart.items[idx].qty = qty;
    } else {
      cart.items.splice(idx, 1);
    }
    await cart.save();
  }

  res.json(cart);
});

// Clear cart
app.delete("/api/cart/:userId", async (req, res) => {
  await Cart.deleteOne({ userId: req.params.userId });
  res.json({ success: true });
});

// Checkout (create order in PostgreSQL)
app.post("/api/checkout/:userId", async (req, res) => {
  const cart = await Cart.findOne({ userId: req.params.userId });
  // Create order record in PostgreSQL if needed
  await Cart.deleteOne({ userId: req.params.userId });
  res.json({ success: true, message: "Order placed!" });
});

// ========== Start Server ==========
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
