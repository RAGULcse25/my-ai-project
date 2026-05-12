import express from 'express'
import { PrismaClient } from '@prisma/client'
import { authenticate } from '../middleware/auth.js'
import { z } from 'zod'

const router = express.Router()
const prisma = new PrismaClient()

const createSchema = z.object({
  title:       z.string().min(1).max(200),
  description: z.string().optional(),
  status:      z.enum(['active','inactive','draft']).optional(),
  priority:    z.enum(['low','medium','high']).optional(),
})

// GET /api/items — List all (with pagination + search)
router.get('/', authenticate, async (req, res) => {
  try {
    const { page=1, limit=20, search='', status } = req.query
    const skip = (Number(page)-1) * Number(limit)

    const where = {
      userId: req.user.userId,
      ...(search && { title: { contains: search } }),
      ...(status && { status }),
    }

    const [items, total] = await Promise.all([
      prisma.item.findMany({ where, skip, take: Number(limit),
        orderBy: { createdAt: 'desc' } }),
      prisma.item.count({ where }),
    ])

    res.json({ items, total, page: Number(page),
               pages: Math.ceil(total / Number(limit)) })
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch items' })
  }
})

// GET /api/items/:id
router.get('/:id', authenticate, async (req, res) => {
  try {
    const item = await prisma.item.findFirst({
      where: { id: req.params.id, userId: req.user.userId },
    })
    if (!item) return res.status(404).json({ error: 'Not found' })
    res.json({ item })
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch item' })
  }
})

// POST /api/items
router.post('/', authenticate, async (req, res) => {
  try {
    const data = createSchema.parse(req.body)
    const item = await prisma.item.create({
      data: { ...data, userId: req.user.userId },
    })
    res.status(201).json({ item, message: 'Created successfully' })
  } catch (err) {
    if (err.name === 'ZodError') return res.status(400).json({ error: err.errors })
    res.status(500).json({ error: 'Failed to create' })
  }
})

// PUT /api/items/:id
router.put('/:id', authenticate, async (req, res) => {
  try {
    const existing = await prisma.item.findFirst({
      where: { id: req.params.id, userId: req.user.userId },
    })
    if (!existing) return res.status(404).json({ error: 'Not found' })

    const data = createSchema.partial().parse(req.body)
    const item = await prisma.item.update({
      where: { id: req.params.id }, data,
    })
    res.json({ item, message: 'Updated successfully' })
  } catch (err) {
    if (err.name === 'ZodError') return res.status(400).json({ error: err.errors })
    res.status(500).json({ error: 'Failed to update' })
  }
})

// DELETE /api/items/:id
router.delete('/:id', authenticate, async (req, res) => {
  try {
    const existing = await prisma.item.findFirst({
      where: { id: req.params.id, userId: req.user.userId },
    })
    if (!existing) return res.status(404).json({ error: 'Not found' })
    await prisma.item.delete({ where: { id: req.params.id } })
    res.json({ message: 'Deleted successfully' })
  } catch (err) {
    res.status(500).json({ error: 'Failed to delete' })
  }
})

export default router
