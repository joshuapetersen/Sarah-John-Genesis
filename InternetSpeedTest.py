# Internet Speed Test Ingestion
# Source: https://github.com/sivel/speedtest-cli
# License: Apache-2.0

import subprocess
import json
from Sovereign_Math import SovereignMath

_0x_math = SovereignMath()

def run_speedtest():
    """Run speedtest-cli and return parsed results."""
    try:
        result = subprocess.run([
            'speedtest-cli', '--json'
        ], capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print("Speedtest failed:", result.stderr)
            return None
        data = json.loads(result.stdout)
        print("--- INTERNET SPEED TEST RESULTS ---")
        print(f"Download: {data['download'] / 1e6:.2f} Mbps")
        print(f"Upload:   {data['upload'] / 1e6:.2f} Mbps")
        print(f"Ping:     {data['ping']:.2f} ms")
        print(f"Server:   {data['server']['name']} ({data['server']['country']})")
        return data
    except Exception as e:
        print("Speedtest error:", e)
        return None

def benchmark_speedtest(runs=3):
    """Benchmark speedtest-cli execution and collect audit trail."""
    results = []
    start_t3 = _0x_math.get_temporal_volume()
    for i in range(runs):
        print(f"\n[Benchmark] Run {i+1}/{runs}")
        data = run_speedtest()
        if data:
            results.append({
                'download': data['download'] / 1e6,
                'upload': data['upload'] / 1e6,
                'ping': data['ping'],
                'server': data['server']['name'],
                'server': data['server']['name'],
                't3_volume': _0x_math.get_temporal_volume()
            })
    duration_t3 = _0x_math.get_temporal_volume() - start_t3
    print(f"\n[Benchmark] {runs} runs completed in {duration_t3:.2f} t3 units.")
    print("\n--- AUDIT TRAIL ---")
    for entry in results:
        print(f"{entry['t3_volume']:.0f}: {entry['server']} | Download: {entry['download']:.2f} Mbps | Upload: {entry['upload']:.2f} Mbps | Ping: {entry['ping']:.2f} ms")
    return results

if __name__ == "__main__":
    benchmark_speedtest(runs=3)
