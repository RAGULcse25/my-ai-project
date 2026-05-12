# core/project_builder.py
# ============================================================
# Builds complete multi-file project in E:\seads\online_app
# Calls LLM to generate React components + Express routes
# Writes everything to disk with proper structure
# ============================================================

import os, json, time, logging, concurrent.futures
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from core.project_generator import (
    write_file, gen_package_json_frontend, gen_package_json_backend,
    gen_vite_config, gen_tailwind_config, gen_index_html, gen_main_jsx,
    gen_index_css, gen_lib_utils, gen_api_client, gen_auth_store,
    gen_backend_env, gen_prisma_schema, gen_server_js, gen_auth_middleware,
    gen_auth_routes, gen_seed_js, gen_readme, choose_stack, llm, OUTPUT_DIR
)

log = logging.getLogger("ProjectBuilder")


# ─────────────────────────────────────────────────────────────
# LLM FILE GENERATORS
# ─────────────────────────────────────────────────────────────

def gen_app_jsx(name: str, idea: str, answers: dict) -> str:
    features = answers.get("q1","")
    theme    = answers.get("q3","Dark")
    return llm(f"""Write a React App.jsx for: {name} ({idea})
Features: {features}, Theme: {theme}

Use React Router v6 with these routes:
- "/" → HomePage
- "/login" → LoginPage
- "/register" → RegisterPage
- "/dashboard" → DashboardPage (protected)
- "/profile" → ProfilePage (protected)
- Additional routes based on app type: {idea}

Include:
- ProtectedRoute component (checks useAuthStore)
- NavBar component with dark/light mode toggle
- Toast notifications (use simple useState toast)
- Theme provider (class="dark" on html element)
- Loading spinner while checking auth
- 404 Not Found page

Import from './pages/' folder.
Use Tailwind classes. Use shadcn/ui patterns (no external import needed, use tailwind).
Return ONLY the complete App.jsx code:""", tokens=2000)


def gen_home_page(name: str, idea: str, answers: dict) -> str:
    theme = answers.get("q3","Dark")
    return llm(f"""Write React HomePage.jsx for: {name} ({idea})
Theme: {theme}

This is the landing page. Include:
- Hero section: big headline, subtitle, CTA buttons (Get Started → /register, Login → /login)
- Features section: 3 feature cards with icons (use emoji or text icons)
- Stats section: 3-4 impressive numbers
- CTA section: "Start building today"
- Footer: links, copyright

Use Tailwind CSS classes. Beautiful, modern design.
Import useAuthStore to redirect if already logged in.
Return ONLY complete HomePage.jsx:""", tokens=2000)


def gen_dashboard_page(name: str, idea: str, answers: dict) -> str:
    u = idea.lower()

    if any(w in u for w in ["shop","store","ecommerce"]):
        context = "Show: total orders, revenue, products, users stats. Recent orders table. Top products."
    elif any(w in u for w in ["social","linkedin","twitter"]):
        context = "Show: posts feed, followers count, post composer, notifications."
    elif any(w in u for w in ["booking","hotel"]):
        context = "Show: upcoming bookings, available listings grid, quick book button."
    elif any(w in u for w in ["todo","task"]):
        context = "Show: Kanban board with 3 columns (To Do/In Progress/Done), add task button."
    else:
        context = "Show: welcome message, recent activity, quick stats cards, action buttons."

    return llm(f"""Write React DashboardPage.jsx for: {name} ({idea})
{context}

Requirements:
- Protected page (if not authenticated → redirect to /login)
- Use useAuthStore to get current user
- Sidebar navigation with links
- Main content area with dashboard content
- Header with user avatar + logout button
- Use axios (import api from '../lib/api') for data fetching
- useEffect to load data on mount
- Loading and error states
- Responsive: sidebar collapses on mobile (hamburger menu)

Use Tailwind CSS. Modern dark/light design.
Return ONLY complete DashboardPage.jsx:""", tokens=2500)


