"""Enums for event types."""

from enum import Enum


class EventType(str, Enum):
    FOLLOW_UP = "follow_up"
    CAMPAIGN = "campaign"
    REMINDER = "reminder"
