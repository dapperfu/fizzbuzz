# Cursor Rules - Copilot Instructions

This document consolidates all atomic cursor rules from the cursor_rules repository into a unified copilot-instructions format for AI agents and developers.

---

## SAFETY RULES (Universal - Apply to All Code)

### No Sudo Usage
Under no circumstances SHALL you run `sudo`. All commands SHALL be executed in userspace only.

### Home Directory Protection
NEVER under any circumstances run `rm -rf ~/`. This command SHALL NOT be used as it is extremely dangerous and destroys the entire home directory.

### Command-Line Safety
SHALL NOT use `!` in strings meant for the command line / bash, as this can cause unintended command interpretation.

---

## GIT RULES (Universal - Apply to All Projects)

### Git User Configuration
Before committing, the git user SHALL be configured to identify automated commits from AI assistance: `"$(whoami) | Cursor.sh | <model>"`

### Git Commit Message Format
All git commit messages SHALL follow this structured format:

**Format Structure:**
1. First line: Brief one-liner summary
2. Blank line
3. List of changes (each prefixed with `- `)
4. Blank line
5. Separator line with exactly 5 dashes: `-----`
6. Technical attribution section

**Technical Attribution Template:**
```
Prompt: {{prompt}}
Context: {{brief_description_of_what_this_code_does}}

Technical details:
- Model: {{specific_llm_model}}
- IDE: Cursor {{cursor_version}}
- Generation method: AI-assisted pair programming
- Code style: {{language_specific_style_guide}}
- Dependencies: {{key_dependencies}}
```

### Git Push Requirement
ALL git commits SHALL be followed by a `git push` if and only if a remote exists.

### Git Upstream Sync
SHALL sync with upstream before committing. The upstream sync workflow SHALL follow these steps:

1. `git fetch upstream && git fetch origin`
2. Detect upstream branch: `git symbolic-ref refs/remotes/upstream/HEAD | sed 's@^refs/remotes/upstream/@@' || echo "main"`
3. Merge upstream changes: `git merge upstream/<branch>`
4. Resolve any merge conflicts automatically when possible
5. Then proceed with commit
6. After commit, push if remote exists

---

## PYTHON RULES

### Python Version and Modern Practices
All Python projects SHALL target Python 3.10 or higher. All Python code SHALL use the most idiomatic Python practices for 2025, including:

- Type hints with modern syntax (PEP 604 union types: `str | int` instead of `Union[str, int]`)
- Structural pattern matching (match/case statements) where appropriate
- Dataclasses and modern data structures
- Context managers and async/await patterns where applicable
- f-strings for string formatting
- Path objects from `pathlib` instead of string paths
- Modern exception handling patterns
- Type guards and type narrowing
- Generic types and type variables for reusable code

### Python Virtual Environment Requirement
All Python-related work SHALL use a virtual environment. Do NOT attempt to use the system pip or install Python packages to the system.

### Python Virtual Environment Naming
Virtual environments SHALL be named `venv_$(basename $(pwd))`. This naming convention makes them unique among multiple venv-based projects and allows easy identification of the active environment in bash.

Example: For project `/project/foo`, the venv SHALL be `venv_foo`.

### Python Virtual Environment Paths in Makefiles
All Makefile references to pip and python-installed tools (like pytest) SHALL use the full path to the venv bin directory.

Examples:
- `venv_{project}/bin/pytest`
- `venv_{project}/bin/pip`

### Python Type Checking
All Python language scripts SHALL use full mypy typing.

### Python Documentation
All Python language scripts SHALL be documented with NumPy-style docstrings (NumPy docstring format).

### Python Documentation Linting
Documentation SHALL be linted for correctness.

### Python Line Length
Python line lengths SHALL be 120 characters.

### Python Logging Levels
All Python projects SHALL implement custom logging levels between INFO (20) and DEBUG (10) for granular verbosity control:

- **VERBOSE (18)**: General verbose output, one level below INFO. Corresponds to `-v` flag.
- **DETAIL (16)**: Detailed information about operations. Corresponds to `-vv` flag.
- **TRACE (14)**: Execution flow tracing. Corresponds to `-vvv` flag.
- **FINE (12)**: Fine-grained debugging information. Corresponds to `-vvvv` flag.

Verbosity flag mapping:
- No flag: INFO level (20)
- `-v`: VERBOSE (18)
- `-vv`: DETAIL (16)
- `-vvv`: TRACE (14)
- `-vvvv`: FINE (12)
- `-vvvvv` or more: DEBUG (10)

