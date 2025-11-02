# Azure Deployment Configuration

This directory contains configuration files for deploying Places2Go to Azure Static Web Apps.

## Files

- `staticwebapp.config.json` - Azure Static Web Apps configuration
- `config/` - Environment-specific configuration files
- `deployment/` - Static files to be deployed
- `.github/workflows/deploy.yml` - CI/CD pipeline

## Quick Start

### Prerequisites

1. **Azure Account** - Sign up at https://portal.azure.com (free tier available)
2. **GitHub Repository** - Fork or clone this repository
3. **Azure Static Web Apps API Token** - Get from Azure Portal

### Setup Steps

1. **Create Azure Static Web App**
   ```bash
   # Option 1: Using Azure Portal (Recommended)
   # Follow the visual guide in docs/DEPLOYMENT.md
   
   # Option 2: Using Azure CLI
   az staticwebapp create \
     --name places2go \
     --resource-group places2go-rg \
     --source https://github.com/YOUR_USERNAME/places2go \
     --location eastus \
     --branch main \
     --app-location "/deployment"
   ```

2. **Add GitHub Secret**
   - Go to GitHub repository → Settings → Secrets → Actions
   - Add secret: `AZURE_STATIC_WEB_APPS_API_TOKEN`
   - Get token from Azure Portal → Static Web App → Overview → Manage deployment token

3. **Push to Main Branch**
   ```bash
   git checkout main
   git push origin main
   ```

4. **Monitor Deployment**
   - Check GitHub Actions tab for workflow progress
   - Deployment typically completes in 3-5 minutes

## Configuration Files

### staticwebapp.config.json

Configures routing, headers, and security settings for Azure Static Web Apps:

- **Navigation Fallback**: Redirects to index.html for SPA routing
- **Routes**: Custom routing rules and caching policies
- **Response Overrides**: Custom error pages (404, 401, etc.)
- **Global Headers**: Security headers (CSP, X-Frame-Options, etc.)
- **MIME Types**: File type configurations
- **Platform Settings**: Runtime configuration (Python 3.11)

### Environment Configurations

| File | Environment | Purpose |
|------|-------------|---------|
| `config/.env.development` | Local dev | Development settings |
| `config/.env.staging` | Staging/Preview | Testing before production |
| `config/.env.production` | Production | Live deployment |

## CI/CD Pipeline

The deployment workflow (`.github/workflows/deploy.yml`) automatically:

1. ✅ **Lints** - Checks code quality (black, flake8)
2. ✅ **Tests** - Runs pytest suite
3. ✅ **Builds** - Generates HTML visualizations
4. ✅ **Deploys** - Uploads to Azure Static Web Apps
5. ✅ **Validates** - Health checks after deployment

### Trigger Events

- **Push to main** → Production deployment
- **Pull Request to main** → Preview environment
- **Manual trigger** → Run workflow manually

## Monitoring

### Application Insights (Optional)

Track errors, performance, and usage:

```bash
# Create Application Insights resource
az monitor app-insights component create \
  --app places2go-insights \
  --location eastus \
  --resource-group places2go-rg \
  --application-type web

# Add connection string to GitHub Secrets
# Secret name: APPLICATIONINSIGHTS_CONNECTION_STRING
```

### Google Analytics (Optional)

Track user behavior:

1. Create GA4 property at https://analytics.google.com
2. Get Measurement ID (G-XXXXXXXXXX)
3. Add to GitHub Secrets: `GOOGLE_ANALYTICS_ID`

## Deployment Environments

| Environment | URL | Branch | Auto-Deploy |
|-------------|-----|--------|-------------|
| Development | http://localhost:8000 | develop | No |
| Preview | https://staging-*.azurestaticapps.net | PR to main | Yes |
| Production | https://places2go.azurestaticapps.net | main | Yes |

## Security

### Secrets Management

**Never commit secrets to Git!** Use:

