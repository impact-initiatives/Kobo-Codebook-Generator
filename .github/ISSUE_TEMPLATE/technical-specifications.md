---
name: Technical Specifications
about: Define the technical requirements for the project
---

# Technical Specifications for the Codebook Generator

## Objective
Develop a tool to convert KOBO Form into a basic codebook with the following minimum fields:
- Variable name
- Variable label/description
- Data type
- Value labels (for categorical variables)
- Allowed values (range; for percentages or integer variables)

## Requirements
1. **Input**: KOBO forms via API or Excel file uploads.
2. **Output**: A codebook containing the specified fields.
3. **Data Transformations**:
   - Convert `select_one` in KOBO to categorical in the final codebook.
   - Convert `select_multiple` in KOBO to multiple binary variables or a single variable with concatenated values in the final codebook.
4. **Technology**:
   - Use Python for backend processing.
   - Use Streamlit for the web interface.
5. **Progress**:
   - First operational version completed in May 2025.

## Additional Notes
- The tool is user-friendly to accommodate the lower capacity of some country teams.
- Automates as much of the process as possible to reduce manual effort.
- Provides CSV download functionality for extracted variables.

## Questions
- Are there any additional fields or transformations required?
- Should the tool support multiple languages for the interface?

---

Please review and provide feedback or additional requirements.
