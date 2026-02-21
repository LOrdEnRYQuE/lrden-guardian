#!/usr/bin/env python3
"""
LRDEnE Guardian - Database Adapter
==================================

Handles persistence for licensing, API keys, and subscriptions.
Defaults to SQLite for local development but supports PostgreSQL/Supabase.
"""

import sqlite3
import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

class DatabaseAdapter:
    """Persistent storage for commercial licensing and user data."""
    
    def __init__(self, db_path: str = "guardian_commercial.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initializes the commercial database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Licenses Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS licenses (
                    license_key TEXT PRIMARY KEY,
                    tier TEXT NOT NULL,
                    company TEXT,
                    contact TEXT,
                    created_at INTEGER,
                    expires_at INTEGER,
                    features TEXT, -- JSON string
                    usage_limits TEXT, -- JSON string
                    status TEXT DEFAULT 'active'
                )
            ''')
            # API Usage Tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS api_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    license_key TEXT,
                    timestamp TEXT,
                    action TEXT,
                    usage_count INTEGER,
                    FOREIGN KEY(license_key) REFERENCES licenses(license_key)
                )
            ''')
            conn.commit()

    def save_license(self, license_info: Any):
        """Stores or updates a license in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO licenses 
                (license_key, tier, company, contact, created_at, expires_at, features, usage_limits)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                license_info.license_key,
                license_info.tier.value,
                license_info.company,
                license_info.contact,
                license_info.created_at,
                license_info.expires_at,
                json.dumps([f.value for f in license_info.features]),
                json.dumps(license_info.usage_limits)
            ))
            conn.commit()

    def get_license(self, license_key: str) -> Optional[Dict[str, Any]]:
        """Retrieves a license by its key."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM licenses WHERE license_key = ? AND status = "active"', (license_key,))
            row = cursor.fetchone()
            if row:
                data = dict(row)
                data['features'] = json.loads(data['features'])
                data['usage_limits'] = json.loads(data['usage_limits'])
                return data
            return None

    def log_usage(self, license_key: str, action: str, count: int = 1):
        """Logs usage event for a specific license."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO api_usage (license_key, timestamp, action, usage_count)
                VALUES (?, ?, ?, ?)
            ''', (license_key, datetime.now().isoformat(), action, count))
            conn.commit()

    def get_aggregated_usage(self, license_key: str, action: str = None) -> int:
        """Returns total usage for a license."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if action:
                cursor.execute('SELECT SUM(usage_count) FROM api_usage WHERE license_key = ? AND action = ?', (license_key, action))
            else:
                cursor.execute('SELECT SUM(usage_count) FROM api_usage WHERE license_key = ?', (license_key,))
            result = cursor.fetchone()[0]
            return result if result else 0

# Global DB adapter instance
db_adapter = DatabaseAdapter()
