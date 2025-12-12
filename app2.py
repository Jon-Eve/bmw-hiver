import streamlit as st
import pandas as pd
import io

# --- CONFIG ---
st.set_page_config(page_title="BMW Bilia - Kits Hiver 2025/26", page_icon="❄️", layout="centered")

# --- BACKGROUND IMAGE (BMW Série 5 en hiver neige) ---
background_url = "https://cdn.bmwblog.com/wp-content/uploads/2023/03/bmw-i5-winter-testing-32.jpg"

st.markdown(f"""
<style>
    .stApp {{
        background-image: url("{background_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .main-container {{
        background-color: rgba(0, 0, 0, 0.7);
        padding: 20px;
        border-radius: 15px;
        margin: 10px;
    }}
    h1, h2, h3, label, .stCaption {{
        color: white !important;
    }}
    .stSelectbox > div > div > div, .stToggle > div > label {{
        color: white !important;
    }}
    .big-price {{
        font-size: 32px !important;
        color: #ff6600 !important;  /* Orange BMW */
        font-weight: bold;
        text-align: center;
    }}
    .ref-code {{
        font-family: monospace;
        font-size: 20px;
        background: #333;
        color: white;
        padding: 10px 15px;
        border-radius: 8px;
        display: inline-block;
    }}
    .stButton>button {{
        width: 100%;
        background: #1c69d4;
        color: white;
        font-weight: bold;
        height: 60px;
        font-size: 20px;
        border-radius: 10px;
    }}
    .stButton>button:hover {{
        background: #1452a6;
    }}
    img {{
        max-width: 100%;
        height: auto;
        border-radius: 10px;
    }}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("🔵 **Bilia**")
with col2:
    st.markdown("<h1 style='color:#ff6600;'>CAMPAGNE KITS HIVER BMW<br>2025 - 2026</h1>", unsafe_allow_html=True)

st.caption("👋 Outil rapide pour trouver le kit hiver idéal – Prix remisés −10%")

# --- DONNÉES ---
csv_data = """... (exactement le même CSV que avant, je ne le répète pas pour la longueur) ..."""

# --- IMAGES DES JANTES (meilleures trouvées) ---
image_urls = {
    '474': 'https://cdn.ekris.nl/47395/conversions/36115A92C63(1)-responsive.jpg',
    '489': 'https://cdn.ekris.nl/580/conversions/5(5)-responsive.jpg',
    '554M': 'https://cargym.com/cdn/shop/products/554M_b4bb568d-083a-4db3-b2a1-9ba0e4673b11_1270x.jpg?v=1665051800',
    '967': 'https://assets.turnermotorsport.com/product_library_tms/1631593_x800.webp',  # proche
    '974': 'https://buybestparts.com/hpeciai/8d58d282fa76e688a8dac19d02691cd0/eng_pl_NEW-16-Winter-Kit-Wheels-BMW-Style-774-Tires-Sensors-G20-G21-G22-G23-26176_12.webp',  # proche
    '968M': 'https://i.ebayimg.com/images/g/DOcAAOSw8NplLtwK/s-l1200.jpg',
    '975M': 'https://cargym.com/cdn/shop/files/rn-image_picker_lib_temp_00bebe94-1cb6-4f46-bc37-1d8dde6258c0_846x.jpg?v=1743613769',
    '976M': 'https://cdn.ekris.nl/33861/conversions/BMW-1-Serie-F70-2-Serie-F74-styling-976M-winterbanden-responsive.jpg',
    '778': 'https://buybestparts.com/hpeciai/a613276e16ecb9cf81c7ba603bb6a86e/eng_pl_17-Summer-Kit-BMW-Wheels-Style-778-Tires-Pirelli-Sensors-BMW-G20-G21-G22-G23-G42-17361_1.webp',
    '778 (RFT)': 'https://buybestparts.com/hpeciai/a613276e16ecb9cf81c7ba603bb6a86e/eng_pl_17-Summer-Kit-BMW-Wheels-Style-778-Tires-Pirelli-Sensors-BMW-G20-G21-G22-G23-G42-17361_1.webp',
    '796M': 'https://djantite.bg/hpeciai/d14ec797d9d8a6f263c8fc34ed1d5d74/eng_pl_18-Winter-Kit-BMW-Wheels-Style-M796-Tires-Bridgestone-Sensors-BMW-G20-G21-G22-G23-17353_6.webp',
    '848M': 'https://i.ebayimg.com/images/g/0mQAAOSwFm1k5H5l/s-l1200.jpg',
    '898M': 'https://www.salesafter.eu/images/product_images/original_images/36115a8e220.jpeg',  # proche
    '186': 'https://cdn.ekris.nl/33864/conversions/Winterwielset-1-inch-Styling-186-incl_-Goodyear,-BMW-2-Serie-Active-Tourer-(U06)-responsive.jpg',
    '840': 'https://cdn.ekris.nl/33864/conversions/Winterwielset-1-inch-Styling-186-incl_-Goodyear,-BMW-2-Serie-Active-Tourer-(U06)-responsive.jpg',  # proche
    '875': 'https://cdn.ekris.nl/33870/conversions/Winterwielset-1-inch-Styling-875-incl_-Hankook,-BMW-2-Serie-(U06)-responsive.jpg',
    '838M': 'https://cdn.ekris.nl/73315/conversions/Winterwielset-18-inch-Styling-838M-incl_-Pirelli,-BMW-X1-&-X2-(U11,-U10)(2)-responsive.jpg',
    '851': 'http://www.recambiosyaccesoriosbmw.com/cdn/shop/files/0ca6f5e061a85247eaca78bce971d4f5fad9b9f0_v_speiche_851_reflexsilber_1_4fbaacb7-faff-4845-8a18-64bcaed2f9bb.jpg?v=1738352001',
    '853': 'https://cdn.ekris.nl/33880/conversions/Winterwielset-17-inch-Styling-851-incl_-Goodyear,-BMW-4-Serie-(G26)-responsive.jpg',  # proche
    '858M': 'http://www.recambiosyaccesoriosbmw.com/cdn/shop/files/e2ff61a7f98c74ba64c834b1c7de3effd23e14eb_m_aerodynamikrad_858_midnight_grey_glanzgedreht_2_72d76482-eb05-4e31-a061-27546064f3a7.jpg?v=1755724499',
    '859M': 'https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=1246643264145764',
    '932': 'https://www.salesafter.eu/images/product_images/original_images/36115B5CFE3.webp',
    '933': 'https://s3.amazonaws.com/rp-part-images/assets/272563f6197781656956321e664bdb31.webp',
    '942M': 'https://www.salesafter.eu/images/product_images/original_images/36115a8e220.jpeg',
    '939M': 'https://mediapool.bmwgroup.com/cache/P9/202404/P90546890/P90546890-m-performance-parts-for-the-new-bmw-5-series-touring-20-inch-m-aerodynamic-wheel-939-m-bicolor--midn-1999px.jpg',
    '906': 'https://cdn.ekris.nl/33895/conversions/BMW-winterwielset-20-inch-Styling-906-Breed-Gunmetal-incl_-Pirelli,-BMW-i7-(G70)-responsive.jpg',
    '911M': 'https://cdn.revolutionparts.io/images/285f89b802bcb2651801455c86d78f2a/1b49e18b6ed43c0fe8a7463459834a60.jpg',
    '909M': 'https://cdn.ekris.nl/33893/conversions/Winterwielset-21-inch-Styling-909M-Bicolor-Breed,-BMW-7-Serie-(G70)-responsive.jpg',
    '833': 'https://i.ebayimg.com/images/g/pPUAAeSw0PtoKw2E/s-l1200.jpg',
    '879': 'https://www.picclickimg.com/8C0AAeSwdTVo56gE/Original-BMW-X1-iX1-U11-18-Inch-Winter.webp',
    '1041': 'https://cdn.ekris.nl/33811/conversions/BMW-X1-U11-X2-U10-styling-1040-winterbanden-responsive.jpg',
    '871M': 'https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=1272608311549259',
    '872M': 'https://cdn.ekris.nl/33809/conversions/BMW-X1-U11-X2-U10-styling-872M-winterbanden-responsive.jpg',
    '618': 'https://djantite.bg/hpeciai/9ae10d28e39736ec7942e4de657bc6af/eng_pl_Winter-Kit-17-BMW-Wheels-618-Pirelli-Tires-Sensors-BMW-5-G30-G31-G32-7-G11-G12-14008_8.webp',
    '698M': 'https://i.ebayimg.com/images/g/g-AAAOSw1tNbqqhs/s-l400.jpg',
    '921': 'https://s3.amazonaws.com/rp-part-images/assets/66e0ccd3e39dd12ab84f958f60083f3c.webp',
    '903': 'https://cdn.ekris.nl/33818/conversions/BMW-X3-G45-styling-903-winterbanden-Refinde-Silver-responsive.jpg',
    '1035M': 'https://s3.amazonaws.com/rp-part-images/assets/5b5eeeab2d4ec1d2151413e6356876e1.webp',
    '842': 'https://cotswoldherefordparts.com/cdn/shop/files/36115A085B1_3.jpg?v=1751355755&width=1946',
    '735': 'https://buybestparts.com/hpeciai/a8f90dfeb7544d13c0086ad84bc8bb00/eng_pl_19-Winter-Kit-BMW-Wheels-Style-735-Pirelli-Tires-2021-Sensors-BMW-X5-G05-X6-G06-27065_2.webp',
    '748M': 'https://assets.turnermotorsport.com/product_library_tms/1614715_x600.jpg',
    '740M': 'https://buybestparts.com/hpeciai/39130291c63794ca9c38a75ed8bee1d7/eng_pl_20-Winter-Kit-BMW-Wheels-Style-740-M-Tires-Michelin-2020-Sensors-BMW-X5-G05-X6-G06-26199_8.webp',
    '741M': 'https://cargym.com/cdn/shop/files/2025_01_24_9999_51_1_1800x.jpg?v=1762760909'
}

# --- CHARGEMENT DONNÉES (même que avant) ---
@st.cache_data
def load_data():
    df = pd.read_csv(io.StringIO(csv_data), sep=";")
    df.columns = df.columns.str.strip()
    df['Pouces'] = pd.to_numeric(df['Pouces'], errors='coerce')
    df['Prix_Promo'] = pd.to_numeric(df['Prix_Promo'], errors='coerce')
    return df

df = load_data()

# --- TRI MODÈLES ---
ordre_modeles = [ ... même liste ... ]

modeles_tries = sorted(df['Modele'].unique(), key=lambda x: ordre_modeles.index(x) if x in ordre_modeles else 999)

# --- INTERFACE (même logique, mais colonnes adaptées mobile) ---
st.markdown("---")
choix_modele = st.selectbox("🚗 Modèle du client", modeles_tries)

kits = df[df['Modele'] == choix_modele].copy()
chassis = kits['Chassis'].iloc[0]
st.info(f"📋 Châssis : **{chassis}**")

st.markdown("---")
st.subheader("⚙️ Options")

freins_m = st.toggle("Freins M Sport", help="Étriers bleus ou rouges")
chainable = st.toggle("Doit être chainable")
if st.button("🔄 Reset filtres"):
    st.experimental_rerun()

filtered = kits.copy()
if freins_m:
    filtered = filtered[filtered['Compatibilite_Freins_M'] == "OUI"]
if chainable:
    filtered = filtered[filtered['Chainable'] == "OUI"]

filtered = filtered.sort_values(by=['Pouces', 'Prix_Promo'])

st.markdown("---")
st.subheader(f"📦 {len(filtered)} kit(s) trouvé(s)")

if len(filtered) == 0:
    st.error("⛔ Aucun kit compatible.")
else:
    for _, row in filtered.iterrows():
        with st.expander(f"🛞 {row['Pouces']}\" - Style {row['Style']} | {row['Pneu']}", expanded=True):
            image_url = image_urls.get(row['Style'])
            if image_url:
                st.image(image_url, use_column_width=True)
            else:
                st.caption("Photo non disponible")
            
            # Sur mobile : tout en colonne
            col_g = st.container()
            with col_g:
                st.markdown(f"**Référence :** <span class='ref-code'>{row['Ref']}</span>", unsafe_allow_html=True)
                if pd.notna(row['Note_Importante']):
                    st.warning(f"⚠️ {row['Note_Importante']}")
                st.write(f"**Chainable :** {'✅ Oui' if row['Chainable'] == 'OUI' else '🚫 Non'}")
                st.write(f"**Freins M :** {'✅ Compatible' if row['Compatibilite_Freins_M'] == 'OUI' else '❌ Non'}")
                st.markdown(f"<div class='big-price'>{row['Prix_Promo']:,.0f} €</div>".replace(",", " "), unsafe_allow_html=True)
                st.caption("Prix promo −10%")
                
                if st.button("✅ CHOISIR CE KIT", key=row['Ref']):
                    st.balloons()
                    st.success("Sélectionné !")
                    st.markdown(f"""
                    <script>
                    navigator.clipboard.writeText("{row['Ref']}");
                    alert("Réf {row['Ref']} copiée !");
                    </script>
                    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.caption("Outil Bilia – Hiver 2025/2026")
