# Rollback Procedures

Comprehensive guide for reverting deployments in case of issues.

## Quick Reference

| Scenario | Method | Time to Rollback |
|----------|--------|------------------|
| Build fails | Automatic (workflow stops) | Immediate |
| Tests fail | Automatic (workflow stops) | Immediate |
| Deploy succeeds but app broken | Manual rollback | 2-5 minutes |
| Critical production bug | Emergency rollback | 1-2 minutes |
| Performance degradation | Gradual rollback | 5-10 minutes |

## Automatic Rollback

The deployment workflow includes safeguards that prevent bad deployments:

### Pre-Deployment Checks

The workflow automatically stops if:
1. ❌ Linting fails (black, flake8)
2. ❌ Type checking fails (mypy)
3. ❌ Tests fail (pytest)
4. ❌ Visualization generation fails

**Result:** Previous version remains deployed. No action needed.

### Health Check Failure

If health checks fail after deployment:
- Deployment marked as failed in GitHub Actions
- Alert notifications sent
- Previous version remains active

## Manual Rollback Methods

### Method 1: Git Revert (Recommended)

**Use when:** Bad commit merged to main

```bash
# 1. Identify the bad commit
git log --oneline main -10

# 2. Revert the commit (creates new commit)
git revert <bad-commit-hash>

# 3. Push to trigger new deployment
git push origin main

# 4. Verify deployment
# Check GitHub Actions workflow completes successfully
```

**Advantages:**
- Preserves history
- Safe and auditable
- Can revert multiple commits
- Easy to undo the revert if needed

**Example:**
```bash
# Revert the last commit
git revert HEAD
git push origin main

# Revert multiple commits
git revert HEAD~3..HEAD
git push origin main
```

### Method 2: Deploy Previous Version

**Use when:** Need to quickly get back to known good state

```bash
# 1. Find last known good commit
git log --oneline main -20

# 2. Create rollback tag
git tag rollback-$(date +%Y%m%d-%H%M%S)
git push --tags

# 3. Create branch from good commit
git checkout <good-commit-hash>
git checkout -b rollback/restore-<commit-hash>

# 4. Push and create PR (recommended)
git push origin rollback/restore-<commit-hash>
# Then create PR and merge

# OR force push to main (EMERGENCY ONLY)
# git push --force origin HEAD:main
```

**Advantages:**
- Fast rollback
- Returns to known good state
- Can be done in emergency

**Disadvantages:**
- Force push required for immediate effect
- More disruptive

### Method 3: Azure Portal Redeployment

**Use when:** Need to rollback without Git access

1. **Navigate to Azure Portal**
   - Go to https://portal.azure.com
   - Find your Static Web App

2. **Access Deployment History**
   - Click on "Deployment history" in left menu
   - View list of previous deployments

3. **Redeploy Previous Version**
   - Find last successful deployment
   - Click on deployment
   - Click "Redeploy"
   - Confirm redeployment

4. **Monitor Progress**
   - Watch deployment status
   - Usually completes in 1-2 minutes

**Advantages:**
- No Git access needed
- Visual interface
- Quick for non-technical users

**Disadvantages:**
- Doesn't update Git history
- Subsequent Git push will re-deploy bad version

### Method 4: GitHub Actions Manual Trigger

**Use when:** Need to redeploy specific commit

1. **Go to GitHub Actions**
   - Navigate to repository on GitHub
   - Click "Actions" tab

2. **Select Deploy Workflow**
   - Click "Deploy to Azure Static Web Apps"

3. **Trigger Workflow**
   - Click "Run workflow"
   - Select branch or commit
   - Click "Run workflow"

**Advantages:**
- Control over what gets deployed
- Can deploy any branch/commit
- No local Git changes needed

## Emergency Rollback (Critical Issues)

**When to use:** Production is completely broken, users affected

### Step 1: Immediate Communication (30 seconds)

```bash
# Post incident notice
# - Update status page
# - Notify team in Slack/Teams
# - Post to social media if public-facing
```

### Step 2: Quick Rollback (1-2 minutes)

**Option A: Azure Portal (Fastest)**
1. Open Azure Portal on phone/tablet
2. Navigate to Static Web App
3. Deployment history → Previous version → Redeploy

**Option B: Git Revert from Command Line**
```bash
# On any machine with Git access
git clone https://github.com/NCAsterism/places2go.git --depth 5
cd places2go
git checkout main
git revert HEAD --no-edit
git push origin main
```

### Step 3: Verification (1 minute)

```bash
# Check production URL
curl -I https://places2go.azurestaticapps.net

# Verify key pages load
curl https://places2go.azurestaticapps.net/README.html | grep -i "places2go"

# Check Application Insights for errors
# (via Azure Portal)
```

### Step 4: Post-Incident (5-10 minutes)

```bash
# 1. Update team
# 2. Document what happened
# 3. Create incident report
# 4. Schedule post-mortem
# 5. Update status page
```

## Rollback Decision Tree

```
Issue Detected
    │
    ├── Build/Test Failed?
    │   └── No action needed (automatic)
    │
    ├── Visual/UI Issue?
    │   └── Method 1: Git Revert
    │
    ├── Performance Issue?
    │   ├── Minor: Monitor and fix forward
    │   └── Major: Method 1 or 2
    │
    ├── Data/Logic Issue?
    │   └── Method 1: Git Revert (preserves history)
    │
    └── Complete Failure?
        └── Emergency Rollback: Method 3 (Azure Portal)
```

