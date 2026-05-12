# core/project_generator.py — S.E.A.D.S. v10.0
# ============================================================
# Generates REAL multi-file projects:
#   frontend/  → React + Vite + Tailwind + shadcn/ui
#   backend/   → Express/Fastify + Prisma + JWT
#   database/  → SQLite (dev) / PostgreSQL (prod)
# Saves to E:\seads\online_app\<project_name>\
# ============================================================

import os, json, subprocess, shutil, time, logging
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

log = logging.getLogger("ProjectGenerator")

OUTPUT_DIR = Path(os.getenv("ONLINE_APP_DIR", r"E:\seads\online_app"))

# ─────────────────────────────────────────────────────────────
# LLM HELPER
# ─────────────────────────────────────────────────────────────
def llm(prompt: str, tokens: int = 3000) -> str:
    from core.llm_config import get_llm_response
    return get_llm_response(
        prompt=prompt, max_tokens=tokens, temperature=0.1,
        system=(
            "Expert React/Node.js architect. Return ONLY raw code. "
            "No explanations. No markdown fences. "
            "Production-quality, fully working code."
        ),
        task_type="code",
    )


# ─────────────────────────────────────────────────────────────
# FILE WRITER
# ─────────────────────────────────────────────────────────────
def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    log.info(f"  ✅ {path.relative_to(OUTPUT_DIR)} ({len(content):,} chars)")


# ═══════════════════════════════════════════════════════════
#  TECHNOLOGY DECISION ENGINE
# ═══════════════════════════════════════════════════════════

def choose_stack(idea: str, answers: dict) -> dict:
    """
    Picks optimal stack based on app type.
    Returns tech decisions with justifications.
    """
    u = idea.lower()
    features = str(answers).lower()

    stack = {
        # Frontend
        "frontend_framework": "react",           # React 18 + Vite
        "build_tool":         "vite",            # Faster than CRA/Next for SPAs
        "ui_library":         "tailwindcss",     # Utility-first CSS
        "component_lib":      "shadcn/ui",       # Accessible components
        "routing":            "react-router-dom", # v6 for SPAs
        "state":              "zustand",          # Lightweight, no boilerplate
        "http_client":        "axios",            # Better than fetch (interceptors)
        "icons":              "lucide-react",     # Consistent icon set

        # Backend
        "server":             "express",          # Mature ecosystem
        "database":           "sqlite3",          # Zero-config for dev
        "orm":                "prisma",           # Type-safe, great DX
        "auth":               "jsonwebtoken",     # JWT stateless auth
        "password":           "bcryptjs",         # Secure hashing
        "validation":         "zod",              # Runtime type safety
        "cors":               "cors",             # CORS middleware

        # Build/Deploy
        "package_manager":    "npm",
        "port_frontend":      5173,
        "port_backend":       3001,
    }

    # Override for specific app types
    if any(w in u for w in ["realtime","chat","live","websocket","multiplayer"]):
        stack["server"] = "fastify"       # Better WebSocket performance
        stack["realtime"] = "socket.io"

    if any(w in u for w in ["blog","news","seo","public"]):
        stack["build_tool"]  = "nextjs"   # SSR for SEO
        stack["routing"]     = "nextjs"   # Built-in routing

    if any(w in u for w in ["large","enterprise","complex","redux"]):
        stack["state"] = "redux-toolkit"  # More predictable for large apps

    if any(w in u for w in ["postgres","production","deploy","scale"]):
        stack["database"] = "postgresql"  # Production-grade

    return stack


# ═══════════════════════════════════════════════════════════
#  FILE GENERATORS — Each returns file content
# ═══════════════════════════════════════════════════════════

def gen_package_json_frontend(name: str, stack: dict) -> str:
    deps = {
        "react":               "^18.2.0",
        "react-dom":           "^18.2.0",
        "react-router-dom":    "^6.21.0",
        "axios":               "^1.6.0",
        "zustand":             "^4.4.7",
        "lucide-react":        "^0.303.0",
        "@radix-ui/react-dialog": "^1.0.5",
        "@radix-ui/react-dropdown-menu": "^2.0.6",
        "class-variance-authority": "^0.7.0",
        "clsx":                "^2.0.0",
        "tailwind-merge":      "^2.2.0",
    }
    dev_deps = {
        "@types/react":        "^18.2.43",
        "@types/react-dom":    "^18.2.17",
        "@vitejs/plugin-react": "^4.2.1",
        "autoprefixer":        "^10.4.16",
        "postcss":             "^8.4.32",
        "tailwindcss":         "^3.4.0",
        "vite":                "^5.0.8",
    }
    if stack.get("realtime"):
        deps["socket.io-client"] = "^4.6.0"

    return json.dumps({
        "name": name.lower().replace(" ","-"),
        "private": True,
        "version": "0.1.0",
        "type": "module",
        "scripts": {
            "dev":     "vite --port 5173",
            "build":   "vite build",
            "preview": "vite preview",
            "lint":    "eslint . --ext js,jsx --report-unused-disable-directives"
        },
        "dependencies": deps,
        "devDependencies": dev_deps,
    }, indent=2)


