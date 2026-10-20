import streamlit as st
import pandas as pd
from datetime import date, timedelta
from io import BytesIO
from utils.data_manager import load_products, load_sales, money
from utils.analytics import filtered_sales, kpis, monthly_sales, category_sales
from utils.charts import revenue_line, revenue_profit, category_bar

def make_pdf(sales, products):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    buf=BytesIO(); doc=SimpleDocTemplate(buf,pagesize=A4,rightMargin=32,leftMargin=32,topMargin=32,bottomMargin=32)
    styles=getSampleStyleSheet(); story=[]
    k=kpis(sales)
    story.append(Paragraph("OWNSHOES — Sales Summary Report",styles["Title"]))
    story.append(Paragraph(f"Generated {date.today().isoformat()}",styles["Normal"])); story.append(Spacer(1,16))
    data=[["Metric","Value"],["Total revenue",money(k["Revenue"])],["Total profit",money(k["Profit"])],["Units sold",str(k["Units Sold"])],["Orders",str(k["Orders"])],["Average order value",money(k["Average Order Value"])]]
    t=Table(data,colWidths=[230,220]); t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#ff3b1d")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.4,colors.grey),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.whitesmoke,colors.lightgrey]),("PADDING",(0,0),(-1,-1),8)])); story.append(t); story.append(Spacer(1,18))
    story.append(Paragraph("Top products by revenue",styles["Heading2"]))
    if not sales.empty:
        top=sales.groupby("product_name",as_index=False).agg(Revenue=("revenue","sum"),Units=("quantity","sum")).sort_values("Revenue",ascending=False).head(10)
        data=[["Product","Revenue","Units"]]+[[r["product_name"],money(r["Revenue"]),str(int(r["Units"]))] for _,r in top.iterrows()]
        t=Table(data,colWidths=[250,120,80]); t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#242a31")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.4,colors.grey),("PADDING",(0,0),(-1,-1),6)])); story.append(t)
    story.append(Spacer(1,16)); story.append(Paragraph(f"Products currently in catalogue: {len(products)}",styles["Normal"]))
    doc.build(story); buf.seek(0); return buf.getvalue()

def render():
    st.title("Reports & Downloads")
    st.caption("Export your current local data and generate a concise business report.")
    sales=load_sales(); products=load_products()
    a,b=st.columns(2)
    start=a.date_input("Report from",date.today()-timedelta(days=330))
    end=b.date_input("Report to",date.today())
    df=filtered_sales(sales,start,end)
    k=kpis(df)
    cols=st.columns(4)
    cols[0].metric("REVENUE",money(k["Revenue"]))
    cols[1].metric("PROFIT",money(k["Profit"]))
    cols[2].metric("UNITS SOLD",f'{k["Units Sold"]:,}')
    cols[3].metric("ORDERS",f'{k["Orders"]:,}')
    st.markdown("### Download centre")
    c1,c2,c3=st.columns(3)
    with c1:
        st.markdown("<div class='sv-panel'><span class='sv-tag'>CSV</span><h3>Sales data</h3><p style='color:#a3a8b0'>Transactions within selected dates.</p></div>",unsafe_allow_html=True)
        st.download_button("Download sales CSV",df.to_csv(index=False).encode("utf-8"),"ownshoes_sales.csv","text/csv",use_container_width=True)
    with c2:
        st.markdown("<div class='sv-panel'><span class='sv-tag'>CSV</span><h3>Product inventory</h3><p style='color:#a3a8b0'>Current catalogue and stock levels.</p></div>",unsafe_allow_html=True)
        st.download_button("Download products CSV",products.to_csv(index=False).encode("utf-8"),"ownshoes_products.csv","text/csv",use_container_width=True)
    with c3:
        st.markdown("<div class='sv-panel'><span class='sv-tag'>PDF</span><h3>Sales summary</h3><p style='color:#a3a8b0'>Key metrics and top products.</p></div>",unsafe_allow_html=True)
        st.download_button("Generate PDF report",make_pdf(df,products),"ownshoes_report.pdf","application/pdf",use_container_width=True)
    st.markdown("### Chart downloads")
    monthly=monthly_sales(df); cats=category_sales(df)
    st.download_button("Download monthly chart data (CSV)",monthly.to_csv(index=False).encode(),"monthly_revenue.csv","text/csv")
    st.download_button("Download category chart data (CSV)",cats.to_csv(index=False).encode(),"category_performance.csv","text/csv")
    st.markdown("### Simple charts — quick to understand")
    left, right = st.columns(2)
    with left:
        st.markdown("#### Monthly revenue")
        st.plotly_chart(revenue_line(monthly), use_container_width=True)
    with right:
        st.markdown("#### Sales by shoe category")
        st.plotly_chart(category_bar(cats), use_container_width=True)
    st.markdown("### Report preview")
    st.dataframe(df.sort_values("date",ascending=False)[["date","product_name","brand","quantity","revenue","profit"]].head(12),hide_index=True,use_container_width=True)
