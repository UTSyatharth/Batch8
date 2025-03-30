import pandas as pd
from collections import defaultdict, Counter
from itertools import tee

df = pd.read_csv("/Users/shrutisharma/PycharmProjects/Batch8/mypandasmodule/dataset2.csv")

# 1. Advanced Data Cleaning
# 1.1 Removing duplicate rows
df = df.drop_duplicates(keep="first")
print("1.1 After removing duplicates:")
print(df.head(10))

# 1.2 Standardizing product names
product_mapping = {"ProdA": "Product A", "Product A": "Product A", "ProdB": "Product B"}
df["Product"] = df["Product"].replace(product_mapping)
print("1.2 After fixing product typos:")
print(df.head(10))

#1.3 Validating numericals
df["Quantity"] = df["Quantity"].apply(lambda x: 1 if x < 0 else x)
df = df[df["Price"] >= 0]
print("1.3 After validating numericals:")
print(df.head(10))

# 1.4 Standardizing category names
df["Category"] = df["Category"].str.lower().replace({"electronics": "Electronics", "electrnics": "Electronics", "electronic": "Electronics"})
print("1.4 After fixing category inconsistencies:")
print(df.head(10))

# 1.5 Fill missing regions with the most common region per CustomerID
df["Region"] = df.groupby("CustomerID")["Region"].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else "Unknown"))
print("1.5 After imputing missing regions:")
print(df.head(10))

# 1.6 Creating IsPromo flag
df["IsPromo"] = df["PromoCode"].notna().astype(int)
print("1.6 After creating IsPromo flag:")
print(df.head(10))
#
#
#
#
# 2. Complex DateTime Operations
# 2.1 Converting all dates to UTC datetime
df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")

if df["OrderDate"].dt.tz is None:
    df["OrderDate"] = df["OrderDate"].dt.tz_localize("UTC")
else:
    df["OrderDate"] = df["OrderDate"].dt.tz_convert("UTC")

print("2.1 After converting dates to UTC:")
print(df.head(10))


# 2.2 Calculating order processing time
df["ReturnDate"] = df["OrderDate"] + pd.Timedelta(days=7)
print("2.2 After calculating return dates:")
print(df.head(10))

# 2.3 weekly sales trends for electronics vs home goods

return_rate = defaultdict(lambda: 0)

region_returns = df[df["ReturnFlag"] == 1].groupby("Region")["OrderID"].count() if "ReturnFlag" in df.columns else pd.Series()
region_orders = df.groupby("Region")["OrderID"].count()

for region in region_orders.index:
    return_rate[region] = region_returns.get(region, 0) / region_orders[region] if region in region_returns else 0

return_rate_df = pd.DataFrame(list(return_rate.items()), columns=["Region", "Return Rate"])

print("2.3 Return rates by region:")
print(return_rate_df)





# 3. Advanced Collections & Optimization
# 3.1 Buildong nested dictionary
customer_stats = df.groupby(["CustomerID", "Category"])["Price"].sum().unstack(fill_value=0)
customer_dict = {cid: {"total_spent": row.sum(), "favorite_category": row.idxmax()} for cid, row in customer_stats.iterrows()}
print("3.1 Customer spending and favorite category:")
print(customer_dict)

# 3.2 Tracking  return rates by region
return_rate = defaultdict(lambda: 0)
regionreturns = df[df["ReturnFlag"] == 1].groupby("Region")["OrderID"].count()
region_orders = df.groupby("Region")["OrderID"].count()
for region in region_orders.index:
    return_rate[region] = region_returns.get(region, 0) / region_orders[region]
print("3.2 Return rates by region:")
print(dict(return_rate))

# 3.3 most common promo code sequence
def generate_bigrams(promo_list):
    a, b = tee(promo_list)
    next(b, None)
    return list(zip(a, b))

df_sorted = df.sort_values(["CustomerID", "OrderDate"])
df_sorted["PromoCode"] = df_sorted["PromoCode"].fillna("None")
customer_promos = df_sorted.groupby("CustomerID")["PromoCode"].apply(list)
promo_sequences = Counter()
for promos in customer_promos:
    promo_sequences.update(generate_bigrams(promos))
most_common_sequence = promo_sequences.most_common(1)
print("3.3 Most common promo code sequence:")
print(most_common_sequence)

# 3.4 Optimizing memory usage
df["Quantity"] = pd.to_numeric(df["Quantity"], downcast="integer")
df["Price"] = pd.to_numeric(df["Price"], downcast="float")
print("3.4 After optimizing memory usage:")
print(df.info())

# 4.
# 4.1 UDF to flag "suspicious orders" (multiple returns + high value)
def is_suspicious(order):
    return order["ReturnFlag"] > 1 and order["Price"] > 500

df["SuspiciousOrder"] = df.apply(is_suspicious, axis=1)
print("4.1 After flagging suspicious orders:")
print(df.head(10))

# Save cleaned data
df.to_csv("/Users/shrutisharma/PycharmProjects/Batch8/mypandasmodule/dataset2.csv", index=False)


