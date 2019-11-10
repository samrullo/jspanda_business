import os
import datetime
import pandas as pd
import numpy as np
import logging
import re

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__file__)

folder = r'C:\Users\amrul\Documents\programming\japansweet'
file = r'japansweet_orders_raw_data_from_google.xlsx'
seven_cols = ['name', 'quantity', 'order_sum', 'price', 'selling_price_per_unit', 'remainder', 'ordered_by', 'notes', 'something_else']
nine_cols = ['product_name', 'quantity', 'order_sum', 'cost', 'price', 'remainder', 'ordered_by', 'notes', 'something_else', 'extra1', 'extra2']

xl = pd.ExcelFile(os.path.join(folder, file))
sheet_names = xl.sheet_names
logger.info("Sheet names : {}".format(sheet_names))
all_data_list = []
all_data_dict = {}
for sheet_name in sheet_names:
    if re.search("Заказы", sheet_name) or re.search("Заказ", sheet_name):
        try:
            logger.info("About to load {}".format(sheet_name))
            df = pd.read_excel(xl, sheetname=sheet_name, skiprows=[1], usecols=[i for i in range(8)], index_col=None)
            # df = pd.read_excel(os.path.join(folder, file), header=2, sheetname=sheet_name, usecols=[i for i in range(7)])
            df.columns = seven_cols[1:]
            df['name'] = df.index
            df.index = range(len(df))
            df = df.loc[np.logical_not(df['quantity'].isnull())]
            adate = sheet_name.split()[1]
            if len(adate) == 6:
                day = adate[:2]
                month = adate[2:4]
                year = adate[4:]
                adate = '20' + year + month + day
                logger.info("Adate is {}".format(adate))
                df['adate'] = adate
            elif len(adate) == 8:
                day = adate[:2]
                month = adate[2:4]
                year = adate[4:]
                adate = year + month + day
                logger.info("Adate is {}".format(adate))
                df['adate'] = adate
            logger.info(f"{sheet_name} df length : {len(df)}, order_sum total : {df['order_sum'].sum()}")
            all_data_list.append(df)
            all_data_dict[sheet_name] = df
            logger.info("Successfully loaded sheet : {}".format(sheet_name))
        except Exception as e:
            logging.info(f"{sheet_name} had some errors, so it will be skipped")
            print(e)
            pass

all_df = pd.concat(all_data_list)
all_df['order_sum'] = all_df['order_sum'].fillna(0)
all_df.loc[all_df['order_sum'].apply(lambda x: isinstance(x, str)), 'order_sum'] = 0
orders_df = all_df.loc[np.logical_not(all_df['name'].isnull())]
zakazi_df = orders_df.loc[np.logical_and(np.logical_not(orders_df['price'].isnull()), np.logical_not(orders_df['quantity'].isnull()))].copy()
zakazi_df['adate'] = pd.to_datetime(zakazi_df['adate'])
zakazi_df.sort_values('adate', ascending=False, inplace=True)

final_orders_df = zakazi_df[['adate'] + seven_cols]
final_orders_df.index = range(len(final_orders_df))
logger.info("Total number of records : {}".format(len(orders_df)))

logger.info("Will remove any record that doesn't have number in price column")
for i, row in final_orders_df.iterrows():
    try:
        final_orders_df.loc[i, 'price'] = float(row['price'])
    except Exception as e:
        logger.info(f"Exception when processing {i} price : {e}")
        final_orders_df.drop(i, inplace=True)

logger.info("Will remove any record that doesn't have number in quantity column")
for i, row in final_orders_df.iterrows():
    try:
        final_orders_df.loc[i, 'quantity'] = float(row['quantity'])
    except Exception as e:
        logger.info(f"Exception when processing {i} quantity : {e}")
        final_orders_df.drop(i, inplace=True)

final_orders_df.loc[final_orders_df['selling_price_per_unit'].isnull(), 'selling_price_per_unit'] = final_orders_df.loc[final_orders_df['selling_price_per_unit'].isnull(), 'price']
final_orders_df['selling_price_per_unit'] = final_orders_df['selling_price_per_unit'].fillna(0)
final_orders_df['selling_price_per_unit'] = final_orders_df['selling_price_per_unit'].apply(str).apply(lambda x: x.replace("total", ""))
final_orders_df['selling_price_per_unit'] = final_orders_df['selling_price_per_unit'].apply(str).apply(lambda x: x.replace("Итого", ""))
final_orders_df['selling_price_per_unit'] = final_orders_df['selling_price_per_unit'].apply(str).apply(lambda x: x.replace("$", ""))

for i, row in final_orders_df.iterrows():
    logging.info(f"Will convert selling price per unit to float for {i}")
    try:
        final_orders_df.loc[i, 'selling_price_per_unit'] = float(row['selling_price_per_unit'])
    except Exception as e:
        logging.info(e)
        final_orders_df.loc[i, 'selling_price_per_unit'] = row['price']

final_orders_df['selling_price_per_unit'] = pd.to_numeric(final_orders_df['selling_price_per_unit'])

final_orders_df.to_excel(os.path.join(folder, "jspanda_orders_20181210_to_20191101.xlsx"), index=False)
