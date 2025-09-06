# PowerPaperParser

This is the PowerPaperParser Agent!
Be prepared!

Setup: Have the requirements.txt from the Python directory installed.

## Statistical Test Extraction (Original Functionality)

### *First Option:* Running via command line (single paper, output printed):

**Note: The topic extraction will not be applied!**

```
export OPENAI_API_KEY=YOUR_KEY
python main.py
```

### *Second Option:* Running the script without arguments (multiple papers supported):

*(Optional)* If the OpenAI Key is not set as an environment variable, make a file OPENAI_API_KEY with the key in it.

In src/settings, set the path (html_folder_path) to the folder with the HTML paper files.
Add the papers to be evaluated to the papers list (papers) with the .html ending.

```
python main_IDE.py
```

After executing, there should be a results folder with the extracted test data.
The result file name is equivalent to the HTML paper name but as a JSON.
There is also a .md file with equivalent name, which is a protocol of the conversation with the LLM.

## Scale Validation Analysis (New Functionality)

The PowerPaperParser now includes a new mode for analyzing psychometric scale validation reporting in research papers. This functionality evaluates how well authors report the use of psychometric scales according to 22 validation criteria based on best practices from the psychometric literature.

### Running Scale Validation Analysis:

*(Optional)* If the OpenAI Key is not set as an environment variable, make a file OPENAI_API_KEY with the key in it.

In src/settings, configure:
- `html_folder_path`: path to the folder with HTML paper files
- `papers`: list of papers to analyze (with .html ending)
- `TARGET_SCALE`: which scale to analyze ("nasa_tlx", "sus", "tam")

```
python main_scale_validation.py
```

### Scale Validation Criteria:

The system evaluates papers against 22 criteria organized into 6 reporting guidelines:

1. **Justification and Consequences of Scale Selection and Modification** (5 criteria)
2. **Reporting of Measurement Details** (4 criteria)
3. **Sample Description and Justification** (2 criteria)
4. **Documentation of Procedure and Analysis** (2 criteria)
5. **Objectivity, Reliability, and Validity** (5 criteria)
6. **Registration and Transparency** (3 criteria)
7. **Comprehensive Reporting of Results** (1 criterion)

### Output:

Results are saved as `{paper_name}_scale_validation.json` and include:
- Paper metadata (title, authors, DOI, etc.)
- Scale validation analysis with all 22 criteria evaluated
- Additional notes and confidence ratings

### Supported Scales:

Currently configured for:
- **NASA-TLX**: Task Load Index for workload assessment
- **SUS**: System Usability Scale
- **TAM**: Technology Acceptance Model

The system is modular and can be easily extended to support additional scales by adding configurations to `scale_validation_models.py`.
