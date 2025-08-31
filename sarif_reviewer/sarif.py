from json import load
from typing import List, Optional

from sarif_pydantic import Sarif, Result

from sarif_reviewer.context_parser import ContextParser
from sarif_reviewer.logging import get_logger

logger = get_logger(__name__)


class ContextualResult(Result):
    code_snippets: Optional[List[str]] = None


class SarifParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.sarif_data = self.load_sarif()

    def load_sarif(self):
        try:
            with open(self.file_path, "r") as f:
                sarif_data = load(f)
            return Sarif.model_validate(sarif_data)
        except Exception as e:
            logger.error(f"Error loading SARIF file {self.file_path}: {e}", exc_info=True)
            raise ValueError(f"Invalid SARIF file: {self.file_path}") from e

    def get_contextual_results(self, language: str, encoding: str = "utf-8", base_dir: str = None):
        results = []
        # Access data via typed objects
        for run in self.sarif_data.runs:
            for result in run.results or []:
                contextual_result = ContextualResult.model_validate(result.model_dump())
                logger.debug(f"Rule: {result.rule_id}, Level: {result.level}")
                logger.debug(f"Message: {result.message.text}")
                
                if contextual_result.code_snippets is None:
                    contextual_result.code_snippets = []

                if result.locations:
                    for location in result.locations:
                        context_parser = ContextParser(language)
                        file_path = location.physical_location.artifact_location.uri
                        root_node = context_parser.parse(file_path, base_dir=base_dir)
                        starting_pt = (
                            location.physical_location.region.start_line,
                            location.physical_location.region.start_column,
                        )
                        # ending_pt = (
                        #     location.physical_location.region.end_line or location.physical_location.region.start_line,
                        #     location.physical_location.region.end_column,
                        # )
                        code_snippet = context_parser.get_contextual_code_for_point(
                            starting_point=starting_pt,
                            # ending_point=ending_pt,
                            encoding=encoding
                        )
                        logger.info(f"Extracted code snippet for {file_path}: {code_snippet}")

                        if code_snippet:
                            contextual_result.code_snippets.append(code_snippet)
                            results.append(contextual_result)
                            logger.debug(f"Code Snippet: {code_snippet}")
                        else:
                            logger.debug("No code snippet found.")

                        if root_node:
                            logger.debug(
                                f"Location: {location.physical_location.artifact_location.uri}"
                            )
                            logger.debug(
                                f"  Start Line: {location.physical_location.region.start_line}"
                            )
                            logger.debug(
                                f"  Start Column: {location.physical_location.region.start_column}"
                            )
                            logger.debug(
                                f"  End Line: {location.physical_location.region.end_line}"
                            )
                            logger.debug(
                                f"  End Column: {location.physical_location.region.end_column}"
                            )

                # if result.code_flows:
                #     for code_flow in result.code_flows:
                #         if code_flow.thread_flows:
                #             for thread_flow in code_flow.thread_flows:
                #                 for thread_flow_location in thread_flow.locations:
                #                     location = thread_flow_location.location
                #                     logger.debug(f"  Location: {location.physical_location.artifact_location.uri}")
                #                     logger.debug(f"    Start Line: {location.physical_location.region.start_line}")
                #                     logger.debug(f"    Start Column: {location.physical_location.region.start_column}")
                #                     logger.debug(f"    End Line: {location.physical_location.region.end_line}")
                #                     logger.debug(f"    End Column: {location.physical_location.region.end_column}")

        return results