1. **GitHub Secrets** - For CI/CD credentials
2. **Azure Key Vault** - For application secrets
3. **Environment Variables** - For runtime configuration

### Required Secrets

| Secret | Required | Purpose |
|--------|----------|---------|
| `AZURE_STATIC_WEB_APPS_API_TOKEN` | ✅ Yes | Deployment authentication |
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | ⚠️ Recommended | Error tracking |
| `GOOGLE_ANALYTICS_ID` | ❌ Optional | Usage analytics |

### Content Security Policy

Default CSP allows:
- Self-hosted content
- Plotly CDN for visualizations
- Inline styles/scripts (for Plotly)
- External images and fonts

Modify in `staticwebapp.config.json` if needed.

## Troubleshooting

### Deployment Fails

**Check workflow logs:**
```bash
gh run list --workflow=deploy.yml
gh run view <run-id> --log
```

**Common issues:**
- Missing GitHub secret → Add `AZURE_STATIC_WEB_APPS_API_TOKEN`
- Test failures → Fix tests locally and push
- Build errors → Check Python dependencies

### Application Not Loading

1. **Check deployment status** in Azure Portal
2. **Verify workflow succeeded** in GitHub Actions
3. **Check browser console** for JavaScript errors
4. **Test locally** to reproduce the issue

### Missing Visualizations

```bash
# Regenerate visualizations locally
python -m scripts.visualizations.destinations_map
python -m scripts.visualizations.cost_comparison
python -m scripts.visualizations.flight_prices
python -m scripts.visualizations.weather_forecast

# Check output
ls -la .build/visualizations/
```

## Performance Optimization

### Caching Strategy

- **Static assets**: 1 hour cache with must-revalidate
- **HTML files**: 1 hour cache
- **API responses**: Configured per endpoint

### CDN

Azure Static Web Apps automatically uses Azure CDN for:
- Global content distribution
- Reduced latency
- Improved performance

### Compression

Automatic gzip/brotli compression for:
- HTML files
- CSS files
- JavaScript files
- JSON responses

## Custom Domain (Optional)

To use your own domain:

```bash
# Add custom domain
az staticwebapp hostname set \
  --name places2go \
  --resource-group places2go-rg \
  --hostname www.yourdomain.com

# Update DNS records (at your domain registrar)
# Add CNAME: www → places2go.azurestaticapps.net
```

SSL certificate is automatically provisioned by Azure.

## Rollback

If deployment fails or introduces issues:

### Automatic Rollback

- Build/test failures automatically prevent deployment
- Previous version remains active

### Manual Rollback

```bash
# Method 1: Git revert
git revert HEAD
git push origin main

# Method 2: Azure Portal
# Navigate to Static Web App → Deployment History
# Select previous deployment → Redeploy
```

See [docs/ROLLBACK.md](../docs/ROLLBACK.md) for detailed procedures.

## Documentation

- [Deployment Guide](../docs/DEPLOYMENT.md) - Complete setup instructions
- [Rollback Procedures](../docs/ROLLBACK.md) - Emergency procedures
- [Monitoring Setup](../docs/MONITORING.md) - Analytics and alerts
- [Azure Static Web Apps Docs](https://docs.microsoft.com/azure/static-web-apps/)

## Support

- **GitHub Issues**: https://github.com/NCAsterism/places2go/issues
- **Azure Support**: https://portal.azure.com → Support
- **Documentation**: See `/docs` directory

## Success Metrics

Target metrics from Phase 4D:

- ✅ Zero-downtime deployments
- ✅ < 5 minute deploy time
- ✅ 99.9% uptime
- ✅ Automated rollback on failures
- ✅ Monitoring alerts working

Monitor these in:
- GitHub Actions (deployment time)
- Azure Portal (uptime, performance)
- Application Insights (errors, usage)

---

**Last Updated**: 2024
**Version**: 1.0
**Maintained By**: Places2Go Team
