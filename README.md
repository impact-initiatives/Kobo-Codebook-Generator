# Kobo Codebook Generator

## Description
Kobo Codebook Generator is a Python-based tool with a Streamlit web interface designed to convert Kobo forms into a basic codebook. The generated codebook includes essential fields such as:
- Variable names
- Descriptions
- Data types
- Value labels
- Allowed value ranges

This tool aims to streamline dataset navigation.

## Features
- Automated conversion of Kobo forms to codebooks.
- User-friendly web interface built with Streamlit.
- Supports categorical and numerical data transformations.
- Fetch Kobo forms via API or upload Excel files manually.
- Download extracted variables as a CSV file.

## Requirements
- Python 3.8+
- Streamlit
- pandas
- requests
- pyyaml
- openpyxl  # Required for handling Excel files

## Installation
1. Clone the repository:
   ```bash
   git clone git@github.com-impact:kobo-codebook-generator.git
   ```
2. Navigate to the project directory:
   ```bash
   cd kobo-codebook-generator
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the Streamlit application:
```bash
streamlit run app.py
```

### API Token Template
To upload your API token securely, use the following JSON format:

```json
{
  "token": "your_api_token_here"
}
```

Save this file as `token.json` and upload it when prompted in the application.

## Contributing
Contributions are welcome! Please create a pull request on the `dev` branch for any changes.

## License
This project is licensed under the MIT License.
