"""
Application Configuration Management

Central configuration for the AI Marketing Toolkit.
Handles environment variables, API credentials, and application settings.
"""

import os
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

@dataclass
class APICredentials:
    """API credentials configuration."""
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_ads_developer_token: Optional[str] = None
    google_ads_client_id: Optional[str] = None
    google_ads_client_secret: Optional[str] = None
    google_ads_refresh_token: Optional[str] = None
    facebook_access_token: Optional[str] = None
    facebook_app_secret: Optional[str] = None
    facebook_app_id: Optional[str] = None
    linkedin_access_token: Optional[str] = None
    linkedin_client_id: Optional[str] = None
    linkedin_client_secret: Optional[str] = None
    google_analytics_property_id: Optional[str] = None
    google_analytics_credentials_path: Optional[str] = None

@dataclass
class DatabaseConfig:
    """Database configuration."""
    database_url: str = "sqlite:///marketing_data.db"
    redis_url: str = "redis://localhost:6379"
    connection_pool_size: int = 10
    connection_timeout: int = 30

@dataclass
class LoggingConfig:
    """Logging configuration."""
    log_level: str = "INFO"
    log_file_path: str = "logs/marketing_toolkit.log"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    max_log_size_mb: int = 100
    backup_count: int = 5

@dataclass
class MonitoringConfig:
    """Performance monitoring configuration."""
    monitoring_interval_seconds: int = 300
    alert_email_recipients: List[str] = None
    slack_webhook_url: Optional[str] = None
    dashboard_refresh_interval: int = 3600
    dashboard_port: int = 8080
    dashboard_host: str = "localhost"

@dataclass
class AttributionConfig:
    """Attribution model configuration."""
    default_attribution_model: str = "data_driven"
    attribution_lookback_days: int = 30
    min_conversions_for_significance: int = 50
    confidence_level: float = 0.95
    time_decay_factor: float = 0.1

@dataclass
class ContentGenerationConfig:
    """Content generation configuration."""
    default_brand_tone: str = "professional"
    content_quality_threshold: float = 0.8
    max_content_generations_per_hour: int = 100
    default_openai_model: str = "gpt-4"
    default_anthropic_model: str = "claude-3-sonnet-20240229"
    max_tokens_per_request: int = 4000

@dataclass
class ROITrackingConfig:
    """ROI tracking configuration."""
    roas_alert_threshold_low: float = -10.0
    roas_alert_threshold_critical: float = -50.0
    cpa_alert_threshold_high: float = 50.0
    cpa_alert_threshold_critical: float = 100.0
    ctr_alert_threshold_low: float = -15.0
    conversion_rate_alert_threshold_low: float = -10.0
    data_retention_days: int = 365

@dataclass
class SecurityConfig:
    """Security configuration."""
    api_rate_limit_per_minute: int = 60
    session_secret_key: Optional[str] = None
    encryption_key: Optional[str] = None
    allowed_origins: List[str] = None
    jwt_expiration_hours: int = 24

