import streamlit as st
import pandas as pd
from utils.data_manager import load_products, save_products, money
from utils.charts import stock_bar

def render():
    st.title("Inventory Control")
    st.caption("Monitor stock, update quantities and catch low-stock products.")
    products=load_products()
    low=products[products["stock"]<=products["reorder_level"]]
    out=products[products["stock"]<=0]
    cols=st.columns(4)
    cols[0].metric("TOTAL STOCK",f'{int(products["stock"].sum()):,}')
    cols[1].metric("LOW STOCK",len(low))
    cols[2].metric("OUT OF STOCK",len(out))
    cols[3].metric("CATEGORIES",products["category"].nunique())
    left,right=st.columns([1.2,1])
    with left:
        st.markdown("### Stock by product")
        st.plotly_chart(stock_bar(products),use_container_width=True)
    with right:
        st.markdown("### Low-stock alerts")
        if low.empty: st.success("All products are above their reorder level.")
        else:
            for _,p in low.sort_values("stock").iterrows():
                st.markdown(f"<div class='sv-panel' style='margin-bottom:8px;padding:10px'><span style='color:#ff3b1d;font-weight:800'>● {p['name']}</span><br><small>{p['brand']} · only {p['stock']} units left (reorder at {p['reorder_level']})</small></div>",unsafe_allow_html=True)
    st.markdown("### Update stock")
    options={f"{r['product_id']} · {r['name']}":r["product_id"] for _,r in products.iterrows()}
    with st.form("stock_update"):
        x,y=st.columns(2)
        selected=x.selectbox("Product",list(options))
        amount=y.number_input("Quantity to add / remove",min_value=1,value=5,step=1)
        action=st.radio("Action",["Add stock","Remove stock"],horizontal=True)
        submit=st.form_submit_button("Update inventory")
        if submit:
            df=load_products(); idx=df.index[df["product_id"].astype(str)==str(options[selected])][0]
            new=int(df.loc[idx,"stock"])+(int(amount) if action=="Add stock" else -int(amount))
            if new<0: st.error("Stock cannot become negative.")
            else:
                df.loc[idx,"stock"]=new; save_products(df); st.success("Inventory updated."); st.rerun()
    st.markdown("### Full inventory")
    st.dataframe(products[["product_id","name","brand","category","price","stock","reorder_level"]].sort_values("stock"),hide_index=True,use_container_width=True)
    st.download_button("Download inventory CSV",products.to_csv(index=False).encode("utf-8"),"inventory.csv","text/csv")