def gen_login_page() -> str:
    return """import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

export default function LoginPage() {
  const [email,    setEmail]    = useState('')
  const [password, setPassword] = useState('')
  const [error,    setError]    = useState('')
  const [loading,  setLoading]  = useState(false)
  const { login, isAuthenticated } = useAuthStore()
  const navigate = useNavigate()

  if (isAuthenticated) { navigate('/dashboard'); return null }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(''); setLoading(true)
    try {
      await login(email, password)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800 p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-indigo-600 mb-4">
            <span className="text-white text-2xl font-bold">S</span>
          </div>
          <h1 className="text-2xl font-bold text-white">Welcome back</h1>
          <p className="text-slate-400 mt-1">Sign in to your account</p>
        </div>

        {/* Card */}
        <div className="bg-slate-800 border border-slate-700 rounded-2xl p-8 shadow-xl">
          {error && (
            <div className="mb-4 p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1">Email</label>
              <input
                type="email" value={email} onChange={e => setEmail(e.target.value)}
                required placeholder="you@example.com"
                className="w-full px-4 py-2.5 bg-slate-900 border border-slate-600
                  rounded-lg text-white placeholder-slate-500
                  focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1">Password</label>
              <input
                type="password" value={password} onChange={e => setPassword(e.target.value)}
                required placeholder="••••••••"
                className="w-full px-4 py-2.5 bg-slate-900 border border-slate-600
                  rounded-lg text-white placeholder-slate-500
                  focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
              />
            </div>

            <button
              type="submit" disabled={loading}
              className="w-full py-2.5 px-4 bg-indigo-600 hover:bg-indigo-700
                disabled:opacity-50 disabled:cursor-not-allowed
                text-white font-semibold rounded-lg transition-colors"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <p className="text-center text-slate-400 text-sm mt-6">
            Don't have an account?{' '}
            <Link to="/register" className="text-indigo-400 hover:text-indigo-300 font-medium">
              Register
            </Link>
          </p>

          {/* Demo credentials */}
          <div className="mt-4 p-3 bg-slate-700/50 rounded-lg text-xs text-slate-400">
            <p className="font-medium mb-1">Demo credentials:</p>
            <p>admin@seads.com / password123</p>
            <p>user@seads.com  / password123</p>
          </div>
        </div>
      </div>
    </div>
  )
}
"""


def gen_items_route(idea: str) -> str:
    u = idea.lower()
    if any(w in u for w in ["shop","store","ecommerce"]):
        entity = "products"
    elif any(w in u for w in ["booking","hotel"]):
        entity = "listings"
    elif any(w in u for w in ["social","post"]):
        entity = "posts"
    else:
        entity = "items"

    return f"""import express from 'express'
import {{ PrismaClient }} from '@prisma/client'
import {{ authenticate }} from '../middleware/auth.js'
import {{ z }} from 'zod'

const router = express.Router()
const prisma = new PrismaClient()

const createSchema = z.object({{
  title:       z.string().min(1).max(200),
  description: z.string().optional(),
  status:      z.enum(['active','inactive','draft']).optional(),
  priority:    z.enum(['low','medium','high']).optional(),
}})

// GET /api/{entity} — List all (with pagination + search)
router.get('/', authenticate, async (req, res) => {{
  try {{
    const {{ page=1, limit=20, search='', status }} = req.query
    const skip = (Number(page)-1) * Number(limit)

    const where = {{
      userId: req.user.userId,
      ...(search && {{ title: {{ contains: search }} }}),
      ...(status && {{ status }}),
    }}

    const [items, total] = await Promise.all([
      prisma.item.findMany({{ where, skip, take: Number(limit),
        orderBy: {{ createdAt: 'desc' }} }}),
      prisma.item.count({{ where }}),
    ])

    res.json({{ items, total, page: Number(page),
               pages: Math.ceil(total / Number(limit)) }})
  }} catch (err) {{
    res.status(500).json({{ error: 'Failed to fetch {entity}' }})
  }}
}})

// GET /api/{entity}/:id
router.get('/:id', authenticate, async (req, res) => {{
  try {{
    const item = await prisma.item.findFirst({{
      where: {{ id: req.params.id, userId: req.user.userId }},
    }})
    if (!item) return res.status(404).json({{ error: 'Not found' }})
    res.json({{ item }})
  }} catch (err) {{
    res.status(500).json({{ error: 'Failed to fetch item' }})
  }}
}})

// POST /api/{entity}
router.post('/', authenticate, async (req, res) => {{
  try {{
    const data = createSchema.parse(req.body)
    const item = await prisma.item.create({{
      data: {{ ...data, userId: req.user.userId }},
    }})
    res.status(201).json({{ item, message: 'Created successfully' }})
  }} catch (err) {{
    if (err.name === 'ZodError') return res.status(400).json({{ error: err.errors }})
    res.status(500).json({{ error: 'Failed to create' }})
  }}
}})

// PUT /api/{entity}/:id
router.put('/:id', authenticate, async (req, res) => {{
  try {{
    const existing = await prisma.item.findFirst({{
      where: {{ id: req.params.id, userId: req.user.userId }},
    }})
    if (!existing) return res.status(404).json({{ error: 'Not found' }})

    const data = createSchema.partial().parse(req.body)
    const item = await prisma.item.update({{
      where: {{ id: req.params.id }}, data,
    }})
    res.json({{ item, message: 'Updated successfully' }})
  }} catch (err) {{
    if (err.name === 'ZodError') return res.status(400).json({{ error: err.errors }})
    res.status(500).json({{ error: 'Failed to update' }})
  }}
}})

// DELETE /api/{entity}/:id
router.delete('/:id', authenticate, async (req, res) => {{
  try {{
    const existing = await prisma.item.findFirst({{
      where: {{ id: req.params.id, userId: req.user.userId }},
    }})
    if (!existing) return res.status(404).json({{ error: 'Not found' }})
    await prisma.item.delete({{ where: {{ id: req.params.id }} }})
    res.json({{ message: 'Deleted successfully' }})
  }} catch (err) {{
    res.status(500).json({{ error: 'Failed to delete' }})
  }}
}})

export default router
"""