def gen_package_json_backend(name: str, stack: dict) -> str:
    deps = {
        "express":       "^4.18.2",
        "cors":          "^2.8.5",
        "dotenv":        "^16.3.1",
        "jsonwebtoken":  "^9.0.2",
        "bcryptjs":      "^2.4.3",
        "zod":           "^3.22.4",
        "@prisma/client":"^5.7.0",
        "morgan":        "^1.10.0",
        "helmet":        "^7.1.0",
    }
    dev_deps = {
        "prisma":        "^5.7.0",
        "nodemon":       "^3.0.2",
    }
    if stack.get("server") == "fastify":
        deps["fastify"]            = "^4.24.3"
        deps["@fastify/cors"]      = "^8.4.1"
        deps["@fastify/jwt"]       = "^7.2.4"
        deps.pop("express", None)
        deps.pop("cors", None)
    if stack.get("realtime"):
        deps["socket.io"] = "^4.6.0"

    return json.dumps({
        "name": f"{name.lower().replace(' ','-')}-backend",
        "version": "1.0.0",
        "main": "src/server.js",
        "type": "module",
        "scripts": {
            "dev":   "nodemon src/server.js",
            "start": "node src/server.js",
        },
        "dependencies": deps,
        "devDependencies": dev_deps,
    }, indent=2)


def gen_vite_config() -> str:
    return """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:3001',
        changeOrigin: true,
      },
    },
  },
})
"""


def gen_tailwind_config() -> str:
    return """/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input:  "hsl(var(--input))",
        ring:   "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground:  "hsl(var(--foreground))",
        primary: {
          DEFAULT:    "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT:    "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        accent: {
          DEFAULT:    "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        destructive: {
          DEFAULT:    "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT:    "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        card: {
          DEFAULT:    "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [],
}
"""


def gen_index_html(name: str) -> str:
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#6366f1" />
    <title>{name}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""


def gen_main_jsx() -> str:
    return """import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
)
"""


def gen_index_css() -> str:
    return """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 224.3 76.3% 48%;
  }
}

@layer base {
  * { @apply border-border; }
  body {
    @apply bg-background text-foreground;
    font-feature-settings: "rlig" 1, "calt" 1;
  }
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-thumb { @apply bg-border rounded; }

/* Transitions */
* { transition-property: color, background-color, border-color;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 150ms; }
"""


def gen_lib_utils() -> str:
    return """import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}
"""


def gen_api_client() -> str:
    return """import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
})

// Request interceptor — attach JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) config.headers.Authorization = `Bearer ${token}`
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor — handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('auth_user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
"""


def gen_auth_store() -> str:
    return """import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import api from './api'

export const useAuthStore = create(
  persist(
    (set, get) => ({
      user:  null,
      token: null,
      isAuthenticated: false,

      login: async (email, password) => {
        const { data } = await api.post('/auth/login', { email, password })
        localStorage.setItem('auth_token', data.token)
        set({ user: data.user, token: data.token, isAuthenticated: true })
        return data
      },

      register: async (name, email, password) => {
        const { data } = await api.post('/auth/register', { name, email, password })
        localStorage.setItem('auth_token', data.token)
        set({ user: data.user, token: data.token, isAuthenticated: true })
        return data
      },

      logout: () => {
        localStorage.removeItem('auth_token')
        set({ user: null, token: null, isAuthenticated: false })
      },

      updateUser: (userData) => {
        set((state) => ({ user: { ...state.user, ...userData } }))
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ user: state.user, token: state.token, isAuthenticated: state.isAuthenticated }),
    }
  )
)
"""


