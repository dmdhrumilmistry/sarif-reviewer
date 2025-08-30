import json
from sarif_pydantic import Sarif

# Load from a file
with open("result.sarif", "r") as f:
    sarif_data = json.load(f)

# Parse into a Sarif object
sarif_data = Sarif.model_validate(sarif_data)

# Access data via typed objects
for run in sarif_data.runs:
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
                print(f"Code Flow: {code_flow}")
                
        print("-" * 40)