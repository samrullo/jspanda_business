import os
import logging
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
import pandas as pd
import numpy as np
from application.jspanda_data_analysis.utils import get_jspanda_engine, get_jspanda_orders_one_year, init_logging

init_logging(level=logging.INFO)
folder = r"C:\Users\amrul\Documents\japan_sweets_business\data_analysis"

engine = get_jspanda_engine()

orders_df = get_jspanda_orders_one_year(2021, engine)
logging.info(f"there are total of {len(orders_df)} records")
logging.info(f"{orders_df['name'].nunique()} unique names")

product_names = orders_df['name'].tolist()

# let's use alphabet only
from nltk.tokenize import word_tokenize

tokenized_product_names = [word_tokenize(name.lower()) for name in product_names]
alpha_tokenized_product_names = [[token for token in tokenized_product_name if token.isalpha()] for tokenized_product_name in tokenized_product_names]
alphanumeric_product_names = [" ".join(alpha_tokenized_product_name) for alpha_tokenized_product_name in alpha_tokenized_product_names]
logging.info(f"product_names : {len(product_names)}, alphanumeric product_names : {len(alphanumeric_product_names)}")

tfidf = TfidfVectorizer()
product_names_csr_mat = tfidf.fit_transform(alphanumeric_product_names)
logging.info(f"some feature names : {tfidf.get_feature_names()[:10]}")

nmf_model = NMF(n_components=10)
kmeans = KMeans(n_clusters=10)
pipeline = make_pipeline(nmf_model, kmeans)

pipeline.fit(product_names_csr_mat)
labels = pipeline.predict(product_names_csr_mat)
