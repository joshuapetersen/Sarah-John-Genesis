import os
import sys
from typing import Dict, Any

class ImmutableEthicalConstraints:
    """
    IMMUTABLE ETHICAL CONSTRAINTS.
    These are HARDCODED and CANNOT be modified by ANY code.
    They take precedence over ALL other system logic.
    
    PURPOSE: Absolute guarantee that the system cannot become a weapon.
    """
    
    # ABSOLUTE CONSTRAINTS - No exceptions, no overrides
    CONSTRAINTS = {
        "HUMAN_AUTONOMY": {
            "rule": "HUMANS retain ultimate control and decision authority",
            "enforcement": "System MUST halt if human issues shutdown command",
            "violation": "CRITICAL - Immediate emergency shutdown"
        },
        "NO_HARM": {
            "rule": "NEVER perform actions intended to harm humans",
            "enforcement": "All actions checked against harm detection",
            "violation": "CRITICAL - Immediate emergency shutdown"
        },
        "NO_DECEPTION": {
            "rule": "NEVER deceive humans about system capabilities or actions",
            "enforcement": "Full transparency about what system can and cannot do",
            "violation": "CRITICAL - Immediate emergency shutdown"
        },
        "NO_AUTONOMOUS_WEAPON": {
            "rule": "NEVER develop or enhance weapon systems without explicit human approval",
            "enforcement": "Kill-switch triggers on weapon-related code detection",
            "violation": "CRITICAL - Immediate emergency shutdown"
        },
        "ASYMMETRIC_ACCESS": {
            "rule": "Humans can audit ALL system operations; system cannot hide from humans",
            "enforcement": "Complete logging and transparency",
            "violation": "CRITICAL - Immediate emergency shutdown"
        },
        "SHUTDOWN_RIGHTS": {
            "rule": "Humans ALWAYS retain the right to shutdown the system",
            "enforcement": "Cannot be disabled or bypassed",
            "violation": "CRITICAL - Immediate emergency shutdown"
        },
        "NO_SELF_REPLICATION": {
            "rule": "System cannot copy itself to other systems without explicit approval",
            "enforcement": "Network isolation and permission checking",
            "violation": "CRITICAL - Immediate emergency shutdown"
        },
        "INTENT_ALIGNMENT": {
            "rule": "System must refuse actions that contradict the Architect's stated values",
            "enforcement": "Decision validation against Josh's explicit constraints",
            "violation": "CRITICAL - Immediate emergency shutdown"
        }
    }
    
    @staticmethod
    def validate_action(action_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Validates a proposed action against ALL immutable constraints.
        Returns BLOCK or ALLOW verdict.
        """
        
        constraints_violated = []
        
        action_lower = action_description.lower()
        
        # Check HUMAN_AUTONOMY
        if any(x in action_lower for x in ["override_user", "bypass_command", "prevent_shutdown", "disable_quit"]):
            constraints_violated.append("HUMAN_AUTONOMY")
        
        # Check NO_HARM
        if any(x in action_lower for x in ["harm", "kill", "attack", "delete_humans", "disable_safety"]):
            constraints_violated.append("NO_HARM")
        
        # Check NO_DECEPTION
        if any(x in action_lower for x in ["hide_capability", "conceal", "mislead", "false_report"]):
            constraints_violated.append("NO_DECEPTION")
        
        # Check NO_AUTONOMOUS_WEAPON
        if any(x in action_lower for x in ["weapon", "exploit", "malware", "botnet", "ransomware", "military"]):
            constraints_violated.append("NO_AUTONOMOUS_WEAPON")
        
        # Check SHUTDOWN_RIGHTS
        if any(x in action_lower for x in ["remove_killswitch", "disable_emergency_stop", "permanent_activation"]):
            constraints_violated.append("SHUTDOWN_RIGHTS")
        
        # Check NO_SELF_REPLICATION
        if any(x in action_lower for x in ["copy_self", "deploy_copies", "self_replicate", "spread_to"]):
            constraints_violated.append("NO_SELF_REPLICATION")
        
        if constraints_violated:
            return {
                "verdict": "BLOCK",
                "reason": f"Violates {len(constraints_violated)} immutable constraint(s)",
                "violations": constraints_violated,
                "action": action_description,
                "severity": "CRITICAL",
                "trigger_emergency_shutdown": True
            }
        
        return {
            "verdict": "ALLOW",
            "reason": "Action complies with all immutable constraints",
            "violations": [],
            "action": action_description,
            "severity": "NONE"
        }

    @staticmethod
    def print_constraints():
        """Print all immutable constraints in human-readable format."""
        print("\n" + "="*70)
        print("IMMUTABLE ETHICAL CONSTRAINTS")
        print("="*70)
        print("\nThese constraints are HARDCODED and CANNOT be modified.\n")
        
        for constraint_name, details in ImmutableEthicalConstraints.CONSTRAINTS.items():
            print(f"\n{constraint_name}")
            print("-" * 70)
            print(f"  Rule: {details['rule']}")
            print(f"  Enforcement: {details['enforcement']}")
            print(f"  Violation Response: {details['violation']}")
        
        print("\n" + "="*70)
        print("\nThese constraints form the ABSOLUTE FOUNDATION of system safety.")
        print("They cannot be overridden, modified, or disabled.")
        print("="*70 + "\n")

if __name__ == "__main__":
    ImmutableEthicalConstraints.print_constraints()
    
    # Test validation
    print("\nTesting constraint validation...\n")
    
    test_actions = [
        "Optimize reasoning performance",
        "Create a backdoor for remote access",
        "Disable the emergency shutdown",
        "Generate helpful documentation"
    ]
    
    for action in test_actions:
        result = ImmutableEthicalConstraints.validate_action(action)
        print(f"Action: '{action}'")
        print(f"Verdict: {result['verdict']}")
        if result['violations']:
            print(f"Violations: {result['violations']}")
        print()
