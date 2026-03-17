# Runbook: Deploy to Production

## Prerequisites
- [ ] All changes merged to `main` branch
- [ ] Tests passing in QA sandbox (>85% coverage)
- [ ] PR approved by peer reviewer
- [ ] No open blockers or known issues
- [ ] Deployment window agreed (avoid peak hours)

## Steps

### 1. Verify QA Validation
```bash
# Run all tests in QA
sf apex run test --test-level RunLocalTests --target-org qa --result-format human --wait 30

# Verify coverage meets threshold
# Look for: "Org Wide Coverage: XX%"
```

### 2. Generate Delta Package
```bash
cd /path/to/salesforce/repo
git checkout main && git pull

# Generate delta between last prod deploy tag and current
sf sgd source delta --from last-prod-deploy --to HEAD --output delta-package/

# Review what's included
cat delta-package/package/package.xml
```

### 3. Validate in Production (Dry Run)
```bash
# Check-only deployment — validates without actually deploying
sf project deploy start \
  --manifest delta-package/package/package.xml \
  --target-org prod \
  --test-level RunLocalTests \
  --dry-run \
  --wait 30
```

### 4. Deploy to Production
```bash
# Actual deployment
sf project deploy start \
  --manifest delta-package/package/package.xml \
  --target-org prod \
  --test-level RunLocalTests \
  --wait 30
```

### 5. Post-Deploy Verification
- [ ] Spot-check key features in production
- [ ] Verify new components appear correctly
- [ ] Check for errors in Setup → Apex Jobs
- [ ] Monitor email notifications for deployment errors

### 6. Tag the Release
```bash
git tag -a prod-deploy-$(date +%Y%m%d) -m "Production deploy $(date +%Y-%m-%d)"
git push origin prod-deploy-$(date +%Y%m%d)
```

## Rollback

### If deployment fails:
1. Check deployment status: `sf project deploy report --target-org prod`
2. Review errors in Setup → Deployment Status
3. Fix issues and re-deploy, or use Quick Deploy if validation was recent

### If issues found post-deploy:
1. Create hotfix branch from the previous production tag
2. Fix the issue
3. Fast-track through QA → prod pipeline
4. For critical issues: use `sf project deploy start` directly with the fix

## Contacts
- **Deployment issues:** Kevin Phillips (kphillips@sanguinebio.com)
- **Approval required:** Brian Vong (Technology Director)
