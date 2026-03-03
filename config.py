"""
Configuration module for Adaptive Evolutionary Trading AI.
Centralizes all configuration with environment variable fallbacks.
"""
import os
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum
import yaml
from dotenv import load_dotenv

load_dotenv()

class TradingMode(Enum):
    SIMULATION = "simulation"
    PAPER = "paper"
    LIVE = "live"

class MarketCondition(Enum):
    BULL = "bull"
    BEAR = "bear"
    SIDEWAYS = "sideways"
    VOLATILE = "volatile"

@dataclass
class ExchangeConfig:
    """Configuration for cryptocurrency exchange API"""
    name: str = "binance"
    api_key: str = ""
    api_secret: str = ""
    testnet: bool = True
    rate_limit: int = 1200
    timeout: int = 30000

@dataclass
class TradingConfig:
    """Core trading parameters"""
    initial_capital: float = 10000.0
    risk_per_trade: float = 0.02  # 2% risk per trade
    max_position_size: float = 0.1  # 10% of capital
    stop_loss_pct: float = 0.02  # 2% stop loss
    take_profit_pct: float = 0.04  # 4% take profit
    trading_pair: str = "BTC/USDT"
    timeframe: str = "1h"
    max_open_trades: int = 5

@dataclass
class EvolutionConfig:
    """Evolutionary learning parameters"""
    analysis_window: int = 100  # Analyze last 100 trades
    fitness_metric: str = "sharpe_ratio"  # Options: sharpe_ratio, profit_factor, win_rate
    mutation_rate: float = 0.1
    crossover_rate: float = 0.7
    population_size: int = 20
    generations: int = 100
    elite_count: int = 2

@dataclass
class RLConfig:
    """Reinforcement learning configuration"""
    learning_rate: float = 0.0003
    gamma: float = 0.99
    batch_size: int = 64
    buffer_size: int = 100000
    exploration_rate: float = 0.1
    training_episodes: int = 1000
    validation_frequency: int = 100

@dataclass
class FirebaseConfig:
    """Firebase configuration"""
    project_id: str = os.getenv("FIREBASE_PROJECT_ID", "")
    credentials_path: str = os.getenv("FIREBASE_CREDENTIALS", "firebase_credentials.json")
    database_url: str = os.getenv("FIREBASE_DATABASE_URL", "")

class Config:
    """Main configuration class"""
    def __init__(self):
        self.mode = TradingMode(os.getenv("TRADING_MODE", "paper"))
        self.exchange = ExchangeConfig(
            name=os.getenv("EXCHANGE_NAME", "binance"),
            api_key=os.getenv("EXCHANGE_API_KEY", ""),
            api_secret=os.getenv("EXCHANGE_API_SECRET", ""),
            testnet=self.mode != TradingMode.LIVE
        )
        self.trading = TradingConfig()
        self.evolution = EvolutionConfig()
        self.rl = RLConfig()
        self.firebase = FirebaseConfig()
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
    def validate(self) -> bool:
        """Validate configuration"""
        if self.mode == TradingMode.LIVE:
            if not self.exchange.api_key or not self.exchange.api_secret:
                raise ValueError("API credentials required for live trading")
        if not self.firebase.project_id:
            raise ValueError("Firebase project ID is required")
        return True
    
    def save(self, filepath: str = "config.yaml"):
        """Save configuration to file"""
        with open(filepath, 'w') as f:
            yaml.dump(self.__dict__, f)
    
    @classmethod
    def load(cls, filepath: str = "config.yaml") -> 'Config':
        """Load configuration from file"""
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        config = cls()
        # Update config with loaded data
        for key, value in data.items():
            setattr(config, key, value)
        return config

# Singleton instance
config = Config()