# DB-GPT Setup Script (Windows PowerShell)
Write-Host "=== DB-GPT Local AI Data Assistant Setup ===" -ForegroundColor Cyan

# 1. Check prerequisites
$hasPython = Get-Command python -ErrorAction SilentlyContinue
$hasNode = Get-Command node -ErrorAction SilentlyContinue
$hasDocker = Get-Command docker -ErrorAction SilentlyContinue

if (-not $hasPython) { Write-Host "ERROR: Python 3.12+ is required" -ForegroundColor Red; exit 1 }
if (-not $hasNode) { Write-Host "ERROR: Node.js 20+ is required" -ForegroundColor Red; exit 1 }

Write-Host "[1/5] Setting up environment..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example - please edit with your API keys" -ForegroundColor Green
}

# 2. Setup backend
Write-Host "[2/5] Setting up Python backend..." -ForegroundColor Yellow
Set-Location backend
python -m venv venv
if ($IsWindows) {
    .\venv\Scripts\pip install -r requirements.txt
} else {
    ./venv/bin/pip install -r requirements.txt
}
Set-Location ..

# 3. Setup frontend
Write-Host "[3/5] Setting up Next.js frontend..." -ForegroundColor Yellow
Set-Location frontend
npm install
Set-Location ..

# 4. Database
Write-Host "[4/5] Database setup..." -ForegroundColor Yellow
if ($hasDocker) {
    docker compose up -d db
    Write-Host "PostgreSQL started via Docker" -ForegroundColor Green
} else {
    Write-Host "WARNING: Docker not found. Please ensure PostgreSQL is running on localhost:5432" -ForegroundColor Yellow
}

Write-Host "[5/5] Running migrations..." -ForegroundColor Yellow
Set-Location backend
.\venv\Scripts\alembic upgrade head
Set-Location ..

Write-Host ""
Write-Host "=== Setup Complete! ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Start the backend:" -ForegroundColor Green
Write-Host "  cd backend && .\venv\Scripts\uvicorn app.main:app --reload --port 8000"
Write-Host ""
Write-Host "Start the frontend:" -ForegroundColor Green
Write-Host "  cd frontend && npm run dev"
Write-Host ""
Write-Host "Open http://localhost:3000 in your browser" -ForegroundColor Green
Write-Host ""
Write-Host "Default login (if seeded):" -ForegroundColor Yellow
Write-Host "  Email: mzoraofficila@gmail.com"
Write-Host "  Password: zabi12345"
