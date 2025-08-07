"""
Real-time ROI Tracker

Live campaign performance monitoring with immediate optimization opportunities identification.
Delivers dashboard creation, alert systems, and reporting automation.
"""

import asyncio
import logging
import json
from typing import Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import pandas as pd
import numpy as np
from collections import defaultdict

class AlertSeverity(Enum):
    """Alert severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class MetricType(Enum):
    """Types of metrics to track."""
    ROAS = "roas"
    CPA = "cpa"
    CTR = "ctr"
    CONVERSION_RATE = "conversion_rate"
    COST = "cost"
    REVENUE = "revenue"
    IMPRESSIONS = "impressions"
    CLICKS = "clicks"
    CONVERSIONS = "conversions"

@dataclass
class PerformanceMetric:
    """Individual performance metric data point."""
    campaign_id: str
    channel: str
    metric_type: MetricType
    value: float
    timestamp: datetime
    comparison_period_value: Optional[float] = None
    target_value: Optional[float] = None
    
    @property
    def variance_percentage(self) -> Optional[float]:
        """Calculate variance from comparison period."""
        if self.comparison_period_value and self.comparison_period_value != 0:
            return ((self.value - self.comparison_period_value) / self.comparison_period_value) * 100
        return None
    
    @property
    def target_variance_percentage(self) -> Optional[float]:
        """Calculate variance from target."""
        if self.target_value and self.target_value != 0:
            return ((self.value - self.target_value) / self.target_value) * 100
        return None

@dataclass
class Alert:
    """Performance alert."""
    alert_id: str
    campaign_id: str
    channel: str
    metric_type: MetricType
    severity: AlertSeverity
    message: str
    current_value: float
    threshold_value: float
    variance_percentage: float
    timestamp: datetime
    is_resolved: bool = False
    resolution_timestamp: Optional[datetime] = None

@dataclass
class CampaignSnapshot:
    """Campaign performance snapshot."""
    campaign_id: str
    channel: str
    timestamp: datetime
    metrics: Dict[MetricType, float]
    
    @property
    def roas(self) -> float:
        """Return on ad spend."""
        cost = self.metrics.get(MetricType.COST, 0)
        revenue = self.metrics.get(MetricType.REVENUE, 0)
        return revenue / cost if cost > 0 else 0
    
    @property
    def cpa(self) -> float:
        """Cost per acquisition."""
        cost = self.metrics.get(MetricType.COST, 0)
        conversions = self.metrics.get(MetricType.CONVERSIONS, 0)
        return cost / conversions if conversions > 0 else float('inf')
    
    @property
    def ctr(self) -> float:
        """Click-through rate."""
        clicks = self.metrics.get(MetricType.CLICKS, 0)
        impressions = self.metrics.get(MetricType.IMPRESSIONS, 0)
        return clicks / impressions if impressions > 0 else 0
    
    @property
    def conversion_rate(self) -> float:
        """Conversion rate."""
        conversions = self.metrics.get(MetricType.CONVERSIONS, 0)
        clicks = self.metrics.get(MetricType.CLICKS, 0)
        return conversions / clicks if clicks > 0 else 0

class ROITracker:
    """
    Real-time ROI and performance tracking system.
    
    Features:
    - Real-time metric monitoring
    - Automated alert system
    - Performance anomaly detection
    - Executive dashboard generation
    - Historical trend analysis
    - Budget optimization recommendations
    """
    
    def __init__(self, alert_thresholds: Optional[Dict[MetricType, Dict[str, float]]] = None):
        """
        Initialize ROI tracker.
        
        Args:
            alert_thresholds: Custom alert thresholds per metric type
        """
        self.logger = self._setup_logging()
        self.snapshots: List[CampaignSnapshot] = []
        self.alerts: List[Alert] = []
        self.alert_callbacks: List[Callable[[Alert], None]] = []
        
        # Default alert thresholds
        self.alert_thresholds = alert_thresholds or {
            MetricType.ROAS: {'low': -10, 'medium': -20, 'high': -30, 'critical': -50},
            MetricType.CPA: {'low': 10, 'medium': 25, 'high': 50, 'critical': 100},
            MetricType.CTR: {'low': -15, 'medium': -30, 'high': -45, 'critical': -60},
            MetricType.CONVERSION_RATE: {'low': -10, 'medium': -20, 'high': -35, 'critical': -50},
            MetricType.COST: {'low': 20, 'medium': 50, 'high': 100, 'critical': 200}
        }
        
        self.performance_targets = {}
        self.monitoring_active = False
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for ROI tracking."""
        logger = logging.getLogger('roi_tracker')
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def set_performance_targets(self, targets: Dict[str, Dict[MetricType, float]]) -> None:
        """
        Set performance targets for campaigns.
        
        Args:
            targets: Dictionary with campaign_id as key and metrics targets as values
        """
        self.performance_targets = targets
        self.logger.info(f"Performance targets set for {len(targets)} campaigns")
    
    def add_alert_callback(self, callback: Callable[[Alert], None]) -> None:
        """
        Add callback function to be called when alerts are triggered.
        
        Args:
            callback: Function to call with Alert object
        """
        self.alert_callbacks.append(callback)
    
    def record_campaign_snapshot(self, snapshot: CampaignSnapshot) -> None:
        """
        Record a campaign performance snapshot.
        
        Args:
            snapshot: Campaign performance data
        """
        self.snapshots.append(snapshot)
        self.logger.debug(f"Recorded snapshot for campaign {snapshot.campaign_id}")
        
        # Check for alerts
        self._check_performance_alerts(snapshot)
        
        # Maintain rolling window of snapshots (keep last 10k)
        if len(self.snapshots) > 10000:
            self.snapshots = self.snapshots[-10000:]
    
    def get_current_performance(self, campaign_id: str, time_window_hours: int = 24) -> Optional[CampaignSnapshot]:
        """
        Get current performance for a campaign.
        
        Args:
            campaign_id: Campaign identifier
            time_window_hours: Time window for "current" performance
            
        Returns:
            Latest campaign snapshot within time window
        """
        cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
        
        recent_snapshots = [
            s for s in self.snapshots 
            if s.campaign_id == campaign_id and s.timestamp >= cutoff_time
        ]
        
        if recent_snapshots:
            return max(recent_snapshots, key=lambda x: x.timestamp)
        
        return None
    
    def get_performance_trend(self, 
                            campaign_id: str, 
                            metric_type: MetricType, 
                            days: int = 7) -> List[Tuple[datetime, float]]:
        """
        Get performance trend for a campaign and metric.
        
        Args:
            campaign_id: Campaign identifier
            metric_type: Type of metric to analyze
            days: Number of days of history to include
            
        Returns:
            List of (timestamp, value) tuples
        """
        cutoff_time = datetime.now() - timedelta(days=days)
        
        relevant_snapshots = [
            s for s in self.snapshots 
            if s.campaign_id == campaign_id and s.timestamp >= cutoff_time
        ]
        
        trend_data = []
        for snapshot in relevant_snapshots:
            if metric_type == MetricType.ROAS:
                value = snapshot.roas
            elif metric_type == MetricType.CPA:
                value = snapshot.cpa
            elif metric_type == MetricType.CTR:
                value = snapshot.ctr
            elif metric_type == MetricType.CONVERSION_RATE:
                value = snapshot.conversion_rate
            else:
                value = snapshot.metrics.get(metric_type, 0)
            
            trend_data.append((snapshot.timestamp, value))
        
        return sorted(trend_data, key=lambda x: x[0])
    
    def detect_anomalies(self, 
                        campaign_id: str, 
                        metric_type: MetricType,
                        sensitivity: float = 2.0) -> List[Tuple[datetime, float, str]]:
        """
        Detect performance anomalies using statistical analysis.
        
        Args:
            campaign_id: Campaign identifier
            metric_type: Metric to analyze
            sensitivity: Standard deviation multiplier for anomaly detection
            
        Returns:
            List of (timestamp, value, anomaly_type) tuples
        """
        trend_data = self.get_performance_trend(campaign_id, metric_type, days=30)
        
        if len(trend_data) < 10:
            return []
        
        values = [x[1] for x in trend_data]
        mean_value = np.mean(values)
        std_value = np.std(values)
        
        anomalies = []
        
        for timestamp, value in trend_data[-7:]:  # Check last 7 data points
            if abs(value - mean_value) > sensitivity * std_value:
                if value > mean_value + sensitivity * std_value:
                    anomaly_type = "positive_spike"
                else:
                    anomaly_type = "negative_drop"
                
                anomalies.append((timestamp, value, anomaly_type))
        
        return anomalies
    
    def generate_performance_summary(self, time_period_hours: int = 24) -> Dict[str, Dict[str, Union[float, str]]]:
        """
        Generate performance summary for all campaigns.
        
        Args:
            time_period_hours: Time period for summary
            
        Returns:
            Dictionary with campaign performance summaries
        """
        cutoff_time = datetime.now() - timedelta(hours=time_period_hours)
        recent_snapshots = [s for s in self.snapshots if s.timestamp >= cutoff_time]
        
        # Group by campaign
        campaign_data = defaultdict(list)
        for snapshot in recent_snapshots:
            campaign_data[snapshot.campaign_id].append(snapshot)
        
        summary = {}
        
        for campaign_id, snapshots in campaign_data.items():
            if not snapshots:
                continue
            
            # Calculate averages
            latest_snapshot = max(snapshots, key=lambda x: x.timestamp)
            
            total_cost = sum(s.metrics.get(MetricType.COST, 0) for s in snapshots)
            total_revenue = sum(s.metrics.get(MetricType.REVENUE, 0) for s in snapshots)
            total_conversions = sum(s.metrics.get(MetricType.CONVERSIONS, 0) for s in snapshots)
            total_clicks = sum(s.metrics.get(MetricType.CLICKS, 0) for s in snapshots)
            total_impressions = sum(s.metrics.get(MetricType.IMPRESSIONS, 0) for s in snapshots)
            
            avg_roas = total_revenue / total_cost if total_cost > 0 else 0
            avg_cpa = total_cost / total_conversions if total_conversions > 0 else float('inf')
            avg_ctr = total_clicks / total_impressions if total_impressions > 0 else 0
            avg_conversion_rate = total_conversions / total_clicks if total_clicks > 0 else 0
            
            summary[campaign_id] = {
                'channel': latest_snapshot.channel,
                'total_cost': total_cost,
                'total_revenue': total_revenue,
                'total_conversions': total_conversions,
                'avg_roas': avg_roas,
                'avg_cpa': avg_cpa if avg_cpa != float('inf') else 0,
                'avg_ctr': avg_ctr,
                'avg_conversion_rate': avg_conversion_rate,
                'data_points': len(snapshots),
                'last_updated': latest_snapshot.timestamp.isoformat()
            }
        
        return summary
    
    def generate_executive_dashboard(self) -> str:
        """
        Generate executive dashboard with key metrics and insights.
        
        Returns:
            Formatted dashboard string
        """
        summary = self.generate_performance_summary(24)
        active_alerts = [a for a in self.alerts if not a.is_resolved]
        
        dashboard = f"""
MARKETING ROI DASHBOARD
=====================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Monitoring Period: Last 24 Hours

OVERALL PERFORMANCE
==================
Total Campaigns: {len(summary)}
Active Alerts: {len(active_alerts)}
Critical Alerts: {len([a for a in active_alerts if a.severity == AlertSeverity.CRITICAL])}

"""
        
        if summary:
            total_cost = sum(s['total_cost'] for s in summary.values())
            total_revenue = sum(s['total_revenue'] for s in summary.values())
            overall_roas = total_revenue / total_cost if total_cost > 0 else 0
            
            dashboard += f"Portfolio Metrics:\n"
            dashboard += f"- Total Ad Spend: ${total_cost:,.2f}\n"
            dashboard += f"- Total Revenue: ${total_revenue:,.2f}\n"
            dashboard += f"- Portfolio ROAS: {overall_roas:.2f}x\n\n"
        
        # Top performing campaigns
        if summary:
            top_campaigns = sorted(summary.items(), key=lambda x: x[1]['avg_roas'], reverse=True)[:5]
            
            dashboard += "TOP PERFORMING CAMPAIGNS\n"
            dashboard += "=======================\n"
            
            for i, (campaign_id, data) in enumerate(top_campaigns, 1):
                dashboard += f"{i}. {campaign_id} ({data['channel']})\n"
                dashboard += f"   ROAS: {data['avg_roas']:.2f}x | "
                dashboard += f"CPA: ${data['avg_cpa']:.2f} | "
                dashboard += f"Revenue: ${data['total_revenue']:,.2f}\n\n"
        
        # Critical alerts
        critical_alerts = [a for a in active_alerts if a.severity == AlertSeverity.CRITICAL]
        if critical_alerts:
            dashboard += "CRITICAL ALERTS\n"
            dashboard += "==============\n"
            
            for alert in critical_alerts[:5]:
                dashboard += f"⚠️  {alert.campaign_id} ({alert.channel})\n"
                dashboard += f"   {alert.message}\n"
                dashboard += f"   Current: {alert.current_value:.2f} | "
                dashboard += f"Change: {alert.variance_percentage:+.1f}%\n\n"
        
        # Performance recommendations
        dashboard += self._generate_performance_recommendations(summary)
        
        return dashboard
    
    def _check_performance_alerts(self, snapshot: CampaignSnapshot) -> None:
        """Check for performance alerts based on snapshot data."""
        campaign_id = snapshot.campaign_id
        
        # Get comparison data (previous day)
        comparison_snapshots = [
            s for s in self.snapshots 
            if (s.campaign_id == campaign_id and 
                s.timestamp >= datetime.now() - timedelta(days=2) and
                s.timestamp < datetime.now() - timedelta(days=1))
        ]
        
        if not comparison_snapshots:
            return
        
        # Calculate average metrics for comparison period
        comparison_metrics = {}
        for metric_type in MetricType:
            if metric_type == MetricType.ROAS:
                values = [s.roas for s in comparison_snapshots if s.roas > 0]
            elif metric_type == MetricType.CPA:
                values = [s.cpa for s in comparison_snapshots if s.cpa != float('inf')]
            elif metric_type == MetricType.CTR:
                values = [s.ctr for s in comparison_snapshots]
            elif metric_type == MetricType.CONVERSION_RATE:
                values = [s.conversion_rate for s in comparison_snapshots]
            else:
                values = [s.metrics.get(metric_type, 0) for s in comparison_snapshots]
            
            if values:
                comparison_metrics[metric_type] = np.mean(values)
        
        # Check each metric for alerts
        metrics_to_check = {
            MetricType.ROAS: snapshot.roas,
            MetricType.CPA: snapshot.cpa,
            MetricType.CTR: snapshot.ctr,
            MetricType.CONVERSION_RATE: snapshot.conversion_rate,
            MetricType.COST: snapshot.metrics.get(MetricType.COST, 0)
        }
        
        for metric_type, current_value in metrics_to_check.items():
            if metric_type not in comparison_metrics or current_value == 0:
                continue
                
            comparison_value = comparison_metrics[metric_type]
            if comparison_value == 0:
                continue
            
            variance_pct = ((current_value - comparison_value) / comparison_value) * 100
            
            # Determine alert severity
            thresholds = self.alert_thresholds.get(metric_type, {})
            severity = None
            
            # For metrics where decrease is bad (ROAS, CTR, Conversion Rate)
            if metric_type in [MetricType.ROAS, MetricType.CTR, MetricType.CONVERSION_RATE]:
                if variance_pct <= thresholds.get('critical', -50):
                    severity = AlertSeverity.CRITICAL
                elif variance_pct <= thresholds.get('high', -30):
                    severity = AlertSeverity.HIGH
                elif variance_pct <= thresholds.get('medium', -20):
                    severity = AlertSeverity.MEDIUM
                elif variance_pct <= thresholds.get('low', -10):
                    severity = AlertSeverity.LOW
            
            # For metrics where increase is bad (CPA, Cost)
            elif metric_type in [MetricType.CPA, MetricType.COST]:
                if variance_pct >= thresholds.get('critical', 100):
                    severity = AlertSeverity.CRITICAL
                elif variance_pct >= thresholds.get('high', 50):
                    severity = AlertSeverity.HIGH
                elif variance_pct >= thresholds.get('medium', 25):
                    severity = AlertSeverity.MEDIUM
                elif variance_pct >= thresholds.get('low', 10):
                    severity = AlertSeverity.LOW
            
            if severity:
                alert = Alert(
                    alert_id=f"{campaign_id}_{metric_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    campaign_id=campaign_id,
                    channel=snapshot.channel,
                    metric_type=metric_type,
                    severity=severity,
                    message=f"{metric_type.value.replace('_', ' ').title()} {variance_pct:+.1f}% vs yesterday",
                    current_value=current_value,
                    threshold_value=comparison_value,
                    variance_percentage=variance_pct,
                    timestamp=datetime.now()
                )
                
                self.alerts.append(alert)
                self.logger.warning(f"Alert triggered: {alert.message} for {campaign_id}")
                
                # Call alert callbacks
                for callback in self.alert_callbacks:
                    try:
                        callback(alert)
                    except Exception as e:
                        self.logger.error(f"Alert callback failed: {e}")
    
    def resolve_alert(self, alert_id: str, resolution_note: str = "") -> bool:
        """
        Resolve an active alert.
        
        Args:
            alert_id: Alert identifier
            resolution_note: Optional resolution note
            
        Returns:
            True if alert was resolved, False if not found
        """
        for alert in self.alerts:
            if alert.alert_id == alert_id and not alert.is_resolved:
                alert.is_resolved = True
                alert.resolution_timestamp = datetime.now()
                self.logger.info(f"Alert {alert_id} resolved: {resolution_note}")
                return True
        
        return False
    
    def get_budget_optimization_recommendations(self) -> Dict[str, Dict[str, Union[str, float]]]:
        """
        Generate budget optimization recommendations based on performance data.
        
        Returns:
            Dictionary with optimization recommendations per campaign
        """
        summary = self.generate_performance_summary(168)  # Last week
        recommendations = {}
        
        if len(summary) < 2:
            return recommendations
        
        # Calculate performance rankings
        campaigns_by_roas = sorted(summary.items(), key=lambda x: x[1]['avg_roas'], reverse=True)
        campaigns_by_cpa = sorted(summary.items(), key=lambda x: x[1]['avg_cpa'])
        
        median_roas = np.median([data['avg_roas'] for _, data in summary.items()])
        median_cpa = np.median([data['avg_cpa'] for _, data in summary.items() if data['avg_cpa'] > 0])
        
        for campaign_id, data in summary.items():
            roas = data['avg_roas']
            cpa = data['avg_cpa']
            
            if roas > median_roas * 1.5 and cpa < median_cpa * 0.7:
                recommendation = "INCREASE_BUDGET"
                impact = "High ROI opportunity - consider 25-50% budget increase"
                confidence = 0.9
            
            elif roas > median_roas * 1.2:
                recommendation = "MODERATE_INCREASE"
                impact = "Above average performance - consider 10-25% budget increase"
                confidence = 0.75
            
            elif roas < median_roas * 0.5 or cpa > median_cpa * 2:
                recommendation = "DECREASE_BUDGET"
                impact = "Poor performance - consider 30-50% budget reduction"
                confidence = 0.85
            
            elif roas < median_roas * 0.8:
                recommendation = "OPTIMIZE"
                impact = "Below average performance - optimize targeting and creative"
                confidence = 0.7
            
            else:
                recommendation = "MAINTAIN"
                impact = "Performance in line with portfolio average"
                confidence = 0.6
            
            recommendations[campaign_id] = {
                'recommendation': recommendation,
                'impact_description': impact,
                'confidence_score': confidence,
                'current_roas': roas,
                'median_roas': median_roas,
                'current_cpa': cpa,
                'median_cpa': median_cpa
            }
        
        return recommendations
    
    def _generate_performance_recommendations(self, summary: Dict) -> str:
        """Generate performance recommendations section."""
        if not summary:
            return ""
        
        recommendations = self.get_budget_optimization_recommendations()
        
        section = "OPTIMIZATION RECOMMENDATIONS\n"
        section += "==========================\n"
        
        # High priority recommendations
        high_impact_recs = {
            k: v for k, v in recommendations.items() 
            if v['recommendation'] in ['INCREASE_BUDGET', 'DECREASE_BUDGET'] and v['confidence_score'] > 0.8
        }
        
        if high_impact_recs:
            section += "High Impact Opportunities:\n"
            for campaign_id, rec in list(high_impact_recs.items())[:3]:
                section += f"• {campaign_id}: {rec['impact_description']}\n"
            section += "\n"
        
        # Budget reallocation summary
        increase_budget = [k for k, v in recommendations.items() if 'INCREASE' in v['recommendation']]
        decrease_budget = [k for k, v in recommendations.items() if 'DECREASE' in v['recommendation']]
        
        if increase_budget and decrease_budget:
            section += f"Budget Reallocation Opportunity:\n"
            section += f"• Scale up: {len(increase_budget)} campaigns\n"
            section += f"• Scale down: {len(decrease_budget)} campaigns\n"
            section += f"• Net optimization potential: Significant\n\n"
        
        return section
    
    def export_performance_data(self, 
                              campaign_ids: Optional[List[str]] = None,
                              days: int = 30) -> pd.DataFrame:
        """
        Export performance data to pandas DataFrame.
        
        Args:
            campaign_ids: Optional list of campaign IDs to filter
            days: Number of days of history to export
            
        Returns:
            DataFrame with performance data
        """
        cutoff_time = datetime.now() - timedelta(days=days)
        
        filtered_snapshots = [
            s for s in self.snapshots 
            if s.timestamp >= cutoff_time and 
            (campaign_ids is None or s.campaign_id in campaign_ids)
        ]
        
        data = []
        for snapshot in filtered_snapshots:
            row = {
                'campaign_id': snapshot.campaign_id,
                'channel': snapshot.channel,
                'timestamp': snapshot.timestamp,
                'roas': snapshot.roas,
                'cpa': snapshot.cpa,
                'ctr': snapshot.ctr,
                'conversion_rate': snapshot.conversion_rate,
                **{f'metric_{metric.value}': value for metric, value in snapshot.metrics.items()}
            }
            data.append(row)
        
        return pd.DataFrame(data)
    
    async def start_monitoring(self, check_interval_seconds: int = 300) -> None:
        """
        Start continuous monitoring with specified interval.
        
        Args:
            check_interval_seconds: How often to check for new data
        """
        self.monitoring_active = True
        self.logger.info(f"Started monitoring with {check_interval_seconds}s interval")
        
        while self.monitoring_active:
            try:
                # This would integrate with actual data sources
                # For demo purposes, we'll just log
                active_alerts = len([a for a in self.alerts if not a.is_resolved])
                if active_alerts > 0:
                    self.logger.info(f"Monitoring: {active_alerts} active alerts")
                
                await asyncio.sleep(check_interval_seconds)
                
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    def stop_monitoring(self) -> None:
        """Stop continuous monitoring."""
        self.monitoring_active = False
        self.logger.info("Monitoring stopped")


