"""Command-line interface for autograde."""

import argparse
import json
from autograde.validator import RepositoryValidator


def main():
    """Main entry point for the CLI tool."""
    parser = argparse.ArgumentParser(
        description="Validate GitHub repositories against specified conditions"
    )
    parser.add_argument(
        "repo_url",
        help="Valid repository URL to validate"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    validator = RepositoryValidator(args.repo_url)
    results = validator.validate()

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_results(results)

    # Return exit code based on validation
    return 0 if results["all_conditions_met"] else 1


def print_results(results: dict):
    """Pretty print the validation results."""
    print(f"\nValidation Results for: {results['url']}")
    print("=" * 60)
    print(f"Is Git Repository:        {results['is_git_repository']}")
    print(f"Has Main Branch:          {results['has_main_branch']}")
    print(f"Has Feature Branch:       {results['has_feature_branch']}")
    print(f"Has file.txt on Main:     {results['has_file_txt_on_main']}")
    print("=" * 60)
    print(f"All Conditions Met:       {results['all_conditions_met']}")
    
    if results['errors']:
        print("\nErrors:")
        for error in results['errors']:
            print(f"  - {error}")


if __name__ == "__main__":
    exit(main())
