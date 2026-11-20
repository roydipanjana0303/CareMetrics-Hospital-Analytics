import pandas as pd
import numpy as np

def standardize_columns(df):
    """Maps common hospital/healthcare CSV column variations to CareMetrics standard names."""
    df = df.copy()

    column_mapping = {
        'hospital': 'Hospital_Name',
        'hospital name': 'Hospital_Name',
        'medical condition': 'Medical_Condition',
        'condition': 'Medical_Condition',
        'billing amount': 'Treatment_Cost',
        'treatment cost': 'Treatment_Cost',
        'cost': 'Treatment_Cost',
        'date of admission': 'Admission_Date',
        'admission date': 'Admission_Date',
        'admission type': 'Admission_Type',
        'patient id': 'Patient_ID',
        'name': 'Patient_ID',
        'stay days': 'Stay_Days',
        'discharge date': 'Discharge Date',
    }
    df = df.rename(
        columns={
            column: column_mapping.get(
                ' '.join(str(column).strip().casefold().replace('_', ' ').split()),
                str(column).strip(),
            )
            for column in df.columns
        }
    )
    
    # Create fallback Patient_ID if missing
    if 'Patient_ID' not in df.columns:
        df.insert(0, 'Patient_ID', [f'P{1000 + i}' for i in range(len(df))])
        
    # Calculate Stay_Days from Discharge Date if available, else generate default
    if 'Stay_Days' not in df.columns:
        if 'Discharge Date' in df.columns and 'Admission_Date' in df.columns:
            adm = pd.to_datetime(df['Admission_Date'], errors='coerce')
            dis = pd.to_datetime(df['Discharge Date'], errors='coerce')
            df['Stay_Days'] = (dis - adm).dt.days.fillna(3).clip(lower=1)
        else:
            df['Stay_Days'] = 3

    return df

def inspect_raw_data(df):
    """Returns basic health metrics of the raw uploaded dataset."""
    total_rows, total_cols = df.shape
    missing_values = df.isnull().sum().to_dict()
    total_missing = int(df.isnull().sum().sum())
    duplicate_count = int(df.duplicated().sum())
    
    return {
        "rows": total_rows,
        "cols": total_cols,
        "missing_by_col": missing_values,
        "total_missing": total_missing,
        "duplicates": duplicate_count
    }

def clean_dataset(df):
    """Standardizes columns and applies Pandas cleaning techniques."""
    cleaned_df = standardize_columns(df)
    
    # 1. Remove duplicate patient records
    cleaned_df = cleaned_df.drop_duplicates()
    
    # 2. Drop rows where critical columns are missing
    critical_cols = [col for col in ['Patient_ID', 'Hospital_Name', 'Medical_Condition'] if col in cleaned_df.columns]
    cleaned_df = cleaned_df.dropna(subset=critical_cols)
    
    # 3. Fill missing numerical values using median/mean
    if 'Age' in cleaned_df.columns:
        cleaned_df['Age'] = pd.to_numeric(cleaned_df['Age'], errors='coerce')
        cleaned_df['Age'] = cleaned_df['Age'].fillna(cleaned_df['Age'].median())
    if 'Treatment_Cost' in cleaned_df.columns:
        cleaned_df['Treatment_Cost'] = pd.to_numeric(cleaned_df['Treatment_Cost'], errors='coerce')
        cleaned_df['Treatment_Cost'] = cleaned_df['Treatment_Cost'].fillna(cleaned_df['Treatment_Cost'].mean())
        
    # 4. Fill missing categorical values with 'Unknown'
    if 'Gender' in cleaned_df.columns:
        cleaned_df['Gender'] = cleaned_df['Gender'].fillna('Unknown')
    if 'Hospital_Name' not in cleaned_df.columns:
        cleaned_df['Hospital_Name'] = 'General Hospital'
    if 'Medical_Condition' not in cleaned_df.columns:
        cleaned_df['Medical_Condition'] = 'Unknown'
        
    # 5. Parse dates and sort chronologically
    if 'Admission_Date' in cleaned_df.columns:
        cleaned_df['Admission_Date'] = pd.to_datetime(cleaned_df['Admission_Date'], errors='coerce')
        cleaned_df = cleaned_df.dropna(subset=['Admission_Date'])
        cleaned_df = cleaned_df.sort_values(by='Admission_Date', ascending=True)
        
    cleaned_df = cleaned_df.reset_index(drop=True)
    return cleaned_df

def demonstrate_indexing_and_slicing(df):
    """Demonstrates loc, iloc, slicing, filtering, and sorting."""
    first_ten = df.iloc[0:10]
    
    if 'Treatment_Cost' in df.columns:
        sorted_cost = df.sort_values(by='Treatment_Cost', ascending=False)
        cols_to_show = [c for c in ['Patient_ID', 'Hospital_Name', 'Medical_Condition', 'Treatment_Cost'] if c in df.columns]
        high_cost_patients = sorted_cost.loc[:, cols_to_show].head(5)
    else:
        high_cost_patients = first_ten
        
    return first_ten, high_cost_patients

def compute_analytics(df):
    """Computes summary statistics and grouped aggregations."""
    df = standardize_columns(df)
    if 'Hospital_Name' not in df.columns:
        df['Hospital_Name'] = 'General Hospital'
    if 'Medical_Condition' not in df.columns:
        df['Medical_Condition'] = 'Unknown'

    summary_stats = df.describe().round(2)

    agg_columns = {}
    if 'Patient_ID' in df.columns:
        agg_columns['Total_Patients'] = ('Patient_ID', 'count')
    if 'Treatment_Cost' in df.columns:
        agg_columns['Avg_Treatment_Cost'] = ('Treatment_Cost', 'mean')
        agg_columns['Total_Treatment_Cost'] = ('Treatment_Cost', 'sum')
    if 'Stay_Days' in df.columns:
        agg_columns['Avg_Stay_Days'] = ('Stay_Days', 'mean')

    if not agg_columns:
        hospital_summary = pd.DataFrame({'Hospital_Name': df['Hospital_Name'].unique()})
    else:
        hospital_summary = df.groupby('Hospital_Name').agg(**agg_columns).round(2).reset_index()

    condition_counts = df['Medical_Condition'].value_counts().reset_index()
    condition_counts.columns = ['Medical_Condition', 'Patient_Count']
    
    return summary_stats, hospital_summary, condition_counts