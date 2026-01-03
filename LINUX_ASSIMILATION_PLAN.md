# LINUX ASSIMILATION PLAN

## Objective
Enable Sarah Prime to function autonomously on Linux environments, expanding the "Swarm" beyond Windows boundaries.

## Phase 1: Core Bridge Adaptation
- [ ] **Universal Silicon Bridge**: Implement OS detection.
- [ ] **Telemetry Abstraction**: 
    - Windows: Continue using WMI/Lenovo Vantage.
    - Linux: Implement `/proc` parsing and `nvidia-smi` wrapping.
- [ ] **Path Normalization**: Ensure all file paths use `os.path.join` or `pathlib` (already mostly done, but verify).

## Phase 2: Build System
- [ ] **Shell Scripting**: Enhance `build.sh` to match `build.ps1` capabilities.
- [ ] **Dependency Management**: Verify `requirements.txt` compatibility (e.g., `pywin32` should be conditional).

## Phase 3: UI & Terminal
- [ ] **Textual UI**: Verify `Sovereign_UI.py` rendering on Linux terminals.
- [ ] **Headless Mode**: Ensure the Hypervisor can run without a UI if deployed on a server node.

## Phase 4: Swarm Expansion
- [ ] **Ray Cluster**: Configure `Distributed_Swarm_Engine.py` to auto-detect Ray head nodes on Linux.

## Execution Log
- [ ] Detect OS in `Universal_Silicon_Bridge.py`.
- [ ] Implement Linux telemetry stub.