def gen_backend_env(name: str, stack: dict) -> str:
    return f"""# {name} Backend Environment
NODE_ENV=development
PORT=3001

# Database
DATABASE_URL="file:./dev.db"

# JWT
JWT_SECRET=seads_{name.lower().replace(' ','_')}_secret_change_in_production_2024
JWT_EXPIRES_IN=7d

# CORS
FRONTEND_URL=http://localhost:5173

# Optional: PostgreSQL (for production)
# DATABASE_URL="postgresql://user:password@localhost:5432/{name.lower().replace(' ','_')}_db"
"""


def gen_prisma_schema(idea: str) -> str:
    u = idea.lower()

    # E-commerce
    if any(w in u for w in ["shop","store","ecommerce","flipkart","amazon"]):
        return """datasource db {
  provider = "sqlite"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        String   @id @default(cuid())
  name      String
  email     String   @unique
  password  String
  role      String   @default("user")
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  orders    Order[]
  reviews   Review[]
  wishlist  Wishlist[]
}

model Product {
  id          String   @id @default(cuid())
  name        String
  description String
  price       Float
  mrp         Float
  stock       Int      @default(0)
  category    String
  brand       String?
  rating      Float    @default(0)
  imageUrl    String?
  createdAt   DateTime @default(now())
  orderItems  OrderItem[]
  reviews     Review[]
  wishlist    Wishlist[]
}

model Order {
  id        String      @id @default(cuid())
  userId    String
  user      User        @relation(fields: [userId], references: [id])
  status    String      @default("pending")
  total     Float
  address   String
  createdAt DateTime    @default(now())
  items     OrderItem[]
}

model OrderItem {
  id        String  @id @default(cuid())
  orderId   String
  order     Order   @relation(fields: [orderId], references: [id])
  productId String
  product   Product @relation(fields: [productId], references: [id])
  quantity  Int
  price     Float
}

model Review {
  id        String   @id @default(cuid())
  userId    String
  user      User     @relation(fields: [userId], references: [id])
  productId String
  product   Product  @relation(fields: [productId], references: [id])
  rating    Int
  comment   String?
  createdAt DateTime @default(now())
}

model Wishlist {
  id        String  @id @default(cuid())
  userId    String
  user      User    @relation(fields: [userId], references: [id])
  productId String
  product   Product @relation(fields: [productId], references: [id])
  @@unique([userId, productId])
}
"""

    # Social/LinkedIn
    if any(w in u for w in ["linkedin","social","twitter","instagram"]):
        return """datasource db {
  provider = "sqlite"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        String   @id @default(cuid())
  name      String
  email     String   @unique
  password  String
  bio       String?
  title     String?
  avatar    String?
  createdAt DateTime @default(now())
  posts     Post[]
  followers Follow[] @relation("following")
  following Follow[] @relation("follower")
  likes     Like[]
  comments  Comment[]
}

model Post {
  id        String    @id @default(cuid())
  content   String
  imageUrl  String?
  userId    String
  user      User      @relation(fields: [userId], references: [id])
  createdAt DateTime  @default(now())
  likes     Like[]
  comments  Comment[]
}

model Follow {
  id          String @id @default(cuid())
  followerId  String
  follower    User   @relation("follower", fields: [followerId], references: [id])
  followingId String
  following   User   @relation("following", fields: [followingId], references: [id])
  @@unique([followerId, followingId])
}

model Like {
  id     String @id @default(cuid())
  userId String
  user   User   @relation(fields: [userId], references: [id])
  postId String
  post   Post   @relation(fields: [postId], references: [id])
  @@unique([userId, postId])
}

model Comment {
  id        String   @id @default(cuid())
  content   String
  userId    String
  user      User     @relation(fields: [userId], references: [id])
  postId    String
  post      Post     @relation(fields: [postId], references: [id])
  createdAt DateTime @default(now())
}
"""

    # Dashboard/Analytics
    if any(w in u for w in ["dashboard","analytics"]):
        return """datasource db {
  provider = "sqlite"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        String   @id @default(cuid())
  name      String
  email     String   @unique
  password  String
  role      String   @default("viewer")
  createdAt DateTime @default(now())
  reports   Report[]
}

model Metric {
  id        String   @id @default(cuid())
  name      String
  value     Float
  category  String
  date      DateTime @default(now())
  meta      String?
}

model Report {
  id        String   @id @default(cuid())
  title     String
  type      String
  config    String
  userId    String
  user      User     @relation(fields: [userId], references: [id])
  createdAt DateTime @default(now())
}
"""

    # Booking
    if any(w in u for w in ["booking","hotel","appointment","reservation"]):
        return """datasource db {
  provider = "sqlite"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        String    @id @default(cuid())
  name      String
  email     String    @unique
  password  String
  phone     String?
  createdAt DateTime  @default(now())
  bookings  Booking[]
}

model Listing {
  id          String    @id @default(cuid())
  name        String
  type        String
  description String
  price       Float
  rating      Float     @default(0)
  imageUrl    String?
  location    String
  available   Boolean   @default(true)
  createdAt   DateTime  @default(now())
  bookings    Booking[]
  reviews     Review[]
}

model Booking {
  id        String   @id @default(cuid())
  userId    String
  user      User     @relation(fields: [userId], references: [id])
  listingId String
  listing   Listing  @relation(fields: [listingId], references: [id])
  checkIn   DateTime
  checkOut  DateTime
  guests    Int      @default(1)
  total     Float
  status    String   @default("pending")
  createdAt DateTime @default(now())
}

model Review {
  id        String   @id @default(cuid())
  userId    String
  listingId String
  listing   Listing  @relation(fields: [listingId], references: [id])
  rating    Int
  comment   String?
  createdAt DateTime @default(now())
}
"""

    # Generic / Todo / Dashboard
    return """datasource db {
  provider = "sqlite"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        String   @id @default(cuid())
  name      String
  email     String   @unique
  password  String
  role      String   @default("user")
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  items     Item[]
}

model Item {
  id          String   @id @default(cuid())
  title       String
  description String?
  status      String   @default("active")
  priority    String   @default("medium")
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}
"""


