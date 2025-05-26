import streamlit as st
from modules.api_handler import fetch_kobo_form
from modules.file_uploader import handle_file_upload

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
                form_data = fetch_kobo_form(kobo_id, api_token)
                st.success("Form fetched successfully!")
                # Extract and display only the form structure
                form_structure = form_data.get("content", {})
                st.json(form_structure)
            else:
                st.error("Please provide both Kobo Form ID and API Token.")

    elif upload_method == "File Upload":
        st.subheader("Upload Excel File")
        uploaded_file = st.file_uploader("Upload Kobo Form (Excel):", type=["xlsx"])

        if uploaded_file is not None:
            form_data = handle_file_upload(uploaded_file)
            st.success("File uploaded successfully!")
            st.dataframe(form_data)

if __name__ == "__main__":
    main()
