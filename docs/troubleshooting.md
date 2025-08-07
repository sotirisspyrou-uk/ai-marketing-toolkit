# Troubleshooting Guide

**Professional support for AI Marketing Toolkit issues and optimization**

*Expert solutions by [Sotirios Spyrou](https://www.linkedin.com/in/sspyrou/) - Technical Marketing Leadership*

---

## 🚨 Quick Issue Resolution

**Most Common Issues (90% of problems):**

1. **API Authentication Failures** → Section 2.1
2. **Attribution Model Low Confidence** → Section 3.2
3. **Campaign Optimization Not Running** → Section 4.1
4. **Performance Degradation** → Section 5.1
5. **Dashboard Data Inconsistencies** → Section 6.2

**Emergency Support Checklist:**
- ✅ Check system status: `python scripts/health_check.py`
- ✅ Verify API connections: `python scripts/api_status.py`
- ✅ Review error logs: `tail -100 logs/application.log`
- ✅ Test core functions: `python scripts/integration_test.py`

---

## 🔐 Authentication & API Issues

### 2.1 Google Ads API Connection Failed

**Symptoms:**
```
ERROR: google.ads.googleads.errors.GoogleAdsException: 
Request contains an invalid customer ID
```

**Root Causes & Solutions:**

**Issue A: Invalid Customer ID Format**
```python
# ❌ Wrong format
GOOGLE_ADS_CUSTOMER_ID=1234567890

# ✅ Correct format  
GOOGLE_ADS_CUSTOMER_ID=123-456-7890
```

**Issue B: Developer Token Not Approved**
```bash
# Check token status
python -c "
from google.ads.googleads.client import GoogleAdsClient
client = GoogleAdsClient.load_from_env()
customer_service = client.get_service('CustomerService')
print('Developer token is active')
"
```

**Issue C: OAuth2 Token Expired**
```bash
# Regenerate refresh token
python examples/generate_google_ads_token.py

# Update .env file with new refresh token
GOOGLE_ADS_REFRESH_TOKEN=1//your-new-refresh-token
```

**Advanced Diagnostics:**
```python
# scripts/diagnose_google_ads.py
from google.ads.googleads.client import GoogleAdsClient

def diagnose_google_ads_connection():
    try:
        client = GoogleAdsClient.load_from_env()
        customer_service = client.get_service('CustomerService')
        
        # Test basic connection
        customers = customer_service.list_accessible_customers()
        print(f"✅ Connected to {len(customers.resource_names)} accounts")
        
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
```

### 2.2 Facebook Marketing API Issues

**Symptoms:**
```
FacebookRequestError: (#100) The App_id in the input_token did not match the Viewable App_id
```

**Solutions:**

**App ID Mismatch:**
```bash
# Verify app configuration
python -c "
import os
print(f'App ID in token: {os.getenv(\"FACEBOOK_APP_ID\")}')
print(f'Check token at: https://developers.facebook.com/tools/debug/accesstoken/')
"
```

**Token Permissions Missing:**
```python
# Check token permissions
import requests
token = os.getenv('FACEBOOK_ACCESS_TOKEN')
response = requests.get(f'https://graph.facebook.com/me/permissions?access_token={token}')
permissions = response.json()

required_permissions = ['ads_management', 'ads_read', 'business_management']
missing = [p for p in required_permissions if p not in [item['permission'] for item in permissions['data']]]

if missing:
    print(f"❌ Missing permissions: {missing}")
    print("Visit: https://developers.facebook.com/tools/explorer/")
```

### 2.3 OpenAI API Rate Limits

**Symptoms:**
```
RateLimitError: Rate limit reached for requests
```

**Immediate Solutions:**
```python
# Implement exponential backoff
import time
import random
from openai import OpenAI

def robust_openai_call(prompt, max_retries=3):
    client = OpenAI()
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}]
            )
            return response
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"Rate limit hit. Waiting {wait_time:.1f}s...")
                time.sleep(wait_time)
            else:
                raise e
```

**Long-term Optimization:**
```python
# Optimize token usage
def optimize_content_generation():
    # Batch multiple requests
    # Use shorter prompts where possible
    # Implement local caching
    # Consider GPT-3.5-turbo for non-critical tasks
    pass
```

---

## 📊 Attribution Model Issues

### 3.1 Low Statistical Confidence

**Symptoms:**
```
WARNING: Attribution model confidence only 67%, below 80% threshold
Recommendations may not be statistically significant
```

**Root Cause Analysis:**
```python
# scripts/attribution_diagnostics.py
from attribution_models import AttributionModelBuilder

def diagnose_attribution_confidence():
    builder = AttributionModelBuilder()
    diagnostics = builder.diagnose_data_quality()
    
    print(f"Total conversions: {diagnostics.total_conversions}")
    print(f"Average path length: {diagnostics.avg_path_length}")
    print(f"Data completeness: {diagnostics.completeness_percentage:.1%}")
    
    # Minimum requirements for confidence
    if diagnostics.total_conversions < 1000:
        print("❌ Need at least 1000 conversions for reliable attribution")
    if diagnostics.avg_path_length < 2:
        print("❌ Customer journeys too simple for multi-touch attribution")
    if diagnostics.completeness_percentage < 0.85:
        print("❌ Too much missing data in customer journeys")
```

**Solutions by Issue:**

**Insufficient Data Volume:**
```python
# Extend lookback window
ATTRIBUTION_CONFIG = {
    'lookback_window_days': 90,  # Increased from 30
    'minimum_touchpoints': 500,  # Reduced from 1000
    'confidence_threshold': 0.75, # Temporarily reduced
}
```

**Data Quality Issues:**
```python
# Improve data collection
def improve_attribution_data():
    # Enable cross-device tracking
    # Implement server-side tracking
    # Add offline conversion imports
    # Fill data gaps with probabilistic matching
    pass
```

### 3.2 Attribution Results Don't Match Platform Data

**Symptoms:**
- Google Ads reports $100K revenue
- Attribution model shows $75K for Google Ads
- CFO questions data accuracy

**Explanation & Resolution:**
```python
# This is expected behavior - here's why:
def explain_attribution_differences():
    """
    Platform Attribution vs Multi-Touch Attribution
    
    Google Ads: Last-click attribution
    - Only counts conversions where Google Ads was final touch
    - Ignores influence of other channels
    - Overvalues bottom-funnel, undervalues awareness
    
    Multi-Touch Attribution: 
    - Distributes credit across entire customer journey
    - More accurate representation of channel contribution
    - Better for budget optimization decisions
    """
    
    reconciliation_report = {
        'google_ads_last_click': 100000,  # What Google Ads reports
        'google_ads_multi_touch': 75000,  # More accurate attribution
        'attribution_difference': 25000,   # Credit redistributed to other channels
        'total_revenue_same': True,        # Total revenue unchanged
        'budget_accuracy': 'improved'      # Better allocation decisions
    }
    
    return reconciliation_report
```

**Executive Communication Template:**
```
Attribution Model Reconciliation Report
=====================================

Platform Reporting vs Multi-Touch Attribution

Google Ads Platform:    $100,000 (last-click only)
Google Ads Multi-Touch: $75,000  (journey-based)
Difference:            $25,000   (redistributed to other channels)

Key Points:
✅ Total revenue unchanged ($500K)
✅ Budget allocation now more accurate
✅ All channels get proper credit for customer journey
✅ ROI optimization improved by 23%

This difference indicates our other channels (email, social, display) 
were previously under-credited for their contribution to conversions.
```

---

## ⚡ Campaign Optimization Issues

### 4.1 Optimization Engine Not Running

**Symptoms:**
```
INFO: No optimization recommendations generated
Campaign performance unchanged for 48+ hours
```

**Diagnostic Steps:**
```bash
# Check optimization service status
python scripts/check_optimization_status.py

# Verify campaign data freshness
python scripts/check_data_freshness.py

# Test optimization algorithms
python scripts/test_optimization_engine.py
```

**Common Fixes:**

**Issue A: Insufficient Performance Data**
```python
def fix_data_threshold_issues():
    # Lower minimum data requirements temporarily
    optimization_config = {
        'minimum_impressions': 1000,  # Reduced from 10000
        'minimum_clicks': 50,         # Reduced from 500
        'data_freshness_hours': 48,   # Increased from 24
    }
    
    # This allows optimization on smaller campaigns
    return optimization_config
```

**Issue B: API Rate Limiting**
```python
# Add intelligent rate limiting
import time
from functools import wraps

def rate_limit_decorator(calls_per_minute=60):
    def decorator(func):
        last_called = [0.0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = 60.0 / calls_per_minute - elapsed
            
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        
        return wrapper
    return decorator

@rate_limit_decorator(calls_per_minute=50)
def optimize_campaign_bids():
    # Your optimization logic here
    pass
```

### 4.2 Bid Adjustments Too Aggressive

**Symptoms:**
- Campaign spend increases 300% overnight
- Quality scores drop significantly
- CFO calls emergency meeting

**Immediate Action:**
```python
# Emergency bid reset
def emergency_bid_reset():
    from campaign_optimizer import CampaignOptimizer
    
    optimizer = CampaignOptimizer()
    
    # Get all campaigns with bid adjustments in last 24 hours
    recent_changes = optimizer.get_recent_bid_changes(hours=24)
    
    # Revert aggressive changes (>50% adjustment)
    for campaign_id, change in recent_changes.items():
        if abs(change) > 0.50:  # More than 50% change
            optimizer.revert_bid_adjustment(campaign_id)
            print(f"Reverted {campaign_id}: {change:.1%} → baseline")
```

**Root Cause & Prevention:**
```python
# Implement bid adjustment limits
OPTIMIZATION_LIMITS = {
    'max_bid_increase': 0.25,      # Maximum 25% increase
    'max_bid_decrease': 0.30,      # Maximum 30% decrease  
    'daily_budget_limit': 0.15,    # Maximum 15% daily change
    'quality_score_threshold': 6,  # Don't optimize if QS < 6
}

def safe_bid_optimization(campaign_metrics):
    adjustments = calculate_optimal_adjustments(campaign_metrics)
    
    # Apply safety limits
    for campaign_id, adjustment in adjustments.items():
        # Limit adjustment size
        adjustment = max(-0.30, min(0.25, adjustment))
        
        # Check quality score
        if campaign_metrics[campaign_id].quality_score < 6:
            adjustment = min(adjustment, 0)  # Only allow decreases
        
        adjustments[campaign_id] = adjustment
    
    return adjustments
```

---

## 🐛 Performance Issues

### 5.1 Slow Dashboard Loading

**Symptoms:**
- Executive dashboard takes >60 seconds to load
- Browser timeouts during report generation
- C-suite complaints about system performance

**Performance Profiling:**
```python
# scripts/profile_dashboard_performance.py
import time
import cProfile
from roi_tracker import ROITracker

def profile_dashboard_generation():
    profiler = cProfile.Profile()
    profiler.enable()
    
    start_time = time.time()
    tracker = ROITracker()
    dashboard_data = tracker.generate_executive_dashboard()
    end_time = time.time()
    
    profiler.disable()
    
    print(f"Dashboard generation took: {end_time - start_time:.2f} seconds")
    profiler.print_stats(sort='cumulative')
```

**Optimization Solutions:**

**Database Query Optimization:**
```python
# Before: Multiple individual queries
def slow_dashboard_data():
    campaigns = get_all_campaigns()  # 1 query
    for campaign in campaigns:
        performance = get_campaign_performance(campaign.id)  # N queries
        attribution = get_attribution_data(campaign.id)     # N queries
    
# After: Bulk data retrieval
def fast_dashboard_data():
    # Single query with joins
    campaign_data = get_bulk_campaign_data()  # 1 optimized query
    performance_data = get_bulk_performance_data()  # 1 query
    attribution_data = get_bulk_attribution_data()  # 1 query
```

**Caching Implementation:**
```python
from functools import lru_cache
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

@lru_cache(maxsize=100)
def cached_campaign_metrics(campaign_id, date_range):
    """Cache expensive calculations"""
    cache_key = f"metrics:{campaign_id}:{date_range}"
    
    # Check cache first
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result)
    
    # Calculate and cache
    metrics = expensive_calculation(campaign_id, date_range)
    redis_client.setex(cache_key, 300, json.dumps(metrics))  # 5 minute TTL
    
    return metrics
```

### 5.2 Memory Usage Issues

**Symptoms:**
```
MemoryError: Unable to allocate array
Process killed by system (OOM)
```

**Memory Optimization:**

**Chunked Data Processing:**
```python
def process_large_dataset_efficiently():
    chunk_size = 10000
    
    # Instead of loading all data at once
    for chunk_start in range(0, total_records, chunk_size):
        chunk_end = min(chunk_start + chunk_size, total_records)
        
        # Process chunk
        chunk_data = load_data_chunk(chunk_start, chunk_end)
        process_chunk(chunk_data)
        
        # Free memory
        del chunk_data
        gc.collect()
```

**Memory Profiling:**
```python
# Monitor memory usage
import psutil
import os

def monitor_memory_usage():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    
    print(f"Memory Usage: {memory_info.rss / 1024 / 1024:.1f} MB")
    print(f"Memory Percent: {process.memory_percent():.1f}%")
    
    if memory_info.rss > 1024 * 1024 * 1024:  # > 1GB
        print("⚠️  High memory usage detected")
        # Trigger garbage collection
        import gc
        gc.collect()
```

---

## 📈 Data Quality Issues

### 6.1 Missing Conversion Data

**Symptoms:**
- Attribution models show 0% conversion attribution
- ROI calculations return negative values
- Executive dashboards show blank metrics

**Diagnostic Process:**
```python
def diagnose_conversion_tracking():
    # Check conversion import status
    conversion_sources = check_conversion_sources()
    
    for source, status in conversion_sources.items():
        print(f"{source}: {status}")
        
        if status != 'active':
            print(f"⚠️  Issue with {source} conversion tracking")
            
    # Verify conversion attribution
    attribution_coverage = check_attribution_coverage()
    
    if attribution_coverage < 0.80:
        print(f"❌ Only {attribution_coverage:.1%} of conversions have attribution data")
```

**Resolution Steps:**

**Step 1: Verify Tracking Implementation**
```javascript
// Check website tracking
gtag('event', 'purchase', {
  'transaction_id': '12345',
  'value': 25.42,
  'currency': 'USD',
  'items': [{
    'item_id': 'SKU123',
    'item_name': 'Product Name',
    'quantity': 1,
    'price': 25.42
  }]
});

// Verify tracking is firing
console.log('Conversion tracking active');
```

**Step 2: Import Offline Conversions**
```python
def import_offline_conversions():
    # CRM integration for offline conversions
    crm_conversions = get_crm_conversions()
    
    for conversion in crm_conversions:
        # Match to marketing touchpoints
        matched_journey = match_conversion_to_journey(conversion)
        
        if matched_journey:
            import_conversion_to_attribution_model(conversion, matched_journey)
```

### 6.2 Data Discrepancies Between Platforms

**Symptoms:**
- Google Ads: 1,000 conversions
- Facebook Ads: 800 conversions  
- Attribution Model: 1,200 total conversions
- Finance Team: "Which number is correct?"

**Reconciliation Process:**
```python
def create_data_reconciliation_report():
    platform_data = {
        'google_ads': get_google_ads_conversions(),
        'facebook_ads': get_facebook_conversions(),
        'linkedin_ads': get_linkedin_conversions(),
        'attribution_model': get_attribution_conversions()
    }
    
    reconciliation = {
        'total_unique_conversions': deduplicate_conversions(platform_data),
        'platform_overlap': calculate_overlap(platform_data),
        'discrepancy_reasons': analyze_discrepancies(platform_data)
    }
    
    # Generate executive explanation
    explanation = """
    Data Reconciliation Explanation:
    
    Platform Numbers vs Attribution Model:
    • Each platform reports conversions it influenced
    • Same conversion may be counted by multiple platforms
    • Attribution model deduplicates and assigns fractional credit
    • Total unique conversions: {total_unique}
    
    Discrepancies are normal and expected in multi-platform marketing.
    """.format(total_unique=reconciliation['total_unique_conversions'])
    
    return reconciliation, explanation
```

---

## 🔧 Advanced Troubleshooting

### 7.1 Custom Attribution Model Issues

**Creating Debug Attribution Model:**
```python
class DebugAttributionModel:
    def __init__(self):
        self.debug_mode = True
        self.step_logs = []
    
    def calculate_attribution(self, customer_journeys):
        if self.debug_mode:
            print(f"Processing {len(customer_journeys)} customer journeys...")
        
        for i, journey in enumerate(customer_journeys):
            if self.debug_mode:
                self.step_logs.append(f"Journey {i}: {len(journey.touchpoints)} touchpoints")
            
            # Your attribution logic here
            attribution = self.process_journey(journey)
            
            if self.debug_mode and i < 3:  # Log first 3 journeys
                print(f"Journey {i} attribution: {attribution}")
        
        return self.aggregate_attribution()
    
    def generate_debug_report(self):
        return {
            'step_logs': self.step_logs,
            'processing_stats': self.get_processing_stats(),
            'data_quality_metrics': self.calculate_data_quality()
        }
```

### 7.2 Integration Testing Framework

**Comprehensive Integration Testing:**
```python
# tests/integration/test_full_pipeline.py
import pytest
from datetime import datetime, timedelta

class TestFullPipeline:
    def test_complete_optimization_workflow(self):
        """Test entire optimization pipeline"""
        
        # 1. Data ingestion
        campaign_data = self.ingest_test_campaign_data()
        assert len(campaign_data) > 0
        
        # 2. Attribution modeling
        attribution_result = self.run_attribution_model(campaign_data)
        assert attribution_result.statistical_significance > 0.80
        
        # 3. Optimization recommendations
        recommendations = self.generate_optimizations(attribution_result)
        assert len(recommendations) > 0
        
        # 4. Executive reporting
        executive_report = self.generate_executive_report(
            attribution_result, recommendations
        )
        assert executive_report.is_valid()
        
    def test_error_recovery(self):
        """Test system behavior when APIs fail"""
        
        # Simulate API failures
        with mock.patch('google_ads_client.get_campaigns', side_effect=Exception):
            result = self.run_optimization_with_fallback()
            
            # Should fall back gracefully
            assert result.status == 'partial_success'
            assert 'google_ads_unavailable' in result.warnings
```

---

## 🆘 Emergency Procedures

### 8.1 System Recovery Checklist

**When Everything Breaks:**

```bash
#!/bin/bash
# Emergency recovery script

echo "🚨 AI Marketing Toolkit Emergency Recovery"
echo "========================================"

# 1. Stop all running processes
echo "1. Stopping optimization processes..."
pkill -f "campaign_optimizer"
pkill -f "roi_tracker"

# 2. Backup current state
echo "2. Creating system backup..."
python scripts/emergency_backup.py

# 3. Reset to known good state
echo "3. Resetting to stable configuration..."
git checkout HEAD~1  # Go back one commit
pip install -r requirements.txt --force-reinstall

# 4. Run health check
echo "4. Running system health check..."
python scripts/comprehensive_health_check.py

# 5. Restart services
echo "5. Restarting services..."
python scripts/restart_services.py

echo "✅ Emergency recovery complete"
echo "Check logs at: logs/emergency_recovery_$(date +%Y%m%d_%H%M%S).log"
```

### 8.2 Incident Response Protocol

**For Production Issues:**

1. **Immediate Response (0-15 minutes):**
   - Stop automated optimizations
   - Preserve current bid settings
   - Notify stakeholders of issue

2. **Assessment (15-30 minutes):**
   - Identify root cause
   - Estimate impact scope
   - Determine recovery timeline

3. **Communication Template:**
```
Subject: AI Marketing Toolkit - Service Issue [RESOLVED/INVESTIGATING]

Status: [INVESTIGATING/RESOLVED]
Impact: [Campaign optimization paused/Attribution reporting delayed]
Affected Systems: [Google Ads/Facebook Ads/Executive Dashboards]

Current Actions:
• Automated optimizations safely paused
• Manual campaign management resumed
• Root cause analysis in progress

Timeline:
• Issue detected: [Time]
• Investigation started: [Time]
• Expected resolution: [Time]

Next Update: [Time]

Contact: [Your email] for urgent questions
```

---

## 💼 Professional Support

**When to Escalate to Professional Services:**

1. **Enterprise Integration Issues**: Custom API integrations, security requirements
2. **Performance at Scale**: >1000 campaigns, >10M monthly impressions
3. **Custom Attribution Models**: Industry-specific attribution logic
4. **Executive Training**: C-suite education on AI marketing transformation

**Available Support Levels:**

**Technical Consulting:**
- Advanced troubleshooting and performance optimization
- Custom integration development
- Security and compliance audits
- Team training and skill development

**Strategic Implementation:**
- Marketing technology architecture design
- Change management and organizational adoption
- Executive briefing and board presentations
- Ongoing optimization and performance review

---

**📞 Connect with Sotirios Spyrou**
- **LinkedIn**: https://www.linkedin.com/in/sspyrou/
- **Portfolio**: https://verityai.co
- **Expertise**: Technical Marketing Leadership, AI Implementation, Enterprise Troubleshooting

---

## 📚 Additional Resources

### Documentation Links
- **Setup Guide**: `/docs/technical-setup.md`
- **Executive Guide**: `/docs/executive-guide.md`
- **API Documentation**: `/docs/api-reference.md`
- **Performance Guide**: `/docs/performance-optimization.md`

### Community Support
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Technical questions and best practices
- **Community Wiki**: User-contributed solutions and tips

---

## 📋 Disclaimer

*This troubleshooting guide is provided as demonstration of advanced marketing technology support capabilities. All examples use simulated error scenarios and template solutions for illustration purposes. Production troubleshooting should include comprehensive system analysis, security review, and backup procedures. This material showcases technical marketing leadership expertise and is designed for portfolio demonstration purposes.*

---

*© 2024 Sotirios Spyrou. This troubleshooting guide demonstrates technical marketing leadership combining deep technical knowledge with practical enterprise support experience.*