def gen_server_js(name: str, stack: dict) -> str:
    has_socket = bool(stack.get("realtime"))
    return f"""import express from 'express'
import cors from 'cors'
import helmet from 'helmet'
import morgan from 'morgan'
import dotenv from 'dotenv'
{"import { createServer } from 'http'" if has_socket else ""}
{"import { Server } from 'socket.io'" if has_socket else ""}

import authRoutes from './routes/auth.js'
import itemRoutes from './routes/items.js'
import userRoutes from './routes/users.js'

dotenv.config()

const app  = express()
{"const httpServer = createServer(app)" if has_socket else ""}
const PORT = process.env.PORT || 3001

// ── Security Middleware ────────────────────────────────────
app.use(helmet())
app.use(cors({{
  origin:      process.env.FRONTEND_URL || 'http://localhost:5173',
  credentials: true,
  methods:     ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}}))
app.use(morgan('dev'))
app.use(express.json({{ limit: '10mb' }}))
app.use(express.urlencoded({{ extended: true }}))

// ── Routes ────────────────────────────────────────────────
app.use('/api/auth',  authRoutes)
app.use('/api/items', itemRoutes)
app.use('/api/users', userRoutes)

// ── Health Check ──────────────────────────────────────────
app.get('/api/health', (req, res) => {{
  res.json({{
    status:    'ok',
    app:       '{name}',
    version:   '1.0.0',
    timestamp: new Date().toISOString(),
  }})
}})

{"// ── WebSocket ──────────────────────────────────────────────" if has_socket else ""}
{"const io = new Server(httpServer, { cors: { origin: process.env.FRONTEND_URL } })" if has_socket else ""}
{"io.on('connection', (socket) => {" if has_socket else ""}
{"  console.log('Client connected:', socket.id)" if has_socket else ""}
{"  socket.on('disconnect', () => console.log('Client disconnected:', socket.id))" if has_socket else ""}
{"})" if has_socket else ""}

// ── Error Handler ─────────────────────────────────────────
app.use((err, req, res, next) => {{
  console.error(err.stack)
  res.status(err.status || 500).json({{
    error:   err.message || 'Internal Server Error',
    ...(process.env.NODE_ENV === 'development' && {{ stack: err.stack }}),
  }})
}})

// ── 404 Handler ───────────────────────────────────────────
app.use((req, res) => {{
  res.status(404).json({{ error: `Route ${{req.method}} ${{req.url}} not found` }})
}})

// ── Start ─────────────────────────────────────────────────
{"httpServer" if has_socket else "app"}.listen(PORT, () => {{
  console.log(`✅ {name} backend running on http://localhost:${{PORT}}`)
  console.log(`   Environment: ${{process.env.NODE_ENV || 'development'}}`)
}})

export {{ {"io, " if has_socket else ""}app }}
"""


