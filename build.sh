#!/bin/bash
set -e

echo "🔨 Building Sovereign Network Mono-Repo..."

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found."
    exit 1
fi

# Check for CMake
if ! command -v cmake &> /dev/null; then
    echo "❌ CMake not found. Please install cmake."
    exit 1
fi

echo "🐍 Building pybind11 Bridge..."
cmake -S . -B build
cmake --build build --config Release

# Check for Rust installation
if ! command -v cargo &> /dev/null; then
    echo "⚠️ Cargo not found. Skipping Rust build."
else
    echo "📦 Building all workspace crates..."
    cargo build --release --workspace
fi

echo "✅ Build complete!"
echo ""
echo "To run the Hypervisor:"
echo "  python3 Sarah_Prime_Hypervisor.py"
echo "  or"
echo "  ./target/release/zhtp-orchestrator --config zhtp/configs/test-node1.toml"
