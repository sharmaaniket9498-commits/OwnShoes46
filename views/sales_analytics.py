import streamlit as st
import pandas as pd
from datetime import date, timedelta
from utils.data_manager import load_sales, load_products, money
from utils.analytics import filtered_sales, kpis, monthly_sales, category_sales
from utils.charts import revenue_line, revenue_profit, category_bar

def render():
    st.title("Sales Performance Overview")
    st.caption("Explore revenue, profit and product category performance.")
    sales=load_sales(); products=load_products()
    c1,c2,c3=st.columns([1,1,1])
    start=c1.date_input("From",value=(date.today()-timedelta(days=330)))
    end=c2.date_input("To",value=date.today())
    categories=["All"]+sorted(sales["category"].dropna().unique().tolist())
    brands=["All"]+sorted(sales["brand"].dropna().unique().tolist())
    category=c3.selectbox("Category",categories)
    brand=st.selectbox("Brand",brands)
    df=filtered_sales(sales,start,end,category,brand)
    k=kpis(df)
    cols=st.columns(4)
    for col,(label,value) in zip(cols,[("TOTAL REVENUE",money(k["Revenue"])),("TOTAL PROFIT",money(k["Profit"])),("UNITS SOLD",f'{k["Units Sold"]:,}'),("AVG ORDER VALUE",money(k["Average Order Value"]))]):
        col.metric(label,value)
    monthly=monthly_sales(df); cats=category_sales(df)
    left,right=st.columns(2)
    with left:
        st.markdown("### Monthly Revenue Trend")
        st.plotly_chart(revenue_line(monthly),use_container_width=True)
        st.download_button("Download revenue chart (HTML)",monthly.to_csv(index=False).encode(),file_name="monthly_revenue.csv",mime="text/csv")
    with right:
        st.markdown("### Revenue & Profit")
        st.plotly_chart(revenue_profit(monthly),use_container_width=True)
    st.markdown("### Category Performance")
    st.plotly_chart(category_bar(cats,"revenue"),use_container_width=True)
    st.markdown("### Recent transactions")
    st.dataframe(df.sort_values("date",ascending=False)[["date","product_name","brand","category","quantity","revenue","profit"]].head(15),hide_index=True,use_container_width=True)
    if not df.empty:
        best=df.groupby("product_name")["revenue"].sum().sort_values(ascending=False)
        st.success(f"Top revenue product in this selection: {best.index[0]} ({money(best.iloc[0])}).")
    else:
        st.warning("No sales match these filters.")
