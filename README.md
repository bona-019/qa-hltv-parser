# 🎮 HLTV Match Parser
![Python](https://img.shields.io/badge/python-3.10+-blue)
![Coverage](https://img.shields.io/badge/coverage-99%25-brightgreen)
![Tests](https://img.shields.io/badge/tests-120+-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

This project is a Python-based parser designed to extract Counter-Strike (CS2) matches data from HLTV (https://hltv.org), structuring data in JSON format.
The script reads local stored (mocked)d HTML files as input, ensuring consistency in page structure during development and automated tests.
It was used 40 sample files representing all matches ocurred during the **StarLadder Budapest Major 2025** event. (https://www.hltv.org/results?event=8042)
Collecting, processing and storing data enables downstream analysis to generate insights such as winning team statistics, most played/banned maps and other performance-related metrics.

### ✅ Objectives Achieved
- ✅ **99% test coverage** with a complete test suite
- ✅ **Clean architecture** with clear separation of concerns
- ✅ **Comprehensive technical documentation** (code, tests and design decisions)
- ✅ **Robust handling** of edge cases and validations
- ✅ **Testable code** with small, well-defined functions
- ✅ **Fast automated test execution** (< 1:30min runtime)

# 🔭 Scope
#### ✅ Current scope
- Locally saved HTML files as input
- Supports any match format (BO1/BO3/BO5)
- Supports any match type (LAN/Online)
- Normalized and structured JSON output
- Focus on parsing reliability and test quality
- Demonstrates QA skills without external dependencies

#### ❌ Out of scope (intentionally)
- Data extraction via scraping/HTTP
- Database persistence
- Dynamic scraping with Selenium
- Handling HTML page structure changes  
- REST API for data access

# 🗂️ Project structure
    .
    ├── parser/
        ├── output/                     # Output folder for generated JSON files
        ├── samples/                    # Samples folder
        ├── tests/                      # Test folder
            ├── __init__.py
            ├── test_sanity.py          # Sanity tests
            ├── test_utils_unity.py     # Unit tests for utility functions
        ├── __init__.py
        ├── parser_fetch_data.py        # Builds and exports JSON file
        ├── parser_script.py            # Reads HTML files and extracts raw data
        ├── parser_utils.py             # Has utility functons for conversion and normalization
    ├── README.md
    └── requirements.txt

# 📑 Project files
### 📄 parser\parser_script.py
- Contains all logic for extracting data from HTML tags
- Divided into small methods for easier testing and maintenance

### 📄 parser\parser_utils.py
- Contains formatting, transformation and normalization functions

### 📄 parser\parser_fetch_data.py
- Contains the logic for building and exporting the final JSON output

# ⛔ Error handling
- Clear error messages for invalid or unsupported files
- `score` values converted to `int`; if a map was not played then `score == None`
- Date format validation
- Match format validation (Best of x)
- LAN/Online match type validation

# 💻 Running the script
#### 1. Install the required libraries (`python -m pip install -r requirements.txt` - Python 3.10+)
#### 2. Save the HTML file(s) into the `samples` folder
#### 3. Navigate to project root folder
#### 4. Run
- `python -m parser.parser_fetch_data file.html`
#### 5. Output
- A JSON file will be generated in the `output` folder named `file.html.json`

# 📤 Example output (JSON)
Handled edge case: BO5 matches taht finished before the 5th map (e.g: 3-1), returning `None` for the `score` values of non-played maps.

`{
    "event": "StarLadder Budapest Major 2025",
    "date": "2025-12-14",
    "teams": [
        {
            "team1": "Vitality",
            "team2": "FaZe"
        }
    ],
    "format": "bo5",
    "mode": "LAN",
    "stage": "Grand final",
    "score": [
        {
            "map": "Nuke",
            "team1_score": 6,
            "team2_score": 13
        },
        {
            "map": "Dust2",
            "team1_score": 13,
            "team2_score": 3
        },
        {
            "map": "Inferno",
            "team1_score": 13,
            "team2_score": 9
        },
        {
            "map": "Overpass",
            "team1_score": 13,
            "team2_score": 2
        },
        {
            "map": "Mirage",
            "team1_score": null,
            "team2_score": null
        }
    ]
}`

# ⁉️ Tests

## 📊 Quality metrics

| Metric | Value |
|---------|-------|
| **Code coverage** | 99%
| **Total tests** | 120+
| **Runtime** | < 30s

## 🧪 Test strategy

### Test layers

| File | Type | Objective | Quantity |
|---------|------|----------|------------|
| `test_sanity.py` | **Sanity** | Validate core functionalities using real HTML files | 100+ tests |
| `test_utils_unit.py` | **Unit** | Test isolated utility functions | 20 tests |

### Scenario coverage

#### ✅ Happy path
- Complete BO1, BO3, and BO5 matches  
- Multiple date formats (1st, 2nd, 3rd, 4th, etc.)  
- Teams with special names and Unicode characters  
- Format normalization (Best of X → boX)  

#### ✅ Edge cases
- **Non-played maps**: BO5 ending 3–0 (scores = `null`)  
- **Whitespace handling**: data containing spaces, tabs, and newlines  

#### ✅ Validation tests
- Returned data types (string, int, list, dict)  
- JSON structure validation (required fields)  
- Normalized date format (YYYY-MM-DD)  
- Normalized match format (bo1/bo3/bo5)  
- Exported data integrity  

#### ✅ Negative tests (error handling)
- Invalid date format → `ValueError`  
- Unknown match format → `ValueError`  
- Invalid score conversion → returns `None`  
- Invalid input type → `TypeError`  
---

### Test files

#### `test_sanity.py` — Sanity tests  
Validates core functionality using real HTML files with pytest parametrization.

**Coverage:**
- Parser instantiation with all HTML samples  
- All methods return the expected data types  
- `fetch_data()` generates a valid dictionary  
- `export_json()` creates the file and preserves data integrity  

**Techniques used:**
- Pytest parametrize  
- Fixtures for parser reuse  
- Type validation and presence checks  
---

#### `test_utils_unit.py` — Unit tests  
Tests transformation and normalization functions in isolation, without external dependencies.

**Test classes:**

**`TestConvertScore`**
- Conversion of valid strings to int  
- Conversion of invalid values to `None`  
- Whitespace handling (spaces, tabs)  
- Negative numbers (edge case)  

**`TestFetchTeamData`**
- Correct team dictionary structure  
- Key validation (`team1`, `team2`)  
- Return type validation (single-element list)  

**`TestNormalizeDate`**
- Normalization with suffixes: st, nd, rd, th  
- Output format: YYYY-MM-DD  

**`TestNormalizeFormat`**
- Valid formats: Best of 1/3/5 → bo1/bo3/bo5  
- Invalid formats raise `ValueError`  
- Type validation: non-strings raise `TypeError`  

**`TestNormalizeMode`**
- Valid formats: Best of X (LAN)/(Online) → LAN/Online  
- Invalid formats raise `ValueError`  
- Type validation: non-strings raise `TypeError`  

**`TestFetchMapData`**
- BO1: 1 map played  
- BO3: 2 maps (2–0) and 3 maps (2–1)  
- BO5: 3 maps (3–0), 4 maps (3–1), 5 maps (3–2)  
- Structure validation: map, team1_score, team2_score  
- Non-played maps: scores = `None`  
---

## 🚀 Running tests

### Basic commands
```bash
# Run all tests
pytest -v

# Run tests with coverage
pytest -v --cov=parser --cov-report=html

# Run specific test files
pytest tests/test_sanity.py -v
pytest tests/test_utils_unit.py -v

### Viewing coverage reports
```bash
# Generate HTML report
pytest -v --cov=parser --cov-report=html

# Generate terminal report
pytest -v --cov=parser
```

### Expected output (formatted)
```
...
parser/tests/test_utils_unit.py::TestNormalizeFormat::test_normalize_format_invalid PASSED
parser/tests/test_utils_unit.py::TestNormalizeMode::test_normalize_mode_valid PASSED
parser/tests/test_utils_unit.py::TestNormalizeMode::test_normalize_mode_invalid PASSED
parser/tests/test_utils_unit.py::TestFetchMapData::test_fetch_map_data_valid_bo1 PASSED
parser/tests/test_utils_unit.py::TestFetchMapData::test_fetch_map_data_valid_bo3_2maps PASSED

coverage: platform win32, python 3.13.9-final-0
Name                              Stmts   Miss  Cover
-----------------------------------------------------
parser\__init__.py                    0      0   100%
parser\parser_fetch_data.py          29      4    86%
parser\parser_script.py              28      0   100%
parser\parser_utils.py               26      0   100%
parser\tests\__init__.py              0      0   100%
parser\tests\test_sanity.py          49      0   100%
parser\tests\test_utils_unit.py     143      0   100%
-----------------------------------------------------
TOTAL                               275      4    99%
140 passed in 76.11s (0:01:16)
```

# 🛠️ Tech stack

- Python 3.10+
- BeautifulSoup4 (parsing de HTML)
- Pytest (framework de testes)
- JSON (formato de saída)
- Regex (extração de padrões)
- Datetime (manipulação de datas)