"""
Firebase client for state management and real-time data streaming.
Handles trade data storage, strategy state, and performance metrics.
"""
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import asdict
import firebase_admin
from firebase_admin import credentials, firestore, db
from google.cloud.firestore_v1.base_query import FieldFilter
from google.api_core.exceptions import GoogleAPICallError, RetryError

from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FirebaseClient:
    """Firebase client for adaptive trading system"""
    
    def __init__(self, config: Config):
        """Initialize Firebase connection"""
        self.config = config
        self._initialize_firebase()
        self.db = firestore.client()
        self.rtdb = None
        
    def _initialize_firebase(self):
        """Initialize Firebase app with error handling"""
        try:
            # Check if Firebase app already exists
            if not firebase_admin._apps:
                cred_path = self.config.firebase.credentials_path
                
                # Try multiple credential loading methods
                if cred_path and os.path.exists(cred_path):
                    cred = credentials.Certificate(cred_path)
                else:
                    # Try environment variable
                    cred_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
                    if cred_json:
                        cred