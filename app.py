import streamlit as st
from pathlib import Path
from utils.data_manager import load_products, load_sales, money
from utils.analytics import kpis, monthly_sales
from utils.charts import revenue_line
from utils.shoe_art import shoe_data_uri, shoe_image_src, safe

ROOT = Path(__file__).parent
st.set_page_config(page_title="OwnSHoes | Shoe Sales Analytics", page_icon="👟", layout="wide", initial_sidebar_state="collapsed")
css = (ROOT / "styles/main.css").read_text(encoding="utf-8")
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

PAGES = [("Home", "⌂"), ("Shoe Showcase", "👟"), ("Sales Analytics", "↗"), ("Products", "◇"), ("Inventory", "▦"), ("Reports & Downloads", "↓")]
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Top-only navigation — no duplicate Streamlit sidebar navigation.
brand, nav = st.columns([1.25, 4.75], vertical_alignment="center")
with brand:
    st.markdown("<div class='sv-brand'><span class='sv-mark'>SV</span><span>OWNSHOES</span></div><div class='sv-brand-sub'>SHOES / STYLE / PERFORMANCE</div>", unsafe_allow_html=True)
with nav:
    navcols = st.columns([0.78, 1.05, 1.35, 0.82, 0.82, 1.55], vertical_alignment="center")
    for i, (label, glyph) in enumerate(PAGES):
        with navcols[i]:
            if st.button(f"{glyph}  {label}", key=f"top_{label}", use_container_width=True, type="primary" if st.session_state.page == label else "secondary"):
                st.session_state.page = label
                st.rerun()
st.markdown("<div class='sv-top-rule'></div>", unsafe_allow_html=True)

products = load_products()
sales = load_sales()
page = st.session_state.page

if page == "Shoe Showcase":
    st.markdown("<div class='sv-season'>OWNSHOES / THE ROTATION</div><div class='sv-showcase-title'>FIND YOUR<br><span>PACE.</span></div><div class='sv-showcase-copy'>Performance silhouettes. Everyday essentials. A closer look at the shoes moving the numbers.</div>", unsafe_allow_html=True)
    # Use a real product photo for the hero, not the old black/orange placeholder image.
    hero_photo = "https://images.puma.com/image/upload/f_auto,q_auto,b_rgb:fafafa,w_1200,h_1200/global/397194/01/sv01/fnd/PHL/fmt/png/BLKTOP-RIDER-CNY-Casual-shoes"
    st.markdown("<div class='sv-showcase-hero'><div><div class='sv-season'>THE FOOTWEAR EXPERIENCE</div><div class='sv-showcase-promo'>STEP INTO<br><span>THE NEXT.</span></div><p>Discover the collection. Track every sale. Find your next best seller.</p><div class='sv-promo-pills'><span>NEW SEASON</span><span>PERFORMANCE SERIES</span><span>OWNSHOES SELECT</span></div></div><div class='sv-promo-shoe'><img src='" + hero_photo + "' alt='PUMA Blacktop Rider sneakers'></div></div>", unsafe_allow_html=True)
    st.markdown("<div class='sv-section-head'><div><div class='sv-season'>THE ROTATION</div><h2>20 styles. Find your pair.</h2></div><div class='sv-muted-note'>AUTOMATIC SHOE CAROUSEL · REAL PRODUCT PHOTOS + SHOE IMAGES</div></div>", unsafe_allow_html=True)
    # Put the user's real linked product photos first; never lead with the generated SVG illustrations.
    photo_ids = {f"SV{i:03d}" for i in range(21, 31)}
    photo_products = products[products["product_id"].astype(str).isin(photo_ids)]
    other_products = products[~products["product_id"].astype(str).isin(photo_ids)].sort_values("stock", ascending=False)
    ordered_products = __import__("pandas").concat([photo_products, other_products], ignore_index=True)
    shoe_items = [row for _, row in ordered_products.iterrows()]
    while len(shoe_items) < 20 and shoe_items:
        shoe_items += shoe_items[:max(1, min(len(shoe_items), 20-len(shoe_items)))]
    shoe_items = shoe_items[:20]
    shoe_cards = []
    for idx, item in enumerate(shoe_items):
        image_data = shoe_image_src(item.get("product_id", ""), item.get("name", ""), idx)
        shoe_cards.append(f"<div class='sv-marquee-card'><div class='sv-marquee-img'><img src='{image_data}' alt='{safe(item['name'])} product photo'></div><div class='sv-marquee-num'>STYLE {idx+1:02d}</div><div class='sv-marquee-name'>{safe(item['name'])}</div><div class='sv-product-meta'>{safe(item['brand'])} · {safe(item['color'])}</div><div class='sv-marquee-price'>{money(item['price'])}</div></div>")
    cards_html = ''.join(shoe_cards)
    st.markdown("<div class='sv-marquee-wrap'><div class='sv-marquee-track'>" + cards_html + cards_html + "</div></div>", unsafe_allow_html=True)
    st.caption("Real product photos from the linked shoe listings appear first in the carousel.")
