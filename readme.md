# Synthetic Healthcare Data Generator

## Overview
This project provides a tool for generating synthetic healthcare data based on real datasets. It uses the Groq LLM API to analyze patterns in real healthcare data and generate realistic synthetic data while maintaining statistical properties and relationships between variables.

## Features
- Reads CSV format healthcare datasets
- Generates exactly 100 rows of synthetic data
- Maintains statistical properties and relationships of the original data
- Preserves data types and business rules
- Automatic handling of unique identifiers
- Supports extraction of data from XML-style tags
- UTF-8 encoding support

## Prerequisites
- Python 3.x
- Access to Groq API (API key required)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/SamnangGit/synthetic-data-generation.git
cd synthetic-data-generation
```

### 2. Create a Virtual Environment

#### For macOS/Linux:
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate   # For bash/zsh
# OR
source venv/bin/activate.fish   # For fish shell
# OR
source venv/bin/activate.csh    # For csh/tcsh
```

#### For Windows:
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# In Command Prompt:
venv\Scripts\activate.bat
# OR in PowerShell:
venv\Scripts\Activate.ps1
```

### 3. Install required dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root with:
```
GROQ_API_KEY=your_groq_api_key_here
```

### Notes:
- To deactivate the virtual environment when you're done, simply run:
  ```bash
  deactivate
  ```
- Make sure you always activate the virtual environment before running the project
- If you see permission errors on Windows PowerShell, you might need to run:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```


## Project Structure
```
.
├── dataset/
│   └── healthcare_dataset.csv
├── output/
│   └── new_two.csv
├── .env
└── main.py
```

## Usage

### Basic Usage
1. Place your source CSV file in the `dataset` folder
2. Run the script:
```bash
python main.py
```
3. Find the generated synthetic data in the `output` folder

### Functions

#### `read_csv(path)`
Reads a CSV file and returns its contents as a string.
- Parameters:
  - `path` (str): Path to the CSV file
- Returns:
  - String containing CSV content
- Raises:
  - FileNotFoundError: If file doesn't exist
  - IOError: If reading error occurs

#### `write_csv(csv_string, output_path, extract_from_tags=True)`
Writes CSV string content to a new file.
- Parameters:
  - `csv_string` (str): CSV content to write
  - `output_path` (str): Destination path
  - `extract_from_tags` (bool): Whether to extract content from XML tags
- Raises:
  - ValueError: If CSV string is empty
  - IOError: If writing error occurs

#### `data_generation(prompt, model)`
Generates synthetic data using Groq API.
- Parameters:
  - `prompt` (str): Formatted prompt with real data
  - `model` (str): Name of the Groq model to use
- Returns:
  - Generated synthetic data as string

## Model Configuration
The project uses the `llama-3.2-11b-text-preview` model from Groq. This can be modified by changing the `model` variable in the script.

## Data Format
The synthetic data maintains the same format as the input data, including:
- Same column names and order
- Similar data distributions
- Preserved relationships between variables
- Matching data types
- New unique identifiers where applicable

## Error Handling
The script includes comprehensive error handling for common issues:
- File not found errors
- IO errors
- Empty data validation
- Directory creation errors
- API communication errors

## Limitations
- Currently generates exactly 100 rows of data
- Requires Groq API access
- Input CSV must be properly formatted

## Contributing
Feel free to submit issues and enhancement requests!

