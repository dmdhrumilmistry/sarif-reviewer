from argparse import ArgumentParser
from os import getcwd

from sarif_reviewer.sarif import SarifParser, ContextualResult
from sarif_reviewer.config import default_config


if __name__ == "__main__":
    parser = ArgumentParser(description="SARIF Reviewer")
    parser.add_argument(
        "-f", "--file", dest="file", help="Path to the SARIF file to review", required=True
    )
    parser.add_argument(
        "-l", "--level", dest="level", help="Logging level", choices=["DEBUG", "INFO", "ERROR", "CRITICAL"], default="INFO"
    )
    parser.add_argument(
        "-lang", "--language", dest="language", help="Programming language for context parsing", required=True,
    )
    parser.add_argument(
        "-e", "--encoding", dest="encoding", help="File encoding", default="utf-8"
    )
    parser.add_argument("-b", "--base-dir", dest="base_dir", help="Base directory of source code", default=getcwd())
    args = parser.parse_args()

    default_config.logging_level = args.level
    default_config.language = args.language
    default_config.encoding = args.encoding
    default_config.base_dir = args.base_dir

    sarif_parser = SarifParser(args.file)
    contextual_results: list[ContextualResult] = sarif_parser.get_contextual_results(
        language=default_config.language, encoding=default_config.encoding, base_dir=default_config.base_dir
    )
    print(f"Found {len(contextual_results)} results with context.")

    # for result in contextual_results:
    #     print(f" - Rule: {result.rule_id}, Level: {result.level}")
    #     print(f"   Message: {result.message.text}")
    #     if result.code_snippet:
    #         print(f"   Code Snippet: {result.code_snippet}")
