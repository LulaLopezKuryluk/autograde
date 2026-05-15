import sys

from .checker import check_repository


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else list(argv)
    
    # Parse arguments
    run_tests = False
    url = None
    
    for arg in argv:
        if arg in ("--run-tests", "-t"):
            run_tests = True
        elif not arg.startswith("-"):
            url = arg
    
    if not url:
        print("Usage: github-checker [--run-tests] <github-repo-url>", file=sys.stderr)
        return 1

    result = check_repository(url, run_tests=run_tests)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
