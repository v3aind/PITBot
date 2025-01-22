import pandas as pd
import streamlit as st
from io import BytesIO

# Function to handle the processing
def process_files(file1, file2):
    # Load the two Excel files into pandas DataFrames
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

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

    # Populate the output DataFrame from the merged DataFrame
    output_df["AREA"] = merged_df["AREACODE"].astype(str).apply(lambda x: x.zfill(3))  # Ensure leading zeros
    output_df["PACKAGE_CODE"] = merged_df["PROGRAM_CODE"]
    output_df["AREA_DESCRIPTION"] = merged_df["AREA_DESCRIPTION"]
    output_df["AREA_NEW"] = merged_df["AREA_NEW"]
    output_df["SERVICE_CLASS_NEW"] = merged_df["SC"]
    output_df["BASE_PO"] = merged_df["BASE_PO"]
    output_df["AREA_OFFER_ID"] = "200000300"
    output_df["BLOCKING_OFFER_ID"] = "4444"
    output_df["SIMCARD_TYPE_OFFER"] = "200090010"
    output_df["PAM_TYPE"] = "DailyPAM"
    output_df["PROMOTION_PLAN"] = ""
    output_df["PROMOTION_PLAN_STARTDATE"] = ""
    output_df["PROMOTION_PLAN_ENDDATE"] = ""
    output_df["PRODUCT_SEGMENT_OFFER"] = merged_df["OfferSegment"]
    output_df["PRODUCT_ID"] = "IM3"
    output_df["SERVICE_CLASS_LEGACY"] = ""
    output_df["FULFILLMENT_MODE"] = "D"

    # Save the output DataFrame to a BytesIO object (for download)
    output_file = BytesIO()
    output_df.to_excel(output_file, index=False)
    output_file.seek(0)
    return output_file

# Streamlit UI
def main():
    st.title("Starterpack Area Details DMP Processing")

    st.subheader("Upload the two Excel files")
    file1 = st.file_uploader("Choose the programcode file (programcode.xlsx)", type=["xlsx"])
    file2 = st.file_uploader("Choose the area reference file (arearef.xlsx)", type=["xlsx"])

    if file1 is not None and file2 is not None:
        st.write("Processing the files...")

        # Process the files and get the output file
        output_file = process_files(file1, file2)

        # Allow the user to download the output file
        st.download_button(
            label="Download Output File",
            data=output_file,
            file_name="output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
