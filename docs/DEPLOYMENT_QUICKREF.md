# Deployment Quick Reference

Quick command reference for deploying Places2Go.

## Prerequisites Checklist

- [ ] Azure account created
- [ ] GitHub repository access
- [ ] Azure CLI installed (optional)

## Initial Setup (One-Time)

### 1. Create Azure Static Web App

**Option A: Azure Portal** (Easiest)
```
1. Go to portal.azure.com
2. Search "Static Web Apps"
3. Click "Create"
4. Fill form:
   - Name: places2go
   - Plan: Free
   - Source: GitHub
   - Repo: places2go
   - Branch: main
   - App location: /deployment
5. Review + Create
```

**Option B: Azure CLI**
```bash
az staticwebapp create \
  --name places2go \
  --resource-group places2go-rg \
  --source https://github.com/YOUR_USERNAME/places2go \
  --location eastus \
  --branch main \
  --app-location "/deployment"
```

### 2. Add GitHub Secret

```bash
# Get deployment token from Azure Portal
# Go to: Static Web App → Overview → Manage deployment token

# Add to GitHub:
# Settings → Secrets → Actions → New secret
# Name: AZURE_STATIC_WEB_APPS_API_TOKEN
# Value: [paste token]
```

## Deploy to Production

```bash
# Merge to main branch
git checkout main
git merge develop
git push origin main

# GitHub Actions will automatically:
# 1. Run tests
# 2. Build visualizations
# 3. Deploy to Azure
# 4. Run health checks
```

## Create Preview Environment

```bash
# Open PR to main
gh pr create --base main --head feature-branch

# Preview URL will be posted in PR comments
# Format: https://staging-xxx.azurestaticapps.net
```

## Manual Deployment

```bash
# Trigger workflow manually
gh workflow run deploy.yml

# Or via GitHub UI:
# Actions → Deploy to Azure → Run workflow
```

## Monitor Deployment

```bash
# Check workflow status
gh run list --workflow=deploy.yml

# View specific run
gh run view <run-id>

# Watch logs in real-time
gh run watch
```

## Rollback

### Quick Rollback (Emergency)

```bash
# Method 1: Git revert (recommended)
git revert HEAD
git push origin main

# Method 2: Azure Portal
# portal.azure.com → Static Web App → Deployment History
# Select previous deployment → Redeploy
```

### Verify Rollback

```bash
# Check site is loading
curl -I https://places2go.azurestaticapps.net

# Check for errors
curl https://places2go.azurestaticapps.net | grep -i error
```

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run tests
pytest

# Generate visualizations
python -m scripts.visualizations.destinations_map
python -m scripts.visualizations.cost_comparison
python -m scripts.visualizations.flight_prices
python -m scripts.visualizations.weather_forecast

# Check output
ls -lh .build/visualizations/
```

## Monitoring

### Application Insights

```bash
# Create Application Insights
az monitor app-insights component create \
  --app places2go-insights \
  --location eastus \
  --resource-group places2go-rg

# Get connection string
az monitor app-insights component show \
  --app places2go-insights \
  --resource-group places2go-rg \
  --query "connectionString" -o tsv

# Add to GitHub Secrets:
# Name: APPLICATIONINSIGHTS_CONNECTION_STRING
```

### Check Uptime

```bash
# Manual check
curl -I https://places2go.azurestaticapps.net

# Expected: HTTP/2 200

# Check all pages
for page in index destinations_map flight_prices cost_comparison weather_forecast; do
  echo "Checking $page.html..."
  curl -I "https://places2go.azurestaticapps.net/$page.html" | head -1
done
```

## Troubleshooting

### Deployment Fails

```bash
# Check workflow logs
gh run list --workflow=deploy.yml --limit 5
gh run view <run-id> --log

# Check test failures
pytest -v

# Check formatting
black --check scripts tests
flake8 scripts tests
```

### Site Not Loading

```bash
# 1. Check Azure status
az staticwebapp show \
  --name places2go \
  --resource-group places2go-rg \
  --query "defaultHostname"

# 2. Check deployment status
gh run list --workflow=deploy.yml --limit 1

# 3. Check browser console (F12)
# Look for JavaScript errors
```

### Missing Visualizations

```bash
# Regenerate locally
python -m scripts.visualizations.destinations_map
python -m scripts.visualizations.cost_comparison
python -m scripts.visualizations.flight_prices
python -m scripts.visualizations.weather_forecast

# Check they were created
ls -lh .build/visualizations/

# Push to trigger redeploy
git add .build/visualizations/
git commit -m "Regenerate visualizations"
git push
```

## Common Commands

```bash
# Check Azure resources
az staticwebapp list --resource-group places2go-rg -o table

# Get deployment URL
az staticwebapp show \
  --name places2go \
  --resource-group places2go-rg \
  --query "defaultHostname" -o tsv

# List deployments
az staticwebapp deployment list \
  --name places2go \
  --resource-group places2go-rg -o table

# Delete Static Web App (if needed)
az staticwebapp delete \
  --name places2go \
  --resource-group places2go-rg
```

## Environment URLs

| Environment | URL | Branch |
|-------------|-----|--------|
| Local | http://localhost:8000 | develop |
| Preview | https://staging-*.azurestaticapps.net | PR to main |
| Production | https://places2go.azurestaticapps.net | main |

## Support

- 📚 [Full Deployment Guide](../DEPLOYMENT.md)
- 🔄 [Rollback Procedures](../ROLLBACK.md)
- 📊 [Monitoring Setup](../MONITORING.md)
- 🐛 [GitHub Issues](https://github.com/NCAsterism/places2go/issues)

## Quick Links

- Azure Portal: https://portal.azure.com
- GitHub Actions: https://github.com/NCAsterism/places2go/actions
- Application Insights: https://portal.azure.com → Application Insights
- Static Web Apps Docs: https://docs.microsoft.com/azure/static-web-apps/

---

**Last Updated**: October 2024
**Version**: 1.0
