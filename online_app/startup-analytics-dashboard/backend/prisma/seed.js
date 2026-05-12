import { PrismaClient } from '@prisma/client'
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