elif page == "Home":
    k = kpis(sales)
    left, right = st.columns([1.12, 0.88], gap="large", vertical_alignment="center")
    with left:
        st.markdown("<div class='sv-season'>THE NEW SEASON  /  OWNSHOES EDITION</div><div class='sv-hero-title'>STEP INTO<br><span>YOUR EDGE.</span></div><div class='sv-hero-copy'>A sharper view of every sale. Explore your best-selling styles, track inventory, and turn shoe-store data into your next move.</div>", unsafe_allow_html=True)
        st.markdown("<div class='sv-hero-actions'>BUILT FOR PERFORMANCE <span>✳</span> MADE FOR MOMENTUM</div>", unsafe_allow_html=True)
        if st.button("EXPLORE SALES  ↗", key="hero_sales", type="primary"):
            st.session_state.page = "Sales Analytics"
            st.rerun()
    with right:
        st.markdown("<div class='sv-shoe-stage'><div class='sv-shoe-stage-label'>OWNSHOES SELECT <span>01 / 03</span></div>", unsafe_allow_html=True)
        st.image("https://images.puma.com/image/upload/f_auto,q_auto,b_rgb:fafafa,w_1200,h_1200/global/397194/01/sv01/fnd/PHL/fmt/png/BLKTOP-RIDER-CNY-Casual-shoes", use_container_width=True)
        st.markdown("<div class='sv-image-caption'><span>ENGINEERED FOR EVERYDAY MOMENTUM</span><span>NEW SEASON</span></div></div>", unsafe_allow_html=True)

    st.markdown("<div class='sv-section-head'><div><div class='sv-season'>STORE SNAPSHOT</div><h2>Numbers that move.</h2></div><div class='sv-muted-note'>LIVE FROM YOUR LOCAL SALES FILE</div></div>", unsafe_allow_html=True)
    cols = st.columns(4, gap="medium")
    for col, (label, value, note) in zip(cols, [
        ("TOTAL REVENUE", money(k["Revenue"]), "Gross sales value"),
        ("TOTAL PROFIT", money(k["Profit"]), "Estimated profit"),
        ("UNITS SOLD", f'{k["Units Sold"]:,}', "Across all products"),
        ("TOTAL ORDERS", f'{k["Orders"]:,}', "Recorded transactions"),
    ]):
        with col:
            st.markdown(f"<div class='sv-stat'><div class='sv-stat-label'>{label}</div><div class='sv-stat-value'>{value}</div><div class='sv-stat-note'>{note}</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='sv-section-head'><div><div class='sv-season'>THE ROTATION</div><h2>Featured footwear.</h2></div><div class='sv-muted-note'>A FEW STORE FAVOURITES</div></div>", unsafe_allow_html=True)
    photo_ids = {f"SV{i:03d}" for i in range(21, 31)}
    featured = products[products["product_id"].astype(str).isin(photo_ids)].head(3)
    if len(featured) < 3:
        remaining = products[~products["product_id"].astype(str).isin(photo_ids)].sort_values("stock", ascending=False)
        featured = __import__("pandas").concat([featured, remaining.head(3-len(featured))])
    cards = st.columns(3, gap="medium")
    for col, (_, p), idx in zip(cards, featured.iterrows(), range(3)):
        with col:
            art = shoe_image_src(p.get("product_id", ""), p.get("name", ""), idx)
            st.markdown(f"<div class='sv-product-card'><div class='sv-product-art'><img src='{art}' alt='{safe(p['name'])} shoe'><span class='sv-tag'>{safe(str(p['category']).upper())}</span><span class='sv-product-index'>0{idx+1}</span></div><div class='sv-product-info'><div class='sv-product-name'>{safe(p['name'])}</div><div class='sv-product-meta'>{safe(p['brand'])} · {safe(p['color'])}</div><div class='sv-product-bottom'><strong>{money(p['price'])}</strong><span>{int(p['stock'])} IN STOCK</span></div></div></div>", unsafe_allow_html=True)
    lower_left, lower_right = st.columns([1.2, 1], gap="large")
    with lower_left:
        st.markdown("### Revenue, over time")
        st.plotly_chart(revenue_line(monthly_sales(sales)), use_container_width=True)
    with lower_right:
        st.markdown("### Recent orders")
        recent = sales.sort_values("date", ascending=False)[["date", "product_name", "quantity", "revenue"]].head(6).copy()
        recent["date"] = recent["date"].dt.strftime("%d %b %Y")
        st.dataframe(recent, hide_index=True, use_container_width=True)

elif page == "Sales Analytics":
    from views.sales_analytics import render
    render()
elif page == "Products":
    from views.products import render
    render()
elif page == "Inventory":
    from views.inventory import render
    render()
elif page == "Reports & Downloads":
    from views.reports import render
    render()
