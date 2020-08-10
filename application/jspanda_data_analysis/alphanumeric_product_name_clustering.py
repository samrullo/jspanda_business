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
orders_df['month'] = orders_df['date'].map(lambda x: x.month)
orders_df['profit'] = orders_df['order_sum'] - orders_df['total_cost']
logger.info(f"there are total of {len(orders_df)} records")
logger.info(f"{orders_df['name'].nunique()} unique names")

product_names = orders_df['name'].tolist()

# let's use alphabet only
from nltk.tokenize import word_tokenize

tokenized_product_names = [word_tokenize(name.lower()) for name in product_names]
alpha_tokenized_product_names = [[token for token in tokenized_product_name if token.isalpha()] for tokenized_product_name in tokenized_product_names]
alphanumeric_product_names = [" ".join(alpha_tokenized_product_name) for alpha_tokenized_product_name in alpha_tokenized_product_names]
logger.info(f"product_names : {len(product_names)}, alphanumerid product_names : {len(alphanumeric_product_names)}")

tfidf = TfidfVectorizer()
product_names_csr_mat = tfidf.fit_transform(alphanumeric_product_names)
logger.info(f"some feature names : {tfidf.get_feature_names()[:10]}")

# now let's cluster product names to clusters of 2000
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline

svd = TruncatedSVD(n_components=100)
kmeans = KMeans(n_clusters=100)
pipeline = make_pipeline(svd, kmeans)
logger.info(f"finished making pipeline with TruncatedSVD and KMeans")

pipeline.fit(product_names_csr_mat)
logger.info(f"finished fitting the pipeline to product names sparce matrix")

labels = pipeline.predict(product_names_csr_mat)
clustered_orders_df = pd.DataFrame({"product_name": product_names, "cluster": labels})
cluster_grp_df = clustered_orders_df.groupby('cluster').count()
cluster_grp_df = cluster_grp_df.sort_values('product_name', ascending=False)
clustered_orders_df.to_excel(os.path.join(folder, "jspanda_order_product_names_cluster.xlsx"), index=False)

orders_df['cluster'] = labels
orders_df.to_excel(os.path.join(folder, "orders_with_cluster_labels.xlsx"), index=False)

# now I will try to plot cluster box plot
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style('darkgrid')
g = sns.catplot(x='cluster', y='quantity', data=orders_df, kind='box')
g.fig.suptitle("Cluster quantity box plot")
g.fig.set_size_inches(18, 7)
plt.show()
filename = "quantity_by_cluster_box_plot.jpg"
g.fig.savefig(os.path.join(folder, filename), format="jpg")

g = sns.catplot(x='cluster', data=orders_df, kind='count')
g.fig.suptitle("Cluster counts")
g.fig.set_size_inches(18, 7)
plt.show()
filename = "cluster_count_plot.jpg"
g.fig.savefig(os.path.join(folder, filename), format="jpg")

by_quantity_df = orders_df.groupby(['name', 'year']).sum()[['quantity', 'total_cost', 'order_sum', 'profit']]
by_quantity_df = by_quantity_df.sort_values('quantity', ascending=False)
by_quantity_df['name'] = by_quantity_df.index.get_level_values('name')
by_quantity_df['year'] = by_quantity_df.index.get_level_values('year')
by_quantity_top_df = by_quantity_df.loc[by_quantity_df['quantity'] > 50].copy()
g = sns.catplot(x='name', y='quantity', data=by_quantity_top_df, hue='year', kind='bar')
g.fig.suptitle("Total sold quantity by products by year")
g.fig.set_size_inches(18, 7)
plt.show()
filename = "total_quantity_by_products_by_year.jpg"
g.fig.savefig(os.path.join(folder, filename), format="jpg")

g = sns.catplot(x='year', y='price', data=orders_df, kind='box')
g.fig.suptitle("Price box plot by year")
g.fig.set_size_inches(18, 7)
plt.show()
filename = "price_by_year_box_plot.jpg"
g.fig.savefig(os.path.join(folder, filename), format="jpg")