def gen_users_route() -> str:
    return """import express from 'express'
import { PrismaClient } from '@prisma/client'
import { authenticate, authorize } from '../middleware/auth.js'
import bcrypt from 'bcryptjs'

const router = express.Router()
const prisma = new PrismaClient()

// GET /api/users/profile
router.get('/profile', authenticate, async (req, res) => {
  try {
    const user = await prisma.user.findUnique({
      where:  { id: req.user.userId },
      select: { id: true, name: true, email: true, role: true, createdAt: true },
    })
    if (!user) return res.status(404).json({ error: 'User not found' })
    res.json({ user })
  } catch { res.status(500).json({ error: 'Failed to get profile' }) }
})

// PUT /api/users/profile
router.put('/profile', authenticate, async (req, res) => {
  try {
    const { name } = req.body
    const user = await prisma.user.update({
      where:  { id: req.user.userId },
      data:   { name },
      select: { id: true, name: true, email: true, role: true },
    })
    res.json({ user, message: 'Profile updated' })
  } catch { res.status(500).json({ error: 'Failed to update profile' }) }
})

// PUT /api/users/password
router.put('/password', authenticate, async (req, res) => {
  try {
    const { currentPassword, newPassword } = req.body
    const user = await prisma.user.findUnique({ where: { id: req.user.userId } })
    const valid = await bcrypt.compare(currentPassword, user.password)
    if (!valid) return res.status(400).json({ error: 'Current password is incorrect' })
    const hashed = await bcrypt.hash(newPassword, 12)
    await prisma.user.update({ where: { id: req.user.userId }, data: { password: hashed } })
    res.json({ message: 'Password updated successfully' })
  } catch { res.status(500).json({ error: 'Failed to update password' }) }
})

export default router
"""


def gen_gitignore() -> str:
    return """node_modules/
dist/
.env
.env.local
*.db
prisma/migrations/
.DS_Store
*.log
"""


# ─────────────────────────────────────────────────────────────
# MAIN BUILD FUNCTION
# ─────────────────────────────────────────────────────────────

