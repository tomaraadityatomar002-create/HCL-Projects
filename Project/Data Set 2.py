import numpy as np
import pandas as pd

# 1. Load the dataset and treat all placeholder strings as missing values (NaN)
missing_placeholders = ['unknown', '?', 'N/A', 'n/a', 'na', '']
df = pd.read_csv('House_Price_Prediction_Extra_Rough.csv', na_values=missing_placeholders)


# 2. Clean numeric columns
numeric_cols = [
    'Area',
    'Bedrooms',
    'Bathrooms',
    'Floors',
    'YearBuilt',
    'Price',
]

for col in numeric_cols:
  df[col] = df[col].astype(str).str.replace(',', '').str.strip()
  df[col] = pd.to_numeric(df[col], errors='coerce')
  
  # Remove rows where Area is less than 500 or greater than 5000
df = df[(df['Area'] >= 500) & (df['Area'] <= 5000)]

# 3. Clean text columns (remove extra spaces and convert to lowercase)
text_cols = ['Location', 'Condition', 'Garage']
for col in text_cols:
  df[col] = df[col].astype(str).str.strip().str.lower()

# 4. Fix typos and abbreviations in 'Location'
location_fixes = {
    'dtown': 'Downtown',
    'dt': 'Downtown',
    'downtown': 'Downtown',
    'urb': 'Urban',
    'urban': 'Urban',
    'sub': 'Suburban',
    'suburb': 'Suburban',
    'suburban': 'Suburban',
    'rur': 'Rural',
    'rural': 'Rural',
    'nan': np.nan,
}
df['Location'] = df['Location'].replace(location_fixes)

# 5. Fix typos and abbreviations in 'Condition'
condition_fixes = {
    'exc': 'Excellent',
    'exellent': 'Excellent',
    'excellent': 'Excellent',
    'gud': 'Good',
    'good': 'Good',
    'f': 'Fair',
    'fair': 'Fair',
    'pr': 'Poor',
    'poor': 'Poor',
    'nan': np.nan,
}
df['Condition'] = df['Condition'].replace(condition_fixes)

# 6. Standardize 'Garage' into 'Yes' or 'No'
garage_fixes = {
    '1': 'Yes',
    'y': 'Yes',
    'yes': 'Yes',
    '0': 'No',
    'n': 'No',
    'no': 'No',
    'nan': np.nan,
}
df['Garage'] = df['Garage'].replace(garage_fixes)

# 7. Handle missing values
# Remove rows where 'Price' is missing
df = df.dropna(subset=['Price'])

# Fill missing numbers with the median (middle value)
for col in ['Area', 'Bedrooms', 'Bathrooms', 'Floors', 'YearBuilt']:
  df[col] = df[col].fillna(df[col].median())

# Fill blank spaces in Location, Condition, and Garage using .mode()[0]
df['Location'] = df['Location'].fillna(df['Location'].mode()[0])
df['Condition'] = df['Condition'].fillna(df['Condition'].mode()[0])
df['Garage'] = df['Garage'].fillna(df['Garage'].mode()[0])

# 8. Convert whole-number columns to integers
int_cols = ['Bedrooms', 'Bathrooms', 'Floors', 'YearBuilt']
for col in int_cols:
  df[col] = df[col].astype(int)

# 9. Verify that 0 blank spaces remain
print('Remaining missing values per column:')
print(df.isnull().sum())

# 10. Save the cleaned dataset
df.to_csv('cleaned_housing_data.csv', index=False)
