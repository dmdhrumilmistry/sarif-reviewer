from argparse import ArgumentParser
from os import getcwd, environ

from sarif_reviewer.analyzer import AIAnalyzer
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
    parser.add_argument("-m", "--model", dest="model", help="AI model to use", default="gpt-5")
    parser.add_argument("-u", "--ai-base-url", dest="ai_base_url", help="AI base URL. For OLLAMA hosted locally use: http://localhost:11434/v1", default="https://api.openai.com/v1")
    args = parser.parse_args()

    default_config.logging_level = args.level
    default_config.language = args.language
    default_config.encoding = args.encoding
    default_config.base_dir = args.base_dir

    default_config.ai_api_key = environ.get("OPENAI_API_KEY")
    default_config.ai_base_url = args.ai_base_url

    sarif_parser = SarifParser(args.file)
    contextual_results: list[ContextualResult] = sarif_parser.get_contextual_results(
        language=default_config.language, encoding=default_config.encoding, base_dir=default_config.base_dir
    )
    print(f"Found {len(contextual_results)} results with context.")

    # analyze code using AI
    analyzer = AIAnalyzer(
        base_url=default_config.ai_base_url,
        api_key=default_config.ai_api_key
    )
    for result in contextual_results:
        prompt = analyzer.create_prompt(result)
        print(prompt)
        print("Analyzing Result using AI...")
        response = analyzer.analyze(prompt, stream=True)
        print(response)
        print("-" * 80)
