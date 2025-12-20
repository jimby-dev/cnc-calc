# Security Setup Guide

## Quick Setup Checklist

To protect your application from unauthorized access and prevent cost abuse:

### 1. Set API Key (Required)

**Backend:**
```bash
# Generate a strong API key
openssl rand -hex 32

# Add to backend/.env or environment variables
API_KEY=your-generated-key-here
```

**Frontend:**
```bash
# Add to frontend/.env.local
NEXT_PUBLIC_API_KEY=your-generated-key-here
```

### 2. Restrict IP Access (Recommended)

Update AWS Security Groups to only allow your IP addresses:

**Option A: Via AWS Console**
1. Go to EC2 → Security Groups
2. Find `cnc-calc-backend-sg`
3. Edit inbound rules:
   - Remove: `0.0.0.0/0` on port 8000
   - Add: Your IP (e.g., `1.2.3.4/32`) on port 8000
4. Repeat for `cnc-calc-frontend-sg` on port 3000

**Option B: Via CloudFormation**
```bash
# Find your IP: https://whatismyipaddress.com/
# Deploy with AllowedIPs parameter
aws cloudformation deploy \
  --template-file infra/services.yml \
  --stack-name cnc-calc-services-prod \
  --parameter-overrides \
    Environment=prod \
    AllowedIPs=YOUR_IP/32,PARTNER_IP/32 \
  --region us-east-2
```

**Note:** The current CloudFormation template only supports one IP in the parameter. For multiple IPs, manually update security groups or use AWS Console.

### 3. Set Rate Limits

Rate limiting is already configured (60 requests/minute). To adjust:
```bash
# In backend/.env
RATE_LIMIT_PER_MINUTE=30  # More restrictive
```

### 4. Monitor Costs

Set up AWS Billing Alerts:
1. Go to AWS Billing → Budgets
2. Create budget alert (e.g., $10/month)
3. Set up CloudWatch alarms for unusual traffic

## Security Features Implemented

✅ **API Key Authentication** - All endpoints protected (except health checks)
✅ **Rate Limiting** - 60 requests/minute per IP
✅ **IP Whitelisting Support** - CloudFormation parameter + manual option
✅ **Resource Limits** - Fixed ECS service count (no auto-scaling)
✅ **CORS Protection** - Restricted origins
✅ **Production Hardening** - Docs disabled, trusted hosts

## Testing

After setup, test authentication:
```bash
# Should fail (no API key)
curl http://your-backend-url/api/tools

# Should succeed (with API key)
curl -H "X-API-Key: your-api-key" http://your-backend-url/api/tools
```

## Troubleshooting

**"Invalid or missing API key"**
- Verify `API_KEY` is set in backend environment
- Check frontend has `NEXT_PUBLIC_API_KEY` set
- Ensure header is `X-API-Key` (case-sensitive)

**"Rate limit exceeded"**
- Wait 1 minute
- Check if legitimate traffic or abuse
- Consider increasing limit if needed

**Cannot connect from your IP**
- Verify IP is whitelisted in security group
- Check if IP changed (use dynamic DNS if needed)
- Verify security group rules are active

## Next Steps

1. Generate and set API key
2. Whitelist your IPs in security groups
3. Test authentication
4. Set up billing alerts
5. Monitor CloudWatch logs for suspicious activity

For detailed security documentation, see `docs/SECURITY.md`.

