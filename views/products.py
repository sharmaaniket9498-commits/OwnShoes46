import streamlit as st
import pandas as pd
from utils.data_manager import load_products, save_products, load_sales, record_sale, money, PRODUCT_COLUMNS
from utils.shoe_art import shoe_data_uri, shoe_image_src, safe

def render():
    st.title("Product Collection")
    st.caption("Manage your catalogue with a compact, searchable product view.")
    products=load_products()
    a,b,c=st.columns(3)
    a.metric("Products",len(products)); b.metric("Brands",products["brand"].nunique()); c.metric("Categories",products["category"].nunique())
    with st.expander("＋ Add a product",expanded=False):
        with st.form("add_product",clear_on_submit=True):
            x1,x2,x3=st.columns(3)
            pid=x1.text_input("Product ID",placeholder="SV013")
            name=x2.text_input("Product name")
            brand=x3.text_input("Brand")
            x4,x5,x6=st.columns(3)
            category=x4.selectbox("Category",["Sneakers","Running Shoes","Casual Shoes","Sports Shoes","Boots","Formal Shoes"])
            price=x5.number_input("Price (₹)",min_value=1,value=4999,step=100)
            stock=x6.number_input("Initial stock",min_value=0,value=10,step=1)
            color=st.text_input("Color",value="Black")
            submit=st.form_submit_button("Add Product")
            if submit:
                if not pid.strip() or not name.strip() or not brand.strip():
                    st.error("Product ID, name and brand are required.")
                elif pid in products["product_id"].astype(str).tolist():
                    st.error("That product ID already exists.")
                else:
                    row={"product_id":pid.strip(),"name":name.strip(),"brand":brand.strip(),"category":category,"price":int(price),"stock":int(stock),"reorder_level":6,"color":color}
                    products=pd.concat([products,pd.DataFrame([row])],ignore_index=True); save_products(products)
                    st.success("Product added."); st.rerun()
    f1,f2=st.columns([2,1])
    query=f1.text_input("Search products",placeholder="Search by name, brand or ID")
    cats=["All"]+sorted(products["category"].unique().tolist())
    cat=f2.selectbox("Category filter",cats)
    view=products.copy()
    if query: view=view[view.astype(str).apply(lambda r:r.str.contains(query,case=False,na=False)).any(axis=1)]
    if cat!="All": view=view[view["category"]==cat]
    st.markdown(f"### {len(view)} products")
    cols=st.columns(3)
    for i,(_,p) in enumerate(view.iterrows()):
        with cols[i%3]:
            status="LOW STOCK" if p["stock"]<=p["reorder_level"] else "IN STOCK"
            art = shoe_image_src(p.get("product_id", ""), p.get("name", ""), i)
            st.markdown(f"<div class='sv-product-card sv-catalog-card'><div class='sv-product-art sv-catalog-art'><img src='{art}' alt='{safe(p['name'])} shoe'><span class='sv-tag'>{status}</span><span class='sv-product-index'>{i+1:02d}</span></div><div class='sv-product-info'><div class='sv-product-name'>{safe(p['name'])}</div><div class='sv-product-meta'>{safe(p['brand'])} · {safe(p['category'])} · {safe(p['color'])}</div><div class='sv-product-bottom'><strong>{money(p['price'])}</strong><span>{int(p['stock'])} IN STOCK</span></div><small>Product ID: {safe(p['product_id'])}</small></div></div>",unsafe_allow_html=True)
            with st.expander(f"Manage {p['product_id']}"):
                with st.form(f"edit_{p['product_id']}"):
                    new_name=st.text_input("Name",p["name"])
                    new_brand=st.text_input("Brand",p["brand"])
                    new_price=st.number_input("Price",min_value=1,value=int(p["price"]),step=100)
                    new_stock=st.number_input("Stock",min_value=0,value=int(p["stock"]),step=1)
                    new_cat=st.selectbox("Category",["Sneakers","Running Shoes","Casual Shoes","Sports Shoes","Boots","Formal Shoes"],index=["Sneakers","Running Shoes","Casual Shoes","Sports Shoes","Boots","Formal Shoes"].index(p["category"]) if p["category"] in ["Sneakers","Running Shoes","Casual Shoes","Sports Shoes","Boots","Formal Shoes"] else 0)
                    save=st.form_submit_button("Save changes")
                    if save:
                        current=load_products(); ix=current.index[current["product_id"].astype(str)==str(p["product_id"])][0]
                        current.loc[ix,["name","brand","price","stock","category"]]=[new_name,new_brand,int(new_price),int(new_stock),new_cat]
                        save_products(current); st.success("Product updated."); st.rerun()
                if st.button("Delete product",key=f"del_{p['product_id']}"):
                    current=load_products()
                    current=current[current["product_id"].astype(str)!=str(p["product_id"])]
                    save_products(current); st.warning("Product deleted."); st.rerun()
    st.markdown("### Record a sale")
    product_options={f"{r['product_id']} · {r['name']} (stock {r['stock']})":r["product_id"] for _,r in products.iterrows()}
    with st.form("record_sale"):
        selected=st.selectbox("Product",list(product_options))
        qty=st.number_input("Quantity",min_value=1,value=1,step=1)
        ok=st.form_submit_button("Record sale")
        if ok:
            success,msg=record_sale(product_options[selected],qty)
            (st.success if success else st.error)(msg)
            if success: st.rerun()
