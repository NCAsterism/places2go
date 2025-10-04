# Push Wiki Pages to GitHub
# This script pushes wiki markdown files to the GitHub wiki repository
# PREREQUISITE: Create the first wiki page via GitHub UI to initialize wiki.git

$ErrorActionPreference = "Stop"

Write-Host "`n🌍 Places2Go Wiki Publisher" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray

# Check if we're in the right directory
if (-not (Test-Path "wiki")) {
    Write-Host "❌ Error: wiki directory not found!" -ForegroundColor Red
    Write-Host "   Run this script from the project root directory." -ForegroundColor Yellow
    exit 1
}

# Check if wiki.git is cloned
$wikiPath = "..\places2go.wiki"
if (-not (Test-Path $wikiPath)) {
    Write-Host "`n📥 Cloning wiki repository..." -ForegroundColor Yellow
    
    try {
        Set-Location ..
        git clone https://github.com/NCAsterism/places2go.wiki.git
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "`n⚠️  Wiki repository not available yet!" -ForegroundColor Yellow
            Write-Host "`nThe wiki.git repository is created after you create the first page via GitHub UI." -ForegroundColor Cyan
            Write-Host "`nSteps to initialize wiki:" -ForegroundColor White
            Write-Host "  1. Go to: https://github.com/NCAsterism/places2go/wiki" -ForegroundColor Gray
            Write-Host "  2. Click 'Create the first page'" -ForegroundColor Gray
            Write-Host "  3. Add any content (e.g., 'Initial page')" -ForegroundColor Gray
            Write-Host "  4. Click 'Save Page'" -ForegroundColor Gray
            Write-Host "  5. Run this script again" -ForegroundColor Gray
            Write-Host "`nAlternatively, I've created all wiki content in the 'wiki/' folder." -ForegroundColor Cyan
            Write-Host "You can manually copy-paste the content to GitHub wiki pages." -ForegroundColor Cyan
            Set-Location places2go
            exit 1
        }
        
        Set-Location places2go
    }
    catch {
        Write-Host "❌ Failed to clone wiki: $_" -ForegroundColor Red
        Set-Location places2go
        exit 1
    }
}

Write-Host "`n📄 Copying wiki pages..." -ForegroundColor Yellow

# Copy all markdown files from wiki/ to wiki repository
$wikiFiles = Get-ChildItem -Path "wiki\*.md"
$copiedCount = 0

foreach ($file in $wikiFiles) {
    $destPath = Join-Path $wikiPath $file.Name
    Copy-Item -Path $file.FullName -Destination $destPath -Force
    Write-Host "  ✓ Copied: $($file.Name)" -ForegroundColor Green
    $copiedCount++
}

Write-Host "`n📝 Committing changes..." -ForegroundColor Yellow

# Commit and push
Set-Location $wikiPath

git add .
$commitMessage = "docs: add comprehensive wiki documentation

- Home page with navigation
- Installation guide
- Quick start guide
- Development guide
- Contributing guidelines
- Architecture overview

Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"

git commit -m $commitMessage

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Changes committed" -ForegroundColor Green
    
    Write-Host "`n🚀 Pushing to GitHub..." -ForegroundColor Yellow
    git push origin master
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ Wiki published successfully!" -ForegroundColor Green
        Write-Host "`n📖 View wiki at: https://github.com/NCAsterism/places2go/wiki" -ForegroundColor Cyan
        Write-Host "`nPublished pages:" -ForegroundColor White
        foreach ($file in $wikiFiles) {
            $pageName = $file.BaseName
            Write-Host "  • $pageName" -ForegroundColor Gray
        }
    }
    else {
        Write-Host "❌ Failed to push changes" -ForegroundColor Red
    }
}
else {
    Write-Host "  ℹ️  No changes to commit (wiki already up-to-date)" -ForegroundColor Cyan
}

Set-Location ..\places2go

Write-Host "`n✨ Done!" -ForegroundColor Green
