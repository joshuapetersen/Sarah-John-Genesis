import importlib
import os
import sys

class SarahCore:
    def __init__(self):
        self.plugins = {}
        self.commands = {}
        self.load_plugins()
        self.register_core_commands()

    def load_plugins(self, plugin_dir="plugins"):
        if not os.path.exists(plugin_dir):
            print(f"[SarahCore] Plugin directory '{plugin_dir}' not found.")
            return
        for fname in os.listdir(plugin_dir):
            if fname.endswith(".py") and not fname.startswith("__"):
                mod_name = fname[:-3]
                try:
                    mod = importlib.import_module(f"plugins.{mod_name}")
                    self.plugins[mod_name] = mod
                    if hasattr(mod, "register"):
                        mod.register(self)
                    print(f"[SarahCore] Loaded plugin: {mod_name}")
                except Exception as e:
                    print(f"[SarahCore] Failed to load plugin {mod_name}: {e}")

    def register_command(self, name, func):
        self.commands[name] = func
        print(f"[SarahCore] Registered command: {name}")

    def register_core_commands(self):
        self.register_command("selftest", self.self_test)
        self.register_command("list_plugins", self.list_plugins)
        self.register_command("help", self.help)

    def self_test(self):
        print("[SarahCore] Running core self-test...")
        print(f"Python: {sys.version}")
        print(f"Plugins loaded: {list(self.plugins.keys())}")
        print(f"Commands available: {list(self.commands.keys())}")
        print("[SarahCore] Self-test complete.")

    def list_plugins(self):
        print("[SarahCore] Plugins:")
        for name in self.plugins:
            print(f" - {name}")

    def help(self):
        print("[SarahCore] Available commands:")
        for name in self.commands:
            print(f" - {name}")

    def run(self):
        print("[SarahCore] Ready. Type a command:")
        while True:
            try:
                cmd = input("SarahCore> ").strip()
                if cmd in ("exit", "quit", "0"):
                    print("[SarahCore] Exiting.")
                    break
                if cmd in self.commands:
                    self.commands[cmd]()
                else:
                    print(f"[SarahCore] Unknown command: {cmd}")
            except KeyboardInterrupt:
                print("\n[SarahCore] Interrupted. Type 'exit' to quit.")
            except Exception as e:
                print(f"[SarahCore] Error: {e}")

if __name__ == "__main__":
    SarahCore().run()
