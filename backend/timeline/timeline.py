from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
from memory.memory_engine import MemoryEngine
from memory.memory_node import Memory
import json
import os


@dataclass
class TimelineEvent:
    id: str
    content: str
    timestamp: datetime
    category: str
    importance: float
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "category": self.category,
            "importance": self.importance,
            "tags": self.tags,
            "metadata": self.metadata
        }

    @classmethod
    def from_memory(cls, memory: Memory) -> "TimelineEvent":
        return cls(
            id=memory.id,
            content=memory.content,
            timestamp=memory.timestamp,
            category="memory",
            importance=memory.importance,
            tags=memory.tags or [],
            metadata={}
        )


@dataclass
class TimelineGroup:
    year: int
    month: Optional[int] = None
    events: List[TimelineEvent] = field(default_factory=list)

    def to_dict(self) -> dict:
        result = {
            "year": self.year,
            "events": [e.to_dict() for e in self.events]
        }
        if self.month is not None:
            result["month"] = self.month
        return result


class MemoryTimeline:
    def __init__(self):
        self.memory_engine = MemoryEngine()

    def get_all_events(self) -> List[TimelineEvent]:
        memories = self.memory_engine.get_all_memories()
        events = [TimelineEvent.from_memory(m) for m in memories]
        return sorted(events, key=lambda e: e.timestamp, reverse=True)

    def get_events_by_time_range(self, start_time: datetime, end_time: datetime) -> List[TimelineEvent]:
        all_events = self.get_all_events()
        return [
            event for event in all_events
            if start_time <= event.timestamp <= end_time
        ]

    def get_events_by_year(self, year: int) -> List[TimelineEvent]:
        all_events = self.get_all_events()
        return [
            event for event in all_events
            if event.timestamp.year == year
        ]

    def get_events_by_month(self, year: int, month: int) -> List[TimelineEvent]:
        all_events = self.get_all_events()
        return [
            event for event in all_events
            if event.timestamp.year == year and event.timestamp.month == month
        ]

    def get_timeline_by_year(self) -> List[TimelineGroup]:
        events = self.get_all_events()
        year_groups: Dict[int, List[TimelineEvent]] = {}

        for event in events:
            year = event.timestamp.year
            if year not in year_groups:
                year_groups[year] = []
            year_groups[year].append(event)

        sorted_years = sorted(year_groups.keys(), reverse=True)
        return [
            TimelineGroup(year=year, events=year_groups[year])
            for year in sorted_years
        ]

    def get_timeline_by_month(self) -> List[TimelineGroup]:
        events = self.get_all_events()
        month_groups: Dict[tuple, List[TimelineEvent]] = {}

        for event in events:
            key = (event.timestamp.year, event.timestamp.month)
            if key not in month_groups:
                month_groups[key] = []
            month_groups[key].append(event)

        sorted_keys = sorted(month_groups.keys(), reverse=True)
        return [
            TimelineGroup(year=year, month=month, events=month_groups[(year, month)])
            for year, month in sorted_keys
        ]

    def get_timeline_summary(self) -> Dict[str, Any]:
        events = self.get_all_events()
        if not events:
            return {
                "total_events": 0,
                "years": [],
                "monthly_distribution": {}
            }

        year_counts: Dict[int, int] = {}
        month_counts: Dict[str, int] = {}

        for event in events:
            year = event.timestamp.year
            month_key = f"{year}-{event.timestamp.month:02d}"

            year_counts[year] = year_counts.get(year, 0) + 1
            month_counts[month_key] = month_counts.get(month_key, 0) + 1

        return {
            "total_events": len(events),
            "years": sorted(year_counts.keys(), reverse=True),
            "yearly_distribution": year_counts,
            "monthly_distribution": month_counts,
            "first_event": events[-1].to_dict() if events else None,
            "latest_event": events[0].to_dict() if events else None
        }

    def get_events_by_tag(self, tag: str) -> List[TimelineEvent]:
        events = self.get_all_events()
        return [
            event for event in events
            if tag.lower() in [t.lower() for t in event.tags]
        ]

    def get_events_by_importance(self, min_importance: float = 0.7) -> List[TimelineEvent]:
        events = self.get_all_events()
        return [
            event for event in events
            if event.importance >= min_importance
        ]

    def get_milestone_events(self) -> List[TimelineEvent]:
        return self.get_events_by_importance(min_importance=0.8)

    def export_timeline(self, file_path: str = "timeline_export.json") -> bool:
        events = self.get_all_events()
        data = {
            "exported_at": datetime.now().isoformat(),
            "total_events": len(events),
            "events": [e.to_dict() for e in events]
        }

        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def get_timeline_stats(self) -> Dict[str, Any]:
        events = self.get_all_events()
        if not events:
            return {
                "total_events": 0,
                "avg_importance": 0.0,
                "categories": [],
                "top_tags": []
            }

        tag_counts: Dict[str, int] = {}
        for event in events:
            for tag in event.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            "total_events": len(events),
            "avg_importance": sum(e.importance for e in events) / len(events),
            "categories": ["memory"],
            "top_tags": [{"tag": tag, "count": count} for tag, count in top_tags],
            "earliest_date": events[-1].timestamp.isoformat(),
            "latest_date": events[0].timestamp.isoformat()
        }
