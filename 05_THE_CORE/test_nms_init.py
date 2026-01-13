
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add core dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from Neural_Memory_Core import NeuralMemory
    nms = NeuralMemory()
    if nms.client:
        print("Neural Memory initialized with API Key.")
    else:
        print("Neural Memory initialized WITHOUT API Key (Amnesiac Mode).")
except Exception as e:
    print(f"Error initializing Neural Memory: {e}")
