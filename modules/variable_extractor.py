import pandas as pd

def extract_variables_from_json(json_data: dict) -> pd.DataFrame:
    """
    Extract variables from a Kobo form JSON structure, including multilingual labels and category values.

    Args:
        json_data (dict): The JSON data of the Kobo form.

    Returns:
        pd.DataFrame: A DataFrame containing variable names, multilingual labels, data types, and category values.
    """
    content = json_data.get("content", {}).get("survey", [])
    choices = json_data.get("content", {}).get("choices", {})
    variables = []

    for question in content:
        # Collect all labels for available languages
        labels = question.get("label", {})

        # Extract category values for select_one and select_multiple types
        category_values = None
        if question.get("type", "").startswith("select_one") or question.get("type", "").startswith("select_multiple"):
            list_name = question.get("type", "").split(" ")[1] if " " in question.get("type", "") else None
            if list_name and list_name in choices:
                category_values = [choice.get("name") for choice in choices[list_name]]

        variables.append({
            "name": question.get("name"),
            "labels": labels,  # Store all multilingual labels as a dictionary
            "type": map_data_type(question.get("type")),
            "categories": category_values  # Add category values
        })

    # Convert the list of variables into a DataFrame
    variables_df = pd.DataFrame(variables)

    # Expand the labels dictionary into separate columns for each language
    if not variables_df.empty:
        labels_df = variables_df["labels"].apply(lambda x: pd.Series(x, dtype="object"))
        variables_df = pd.concat([variables_df.drop(columns=["labels"]), labels_df], axis=1)

    return variables_df

def extract_variables_from_excel(file_path: str) -> pd.DataFrame:
    """
    Extract variables from a Kobo form Excel file, including multilingual labels and category values.
    Handles missing or empty 'choices' sheet gracefully.

    Args:
        file_path (str): The path to the Excel file.

    Returns:
        pd.DataFrame: A DataFrame containing variable names, English labels, data types, and category values with multilingual labels.
    """
    # Try to load both 'survey' and 'choices' sheets from the Excel file
    try:
        xls = pd.ExcelFile(file_path)
        if 'survey' not in xls.sheet_names:
            return pd.DataFrame()  # No survey sheet, return empty
        survey_df = pd.read_excel(xls, sheet_name="survey")
        if 'choices' in xls.sheet_names:
            choices_df = pd.read_excel(xls, sheet_name="choices")
        else:
            choices_df = None
    except Exception:
        return pd.DataFrame()  # If file is not a valid Excel, return empty

    variables = []
    survey_label_columns = [col for col in survey_df.columns if col.startswith("label::")]
    choices_label_columns = []
    if choices_df is not None:
        choices_label_columns = [col for col in choices_df.columns if col.startswith("label::")]

    for _, row in survey_df.iterrows():
        english_label = row.get("label::english", None)
        category_values = None
        category_labels = None
        if (choices_df is not None and (row["type"].startswith("select_one") or row["type"].startswith("select_multiple"))):
            list_name = row["type"].split(" ")[1] if " " in row["type"] else None
            if list_name:
                category_values = choices_df[choices_df["list_name"] == list_name]["name"].tolist()
                category_labels = choices_df[choices_df["list_name"] == list_name][choices_label_columns].to_dict(orient="records") if choices_label_columns else None
        variables.append({
            "name": row["name"],
            "label::english": english_label,
            "type": map_data_type(row["type"]),
            "categories": category_values,
            "category_labels": category_labels
        })
    variables_df = pd.DataFrame(variables)
    return variables_df

def map_data_type(data_type: str) -> str:
    """
    Map Kobo data types to human-readable categories.

    Args:
        data_type (str): The Kobo data type.

    Returns:
        str: A human-readable category.
    """
    if data_type.startswith("select_one"):
        return "Categorical variable"
    elif data_type.startswith("select_multiple"):
        return "Multiple-choice Categorical variable"
    elif data_type in ["start", "end"]:
        return "date"
    else:
        return data_type  # Keep the original type for all other cases
