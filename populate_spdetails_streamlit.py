import pandas as pd
import streamlit as st
from io import BytesIO
import openpyxl  # Add openpyxl import for Excel file handling

# Function to handle the processing
def process_files(file1, file2):
    try:
        # Load the two Excel files into pandas DataFrames
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)

        # Check for required columns in both files
        required_columns_file1 = ["AREA_GROUP", "AREACODE", "PROGRAM_CODE", "AREA_DESCRIPTION", "AREA_NEW", "SC", "BASE_PO", "OfferSegment"]
        required_columns_file2 = ["AREA_GROUP"]

        if not all(col in df1.columns for col in required_columns_file1):
            raise ValueError(f"File 1 is missing one or more required columns: {required_columns_file1}")
        if not all(col in df2.columns for col in required_columns_file2):
            raise ValueError(f"File 2 is missing one or more required columns: {required_columns_file2}")

        # Create a new DataFrame for the output
        output_df = pd.Da
