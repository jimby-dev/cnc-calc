# Infrastructure as Code - CloudFormation Templates

This directory contains CloudFormation templates for deploying the CNC Calculator infrastructure to AWS.

## Stack Architecture

The infrastructure is split into multiple stacks for better organization and modularity:

1. **main.yml** - VPC, networking, RDS database, ElastiCache
2. **ecs-cluster.yml** - ECS cluster, ECR repositories, CloudWatch log groups
3. **task-definitions.yml** - ECS task definitions and IAM roles
4. **services.yml** - ECS services and security groups

## Deployment Order

Stacks must be deployed in this order:

1. Main Infrastructure (`main.yml`)
2. ECS Cluster (`ecs-cluster.yml`)
3. Task Definitions (`task-definitions.yml`)
4. Services (`services.yml`)

## Manual Deployment (if needed)

### Prerequisites

- AWS CLI configured
- Appropriate IAM permissions
- GitHub Actions role already created (for automated deployments)

### Deploy Main Infrastructure

```bash
aws cloudformation deploy \
  --template-file main.yml \
  --stack-name cnc-calc-main-prod \
  --parameter-overrides Environment=prod \
  --capabilities CAPABILITY_IAM \
  --region us-east-2
```

### Deploy ECS Cluster

```bash
aws cloudformation deploy \
  --template-file ecs-cluster.yml \
  --stack-name cnc-calc-ecs-cluster-prod \
  --parameter-overrides Environment=prod \
  --region us-east-2
```

### Deploy Task Definitions

```bash
aws cloudformation deploy \
  --template-file task-definitions.yml \
  --stack-name cnc-calc-task-definitions-prod \
  --parameter-overrides \
    Environment=prod \
    ClusterStackName=cnc-calc-ecs-cluster-prod \
    DatabaseEndpoint=your-rds-endpoint \
    DatabaseName=cnc_calc \
    DatabaseUser=cnc_user \
    DatabasePassword=your-password \
    BackendURL=http://placeholder-backend-url \
  --capabilities CAPABILITY_IAM \
  --region us-east-2
```

### Deploy Services

```bash
# First, get task definition ARNs
BACKEND_TD=$(aws cloudformation describe-stacks \
  --stack-name cnc-calc-task-definitions-prod \
  --query 'Stacks[0].Outputs[?OutputKey==`BackendTaskDefinitionArn`].OutputValue' \
  --output text \
  --region us-east-2)

FRONTEND_TD=$(aws cloudformation describe-stacks \
  --stack-name cnc-calc-task-definitions-prod \
  --query 'Stacks[0].Outputs[?OutputKey==`FrontendTaskDefinitionArn`].OutputValue' \
  --output text \
  --region us-east-2)

# Deploy services
aws cloudformation deploy \
  --template-file services.yml \
  --stack-name cnc-calc-services-prod \
  --parameter-overrides \
    Environment=prod \
    ClusterStackName=cnc-calc-ecs-cluster-prod \
    TaskDefinitionsStackName=cnc-calc-task-definitions-prod \
    MainStackName=cnc-calc-main-prod \
    BackendTaskDefinitionArn=$BACKEND_TD \
    FrontendTaskDefinitionArn=$FRONTEND_TD \
  --region us-east-2
```

## Automated Deployment

GitHub Actions automatically deploys all stacks when you push to the `main` branch. See `.github/workflows/ci-cd.yml` for details.

## Required GitHub Secrets

- `DATABASE_PASSWORD` - RDS database password

## Updating Resources

To update resources:

1. Modify the CloudFormation template
2. Push to GitHub
3. GitHub Actions will automatically update the stacks

Or manually:

```bash
aws cloudformation deploy \
  --template-file <template-file> \
  --stack-name <stack-name> \
  --region us-east-2
```

## Cleanup

To delete all infrastructure:

```bash
aws cloudformation delete-stack --stack-name cnc-calc-services-prod --region us-east-2
aws cloudformation delete-stack --stack-name cnc-calc-task-definitions-prod --region us-east-2
aws cloudformation delete-stack --stack-name cnc-calc-ecs-cluster-prod --region us-east-2
aws cloudformation delete-stack --stack-name cnc-calc-main-prod --region us-east-2
```

**Note**: Delete stacks in reverse order (services first, main last).

