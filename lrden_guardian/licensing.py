#!/usr/bin/env python3
"""
LRDEnE Guardian - Licensing System
===================================

Copyright (c) 2026 LRDEnE. All rights reserved.

Manage LRDEnE Guardian licensing and feature access control.
"""

import json
import hashlib
import time
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass
from .db_adapter import db_adapter

class LicenseTier(Enum):
    """LRDEnE Guardian license tiers"""
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"

class FeatureType(Enum):
    """Available feature types"""
    BASIC_ANALYSIS = "basic_analysis"
    STANDARD_VALIDATIONS = "standard_validations"
    CLI_TOOLS = "cli_tools"
    ADVANCED_ANALYTICS = "advanced_analytics"
    PRIORITY_SUPPORT = "priority_support"
    CUSTOM_THRESHOLDS = "custom_thresholds"
    API_ACCESS = "api_access"
    BATCH_PROCESSING = "batch_processing"
    UNLIMITED_PROCESSING = "unlimited_processing"
    DEDICATED_SUPPORT = "dedicated_support"
    CUSTOM_MODELS = "custom_models"
    ON_PREMISE_DEPLOYMENT = "on_premise_deployment"
    WHITE_LABELING = "white_labeling"
    ADVANCED_MONITORING = "advanced_monitoring"

@dataclass
class LicenseInfo:
    """License information"""
    tier: LicenseTier
    license_key: str
    expires_at: Optional[int]
    features: List[FeatureType]
    usage_limits: Dict[str, Any]
    created_at: int
    company: Optional[str] = None
    contact: Optional[str] = None

