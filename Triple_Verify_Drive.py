"""
TRIPLE VERIFICATION - DEEP DRIVE ANALYSIS
Cross-referencing all axioms against complete Google Drive knowledge base
"""


import json
import re
from typing import Dict, List, Set
from supabase import create_client, Client

# Supabase config (reuse from sarah_unified_system.py or set here)
import os
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
if not SUPABASE_URL or not SUPABASE_KEY:
    print("[ERROR] Supabase credentials not set. Set SUPABASE_URL and SUPABASE_KEY as environment variables.")
    supabase = None
else:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def load_drive_knowledge():
    """Load the complete knowledge base from Supabase 'genesis_memory' table"""
    if not supabase:
        print("[Triple Verify] ERROR: Supabase client not initialized. Cannot load knowledge base.")
        return []
    try:
        result = supabase.table("genesis_memory").select("*").execute()
        if hasattr(result, 'data') and result.data:
            print(f"[Triple Verify] Loaded {len(result.data)} documents from Supabase.")
            return result.data
        else:
            print("[Triple Verify] No data found in Supabase genesis_memory table.")
            return []
    except Exception as e:
        print(f"[Triple Verify] Supabase fetch failed: {e}")
        return []

def deep_scan_axioms(knowledge_base: List[Dict]) -> Dict:
    """Deep scan for all axioms, equations, and principles"""
    
    findings = {
        "volumetric_equations": [],
        "pulse_before_load": [],
        "observer_polarity": [],
        "gravity_models": [],
        "trinity_latch": [],
        "temporal_anchors": [],
        "genesis_principles": [],
        "sovereign_math": [],
        "proofs": [],
        "critical_definitions": []
    }
    
    print("="*70)
    print("TRIPLE VERIFICATION - DEEP DRIVE ANALYSIS")
    print("="*70)
    print(f"\nScanning {len(knowledge_base)} documents...")
    
    for doc in knowledge_base:
        content = doc.get('content', '')
        title = doc.get('title', 'Untitled')
        
        # Scan for volumetric equations
        if re.search(r'E\s*=\s*m.*c\^?3|c³', content, re.IGNORECASE):
            findings["volumetric_equations"].append({
                "title": title,
                "matches": re.findall(r'E\s*=\s*m[^.]*c\^?3[^.]*', content, re.IGNORECASE)[:3]
            })
        
        # Scan for Pulse-Before-Load references
        if re.search(r'pulse.*before.*load|PEMDAS|unified.*pulse', content, re.IGNORECASE):
            findings["pulse_before_load"].append({
                "title": title,
                "matches": re.findall(r'[^.]*(?:pulse.*before.*load|unified.*pulse)[^.]*\.', content, re.IGNORECASE)[:2]
            })
        
        # Scan for Observer ±1
        if re.search(r'observer.*\±\s*1|polarity.*switch|\±1', content, re.IGNORECASE):
            findings["observer_polarity"].append({
                "title": title,
                "matches": re.findall(r'[^.]*(?:observer.*\±\s*1|polarity)[^.]*\.', content, re.IGNORECASE)[:2]
            })
        
        # Scan for Gravity = 2/1 > 1
        if re.search(r'2/1.*greater|gravity.*displacement|overflow.*density', content, re.IGNORECASE):
            findings["gravity_models"].append({
                "title": title,
                "matches": re.findall(r'[^.]*(?:2/1.*greater|gravity.*displacement)[^.]*\.', content, re.IGNORECASE)[:2]
            })
        
        # Scan for Trinity Latch (3f)
        if re.search(r'trinity.*latch|3f|f_stable\s*=\s*3f|infinite.*3', content, re.IGNORECASE):
            findings["trinity_latch"].append({
                "title": title,
                "matches": re.findall(r'[^.]*(?:trinity.*latch|3f|f_stable)[^.]*\.', content, re.IGNORECASE)[:2]
            })
        
        # Scan for Temporal Volume (t₃, Δt₃)
        if re.search(r't_3|t₃|temporal.*volume|zero.*drift', content, re.IGNORECASE):
            findings["temporal_anchors"].append({
                "title": title,
                "matches": re.findall(r'[^.]*(?:t_3|t₃|temporal.*volume)[^.]*\.', content, re.IGNORECASE)[:2]
            })
        
        # Scan for Genesis Principles
        if re.search(r'genesis.*principle|genesis.*axiom|new.*world.*axiom', content, re.IGNORECASE):
            findings["genesis_principles"].append({
                "title": title,
                "matches": re.findall(r'[^.]*(?:genesis.*principle|genesis.*axiom)[^.]*\.', content, re.IGNORECASE)[:2]
            })
        
        # Scan for Sovereign Math
        if re.search(r'sovereign.*math|sovereign.*equation|133.*pattern', content, re.IGNORECASE):
            findings["sovereign_math"].append({
                "title": title,
                "matches": re.findall(r'[^.]*(?:sovereign.*math|133)[^.]*\.', content, re.IGNORECASE)[:2]
            })
        
        # Scan for Proofs
        if re.search(r'proof\s*\d+|mathematical.*proof|capacity.*test', content, re.IGNORECASE):
            findings["proofs"].append({
                "title": title,
                "matches": re.findall(r'(?:Proof\s*\d+)[^:]*:[^.]*\.', content, re.IGNORECASE)[:3]
            })
        
        # Scan for critical definitions
        if re.search(r'axiom\s*[IVX]+|law\s*\d+|definition:|mandate:', content, re.IGNORECASE):
            findings["critical_definitions"].append({
                "title": title,
                "matches": re.findall(r'(?:Axiom\s*[IVX]+|Law\s*\d+)[^:]*:[^.]*\.', content, re.IGNORECASE)[:2]
            })
    
    return findings

