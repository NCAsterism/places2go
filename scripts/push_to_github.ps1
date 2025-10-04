#!/usr/bin/env pwsh
# Push Places2Go to GitHub (ncasterism/places2go)
# This script will help you push the repository after it's created on GitHub

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Places2Go - GitHub Push Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if repository exists on GitHub
Write-Host "Checking if repository exists on GitHub..." -ForegroundColor Yellow
$response = gh repo view ncasterism/places2go 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Repository exists on GitHub!" -ForegroundColor Green
} else {
    Write-Host "✗ Repository not found on GitHub" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please create the repository first:" -ForegroundColor Yellow
    Write-Host "  Option 1: gh repo create ncasterism/places2go --public --source=. --remote=origin --push" -ForegroundColor White
    Write-Host "  Option 2: Create manually at https://github.com/new" -ForegroundColor White
    Write-Host ""
    exit 1
}

# Push main branch
Write-Host ""
Write-Host "Pushing main branch..." -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Main branch pushed successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to push main branch" -ForegroundColor Red
    exit 1
}

# Push develop branch
Write-Host ""
Write-Host "Pushing develop branch..." -ForegroundColor Yellow
git push -u origin develop

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Develop branch pushed successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to push develop branch" -ForegroundColor Red
    exit 1
}

# Summary
Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "✓ SUCCESS!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "Repository pushed to: https://github.com/ncasterism/places2go" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Set develop as default branch (optional)" -ForegroundColor White
Write-Host "  2. Create labels and milestones" -ForegroundColor White
Write-Host "  3. Create GitHub issues: python scripts/create_issues.py" -ForegroundColor White
Write-Host "  4. Set up GitHub Project board" -ForegroundColor White
Write-Host ""
Write-Host "See READY_TO_PUSH.md for detailed instructions" -ForegroundColor Cyan
