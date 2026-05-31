from datetime import datetime, timedelta
from typing import List
from .memory_node import Memory


class MemoryScore:
    IMP_WEIGHT = 0.6
    ACCESS_WEIGHT = 0.3
    RECENT_WEIGHT = 0.1

    DECAY_BASE = 0.95
    DECAY_INTERVAL_HOURS = 24

    @classmethod
    def calculate_recent_score(cls, last_accessed: datetime) -> float:
        now = datetime.now()
        hours_since = (now - last_accessed).total_seconds() / 3600
        decay_periods = hours_since / cls.DECAY_INTERVAL_HOURS
        return pow(cls.DECAY_BASE, decay_periods)

    @classmethod
    def calculate_score(cls, memory: Memory) -> float:
        recent_score = cls.calculate_recent_score(memory.last_accessed)
        score = (
            memory.importance * cls.IMP_WEIGHT +
            min(memory.access_count / 100, 1.0) * cls.ACCESS_WEIGHT +
            recent_score * cls.RECENT_WEIGHT
        )
        return round(score, 4)

    @classmethod
    def should_delete(cls, memory: Memory, threshold: float = 0.3) -> bool:
        return cls.calculate_score(memory) < threshold

    @classmethod
    def get_all_scores(cls, memories: List[Memory]) -> List[tuple]:
        return [(m, cls.calculate_score(m)) for m in memories]