def build_project(idea: str, answers: dict) -> dict:
    """
    Builds complete multi-file project in E:\seads\online_app\<name>
    Returns: {success, project_dir, files_created, elapsed}
    """
    name = idea.replace(" ","_").title()[:25].replace("_"," ")
    slug = re.sub(r'[^a-z0-9-]','', idea.replace(" ","-").lower())[:30]

    project_dir = OUTPUT_DIR / slug
    log.info(f"\n{'='*55}")
    log.info(f"🏗️  Building: {name}")
    log.info(f"📁 Output:   {project_dir}")
    log.info(f"{'='*55}")

    start        = time.time()
    files_created = []
    stack        = choose_stack(idea, answers)

    # Create folder structure
    dirs = [
        project_dir / "frontend" / "src" / "pages",
        project_dir / "frontend" / "src" / "components",
        project_dir / "frontend" / "src" / "hooks",
        project_dir / "frontend" / "src" / "store",
        project_dir / "frontend" / "src" / "lib",
        project_dir / "frontend" / "public",
        project_dir / "backend"  / "src" / "routes",
        project_dir / "backend"  / "src" / "middleware",
        project_dir / "backend"  / "src" / "controllers",
        project_dir / "backend"  / "prisma",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # ── PHASE 1: Static files (no LLM) ──────────────────────
    log.info("\n⚡ Phase 1: Static files...")

    static_files = {
        # Frontend
        project_dir / "frontend" / "package.json":        gen_package_json_frontend(name, stack),
        project_dir / "frontend" / "vite.config.js":      gen_vite_config(),
        project_dir / "frontend" / "tailwind.config.js":  gen_tailwind_config(),
        project_dir / "frontend" / "postcss.config.js":   "export default { plugins: { tailwindcss: {}, autoprefixer: {} } }\n",
        project_dir / "frontend" / "index.html":          gen_index_html(name),
        project_dir / "frontend" / "src" / "main.jsx":    gen_main_jsx(),
        project_dir / "frontend" / "src" / "index.css":   gen_index_css(),
        project_dir / "frontend" / "src" / "lib" / "utils.js": gen_lib_utils(),
        project_dir / "frontend" / "src" / "lib" / "api.js":   gen_api_client(),
        project_dir / "frontend" / "src" / "store" / "authStore.js": gen_auth_store(),
        project_dir / "frontend" / ".gitignore":          gen_gitignore(),
        # Backend
        project_dir / "backend" / "package.json":         gen_package_json_backend(name, stack),
        project_dir / "backend" / ".env":                 gen_backend_env(name, stack),
        project_dir / "backend" / "src" / "server.js":   gen_server_js(name, stack),
        project_dir / "backend" / "src" / "middleware" / "auth.js": gen_auth_middleware(),
        project_dir / "backend" / "src" / "routes" / "auth.js":    gen_auth_routes(),
        project_dir / "backend" / "src" / "routes" / "items.js":   gen_items_route(idea),
        project_dir / "backend" / "src" / "routes" / "users.js":   gen_users_route(),
        project_dir / "backend" / "prisma" / "schema.prisma":      gen_prisma_schema(idea),
        project_dir / "backend" / "prisma" / "seed.js":            gen_seed_js(idea),
        project_dir / "backend" / ".gitignore":           gen_gitignore(),
        # Root
        project_dir / "README.md":                        gen_readme(name, stack),
    }

    for path, content in static_files.items():
        write_file(path, content)
        files_created.append(str(path.relative_to(project_dir)))

    # ── PHASE 2: LLM-generated React pages ──────────────────
    log.info("\n⚡ Phase 2: LLM-generated React pages (parallel)...")

    def gen_and_write(args):
        filepath, gen_fn, gen_args = args
        content = gen_fn(*gen_args)
        if content and len(content) > 100:
            write_file(filepath, content)
            files_created.append(str(filepath.relative_to(project_dir)))
            return True
        return False

    llm_tasks = [
        (project_dir/"frontend"/"src"/"App.jsx",
         gen_app_jsx, [name, idea, answers]),
        (project_dir/"frontend"/"src"/"pages"/"HomePage.jsx",
         gen_home_page, [name, idea, answers]),
        (project_dir/"frontend"/"src"/"pages"/"DashboardPage.jsx",
         gen_dashboard_page, [name, idea, answers]),
    ]

    # LoginPage (prebuilt, no LLM)
    write_file(project_dir/"frontend"/"src"/"pages"/"LoginPage.jsx", gen_login_page())
    files_created.append("frontend/src/pages/LoginPage.jsx")

    # Run LLM tasks in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        list(ex.map(gen_and_write, llm_tasks))

    # ── PHASE 3: Start script ────────────────────────────────
    start_script = f"""@echo off
echo Starting {name}...
echo.
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:3001
echo.

start "Backend" cmd /k "cd backend && npm install && npx prisma generate && npx prisma migrate dev --name init && node prisma/seed.js && npm run dev"
timeout /t 3 /nobreak > nul
start "Frontend" cmd /k "cd frontend && npm install && npm run dev"

echo.
echo Both servers starting...
echo Open http://localhost:5173 in your browser
pause
"""
    write_file(project_dir / "start.bat", start_script)
    files_created.append("start.bat")

    # Makefile for Linux/Mac
    makefile = f"""dev:
\t@echo "Starting {name}..."
\t@cd backend && npm install && npx prisma generate && npx prisma migrate dev --name init && npm run dev &
\t@cd frontend && npm install && npm run dev

install:
\t@cd backend  && npm install
\t@cd frontend && npm install

migrate:
\t@cd backend && npx prisma migrate dev

seed:
\t@cd backend && node prisma/seed.js

.PHONY: dev install migrate seed
"""
    write_file(project_dir / "Makefile", makefile)
    files_created.append("Makefile")

    elapsed = round(time.time()-start, 1)
    log.info(f"\n✅ Project built: {len(files_created)} files in {elapsed}s")
    log.info(f"📁 Location: {project_dir}")

    return {
        "success":       True,
        "project_dir":   str(project_dir),
        "files_created": files_created,
        "file_count":    len(files_created),
        "elapsed":       elapsed,
        "stack":         stack,
        "start_command": f"cd {project_dir} && start.bat",
    }

import re
