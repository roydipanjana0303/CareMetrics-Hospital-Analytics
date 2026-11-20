import pandas as pd
import numpy as np

np.random.seed(42)
n_rows = 200

hospitals = ['City Care Hospital', 'Apollo General', 'Sunrise Medical Center', 'Metro Health']
conditions = ['Hypertension', 'Diabetes', 'Viral Fever', 'Fracture', 'Asthma', 'Cardiac Arrest']
genders = ['Male', 'Female', 'Other']
admission_types = ['Emergency', 'Urgent', 'Elective']

dates = pd.date_range(start='2025-01-01', end='2025-12-31', periods=n_rows)

data = {
    'Patient_ID': [f'P{1000 + i}' for i in range(n_rows)],
    'Admission_Date': np.random.choice(dates, n_rows),
    'Hospital_Name': np.random.choice(hospitals, n_rows),
    'Age': np.random.randint(5, 85, n_rows).astype(float),
    'Gender': np.random.choice(genders, n_rows, p=[0.48, 0.49, 0.03]),
    'Medical_Condition': np.random.choice(conditions, n_rows),
    'Admission_Type': np.random.choice(admission_types, n_rows),
    'Stay_Days': np.random.randint(1, 15, n_rows),
    'Treatment_Cost': np.round(np.random.uniform(5000, 150000, n_rows), 2)
}

df = pd.DataFrame(data)

# Introduce realistic dirty data (NaNs and duplicates) for preprocessing demonstration
df.loc[np.random.choice(df.index, 12, replace=False), 'Age'] = np.nan
df.loc[np.random.choice(df.index, 8, replace=False), 'Treatment_Cost'] = np.nan
df.loc[np.random.choice(df.index, 6, replace=False), 'Gender'] = np.nan

# Append 5 duplicate rows
df = pd.concat([df, df.iloc[:5]], ignore_index=True)

df.to_csv('sample_hospital_data.csv', index=False)
print("Generated 'sample_hospital_data.csv' with 205 rows (including NaNs and duplicates).")