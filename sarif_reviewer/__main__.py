from argparse import ArgumentParser
from .sarif import SarifParser


if __name__ == "__main__":
    parser = ArgumentParser(description="SARIF Reviewer")
    parser.add_argument("-f", "--file", help="Path to the SARIF file to review", required=True)
    args = parser.parse_args()
    
    sarif_parser = SarifParser(args.file)
    sarif_parser.get_contextual_results()