### Python pyproject.toml Requirement
All Python projects SHALL use `pyproject.toml` for project configuration and metadata. Python projects SHALL NOT use `setup.py`. The `pyproject.toml` file SHALL contain all project metadata, dependencies, build system configuration, and tool configurations (e.g., mypy, ruff, pytest).

### Python Ruff Check and Format
All Python files and notebooks SHALL be checked with ruff. All Python files and notebooks SHALL be formatted with ruff. This applies to both `.py` files and `.ipynb` notebook files.

### Python UV Package Manager
UV SHALL be used for all package transactions other than initial setup of UV itself. UV SHALL be used for speed in package management operations.

### Click Library Requirement
All Python command-line interface (CLI) projects SHALL use the Click library for argument parsing and command definition. Python CLI projects SHALL NOT use argparse or other argument parsing libraries.

Click provides:
- Consistent command-line interface patterns across projects
- Built-in shell completion support (bash, zsh, fish)
- Better help text generation
- Command grouping and nesting capabilities
- Type conversion and validation
- Consistent error handling

### Click CLI Completions
For all Click CLI projects, there SHALL be commands to install and uninstall shell completions with automatic shell detection.

**Required Commands:**
- `{tool} install-completions` - Auto-detect shell and install appropriate completions
- `{tool} install-completions --shell {bash|zsh|fish}` - Install for specific shell
- `{tool} uninstall-completions` - Remove completions for detected shell
- `{tool} uninstall-completions --shell {bash|zsh|fish}` - Remove for specific shell

**Shell Detection:** Auto-detect shell by checking `SHELL` environment variable and parent process.

**Supported Shells:** bash, zsh, fish

**RC File Locations:**
- bash: `~/.bashrc` or `~/.bash_profile`
- zsh: `~/.zshrc`
- fish: `~/.config/fish/config.fish`

---

## MAKEFILE RULES

### Makefile Variable Escaping
Makefiles SHALL use full escape for all variables: `${VAR}` not `$VAR` to avoid confusion.

### Makefile Target Dependencies
All makefiles SHALL use actual files/folders where possible as targets. Any target that depends on Python having the venv built SHALL use the venv directory/file as a dependency so that GNU make resolves everything correctly and in the right order.

Example: A training target depending on data preparation SHALL reference the actual data files as dependencies.

---

## AI/ML RULES

### Model Naming Conventions
All machine learning models SHALL be named using the pattern: `{ProjectName}{Architecture}{Variant}`

Model names SHALL follow CamelCase or PascalCase conventions and be descriptive enough to identify the architecture.

Examples:
- `EucherAlphaGo` - Project: Eucher, Architecture: AlphaGo
- `PokerMonteCarlo` - Project: Poker, Architecture: MonteCarlo
- `ImageClassifierResNet50` - Project: ImageClassifier, Architecture: ResNet50

Model-related files and directories SHALL use consistent naming:
- Model checkpoints: `checkpoints/{model_name}/`
- Model definitions: `models/{model_name}.py` or `models/{model_name}/`
- Configuration files: `configs/{model_name}.yaml`
- Logs: `logs/{model_name}/`

### Model Checkpoints and Resume
All machine learning training scripts SHALL implement regular checkpointing (default: every epoch or N iterations). Checkpoints SHALL include:

- Model state (weights, parameters)
- Optimizer state (for resume training)
- Training metadata: current epoch/iteration, best validation loss/metric, training history, random number generator state

Training scripts SHALL:
- Checkpoint at the end of each epoch (default) or at configurable intervals
- Automatically detect and resume from the latest checkpoint by default
- Support `--resume` flag to explicitly specify checkpoint path
- Support `--no-resume` flag to start training from scratch
- Support `--checkpoint-dir` command-line argument
- Support `--checkpoint-interval` argument

Checkpoint directory structure:
```
checkpoints/
  {model_name}/
    checkpoint_epoch_{N}.pth
    checkpoint_best.pth
    checkpoint_latest.pth
```

### Experiment Tracking
All machine learning training runs SHALL log experiment metadata (hyperparameters, dataset info, git commit hash). Training scripts SHALL output structured logs (JSON or structured logging format). Experiment runs SHALL be uniquely identifiable (timestamp, run ID, or commit hash). Logs SHALL include training metrics, validation metrics, and system metrics (GPU/CPU usage).

**Experiment Metadata to Log:**
- Hyperparameters (learning rate, batch size, architecture parameters)
- Dataset information (path, version, size, splits)
- Git commit hash (for code version tracking)
- Environment information (Python version, framework versions)
- System configuration (GPU model, CPU count, memory)

