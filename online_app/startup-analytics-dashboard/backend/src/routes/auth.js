import express from 'express'
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
