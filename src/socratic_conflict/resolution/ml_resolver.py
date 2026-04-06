"""Machine Learning-based conflict resolution strategies."""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from socratic_conflict.core.conflict import Conflict, Proposal, Resolution

from .strategies import ResolutionStrategy

logger = logging.getLogger(__name__)


@dataclass
class ResolutionScore:
    """Scores for evaluating resolution quality."""

    proposal_id: str
    ml_score: float  # 0-1 ML model score
    consensus_score: float  # 0-1 consensus alignment
    stakeholder_alignment: float  # 0-1 stakeholder preference alignment
    escalation_risk: float  # 0-1 risk of escalation
    overall_score: float  # Combined weighted score
    explanation: str = ""

    def __repr__(self) -> str:
        """Return string representation."""
        return f"ResolutionScore(proposal={self.proposal_id}, score={self.overall_score:.3f})"


@dataclass
class ResolutionPath:
    """Recommended escalation/resolution path."""

    steps: List[str]  # Ordered list of resolution steps
    estimated_rounds: int  # Estimated negotiation rounds needed
    success_probability: float  # 0-1 probability of resolution
    recommended_mediator: Optional[str] = None
    escalation_triggers: List[str] = None

    def __post_init__(self):
        """Initialize defaults."""
        if self.escalation_triggers is None:
            self.escalation_triggers = []


