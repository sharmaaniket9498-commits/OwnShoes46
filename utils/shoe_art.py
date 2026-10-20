from pathlib import Path
import html

ROOT = Path(__file__).resolve().parents[1]

# Real shoe product-photo URLs. No generated shoe illustrations are used in the UI.
REAL_SHOE_IMAGES = {
    "SV021": "https://images.puma.com/image/upload/f_auto,q_auto,b_rgb:fafafa,w_2000,h_2000/global/397194/01/sv01/fnd/PHL/fmt/png/BLKTOP-RIDER-CNY-Casual-shoes",
    "SV022": "https://converse.static.n7.io/media/catalog/product/m/9/m9160c_a_107x1-web.jpg",
    "SV023": "https://images.puma.com/image/upload/f_auto,q_auto,b_rgb:fafafa,w_750,h_750/global/397128/02/fnd/IND/fmt/png/Smash-Pop-Men%27s-Sneakers",
    "SV024": "https://images.puma.com/image/upload/f_auto,q_auto,b_rgb:fafafa,w_750,h_750/global/400357/02/sv01/fnd/IND/fmt/png/Smash-Comfort-Sneakers",
    "SV025": "https://images.puma.com/image/upload/f_auto,q_auto,b_rgb:fafafa,w_750,h_750/global/403692/05/sv01/fnd/IND/fmt/png/H-Street-Lightweight-OG-Sneakers",
    "SV026": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcRchlbrx0cNNxHPV-MXQBrBeytVezDFXcvsPu9IC-Cq1yy0J2H4VCW29VchLa7yrlLO-XbvP1Qrg4AOwp_dw9I5G9e7YTFXARHCgGsyRDYWPoULiVAZwFgKwg",
    "SV027": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcToWRMWJAQJZ-1-AGdJep1wyM7IMY4j5oxpAg4jYbXucS4Z-OjxM9wh-olI7m9wR6NNivhqWLYmvLLgjlL9em371gvwJhgF5vNNKzz_EJ_RtRLXU2p24uZhzH0",
    "SV028": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcThoS4__vWC8JAbodVn21tvZLCD5vHdLW6p3eCAZJqoyDSyHU2JjW3tDjz3XHJUh5QYUx6RjZN3nj-ahIIlLW0U17GtJeaqWF9iNqlGlRl2GqCEG87YYoCW",
    "SV029": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcSIqVCJFHzCIpqzoqORBU9QsDdOzOsW_-Vtq75-MpYwdu280hBjXMQcR_l5zaFi2zFOvuAFrEyBcTNp7CJw8iVZob6WKV1HMpNsW3wD0_a6VIqTaGTvbW00NQ",
    "SV030": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcQ10_3DYxSXZNPxmT2_d7itEPWXalbN7h6HweeBnYim7T-847YTcjddh-yM8h80hEomfbZdX72a0GHrXh81YzT8Nwy5qsL9",
}
PHOTO_URLS = list(REAL_SHOE_IMAGES.values())

def safe(value):
    return html.escape(str(value), quote=True)

def shoe_image_src(product_id="", name="", fallback=0):
    # Use real product photos for every card; never fall back to drawn/AI shoe SVGs.
    key = str(product_id).strip().upper()
    if key in REAL_SHOE_IMAGES:
        return REAL_SHOE_IMAGES[key]
    try:
        idx = max(0, int(key.replace("SV", "")) - 1) % len(PHOTO_URLS)
    except ValueError:
        idx = sum(ord(c) for c in str(name)) % len(PHOTO_URLS) if name else fallback % len(PHOTO_URLS)
    return PHOTO_URLS[idx]

# Kept for compatibility with older code imports.
def shoe_data_uri(product_id="", name="", fallback=0):
    return shoe_image_src(product_id, name, fallback)
