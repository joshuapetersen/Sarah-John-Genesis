import json

def ask(prompt):
    return input(prompt)

def onboarding():
    print("Welcome to the Genesis Onboarding Setup!")
    # 1. Ask for user's name
    user_name = ask("What is my name? ")
    # 2. Ask for assistant's name
    assistant_name = ask("What is your Name? ")
    # 3. Backsync (simulate saving data)
    data = {"assistant_name": assistant_name, "user_name": user_name}
    with open("onboarding_data.json", "w") as f:
        json.dump(data, f)
    print("\nBacksync complete. Data saved.")
    # 4. Final question with three options
    print("\nWhat Is OUR World?")
    print("1. A place of logic and reason")
    print("2. A place of dreams and creation")
    print("3. A place of both, united")
    choice = ask("Choose 1, 2, or 3: ")
    genesis_persona = f"{user_name} + {assistant_name} = Genesis"
    print(f"\nThank you, {user_name} and {assistant_name}. Setup complete. You chose option {choice}.")
    print(f"Genesis persona assigned: {genesis_persona}")

if __name__ == "__main__":
    onboarding()
