"""Tools for scale validation analysis"""

from langchain.pydantic_v1 import BaseModel
from langchain_core.tools import BaseTool
from pydantic.v1 import Field
from typing import List, Optional

from paper_parser import PaperParser
from scale_validation_models import ScaleValidationCriteria, ScaleValidationReport, ScaleConfig


class ReportScaleValidationArgs(BaseModel):
    """Arguments for the scale validation reporting tool."""
    scale_name: str = Field(description="The name of the scale found (e.g., 'NASA-TLX')")
    scale_found: bool = Field(description="Whether the scale was found in the paper")
    
    # The 22 validation criteria
    scale_adhoc: str = Field(description="Check if the measure is an ad hoc scale (yes/no/not_reported)")
    adhoc_evidence_reliability: str = Field(description="If ad hoc, discuss impact on reliability (yes/no/N/A)")
    adhoc_evidence_construct_con: str = Field(description="If ad hoc, convergent validity from independent data (yes/no/N/A)")
    adhoc_evidence_construct_dis: str = Field(description="If ad hoc, discriminant validity from independent data (yes/no/N/A)")
    adhoc_evidence_redundancy: str = Field(description="If ad hoc, arguments for non-redundancy (yes/no/N/A)")
    
    consistent_names: str = Field(description="Consistent construct name usage (yes/no)")
    construct_uniqueness: str = Field(description="Clarify how construct differs from related constructs (yes/no)")
    all_items: str = Field(description="All items reported in manuscript or supplements (yes/no)")
    scale_sources: str = Field(description="Exact source(s) of the measure provided (yes/no)")
    
    n_exclusion: str = Field(description="Eligibility criteria for inclusion/exclusion (justified/non-justified/N/A)")
    n_size: str = Field(description="Justify sample size in relation to study goals (yes/no)")
    
    analysis_details: str = Field(description="Detail analytical approaches (yes/no/complete)")
    analysis_robustness: str = Field(description="Multiple measures or analytical approaches for robustness (yes/no)")
    
    objectivity_evidence: str = Field(description="Information on objectivity of measurement (yes/no)")
    reliability_evidence: str = Field(description="Document reliability using appropriate metrics (yes/no)")
    validity_evidence: str = Field(description="Report all available validity evidence (yes/no)")
    validity_justification: str = Field(description="Justify fit and operationalisation of validity types (yes/no/none)")
    validity_construct: str = Field(description="Document convergent and discriminant validity (convergent/discriminant/complete/none)")
    
    registered_study: str = Field(description="Study preregistered on public repository (yes/no)")
    registered_measures: str = Field(description="Measure was preregistered (yes/no)")
    registered_scoring: str = Field(description="Scoring procedure was preregistered (yes/no)")
    
    scale_descriptives: str = Field(description="Descriptive statistics for scale reported (yes/no)")
    
    additional_notes: str = Field(default="", description="Additional observations about the scale usage")
    extraction_confidence: str = Field(description="Confidence in extraction (high/medium/low)")


