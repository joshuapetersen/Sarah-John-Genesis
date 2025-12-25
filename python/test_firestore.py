from firebase_client import health_check


def main() -> None:
    ok = health_check()
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
