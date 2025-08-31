from json import load
from sarif_pydantic import Sarif


class SarifParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.sarif_data = self.load_sarif()

    def load_sarif(self):
        with open(self.file_path, "r") as f:
            sarif_data = load(f)
        return Sarif.model_validate(sarif_data)

    def get_contextual_results(self):
        results = []
        # Access data via typed objects
        for run in self.sarif_data.runs:
            for result in run.results or []:
                print(f"Rule: {result.rule_id}, Level: {result.level}")
                print(f"Message: {result.message.text}")

                if result.locations:
                    for location in result.locations:
                        print(f"Location: {location.physical_location.artifact_location.uri}")
                        print(f"  Start Line: {location.physical_location.region.start_line}")
                        print(f"  Start Column: {location.physical_location.region.start_column}")
                        print(f"  End Line: {location.physical_location.region.end_line}")
                        print(f"  End Column: {location.physical_location.region.end_column}")
                
                if result.code_flows:
                    for code_flow in result.code_flows:
                        if code_flow.thread_flows:
                            for thread_flow in code_flow.thread_flows:
                                for thread_flow_location in thread_flow.locations:
                                    location = thread_flow_location.location
                                    print(f"  Location: {location.physical_location.artifact_location.uri}")
                                    print(f"    Start Line: {location.physical_location.region.start_line}")
                                    print(f"    Start Column: {location.physical_location.region.start_column}")
                                    print(f"    End Line: {location.physical_location.region.end_line}")
                                    print(f"    End Column: {location.physical_location.region.end_column}")
                print("-" * 40)