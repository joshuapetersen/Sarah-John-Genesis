"""
Utility CLI for Sarah Core:
- Mint HS256 JWTs for testing
- Verify the hash chain of the audit log

Usage:
  python tools/jwt_audit_cli.py mint --sub tester --scope read --secret secret --alg HS256 --aud myaud --iss myiss
  python tools/jwt_audit_cli.py verify --path integrity_logs/audit_log.jsonl
"""
import argparse
import json
import os
import sys
import hashlib
from pathlib import Path
from typing import List

import jwt  # type: ignore


def mint(args):
    payload = {"sub": args.sub, "scope": " ".join(args.scope)}
    if args.aud:
        payload["aud"] = args.aud
    if args.iss:
        payload["iss"] = args.iss
    token = jwt.encode(payload, args.secret, algorithm=args.alg)
    print(token)


def verify(args):
    path = Path(args.path)
    if not path.exists():
        print(f"No audit log found at {path}")
        return 1
    prev = "0" * 64
    ok = True
    with path.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                print(f"Line {idx}: invalid JSON")
                ok = False
                continue
            expected = obj.get("prev_hash", "")
            if expected != prev:
                print(f"Line {idx}: prev_hash mismatch (expected {prev}, got {expected})")
                ok = False
            # recompute hash
            clone = obj.copy()
            clone.pop("hash", None)
            prev_hash = clone.pop("prev_hash", "")
            entry_bytes = json.dumps(clone, sort_keys=True).encode("utf-8")
            computed = hashlib.sha256(prev_hash.encode("utf-8") + entry_bytes).hexdigest()
            if computed != obj.get("hash"):
                print(f"Line {idx}: hash mismatch")
                ok = False
            prev = obj.get("hash", "")
    if ok:
        print("Audit log integrity OK")
    return 0 if ok else 2


def main(argv: List[str]):
    parser = argparse.ArgumentParser(description="Sarah Core JWT/Audit CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_mint = sub.add_parser("mint", help="Mint a JWT")
    p_mint.add_argument("--sub", required=True)
    p_mint.add_argument("--scope", nargs="+", default=["read"], help="Scopes separated by space")
    p_mint.add_argument("--secret", default=os.getenv("SARAH_JWT_SECRET", "supersecret"))
    p_mint.add_argument("--alg", default="HS256")
    p_mint.add_argument("--aud")
    p_mint.add_argument("--iss")
    p_mint.set_defaults(func=mint)

    p_verify = sub.add_parser("verify", help="Verify audit log hash chain")
    p_verify.add_argument("--path", default=os.getenv("SARAH_AUDIT_LOG", "integrity_logs/audit_log.jsonl"))
    p_verify.set_defaults(func=verify)

    args = parser.parse_args(argv)
    return args.func(args) or 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