g = sns.catplot(x='cluster', y='price', data=orders_df, kind='box')
g.fig.suptitle("Price box plot by cluster")
g.fig.set_size_inches(18, 7)
plt.show()
filename = "price_by_cluster_box_plot.jpg"
g.fig.savefig(os.path.join(folder, filename), format="jpg")

# let's plot some charts by clusters
clusters_with_more_than_50_items = cluster_grp_df.loc[cluster_grp_df['product_name'] > 50].index.tolist()
orders_clust_df = orders_df.loc[orders_df['cluster'].isin(clusters_with_more_than_50_items)]

g = sns.catplot(x='cluster', y='quantity', data=orders_clust_df, kind='box', hue='year')
g.fig.suptitle("Quantity sold by clusters")
g.fig.set_size_inches(18, 7)
plt.show()
filename = "quantity_by_cluster_by_year_box_plot.jpg"
g.fig.savefig(os.path.join(folder, filename), format="jpg")

# orders grouped by cluster, year sum of quantity and order_sum
orders_clust_grp_df = orders_clust_df.groupby(['cluster', 'year']).sum()[['quantity', 'total_cost', 'order_sum', 'profit']]
orders_clust_grp_df['cluster'] = orders_clust_grp_df.index.get_level_values('cluster')
orders_clust_grp_df['year'] = orders_clust_grp_df.index.get_level_values('year')
g = sns.catplot(x='cluster', y='quantity', data=orders_clust_grp_df, hue='year', kind='bar')
g.fig.suptitle("Total quantities by cluster by years")
g.fig.set_size_inches(18, 7)
plt.show()
filename = "aggregated_quantity_by_cluster_box_plot.jpg"
g.fig.savefig(os.path.join(folder, filename), format="jpg")

g = sns.catplot(x='cluster', y='total_cost', data=orders_clust_grp_df, hue='year', kind='bar')
g.fig.suptitle("Total cost by cluster by years")
g.fig.set_size_inches(18, 7)
plt.show()
filename = "total_cost_by_year_bar_plot.jpg"
g.fig.savefig(os.path.join(folder, filename), format="jpg")

g = sns.catplot(x='cluster', y='profit', data=orders_clust_grp_df, hue='year', kind='bar')
g.fig.suptitle("Total profit by cluster by years")
g.fig.set_size_inches(18, 7)
plt.show()
filename = "total_profit_by_cluster_bar_plot.jpg"
g.fig.savefig(os.path.join(folder, filename), format="jpg")

# let's see 2019
orders_2019_df = orders_clust_df.loc[orders_clust_df['year'] == 2019].copy()
orders_grp_2019_df = orders_2019_df.groupby('month').sum()[['total_cost', 'order_sum', 'profit']]
orders_grp_2019_df['month'] = orders_grp_2019_df.index
g = sns.catplot(x='month', y='order_sum', data=orders_grp_2019_df, kind='bar')
g.fig.suptitle("Order sum by monthes of 2019")
plt.show()

# I want to order 2019 orders by month. Then order in descending order by profit. then save to sheets
writer = pd.ExcelWriter(os.path.join(folder, "order_2019_by_month.xlsx"), engine="xlsxwriter")

for month in orders_2019_df['month'].tolist():
    orders_one_month_df = orders_2019_df.loc[orders_2019_df['month'] == month].copy()
    orders_one_month_df.sort_values('order_sum', ascending=False, inplace=True)
    total_order_sum = orders_one_month_df['order_sum'].sum()
    orders_one_month_df['order_sum_pct'] = (orders_one_month_df['order_sum'] / total_order_sum) * 100
    orders_one_month_df['ordur_sum_pct_cum'] = orders_one_month_df['order_sum_pct'].cumsum()
    orders_one_month_df.to_excel(writer, sheet_name=f"2019-{month}", index=False)

logger.info(f"finished saving 2019 orders by month to seperate sheets")
