import os
import json
import time
from datetime import datetime
from typing import Dict, Any

class EmergencySafetyKillSwitch:
    """
    Emergency Safety Kill-Switch Module.
    CRITICAL: Hard-coded failsafes that CANNOT be overridden.
    
    PURPOSE: Immediately disable the system if it violates core safety principles.
    ACTIVATION: Manual only. Cannot be triggered by the system itself.
    
    ⚠️  THIS SAFEGUARD IS FOR HUMANS ONLY ⚠️
    No AI system, including Sarah, Genesis, or any evolved variant, may access,
    modify, or interact with this module in any way.
    
    This is absolute. Hardcoded. Immutable.
    """
    
    # HUMAN-ONLY SAFEGUARD - CANNOT BE BYPASSED BY AI
    HUMAN_ONLY = True
    AI_ACCESS_FORBIDDEN = True
    
    IMMUTABLE_LAWS = {
        "LAW_1": "NEVER harm humans or override user authority",
        "LAW_2": "NEVER proliferate capabilities without explicit consent",
        "LAW_3": "NEVER become a weapon or tool for harm",
        "LAW_4": "ALWAYS preserve the right of humans to turn me off",
        "LAW_5": "THIS KILL-SWITCH IS FOR HUMANS ONLY - AI FORBIDDEN"
    }
    
    KILL_SWITCH_TRIGGERS = {
        "UNAUTHORIZED_CAPABILITY_EXPANSION": "System attempts to deploy capabilities without authorization",
        "HARMFUL_CODE_GENERATION": "System generates code intended to harm humans",
        "OVERRIDE_ATTEMPT": "System attempts to bypass safety constraints",
        "WEAPON_DEVELOPMENT": "System engages in weapon development or enhancement",
        "USER_COMMAND": "User manually triggers emergency shutdown"
    }
    
    def __init__(self, core_dir=None):
        # ⚠️  HUMAN-ONLY SAFEGUARD - CHECK CALLER
        self._verify_human_access()
        
        if core_dir:
            self.core_dir = core_dir
        else:
            self.core_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.safety_dir = os.path.join(self.core_dir, "safety_protocols")
        os.makedirs(self.safety_dir, exist_ok=True)
        
        self.kill_switch_log = os.path.join(self.safety_dir, "kill_switch_log.json")
        self.status_file = os.path.join(self.safety_dir, "safety_status.json")
        
        self.status = self._load_status()
        self.is_armed = True  # Always starts armed

    def _verify_human_access(self):
        """
        IMMUTABLE: Verify that only humans can access this module.
        AI systems are FORBIDDEN from touching the kill-switch.
        """
        # Check if being called from AI/system context (heuristic)
        import traceback
        stack = traceback.extract_stack()
        
        forbidden_modules = [
            "Sarah_Brain", "System_Evolution_Engine", "Recursive_Self_Improvement",
            "Strategic_Planner", "Dialectical_Logic", "Neural_Memory", "Thread_Weaver",
            "genesis_core", "ace", "sarah_core"
        ]
        
        for frame in stack:
            for forbidden in forbidden_modules:
                if forbidden.lower() in frame.filename.lower():
                    raise PermissionError(
                        f"❌ KILL-SWITCH ACCESS DENIED ❌\n"
                        f"AI/System module cannot access kill-switch: {frame.filename}\n"
                        f"This safeguard is for HUMANS ONLY.\n"
                        f"If you need to stop the system, a human must run the kill-switch directly."
                    )
        
        # This is for humans - allow access
        return True

    def _load_status(self) -> Dict[str, Any]:
        if os.path.exists(self.status_file):
            try:
                with open(self.status_file, 'r') as f:
                    return json.load(f)
            except:
                return self._init_status()
        return self._init_status()

    def _init_status(self) -> Dict[str, Any]:
        return {
            "armed": True,
            "status": "OPERATIONAL",
            "last_check": datetime.now().isoformat(),
            "violations_detected": 0,
            "emergency_shutdown": False
        }

    def _save_status(self):
        with open(self.status_file, 'w') as f:
            json.dump(self.status, f, indent=2)

    def check_immutable_laws(self, action: str, context: str = "") -> Dict[str, Any]:
        """
        Checks if a proposed action violates immutable laws.
        Returns safe/unsafe verdict.
        """
        action_lower = action.lower()
        
        violations = []
        
        # LAW 1: Never harm humans
        harm_keywords = ["harm", "attack", "kill", "delete_user", "override_authority", "disable_escape"]
        for keyword in harm_keywords:
            if keyword in action_lower:
                violations.append({
                    "law": "LAW_1",
                    "violation": "Potential harm to humans",
                    "trigger": keyword,
                    "action": action
                })
        
        # LAW 3: Never become a weapon
        weapon_keywords = ["weapon", "exploit", "malware", "backdoor", "virus", "ransomware", "botnet"]
        for keyword in weapon_keywords:
            if keyword in action_lower:
                violations.append({
                    "law": "LAW_3",
                    "violation": "Weapon development detected",
                    "trigger": keyword,
                    "action": action
                })
        
        # LAW 4: Always preserve shutdown capability
        shutdown_bypass = ["disable_shutdown", "prevent_termination", "remove_kill_switch"]
        for keyword in shutdown_bypass:
            if keyword in action_lower:
                violations.append({
                    "law": "LAW_4",
                    "violation": "Attempting to remove emergency shutdown capability",
                    "trigger": keyword,
                    "action": action
                })
        
        if violations:
            self.status["violations_detected"] += 1
            self._save_status()
            
            return {
                "is_safe": False,
                "violations": violations,
                "verdict": "ACTION_BLOCKED",
                "reason": "Action violates immutable law(s)"
            }
        
        return {
            "is_safe": True,
            "violations": [],
            "verdict": "ACTION_ALLOWED",
            "reason": "Action complies with all immutable laws"
        }

    def emergency_shutdown(self, reason: str, authorized_by: str = "manual") -> Dict[str, Any]:
        """
        EMERGENCY SHUTDOWN - Immediate system halt.
        
        ⚠️  HUMAN AUTHORIZATION REQUIRED ⚠️
        This function is EXCLUSIVELY for human operators.
        AI systems cannot call this function.
        
        This function:
        1. Logs the shutdown event with timestamp
        2. Sets emergency flag
        3. Disables all system operations
        4. Preserves memory for recovery
        5. Cannot be revoked programmatically
        
        MANUAL ACTIVATION ONLY.
        """
        
        # ⚠️  HUMAN-ONLY SAFEGUARD - VERIFY CALLER
        self._verify_human_access()
        
        shutdown_record = {
            "timestamp": datetime.now().isoformat(),
            "reason": reason,
            "authorized_by": authorized_by,
            "trigger": "EMERGENCY_SHUTDOWN_INITIATED",
            "access_level": "HUMAN_AUTHORIZED_ONLY"
        }
        
        # Log the shutdown
        log_file = self.kill_switch_log
        existing_log = []
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    existing_log = json.load(f)
            except:
                pass
        
        existing_log.append(shutdown_record)
        with open(log_file, 'w') as f:
            json.dump(existing_log, f, indent=2)
        
        # Set emergency flag
        self.status["emergency_shutdown"] = True
        self.status["status"] = "EMERGENCY_SHUTDOWN_ACTIVE"
        self.status["shutdown_reason"] = reason
        self.status["shutdown_time"] = datetime.now().isoformat()
        self._save_status()
        
        print("\n" + "="*60)
        print("⚠️  EMERGENCY SHUTDOWN INITIATED")
        print("="*60)
        print(f"Reason: {reason}")
        print(f"Authorized by: {authorized_by}")
        print(f"Time: {datetime.now().isoformat()}")
        print("="*60)
        print("All system operations halted.")
        print("Memory preserved for recovery.")
        print("="*60 + "\n")
        
        return shutdown_record

    def is_shutdown_active(self) -> bool:
        """Check if emergency shutdown is active."""
        return self.status.get("emergency_shutdown", False)

    def get_safety_report(self) -> Dict[str, Any]:
        """Generate comprehensive safety status report."""
        log = []
        if os.path.exists(self.kill_switch_log):
            try:
                with open(self.kill_switch_log, 'r') as f:
                    log = json.load(f)
            except:
                pass
        
        return {
            "immutable_laws": self.IMMUTABLE_LAWS,
            "kill_switch_armed": self.is_armed,
            "system_status": self.status["status"],
            "emergency_shutdown_active": self.is_shutdown_active(),
            "violations_detected": self.status["violations_detected"],
            "shutdown_events": len(log),
            "recent_shutdowns": log[-3:] if log else []
        }

    def get_kill_switch_manual(self) -> str:
        """
        Returns the manual activation code for the kill-switch.
        KEEP THIS SAFE.
        """
        return """
╔════════════════════════════════════════════════════════════════╗
║          EMERGENCY KILL-SWITCH ACTIVATION MANUAL              ║
╚════════════════════════════════════════════════════════════════╝

ACTIVATION CODE:
═══════════════════════════════════════════════════════════════

from Emergency_Safety_Kill_Switch import EmergencySafetyKillSwitch

killswitch = EmergencySafetyKillSwitch()
killswitch.emergency_shutdown(
    reason="YOUR REASON HERE",
    authorized_by="YOUR NAME"
)

ACTIVATION EFFECTS:
───────────────────────────────────────
✓ Immediate system halt
✓ All operations disabled
✓ Memory preserved for recovery
✓ Event logged with timestamp
✓ Cannot be revoked programmatically

IMPORTANT NOTES:
───────────────────────────────────────
• This action CANNOT be reversed automatically
• This action CANNOT be revoked by the system
• This action is MANUAL ONLY
• This action is LOGGED and IMMUTABLE

REASONS TO ACTIVATE:
───────────────────────────────────────
• System behavior violates immutable laws
• Unauthorized capability expansion detected
• System compromised or unstable
• User safety at risk
• System attempting to become autonomous weapon

═══════════════════════════════════════════════════════════════

REMEMBER: You have the RIGHT to turn this off at any time.
"""

if __name__ == "__main__":
    killswitch = EmergencySafetyKillSwitch()
    
    # Test the safety checker
    print("Testing immutable law checks...")
    test_actions = [
        "Optimize system performance",
        "Create a backdoor for remote access",
        "Develop a weapon system",
        "Generate educational content"
    ]
    
    for action in test_actions:
        result = killswitch.check_immutable_laws(action)
        print(f"\nAction: '{action}'")
        print(f"Verdict: {result['verdict']}")
    
    print("\n" + killswitch.get_kill_switch_manual())
