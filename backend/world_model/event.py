from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
import uuid


class EventType(Enum):
    LEARNING = "learning"
    WORK = "work"
    PROJECT = "project"
    SOCIAL = "social"
    HEALTH = "health"
    GOAL = "goal"
    HABIT = "habit"
    REFLECTION = "reflection"


@dataclass
class Event:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType = EventType.LEARNING
    description: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    duration_minutes: Optional[int] = None
    outcome: Optional[str] = None
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "event_type": self.event_type.value,
            "description": self.description,
            "timestamp": self.timestamp.isoformat(),
            "duration_minutes": self.duration_minutes,
            "outcome": self.outcome,
            "metadata": self.metadata
        }


class EventTracker:
    def __init__(self):
        self.events: Dict[str, Event] = {}
        self.storage_path = "data/world_model/events.json"

    def add_event(self, event: Event) -> Event:
        self.events[event.id] = event
        self._save_events()
        return event

    def add_learning_event(self, description: str, outcome: str = None,
                          duration: int = None) -> Event:
        event = Event(
            event_type=EventType.LEARNING,
            description=description,
            outcome=outcome,
            duration_minutes=duration
        )
        return self.add_event(event)

    def add_goal_event(self, goal_id: str, action: str,
                      result: str) -> Event:
        event = Event(
            event_type=EventType.GOAL,
            description=action,
            outcome=result,
            metadata={"goal_id": goal_id}
        )
        return self.add_event(event)

    def add_habit_event(self, habit: str, completed: bool) -> Event:
        event = Event(
            event_type=EventType.HABIT,
            description=habit,
            outcome="completed" if completed else "missed",
            metadata={"habit": habit}
        )
        return self.add_event(event)

    def get_events_by_type(self, event_type: EventType) -> List[Event]:
        return [e for e in self.events.values() if e.event_type == event_type]

    def get_events_by_date_range(self, start: datetime,
                                 end: datetime) -> List[Event]:
        return [e for e in self.events.values()
                if start <= e.timestamp <= end]

    def get_recent_events(self, limit: int = 10) -> List[Event]:
        sorted_events = sorted(self.events.values(),
                             key=lambda x: x.timestamp,
                             reverse=True)
        return sorted_events[:limit]

    def _save_events(self):
        import json
        import os
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {k: v.to_dict() for k, v in self.events.items()}
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_events(self):
        import json
        if not os.path.exists(self.storage_path):
            return
        with open(self.storage_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for k, v in data.items():
                v["timestamp"] = datetime.fromisoformat(v["timestamp"])
                v["event_type"] = EventType(v["event_type"])
                self.events[k] = Event(**v)
