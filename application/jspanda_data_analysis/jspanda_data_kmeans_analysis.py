import os
import logging
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np

folder = r"C:\Users\amrul\Documents\japan_sweets_business\data_analysis"

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger()

engine = create_engine('mysql://samrullo:18Aranid@jspandabusiness.crrz64gldft9.ap-south-1.rds.amazonaws.com/jspanda?charset=utf8')

query = "SELECT * FROM `jspanda_orders`"
orders_df = pd.read_sql(query, engine)
orders_df['year'] = orders_df['date'].map(lambda x: x.year)
logger.info(f"there are total of {len(orders_df)} records")
logger.info(f"{orders_df['name'].nunique()} unique names")

product_names = orders_df['name'].unique()
tfidf = TfidfVectorizer()
product_names_csr_mat = tfidf.fit_transform(product_names)
logger.info(f"some feature names : {tfidf.get_feature_names()[:10]}")

# now let's cluster product names to clusters of 2000
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline

svd = TruncatedSVD(n_components=100)
kmeans = KMeans(n_clusters=2000)
pipeline = make_pipeline(svd, kmeans)
logger.info(f"finished making pipeline with TruncatedSVD and KMeans")

pipeline.fit(product_names_csr_mat)
logger.info(f"finished fitting the pipeline to product names sparce matrix")

labels = pipeline.predict(product_names_csr_mat)
clustered_orders_df = pd.DataFrame({"product_name": product_names, "cluster": labels})
clustered_orders_df.to_excel(os.path.join(folder, "jspanda_order_product_names_cluster.xlsx"))

# let's use alphabet only
from nltk.tokenize import word_tokenize

tokenized_product_names = [word_tokenize(name.lower()) for name in product_names]
alpha_tokenized_product_names = [[token for token in tokenized_product_name if token.isalpha()] for tokenized_product_name in tokenized_product_names]
alphanumeric_product_names = [" ".join(alpha_tokenized_product_name) for alpha_tokenized_product_name in alpha_tokenized_product_names]
logger.info(f"product_names : {len(product_names)}, alphanumerid product_names : {len(alphanumeric_product_names)}")

tfidf = TfidfVectorizer()
alphanumeric_product_names_csr_mat = tfidf.fit_transform(alphanumeric_product_names)
logger.info(f"some feature names : {tfidf.get_feature_names()[:10]}")
