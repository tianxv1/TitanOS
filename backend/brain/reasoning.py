from typing import List, Dict, Any, Optional
import json


class ReasoningEngine:
    def __init__(self):
        self.reasoning_chain: List[Dict[str, str]] = []

    def think(self, context: str, question: str) -> Dict[str, Any]:
        self.reasoning_chain.append({
            "context": context,
            "question": question,
            "step": "analyze"
        })

        analysis = self._analyze_question(question)
        self.reasoning_chain.append({
            "step": "reasoning",
            "analysis": analysis
        })

        reasoning_result = self._generate_reasoning(context, analysis)
        self.reasoning_chain.append({
            "step": "conclude",
            "result": reasoning_result
        })

        return {
            "analysis": analysis,
            "reasoning": reasoning_result,
            "chain": self.reasoning_chain
        }

    def _analyze_question(self, question: str) -> Dict[str, Any]:
        question_lower = question.lower()

        question_types = []
        if any(kw in question_lower for kw in ["how", "why", "what", "when", "where", "who"]):
            question_types.append("wh_question")
        if any(kw in question_lower for kw in ["compare", "difference", "vs", "versus"]):
            question_types.append("comparison")
        if any(kw in question_lower for kw in ["explain", "describe", "tell"]):
            question_types.append("explanation")
        if any(kw in question_lower for kw in ["do", "make", "create", "build"]):
            question_types.append("action")
        if any(kw in question_lower for kw in ["should", "must", "need", "have to"]):
            question_types.append("recommendation")

        complexity = "simple"
        word_count = len(question.split())
        if word_count > 20:
            complexity = "complex"
        elif word_count > 10:
            complexity = "medium"

        return {
            "types": question_types,
            "complexity": complexity,
            "word_count": word_count,
            "keywords": self._extract_keywords(question)
        }

    def _extract_keywords(self, text: str) -> List[str]:
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
                      "have", "has", "had", "do", "does", "did", "will", "would", "could",
                      "should", "may", "might", "must", "shall", "can", "need", "dare",
                      "ought", "used", "to", "of", "in", "for", "on", "with", "at", "by",
                      "from", "as", "into", "through", "during", "before", "after", "above",
                      "below", "between", "under", "again", "further", "then", "once"}
        words = text.lower().replace("?", "").replace(".", "").replace(",", "").split()
        return [w for w in words if w not in stop_words and len(w) > 2][:10]

    def _generate_reasoning(self, context: str, analysis: Dict[str, Any]) -> str:
        reasoning_parts = []

        if "wh_question" in analysis["types"]:
            reasoning_parts.append(f"这是一个{analysis['complexity']}级的问题，需要提供具体信息。")

        if "comparison" in analysis["types"]:
            reasoning_parts.append("需要对比分析多个方面。")

        if "explanation" in analysis["types"]:
            reasoning_parts.append("需要详细解释概念和原理。")

        if "action" in analysis["types"]:
            reasoning_parts.append("需要提供具体的行动步骤。")

        if "recommendation" in analysis["types"]:
            reasoning_parts.append("需要给出建议或推荐。")

        reasoning_parts.append(f"关键词: {', '.join(analysis['keywords'])}")

        return " ".join(reasoning_parts)

    def chain_of_thought(self, problem: str, steps: int = 5) -> List[str]:
        thoughts = []
        current_problem = problem

        for i in range(steps):
            thought = f"步骤{i+1}: 分析问题 '{current_problem}'"
            thoughts.append(thought)

            if i < steps - 1:
                current_problem = f"基于'{current_problem}'的进一步推理"

        thoughts.append(f"最终结论: {problem}")
        return thoughts

    def deduce(self, premise: str, hypothesis: str) -> Dict[str, Any]:
        premise_lower = premise.lower()
        hypothesis_lower = hypothesis.lower()

        shared_concepts = []
        premise_words = set(premise_lower.replace("?", "").split())
        hypothesis_words = set(hypothesis_lower.replace("?", "").split())
        shared = premise_words & hypothesis_words
        if len(shared) > 2:
            shared_concepts = list(shared)

        confidence = 0.5
        for concept in shared_concepts[:5]:
            if concept in premise_lower and concept in hypothesis_lower:
                confidence += 0.1
        confidence = min(confidence, 0.95)

        conclusion = ""
        if confidence > 0.7:
            conclusion = "假设可能成立"
        elif confidence > 0.4:
            conclusion = "无法确定，需要更多信息"
        else:
            conclusion = "假设可能不成立"

        return {
            "premise": premise,
            "hypothesis": hypothesis,
            "shared_concepts": shared_concepts,
            "confidence": round(confidence, 3),
            "conclusion": conclusion
        }

    def clear_chain(self):
        self.reasoning_chain = []

    def get_context_summary(self) -> str:
        if not self.reasoning_chain:
            return "No reasoning context yet."
        return f"Reasoning chain has {len(self.reasoning_chain)} steps"
