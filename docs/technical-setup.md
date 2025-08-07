# Technical Setup Guide

**Complete implementation guide for AI Marketing Toolkit deployment**

*Professional setup by [Sotirios Spyrou](https://www.linkedin.com/in/sspyrou/) - Technical Marketing Leadership*

---

## 🎯 Quick Start Summary

**Time to Deploy:** 2-4 hours  
**Technical Level:** Intermediate Python/Marketing Technology  
**ROI Timeline:** 15-25% efficiency gains within 30 days

**Prerequisites Checklist:**
- ✅ Python 3.8+ installed
- ✅ Marketing platform API access (Google Ads, Facebook, LinkedIn)
- ✅ OpenAI or Anthropic API key
- ✅ Git and terminal/command prompt familiarity

---

## 🚀 Installation Process

### Step 1: Environment Setup

**Clone and Initialize Repository:**
```bash
# Clone repository
git clone https://github.com/your-org/ai-marketing-toolkit.git
cd ai-marketing-toolkit

# Create isolated Python environment
python -m venv ai_marketing_env
source ai_marketing_env/bin/activate  # Linux/Mac
# On Windows: ai_marketing_env\Scripts\activate

# Verify Python version
python --version  # Should be 3.8 or higher
```

**Install Dependencies:**
```bash
# Install core requirements
pip install -r requirements.txt

# Verify installation
python -c "import pandas, numpy, openai, google.ads.googleads; print('Dependencies installed successfully')"
```

### Step 2: API Configuration

**Create Environment File:**
```bash
# Copy template
cp .env.example .env

# Edit with your favorite editor
nano .env  # or vim .env, code .env, etc.
```

**Required API Keys Configuration:**

```bash
# .env file configuration
# OpenAI API (for content generation)
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# Google Ads API (for campaign optimization)
GOOGLE_ADS_DEVELOPER_TOKEN=your-developer-token
GOOGLE_ADS_CLIENT_ID=your-client-id
GOOGLE_ADS_CLIENT_SECRET=your-client-secret
GOOGLE_ADS_REFRESH_TOKEN=your-refresh-token
GOOGLE_ADS_CUSTOMER_ID=123-456-7890

# Facebook Marketing API
FACEBOOK_ACCESS_TOKEN=your-long-lived-access-token
FACEBOOK_APP_ID=your-app-id
FACEBOOK_APP_SECRET=your-app-secret
FACEBOOK_AD_ACCOUNT_ID=act_123456789

# LinkedIn Marketing API
LINKEDIN_ACCESS_TOKEN=your-linkedin-access-token
LINKEDIN_CLIENT_ID=your-client-id
LINKEDIN_CLIENT_SECRET=your-client-secret

# Analytics and Tracking
GOOGLE_ANALYTICS_PROPERTY_ID=GA-XXXXXXXXX-X
GOOGLE_ANALYTICS_CREDENTIALS_PATH=./config/ga-credentials.json
```

### Step 3: API Setup Walkthrough

**Google Ads API Setup:**
1. **Visit Google Ads API Console**: https://developers.google.com/google-ads/api
2. **Create Developer Token:**
   - Apply for developer token in Google Ads account
   - Wait for approval (typically 24-48 hours)
3. **OAuth2 Credentials:**
   ```bash
   # Generate refresh token
   python examples/generate_google_ads_token.py
   ```

**Facebook Marketing API Setup:**
1. **Business Manager**: https://business.facebook.com
2. **Create Marketing API App:**
   - Go to Meta for Developers
   - Create new app with Marketing API permissions
3. **Generate Long-lived Token:**
   ```bash
   # Generate and verify access token
   python examples/verify_facebook_access.py
   ```

**OpenAI API Setup:**
1. **Visit OpenAI Platform**: https://platform.openai.com
2. **Create API Key**: Generate new secret key
3. **Set Usage Limits**: Configure monthly spending limits

### Step 4: Initial Configuration

**Test All Integrations:**
```bash
# Run comprehensive system check
python setup_verification.py

# Expected output:
# ✅ OpenAI API: Connected successfully
# ✅ Google Ads API: Connected, 12 campaigns found
# ✅ Facebook API: Connected, 8 ad sets found
# ✅ LinkedIn API: Connected, 3 campaigns found
# ✅ Configuration: All required settings present
```

**Configure Business Settings:**
```python
# config/business_settings.py
BUSINESS_CONFIG = {
    'company_name': 'Your Company Name',
    'industry': 'technology',  # Options: technology, ecommerce, b2b_services, healthcare
    'target_markets': ['US', 'UK', 'CA'],
    'fiscal_year_start': 'january',
    'default_currency': 'USD',
    'attribution_lookback_days': 30,
    'statistical_confidence_threshold': 0.85
}
```

---

## ⚙️ Platform-Specific Setup

### Google Ads Integration

**Authentication Process:**
```bash
# Step 1: Generate authentication URL
python -c "
from google.ads.googleads.client import GoogleAdsClient
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow

flow = Flow.from_client_config({
    'web': {
        'client_id': 'YOUR_CLIENT_ID',
        'client_secret': 'YOUR_CLIENT_SECRET',
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://oauth2.googleapis.com/token'
    }
}, scopes=['https://www.googleapis.com/auth/adwords'])
flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
auth_url, _ = flow.authorization_url(prompt='consent')
print(f'Go to: {auth_url}')
"

# Step 2: Exchange authorization code for refresh token
# (Follow prompts after visiting URL above)
```

**Campaign Access Verification:**
```python
# examples/verify_google_ads_access.py
from campaign_optimizer import CampaignOptimizer

optimizer = CampaignOptimizer()
campaigns = optimizer.get_campaign_list()
print(f"Successfully connected to {len(campaigns)} campaigns")

# Sample output shows campaign IDs, names, and current performance
for campaign in campaigns:
    print(f"Campaign: {campaign.name}, ROAS: {campaign.current_roas:.2f}x")
```

### Facebook Marketing API

**Business Manager Setup:**
1. **Verify Business Account**: Ensure business verification is complete
2. **API Permissions**: Request advanced access for ads_management and ads_read
3. **Rate Limits**: Configure for your expected query volume

**Integration Test:**
```python
# examples/verify_facebook_integration.py
from content_generation.content_suite import ContentSuite
from facebook_ads import FacebookAdsApi

# Initialize API connection
FacebookAdsApi.init(access_token=os.getenv('FACEBOOK_ACCESS_TOKEN'))

# Test campaign data retrieval
ad_account = AdAccount(f"act_{os.getenv('FACEBOOK_AD_ACCOUNT_ID')}")
campaigns = ad_account.get_campaigns(fields=['name', 'status', 'spend'])

print(f"Connected to Facebook account with {len(campaigns)} campaigns")
```

### LinkedIn Marketing API

**Application Setup:**
1. **LinkedIn Developer Portal**: https://developer.linkedin.com
2. **Create Marketing API Application**
3. **Request Partner Access**: For advanced features

**Connection Verification:**
```python
# examples/verify_linkedin_integration.py
import requests

headers = {'Authorization': f'Bearer {linkedin_access_token}'}
response = requests.get(
    'https://api.linkedin.com/v2/adAccountsV2',
    headers=headers
)

if response.status_code == 200:
    accounts = response.json()
    print(f"LinkedIn API connected: {len(accounts['elements'])} ad accounts found")
```

---

## 🔧 Advanced Configuration

### Attribution Model Selection

**Choose Attribution Method:**
```python
# config/attribution_settings.py
from attribution_models import AttributionModel

ATTRIBUTION_CONFIG = {
    'primary_model': AttributionModel.DATA_DRIVEN,  # Recommended for most businesses
    'fallback_model': AttributionModel.TIME_DECAY,  # If insufficient data
    'minimum_touchpoints': 1000,  # Monthly minimum for statistical significance
    'confidence_threshold': 0.80,  # 80% statistical confidence required
    'lookback_window_days': 30,   # Attribution window
    'cross_device_tracking': True, # Enable cross-device attribution
}
```

**Model Selection Guide:**
- **B2B Long Sales Cycle**: Position-Based or Data-Driven
- **E-commerce**: Time-Decay or Data-Driven  
- **Brand Awareness Focus**: Linear or First-Touch
- **Direct Response**: Last-Click or Time-Decay

### Performance Optimization

**Database Configuration:**
```python
# config/database_settings.py
DATABASE_CONFIG = {
    'connection_pool_size': 10,
    'max_overflow': 20,
    'pool_timeout': 30,
    'query_timeout': 45,
    'batch_size': 1000,
    'cache_ttl': 300  # 5 minutes
}
```

**Memory and Processing:**
```python
# config/performance_settings.py
PERFORMANCE_CONFIG = {
    'max_concurrent_campaigns': 50,
    'optimization_frequency': '15_minutes',
    'data_refresh_interval': '5_minutes',
    'report_generation_timeout': 60,
    'ml_model_retrain_frequency': 'weekly'
}
```

---

## 📊 Testing and Validation

### Automated Testing Suite

**Run Complete Test Suite:**
```bash
# Full integration testing
python -m pytest tests/ -v --integration

# Performance testing
python -m pytest tests/performance/ -v

# Security testing
python -m pytest tests/security/ -v

# Expected Results:
# ✅ 47 integration tests passed
# ✅ 12 performance tests passed  
# ✅ 8 security tests passed
# ⚠️  2 tests skipped (missing optional APIs)
```

**Individual Component Testing:**
```bash
# Test campaign optimization
python tests/test_campaign_optimizer.py
# Expected: All bid optimization algorithms working correctly

# Test attribution models
python tests/test_attribution_models.py  
# Expected: Multi-touch attribution calculating within statistical bounds

# Test content generation
python tests/test_content_suite.py
# Expected: AI content generation producing brand-consistent output
```

### Production Readiness Checklist

**Security Validation:**
```bash
# Verify secure configuration
python scripts/security_audit.py

# Check for exposed credentials
python scripts/credential_scan.py

# Validate API rate limiting
python scripts/rate_limit_test.py
```

**Performance Benchmarking:**
```bash
# Campaign optimization performance
python scripts/benchmark_optimization.py
# Target: <30 seconds for 100 campaigns

# Attribution model performance  
python scripts/benchmark_attribution.py
# Target: <60 seconds for 10,000 touchpoints

# Dashboard generation performance
python scripts/benchmark_reporting.py
# Target: <15 seconds for executive dashboard
```

---

## 🚀 First Campaign Optimization

### Quick Start Walkthrough

**Run Your First Optimization:**
```bash
# Initialize with your data
python examples/quick_start_guide.py

# This will:
# 1. Connect to your advertising platforms
# 2. Analyze last 30 days of campaign performance  
# 3. Generate optimization recommendations
# 4. Show projected ROI improvements
```

**Expected First Results:**
```bash
CAMPAIGN OPTIMIZATION COMPLETE
==============================
Campaigns Analyzed: 23
Optimization Opportunities Found: 18
Projected ROAS Improvement: +23%
Recommended Budget Reallocation: $45,000
Statistical Confidence: 87%

Next Steps:
1. Review recommendations in generated report
2. Apply suggested bid adjustments  
3. Monitor performance for 7-14 days
4. Run follow-up optimization cycle
```

### Data Quality Verification

**Ensure Clean Data Pipeline:**
```python
# scripts/data_quality_check.py
from roi_tracker import ROITracker

tracker = ROITracker()
quality_report = tracker.run_data_quality_assessment()

print(f"Data Completeness: {quality_report.completeness_score:.1%}")
print(f"Attribution Accuracy: {quality_report.attribution_accuracy:.1%}")
print(f"Integration Health: {quality_report.integration_status}")

# Target Scores:
# Completeness: >95%
# Attribution Accuracy: >85%
# All Integrations: Healthy
```

---

## 📈 Monitoring and Maintenance

### Automated Health Checks

**Daily System Monitoring:**
```bash
# Set up daily health check cron job
# Add to crontab: 0 6 * * * /path/to/python /path/to/daily_health_check.py

# Monitor API quotas
python scripts/api_quota_monitor.py

# Check system performance
python scripts/performance_monitor.py

# Validate attribution accuracy
python scripts/attribution_validation.py
```

**Weekly Performance Review:**
```bash
# Generate weekly performance summary
python scripts/weekly_performance_review.py

# Output includes:
# - ROI trend analysis
# - Campaign performance changes
# - Attribution model accuracy
# - System performance metrics
```

### Troubleshooting Resources

**Common Issues Resolution:**
1. **API Rate Limits**: Automatically handled with exponential backoff
2. **Attribution Data Gaps**: Fallback models prevent reporting interruption
3. **Performance Degradation**: Auto-scaling configuration adjusts resources
4. **Data Inconsistencies**: Built-in validation and correction algorithms

**Support Channels:**
- **Documentation**: `/docs/troubleshooting.md`
- **GitHub Issues**: Technical problems and bug reports
- **Professional Support**: Enterprise-level implementation assistance

---

## 🎯 Success Metrics

### Implementation Success Indicators

**30-Day Targets:**
- ✅ All API integrations functioning (>99.9% uptime)
- ✅ Attribution model statistical confidence >80%
- ✅ Campaign optimization response time <2 minutes
- ✅ Executive dashboard automated and accurate

**90-Day Performance Goals:**
- 🎯 25-40% improvement in marketing ROI
- 🎯 50% reduction in manual campaign management time
- 🎯 Real-time optimization replacing daily manual reviews
- 🎯 Executive reporting automated with strategic insights

### Business Impact Measurement

**ROI Calculation Framework:**
```python
# Calculate implementation ROI
def calculate_implementation_roi():
    setup_costs = 40  # hours * hourly rate
    monthly_efficiency_savings = 120  # hours saved monthly
    roi_improvement_percentage = 0.35  # 35% average improvement
    
    annual_benefit = (monthly_efficiency_savings * 12 * hourly_rate) + \
                    (marketing_budget * roi_improvement_percentage)
    
    roi = (annual_benefit - setup_costs) / setup_costs
    return roi

# Typical result: 15-25x ROI in first year
```

---

## 💼 Professional Services

**Need expert implementation support?**

As a technical marketing leader with 25+ years of enterprise-scale implementation experience, I provide:

**Implementation Services:**
- **Technical Architecture Review**: Optimize setup for your specific infrastructure
- **Custom Integration Development**: Connect proprietary systems and data sources  
- **Team Training Programs**: Comprehensive education for marketing and technical teams
- **Performance Optimization**: Fine-tune algorithms for maximum ROI

**Strategic Consulting:**
- **Marketing Technology Audit**: Evaluate current stack and optimization opportunities
- **Attribution Strategy**: Design attribution models aligned with business objectives
- **Executive Briefing**: C-suite education on AI marketing transformation
- **Change Management**: Organizational adoption and process optimization

---

**📞 Connect with Sotirios Spyrou**
- **LinkedIn**: https://www.linkedin.com/in/sspyrou/
- **Portfolio**: https://verityai.co
- **Expertise**: Technical Marketing Leadership, AI Implementation, Enterprise Analytics

---

## 📋 Disclaimer

*This technical setup guide is provided as demonstration of advanced marketing technology implementation capabilities. All examples use configuration templates and sample data for illustration purposes. Production implementations should include comprehensive security review, data privacy compliance verification, and performance testing. This material showcases technical marketing leadership expertise and is designed for portfolio demonstration purposes.*

---

*© 2024 Sotirios Spyrou. This implementation guide demonstrates technical marketing leadership combining strategic vision with hands-on AI deployment expertise.*