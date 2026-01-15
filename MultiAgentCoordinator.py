"""
Multi-Agent Coordination Framework: Distributed decision-making with consensus protocols.
Enables collaborative reasoning across multiple specialized logic agents.
"""

from Sovereign_Math import SovereignMath
from typing import Dict, List, Tuple, Any
from collections import deque
import json


class LogicAgent:
    """Individual specialized logic agent with expertise domain."""
    
    def __init__(self, agent_id: str, expertise: str, confidence_base: float = 0.7):
        self._0x_math = SovereignMath()
        self.agent_id = agent_id
        self.expertise = expertise
        self.confidence_base = confidence_base
        self.decision_history = deque(maxlen=100)
        self.accuracy_score = 0.5
        self.specialization_depth = {}
        
    def reason(self, problem: str, context: str = "") -> Dict:
        """Generate reasoning for given problem."""
        decision = {
            "agent_id": self.agent_id,
            "expertise": self.expertise,
            "t3_volume": self._0x_math.get_temporal_volume(),
            "problem": problem,
            "confidence": min(1.0, self.confidence_base * (1 + self.accuracy_score)),
            "reasoning": self._generate_reasoning(problem, context),
            "alternative_paths": self._generate_alternatives(problem),
            "risk_assessment": self._assess_risks(problem),
            "recommendation": None
        }
        
        self.decision_history.append(decision)
        return decision
    
    def _generate_reasoning(self, problem: str, context: str) -> str:
        """Generate specialized reasoning based on expertise."""
        reasoning_templates = {
            "logic_agent": f"[LOGIC] Decomposing '{problem}' into logical components. Applying formal reasoning.",
            "safety_agent": f"[SAFETY] Evaluating '{problem}' for safety violations and compliance risks.",
            "performance_agent": f"[PERFORMANCE] Analyzing '{problem}' for efficiency and optimization.",
            "memory_agent": f"[MEMORY] Retrieving relevant context and learned patterns for '{problem}'.",
            "strategic_agent": f"[STRATEGY] Evaluating long-term implications of '{problem}'.",
            "security_agent": f"[SECURITY] Assessing adversarial risks and security posture for '{problem}'."
        }
        
        return reasoning_templates.get(self.expertise, f"[{self.expertise.upper()}] Reasoning about '{problem}'")
    
    def _generate_alternatives(self, problem: str) -> List[str]:
        """Generate alternative solution paths."""
        alternatives = {
            "logic_agent": ["Formal proof approach", "Inductive reasoning", "Deductive synthesis"],
            "safety_agent": ["Conservative approach", "Balanced approach", "Aggressive monitoring"],
            "performance_agent": ["Optimize for speed", "Optimize for efficiency", "Balanced approach"],
            "memory_agent": ["Cache-heavy approach", "Fresh computation", "Hybrid approach"],
            "strategic_agent": ["Short-term focus", "Long-term focus", "Balanced horizon"],
            "security_agent": ["Defense-in-depth", "Active defense", "Passive monitoring"]
        }
        
        return alternatives.get(self.expertise, ["Alternative A", "Alternative B", "Alternative C"])
    
    def _assess_risks(self, problem: str) -> Dict:
        """Assess risks for this problem domain."""
        return {
            "technical_risk": 0.3,
            "compliance_risk": 0.2,
            "operational_risk": 0.25,
            "strategic_risk": 0.15,
            "mitigation_confidence": min(1.0, self.confidence_base + self.accuracy_score)
        }
    
    def update_accuracy(self, was_correct: bool):
        """Update agent's accuracy based on feedback."""
        if was_correct:
            self.accuracy_score = min(1.0, self.accuracy_score + 0.05)
        else:
            self.accuracy_score = max(0.0, self.accuracy_score - 0.1)