def gen_auth_middleware() -> str:
    return """import jwt from 'jsonwebtoken'

export const authenticate = (req, res, next) => {
  const authHeader = req.headers.authorization
  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' })
  }
  const token = authHeader.split(' ')[1]
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET)
    req.user = decoded
    next()
  } catch (err) {
    return res.status(401).json({ error: 'Invalid or expired token' })
  }
}

export const authorize = (...roles) => (req, res, next) => {
  if (!roles.includes(req.user?.role)) {
    return res.status(403).json({ error: 'Insufficient permissions' })
  }
  next()
}
"""


def gen_auth_routes() -> str:
    return """import express from 'express'
import bcrypt from 'bcryptjs'
import jwt from 'jsonwebtoken'
import { z } from 'zod'
import { PrismaClient } from '@prisma/client'

const router  = express.Router()
const prisma  = new PrismaClient()

const registerSchema = z.object({
  name:     z.string().min(2).max(50),
  email:    z.string().email(),
  password: z.string().min(6).max(100),
})

const loginSchema = z.object({
  email:    z.string().email(),
  password: z.string().min(1),
})

// ── POST /api/auth/register ────────────────────────────────
router.post('/register', async (req, res) => {
  try {
    const { name, email, password } = registerSchema.parse(req.body)

    const existing = await prisma.user.findUnique({ where: { email } })
    if (existing) return res.status(409).json({ error: 'Email already registered' })

    const hashed = await bcrypt.hash(password, 12)
    const user   = await prisma.user.create({
      data: { name, email, password: hashed },
      select: { id: true, name: true, email: true, role: true, createdAt: true },
    })

    const token = jwt.sign(
      { userId: user.id, email: user.email, role: user.role },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRES_IN || '7d' }
    )

    res.status(201).json({ user, token, message: 'Registration successful' })
  } catch (err) {
    if (err.name === 'ZodError') return res.status(400).json({ error: err.errors })
    res.status(500).json({ error: 'Registration failed' })
  }
})

// ── POST /api/auth/login ───────────────────────────────────
router.post('/login', async (req, res) => {
  try {
    const { email, password } = loginSchema.parse(req.body)

    const user = await prisma.user.findUnique({ where: { email } })
    if (!user) return res.status(401).json({ error: 'Invalid credentials' })

    const valid = await bcrypt.compare(password, user.password)
    if (!valid) return res.status(401).json({ error: 'Invalid credentials' })

    const token = jwt.sign(
      { userId: user.id, email: user.email, role: user.role },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRES_IN || '7d' }
    )

    const { password: _, ...safeUser } = user
    res.json({ user: safeUser, token, message: 'Login successful' })
  } catch (err) {
    if (err.name === 'ZodError') return res.status(400).json({ error: err.errors })
    res.status(500).json({ error: 'Login failed' })
  }
})

// ── GET /api/auth/me ───────────────────────────────────────
router.get('/me', async (req, res) => {
  const auth = req.headers.authorization
  if (!auth?.startsWith('Bearer ')) return res.status(401).json({ error: 'Unauthorized' })
  try {
    const { userId } = jwt.verify(auth.split(' ')[1], process.env.JWT_SECRET)
    const user = await prisma.user.findUnique({
      where:  { id: userId },
      select: { id: true, name: true, email: true, role: true, createdAt: true },
    })
    if (!user) return res.status(404).json({ error: 'User not found' })
    res.json({ user })
  } catch { res.status(401).json({ error: 'Invalid token' }) }
})

export default router
"""


