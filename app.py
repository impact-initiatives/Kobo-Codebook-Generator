import streamlit as st
from modules.api_handler import fetch_kobo_form
from modules.file_uploader import handle_file_upload
from modules.variable_extractor import extract_variables_from_json, extract_variables_from_excel

# Set the page layout to wide
st.set_page_config(layout="wide")

def main():
    """
    Main function to run the Streamlit app.
    """
    st.title("Kobo Codebook Generator")

    st.sidebar.header("Upload Options")
    upload_method = st.sidebar.radio(
        "Choose upload method:",
        ("API Upload", "File Upload")
    )

    if upload_method == "API Upload":
        st.subheader("Upload via API")
        kobo_id = st.text_input("Enter Kobo Form ID:")
        api_token = st.file_uploader("Upload API Token (JSON):", type=["json"])

        if st.button("Fetch Form"):
            if kobo_id and api_token:
                with st.spinner("Fetching form data..."):
                    form_data = fetch_kobo_form(kobo_id, api_token)
                success_msg = st.success("Form fetched successfully!", icon="✅")
                success_msg.empty()

                # Extract variables and display them
                variables_df = extract_variables_from_json(form_data)
                success_msg2 = st.success("Variables extracted successfully!", icon="✅")
                success_msg2.empty()
                st.dataframe(variables_df, use_container_width=True)

                # Provide download option
                csv = variables_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Variables as CSV",
                    data=csv,
                    file_name="variables.csv",
                    mime="text/csv"
                )

            else:
                st.error("Please provide both Kobo Form ID and API Token.")

    elif upload_method == "File Upload":
        st.subheader("Upload Excel File")
        uploaded_file = st.file_uploader("Upload Kobo Form (Excel):", type=["xlsx"])

        if uploaded_file is not None:
            form_data = handle_file_upload(uploaded_file)
            success_msg = st.success("File uploaded successfully!", icon="✅")
            success_msg.empty()

            # Extract variables and display them
            variables_df = extract_variables_from_excel(uploaded_file)
            if variables_df.empty:
                st.warning("The uploaded Kobo form is empty or does not contain a valid 'survey' sheet.")
            else:
                success_msg2 = st.success("Variables extracted successfully!", icon="✅")
                success_msg2.empty()
                st.dataframe(variables_df, use_container_width=True)

                # Provide download option
                csv = variables_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Variables as CSV",
                    data=csv,
                    file_name="variables.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()