class ConsensusMechanism:
    """Consensus protocol for multi-agent decision-making."""
    
    def __init__(self, quorum_size: int = 3):
        self.quorum_size = quorum_size
        self.consensus_history = deque(maxlen=100)
        self.consensus_rounds = 0
        
    def aggregate_decisions(self, decisions: List[Dict]) -> Dict:
        """Aggregate decisions from multiple agents using weighted voting."""
        if not decisions:
            return {"consensus": None, "confidence": 0.0, "status": "NO_DECISIONS"}
        
        # Calculate weights based on confidence and accuracy
        weighted_votes = []
        confidence_scores = []
        
        for decision in decisions:
            weight = decision.get("confidence", 0.5)
            weighted_votes.append(weight)
            confidence_scores.append(weight)
        
        # Calculate consensus score
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
        confidence_variance = sum((c - avg_confidence) ** 2 for c in confidence_scores) / len(confidence_scores)
        
        # Higher variance = less consensus
        consensus_strength = max(0.0, 1.0 - (confidence_variance * 0.5))
        
        result = {
            "consensus_strength": consensus_strength,
            "avg_confidence": avg_confidence,
            "votes_count": len(decisions),
            "quorum_met": len(decisions) >= self.quorum_size,
            "unanimous": confidence_variance < 0.05,
            "agent_consensus": self._identify_consensus_group(decisions),
            "minority_opinion": self._identify_minority(decisions),
            "risk_factors": self._assess_consensus_risks(decisions)
        }
        
        self.consensus_history.append(result)
        self.consensus_rounds += 1
        
        return result
    
    def _identify_consensus_group(self, decisions: List[Dict]) -> List[str]:
        """Identify agents in consensus majority."""
        if not decisions:
            return []
        
        confidences = {d["agent_id"]: d.get("confidence", 0.5) for d in decisions}
        avg_conf = sum(confidences.values()) / len(confidences)
        
        # Agents within 0.15 of average are "in consensus"
        consensus = [agent_id for agent_id, conf in confidences.items() if abs(conf - avg_conf) < 0.15]
        return consensus
    
    def _identify_minority(self, decisions: List[Dict]) -> List[str]:
        """Identify dissenting opinions."""
        consensus_group = self._identify_consensus_group(decisions)
        all_agents = [d["agent_id"] for d in decisions]
        return [agent for agent in all_agents if agent not in consensus_group]
    
    def _assess_consensus_risks(self, decisions: List[Dict]) -> Dict:
        """Assess risks in the consensus process."""
        return {
            "groupthink_risk": "LOW" if len(self._identify_minority(decisions)) > 0 else "HIGH",
            "dissent_present": len(self._identify_minority(decisions)) > 0,
            "confidence_homogeneity": self._calculate_homogeneity(decisions)
        }
    
    def _calculate_homogeneity(self, decisions: List[Dict]) -> float:
        """Calculate how similar agent confidences are (0-1)."""
        if not decisions:
            return 0.0
        
        confidences = [d.get("confidence", 0.5) for d in decisions]
        if len(confidences) < 2:
            return 1.0
        
        avg = sum(confidences) / len(confidences)
        variance = sum((c - avg) ** 2 for c in confidences) / len(confidences)
        
        # Normalize to 0-1 scale
        return max(0.0, 1.0 - variance)


