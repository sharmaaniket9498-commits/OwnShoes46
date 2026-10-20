import pandas as pd

def filtered_sales(sales, start=None, end=None, category="All", brand="All"):
    df=sales.copy()
    if start is not None: df=df[df["date"].dt.date >= start]
    if end is not None: df=df[df["date"].dt.date <= end]
    if category!="All": df=df[df["category"]==category]
    if brand!="All": df=df[df["brand"]==brand]
    return df

def kpis(sales):
    revenue=float(sales["revenue"].sum()) if len(sales) else 0
    profit=float(sales["profit"].sum()) if len(sales) else 0
    units=int(sales["quantity"].sum()) if len(sales) else 0
    orders=int(sales["sale_id"].nunique()) if len(sales) else 0
    return {"Revenue":revenue,"Profit":profit,"Units Sold":units,"Orders":orders,"Average Order Value":revenue/orders if orders else 0}

def monthly_sales(sales):
    if sales.empty: return pd.DataFrame(columns=["Month","Revenue","Profit"])
    df=sales.copy()
    df["Month"]=df["date"].dt.to_period("M").dt.to_timestamp()
    return df.groupby("Month",as_index=False).agg(Revenue=("revenue","sum"),Profit=("profit","sum")).sort_values("Month")

def category_sales(sales):
    if sales.empty: return pd.DataFrame(columns=["category","revenue","profit","quantity"])
    return sales.groupby("category",as_index=False).agg(revenue=("revenue","sum"),profit=("profit","sum"),quantity=("quantity","sum")).sort_values("revenue",ascending=False)
