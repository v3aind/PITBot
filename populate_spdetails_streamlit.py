import pandas as pd
import streamlit as st
from io import BytesIO
import requests

import threading
import time

file_url="https://github.com/v3aind/PITBot/blob/main/programcode.xlsx"

# Fetch the file content
response = requests.get(file_url)
file_bytes = response.content

# Streamlit Download Button
st.download_button(
    label="Download Program Code Reference File",
    data=file_bytes,
    file_name="reference_file.csv",
    mime="text/csv"
)

def keep_awake():
    while True:
        try:
            requests.get("https://sp-area-details-dmp.streamlit.app")  # Replace with your app URL
        except Exception as e:
            print("Keep-awake request failed:", e)
        time.sleep(600)  # Ping every 10 minutes

# Start keep-awake thread
threading.Thread(target=keep_awake, daemon=True).start()

# Function to handle the processing
def process_files(file1, file2, progress_bar):
    # Load the two Excel files into pandas DataFrames
    progress_bar.progress(10)
    df1 = pd.read_excel(file1)
    progress_bar.progress(30)
    df2 = pd.read_excel(file2)
    progress_bar.progress(50)

    # Create a new DataFrame for the output
    output_df = pd.DataFrame(columns=[
        "AREA", "PACKAGE_CODE", "AREA_DESCRIPTION", "AREA_NEW", "SERVICE_CLASS_NEW",
        "BASE_PO", "AREA_OFFER_ID", "BLOCKING_OFFER_ID", "SIMCARD_TYPE_OFFER",
        "PAM_TYPE", "PROMOTION_PLAN", "PROMOTION_PLAN_STARTDATE",
        "PROMOTION_PLAN_ENDDATE", "PRODUCT_SEGMENT_OFFER", "PRODUCT_ID",
        "SERVICE_CLASS_LEGACY", "FULFILLMENT_MODE"
    ])

    # Merge the two DataFrames based on AREA_GROUP
    merged_df = pd.merge(df2, df1, on="AREA_GROUP", how="left")
    progress_bar.progress(70)

    # Populate the output DataFrame from the merged DataFrame
    output_df["AREA"] = merged_df["AREACODE"].apply(lambda x: str(x).zfill(3))
    output_df["PACKAGE_CODE"] = merged_df["PROGRAM_CODE"]
    output_df["AREA_DESCRIPTION"] = merged_df["AREA_DESCRIPTION"]
    output_df["AREA_NEW"] = merged_df["AREA_NEW"]
    output_df["SERVICE_CLASS_NEW"] = merged_df["SC"]
    output_df["BASE_PO"] = merged_df["BASE_PO"]
    output_df["AREA_OFFER_ID"] = 200000300
    output_df["BLOCKING_OFFER_ID"] = 4444
    output_df["SIMCARD_TYPE_OFFER"] = 200090010
    output_df["PAM_TYPE"] = "DailyPAM"
    output_df["PROMOTION_PLAN"] = ""
    output_df["PROMOTION_PLAN_STARTDATE"] = ""
    output_df["PROMOTION_PLAN_ENDDATE"] = ""

    # Set PRODUCT_SEGMENT_OFFER with exception for SC = 8003
    output_df["PRODUCT_SEGMENT_OFFER"] = merged_df.apply(
    lambda row: 91100310 if row["SC"] in [8003, 8095, 8153] else row["OfferSegment"], axis=1
    )

    output_df["PRODUCT_ID"] = "IM3"
    output_df["SERVICE_CLASS_LEGACY"] = merged_df["SC_LEGACY"]
    output_df["FULFILLMENT_MODE"] = "D"

    # Save the output DataFrame to a BytesIO object (for download)
    progress_bar.progress(90)
    output_file = BytesIO()
    output_df.to_excel(output_file, index=False, engine='openpyxl')
    output_file.seek(0)
    progress_bar.progress(100)
    return output_file

# Streamlit UI
def main():
    st.title("Starterpack Area Details DMP Processing")

    st.subheader("Upload the Programcode and Area Reference Excel files")
    file1 = st.file_uploader("Choose the programcode file (.xls or .xlsx)", type=["xls", "xlsx"])
    file2 = st.file_uploader("Choose the area reference file (.xls or .xlsx)", type=["xls", "xlsx"])

    if file1 is not None and file2 is not None:
        st.write("Processing the files...")

        # Initialize progress bar
        progress_bar = st.progress(0)

        # Process the files and get the output file
        output_file = process_files(file1, file2, progress_bar)

        # Display completion flag
        st.success("Processing completed!")

        # Allow the user to download the output file
        st.download_button(
            label="Download Output File",
            data=output_file,
            file_name="output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
