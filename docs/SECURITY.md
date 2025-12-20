# Security Guide

## Overview

This application implements multiple layers of security to protect against unauthorized access and prevent cost-related abuse.

## Security Measures

### 1. API Key Authentication

All API endpoints (except health checks) require an API key for authentication.

**Setup:**
1. Generate a strong, random API key (e.g., using `openssl rand -hex 32`)
2. Set it as an environment variable:
   ```bash
   export API_KEY="your-secret-api-key-here"
   ```
3. Add it to your backend `.env` file:
   ```
   API_KEY=your-secret-api-key-here
   ```
4. For frontend, add it to your `.env.local`:
   ```
   NEXT_PUBLIC_API_KEY=your-secret-api-key-here
   ```

**Usage:**
- Backend: Automatically validates `X-API-Key` header on all requests
- Frontend: Automatically includes `X-API-Key` header in all API calls via `api-client.ts`

### 2. Rate Limiting

Rate limiting prevents abuse and excessive resource consumption:
- **Limit**: 60 requests per minute per IP address
- **Implementation**: In-memory rate limiter (use Redis for production with multiple instances)
- **Health checks**: Excluded from rate limiting

Rate limit headers are included in responses:
- `X-RateLimit-Limit`: Maximum requests per minute
- `X-RateLimit-Remaining`: Remaining requests in current window
- `X-RateLimit-Reset`: Unix timestamp when limit resets

### 3. IP Whitelisting (Infrastructure Level)

Restrict access at the AWS Security Group level to only allow connections from specific IP addresses.

**Setup:**
1. Find your public IP address: https://whatismyipaddress.com/
2. Update CloudFormation deployment with `AllowedIPs` parameter:
   ```bash
   aws cloudformation deploy \
     --template-file services.yml \
     --stack-name cnc-calc-services-prod \
     --parameter-overrides \
       Environment=prod \
       AllowedIPs=YOUR_IP/32,PARTNER_IP/32 \
     --region us-east-2
   ```

**Note**: Use `/32` for a single IP address (e.g., `1.2.3.4/32`). For multiple IPs, separate with commas.

**Manual Update (AWS Console):**
1. Go to EC2 → Security Groups
2. Find `cnc-calc-backend-sg`
3. Edit inbound rules
4. Remove `0.0.0.0/0` rule
5. Add rule: Type=Custom TCP, Port=8000, Source=YOUR_IP/32
6. Repeat for `cnc-calc-frontend-sg` on port 3000

### 4. Resource Limits

To prevent auto-scaling abuse:
- **ECS Services**: `DesiredCount: 1` (fixed, no auto-scaling)
- **RDS**: `db.t3.micro` (smallest instance)
- **ElastiCache**: `cache.t3.micro` (smallest instance)

### 5. CORS Configuration

CORS is configured to only allow requests from specified origins:
- Development: `http://localhost:3000`, `http://localhost:3001`
- Production: Update `ALLOWED_ORIGINS` in backend config

### 6. Environment-Specific Security

- **Development**: API docs enabled, relaxed security
- **Production**: 
  - API docs disabled (`/docs` and `/redoc` endpoints removed)
  - Trusted host middleware enabled
  - Strict CORS policies

## Cost Prevention Checklist

Before deploying to production:

- [ ] Set `API_KEY` environment variable (use strong, random value)
- [ ] Configure IP whitelisting in security groups
- [ ] Set `RATE_LIMIT_PER_MINUTE` to appropriate value (default: 60)
- [ ] Verify `DesiredCount: 1` for ECS services (no auto-scaling)
- [ ] Disable public access where possible
- [ ] Monitor CloudWatch for unexpected traffic
- [ ] Set up AWS billing alerts
- [ ] Review security group rules monthly

## Monitoring

### CloudWatch Alarms (Recommended)

Set up alarms for:
1. **Unusual API traffic**: Alert on request count > threshold
2. **Database connections**: Alert on connection pool exhaustion
3. **ECS task count**: Alert if tasks exceed 1
4. **Cost**: Daily/monthly cost alerts

### Logs to Monitor

- Invalid API key attempts (logged as warnings)
- Rate limit exceeded events (logged as warnings)
- Unusual request patterns
- Failed authentication attempts

## Troubleshooting

### "Invalid or missing API key" error
- Verify `API_KEY` is set in backend environment
- Check that frontend has `NEXT_PUBLIC_API_KEY` set
- Verify header name is `X-API-Key` (case-sensitive)

### "Rate limit exceeded" error
- Wait 1 minute before retrying
- Check rate limit headers in response
- Consider increasing limit if legitimate traffic

### Cannot connect from IP
- Verify your IP is in the security group whitelist
- Check if IP has changed (use dynamic DNS if needed)
- Verify security group rules are correctly applied

## Security Best Practices

1. **Never commit API keys** to version control
2. **Rotate API keys** periodically (every 90 days recommended)
3. **Use HTTPS** in production (add ALB/CloudFront)
4. **Monitor logs** for suspicious activity
5. **Keep dependencies updated** (run `npm audit` and `pip-audit`)
6. **Use AWS Secrets Manager** for production secrets (future enhancement)

## Future Enhancements

- [ ] JWT-based authentication for user management
- [ ] AWS WAF for additional DDoS protection
- [ ] CloudFront with signed URLs
- [ ] Redis-based distributed rate limiting
- [ ] IP geolocation blocking
- [ ] AWS Secrets Manager integration
- [ ] Multi-factor authentication (MFA)

