# Deployment Guide

This guide covers deploying the Places2Go dashboard to Azure Static Web Apps with automated CI/CD.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Azure Setup](#azure-setup)
3. [GitHub Configuration](#github-configuration)
4. [Deployment Process](#deployment-process)
5. [Monitoring & Analytics](#monitoring--analytics)
6. [Rollback Procedures](#rollback-procedures)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

- GitHub account with repository access
- Azure account (free tier available)
- Azure CLI installed (optional, for manual setup)
- Git installed locally

## Azure Setup

### 1. Create Azure Static Web App

#### Option A: Using Azure Portal (Recommended for First-Time Setup)

1. **Sign in to Azure Portal**
   - Go to https://portal.azure.com
   - Create a free account if you don't have one

2. **Create Static Web App**
   - Search for "Static Web Apps" in the search bar
   - Click "Create"
   - Fill in the details:
     - **Subscription**: Choose your subscription
     - **Resource Group**: Create new or use existing
     - **Name**: `places2go` (or your preferred name)
     - **Plan type**: Free
     - **Region**: Choose closest to your users
     - **Source**: GitHub
     - **Organization**: Your GitHub username/org
     - **Repository**: places2go
     - **Branch**: main
     - **Build Presets**: Custom
     - **App location**: `/deployment`
     - **Api location**: (leave empty)
     - **Output location**: (leave empty)

3. **Review and Create**
   - Click "Review + create"
   - Azure will create the resource and automatically:
     - Generate a deployment token
     - Add it to your GitHub repository secrets as `AZURE_STATIC_WEB_APPS_API_TOKEN`
     - Create a GitHub Actions workflow (you can replace it with ours)

#### Option B: Using Azure CLI

```bash
# Login to Azure
az login

# Create resource group
az group create --name places2go-rg --location eastus

# Create static web app
az staticwebapp create \
  --name places2go \
  --resource-group places2go-rg \
  --source https://github.com/YOUR_USERNAME/places2go \
  --location eastus \
  --branch main \
  --app-location "/deployment" \
  --output-location "" \
  --login-with-github

# Get deployment token
az staticwebapp secrets list \
  --name places2go \
  --resource-group places2go-rg \
  --query "properties.apiKey" -o tsv
```

### 2. Configure Application Insights (Optional but Recommended)

```bash
# Create Application Insights resource
az monitor app-insights component create \
  --app places2go-insights \
  --location eastus \
  --resource-group places2go-rg \
  --application-type web

# Get connection string
az monitor app-insights component show \
  --app places2go-insights \
  --resource-group places2go-rg \
  --query "connectionString" -o tsv
```

## GitHub Configuration

### 1. Add Repository Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add the following secrets:

| Secret Name | Description | Required |
|-------------|-------------|----------|
| `AZURE_STATIC_WEB_APPS_API_TOKEN` | Azure deployment token | ✅ Yes |
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | Application Insights connection | ⚠️ Recommended |
| `GOOGLE_ANALYTICS_ID` | Google Analytics tracking ID | ❌ Optional |

### 2. Verify Workflow File

Ensure `.github/workflows/deploy.yml` exists in your repository. This workflow:
- Runs on push to `main` branch
- Runs on pull requests to `main`
- Builds and tests the application
- Generates HTML visualizations
- Deploys to Azure Static Web Apps
- Creates preview environments for PRs

## Deployment Process

### Automatic Deployment

**Production Deployment:**
```bash
# Merge to main branch
git checkout main
git merge develop
git push origin main
```

The workflow will:
1. ✅ Run linting checks
2. ✅ Run all tests
3. ✅ Generate visualizations
4. ✅ Deploy to production
5. ✅ Run health checks

**Preview Deployment:**
- Open a pull request to `main`
- Azure automatically creates a preview environment
- Preview URL is posted as a comment on the PR
- Preview is destroyed when PR is closed

### Manual Deployment

If needed, trigger deployment manually:

1. Go to GitHub Actions tab
2. Select "Deploy to Azure Static Web Apps" workflow
3. Click "Run workflow"
4. Select branch and click "Run workflow"

## Monitoring & Analytics

### Application Insights

If configured, Application Insights automatically tracks:
- Page views and user sessions
- Load times and performance metrics
- JavaScript errors
- Failed requests
- Custom events

**View metrics:**
1. Go to Azure Portal
2. Navigate to your Application Insights resource
3. Explore metrics in "Application Insights" blade

### Google Analytics

To enable Google Analytics:

1. **Create GA4 Property**
   - Go to https://analytics.google.com
   - Create new property
   - Get Measurement ID (G-XXXXXXXXXX)

2. **Add to GitHub Secrets**
   ```
   Secret name: GOOGLE_ANALYTICS_ID
   Value: G-XXXXXXXXXX
   ```

3. **Redeploy**
   - Push to main or manually trigger deployment

### Uptime Monitoring

Set up external monitoring with UptimeRobot (free tier):

1. Go to https://uptimerobot.com
2. Create free account
3. Add new monitor:
   - Type: HTTP(s)
   - URL: Your Azure Static Web App URL
   - Monitoring Interval: 5 minutes
4. Configure alert contacts (email, Slack, etc.)

## Rollback Procedures

### Automated Rollback

The deployment workflow includes health checks. If deployment fails:
- GitHub Actions workflow fails
- Previous version remains active
- Alerts are sent (if configured)

### Manual Rollback

#### Method 1: Revert to Previous Commit

```bash
# Find the commit to revert to
git log --oneline -10

# Revert to specific commit
git revert <commit-hash>
git push origin main
```

#### Method 2: Redeploy Previous Version

```bash
# Create rollback branch from previous good commit
git checkout <good-commit-hash>
git checkout -b rollback/emergency-fix
git push origin rollback/emergency-fix

# Open PR and merge to main
# Or force push to main (not recommended)
```

#### Method 3: Azure Portal

1. Go to Azure Portal
2. Navigate to your Static Web App
3. Go to "Deployment history"
4. Select previous successful deployment
5. Click "Redeploy"

### Rollback Verification

After rollback:
1. ✅ Check application URL loads correctly
2. ✅ Verify all visualizations display
3. ✅ Check Application Insights for errors
4. ✅ Monitor user feedback channels

## Troubleshooting

### Deployment Fails

**Check workflow logs:**
```bash
# Via GitHub CLI
gh run list --workflow=deploy.yml
gh run view <run-id> --log
```

**Common issues:**
- Missing secrets → Add to GitHub repository secrets
- Test failures → Fix tests locally, commit, and push
- Build errors → Check Python dependencies in requirements.txt

### Application Not Loading

1. **Check Azure Static Web App status**
   - Go to Azure Portal
   - Navigate to your Static Web App
   - Check "Overview" for status

2. **Verify deployment succeeded**
   - Check GitHub Actions for successful workflow run
   - Look for green checkmarks

3. **Check browser console**
   - Open browser developer tools (F12)
   - Look for JavaScript errors
   - Check Network tab for failed requests

### Missing Visualizations

```bash
# Regenerate locally
python -m scripts.visualizations.destinations_map
python -m scripts.visualizations.cost_comparison
python -m scripts.visualizations.flight_prices
python -m scripts.visualizations.weather_forecast

# Check output
ls -la .build/visualizations/

# Commit and push
git add .build/visualizations/
git commit -m "Regenerate visualizations"
git push
```

### Performance Issues

1. **Check Application Insights**
   - Look for slow page loads
   - Identify bottlenecks

2. **Optimize visualizations**
   - Reduce data points if needed
   - Enable caching in configuration

3. **Use CDN**
   - Azure Static Web Apps automatically uses Azure CDN
   - Verify CDN is enabled in Azure Portal

## Environment URLs

| Environment | URL | Branch | Auto-Deploy |
|-------------|-----|--------|-------------|
| Development | http://localhost:8000 | develop | No |
| Staging | https://staging-*.azurestaticapps.net | PR to main | Yes (preview) |
| Production | https://places2go.azurestaticapps.net | main | Yes |

## Success Metrics

Track these metrics to ensure successful deployment:

- ✅ Zero-downtime deployments
- ✅ < 5 minute deploy time
- ✅ 99.9% uptime
- ✅ Automated rollback on failures
- ✅ Monitoring alerts working

## Custom Domain (Optional)

To use a custom domain:

1. **Purchase domain** (from GoDaddy, Namecheap, etc.)

2. **Configure in Azure**
   ```bash
   az staticwebapp hostname set \
     --name places2go \
     --resource-group places2go-rg \
     --hostname www.yourdomain.com
   ```

3. **Update DNS records**
   - Add CNAME record pointing to your Azure Static Web App URL
   - Wait for DNS propagation (up to 48 hours)

4. **Enable HTTPS**
   - Azure automatically provisions SSL certificate
   - Takes 5-10 minutes after DNS propagation

## Support

For issues:
1. Check GitHub Issues: https://github.com/NCAsterism/places2go/issues
2. Review Azure Static Web Apps documentation
3. Contact repository maintainers

## Next Steps

After deployment:
- [ ] Set up monitoring alerts
- [ ] Configure custom domain (optional)
- [ ] Add more visualizations
- [ ] Integrate real-time APIs (Phase 4B)
- [ ] Add user authentication (Phase 4C)