def main():
    """Example usage demonstration."""
    # Initialize tracker
    tracker = ROITracker()
    
    # Add example alert callback
    def alert_handler(alert: Alert):
        print(f"ALERT: {alert.severity.value.upper()} - {alert.message}")
    
    tracker.add_alert_callback(alert_handler)
    
    # Create sample performance data
    campaigns = ['campaign_1', 'campaign_2', 'campaign_3']
    channels = ['paid_search', 'social_media', 'display']
    
    # Generate historical snapshots
    base_time = datetime.now() - timedelta(days=7)
    
    for day in range(7):
        for hour in range(0, 24, 6):  # Every 6 hours
            timestamp = base_time + timedelta(days=day, hours=hour)
            
            for i, campaign in enumerate(campaigns):
                # Simulate performance variation
                base_roas = 3.5 + np.random.normal(0, 0.5)
                base_cost = 1000 + np.random.normal(0, 200)
                
                # Simulate performance degradation for campaign_2 in recent days
                if campaign == 'campaign_2' and day >= 5:
                    base_roas *= 0.7  # 30% drop in ROAS
                    base_cost *= 1.3  # 30% increase in cost
                
                metrics = {
                    MetricType.COST: max(0, base_cost),
                    MetricType.REVENUE: max(0, base_cost * base_roas),
                    MetricType.IMPRESSIONS: int(base_cost * 20),
                    MetricType.CLICKS: int(base_cost * 0.5),
                    MetricType.CONVERSIONS: int(base_cost * 0.02)
                }
                
                snapshot = CampaignSnapshot(
                    campaign_id=campaign,
                    channel=channels[i],
                    timestamp=timestamp,
                    metrics=metrics
                )
                
                tracker.record_campaign_snapshot(snapshot)
    
    # Generate dashboard
    dashboard = tracker.generate_executive_dashboard()
    print(dashboard)
    
    # Show budget recommendations
    recommendations = tracker.get_budget_optimization_recommendations()
    print("\nBUDGET OPTIMIZATION RECOMMENDATIONS:")
    print("=" * 40)
    
    for campaign_id, rec in recommendations.items():
        print(f"\n{campaign_id}:")
        print(f"  Action: {rec['recommendation']}")
        print(f"  Rationale: {rec['impact_description']}")
        print(f"  Confidence: {rec['confidence_score']:.1%}")
    
    # Show anomaly detection
    print("\nANOMALY DETECTION:")
    print("=" * 20)
    
    for campaign in campaigns:
        anomalies = tracker.detect_anomalies(campaign, MetricType.ROAS)
        if anomalies:
            print(f"\n{campaign} ROAS anomalies:")
            for timestamp, value, anomaly_type in anomalies:
                print(f"  {timestamp.strftime('%Y-%m-%d')}: {value:.2f} ({anomaly_type})")


if __name__ == "__main__":
    main()