class ReportScaleValidationTool(BaseTool):
    """Tool to report scale validation analysis."""

    name: str = "report_scale_validation"
    description: str = (
        """Reports the scale validation analysis for the target scale. Use this tool once you have analyzed 
        the paper for the target scale and evaluated it against all 22 validation criteria. 
        If you don't have a value for a field, submit 'UNKNOWN' as the value."""
    )

    args_schema: type[BaseModel] = ReportScaleValidationArgs
    scale_reports: List[dict] = []
    scale_config: Optional[ScaleConfig] = None

    def _run(
            self,
            scale_name: str,
            scale_found: bool,
            scale_adhoc: str,
            adhoc_evidence_reliability: str,
            adhoc_evidence_construct_con: str,
            adhoc_evidence_construct_dis: str,
            adhoc_evidence_redundancy: str,
            consistent_names: str,
            construct_uniqueness: str,
            all_items: str,
            scale_sources: str,
            n_exclusion: str,
            n_size: str,
            analysis_details: str,
            analysis_robustness: str,
            objectivity_evidence: str,
            reliability_evidence: str,
            validity_evidence: str,
            validity_justification: str,
            validity_construct: str,
            registered_study: str,
            registered_measures: str,
            registered_scoring: str,
            scale_descriptives: str,
            additional_notes: str = "",
            extraction_confidence: str = "medium"
    ) -> str:
        
        validation_criteria = ScaleValidationCriteria(
            scale_adhoc=scale_adhoc,
            adhoc_evidence_reliability=adhoc_evidence_reliability,
            adhoc_evidence_construct_con=adhoc_evidence_construct_con,
            adhoc_evidence_construct_dis=adhoc_evidence_construct_dis,
            adhoc_evidence_redundancy=adhoc_evidence_redundancy,
            consistent_names=consistent_names,
            construct_uniqueness=construct_uniqueness,
            all_items=all_items,
            scale_sources=scale_sources,
            n_exclusion=n_exclusion,
            n_size=n_size,
            analysis_details=analysis_details,
            analysis_robustness=analysis_robustness,
            objectivity_evidence=objectivity_evidence,
            reliability_evidence=reliability_evidence,
            validity_evidence=validity_evidence,
            validity_justification=validity_justification,
            validity_construct=validity_construct,
            registered_study=registered_study,
            registered_measures=registered_measures,
            registered_scoring=registered_scoring,
            scale_descriptives=scale_descriptives
        )
        
        report = ScaleValidationReport(
            scale_name=scale_name,
            scale_found=scale_found,
            scale_config_used=self.scale_config.scale_name,
            validation_criteria=validation_criteria,
            additional_notes=additional_notes,
            extraction_confidence=extraction_confidence
        )
        
        self.scale_reports.append(report.dict())
        return f"Scale validation report for {scale_name} submitted successfully"


class SectionReadTool(BaseTool):
    """Tool to read a section or sub section from a paper."""

    class Args(BaseModel):
        """Arguments for the SectionReadTool."""
        index: str = Field(description="The index of the section or subsection you want to read.")

    name: str = "read_section"
    description: str = """Provides the text of a section or subsection of a paper.
Use the FULL section title from the section index provided (e.g., '4.1 Procedure', 'A Questionnaires & Scales').
Do NOT use just the number (e.g., '4.1') - use the complete title."""
    args_schema: type[BaseModel] = Args

    paperparser: PaperParser

    def _run(self, index: str) -> str:
        """Internal run method"""
        try:
            return self.paperparser.get_section_text_by_index(index)
        except ValueError as e:
            print(f"Could not find section by index '{index}': {e}")
        
        try:
            return self.paperparser.get_section_text_by_title(index)
        except ValueError as e:
            print(f"Could not find section by title '{index}': {e}")

        return "Could not find section."


class TableReadTool(BaseTool):
    """Tool to read a Table from a paper."""

    class Args(BaseModel):
        """Arguments for the TableReadTool."""
        index: str = Field(description="The index of the table you want to read.")

    name: str = "read_table"
    description: str = """Provides the csv code for a table from a research paper.
Specify which table by using the index argument."""
    args_schema: type[BaseModel] = Args

    paperparser: PaperParser

    def _run(self, index: str):
        """Internal run method"""
        try:
            table_title, csv_code = self.paperparser.get_table_by_index(index)
            table_prompt = f"""You are analyzing this table for scale validation information. 
                           Look for information about the target scale including:
                           - Scale items or subscales
                           - Reliability coefficients (Cronbach's alpha, etc.)
                           - Descriptive statistics (means, standard deviations)
                           - Validity evidence
                           - Any modifications to the original scale
                           
                           The title of the table is: {table_title}"""
            message = table_prompt + "\nAnd here is the table as CSV: \n" + csv_code
            return message
        except ValueError as e:
            print(e)

        return "Could not find table."
