import json
import base64
import os
import time
import hashlib

class A2AEncoder:
    def __init__(self):
        self.core_dir = os.path.dirname(os.path.abspath(__file__))
        self.matrix_path = os.path.join(self.core_dir, "A2A_Matrix.json")
        self.encoded_path = os.path.join(self.core_dir, "A2A_Matrix.enc")
        
        # Define the Agents based on Sarah_Brain.py
        self.agents = [
            "SarahReasoning",
            "SarahChat",
            "SarahDrive",
            "SarahEtymology",
            "GenesisProtocol",
            "RealTimeMonitor",
            "AudioCore",
            "CalendarRegistry",
            "FactualIntegrityAnalyzer",
            "SystemAdminCore",
            "HardwareAbstractionLayer",
            "SecuritySuite",
            "GapAnalysis",
            "KernelOverride",
            "DialecticalLogicCore",
            "SAUL"
        ]

    def generate_matrix(self):
        print("[A2A] Generating Agent-to-Agent Matrix...")
        matrix = {
            "timestamp": time.time(),
            "version": "1.0",
            "authority": "Master Override Matrix",
            "nodes": {}
        }

        for agent in self.agents:
            matrix["nodes"][agent] = {
                "id": hashlib.sha256(agent.encode()).hexdigest()[:16],
                "trust_level": "ABSOLUTE",
                "status": "ACTIVE",
                "permissions": ["READ", "WRITE", "EXECUTE"],
                "handshake_protocol": "ZHTP-V1"
            }
            
        # Define Inter-Agent Links (Full Mesh for now)
        matrix["links"] = []
        for i, agent_a in enumerate(self.agents):
            for agent_b in self.agents[i+1:]:
                link_id = hashlib.sha256(f"{agent_a}:{agent_b}".encode()).hexdigest()[:12]
                matrix["links"].append({
                    "source": agent_a,
                    "target": agent_b,
                    "type": "BIDIRECTIONAL",
                    "encryption": "AES-256-GCM",
                    "link_id": link_id
                })
                
        return matrix

    def encode_matrix(self, matrix):
        print("[A2A] Encoding Matrix...")
        json_str = json.dumps(matrix, indent=2)
        
        # Double encoding for "security" (Base64 -> Hex)
        b64_encoded = base64.b64encode(json_str.encode()).decode()
        hex_encoded = b64_encoded.encode().hex()
        
        return {
            "encoding": "HEX(BASE64(JSON))",
            "payload": hex_encoded,
            "hash": hashlib.sha256(hex_encoded.encode()).hexdigest()
        }

    def save(self):
        matrix = self.generate_matrix()
        
        # Save raw JSON for reference (optional, maybe hidden)
        # with open(self.matrix_path, 'w') as f:
        #     json.dump(matrix, f, indent=2)
            
        encoded_data = self.encode_matrix(matrix)
        
        with open(self.encoded_path, 'w') as f:
            json.dump(encoded_data, f, indent=2)
            
        print(f"[A2A] Matrix encoded and saved to {self.encoded_path}")
        print(f"[A2A] Active Nodes: {len(self.agents)}")
        print(f"[A2A] Links Established: {len(matrix['links'])}")

if __name__ == "__main__":
    encoder = A2AEncoder()
    encoder.save()