class LRDEnELicenseManager:
    """Manage LRDEnE Guardian licensing and features"""
    
    def __init__(self):
        self.pricing_tiers = self._build_pricing_tiers()
        self.feature_matrix = self._build_feature_matrix()
    
    def _build_feature_matrix(self) -> Dict[LicenseTier, List[FeatureType]]:
        """Build feature availability matrix"""
        return {
            LicenseTier.FREE: [
                FeatureType.BASIC_ANALYSIS,
                FeatureType.STANDARD_VALIDATIONS,
                FeatureType.CLI_TOOLS
            ],
            LicenseTier.PRO: [
                FeatureType.BASIC_ANALYSIS,
                FeatureType.STANDARD_VALIDATIONS,
                FeatureType.CLI_TOOLS,
                FeatureType.ADVANCED_ANALYTICS,
                FeatureType.PRIORITY_SUPPORT,
                FeatureType.CUSTOM_THRESHOLDS,
                FeatureType.API_ACCESS,
                FeatureType.BATCH_PROCESSING
            ],
            LicenseTier.ENTERPRISE: [
                FeatureType.BASIC_ANALYSIS,
                FeatureType.STANDARD_VALIDATIONS,
                FeatureType.CLI_TOOLS,
                FeatureType.ADVANCED_ANALYTICS,
                FeatureType.PRIORITY_SUPPORT,
                FeatureType.CUSTOM_THRESHOLDS,
                FeatureType.API_ACCESS,
                FeatureType.BATCH_PROCESSING,
                FeatureType.UNLIMITED_PROCESSING,
                FeatureType.DEDICATED_SUPPORT,
                FeatureType.CUSTOM_MODELS,
                FeatureType.ON_PREMISE_DEPLOYMENT,
                FeatureType.WHITE_LABELING,
                FeatureType.ADVANCED_MONITORING
            ],
            LicenseTier.CUSTOM: []  # Determined per customer
        }
    
    def _build_pricing_tiers(self) -> Dict[LicenseTier, Dict[str, Any]]:
        """Build pricing tier information"""
        return {
            LicenseTier.FREE: {
                "price": 0,
                "billing": "none",
                "usage_limits": {
                    "analyses_per_month": 1000,
                    "api_calls_per_day": 100,
                    "batch_size": 10
                }
            },
            LicenseTier.PRO: {
                "price": 99,
                "billing": "monthly",
                "usage_limits": {
                    "analyses_per_month": 100000,
                    "api_calls_per_day": 10000,
                    "batch_size": 1000
                }
            },
            LicenseTier.ENTERPRISE: {
                "price": 999,
                "billing": "monthly",
                "usage_limits": {
                    "analyses_per_month": "unlimited",
                    "api_calls_per_day": "unlimited",
                    "batch_size": "unlimited"
                }
            },
            LicenseTier.CUSTOM: {
                "price": "contact",
                "billing": "custom",
                "usage_limits": "custom"
            }
        }
    
    def generate_license_key(self, tier: LicenseTier, company: str = None, 
                            contact: str = None, duration_days: int = 365) -> str:
        """Generate a license key for specified tier"""
        
        # Create license data
        license_data = {
            "tier": tier.value,
            "company": company,
            "contact": contact,
            "issued_at": int(time.time()),
            "expires_at": int(time.time()) + (duration_days * 24 * 60 * 60),
            "features": [f.value for f in self.feature_matrix[tier]]
        }
        
        # Create license hash
        license_json = json.dumps(license_data, sort_keys=True)
        license_hash = hashlib.sha256(license_json.encode()).hexdigest()
        
        # Format license key
        license_key = f"LRDEN-{tier.value.upper()}-{license_hash[:16].upper()}"
        
        # Create LicenseInfo object
        license_info = LicenseInfo(
            tier=tier,
            license_key=license_key,
            expires_at=license_data["expires_at"],
            features=self.feature_matrix[tier],
            usage_limits=self.pricing_tiers[tier]["usage_limits"],
            created_at=license_data["issued_at"],
            company=company,
            contact=contact
        )
        
        # Persistent storage
        db_adapter.save_license(license_info)
        
        return license_key
    
    def validate_license(self, license_key: str) -> Optional[LicenseInfo]:
        """Validate license key and return license info"""
        
        # Try database first
        db_data = db_adapter.get_license(license_key)
        if db_data:
            license_info = LicenseInfo(
                tier=LicenseTier(db_data['tier']),
                license_key=db_data['license_key'],
                expires_at=db_data['expires_at'],
                features=[FeatureType(f) for f in db_data['features']],
                usage_limits=db_data['usage_limits'],
                created_at=db_data['created_at'],
                company=db_data['company'],
                contact=db_data['contact']
            )
            if self._is_license_valid(license_info):
                return license_info
            return None
        
        # Parse license key format
        if not license_key.startswith("LRDEN-"):
            return None
        
        try:
            parts = license_key.split("-")
            if len(parts) != 3:
                return None
            
            tier_str = parts[1].lower()
            hash_part = parts[2]
            
            # Validate tier
            try:
                tier = LicenseTier(tier_str)
            except ValueError:
                return None
            
            # For demo purposes, accept any valid format
            # In production, this would validate against a database
            license_info = LicenseInfo(
                tier=tier,
                license_key=license_key,
                expires_at=int(time.time()) + (365 * 24 * 60 * 60),  # 1 year from now
                features=self.feature_matrix[tier],
                usage_limits=self.pricing_tiers[tier]["usage_limits"],
                created_at=int(time.time())
            )
            
            self.license_cache[license_key] = license_info
            return license_info
            
        except Exception:
            return None
    
    def _is_license_valid(self, license_info: LicenseInfo) -> bool:
        """Check if license is still valid"""
        if license_info.expires_at is None:
            return True  # No expiration
        
        return int(time.time()) < license_info.expires_at
    
    def check_feature_access(self, license_key: str, feature: FeatureType) -> bool:
        """Check if license provides access to specific feature"""
        
        license_info = self.validate_license(license_key)
        if not license_info:
            return False
        
        return feature in license_info.features
    
    def check_usage_limits(self, license_key: str, usage_type: str, current_usage: int) -> Dict[str, Any]:
        """Check usage against license limits"""
        
        license_info = self.validate_license(license_key)
        if not license_info:
            return {
                "allowed": False,
                "limit": 0,
                "current": current_usage,
                "remaining": 0,
                "tier": "none"
            }
        
        limits = license_info.usage_limits
        limit = limits.get(usage_type, 0)
        
        # Get actual current usage from DB
        current_usage = db_adapter.get_aggregated_usage(license_key, action=usage_type)
        
        if limit == "unlimited":
            return {
                "allowed": True,
                "limit": "unlimited",
                "current": current_usage,
                "remaining": "unlimited",
                "tier": license_info.tier.value
            }
        
        remaining = max(0, limit - current_usage)
        allowed = remaining > 0
        
        return {
            "allowed": allowed,
            "limit": limit,
            "current": current_usage,
            "remaining": remaining,
            "tier": license_info.tier.value
        }
    
    def get_license_info(self, license_key: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive license information"""
        
        license_info = self.validate_license(license_key)
        if not license_info:
            return None
        
        return {
            "tier": license_info.tier.value,
            "license_key": license_info.license_key,
            "company": license_info.company,
            "contact": license_info.contact,
            "expires_at": license_info.expires_at,
            "created_at": license_info.created_at,
            "features": [f.value for f in license_info.features],
            "usage_limits": license_info.usage_limits,
            "pricing": self.pricing_tiers[license_info.tier]
        }
    
    def upgrade_license(self, license_key: str, new_tier: LicenseTier) -> Optional[str]:
        """Upgrade license to higher tier"""
        
        current_license = self.validate_license(license_key)
        if not current_license:
            return None
        
        # Generate new license key
        new_license_key = self.generate_license_key(
            tier=new_tier,
            company=current_license.company,
            contact=current_license.contact
        )
        
        return new_license_key
    
    def get_pricing_info(self) -> Dict[str, Any]:
        """Get pricing information for all tiers"""
        
        return {
            "tiers": {
                tier.value: {
                    "price": info["price"],
                    "billing": info["billing"],
                    "features": [f.value for f in self.feature_matrix[tier]],
                    "usage_limits": info["usage_limits"],
                    "description": self._get_tier_description(tier)
                }
                for tier, info in self.pricing_tiers.items()
            },
            "currency": "USD",
            "billing_cycle": "monthly"
        }
    
    def _get_tier_description(self, tier: LicenseTier) -> str:
        """Get description for license tier"""
        descriptions = {
            LicenseTier.FREE: "Perfect for individual developers and small projects",
            LicenseTier.PRO: "Ideal for growing teams and professional use",
            LicenseTier.ENTERPRISE: "Complete solution for large organizations",
            LicenseTier.CUSTOM: "Tailored solutions for specific enterprise needs"
        }
        return descriptions.get(tier, "Custom license tier")

# Global license manager instance
license_manager = LRDEnELicenseManager()

# Demo license keys for testing
DEMO_LICENSES = {
    "free": license_manager.generate_license_key(LicenseTier.FREE, "Demo User", "demo@example.com"),
    "pro": license_manager.generate_license_key(LicenseTier.PRO, "Demo Company", "demo@company.com"),
    "enterprise": license_manager.generate_license_key(LicenseTier.ENTERPRISE, "Demo Enterprise", "enterprise@demo.com")
}

def get_demo_license(tier: str = "free") -> str:
    """Get demo license key for testing"""
    return DEMO_LICENSES.get(tier.lower(), DEMO_LICENSES["free"])

def validate_license_key(license_key: str) -> Optional[Dict[str, Any]]:
    """Validate license key and return info"""
    return license_manager.get_license_info(license_key)
