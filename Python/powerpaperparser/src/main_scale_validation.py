"""Main file for Scale Validation Analysis"""
import json
import os
from pathlib import Path

from langgraph.errors import GraphRecursionError
from minimal_CCS_extraction import get_header
from scale_validation_agent import ScaleValidationAgent
from scale_validation_agent import ScaleValidationAgentContext


def start_scale_validation_agent(path: Path, result_path: Path) -> list:
    """Function to run the scale validation agent"""
    context = ScaleValidationAgentContext(
        paperPath=path,
        result=[],
        result_path=result_path
    )
    agent = ScaleValidationAgent()

    try:
        context = agent.run(context)

    except GraphRecursionError as e:
        print(f"{e}")

    return context.result


def run_scale_validation_agent(html_path: Path, results_folder=Path(__file__).parent.parent / 'results'):
    """The run function for scale validation analysis!"""
    # Extract the name of the HTML file
    html_filename = html_path.name
    # Create the results folder if it doesn't exist
    results_folder.mkdir(parents=True, exist_ok=True)
    # Define the path to the results files
    result_json_path = results_folder / f"{html_filename[:-5]}_scale_validation.json"
    result_md_path = results_folder / f"{html_filename[:-5]}_scale_validation.md"

    # acquire scale validation results
    result = start_scale_validation_agent(html_path, result_md_path)
    # get header and ccs
    ccs_header = get_header(html_path)
    # merge the two
    ccs_header.update({"scale_validation": result})
    # dump the result into a json file
    with open(result_json_path, 'w', encoding="utf-8") as json_file:
        json.dump(ccs_header, json_file, indent=4)


if __name__ == "__main__":
    from settings import *

    api_key_file = Path(__file__).parent.parent / "OPENAI_API_KEY"
    if api_key_file.exists():
        with open(Path(__file__).parent.parent / "OPENAI_API_KEY", 'r') as file:
            OPENAI_API_KEY = file.read()
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    for paper in papers:
        result_file = Path(__file__).parent.parent / "results" / (paper[:-5] + "_scale_validation.json")
        if result_file.exists():
            print(f"Scale validation results already exist for {paper}, skipping...")
            continue
        print("Starting Scale Validation Agent for Paper:", paper)
        run_scale_validation_agent(Path(html_folder_path + "/" + paper))