**Structured Logging:**
- JSON format for machine-readable logs
- Or structured logging format (e.g., Python logging with JSON formatter)
- Logs SHALL be saved to files, not only printed to console

**Log Directory Structure:**
```
logs/
  {model_name}/
    {run_id}/
      metrics.json
      config.json
      system_metrics.json
```

### Data Versioning
Machine learning projects SHALL track data versions and dataset provenance. Training scripts SHALL accept data version identifiers or paths. Data preprocessing SHALL be reproducible and versioned. Dataset checksums or version hashes SHALL be logged with experiments.

Data version tracking:
- Assign version identifiers to datasets (e.g., `v1.0`, `v1.1`, `2024-01-15`)
- Store version information with datasets
- Document dataset changes between versions

Training scripts SHALL:
- Accept data version identifiers as command-line arguments
- Accept data paths that include version information
- Log the data version used in experiment metadata

Example:
```bash
python train.py --data-version v1.0
# or
python train.py --data-path data/v1.0/
```

### Model Evaluation
All machine learning models SHALL have evaluation scripts separate from training scripts. Evaluation scripts SHALL compute standard metrics for the task type. Evaluation results SHALL be saved in a structured format (JSON, CSV, or report). Evaluation SHALL support both validation and test sets. Evaluation scripts SHALL accept model checkpoint paths as arguments.

**Standard Metrics:**
- Classification: accuracy, precision, recall, F1-score, confusion matrix
- Regression: MAE, MSE, RMSE, R²
- Ranking: NDCG, MAP, MRR
- Other task-specific metrics as appropriate

**Command-Line Interface:**
```bash
python evaluate.py \
  --checkpoint checkpoints/model_name/checkpoint_best.pth \
  --data-path data/test/ \
  --split test \
  --output results/evaluation_test.json
```

### Configuration Management
Machine learning projects SHALL use configuration files (YAML, JSON, or TOML) for hyperparameters. Configuration files SHALL be version-controlled. Training scripts SHALL support both command-line arguments and config file overrides. Config files SHALL include sections for model, data, training, and evaluation parameters.

**Configuration Structure:**
```yaml
model:
  architecture: ResNet50
  num_classes: 10

data:
  train_path: data/train/
  val_path: data/val/
  batch_size: 32

training:
  learning_rate: 0.001
  epochs: 100
  optimizer: Adam

evaluation:
  metrics: [accuracy, f1_score]
```

### Training Scripts
All machine learning models SHALL be accompanied by training scripts with appropriate help documentation. Training scripts SHALL:

- Accept command-line arguments for hyperparameters, data paths, and configuration
- Provide `--help` or `-h` documentation explaining all arguments
- Include a Rich dashboard to display training progress in real-time
- Display training loss, validation loss, metrics, epoch/iteration progress, training time, learning rate, and system metrics
- Display humorous quips from the `fortune` command every 30 seconds
- Support fallback options: `--tqdm` flag for tqdm progress bars, `--no-rich` flag to disable Rich dashboard

Each training script SHALL have a corresponding shell script wrapper with sane defaults. Shell wrapper scripts SHALL be executable and documented with usage examples.

Example structure:
```
train_model.py          # Main training script with --help
train_model.sh          # Shell wrapper with defaults
```

### Makefile Integration for ML Projects
Machine learning projects SHALL include Makefile targets for common workflows (train, evaluate, test, clean). Makefile targets SHALL use file-based dependencies (e.g., model checkpoints, data files). Training targets SHALL depend on data preparation targets. Evaluation targets SHALL depend on trained model checkpoints.

**Required Makefile Targets:**
- `train` - Train the model
- `evaluate` - Evaluate trained model
- `test` - Run tests
- `clean` - Clean generated files (checkpoints, logs, etc.)

Example:
```makefile
checkpoints/model.pth: data/preprocessed/train.pt
	$(PYTHON) train.py --data data/preprocessed --checkpoint-dir checkpoints
```

---

## ENDPOINT/API RULES

### Real Endpoints Preferred Over Mocks
Mock interfaces SHALL NOT be preferred. SHALL always prefer to use real endpoints with actual authentication. Live endpoints with real API keys SHALL be preferred over mocks. Real authentication tokens SHALL be used. Actual network calls to services SHALL be used.

Mocks SHALL only be used when:
- Real endpoints are temporarily unavailable
- Testing error handling scenarios
- Development environment setup
- CI/CD pipeline requirements