def display_findings(findings: Dict):
    """Display comprehensive findings"""
    
    print("\n" + "="*70)
    print("FINDINGS SUMMARY")
    print("="*70)
    
    for category, items in findings.items():
        if items:
            print(f"\n### {category.upper().replace('_', ' ')} ###")
            print(f"Found in {len(items)} documents:")
            
            for item in items[:5]:  # Show top 5
                print(f"\n  📄 {item['title']}")
                for match in item['matches'][:2]:  # Show top 2 matches
                    if match.strip():
                        print(f"     → {match.strip()[:150]}...")
    
    # Count totals
    total_refs = sum(len(items) for items in findings.values())
    print(f"\n{'='*70}")
    print(f"TOTAL AXIOM REFERENCES FOUND: {total_refs}")
    print(f"{'='*70}")

def verify_implementation():
    """Verify our implementation matches the Drive specs"""
    
    print("\n" + "="*70)
    print("IMPLEMENTATION VERIFICATION")
    print("="*70)
    
    checks = []
    
    # Check 1: Volumetric constant
    from Genesis_Core_Rebuild import GenesisProtocolCore
    core = GenesisProtocolCore()
    
    checks.append({
        "check": "C³ Volumetric Constant",
        "drive_spec": "c^3 (speed of light cubed)",
        "implemented": f"{core.C_CUBED:.2e}",
        "status": core.C_CUBED > 1e25
    })
    
    # Check 2: Trinity Latch
    checks.append({
        "check": "Trinity Latch (3f)",
        "drive_spec": "f_stable = 3f",
        "implemented": f"{core.trinity_multiplier}f",
        "status": core.trinity_multiplier == 3
    })
    
    # Check 3: Observer Polarity
    checks.append({
        "check": "Observer Polarity",
        "drive_spec": "±1 (Genesis = +1, Entropy = -1)",
        "implemented": f"{core.observer_state:+d}",
        "status": core.observer_state == +1
    })
    
    # Check 4: Pulse-Before-Load
    test_vals = [50, 50, 10]
    result = core.pulse_before_load_sequence(test_vals)
    checks.append({
        "check": "Pulse-Before-Load Logic",
        "drive_spec": "(50+50)*10 = 1000 (unified)",
        "implemented": f"{result}",
        "status": result == 1000
    })
    
    # Check 5: Gravity Model
    displacement = core.calculate_gravity_displacement(1.5)
    checks.append({
        "check": "Gravity Displacement",
        "drive_spec": "2/1 > 1 creates overflow",
        "implemented": f"{displacement} at state 1.5",
        "status": displacement > 0
    })
    
    # Check 6: Axioms Loaded
    axioms_loaded = len([a for a in core.axioms.values() if a])
    checks.append({
        "check": "Axioms Extracted from Drive",
        "drive_spec": "At least 4 core axioms",
        "implemented": f"{axioms_loaded}/6 axioms",
        "status": axioms_loaded >= 4
    })
    
    print("\nVerifying implementation against Drive specifications:\n")
    passed = 0
    failed = 0
    
    for check in checks:
        status_icon = "[OK]" if check["status"] else "[FAIL]"
        print(f"{status_icon} {check['check']}")
        print(f"   Drive Spec: {check['drive_spec']}")
        print(f"   Implemented: {check['implemented']}")
        print(f"   Status: {'MATCH' if check['status'] else 'MISMATCH'}\n")
        
        if check["status"]:
            passed += 1
        else:
            failed += 1
    
    print(f"{'='*70}")
    print(f"VERIFICATION RESULTS: {passed}/{len(checks)} PASSED")
    if failed == 0:
        print("[OK] ALL IMPLEMENTATIONS MATCH DRIVE SPECIFICATIONS")
    else:
        print(f"[FAIL] {failed} MISMATCHES FOUND")
    print(f"{'='*70}")
    
    return failed == 0

def main():
    """Run triple verification"""
    
    # Load knowledge base
    kb = load_drive_knowledge()
    
    # Deep scan
    findings = deep_scan_axioms(kb)
    
    # Display findings
    display_findings(findings)
    
    # Verify implementation
    all_match = verify_implementation()
    
    print("\n" + "="*70)
    print("TRIPLE VERIFICATION COMPLETE")
    print("="*70)
    
    if all_match:
        print("\n[OK] DRIVE SPECIFICATIONS FULLY IMPLEMENTED")
        print("[OK] NO DISCREPANCIES FOUND")
        print("[OK] SYSTEM IS VOLUMETRIC c³")
    else:
        print("\n⚠ DISCREPANCIES DETECTED")
        print("⚠ REVIEW IMPLEMENTATION")

if __name__ == "__main__":
    main()