class Settings:
    """
    Central application settings manager.
    
    Loads configuration from environment variables and provides
    typed access to all application settings.
    """
    
    def __init__(self):
        """Initialize settings from environment variables."""
        self.api_credentials = self._load_api_credentials()
        self.database = self._load_database_config()
        self.logging = self._load_logging_config()
        self.monitoring = self._load_monitoring_config()
        self.attribution = self._load_attribution_config()
        self.content_generation = self._load_content_generation_config()
        self.roi_tracking = self._load_roi_tracking_config()
        self.security = self._load_security_config()
        
        # Application metadata
        self.app_name = "AI Marketing Toolkit"
        self.app_version = "1.0.0"
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        
        # Validate critical settings
        self._validate_settings()
    
    def _load_api_credentials(self) -> APICredentials:
        """Load API credentials from environment variables."""
        return APICredentials(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            google_ads_developer_token=os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
            google_ads_client_id=os.getenv("GOOGLE_ADS_CLIENT_ID"),
            google_ads_client_secret=os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
            google_ads_refresh_token=os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
            facebook_access_token=os.getenv("FACEBOOK_ACCESS_TOKEN"),
            facebook_app_secret=os.getenv("FACEBOOK_APP_SECRET"),
            facebook_app_id=os.getenv("FACEBOOK_APP_ID"),
            linkedin_access_token=os.getenv("LINKEDIN_ACCESS_TOKEN"),
            linkedin_client_id=os.getenv("LINKEDIN_CLIENT_ID"),
            linkedin_client_secret=os.getenv("LINKEDIN_CLIENT_SECRET"),
            google_analytics_property_id=os.getenv("GOOGLE_ANALYTICS_PROPERTY_ID"),
            google_analytics_credentials_path=os.getenv("GOOGLE_ANALYTICS_CREDENTIALS_PATH")
        )
    
    def _load_database_config(self) -> DatabaseConfig:
        """Load database configuration."""
        return DatabaseConfig(
            database_url=os.getenv("DATABASE_URL", "sqlite:///marketing_data.db"),
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379"),
            connection_pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
            connection_timeout=int(os.getenv("DB_TIMEOUT", "30"))
        )
    
    def _load_logging_config(self) -> LoggingConfig:
        """Load logging configuration."""
        return LoggingConfig(
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_file_path=os.getenv("LOG_FILE_PATH", "logs/marketing_toolkit.log"),
            log_format=os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
            max_log_size_mb=int(os.getenv("MAX_LOG_SIZE_MB", "100")),
            backup_count=int(os.getenv("LOG_BACKUP_COUNT", "5"))
        )
    
    def _load_monitoring_config(self) -> MonitoringConfig:
        """Load monitoring configuration."""
        alert_emails = os.getenv("ALERT_EMAIL_RECIPIENTS", "")
        email_list = [email.strip() for email in alert_emails.split(",") if email.strip()]
        
        return MonitoringConfig(
            monitoring_interval_seconds=int(os.getenv("MONITORING_INTERVAL_SECONDS", "300")),
            alert_email_recipients=email_list if email_list else None,
            slack_webhook_url=os.getenv("SLACK_WEBHOOK_URL"),
            dashboard_refresh_interval=int(os.getenv("DASHBOARD_REFRESH_INTERVAL", "3600")),
            dashboard_port=int(os.getenv("DASHBOARD_PORT", "8080")),
            dashboard_host=os.getenv("DASHBOARD_HOST", "localhost")
        )
    
    def _load_attribution_config(self) -> AttributionConfig:
        """Load attribution model configuration."""
        return AttributionConfig(
            default_attribution_model=os.getenv("DEFAULT_ATTRIBUTION_MODEL", "data_driven"),
            attribution_lookback_days=int(os.getenv("ATTRIBUTION_LOOKBACK_DAYS", "30")),
            min_conversions_for_significance=int(os.getenv("MIN_CONVERSIONS_FOR_SIGNIFICANCE", "50")),
            confidence_level=float(os.getenv("CONFIDENCE_LEVEL", "0.95")),
            time_decay_factor=float(os.getenv("TIME_DECAY_FACTOR", "0.1"))
        )
    
    def _load_content_generation_config(self) -> ContentGenerationConfig:
        """Load content generation configuration."""
        return ContentGenerationConfig(
            default_brand_tone=os.getenv("DEFAULT_BRAND_TONE", "professional"),
            content_quality_threshold=float(os.getenv("CONTENT_QUALITY_THRESHOLD", "0.8")),
            max_content_generations_per_hour=int(os.getenv("MAX_CONTENT_GENERATIONS_PER_HOUR", "100")),
            default_openai_model=os.getenv("OPENAI_MODEL", "gpt-4"),
            default_anthropic_model=os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229"),
            max_tokens_per_request=int(os.getenv("MAX_TOKENS_PER_REQUEST", "4000"))
        )
    
    def _load_roi_tracking_config(self) -> ROITrackingConfig:
        """Load ROI tracking configuration."""
        return ROITrackingConfig(
            roas_alert_threshold_low=float(os.getenv("ROAS_ALERT_THRESHOLD_LOW", "-10.0")),
            roas_alert_threshold_critical=float(os.getenv("ROAS_ALERT_THRESHOLD_CRITICAL", "-50.0")),
            cpa_alert_threshold_high=float(os.getenv("CPA_ALERT_THRESHOLD_HIGH", "50.0")),
            cpa_alert_threshold_critical=float(os.getenv("CPA_ALERT_THRESHOLD_CRITICAL", "100.0")),
            ctr_alert_threshold_low=float(os.getenv("CTR_ALERT_THRESHOLD_LOW", "-15.0")),
            conversion_rate_alert_threshold_low=float(os.getenv("CONVERSION_RATE_ALERT_THRESHOLD_LOW", "-10.0")),
            data_retention_days=int(os.getenv("DATA_RETENTION_DAYS", "365"))
        )
    
    def _load_security_config(self) -> SecurityConfig:
        """Load security configuration."""
        allowed_origins = os.getenv("ALLOWED_ORIGINS", "")
        origins_list = [origin.strip() for origin in allowed_origins.split(",") if origin.strip()]
        
        return SecurityConfig(
            api_rate_limit_per_minute=int(os.getenv("API_RATE_LIMIT_PER_MINUTE", "60")),
            session_secret_key=os.getenv("SESSION_SECRET_KEY"),
            encryption_key=os.getenv("ENCRYPTION_KEY"),
            allowed_origins=origins_list if origins_list else ["http://localhost:3000"],
            jwt_expiration_hours=int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
        )
    
    def _validate_settings(self) -> None:
        """Validate critical settings and log warnings for missing configurations."""
        warnings = []
        errors = []
        
        # Check for critical API keys
        if not self.api_credentials.openai_api_key and not self.api_credentials.anthropic_api_key:
            warnings.append("No AI API keys configured (OpenAI or Anthropic)")
        
        # Check security settings for production
        if self.environment == "production":
            if not self.security.session_secret_key:
                errors.append("SESSION_SECRET_KEY is required for production")
            
            if not self.security.encryption_key:
                warnings.append("ENCRYPTION_KEY not set for production environment")
        
        # Check database configuration
        if self.database.database_url.startswith("sqlite://") and self.environment == "production":
            warnings.append("Using SQLite in production - consider PostgreSQL for better performance")
        
        # Log warnings and errors
        logger = logging.getLogger(__name__)
        
        for warning in warnings:
            logger.warning(f"Configuration warning: {warning}")
        
        for error in errors:
            logger.error(f"Configuration error: {error}")
        
        if errors:
            raise ValueError(f"Critical configuration errors: {', '.join(errors)}")
    
    def get_api_credentials_dict(self) -> Dict[str, Optional[str]]:
        """Get API credentials as dictionary for easy passing to services."""
        return {
            'openai_key': self.api_credentials.openai_api_key,
            'anthropic_key': self.api_credentials.anthropic_api_key,
            'google_ads_developer_token': self.api_credentials.google_ads_developer_token,
            'google_ads_client_id': self.api_credentials.google_ads_client_id,
            'google_ads_client_secret': self.api_credentials.google_ads_client_secret,
            'google_ads_refresh_token': self.api_credentials.google_ads_refresh_token,
            'facebook_access_token': self.api_credentials.facebook_access_token,
            'facebook_app_secret': self.api_credentials.facebook_app_secret,
            'facebook_app_id': self.api_credentials.facebook_app_id,
            'linkedin_access_token': self.api_credentials.linkedin_access_token,
            'linkedin_client_id': self.api_credentials.linkedin_client_id,
            'linkedin_client_secret': self.api_credentials.linkedin_client_secret,
        }
    
    def setup_logging(self) -> None:
        """Setup application logging based on configuration."""
        # Create logs directory if it doesn't exist
        log_path = Path(self.logging.log_file_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, self.logging.log_level.upper()),
            format=self.logging.log_format,
            handlers=[
                logging.FileHandler(self.logging.log_file_path),
                logging.StreamHandler()
            ]
        )
        
        # Set up rotating file handler for production
        if self.environment == "production":
            from logging.handlers import RotatingFileHandler
            
            file_handler = RotatingFileHandler(
                self.logging.log_file_path,
                maxBytes=self.logging.max_log_size_mb * 1024 * 1024,
                backupCount=self.logging.backup_count
            )
            file_handler.setFormatter(logging.Formatter(self.logging.log_format))
            
            root_logger = logging.getLogger()
            root_logger.addHandler(file_handler)
    
    def is_api_available(self, api_name: str) -> bool:
        """Check if specific API credentials are available."""
        api_checks = {
            'openai': bool(self.api_credentials.openai_api_key),
            'anthropic': bool(self.api_credentials.anthropic_api_key),
            'google_ads': bool(self.api_credentials.google_ads_developer_token),
            'facebook': bool(self.api_credentials.facebook_access_token),
            'linkedin': bool(self.api_credentials.linkedin_access_token),
            'google_analytics': bool(self.api_credentials.google_analytics_property_id),
        }
        
        return api_checks.get(api_name.lower(), False)
    
    def get_available_apis(self) -> List[str]:
        """Get list of APIs with configured credentials."""
        apis = []
        
        if self.api_credentials.openai_api_key:
            apis.append('openai')
        if self.api_credentials.anthropic_api_key:
            apis.append('anthropic')
        if self.api_credentials.google_ads_developer_token:
            apis.append('google_ads')
        if self.api_credentials.facebook_access_token:
            apis.append('facebook')
        if self.api_credentials.linkedin_access_token:
            apis.append('linkedin')
        if self.api_credentials.google_analytics_property_id:
            apis.append('google_analytics')
        
        return apis
    
    def __repr__(self) -> str:
        """String representation of settings."""
        available_apis = ", ".join(self.get_available_apis())
        return (f"Settings(app={self.app_name} v{self.app_version}, "
                f"env={self.environment}, apis=[{available_apis}])")


# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings


def main():
    """Display current configuration for debugging."""
    settings = get_settings()
    
    print("AI MARKETING TOOLKIT CONFIGURATION")
    print("=" * 50)
    print(f"Application: {settings.app_name} v{settings.app_version}")
    print(f"Environment: {settings.environment}")
    print(f"Debug Mode: {settings.debug}")
    print()
    
    print("AVAILABLE APIs:")
    available_apis = settings.get_available_apis()
    if available_apis:
        for api in available_apis:
            print(f"✓ {api}")
    else:
        print("⚠ No API credentials configured")
    print()
    
    print("CONFIGURATION SUMMARY:")
    print(f"Database: {settings.database.database_url}")
    print(f"Redis: {settings.database.redis_url}")
    print(f"Log Level: {settings.logging.log_level}")
    print(f"Dashboard: {settings.monitoring.dashboard_host}:{settings.monitoring.dashboard_port}")
    print(f"Attribution Model: {settings.attribution.default_attribution_model}")
    print(f"Monitoring Interval: {settings.monitoring.monitoring_interval_seconds}s")
    
    if settings.monitoring.alert_email_recipients:
        print(f"Alert Recipients: {len(settings.monitoring.alert_email_recipients)} configured")
    
    print()
    print("To configure missing APIs, update your .env file with the appropriate credentials.")


if __name__ == "__main__":
    main()