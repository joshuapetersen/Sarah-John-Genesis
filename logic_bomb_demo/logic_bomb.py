import getpass
import sys

# Define the three required vocal architect override passphrases
REQUIRED_OVERRIDES = [
    "alpha-override-2026",
    "bravo-override-2026",
    "charlie-override-2026"
]


def main():
    print("[LOGIC BOMB] Secure environment initialized.")
    for idx, override in enumerate(REQUIRED_OVERRIDES, 1):
        user_input = getpass.getpass(f"Enter vocal architect override {idx}: ")
        if user_input != override:
            print("[LOGIC BOMB] Override sequence failed. System inert.")
            sys.exit(1)
    # Payload: Only executes if all overrides are correct
    print("[LOGIC BOMB] All overrides accepted. Payload activated.")
    # --- PAYLOAD START ---
    # (Demo: print message. Replace with real logic if needed.)
    print("*** LOGIC BOMB DETONATED: SYSTEM BREACH AUTHORIZED ***")
    # --- PAYLOAD END ---

if __name__ == "__main__":
    main()
