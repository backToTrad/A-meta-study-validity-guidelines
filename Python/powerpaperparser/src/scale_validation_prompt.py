"""Prompts for scale validation analysis"""

from scale_validation_models import ScaleConfig


def get_scale_validation_persona() -> str:
    """Personal role of the agent for scale validation"""
    return """
You are a psychometric expert specializing in scale validation and measurement quality assessment. 
Your expertise includes evaluating how researchers report the use of psychometric scales in empirical studies, 
particularly focusing on validity, reliability, and adherence to best practices in scale usage and reporting.

"""


def get_system_prompt() -> str:
    """Get the system prompt for scale validation analysis"""
    return f"""
{get_scale_validation_persona()}
Carefully heed the user's instructions.
Respond using Markdown.
Follow the detailed coding instructions provided for each validation criterion.
    """


def get_scale_validation_task(scale_config: ScaleConfig, title: str, abstract: str, section_index: str, table_index: str) -> str:
    """Get the task description for scale validation analysis"""
    
    scale_aliases_text = ", ".join(scale_config.scale_aliases)
    subscales_text = ", ".join(scale_config.expected_subscales) if scale_config.expected_subscales else "No specific subscales"
    
    return f"""
You need to analyze this paper for the use of {scale_config.scale_name} and evaluate how well the authors 
reported its usage according to 22 validation criteria from psychometric best practices.

## Target Scale Information:
- **Scale Name**: {scale_config.scale_name}
- **Also known as**: {scale_aliases_text}
- **Original Source**: {scale_config.original_source}
- **Description**: {scale_config.scale_description}
- **Expected Subscales**: {subscales_text}
- **Typical Response Format**: {scale_config.typical_response_format}
- **Common Modifications**: {', '.join(scale_config.common_modifications)}

## Your Task:
1. **First, determine if {scale_config.scale_name} is used in this paper**
   - Look for any mention of the scale name or its aliases
   - Check if the construct being measured matches the scale's purpose
   - Note any variations in naming or terminology

2. **If the scale is found, evaluate it against these 22 validation criteria:**

### Justification and Consequences of Scale Selection and Modification:

**scale_adhoc**: Check if the measure is an ad hoc scale. Ad hoc scales are defined by adding completely new items, merging items, leaving out items of the original measure, changing the wording of items, translating the items, or changing how to score items. Ad hoc scales are also defined by changing the response format that is provided to participants. In case that there is no information on this topic, this will be coded as not reported.

Check whether the reported items match 1:1 the original items of the measure cited as the source. Also, check the match of the response format.

Report it as "yes", "no" or "not reported".

**adhoc_evidence_reliability**: If the scale is an ad hoc scale as defined above, check whether the authors discuss the impact of these changes on the reliability of the scale. This can include reporting results with keywords such as "alpha", "omega", "composite", "test–retest", or "split–half" reliability.

Report it as "yes" or "no".

**adhoc_evidence_construct_con**: If the scale is an ad hoc scale as defined above, check whether convergent validity is reported from independent data (i.e., a dataset separate from the main study). This refers to evidence that the scale captures the intended construct and relates appropriately to conceptually similar constructs. Look for theoretical arguments and not arbitrary comparisons. If the evidence is reported to come from another source, verify that the scale was indeed validated there.

Report it as "yes" or "no".

**adhoc_evidence_construct_dis**: If the scale is an ad hoc scale as defined above, check whether discriminant validity is reported from independent data (i.e., a dataset separate from the main study). This refers to evidence that the scale does not overlap with (fairly) unrelated constructs. Look for theoretical arguments and not arbitrary comparisons. If the evidence is reported to come from another source, verify that the scale was indeed validated there.

Report it as "yes" or "no".

**adhoc_evidence_redundancy**: If the scale is an ad hoc scale as defined above, check whether the authors provide arguments for the non-redundancy of the new scale compared to other published measures. Arguments on the meaningfulness or irrelevance of the changes may be theoretical or empirical. Empirical evidence should come from an independent sample (not the main study) and may include convergent or discriminant validity or incremental validity. Correlations with conceptually similar measures are relevant. Incremental validity is supported if the new scale predicts related outcomes over and above an existing well-validated measure of the same construct. Also check whether comparability of the ad hoc scale to the original measure is discussed.

Report it as "yes" or "no".

### Reporting of Measurement Details:

**consistent_names**: Check whether the construct's name is used consistently across the title, abstract, main text, tables, and figures. Inconsistencies include using different terms for the construct without explanation, or using a scale name that does not clearly indicate the construct it measures and appears to misfit without clarification. Missing definitions of subscales, with only a definition for the highest-order factor, should be coded as "no".

Report it as "yes" or "no".

**construct_uniqueness**: Check whether the authors clarify how the construct differs from related constructs. The description should make the uniqueness of the construct explicit. This is also to be coded as "yes" if the clarification is made focusing on the measure itself (not only when it is made with regard to theoretical uniqueness).

Report it as "yes" or "no".

**all_items**: Check whether all items of the measure are reported, either within the manuscript or in openly available supplementary materials. If only part of the items are reported, code as "no". Note: Some scales are under copyright and may not be fully reported by authors, though this is rare. A link to an original publication that includes the wording of the items is not sufficient to be coded as "yes".

For adherence, check whether the reported items match 1:1 the original items of the measure cited as the source.

Report it as "yes" or "no".

**scale_sources**: Check whether the authors provide the exact source(s) of the measure, including proper citation(s) for the original development. This includes references to published scales, books, or repositories. Verify the correctness of the citation in the provided source.

Check the methods section, focusing on subsections about measures, questionnaires, or procedures. Also, look for tables within the manuscript or in the appendix where items and their respective scale names are listed.

Report it as "yes" or "no".

### Sample Description and Justification:

**n_exclusion**: Check whether the authors specify eligibility criteria for inclusion and exclusion of participants that are based on the measure. This includes both formal criteria (e.g., thresholds within the variable to be measured) and procedural criteria (e.g., completeness of responses or technical failures). Also, check whether the number of excluded participants is reported and whether reasons for exclusion based on the measure are documented. Code as "justified" when there are exclusions and those are justified. Code as "non-justified" when there are exclusions and those are not justified. Code as "N/A" when nothing regarding exclusion related to the measure is mentioned.

Look for this information in the methods section, especially subsections on participants, procedure, or data preparation.

Report it as "justified", "non-justified", or "N/A".

**n_size**: Check whether the authors justify their sample size in relation to the study goals. Acceptable justifications may include power analyses based on expected effect sizes, precision estimations, references to previous studies, or arguments based on feasibility restrictions. The justification should demonstrate adequacy for the planned analyses. Simply reporting the number of participants without explanation should be coded as "no".

Look for this information in the methods section, usually in the description of participants, design, or planned analyses.

Report it as "yes" or "no".

### Documentation of Procedure and Analysis:

**analysis_details**: Check whether the authors detail their analytical approaches. For the analytical approach, we are looking for information on whether authors aggregated scores of their measures and how they did it (i.e., built indices/means/sums). Works should provide sufficient information to allow replication of the measure's analysis. Vague references to "standard analyses" without further specification should be coded as "no". If analysis code is available explicating this, it should be coded as "yes". The code does not need to be checked for reproducibility, though. If in addition, the original and corrected values (if applicable), software used, and methods for handling missing data are reported, then this will be coded as "complete".

Look for this information in the methods or results sections, particularly under data analysis, statistical procedure, or supplementary materials of the analysis code.

Report it as "yes", "no", or "complete".

**analysis_robustness**: Check whether the authors report the use of multiple measures or analytical approaches to ensure the robustness of their findings. This needs to be pre-registered to count as "yes". This may include triangulation with different scales, use of alternative models, sensitivity analyses, or robustness checks. To count as "yes", the alternative approaches must be described and results reported (not necessarily within the main manuscript, but referenced).

Report it as "yes" or "no".

### Objectivity, Reliability, and Validity:

**objectivity_evidence**: Check whether the authors include information on the objectivity of measurement and data collection. This involves reporting the role and qualifications of the experimenters as well as their potential susceptibility to bias (e.g., expectancy effects, lack of blinding, vested interests). 

To be coded as "yes" one of the following criteria needs to be reported: (a) naming the experimenter role and address qualifications and/or possible sources of bias; (b) standardized use of materials (e.g., identical instructions to participants and allowed time to respond); (c) definite coding/scoring of each possible response; (d) norming of responses or interpretation examples of scores to allow for objectivity in interpreting scores.

Report it as "yes" or "no".

**reliability_evidence**: Check whether the authors document reliability using appropriate metrics for each measure, subscale, subsample, and language version. Reliability evidence may include composite reliability (e.g., Cronbach's alpha, McDonald's omega), test–retest reliability, or split-half reliability. We are looking for any standard reliability index that is provided for the sample studied. The coefficient should be specified, though, to be coded as "yes". Each relevant level of analysis must be covered to be coded as "yes".

Check the results section and any psychometric analysis in tables, possibly those tables where items are displayed.

Report it as "yes" or "no".

**validity_evidence**: Check whether the authors report all available validity evidence for the measure, specifying which types of validity are addressed. This may include content validity, construct validity, criterion validity, or others. To be coded as "yes", the reporting must explicitly identify the type(s) of validity evidence provided. 

Validity evidence addresses information on the verity of a match between an interpretation of scale scores and the to be measured latent psychological construct. We are looking for evidence that the scale accurately maps onto the construct, e.g., high scores are meaningfully interpreted as high levels of the construct.

Content validity: Whether items are really suitable to capture the construct. As the content validity of a scale is determined by its final list of items, performing good practices during the construction of this list is essential. We report whether there is reporting of the construction process. This mostly involves qualitative approaches: expert assessment of the definition, of the realm of the items, and of their match to the definition.

Construct validity (factor): Whether the construct is captured and no other. The internal structure / factor validity can be measured via EFA, PCA, CFA, or, more generally, SEM (reliability tests cannot be considered a substitute for factor analyses in evaluating structural validity).

Construct validity (discriminant): Whether the construct is captured and no other. Discriminant validity with (fairly) unrelated tests. This could involve (corrected) correlations, multi-trait-multimethod matrix, CFA.

Construct validity (convergent): Whether the construct is captured and no other. Convergent validity with related tests. This could involve (corrected) correlations, multi-trait-multimethod matrix, CFA.

Criterion validity (retrospective / competitive / predictive): How well results of other tests or behaviors can be predicted by the scale score. This could be shown by correlating the current measure of our construct with other measures of an outcome, i.e., effect, variable in the past / also current / made later.

Incremental validity: The incremental validity of the new scale is supported by an association between a new scale and its related outcomes while statistically controlling for scores on another well-validated measure of our construct of interest.

We first look in the methods section, where the measure of interest is listed. Sometimes, validity evidence is reported in the results section (when authors separately validated the measure) or the introduction (when authors introduce the construct and its measures). If it was assessed in an independent sample and reported in the results section, this will be coded as "yes". If it was assessed as part of the main substantive study, this will be coded as "no" due to methodological issues of overfitting (although authors might interpret it as validity evidence).

Report it as "yes" or "no".

**validity_justification**: Check whether the authors justify the fit and operationalisation of each validity type assessed. This includes explaining why the chosen validity types are appropriate and discussing the operationalisation of the other constructs. The implications of absent or contradictory findings should also be addressed. So if there is no validity evidence (yet), this needs to be explicitly acknowledged and stated to be coded as "none". If only evidence is reported without justification or discussion, code as "no". 

Discussing the fit of the validity type can involve information on, e.g., why a certain scale needs to have a certain factor structure, be differentiated, predict a criterion, or be useful to replace an old one. For example, why was the criterion appropriate?

Discussing the operationalisation of the other constructs involves, e.g., arguments on why a scale for a discriminant or criterion-related construct was an appropriate choice / match. So, this focuses on the validity of the other measures involved in the validation study. For example, why was the criterion validly measured?

Report it as "yes", "no" or "none".

**validity_construct**: Check whether the authors document both convergent and discriminant (also called divergent) aspects of construct validity. It needs to be reported from independent data (i.e., a separate dataset from the main study). Convergent validity refers to the extent to which the measure relates to conceptually similar constructs, while discriminant validity refers to (fairly) unrelated constructs. Both aspects need to be addressed to be coded as "complete". We want to look for theoretical arguments here and not random picks of other constructs. If the evidence is reported to come from another source, verify that the scale was indeed validated there.

Look for correlation tables in the methods or results section. The methods section focusing on included measures may also include already published validity evidence. We want the authors to indicate with which other constructs and measures this evidence was established specifically.

Not confident terms: "construct validity", "MTMM", "AVE", "CFA", "SEM", "EVA", "MSV", "Fornell-Larcker criterion"

Report it as "convergent", "discriminant", "complete", or "none".

### Registration and Transparency:

**registered_study**: Check whether the study was preregistered on a public repository. 

Report it as "yes" or "no".

**registered_measures**: Check whether the measure was preregistered (e.g., on OSF, AsPredicted, or other preregistration platforms). Look for explicit mention of registration of measures before data collection. Search for hyperlinks in the text. 

Check the methods, results, or appendix section for preregistration statements and follow hyperlinks if provided. Double-check that the measure was really part of the registration. 

Report it as "yes" or "no".

**registered_scoring**: Check whether the scoring procedure for the measure was preregistered (including data processing steps, scoring algorithms, or cut-off criteria). We are looking for R scripts or other code-based scoring formulations. 

Check preregistration documents (if linked) and the methods section for explicit scoring plans described before data collection.  

Report it as "yes" or "no".

### Comprehensive Reporting of Results:

**scale_descriptives**: Check whether descriptive statistics for the scale are reported, at minimum including means and standard deviations (SDs). If descriptive statistics are only presented for subscales, these count if they cover all items. Code as "no" if descriptives are only vaguely estimable via their illustration in figures.

Report it as "yes" or "no".

## Coding Guidelines:
- Use "yes"/"no" for most criteria
- Use "not_reported" when information is missing
- Use "N/A" when criteria don't apply (e.g., ad hoc evidence when scale isn't ad hoc)
- For n_exclusion: use "justified"/"non-justified"/"N/A"
- For analysis_details: use "yes"/"no"/"complete"
- For validity_justification: use "yes"/"no"/"none"
- For validity_construct: use "convergent"/"discriminant"/"complete"/"none"

## Analysis Process:
1. Read through the paper systematically using the read_section tool with FULL section titles
2. Look for scale usage in methods, measures, results sections
3. Check tables for scale information, reliability coefficients, descriptive statistics
4. Evaluate each criterion carefully based on what is explicitly reported
5. Use the report_scale_validation tool to submit your findings

## Important Note on Reading Sections:
When using the read_section tool, you MUST use the complete section title as shown in the section index above.
For example, use "4.1 Procedure" or "A Questionnaires & Scales", NOT just "4.1" or "A".

The paper you are analyzing has the title: "{title}"

Its abstract is:
```
{abstract}
```

It has the following sections:
```
{section_index}
```

And the following tables:
```
{table_index}
```

Start by reading the relevant sections to identify if and how {scale_config.scale_name} is used, then systematically evaluate each validation criterion.
"""


def get_scale_validation_prompt(scale_config: ScaleConfig, title: str, abstract: str, section_index: str, table_index: str, include_persona: bool = True) -> str:
    """Get the complete prompt for scale validation analysis"""
    return f"""
{get_scale_validation_persona() if include_persona else ''}
{get_scale_validation_task(scale_config, title, abstract, section_index, table_index)}
"""
