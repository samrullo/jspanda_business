import os
import pandas as pd

folder = r"C:\Users\amrul\Documents\japan_sweets_business\analysis_20200822"
raw_file = r"japansweet_missing_analysis_20200822.xlsx"
dinara_raw_file = r"dinara_side_japansweet.xlsx"

cols = ['name', 'quantity', 'missing_quantity', 'price_per_unit', 'total_sum']
numeric_cols = ['quantity', 'missing_quantity', 'price_per_unit', 'total_sum']
zakaz_df = pd.read_excel(os.path.join(folder, raw_file), sheet_name="zakaz")
sklad_df = pd.read_excel(os.path.join(folder, raw_file), sheet_name="sklad")
dinara_raw_df = pd.read_excel(os.path.join(folder, dinara_raw_file), sheet_name="20200807_20200730")
dinara_raw_df['missing_quantity'] = 0
dinara_df = dinara_raw_df[cols].copy()

df = pd.concat([zakaz_df[cols], sklad_df[cols]])
print(f"zakaz {len(zakaz_df)}, sklad {len(sklad_df)}, df {len(df)}, dinara_df {len(dinara_df)}")
print(f"unique number of names : {df['name'].nunique()}")

for col in numeric_cols:
    df[col] = df[col].fillna("")
    df[col] = df[col].apply(str).apply(lambda x: x.replace(',', '.')).apply(str.strip)
    df.loc[df[col] == "", col] = 0
    df[col] = pd.to_numeric(df[col])

for col in numeric_cols:
    dinara_df[col] = dinara_df[col].fillna("")
    dinara_df[col] = dinara_df[col].apply(str).apply(lambda x: x.replace(',', '.')).apply(str.strip)
    dinara_df.loc[dinara_df[col] == "", col] = 0
    dinara_df[col] = pd.to_numeric(dinara_df[col])

print(f"dinara total - sabina total : {dinara_df.total_sum.sum() - df.total_sum.sum()}")

missing_df=df.loc[df.missing_quantity!=0].copy()
missing_df['missing_total_sum']=missing_df['price_per_unit']*missing_df['missing_quantity']
print(f"missing total sum : {missing_df['missing_total_sum'].sum()}")

missing_df.to_excel(os.path.join(folder,"missing_total_sum.xlsx"))