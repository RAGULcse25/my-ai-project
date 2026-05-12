dev:
	@echo "Starting Startup Analytics Dashboa..."
	@cd backend && npm install && npx prisma generate && npx prisma migrate dev --name init && npm run dev &
	@cd frontend && npm install && npm run dev

install:
	@cd backend  && npm install
	@cd frontend && npm install

migrate:
	@cd backend && npx prisma migrate dev

seed:
	@cd backend && node prisma/seed.js

.PHONY: dev install migrate seed