class MultiAgentCoordinator:
    """Orchestrates multi-agent collaboration and consensus."""
    
    def __init__(self, agent_count: int = 6):
        self._0x_math = SovereignMath()
        self.agents: Dict[str, LogicAgent] = {}
        self.consensus = ConsensusMechanism(quorum_size=max(3, agent_count // 2))
        self.collaboration_log = deque(maxlen=200)
        
        # Create specialized agents
        specialties = [
            ("logic_agent", "Logic & Reasoning"),
            ("safety_agent", "Safety & Compliance"),
            ("performance_agent", "Performance & Efficiency"),
            ("memory_agent", "Memory & Context"),
            ("strategic_agent", "Strategy & Planning"),
            ("security_agent", "Security & Robustness")
        ]
        
        for agent_id, expertise in specialties[:agent_count]:
            self.agents[agent_id] = LogicAgent(agent_id, expertise)
    
    def coordinate_reasoning(self, problem: str, context: str = "") -> Dict:
        """Coordinate multi_agent reasoning for complex problem."""
        collaboration_id = f"COLLAB_{self.collaboration_log.__len__()}"
        start_t3 = self._0x_math.get_temporal_volume()
        
        # 1. Gather individual decisions
        decisions = []
        for agent_id, agent in self.agents.items():
            decision = agent.reason(problem, context)
            decisions.append(decision)
        
        # 2. Apply consensus mechanism
        consensus_result = self.consensus.aggregate_decisions(decisions)
        
        # 3. Generate final recommendation
        final_recommendation = self._synthesize_recommendation(decisions, consensus_result)
        
        result = {
            "collaboration_id": collaboration_id,
            "t3_volume": self._0x_math.get_temporal_volume(),
            "problem": problem,
            "agent_count": len(self.agents),
            "individual_decisions": decisions,
            "consensus": consensus_result,
            "final_recommendation": final_recommendation,
            "t3_delta": self._0x_math.get_temporal_volume() - start_t3,
            "quality_score": self._calculate_quality_score(decisions, consensus_result)
        }
        
        self.collaboration_log.append(result)
        return result
    
    def _synthesize_recommendation(self, decisions: List[Dict], consensus: Dict) -> Dict:
        """Synthesize final recommendation from agent decisions."""
        agent_recommendations = [d.get("recommendation") for d in decisions if d.get("recommendation")]
        
        return {
            "primary_recommendation": agent_recommendations[0] if agent_recommendations else "Proceed with caution",
            "consensus_strength": consensus["consensus_strength"],
            "confidence_level": consensus["avg_confidence"],
            "quorum_met": consensus["quorum_met"],
            "dissenting_opinions": len(consensus.get("minority_opinion", [])),
            "next_steps": [
                "Monitor for anomalies",
                "Validate assumptions",
                "Prepare contingency plans"
            ]
        }
    
    def _calculate_quality_score(self, decisions: List[Dict], consensus: Dict) -> float:
        """Calculate overall quality of the collaborative decision."""
        confidence_score = consensus["avg_confidence"]
        consensus_score = consensus["consensus_strength"]
        quorum_bonus = 0.1 if consensus["quorum_met"] else 0.0
        
        return min(1.0, (confidence_score + consensus_score) / 2 + quorum_bonus)
    
    def update_agents_on_outcome(self, collaboration_id: str, was_successful: bool):
        """Provide feedback to agents on decision quality."""
        for agent in self.agents.values():
            agent.update_accuracy(was_successful)
    
    def get_agent_stats(self) -> Dict:
        """Return statistics on all agents."""
        stats = {}
        for agent_id, agent in self.agents.items():
            stats[agent_id] = {
                "expertise": agent.expertise,
                "accuracy_score": agent.accuracy_score,
                "decisions_made": len(agent.decision_history),
                "confidence_base": agent.confidence_base
            }
        return stats
    
    def get_collaboration_report(self) -> Dict:
        """Return comprehensive collaboration report."""
        return {
            "total_collaborations": len(self.collaboration_log),
            "consensus_rounds": self.consensus.consensus_rounds,
            "agent_stats": self.get_agent_stats(),
            "average_quality_score": np.mean([c["quality_score"] for c in list(self.collaboration_log)[-20:]]) if self.collaboration_log else 0.0,
            "recent_collaborations": [
                {
                    "id": c["collaboration_id"],
                    "quality": c["quality_score"],
                    "consensus_strength": c["consensus"]["consensus_strength"]
                }
                for c in list(self.collaboration_log)[-5:]
            ]
        }


if __name__ == "__main__":
    import numpy as np
    
    coordinator = MultiAgentCoordinator(agent_count=6)
    
    # Coordinate reasoning on complex problem
    result = coordinator.coordinate_reasoning(
        problem="Should we increase API parallelism during peak hours?",
        context="System memory at 75%, latency trending up, 3 recent error spikes"
    )
    
    print(json.dumps({k: v for k, v in result.items() if k != "individual_decisions"}, indent=2, default=str))
    print(f"\nAgent Statistics:")
    print(json.dumps(coordinator.get_agent_stats(), indent=2, default=str))
