# Configuration Files

This directory contains environment-specific configuration files for the Places2Go application.

## Files

- `.env.development` - Local development environment
- `.env.staging` - Staging/test deployment environment
- `.env.production` - Production environment

## Usage

### Local Development
Copy `.env.development` to the project root as `.env`:
```bash
cp config/.env.development .env
```

### Azure Deployment
The deployment workflow automatically uses the appropriate environment configuration based on the branch:
- `main` branch → Production environment
- Pull requests → Preview/staging environment

## Configuration Variables

### Required for Production
- `APPLICATIONINSIGHTS_CONNECTION_STRING` - Azure Application Insights connection string
- `GOOGLE_ANALYTICS_ID` - Google Analytics tracking ID (optional)

### Optional API Keys
- `WEATHER_API_KEY` - For future real-time weather data
- `FLIGHT_API_KEY` - For future real-time flight data

## Security Notes

⚠️ **Never commit actual secrets to version control!**

- Store production secrets in GitHub Secrets
- Use Azure Key Vault for sensitive data
- Environment files in this directory contain only placeholders

## GitHub Secrets Required

Add these secrets to your GitHub repository for deployment:

1. `AZURE_STATIC_WEB_APPS_API_TOKEN` - Azure Static Web Apps deployment token
2. `APPLICATIONINSIGHTS_CONNECTION_STRING` - Application Insights (optional)
3. `GOOGLE_ANALYTICS_ID` - Google Analytics (optional)

### How to Add Secrets
1. Go to your repository on GitHub
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add each secret with its value
