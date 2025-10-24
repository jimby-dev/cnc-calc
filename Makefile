# CNC Calculator Makefile
# Universal commands that work on Linux, macOS, and Windows with WSL

.PHONY: help setup dev build test clean container-install db-up db-seed docker-up docker-down deploy-dev deploy-staging deploy-prod infra-up lint format type-check security-scan status

# Default target
help: ## Show all available commands
	@echo "CNC Calculator - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Setup & Development
setup: ## Complete project setup (check prereqs, install deps, configure)
	@echo "🚀 Setting up CNC Calculator..."
	@$(MAKE) check-prereqs
	@$(MAKE) install-deps
	@$(MAKE) configure-env
	@echo "✅ Setup complete! Run 'make dev' to start development."

check-prereqs: ## Check system prerequisites
	@echo "🔍 Checking prerequisites..."
	@command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed. Please install Node.js 18+"; exit 1; }
	@command -v npm >/dev/null 2>&1 || { echo "❌ npm is required but not installed."; exit 1; }
	@command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed."; exit 1; }
	@command -v docker >/dev/null 2>&1 || command -v podman >/dev/null 2>&1 || { echo "⚠️  Docker/Podman not found. Run 'make container-install' if needed."; }
	@echo "✅ Prerequisites check passed"

install-deps: ## Install all dependencies
	@echo "📦 Installing dependencies..."
	npm install
	cd frontend && npm install
	cd backend && python3.11 -m venv .venv && .venv/bin/pip install -r requirements.txt
	@echo "✅ Dependencies installed"

configure-env: ## Configure environment files
	@echo "⚙️  Configuring environment..."
	@if [ ! -f .env ]; then cp .env.example .env; fi
	@if [ ! -f frontend/.env.local ]; then cp frontend/.env.example frontend/.env.local; fi
	@if [ ! -f backend/.env ]; then cp backend/.env.example backend/.env; fi
	@echo "✅ Environment configured"

dev: ## Start full development environment
	@echo "🔥 Starting development environment..."
	npm run dev

build: ## Build both frontend and backend
	@echo "🔨 Building applications..."
	npm run build

test: ## Run all tests
	@echo "🧪 Running tests..."
	npm run test

clean: ## Clean all build artifacts
	@echo "🧹 Cleaning build artifacts..."
	npm run clean
	rm -rf node_modules/.cache
	rm -rf .next
	rm -rf dist
	rm -rf build
	@echo "✅ Clean complete"

# Container Management
container-install: ## Install container tool (Docker on Linux, Apple Container on macOS)
	@echo "🐳 Installing container tool..."
	@if [[ "$$OSTYPE" == "darwin"* ]]; then \
		echo "🍎 macOS detected - installing Apple Container tool..."; \
		brew install apple/container/container; \
	elif [[ "$$OSTYPE" == "linux-gnu"* ]]; then \
		echo "🐧 Linux detected - installing Docker..."; \
		sudo apt-get update && sudo apt-get install -y docker.io; \
		sudo systemctl start docker; \
		sudo systemctl enable docker; \
		sudo usermod -aG docker $$USER; \
		echo "⚠️  Please log out and back in for Docker group changes to take effect"; \
	else \
		echo "❌ Unsupported OS. Please install Docker manually."; \
	fi

# Database & Services
db-up: ## Start local database
	@echo "🗄️  Starting database..."
	docker-compose up -d postgres redis

db-seed: ## Seed database with sample data
	@echo "🌱 Seeding database..."
	cd backend && python scripts/seed_database.py

docker-up: ## Start all services (auto-detects: Docker on Linux, Apple Container on macOS)
	@echo "🐳 Starting all services..."
	@if command -v docker >/dev/null 2>&1; then \
		docker-compose up -d; \
	elif command -v podman >/dev/null 2>&1; then \
		podman-compose up -d; \
	else \
		echo "❌ No container runtime found. Run 'make container-install' first."; \
		exit 1; \
	fi

docker-down: ## Stop all services
	@echo "🛑 Stopping all services..."
	@if command -v docker >/dev/null 2>&1; then \
		docker-compose down; \
	elif command -v podman >/dev/null 2>&1; then \
		podman-compose down; \
	fi

# Deployment
deploy-dev: ## Deploy to development
	@echo "🚀 Deploying to development..."
	npm run deploy:infra
	npm run deploy:backend
	npm run deploy:frontend

deploy-staging: ## Deploy to staging
	@echo "🚀 Deploying to staging..."
	@echo "⚠️  Staging deployment not yet configured"

deploy-prod: ## Deploy to production
	@echo "🚀 Deploying to production..."
	@echo "⚠️  Production deployment not yet configured"

infra-up: ## Deploy infrastructure
	@echo "🏗️  Deploying infrastructure..."
	cd infra && npm run deploy

# Code Quality
lint: ## Lint all code
	@echo "🔍 Linting code..."
	npm run lint

format: ## Format all code
	@echo "✨ Formatting code..."
	npm run format

type-check: ## Type checking
	@echo "🔍 Type checking..."
	cd frontend && npm run type-check
	cd backend && .venv/bin/python -m mypy .

security-scan: ## Security vulnerability scan
	@echo "🔒 Running security scan..."
	@if command -v trivy >/dev/null 2>&1; then \
		trivy fs .; \
	else \
		echo "⚠️  Trivy not installed. Install with: brew install trivy"; \
	fi

# Status & Health
status: ## Show project status and health
	@echo "📊 Project Status:"
	@echo ""
	@echo "📁 Project Structure:"
	@ls -la | grep -E '^d' | awk '{print "  📂 " $$9}'
	@echo ""
	@echo "🐳 Container Status:"
	@if command -v docker >/dev/null 2>&1; then \
		docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(cnc|postgres|redis)" || echo "  No containers running"; \
	fi
	@echo ""
	@echo "🌐 Service URLs:"
	@echo "  Frontend: http://localhost:3000"
	@echo "  Backend:  http://localhost:8000"
	@echo "  Database: localhost:5432"
	@echo "  Redis:    localhost:6379"
