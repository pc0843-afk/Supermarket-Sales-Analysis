from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE = Path(__file__).resolve().parent
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(BASE / "supermarket_sales.csv")
df.columns = df.columns.str.strip()
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df = df.dropna(subset=["Sales"])

# KPIs
kpis = pd.DataFrame({
    "Metric": ["Total Sales", "Average Sale", "Average Rating", "Transactions"],
    "Value": [df.Sales.sum(), df.Sales.mean(), df.Rating.mean(), len(df)]
})
kpis.to_csv(OUT / "kpi_summary.csv", index=False)

# Grouped analyses
product_sales = df.groupby("Product_line", as_index=False).Sales.sum().sort_values("Sales", ascending=False)
branch_sales = df.groupby(["Branch","City"], as_index=False).Sales.sum().sort_values("Sales", ascending=False)
payment_sales = df.groupby("Payment", as_index=False).Sales.sum().sort_values("Sales", ascending=False)
gender_sales = df.groupby("Gender", as_index=False).Sales.sum()

product_sales.to_csv(OUT/"product_line_sales.csv", index=False)
branch_sales.to_csv(OUT/"branch_sales.csv", index=False)
payment_sales.to_csv(OUT/"payment_sales.csv", index=False)
gender_sales.to_csv(OUT/"gender_sales.csv", index=False)

sns.set_theme(style="whitegrid")
for x, y, title, filename in [
    ("Product_line","Sales","Sales by Product Line","sales_by_product_line.png"),
    ("Branch","Sales","Sales by Branch","sales_by_branch.png"),
    ("Payment","Sales","Sales by Payment Method","sales_by_payment_method.png")
]:
    plt.figure(figsize=(9,5))
    if x == "Product_line":
        sns.barplot(data=product_sales, x=y, y=x)
    else:
        source = branch_sales if x == "Branch" else payment_sales
        sns.barplot(data=source, x=x, y=y)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(OUT/filename, dpi=180)
    plt.close()

top_product = product_sales.iloc[0]
top_branch = branch_sales.iloc[0]
top_payment = payment_sales.iloc[0]
(OUT/"insights.txt").write_text(
    f"Total sales: {df.Sales.sum():.2f}\n"
    f"Average transaction: {df.Sales.mean():.2f}\n"
    f"Average rating: {df.Rating.mean():.2f}\n"
    f"Top product line: {top_product.Product_line}\n"
    f"Top branch: {top_branch.Branch} - {top_branch.City}\n"
    f"Top payment method: {top_payment.Payment}\n",
    encoding="utf-8"
)
print("Analysis completed. Results are in outputs/.")
