from pathlib import Path
import pandas as pd
from datetime import date, timedelta
import random

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
PRODUCTS_FILE = DATA / "products.csv"
SALES_FILE = DATA / "sales.csv"

PRODUCT_COLUMNS = ["product_id","name","brand","category","price","stock","reorder_level","color"]
SALES_COLUMNS = ["sale_id","date","product_id","product_name","brand","category","quantity","unit_price","revenue","unit_cost","profit"]

def _seed_data():
    DATA.mkdir(exist_ok=True)
    if not PRODUCTS_FILE.exists():
        products = [
            ["SV001","Air Motion 270","Nike","Sneakers",8999,42,8,"White / Orange"],
            ["SV002","Ultraboost 22","Adidas","Running Shoes",10999,28,8,"Black"],
            ["SV003","Velocity Nitro 3","Puma","Running Shoes",7499,36,8,"White / Orange"],
            ["SV004","Go Walk Flex","Skechers","Casual Shoes",5999,18,6,"Grey"],
            ["SV005","Classic Leather","Reebok","Casual Shoes",5499,24,6,"White"],
            ["SV006","Forum Low","Adidas","Sneakers",6999,12,6,"Cream"],
            ["SV007","Air Force 1","Nike","Sneakers",9999,5,8,"White"],
            ["SV008","Suede Classic","Puma","Casual Shoes",4999,8,6,"Red"],
            ["SV009","Floatride Energy","Reebok","Running Shoes",6499,15,6,"Black / White"],
            ["SV010","Lite Racer","Adidas","Sports Shoes",3999,52,10,"Black"],
            ["SV011","Track Runner","Skechers","Sports Shoes",4599,31,8,"Navy"],
            ["SV013","Red Tape Urban Flex","Red Tape","Casual Shoes",4299,26,7,"White / Red"],
            ["SV014","Red Tape Athleisure","Red Tape","Sneakers",3799,21,7,"Black / White"],
            ["SV015","Campus Nitro Run","Campus","Running Shoes",2899,33,8,"Blue / White"],
            ["SV016","Woodland Trekker","Woodland","Boots",6999,14,5,"Brown"],
            ["SV017","Bata Formal Edge","Bata","Formal Shoes",3299,19,6,"Black"],
            ["SV018","Asian Street Pro","ASIAN","Sneakers",2499,29,7,"Grey / Orange"],
            ["SV019","Sparx Active","Sparx","Sports Shoes",1899,37,9,"Navy"],
            ["SV020","Puma Street Rider","Puma","Sneakers",5999,17,6,"White / Orange"],
            ["SV021","Blacktop Rider CNY","PUMA","Casual Shoes",6499,16,6,"Black / Red"],
            ["SV022","Chuck Taylor All Star","Converse","Sneakers",4999,20,6,"Black / White"],
            ["SV023","Smash Pop","PUMA","Sneakers",3499,24,7,"White"],
            ["SV024","Smash Comfort","PUMA","Sneakers",3999,18,6,"White / Black"],
            ["SV025","H-Street Lightweight OG","PUMA","Sneakers",4999,14,5,"Black / White"],
            ["SV026","OwnSHoes Street Pair 06","OwnSHoes","Sneakers",2999,12,5,"Multi-colour"],
            ["SV027","OwnSHoes Street Pair 07","OwnSHoes","Sneakers",3199,15,5,"Multi-colour"],
            ["SV028","OwnSHoes Street Pair 08","OwnSHoes","Sneakers",2799,17,5,"Multi-colour"],
            ["SV029","OwnSHoes Street Pair 09","OwnSHoes","Sneakers",3299,11,5,"Multi-colour"],
            ["SV030","OwnSHoes Street Pair 10","OwnSHoes","Sneakers",2899,19,5,"Multi-colour"],
        ]
        pd.DataFrame(products, columns=PRODUCT_COLUMNS).to_csv(PRODUCTS_FILE,index=False)
    # Upgrade existing local catalogues without overwriting user edits.
    extra_products = [
        ["SV013","Red Tape Urban Flex","Red Tape","Casual Shoes",4299,26,7,"White / Red"],
        ["SV014","Red Tape Athleisure","Red Tape","Sneakers",3799,21,7,"Black / White"],
        ["SV015","Campus Nitro Run","Campus","Running Shoes",2899,33,8,"Blue / White"],
        ["SV016","Woodland Trekker","Woodland","Boots",6999,14,5,"Brown"],
        ["SV017","Bata Formal Edge","Bata","Formal Shoes",3299,19,6,"Black"],
        ["SV018","Asian Street Pro","ASIAN","Sneakers",2499,29,7,"Grey / Orange"],
        ["SV019","Sparx Active","Sparx","Sports Shoes",1899,37,9,"Navy"],
        ["SV020","Puma Street Rider","Puma","Sneakers",5999,17,6,"White / Orange"],
        ["SV021","Blacktop Rider CNY","PUMA","Casual Shoes",6499,16,6,"Black / Red"],
        ["SV022","Chuck Taylor All Star","Converse","Sneakers",4999,20,6,"Black / White"],
        ["SV023","Smash Pop","PUMA","Sneakers",3499,24,7,"White"],
        ["SV024","Smash Comfort","PUMA","Sneakers",3999,18,6,"White / Black"],
        ["SV025","H-Street Lightweight OG","PUMA","Sneakers",4999,14,5,"Black / White"],
        ["SV026","OwnSHoes Street Pair 06","OwnSHoes","Sneakers",2999,12,5,"Multi-colour"],
        ["SV027","OwnSHoes Street Pair 07","OwnSHoes","Sneakers",3199,15,5,"Multi-colour"],
        ["SV028","OwnSHoes Street Pair 08","OwnSHoes","Sneakers",2799,17,5,"Multi-colour"],
        ["SV029","OwnSHoes Street Pair 09","OwnSHoes","Sneakers",3299,11,5,"Multi-colour"],
        ["SV030","OwnSHoes Street Pair 10","OwnSHoes","Sneakers",2899,19,5,"Multi-colour"],
    ]
    existing = pd.read_csv(PRODUCTS_FILE)
    # Remove sandal/chapal items from older local catalogues as requested.
    existing = existing[existing["category"].astype(str).str.lower().ne("sandals")].copy()
    existing = existing[~existing["name"].astype(str).str.contains(r"sandal|chapal|slipper", case=False, na=False)].copy()
    known_ids = set(existing["product_id"].astype(str))
    missing = [row for row in extra_products if row[0] not in known_ids]
    if missing:
        existing = pd.concat([existing, pd.DataFrame(missing, columns=PRODUCT_COLUMNS)], ignore_index=True)
    existing[PRODUCT_COLUMNS].to_csv(PRODUCTS_FILE, index=False)
    if not SALES_FILE.exists():
        products = pd.read_csv(PRODUCTS_FILE)
        random.seed(22)
        rows=[]
        start = date.today() - timedelta(days=330)
        for i in range(240):
            p = products.iloc[random.randrange(len(products))]
            d = start + timedelta(days=random.randrange(331))
            qty = random.randint(1,4)
            price = int(p["price"])
            cost = int(price * random.uniform(.53,.72))
            rows.append([f"S{i+1:04d}",d.isoformat(),p["product_id"],p["name"],p["brand"],p["category"],qty,price,qty*price,cost,qty*(price-cost)])
        pd.DataFrame(rows,columns=SALES_COLUMNS).to_csv(SALES_FILE,index=False)

