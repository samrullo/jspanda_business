import logging
import datetime
import pandas as pd
import numpy as np

def prepare_jspanda_order(raw_df,adate):
    try:
        logging.info("About to load {}".format(adate))
        raw_df = raw_df.loc[np.logical_not(raw_df['quantity'].isnull())]
        logging.info(f" raw_df length : {len(raw_df)}, order_sum total : {raw_df['order_sum'].sum()}")
        all_data_list.append(raw_df)
        all_data_dict[sheet_name] = raw_df
        logging.info("Successfully loaded sheet : {}".format(sheet_name))
    except Exception as e:
        logging.info(f"{sheet_name} had some errors, so it will be skipped")
        print(e)
        pass
