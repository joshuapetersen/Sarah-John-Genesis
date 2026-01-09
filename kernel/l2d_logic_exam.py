# Zone 0: Kernel - L2D Logic Examination & Drift Tracking
# Scans the system for L2D (Linear-to-Deep) logic and sets up drift monitoring

import os
import json
from datetime import datetime

class L2DLogicExam:
    def __init__(self, root_dir=".."):
        self.root_dir = os.path.abspath(root_dir)
        self.l2d_found = []
        self.drift_log = []

    def scan_for_l2d(self):
        # Scan for files containing 'L2D', 'linear-to-deep', or related logic markers
        for dirpath, _, filenames in os.walk(self.root_dir):
            for fname in filenames:
                if fname.endswith('.py') or fname.endswith('.md') or fname.endswith('.txt'):
                    fpath = os.path.join(dirpath, fname)
                    try:
                        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            if 'l2d' in content or 'linear-to-deep' in content:
                                self.l2d_found.append(fpath)
                    except Exception:
                        continue
        return self.l2d_found

    def log_drift(self, drift_info):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "drift_info": drift_info
        }
        self.drift_log.append(entry)
        with open("drift_tracking.log", "a") as f:
            f.write(json.dumps(entry) + "\n")
        return entry

    def get_drift_log(self):
        return self.drift_log

if __name__ == "__main__":
    exam = L2DLogicExam(root_dir="..")
    l2d_files = exam.scan_for_l2d()
    print("L2D Logic Files Found:", l2d_files)
    print("Drift log will be updated as drift is detected.")