def load_products():
    _seed_data()
    df=pd.read_csv(PRODUCTS_FILE)
    for c in ["price","stock","reorder_level"]:
        df[c]=pd.to_numeric(df[c],errors="coerce").fillna(0).astype(int)
    return df

def save_products(df):
    df[PRODUCT_COLUMNS].to_csv(PRODUCTS_FILE,index=False)

def load_sales():
    _seed_data()
    df=pd.read_csv(SALES_FILE)
    if "category" in df.columns:
        df = df[df["category"].astype(str).str.lower().ne("sandals")].copy()
        df = df[~df["product_name"].astype(str).str.contains(r"sandal|chapal|slipper", case=False, na=False)].copy()
    df["date"]=pd.to_datetime(df["date"],errors="coerce")
    for c in ["quantity","unit_price","revenue","unit_cost","profit"]:
        df[c]=pd.to_numeric(df[c],errors="coerce").fillna(0)
    return df

def save_sales(df):
    out=df.copy()
    out["date"]=pd.to_datetime(out["date"]).dt.strftime("%Y-%m-%d")
    out[SALES_COLUMNS].to_csv(SALES_FILE,index=False)

def record_sale(product_id, quantity):
    products=load_products()
    matches=products.index[products["product_id"].astype(str)==str(product_id)].tolist()
    if not matches: return False, "Product not found."
    idx=matches[0]
    if int(products.loc[idx,"stock"]) < int(quantity): return False, "Not enough stock available."
    product=products.loc[idx]
    sales=load_sales()
    price=int(product["price"]); cost=int(price*.62); qty=int(quantity)
    sale_num=len(sales)+1
    new={"sale_id":f"S{sale_num:04d}","date":pd.Timestamp.today().normalize(),"product_id":product["product_id"],"product_name":product["name"],"brand":product["brand"],"category":product["category"],"quantity":qty,"unit_price":price,"revenue":qty*price,"unit_cost":cost,"profit":qty*(price-cost)}
    sales=pd.concat([sales,pd.DataFrame([new])],ignore_index=True)
    products.loc[idx,"stock"]=int(products.loc[idx,"stock"])-qty
    save_products(products); save_sales(sales)
    return True, f"Sale recorded: {qty} × {product['name']}."

def money(n):
    return "₹ " + f"{float(n):,.0f}"
