import sys

from .checker import check_repository


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else list(argv)
    if len(argv) != 1:
        print("Usage: github-checker <github-repo-url>", file=sys.stderr)
        return 1

    result = check_repository(argv[0])
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
