"""Batch Scale Validation Analysis with Enhanced Logging and Reporting"""
import json
import os
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

from langgraph.errors import GraphRecursionError
from minimal_CCS_extraction import get_header
from scale_validation_agent import ScaleValidationAgent
from scale_validation_agent import ScaleValidationAgentContext
from scale_validation_models import SCALE_CONFIGS


class BatchScaleValidationAnalyzer:
    """Batch analyzer for scale validation with comprehensive logging and reporting"""
    
    def __init__(self, html_folder_path: str, papers: List[str], target_scale: str, 
                 results_folder: Path = None, log_folder: Path = None):
        self.html_folder_path = Path(html_folder_path)
        self.papers = papers
        self.target_scale = target_scale
        self.scale_config = SCALE_CONFIGS[target_scale]
        self.results_folder = results_folder or Path(__file__).parent.parent / 'results'
        self.log_folder = log_folder or Path(__file__).parent.parent / 'batch_logs'
        
        # Create folders if they don't exist
        self.results_folder.mkdir(parents=True, exist_ok=True)
        self.log_folder.mkdir(parents=True, exist_ok=True)
        
        # Initialize logging
        self.batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_folder / f"batch_scale_validation_{self.batch_id}.log"
        self.summary_file = self.log_folder / f"batch_summary_{self.batch_id}.json"
        self.csv_report = self.log_folder / f"validation_report_{self.batch_id}.csv"
        
        self.results = []
        self.errors = []
        self.skipped = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log message to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
    
    def analyze_single_paper(self, paper: str) -> Dict[str, Any]:
        """Analyze a single paper and return results"""
        html_path = self.html_folder_path / paper
        result_file = self.results_folder / f"{paper[:-5]}_scale_validation.json"
        
        if result_file.exists():
            self.log(f"Results already exist for {paper}, skipping...")
            self.skipped.append(paper)
            return {"status": "skipped", "paper": paper}
        
        if not html_path.exists():
            self.log(f"HTML file not found: {html_path}", "ERROR")
            self.errors.append({"paper": paper, "error": "HTML file not found"})
            return {"status": "error", "paper": paper, "error": "HTML file not found"}
        
        try:
            self.log(f"Starting analysis for {paper}")
            
            # Run the scale validation agent
            context = ScaleValidationAgentContext(
                paperPath=html_path,
                result=[],
                result_path=self.results_folder / f"{paper[:-5]}_scale_validation.md"
            )
            agent = ScaleValidationAgent()
            context = agent.run(context)
            
            # Get paper metadata
            ccs_header = get_header(html_path)
            
            # Combine results
            full_result = {**ccs_header, "scale_validation": context.result}
            
            # Save results
            with open(result_file, 'w', encoding="utf-8") as json_file:
                json.dump(full_result, json_file, indent=4)
            
            self.log(f"Successfully analyzed {paper}")
            
            # Extract validation results for summary
            if context.result and len(context.result) > 0:
                validation_data = context.result[0]
                return {
                    "status": "success",
                    "paper": paper,
                    "scale_found": validation_data.get("scale_found", False),
                    "validation_criteria": validation_data.get("validation_criteria", {}),
                    "extraction_confidence": validation_data.get("extraction_confidence", "unknown")
                }
            else:
                return {"status": "success", "paper": paper, "scale_found": False}
                
        except GraphRecursionError as e:
            error_msg = f"Graph recursion error for {paper}: {str(e)}"
            self.log(error_msg, "ERROR")
            self.errors.append({"paper": paper, "error": str(e)})
            return {"status": "error", "paper": paper, "error": str(e)}
        
        except Exception as e:
            error_msg = f"Unexpected error for {paper}: {str(e)}"
            self.log(error_msg, "ERROR")
            self.errors.append({"paper": paper, "error": str(e)})
            return {"status": "error", "paper": paper, "error": str(e)}
    
    def run_batch_analysis(self):
        """Run batch analysis on all papers"""
        self.log(f"Starting batch scale validation analysis")
        self.log(f"Target scale: {self.target_scale} ({self.scale_config.scale_name})")
        self.log(f"Papers to analyze: {len(self.papers)}")
        self.log(f"Results folder: {self.results_folder}")
        
        start_time = datetime.now()
        
        for i, paper in enumerate(self.papers, 1):
            self.log(f"Processing paper {i}/{len(self.papers)}: {paper}")
            result = self.analyze_single_paper(paper)
            self.results.append(result)
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        self.log(f"Batch analysis completed in {duration}")
        self.generate_summary()
        self.generate_csv_report()
    
    def generate_summary(self):
        """Generate batch analysis summary"""
        successful = [r for r in self.results if r["status"] == "success"]
        scales_found = [r for r in successful if r.get("scale_found", False)]
        
        summary = {
            "batch_id": self.batch_id,
            "target_scale": self.target_scale,
            "scale_config": self.scale_config.dict(),
            "analysis_timestamp": datetime.now().isoformat(),
            "total_papers": len(self.papers),
            "successful_analyses": len(successful),
            "papers_with_scale": len(scales_found),
            "skipped_papers": len(self.skipped),
            "errors": len(self.errors),
            "success_rate": len(successful) / len(self.papers) * 100 if self.papers else 0,
            "scale_detection_rate": len(scales_found) / len(successful) * 100 if successful else 0,
            "detailed_results": self.results,
            "error_details": self.errors
        }
        
        with open(self.summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=4)
        
        self.log(f"Summary saved to: {self.summary_file}")
        self.log(f"Success rate: {summary['success_rate']:.1f}%")
        self.log(f"Scale detection rate: {summary['scale_detection_rate']:.1f}%")
    
    def generate_csv_report(self):
        """Generate CSV report with validation criteria results"""
        if not self.results:
            return
        
        # Get all validation criteria from the first successful result
        criteria_fields = []
        for result in self.results:
            if result["status"] == "success" and result.get("validation_criteria"):
                criteria_fields = list(result["validation_criteria"].keys())
                break
        
        # Create CSV with all results
        with open(self.csv_report, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['paper', 'status', 'scale_found', 'extraction_confidence'] + criteria_fields
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in self.results:
                row = {
                    'paper': result['paper'],
                    'status': result['status'],
                    'scale_found': result.get('scale_found', ''),
                    'extraction_confidence': result.get('extraction_confidence', '')
                }
                
                # Add validation criteria
                if result.get('validation_criteria'):
                    row.update(result['validation_criteria'])
                
                writer.writerow(row)
        
        self.log(f"CSV report saved to: {self.csv_report}")


def main():
    """Main function for batch analysis"""
    from settings import html_folder_path, papers, TARGET_SCALE
    
    # Set up API key
    api_key_file = Path(__file__).parent.parent / "OPENAI_API_KEY"
    if api_key_file.exists():
        with open(api_key_file, 'r') as file:
            OPENAI_API_KEY = file.read().strip()
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    
    # Initialize batch analyzer
    analyzer = BatchScaleValidationAnalyzer(
        html_folder_path=html_folder_path,
        papers=papers,
        target_scale=TARGET_SCALE
    )
    
    # Run batch analysis
    analyzer.run_batch_analysis()
    
    print(f"\nBatch analysis complete!")
    print(f"Log file: {analyzer.log_file}")
    print(f"Summary: {analyzer.summary_file}")
    print(f"CSV report: {analyzer.csv_report}")


if __name__ == "__main__":
    main()