## Rollback Checklist

### Pre-Rollback
- [ ] Identify the issue and severity
- [ ] Determine last known good version
- [ ] Notify team of planned rollback
- [ ] Document the issue
- [ ] Choose rollback method

### During Rollback
- [ ] Execute rollback procedure
- [ ] Monitor deployment progress
- [ ] Watch for errors in logs
- [ ] Verify workflow completes

### Post-Rollback
- [ ] Test critical functionality
- [ ] Check all visualizations load
- [ ] Verify no errors in Application Insights
- [ ] Monitor performance metrics
- [ ] Update incident documentation
- [ ] Notify users if needed
- [ ] Schedule fix and re-deployment

## Testing Rollback (Staging)

Practice rollback procedures in staging environment:

```bash
# 1. Create staging branch
git checkout -b staging-rollback-test

# 2. Intentionally introduce breaking change
echo "// Breaking change" >> deployment/README.html

# 3. Commit and push
git add .
git commit -m "Test: Intentional breaking change"
git push origin staging-rollback-test

# 4. Open PR to main (creates preview environment)
gh pr create --title "Test: Rollback Procedure" --body "Testing rollback"

# 5. Practice rollback on preview environment
# Use Method 1 or 2 to rollback the PR

# 6. Close PR and delete branch
gh pr close
git push origin --delete staging-rollback-test
```

## Rollback Monitoring

After rollback, monitor these metrics:

### Immediate (0-5 minutes)
- [ ] Application loads (HTTP 200 status)
- [ ] No JavaScript console errors
- [ ] All visualizations render
- [ ] Page load time < 3 seconds

### Short-term (5-30 minutes)
- [ ] No error spikes in Application Insights
- [ ] User session count stable
- [ ] No increase in bounce rate
- [ ] Response times normal

### Long-term (30 minutes - 24 hours)
- [ ] Uptime maintained at 99.9%+
- [ ] No user-reported issues
- [ ] Performance metrics baseline
- [ ] Analytics tracking correctly

## Common Rollback Scenarios

### Scenario 1: Bad Visualization Update

**Symptoms:**
- Charts don't render
- JavaScript errors in console
- Blank pages

**Rollback:**
```bash
git revert HEAD
git push origin main
```

**Prevention:**
- Add visualization tests
- Test locally before deploying
- Use preview environments

### Scenario 2: Configuration Error

**Symptoms:**
- Application Insights not tracking
- Analytics not working
- Environment variables incorrect

**Rollback:**
```bash
# Revert config changes
git revert <config-commit-hash>
git push origin main
```

**Prevention:**
- Test configuration changes in staging
- Validate environment variables
- Use configuration validation scripts

### Scenario 3: Dependency Update Breaking

**Symptoms:**
- Build fails
- Import errors
- Missing functionality

**Rollback:**
```bash
# Revert requirements.txt changes
git checkout HEAD~1 requirements.txt
git commit -m "Rollback: Revert dependency update"
git push origin main
```

**Prevention:**
- Test dependency updates locally
- Pin versions in requirements.txt
- Use virtual environments
- Review dependency changelogs

## Rollback Communication Template

### Internal Team Notification

```
🚨 ROLLBACK IN PROGRESS

Issue: [Brief description]
Severity: [Critical/High/Medium/Low]
Affected: [Production/Staging]
Rollback Method: [Method #]
ETA: [X minutes]
Status: [In Progress/Complete]

Action Items:
- [Person]: Monitor deployment
- [Person]: Test after rollback
- [Person]: Document incident

Updates in thread 👇
```

### User-Facing Notice (if needed)

```
We've identified an issue with our latest deployment and are 
rolling back to restore full functionality. This should take 
2-5 minutes. We apologize for any inconvenience.

Status: https://status.places2go.com
```

## Post-Rollback Root Cause Analysis

After rollback, conduct RCA:

1. **What happened?**
   - Timeline of events
   - What broke and why

2. **Why did it happen?**
   - Root cause identification
   - Contributing factors

3. **How do we prevent it?**
   - Process improvements
   - Additional tests needed
   - Monitoring enhancements

4. **Action items**
   - Assigned owners
   - Due dates
   - Follow-up meeting

## Rollback Metrics

Track rollback effectiveness:

| Metric | Target | Actual |
|--------|--------|--------|
| Time to detect | < 5 min | |
| Time to decide | < 2 min | |
| Time to rollback | < 5 min | |
| Time to verify | < 3 min | |
| Total MTTR | < 15 min | |
| Rollback success rate | 100% | |

## Reference Links

- [Deployment Guide](DEPLOYMENT.md)
- [GitHub Actions Workflows](../.github/workflows/)
- [Azure Static Web Apps Documentation](https://docs.microsoft.com/azure/static-web-apps/)
- [Incident Response Plan](INCIDENT_RESPONSE.md) (if exists)

## Contact Information

### Escalation Path

1. **Level 1**: Repository maintainers (GitHub issues)
2. **Level 2**: Azure support (for infrastructure issues)
3. **Level 3**: Emergency contacts (critical production issues)

---

**Last Updated**: [Date]  
**Review Frequency**: Quarterly  
**Next Review**: [Date]
