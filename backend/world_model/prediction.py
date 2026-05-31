from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid


class PredictionType(Enum):
    GROWTH = "growth"
    SUCCESS = "success"
    RISK = "risk"
    PATTERN = "pattern"


@dataclass
class Prediction:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    prediction_type: PredictionType = PredictionType.GROWTH
    description: str = ""
    target_event: str = ""
    probability: float = 0.5
    time_horizon_days: int = 30
    confidence: float = 0.5
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "prediction_type": self.prediction_type.value,
            "description": self.description,
            "target_event": self.target_event,
            "probability": self.probability,
            "time_horizon_days": self.time_horizon_days,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }


class PredictionEngine:
    def __init__(self, event_tracker=None, causality_engine=None):
        self.predictions: Dict[str, Prediction] = {}
        self.event_tracker = event_tracker
        self.causality_engine = causality_engine
        self.storage_path = "data/world_model/predictions.json"

    def predict_success_probability(self, goal_id: str,
                                   historical_data: Dict) -> float:
        base_prob = 0.5

        if historical_data.get("completed_subgoals", 0) > 0:
            completion_rate = historical_data["completed_subgoals"] / max(
                historical_data.get("total_subgoals", 1), 1
            )
            base_prob += completion_rate * 0.3

        if historical_data.get("on_time_rate", 0) > 0.8:
            base_prob += 0.15

        if historical_data.get("consistency_score", 0) > 0.7:
            base_prob += 0.1

        return min(base_prob, 0.99)

    def predict_growth_rate(self, learning_hours_per_week: float,
                           project_completion_rate: float) -> float:
        base_growth = learning_hours_per_week * 0.02

        if project_completion_rate > 0.8:
            base_growth *= 1.5
        elif project_completion_rate > 0.5:
            base_growth *= 1.2

        return min(base_growth, 0.5)

    def predict_from_causality(self, cause_event_id: str) -> List[Prediction]:
        if not self.causality_engine:
            return []

        predictions = []
        effects = self.causality_engine.get_effects(cause_event_id)

        for effect in effects:
            pred = Prediction(
                prediction_type=PredictionType.PATTERN,
                description=effect.description,
                target_event=effect.effect_event_id,
                probability=effect.confidence,
                time_horizon_days=7,
                confidence=effect.confidence * 0.8,
                metadata={"cause_link_id": effect.id}
            )
            predictions.append(pred)
            self.predictions[pred.id] = pred

        self._save_predictions()
        return predictions

    def create_prediction(self, prediction_type: PredictionType,
                         description: str, target_event: str,
                         probability: float = 0.5,
                         time_horizon_days: int = 30,
                         confidence: float = 0.5) -> Prediction:
        pred = Prediction(
            prediction_type=prediction_type,
            description=description,
            target_event=target_event,
            probability=probability,
            time_horizon_days=time_horizon_days,
            confidence=confidence
        )
        self.predictions[pred.id] = pred
        self._save_predictions()
        return pred

    def get_predictions_by_type(self, prediction_type: PredictionType) -> List[Prediction]:
        return [p for p in self.predictions.values()
                if p.prediction_type == prediction_type]

    def get_active_predictions(self) -> List[Prediction]:
        now = datetime.now()
        active = []
        for pred in self.predictions.values():
            expiry = pred.created_at + timedelta(days=pred.time_horizon_days)
            if expiry > now:
                active.append(pred)
        return active

    def evaluate_prediction(self, prediction_id: str, actual_outcome: str) -> float:
        pred = self.predictions.get(prediction_id)
        if not pred:
            return 0.0

        predicted = pred.target_event.lower() in actual_outcome.lower()
        if predicted:
            pred.confidence = min(pred.confidence * 1.1, 1.0)
        else:
            pred.confidence *= 0.9

        self._save_predictions()
        return pred.confidence

    def _save_predictions(self):
        import json
        import os
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {k: v.to_dict() for k, v in self.predictions.items()}
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
