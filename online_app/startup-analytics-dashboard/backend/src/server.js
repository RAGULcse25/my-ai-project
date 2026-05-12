import express from 'express'
import cors from 'cors'
import helmet from 'helmet'
import morgan from 'morgan'
import dotenv from 'dotenv'



import authRoutes from './routes/auth.js'
import itemRoutes from './routes/items.js'
import userRoutes from './routes/users.js'

dotenv.config()

const app  = express()

const PORT = process.env.PORT || 3001

// ── Security Middleware ────────────────────────────────────
app.use(helmet())
app.use(cors({
  origin:      process.env.FRONTEND_URL || 'http://localhost:5173',
  credentials: true,
  methods:     ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}))
app.use(morgan('dev'))
app.use(express.json({ limit: '10mb' }))
app.use(express.urlencoded({ extended: true }))

// ── Routes ────────────────────────────────────────────────
app.use('/api/auth',  authRoutes)
app.use('/api/items', itemRoutes)
app.use('/api/users', userRoutes)

// ── Health Check ──────────────────────────────────────────
app.get('/api/health', (req, res) => {
  res.json({
    status:    'ok',
    app:       'Startup Analytics Dashboa',
    version:   '1.0.0',
    timestamp: new Date().toISOString(),
  })
})








// ── Error Handler ─────────────────────────────────────────
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(err.status || 500).json({
    error:   err.message || 'Internal Server Error',
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
  })
})

// ── 404 Handler ───────────────────────────────────────────
app.use((req, res) => {
  res.status(404).json({ error: `Route ${req.method} ${req.url} not found` })
})

// ── Start ─────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`✅ Startup Analytics Dashboa backend running on http://localhost:${PORT}`)
  console.log(`   Environment: ${process.env.NODE_ENV || 'development'}`)
})

export { app }
