import pandas as pd
import pathlib

def convert_to_proper_bool(df,bool_cols):
    for col in bool_cols:
        df[col]=df[col].fillna(0)
        df[col]=df[col].map(lambda _col : bool(int(_col)))
    return df

if __name__=="__main__":
    folder=pathlib.Path(r"C:\Users\amrul\programming\web_programming\jspanda_business\postgres_data\db_dumps\jspanda_db_dump_asof_20220415")
    file="shipment_weight.csv"
    df=pd.read_csv(folder/file)
    bool_cols=["is_paid"]
    df=convert_to_proper_bool(df,bool_cols)
    print(df[bool_cols].head().to_string())
    df.to_csv(folder/file,index=False)