Mocks SHALL NOT be used for happy path testing or authentication flows.

### Endpoint Authentication Handling
If an app returns unauthenticated status, SHALL attempt authentication. If authentication fails, tests SHALL short circuit and exit gracefully. SHALL NOT proceed with unauthenticated requests to live endpoints. All test suites SHALL attempt real authentication first. Authentication failures SHALL trigger graceful test exit with clear error message.

### Endpoint Error Handling
Error handling for endpoints SHALL follow these patterns:

- Unauthenticated responses → Attempt re-authentication
- Authentication failure → Short circuit tests with clear error message
- Network failures → Retry with exponential backoff
- API errors → Log detailed error information for debugging

---

## REQUIREMENTS MANAGEMENT - DOORSTOP

### Doorstop Document Hierarchy
Requirements management SHALL use the `doorstop` Python package with a hierarchical document structure:

- **SYS** (System Requirements): High-level system requirements
- **SRS** (Software Requirements): Detailed software requirements (child of SYS)
- **TEST** (Test Cases): Test cases and validation criteria (child of SRS)

**Directory Structure:**
```
reqs/
├── sys/           # System requirements (SYS)
│   ├── .doorstop.yml
│   └── SYS001.yml
├── srs/           # Software requirements (SRS)
│   ├── .doorstop.yml
│   └── SRS001.yml
└── test/          # Test cases (TEST)
    ├── .doorstop.yml
    └── TEST001.yml
```

### Doorstop Workflow
SHALL use doorstop commands for requirements management workflow:

- `make reqs-init`: Initialize doorstop structure (one-time)
- `make reqs-add`: Add new requirement (interactive)
- `make reqs-edit`: Edit requirements
- `make reqs-validate`: Validate requirement links
- `make reqs-export`: Export to HTML/Markdown/CSV/YAML
- `make reqs-publish`: Generate and publish requirement docs
- `make reqs-tree`: View document tree structure
- `make reqs-help`: Show requirements management help

**Adding Requirements Process:**
1. System Requirements: `make reqs-add` and select SYS
2. Software Requirements: `make reqs-add` and select SRS
3. Test Cases: `make reqs-add` and select TEST

### Doorstop Best Practices
SHALL follow these best practices for requirements management:

- Write clear, testable requirements
- Use consistent terminology
- Include acceptance criteria
- Link requirements to code implementation
- Maintain parent-child relationships
- Document requirement changes
- Export requirements for stakeholders
- Run `make reqs-validate` regularly
- Ensure all requirements have proper links
- Check for orphaned requirements

---

## REQUIREMENTS MANAGEMENT - STRICTDOC (MIL-STD-498)

### StrictDoc Document Hierarchy
Requirements management SHALL use the `strictdoc` Python package with a hierarchical document structure following MIL-STD-498 standards.

Reference: https://github.com/AutomotiveDevOps/MIL-STD-498/tree/master/strictdoc_md

**Document Types (MIL-STD-498):**
- **SRS** (System Requirements Specification): High-level system requirements
- **SSS** (Software Requirements Specification): Detailed software requirements
- **SDD** (Software Design Document): Design specifications
- **IRS** (Interface Requirements Specification): Interface requirements
- **TP** (Test Plan): Test planning documents
- **TD** (Test Description): Test case descriptions

**Directory Structure:**
```
requirements/
├── srs/              # System Requirements Specification
│   └── SRS001.sdoc
├── sss/              # Software Requirements Specification
│   └── SSS001.sdoc
├── sdd/              # Software Design Document
│   └── SDD001.sdoc
├── irs/              # Interface Requirements Specification
│   └── IRS001.sdoc
├── tp/               # Test Plan
│   └── TP001.sdoc
└── td/               # Test Description
    └── TD001.sdoc
```

All requirements documents SHALL use the `.sdoc` file format and follow StrictDoc grammar and syntax rules.

### StrictDoc HTML Output
Generated HTML files SHALL be stored in a separate `requirements_html/` directory. The HTML directory structure SHALL mirror the source document structure.

**Directory Structure:**
```
requirements_html/
├── srs/              # HTML output for System Requirements
│   └── SRS001.html
├── sss/              # HTML output for Software Requirements
│   └── SSS001.html
├── sdd/              # HTML output for Design Documents
│   └── SDD001.html
├── irs/              # HTML output for Interface Requirements
│   └── IRS001.html
├── tp/               # HTML output for Test Plans
│   └── TP001.html
└── td/               # HTML output for Test Descriptions
    └── TD001.html
```

