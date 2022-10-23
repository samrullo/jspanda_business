from curses import raw
import os
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import logging
from config import Config


class GoogleSpreadsheetToDataframe:
    def __init__(self, google_credentials_folder=Config.GOOGLE_CREDENTIALS_FOLDER, google_credentials_file=Config.GOOGLE_CREDENTIALS_FILE):
        logging.info(f"Will initialize jspanda gspread to dataframe instance")
        self.google_credentials_folder = google_credentials_folder
        self.google_credentials_file = google_credentials_file
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        # self.google_credentials_folder = r"C:\Users\amrul\Documents\japan_sweets_business\google_service_key"
        # self.google_credentials_file = "jspanda-abb0ef8b0971.json"
        self.credentials = self.get_credentials(self.google_credentials_folder, self.google_credentials_file, self.scope)
        self.gc = gspread.authorize(self.credentials)

    def get_credentials(self, google_credentials_folder, google_credentials_file, scope):
        logging.info("will get credentials for gspread")
        return ServiceAccountCredentials.from_json_keyfile_name(os.path.join(google_credentials_folder, google_credentials_file), scope)  # Your json file here

    def get_worksheet_as_dataframe(self, google_doc_name, sheet_name):
        logging.info("Will get google doc worksheet as dataframe")
        # wkbook = gc.open("Japansweetproject_new.xlsx")
        wkbook = self.gc.open(google_doc_name)
        wksheet = wkbook.worksheet(sheet_name)
        data = wksheet.get_all_values()
        header = data.pop(0)
        return pd.DataFrame(data, columns=header)

    def prepare_insertable_jspanda_orders_dataframe(self, raw_df, adate,utf8endcode=True):
        logging.info("Will prepare jspanda dataframe insertable into database")
        db_cols = ['date', 'name', 'quantity', 'price', 'selling_price_per_unit', 'total_cost', 'order_sum', 'ordered_by', 'extra_notes', 'is_paid']
        cols = ['name', 'quantity', 'order_sum', 'price', 'selling_price_per_unit', 'remainder', 'ordered_by', 'extra_notes', 'total']
        raw_df.columns = cols
        raw_df = raw_df.loc[raw_df['quantity'] != ""]
        new_df = pd.DataFrame(columns=db_cols)
        new_df['date'] = adate
        new_df['name'] = raw_df['name']
        new_df['quantity'] = pd.to_numeric(raw_df['quantity'])

        # in google docs period is comma
        raw_df['price'] = raw_df['price'].apply(lambda x: x.replace(",", "."))
        raw_df['selling_price_per_unit'] = raw_df['selling_price_per_unit'].apply(lambda x: x.replace(",", "."))

        # sometimes price or selling price may have string total
        raw_df['selling_price_per_unit'] = raw_df['selling_price_per_unit'].apply(lambda x: x.replace("total", "")).apply(lambda x: x.strip())

        # we want to convert selling price to int
        for i,row in raw_df.iterrows():
            try:
                raw_df.loc[i,'selling_price_per_unit']=int(row["selling_price_per_unit"])
            except Exception as e:
                logging.info(f"failed parsing to int : {e}")
                raw_df.loc[i,'selling_price_per_unit']=0

        # if selling price is not a number set it to empty
        for i, row in raw_df.iterrows():
            selling_price = row['selling_price_per_unit']
            selling_price_tokens = selling_price.split(" ")
            if len(selling_price_tokens) > 1:
                raw_df.loc[i, 'selling_price_per_unit'] = row['price']

        # now will attempt to get price and selling_price as numeric
        new_df['price'] = pd.to_numeric(raw_df['price'])
        new_df['selling_price_per_unit'] = pd.to_numeric(raw_df['selling_price_per_unit'])

        # there are cases where selling_price is yet not decided
        new_df.loc[new_df['selling_price_per_unit'].isnull(), 'selling_price_per_unit'] = new_df.loc[new_df['selling_price_per_unit'].isnull(), 'price']

        # for all other cases set price,selling price to zero
        new_df['price'] = new_df['price'].fillna(0)
        new_df['selling_price_per_unit'] = new_df['selling_price_per_unit'].fillna(0)

        # if contains cyrillic characters better convert charset to utf
        if utf8endcode:
            new_df['ordered_by'] = raw_df['ordered_by'].map(lambda _ordered_by: _ordered_by.decode("utf-8") if isinstance(_ordered_by,bytes) else _ordered_by)
            new_df['extra_notes'] = raw_df['extra_notes'].str.encode("utf-8")
            new_df['name'] = new_df['name'].str.encode("utf-8")

        # let's calculate total costs and order_sums
        new_df['total_cost'] = new_df['quantity'] * new_df['price']
        new_df['order_sum'] = new_df['quantity'] * new_df['selling_price_per_unit']
        new_df['date'] = adate
        new_df['is_paid'] = False
        new_df.index = [i for i in range(len(new_df))]
        return new_df
