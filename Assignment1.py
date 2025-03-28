import pandas as pd

df = pd.read_csv("/Users/shrutisharma/PycharmProjects/Batch8/mypandasmodule/dataset1.csv")



# 1.1 category with the highest average rating
highest_avg_rating = df.groupby("Category")["Rating"].mean().idxmax()
print("Category with highest average rating:", highest_avg_rating)

# 1.2 total stock available for each category
total_stock_available_per_category = df.groupby("Category")["Stock"].sum()
print("Total stock available per category:\n", total_stock_available_per_category)




# 2.1 Creating new column 'Final_Price'
df["Final_price"]=df["Price"]-(df["Price"]*df["Discount"]/100)
print(df.head(10))


# 2.2 top 3 most discounted products
top_discounted=(df.nlargest(3, "Discount"))
print("Top 3 discounted Products:\n", top_discounted)







# 3.1 supplier with the highest average price of products
highest_avg_price_supplier = df.groupby("Supplier")["Price"].mean().idxmax()
print("Supplier with highest average price:", highest_avg_price_supplier)

# 3.2 total number of unique suppliers
unique_suppliers = df["Supplier"].nunique()
print("Total unique suppliers:", unique_suppliers)






from collections import Counter

# 4.1 Count occurrences of each category
category_counts = Counter(df["Category"])
print("Category occurrences:", category_counts)





