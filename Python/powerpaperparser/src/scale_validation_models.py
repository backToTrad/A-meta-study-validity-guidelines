"""Data models for scale validation analysis based on scales_coding.tex"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ScaleValidationCriteria(BaseModel):
    """The 22 validation criteria from scales_coding.tex"""
    
    # Justification and Consequences of Scale Selection and Modification
    scale_adhoc: str = Field(description="Check if the measure is an ad hoc scale (yes/no/not_reported)")
    adhoc_evidence_reliability: str = Field(description="If ad hoc, discuss impact on reliability (yes/no)")
    adhoc_evidence_construct_con: str = Field(description="If ad hoc, convergent validity from independent data (yes/no)")
    adhoc_evidence_construct_dis: str = Field(description="If ad hoc, discriminant validity from independent data (yes/no)")
    adhoc_evidence_redundancy: str = Field(description="If ad hoc, arguments for non-redundancy (yes/no)")
    
    # Reporting of Measurement Details
    consistent_names: str = Field(description="Consistent construct name usage (yes/no)")
    construct_uniqueness: str = Field(description="Clarify how construct differs from related constructs (yes/no)")
    all_items: str = Field(description="All items reported in manuscript or supplements (yes/no)")
    scale_sources: str = Field(description="Exact source(s) of the measure provided (yes/no)")
    
    # Sample Description and Justification
    n_exclusion: str = Field(description="Eligibility criteria for inclusion/exclusion (justified/non-justified/N/A)")
    n_size: str = Field(description="Justify sample size in relation to study goals (yes/no)")
    
    # Documentation of Procedure and Analysis
    analysis_details: str = Field(description="Detail analytical approaches (yes/no/complete)")
    analysis_robustness: str = Field(description="Multiple measures or analytical approaches for robustness (yes/no)")
    
    # Objectivity, Reliability, and Validity
    objectivity_evidence: str = Field(description="Information on objectivity of measurement (yes/no)")
    reliability_evidence: str = Field(description="Document reliability using appropriate metrics (yes/no)")
    validity_evidence: str = Field(description="Report all available validity evidence (yes/no)")
    validity_justification: str = Field(description="Justify fit and operationalisation of validity types (yes/no/none)")
    validity_construct: str = Field(description="Document convergent and discriminant validity (convergent/discriminant/complete/none)")
    
    # Registration and Transparency
    registered_study: str = Field(description="Study preregistered on public repository (yes/no)")
    registered_measures: str = Field(description="Measure was preregistered (yes/no)")
    registered_scoring: str = Field(description="Scoring procedure was preregistered (yes/no)")
    
    # Comprehensive Reporting of Results
    scale_descriptives: str = Field(description="Descriptive statistics for scale reported (yes/no)")


class ScaleConfig(BaseModel):
    """Configuration for different psychometric scales"""
    scale_name: str
    scale_aliases: List[str]
    expected_subscales: Optional[List[str]]
    original_source: str
    scale_description: str
    common_modifications: List[str]
    typical_response_format: str
    

class ScaleValidationReport(BaseModel):
    """Complete validation report for a scale"""
    scale_name: str
    scale_found: bool
    scale_config_used: str
    validation_criteria: ScaleValidationCriteria
    additional_notes: str = ""
    extraction_confidence: str = Field(description="high/medium/low confidence in extraction")


# Scale configurations
SCALE_CONFIGS = {
    "nasa_tlx": ScaleConfig(
        scale_name="NASA-TLX",
        scale_aliases=["NASA TLX", "Task Load Index", "TLX", "NASA Task Load Index"],
        expected_subscales=["Mental Demand", "Physical Demand", "Temporal Demand", "Performance", "Effort", "Frustration"],
        original_source="Hart & Staveland (1988)",
        scale_description="Subjective workload assessment tool with 6 subscales",
        common_modifications=["item removal", "response scale changes", "translation", "weighting procedure changes"],
        typical_response_format="21-point scale or 7-point Likert scale"
    ),
    "sus": ScaleConfig(
        scale_name="System Usability Scale",
        scale_aliases=["SUS"],
        expected_subscales=[],
        original_source="Brooke (1996)",
        scale_description="10-item usability questionnaire",
        common_modifications=["item rewording", "response scale changes", "translation"],
        typical_response_format="5-point Likert scale"
    ),
    "tam": ScaleConfig(
        scale_name="Technology Acceptance Model",
        scale_aliases=["TAM", "Technology Acceptance Model questionnaire"],
        expected_subscales=["Perceived Usefulness", "Perceived Ease of Use", "Behavioral Intention"],
        original_source="Davis (1989)",
        scale_description="Model for predicting technology acceptance",
        common_modifications=["item adaptation", "additional constructs", "response scale changes"],
        typical_response_format="7-point Likert scale"
    )
}