class MLResolutionResolver(ResolutionStrategy):
    """ML-based conflict resolution using historical data and predictive models."""

    def __init__(self, historical_data: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize ML resolution resolver.

        Args:
            historical_data: Historical conflict resolution data for training
        """
        self.logger = logging.getLogger(__name__)
        self.model = None
        self.is_trained = False
        self.historical_data = historical_data or []

        self._initialize_model()

        if historical_data:
            self.train(historical_data)

    def _initialize_model(self) -> None:
        """Initialize ML model."""
        try:
            from sklearn.ensemble import RandomForestClassifier

            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                random_state=42,
            )
        except ImportError:
            self.logger.warning(
                "scikit-learn not installed. Install with: pip install scikit-learn"
            )

    def train(self, historical_data: List[Dict[str, Any]]) -> None:
        """
        Train resolution model on historical conflict data.

        Args:
            historical_data: List of historical conflict records with outcomes
        """
        if not self.model:
            raise RuntimeError("scikit-learn not installed")

        if len(historical_data) < 5:
            self.logger.warning(
                f"Insufficient training data ({len(historical_data)} records). "
                "Recommend at least 10."
            )

        # Extract features and labels
        X = []
        y = []

        for record in historical_data:
            features = self._extract_features(record)
            if features is not None:
                X.append(features)
                # Label: 1 if successful, 0 otherwise
                y.append(1 if record.get("successful", False) else 0)

        if X and y:
            self.model.fit(np.array(X), np.array(y))
            self.is_trained = True
            self.logger.info(f"ML resolution model trained on {len(X)} records")

    def resolve(self, conflict: Conflict) -> Optional[Resolution]:
        """
        Resolve conflict using ML-based scoring.

        Args:
            conflict: Conflict to resolve

        Returns:
            Resolution with ML-selected proposal
        """
        if not conflict.proposals:
            return None

        # Score all proposals
        scores = []
        for proposal in conflict.proposals:
            score = self._score_proposal(conflict, proposal)
            scores.append(score)

        # Find best proposal
        best_score = max(scores, key=lambda s: s.overall_score)

        return Resolution(
            conflict_id=conflict.conflict_id,
            strategy="ml_resolver",
            recommended_proposal_id=best_score.proposal_id,
            confidence=best_score.overall_score,
            rationale=best_score.explanation,
            metadata={
                "ml_score": best_score.ml_score,
                "consensus_score": best_score.consensus_score,
                "stakeholder_alignment": best_score.stakeholder_alignment,
                "escalation_risk": best_score.escalation_risk,
                "all_scores": [
                    {
                        "proposal_id": s.proposal_id,
                        "score": s.overall_score,
                    }
                    for s in scores
                ],
            },
        )

    def _score_proposal(self, conflict: Conflict, proposal: Proposal) -> ResolutionScore:
        """
        Score a proposal for resolution quality.

        Args:
            conflict: The conflict
            proposal: Proposal to score

        Returns:
            ResolutionScore with various scoring dimensions
        """
        # ML-based scoring
        ml_score = self._get_ml_score(conflict, proposal)

        # Consensus alignment (how well aligned with other proposals)
        consensus_score = self._get_consensus_score(conflict, proposal)

        # Stakeholder preference alignment
        stakeholder_alignment = self._get_stakeholder_alignment(conflict, proposal)

        # Escalation risk
        escalation_risk = self._calculate_escalation_risk(conflict, proposal)

        # Weighted overall score
        overall_score = (
            ml_score * 0.4
            + consensus_score * 0.3
            + stakeholder_alignment * 0.2
            + (1.0 - escalation_risk) * 0.1
        )

        explanation = (
            f"ML score: {ml_score:.2f}, "
            f"Consensus: {consensus_score:.2f}, "
            f"Stakeholder alignment: {stakeholder_alignment:.2f}, "
            f"Escalation risk: {escalation_risk:.2f}"
        )

        return ResolutionScore(
            proposal_id=proposal.proposal_id,
            ml_score=ml_score,
            consensus_score=consensus_score,
            stakeholder_alignment=stakeholder_alignment,
            escalation_risk=escalation_risk,
            overall_score=overall_score,
            explanation=explanation,
        )

    def _get_ml_score(self, conflict: Conflict, proposal: Proposal) -> float:
        """Get ML model-based score."""
        if not self.is_trained:
            # Default to proposal confidence if model not trained
            return proposal.confidence

        features = np.array([self._extract_proposal_features(conflict, proposal)])
        probability = self.model.predict_proba(features)[0][1]  # Probability of success
        return probability

    def _get_consensus_score(self, conflict: Conflict, proposal: Proposal) -> float:
        """Calculate alignment with consensus."""
        if not conflict.proposals:
            return 0.5

        # Average similarity with other proposals
        similarities = []
        for other in conflict.proposals:
            if other.proposal_id != proposal.proposal_id:
                similarity = self._calculate_proposal_similarity(proposal, other)
                similarities.append(similarity)

        return np.mean(similarities) if similarities else 0.5

    def _get_stakeholder_alignment(self, conflict: Conflict, proposal: Proposal) -> float:
        """Calculate stakeholder preference alignment."""
        if not hasattr(conflict, "stakeholders") or not conflict.stakeholders:
            return 0.5

        # Calculate alignment with stakeholder preferences
        total_alignment = 0.0
        for stakeholder in conflict.stakeholders:
            # Get stakeholder preference (placeholder - would come from actual data)
            preference_score = getattr(stakeholder, "preference_score", 0.5)
            total_alignment += preference_score

        return (
            total_alignment / len(conflict.stakeholders)
            if conflict.stakeholders
            else 0.5
        )

    def _calculate_escalation_risk(
        self, conflict: Conflict, proposal: Proposal
    ) -> float:
        """Calculate risk of conflict escalation if this proposal is chosen."""
        # Factors: proposal acceptance likelihood, stakeholder satisfaction potential
        risk = 0.0

        # Risk increases with number of opposing proposals
        opposing_count = len(
            [p for p in conflict.proposals if p.proposal_id != proposal.proposal_id]
        )
        risk += opposing_count * 0.1

        # Risk based on proposal confidence
        risk += (1.0 - proposal.confidence) * 0.3

        # Clip to 0-1
        return min(1.0, max(0.0, risk))

    def _extract_features(self, record: Dict[str, Any]) -> Optional[List[float]]:
        """Extract features from historical record."""
        try:
            return [
                record.get("proposal_count", 0),
                record.get("stakeholder_count", 0),
                record.get("conflict_complexity", 0.5),
                record.get("average_confidence", 0.5),
                record.get("negotiation_rounds", 0),
            ]
        except Exception:
            return None

    def _extract_proposal_features(
        self, conflict: Conflict, proposal: Proposal
    ) -> List[float]:
        """Extract features from proposal."""
        return [
            len(conflict.proposals),
            len(getattr(conflict, "stakeholders", [])),
            proposal.confidence,
            len(conflict.proposals),  # complexity
            0.5,  # placeholder for other features
        ]

    def _calculate_proposal_similarity(self, proposal1: Proposal, proposal2: Proposal) -> float:
        """Calculate similarity between two proposals."""
        # Simple similarity based on source agent and content
        # Would be enhanced with semantic similarity in production
        similarity = 0.5  # Default neutral similarity
        if proposal1.source_agent == proposal2.source_agent:
            similarity += 0.2
        return min(1.0, similarity)

    def get_resolution_path(
        self, conflict: Conflict, max_rounds: int = 5
    ) -> ResolutionPath:
        """
        Get recommended resolution path with escalation handling.

        Args:
            conflict: Conflict to resolve
            max_rounds: Maximum negotiation rounds

        Returns:
            ResolutionPath with recommended steps
        """
        steps = []
        estimated_rounds = 0

        # Step 1: Initial consensus attempt
        steps.append("consensus_attempt")
        estimated_rounds = 1

        # Step 2: If consensus fails, try ML-based resolution
        if len(conflict.proposals) > 1:
            steps.append("ml_scoring")
            estimated_rounds += 1

        # Step 3: If still unresolved, escalation
        if estimated_rounds >= max_rounds - 1:
            steps.append("escalate_to_mediator")
            estimated_rounds += 1

        # Calculate success probability
        success_prob = 1.0 - (estimated_rounds / max_rounds * 0.3)
        success_prob = max(0.5, min(1.0, success_prob))

        return ResolutionPath(
            steps=steps,
            estimated_rounds=estimated_rounds,
            success_probability=success_prob,
            recommended_mediator="human_mediator" if estimated_rounds > 2 else None,
            escalation_triggers=[
                "disagreement_persists_after_2_rounds",
                "new_stakeholders_added",
                "proposal_similarity_below_threshold",
            ],
        )