def gen_seed_js(idea: str) -> str:
    u = idea.lower()
    if any(w in u for w in ["shop","store","ecommerce","flipkart","amazon"]):
        return """import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()

async function main() {
  console.log('Seeding database...')

  // Admin user
  const admin = await prisma.user.upsert({
    where: { email: 'admin@seads.com' },
    update: {},
    create: {
      name: 'Admin User', email: 'admin@seads.com',
      password: await bcrypt.hash('password123', 12), role: 'admin',
    },
  })

  // Sample products
  const products = [
    { name: 'boAt Airdopes 141', price: 1299, mrp: 4990, category: 'Electronics', brand: 'boAt', stock: 50, rating: 4.1 },
    { name: 'Levi\'s 511 Slim Jeans', price: 1999, mrp: 3999, category: 'Fashion', brand: 'Levi\'s', stock: 30, rating: 4.3 },
    { name: 'OnePlus Nord CE 3 Lite', price: 16999, mrp: 19999, category: 'Electronics', brand: 'OnePlus', stock: 25, rating: 4.2 },
    { name: 'Nike Air Force 1', price: 5995, mrp: 8995, category: 'Fashion', brand: 'Nike', stock: 20, rating: 4.5 },
    { name: 'Prestige Induction Cooktop', price: 1899, mrp: 3500, category: 'Home', brand: 'Prestige', stock: 40, rating: 4.0 },
    { name: 'Samsung 43" 4K TV', price: 32990, mrp: 49990, category: 'Electronics', brand: 'Samsung', stock: 15, rating: 4.4 },
  ]

  for (const p of products) {
    await prisma.product.upsert({
      where: { id: p.name.slice(0,10).replace(/ /g,'') },
      update: {},
      create: { ...p, imageUrl: `https://picsum.photos/seed/${p.name.slice(0,8)}/300/300` },
    })
  }

  console.log('✅ Seed complete')
}

main().catch(console.error).finally(() => prisma.$disconnect())
"""
    return """import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()

async function main() {
  console.log('Seeding database...')

  await prisma.user.upsert({
    where:  { email: 'admin@seads.com' },
    update: {},
    create: {
      name:     'Admin User',
      email:    'admin@seads.com',
      password: await bcrypt.hash('password123', 12),
      role:     'admin',
    },
  })

  await prisma.user.upsert({
    where:  { email: 'user@seads.com' },
    update: {},
    create: {
      name:     'Demo User',
      email:    'user@seads.com',
      password: await bcrypt.hash('password123', 12),
    },
  })

  console.log('✅ Seed complete')
  console.log('   admin@seads.com / password123')
  console.log('   user@seads.com  / password123')
}

main().catch(console.error).finally(() => prisma.$disconnect())
"""


def gen_readme(name: str, stack: dict) -> str:
    return f"""# {name}

> Generated by **S.E.A.D.S. v10.0** — Self-Evolving Autonomous Developer Swarm

## 🛠️ Tech Stack

| Layer     | Technology                              |
|-----------|----------------------------------------|
| Frontend  | React 18 + Vite + Tailwind CSS + shadcn/ui |
| Routing   | React Router v6                         |
| State     | Zustand (persist middleware)            |
| HTTP      | Axios (interceptors + error handling)   |
| Backend   | Node.js + Express                       |
| Database  | SQLite (Prisma ORM)                     |
| Auth      | JWT + bcryptjs                          |
| Validation| Zod                                     |
| Security  | Helmet + CORS                           |

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm 9+

### 1. Backend Setup
```bash
cd backend
npm install
npx prisma generate
npx prisma migrate dev --name init
npm run seed      # Optional: seed demo data
npm run dev       # Starts on http://localhost:3001
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev       # Starts on http://localhost:5173
```

## 📁 Project Structure
```
{name.lower().replace(' ','-')}/
├── frontend/                 # React + Vite
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Route-level pages
│   │   ├── hooks/            # Custom React hooks
│   │   ├── store/            # Zustand state stores
│   │   ├── lib/
│   │   │   ├── api.js        # Axios instance + interceptors
│   │   │   └── utils.js      # Utility functions
│   │   ├── App.jsx           # Root component + routes
│   │   ├── main.jsx          # Entry point
│   │   └── index.css         # Tailwind + CSS variables
│   ├── index.html
│   ├── vite.config.js        # Vite + proxy config
│   └── tailwind.config.js
│
├── backend/                  # Node.js + Express
│   ├── src/
│   │   ├── routes/           # Express route handlers
│   │   ├── middleware/       # Auth, validation, error
│   │   ├── controllers/      # Business logic
│   │   └── server.js         # App entry point
│   ├── prisma/
│   │   ├── schema.prisma     # Database schema
│   │   └── seed.js           # Seed data
│   └── .env
│
└── README.md
```

## 🔐 Default Credentials (development)
- Admin: `admin@seads.com` / `password123`
- User:  `user@seads.com`  / `password123`

## 🔌 API Endpoints
| Method | Endpoint            | Auth | Description          |
|--------|---------------------|------|----------------------|
| POST   | /api/auth/register  | No   | Register new user    |
| POST   | /api/auth/login     | No   | Login, returns JWT   |
| GET    | /api/auth/me        | Yes  | Get current user     |
| GET    | /api/items          | Yes  | List all items       |
| POST   | /api/items          | Yes  | Create item          |
| PUT    | /api/items/:id      | Yes  | Update item          |
| DELETE | /api/items/:id      | Yes  | Delete item          |
| GET    | /api/health         | No   | Health check         |
"""
