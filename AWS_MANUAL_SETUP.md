# AWS Manual Setup Requirements

## Overview

Most infrastructure is deployed via CloudFormation (Infrastructure as Code), but there are **a few one-time manual setup steps** required before automated deployments can work.

---

## ✅ One-Time Manual Setup (Required Before First Deployment)

### 1. **GitHub Actions IAM Role** (REQUIRED)
**Status**: Must be created manually (one-time)  
**Why**: CloudFormation cannot create OIDC identity providers for GitHub Actions

**Steps**:
1. Go to AWS IAM Console → Roles → Create Role
2. Select "Web identity" as trusted entity type
3. Identity provider: `token.actions.githubusercontent.com`
4. Audience: `sts.amazonaws.com`
5. Role name: `GitHubActionsECSRole`
6. Attach policies:
   - `AmazonECS_FullAccess` (or custom policy with ECS, CloudFormation, ECR permissions)
7. In trust policy, add condition:
   ```json
   "Condition": {
     "StringEquals": {
       "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
     },
     "StringLike": {
       "token.actions.githubusercontent.com:sub": "repo:YOUR_GITHUB_USERNAME/cnccalc:*"
     }
   }
   ```
8. Note the Role ARN (e.g., `arn:aws:iam::986341372774:role/GitHubActionsECSRole`)

**Already Done?** ✅ If you already created this role, you're good to go.

---

### 2. **ECS Service-Linked Role** (Usually Auto-Created)
**Status**: Usually auto-created, but may need manual creation  
**Why**: Required for ECS cluster creation

**Check if exists**:
```bash
aws iam get-role --role-name AWSServiceRoleForECS --region us-east-2
```

**If missing, create it**:
```bash
aws iam create-service-linked-role \
  --aws-service-name ecs.amazonaws.com \
  --region us-east-2
```

**Or via Console**:
1. IAM → Roles → Create role
2. Select "AWS service" → ECS → Use case: "ECS"
3. Role name: `AWSServiceRoleForECS` (auto-filled)
4. Create role

**Already Done?** ✅ This is usually auto-created when you first create an ECS cluster. If your cluster exists, this role exists.

---

## ⚠️ Post-Deployment Manual Configuration (Optional but Recommended)

### 3. **IP Whitelisting** (Security - Recommended)
**Status**: Can be done via CloudFormation OR manually  
**When**: After initial deployment

**Option A: Via CloudFormation** (Single IP):
```bash
aws cloudformation deploy \
  --template-file infra/services.yml \
  --stack-name cnc-calc-services-prod \
  --parameter-overrides \
    Environment=prod \
    AllowedIPs=YOUR_IP/32 \
  --region us-east-2
```

**Option B: Via AWS Console** (Multiple IPs):
1. EC2 → Security Groups
2. Find `cnc-calc-backend-sg`
3. Edit inbound rules:
   - Remove: `0.0.0.0/0` on port 8000
   - Add: Your IPs (e.g., `1.2.3.4/32`, `5.6.7.8/32`)
4. Repeat for `cnc-calc-frontend-sg` on port 3000

**Note**: CloudFormation parameter only supports one IP. For multiple IPs, use Console or update security group manually.

---

### 4. **API Key Configuration** (Required for Application)
**Status**: Must be set manually (not in CloudFormation)  
**When**: After deployment, before using the app

**Steps**:
1. Generate API key:
   ```bash
   openssl rand -hex 32
   ```

2. **Update ECS Task Definitions** (via Console or CLI):
   - ECS → Task Definitions → `cnc-calc-backend`
   - Create new revision
   - Add environment variable: `API_KEY=your-generated-key`
   - Update service to use new revision

3. **Or use AWS Secrets Manager** (recommended for production):
   - Create secret: `cnc-calc-api-key`
   - Store API key value
   - Update task definition to reference secret
   - Update CloudFormation template to use Secrets Manager

**Note**: This is application configuration, not infrastructure. CloudFormation doesn't manage application secrets by default.

---

### 5. **Billing Alerts** (Cost Monitoring - Recommended)
**Status**: Manual setup (not in CloudFormation)  
**When**: Anytime, but recommended before production use

**Steps**:
1. AWS Billing → Budgets → Create budget
2. Set budget amount (e.g., $10/month)
3. Configure alerts (email, SNS)
4. Set up CloudWatch alarms for unusual traffic

---

## ✅ Fully Automated (No Manual Steps Needed)

These are handled entirely by CloudFormation:

- ✅ VPC, subnets, internet gateway, route tables
- ✅ RDS PostgreSQL database
- ✅ ElastiCache Redis cluster
- ✅ ECS cluster
- ✅ ECR repositories
- ✅ CloudWatch log groups
- ✅ ECS task execution role
- ✅ ECS task role
- ✅ ECS task definitions
- ✅ ECS services
- ✅ Security groups (structure, but IP whitelisting may need manual update)
- ✅ Database subnet groups
- ✅ ElastiCache subnet groups

---

## Deployment Flow

### First Time Setup:
1. ✅ Create `GitHubActionsECSRole` (manual - one time)
2. ✅ Verify/create `AWSServiceRoleForECS` (usually auto, but check)
3. ✅ Push to GitHub → GitHub Actions deploys everything
4. ⚠️ Configure IP whitelisting (manual - security)
5. ⚠️ Set API key in task definitions (manual - required for app)

### Subsequent Deployments:
- ✅ Push to GitHub → Everything updates automatically
- ⚠️ Only need to manually update if:
  - Adding new IPs to whitelist
  - Rotating API keys
  - Changing security settings

---

## Summary

**Manual Steps Required**:
1. ✅ **GitHub Actions IAM Role** - One-time, before first deployment
2. ⚠️ **IP Whitelisting** - After deployment, for security
3. ⚠️ **API Key Configuration** - After deployment, for app functionality
4. ⚠️ **Billing Alerts** - Optional, but recommended

**Everything Else**: Fully automated via CloudFormation and GitHub Actions

---

## Quick Checklist

Before first deployment:
- [ ] GitHub Actions IAM role created (`GitHubActionsECSRole`)
- [ ] ECS service-linked role exists (usually auto)
- [ ] `DATABASE_PASSWORD` secret set in GitHub

After first deployment:
- [ ] IP whitelisting configured (security groups)
- [ ] API key set in ECS task definitions
- [ ] Billing alerts configured
- [ ] Test application access

---

## Notes

- **GitHub Actions Role**: This is the only infrastructure component that cannot be created via CloudFormation (AWS limitation with OIDC providers)
- **API Keys**: Application secrets are not managed by CloudFormation by default. Consider AWS Secrets Manager for production.
- **IP Whitelisting**: CloudFormation parameter supports one IP. Multiple IPs require manual security group updates or template enhancement.
- **Service Updates**: After setting API key, you'll need to update the ECS service to use the new task definition revision.

