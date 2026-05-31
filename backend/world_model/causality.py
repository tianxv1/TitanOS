from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import uuid


class CauseType(Enum):
    DIRECT = "direct"
    INDIRECT = "indirect"
    ENABLING = "enabling"
    REINFORCING = "reinforcing"


@dataclass
class CausalityLink:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    cause_event_id: str = ""
    effect_event_id: str = ""
    cause_type: CauseType = CauseType.DIRECT
    confidence: float = 0.5
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "cause_event_id": self.cause_event_id,
            "effect_event_id": self.effect_event_id,
            "cause_type": self.cause_type.value,
            "confidence": self.confidence,
            "description": self.description,
            "created_at": self.created_at.isoformat()
        }


class CausalityEngine:
    def __init__(self):
        self.links: Dict[str, CausalityLink] = {}
        self.storage_path = "data/world_model/causality.json"

    def learn_causality(self, cause_event_id: str, effect_event_id: str,
                       cause_type: CauseType = CauseType.DIRECT,
                       confidence: float = 0.5,
                       description: str = "") -> CausalityLink:
        link = CausalityLink(
            cause_event_id=cause_event_id,
            effect_event_id=effect_event_id,
            cause_type=cause_type,
            confidence=confidence,
            description=description
        )
        self.links[link.id] = link
        self._save_links()
        return link

    def learn_from_pattern(self, action: str, result: str,
                          confidence: float = 0.7) -> CausalityLink:
        cause_id = f"action_{hash(action)}"
        effect_id = f"result_{hash(result)}"
        return self.learn_causality(
            cause_id, effect_id,
            CauseType.DIRECT,
            confidence,
            f"{action} → {result}"
        )

    def get_causes(self, event_id: str) -> List[CausalityLink]:
        return [link for link in self.links.values()
                if link.effect_event_id == event_id]

    def get_effects(self, event_id: str) -> List[CausalityLink]:
        return [link for link in self.links.values()
                if link.cause_event_id == event_id]

    def find_causal_chain(self, start_event_id: str,
                         max_depth: int = 5) -> List[List[CausalityLink]]:
        chains = []
        current_chain = []

        def dfs(event_id: str, depth: int):
            if depth > max_depth:
                return

            effects = self.get_effects(event_id)
            for effect in effects:
                current_chain.append(effect)
                chains.append(list(current_chain))
                dfs(effect.effect_event_id, depth + 1)
                current_chain.pop()

        dfs(start_event_id, 0)
        return chains

    def analyze_correlation(self, event_type_a: str, event_type_b: str,
                          time_window_minutes: int = 60) -> float:
        matching = 0
        total = 0

        for link in self.links.values():
            if event_type_a in link.cause_event_id:
                total += 1
                if event_type_b in link.effect_event_id:
                    matching += 1
            elif event_type_b in link.cause_event_id:
                total += 1
                if event_type_a in link.effect_event_id:
                    matching += 1

        return matching / total if total > 0 else 0.0

    def _save_links(self):
        import json
        import os
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {k: v.to_dict() for k, v in self.links.items()}
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