Example mapping: `requirements/srs/SRS001.sdoc` → `requirements_html/srs/SRS001.html`

HTML files SHALL NOT be manually edited; all changes SHALL be made to source `.sdoc` files.

### StrictDoc Pre-Commit HTML Generation
HTML documentation SHALL be generated automatically before each git commit. A pre-commit hook SHALL be configured to run StrictDoc HTML generation at `.git/hooks/pre-commit`. The pre-commit hook SHALL execute `make strictdoc-generate` before allowing commits and SHALL fail the commit if HTML generation fails.

### StrictDoc Workflow
SHALL use StrictDoc commands for requirements management workflow. SHALL provide make targets for all requirements management operations:

- `make strictdoc-init`: Initialize StrictDoc project structure (one-time)
- `make strictdoc-generate`: Generate HTML documentation from `.sdoc` files
- `make strictdoc-validate`: Validate all StrictDoc documents
- `make strictdoc-export`: Export requirements to various formats
- `make strictdoc-serve`: Start StrictDoc web server for viewing/editing
- `make strictdoc-tree`: View document tree structure
- `make strictdoc-help`: Show StrictDoc management help

**Adding Requirements Process:**
1. Create or edit `.sdoc` files in the appropriate directory
2. Use `make strictdoc-validate` to check document validity
3. Use `make strictdoc-generate` to generate HTML output
4. Commit both source `.sdoc` files and generated HTML files

### StrictDoc Best Practices
SHALL follow these best practices for StrictDoc requirements management:

**Requirement Writing:**
- Write clear, testable requirements following MIL-STD-498 standards
- Use consistent terminology across all documents
- Include acceptance criteria for each requirement
- Use proper StrictDoc grammar and syntax
- Maintain requirement uniqueness and avoid duplication

**Document Structure:**
- Organize documents according to MIL-STD-498 document types
- Maintain consistent document structure within each type
- Use proper document metadata (title, version, date, etc.)

**Traceability:**
- Link requirements to code implementation using requirement IDs in comments
- Maintain parent-child relationships between documents
- Establish bidirectional traceability between requirements and tests
- Link design documents to corresponding requirements

**Validation:**
- Run `make strictdoc-validate` before committing changes
- Ensure all requirements have proper links and references
- Check for orphaned requirements and broken links
- Verify requirement IDs follow naming conventions

**Configuration Management:**
- Use StrictDoc configuration files (e.g., `strictdoc.toml`)
- Configure HTML output directory to `requirements_html/`
- Maintain consistent StrictDoc version across the project

---

## TOOL-SPECIFIC RULES

### Mitmproxy Log Handling
NEVER use strings, grep, or plain text tools on mitmproxy logs (*.log files). These files contain binary data and SHALL NOT be treated as plain text. SHALL use `mitmdump` to analyze mitmproxy/mitmweb logs.

---

## GENERAL DEVELOPMENT WORKFLOW

After all file changes, SHALL add and commit per commit message rules (see Git Commit Message Format). SHALL follow git push rules (see Git Push Requirement).

---

## SUMMARY OF REQUIREMENTS LANGUAGE

All rules use consistent requirements terminology:

- **SHALL** - Mandatory requirement (must be implemented)
- **SHALL NOT** - Prohibited action (must not be done)
- **MUST** - Required for correctness
- **SHOULD** - Recommended but not mandatory

---

## RULE SELECTION BY PROJECT TYPE

**Universal Rules (Recommended for all projects):**
- All SAFETY RULES
- All GIT RULES
- General Development Workflow

**Python Projects:**
- All PYTHON RULES
- MAKEFILE RULES (if using Makefiles)

**AI/ML Projects:**
- All AI/ML RULES
- All PYTHON RULES
- MAKEFILE RULES (if using Makefiles)

**API/Web Service Projects:**
- All ENDPOINT/API RULES
- PYTHON RULES (if using Python)

**Requirements Management Projects:**
- Choose **either** DOORSTOP **or** STRICTDOC (not both)

**Tool-Specific:**
- TOOL-SPECIFIC RULES (only when using those tools)

---

## KEY REFERENCES

- `.mdc` files are in category-specific folders in the cursor_rules repository
- Each rule is atomic and focuses on one requirement
- Rules are organized by category: `safety/`, `git/`, `python/`, `ai/`, `makefile/`, `endpoints/`, `requirements/`, `requirements-strictdoc/`, `tools/`
- All rules should be used as git submodule at `.cursor/rules/` in projects using them
- Rules can be selectively included via symlinking or copying specific files

