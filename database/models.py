from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Subscription:
    user_id: int
    chat_id: int
    subscribed_at: datetime


@dataclass
class TargetRate:
    id: Optional[int]
    user_id: int
    currency: str
    target_rate: float
    created_at: datetime


@dataclass
class RateHistory:
    id: Optional[int]
    currency_pair: str
    rate: float
    timestamp: datetime