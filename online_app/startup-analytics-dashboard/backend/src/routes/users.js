import express from 'express'
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
