import streamlit as st
import pandas as pd
import io

# --- CONFIG ---
st.set_page_config(page_title="BMW Bilia - Kits Hiver 2025/26", page_icon="❄️", layout="centered")

# --- BACKGROUND & STYLE ---
background_url = "https://cdn.bmwblog.com/wp-content/uploads/2023/03/bmw-i5-winter-testing-32.jpg"  # BMW en neige

st.markdown(f"""
<style>
    .stApp {{
        background-image: url("{background_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .main-box {{
        background-color: rgba(0, 0, 0, 0.75);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
    }}
    h1, h2, h3, label, .stMarkdown, .stCaption {{
        color: white !important;
    }}
    .orange-title {{
        color: #ff6600 !important;
        font-size: 36px !important;
        font-weight: bold;
        text-align: center;
    }}
    .big-price {{
        font-size: 34px !important;
        color: #ff6600 !important;
        font-weight: bold;
        text-align: center;
    }}
    .ref-code {{
        font-family: monospace;
        font-size: 20px;
        background: #444;
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
        height: 65px;
        font-size: 22px;
        border-radius: 10px;
        margin-top: 20px;
    }}
    .stButton>button:hover {{
        background: #1452a6;
    }}
    img {{
        max-width: 100%;
        height: auto;
        border-radius: 12px;
        margin-bottom: 15px;
    }}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<div class='main-box'>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("🔵 **Bilia**")
with col2:
    st.markdown("<div class='orange-title'>CAMPAGNE KITS HIVER BMW<br>2025 - 2026</div>", unsafe_allow_html=True)

st.caption("👋 Outil rapide pour les conseillers – Prix remisés −10%")

# --- DONNÉES ---
csv_data = """Modele;Chassis;Style;Pouces;Ref;Pneu;Prix_Promo;Compatibilite_Freins_M;Chainable;Note_Importante
Série 1 / Série 2 GC;F40 / F44;474;16;36 11 5 A92 C63;Continental TS860S;1549;NON;OUI;
Série 1 / Série 2 GC;F40 / F44;489;17;36 11 2 471 501;Pirelli Snowcontrol 3;2158;NON;OUI;
Série 1 / Série 2 GC;F40 / F44;554M;18;36 11 5 A92 C69;Continental TS860S SSR;2504;OUI;NON;
New Série 1 / Série 2 GC;F70 / F74;967;17;36 11 5 B4E 8D3;Good Year UltraGrip 3;1775;NON;OUI;
New Série 1 / Série 2 GC;F70 / F74;974;18;36 11 5 B4E 920;Good Year UltraGrip 3;1999;NON;NON;
New Série 1 / Série 2 GC;F70 / F74;968M;18;36 11 5 B4E 919;Good Year UltraGrip 3;2430;OUI;OUI;
New Série 1 / Série 2 GC;F70 / F74;975M;18;36 11 5 B6E 458;Bridgestone Blizzak;2615;OUI;NON;
New Série 1 / Série 2 GC;F70 / F74;976M;19;36 11 5 B4E 923;Hankook Winter i*cept;2615;OUI;OUI;
Série 2 Coupé;G42;778;17;36 11 5 A27 974;Bridgestone Blizzak;2123;OUI;OUI;
Série 2 Coupé;G42;796M;18;36 11 5 A23 FE1;Pirelli Sottozero 3;2448;OUI;OUI;
Série 2 Coupé;G42;848M;18;36 11 5 B84 309;Continental TS860S SSR;2655;OUI;NON;
Série 2 Coupé;G42;898M;19;36 11 5 A92 CA9;Continental TS860S SSR;3406;OUI;NON;
Série 2 Active Tourer;U06;186;16;36 11 5 A4A FD8;Continental TS860S;1845;OUI;OUI;Attention: Non compatible 230eX
Série 2 Active Tourer;U06;840;16;36 11 5 A4A FE1;Good Year UG8;1985;OUI;OUI;Attention: Non compatible 230eX
Série 2 Active Tourer;U06;875;17;36 11 5 A4A FE3;Hankook i*cept evo2;2054;OUI;OUI;
Série 2 Active Tourer;U06;838M;18;36 11 5 A4B 002;Good Year UG Perf;2430;OUI;NON;
Série 3 / 4;G20/G21/G22/G23;778;17;36 11 5 A27 974;Bridgestone Blizzak;2123;NON;OUI;
Série 3 / 4;G20/G21/G22/G23;778 (RFT);17;36 11 5 B83 BC1;Pirelli Sottozero 3;2158;NON;OUI;
Série 3 / 4;G20/G21/G22/G23;796M;18;36 11 5 A23 FE1;Pirelli Sottozero 3;2448;OUI;OUI;Attention: Mixte uniquement sur G21 Hybride
Série 3 / 4;G20/G21/G22/G23;848M;18;36 11 5 B84 309;Continental TS860S SSR;2655;OUI;NON;
Série 3 / 4;G20/G21/G22/G23;898M;19;36 11 5 A92 CA9;Continental TS860S SSR;3406;OUI;NON;
Série 4 GC / i4;G26 / i4;851;17;36 11 5 A45 DE2;Good Year UG Perf;2088;NON;OUI;
Série 4 GC / i4;G26 / i4;853;18;36 11 5 A45 E02;Good Year UG Perf;2338;OUI;OUI;
Série 4 GC / i4;G26 / i4;858M;18;36 11 5 B83 BF2;Pirelli Sottozero 3;2581;OUI;OUI;
Série 4 GC / i4;G26 / i4;859M;19;36 11 5 A4D 504;Pirelli P-Zero;3315;OUI;NON;ATTENTION: Si i4 M50 prendre kit spécifique (3425€)
Série 5 (Thermique);G60 / G61;932;18;36 11 5 B5C FE3;Pirelli Cinturato 2;2210;NON;OUI;
Série 5 (Thermique);G60 / G61;933;19;36 11 5 A8E 059;Continental TS860;3002;OUI;OUI;
Série 5 (Thermique);G60 / G61;942M;19;36 11 5 A8E 220;Pirelli P-Zero;3370;OUI;OUI;
Série 5 (Thermique);G60 / G61;939M;20;36 11 5 B4A 8A6;Pirelli P-Zero;4304;OUI;NON;
i5 / Série 5 Hybride;G60 / G61;933;19;36 11 5 A08 E59;Continental TS860;3002;OUI;OUI;Mixte uniquement pour i5 M60 / Touring
i5 / Série 5 Hybride;G60 / G61;942M;19;36 11 5 A8E 220;Pirelli P-Zero;3370;OUI;OUI;Mixte uniquement pour i5 M60 / Touring
i5 / Série 5 Hybride;G60 / G61;939M;20;36 11 5 B4A 8A6;Pirelli P-Zero;4304;OUI;NON;Mixte uniquement pour i5 M60 / Touring
Série 7 / i7;G70;906;20;36 11 5 B61 CF5;Pirelli P-Zero;4340;OUI;NON;
Série 7 / i7;G70;911M;20;36 11 5 B61 CF9;Pirelli P-Zero;5187;OUI;NON;
Série 7 / i7;G70;909M;21;36 11 5 A64 995;Pirelli P-Zero;5720;OUI;NON;
X1 / X2;U11 / U10;833;17;36 11 5 A65 E64;Pirelli Cinturato 2;2367;NON;OUI;
X1 / X2;U11 / U10;875;17;36 11 5 A88 F94;Continental TS860S;2332;NON;OUI;
X1 / X2;U11 / U10;879;18;36 11 5 B31 424;Continental TS860S;1878;NON;OUI;M35i : Uniquement avec freins composite Gris
X1 / X2;U11 / U10;838M;18;36 11 5 A65 F35;Pirelli Cinturato 2;2485;NON;NON;Pas compatible freins rouges
X1 / X2;U11 / U10;1041;19;36 11 5 A8F E61;Hankook i*cept evo3;2283;NON;OUI;
X1 / X2;U11 / U10;871M;19;36 11 5 B5C FF5;Pirelli P-Zero;3535;NON;OUI;
X1 / X2;U11 / U10;872M;20;36 11 5 A8F DC5;Pirelli P-Zero;4045;NON;NON;
X3 / X4 (Ancien);G01 / G02;618;18;36 11 5 B31 503;Hankook i*cept evo2;1896;OUI;OUI;
X3 / X4 (Ancien);G01 / G02;698M;19;36 11 5 A27 9A0;Pirelli Sottozero 3;3093;OUI;OUI;
X3 (Nouveau);G45;921;18;36 11 5 B4E 9A1;Hankook i*cept evo2;1989;NON;OUI;
X3 (Nouveau);G45;903;19;36 11 5 B4E 9C5;Good Year UG Perf;2688;OUI;OUI;
X3 (Nouveau);G45;1035M;19;36 11 5 B4E 9E2;Pirelli P-Zero;3167;OUI;OUI;
iX3;G08;842;19;36 11 5 A08 5B1;Michelin Pilot Alpin 5;2982;OUI;OUI;Flasque aero obligatoire en +
X5 / X6;G05 / G06 LCI;735;19;36 11 5 B5D 007;Pirelli Scorpion;2983;NON;OUI;Non compatible G06
X5 / X6;G05 / G06 LCI;748M;20;36 11 5 A81 989;Pirelli Scorpion;4138;OUI;OUI;
X5 / X6;G05 / G06 LCI;740M;20;36 11 5 A81 992;Michelin Pilot Alpin;4452;OUI;OUI;
X5 / X6;G05 / G06 LCI;741M;21;36 11 5 A81 9A7;Pirelli Scorpion;5352;OUI;NON;
"""

# --- IMAGES JANTES (meilleures trouvées) ---
image_urls = {
    '474': 'https://shop.bmw.co.uk/dw/image/v2/BJPN_PRD/on/demandware.static/-/Sites-masterCatalog_BMW/default/dw1c0b0a3e/images/hi-res/36_11_5_A92_C63_1.jpg',
    '489': 'https://cdn.ekris.nl/580/conversions/5(5)-responsive.jpg',
    '554M': 'https://cargym.com/cdn/shop/products/554M_b4bb568d-083a-4db3-b2a1-9ba0e4673b11_1270x.jpg?v=1665051800',
    '967': 'https://www.salesafter.eu/images/product_images/original_images/36115B4E8D3.webp',
    '974': 'https://mediapool.bmwgroup.com/cache/P9/2024/P90546890/P90546890-bmw-1-series-18-inch-winter-complete-wheel-v-spoke-974-gunmetal-grey-08-2024-600px.jpg',
    '968M': 'https://cotswoldherefordparts.com/cdn/shop/files/36115B4E919_1.jpg?v=1751355755&width=1946',
    '975M': 'https://cargym.com/cdn/shop/files/rn-image_picker_lib_temp_00bebe94-1cb6-4f46-bc37-1d8dde6258c0_846x.jpg?v=1743613769',
    '976M': 'https://cdn.ekris.nl/33861/conversions/BMW-1-Serie-F70-2-Serie-F74-styling-976M-winterbanden-responsive.jpg',
    '778': 'https://buybestparts.com/hpeciai/a613276e16ecb9cf81c7ba603bb6a86e/eng_pl_17-Summer-Kit-BMW-Wheels-Style-778-Tires-Pirelli-Sensors-BMW-G20-G21-G22-G23-G42-17361_1.webp',
    '778 (RFT)': 'https://buybestparts.com/hpeciai/a613276e16ecb9cf81c7ba603bb6a86e/eng_pl_17-Summer-Kit-BMW-Wheels-Style-778-Tires-Pirelli-Sensors-BMW-G20-G21-G22-G23-G42-17361_1.webp',
    '796M': 'https://djantite.bg/hpeciai/d14ec797d9d8a6f263c8fc34ed1d5d74/eng_pl_18-Winter-Kit-BMW-Wheels-Style-M796-Tires-Bridgestone-Sensors-BMW-G20-G21-G22-G23-17353_6.webp',
    '848M': 'https://i.ebayimg.com/images/g/0mQAAOSwFm1k5H5l/s-l1200.jpg',
    '898M': 'https://mediapool.bmwgroup.com/cache/P9/2020/P90392747/P90392747-the-new-bmw-3-series-sedan-m-performance-parts-19-inch-m-light-alloy-wheels-double-spoke-style-898-m-frozen-gunmetal-600px.jpg',
    '186': 'https://cdn.ekris.nl/33864/conversions/Winterwielset-1-inch-Styling-186-incl_-Goodyear,-BMW-2-Serie-Active-Tourer-(U06)-responsive.jpg',
    '840': 'https://cdn.ekris.nl/33864/conversions/Winterwielset-1-inch-Styling-186-incl_-Goodyear,-BMW-2-Serie-Active-Tourer-(U06)-responsive.jpg',
    '875': 'https://cdn.ekris.nl/33870/conversions/Winterwielset-1-inch-Styling-875-incl_-Hankook,-BMW-2-Serie-(U06)-responsive.jpg',
    '838M': 'https://cdn.ekris.nl/73315/conversions/Winterwielset-18-inch-Styling-838M-incl_-Pirelli,-BMW-X1-&-X2-(U11,-U10)(2)-responsive.jpg',
    '851': 'https://www.recambiosyaccesoriosbmw.com/cdn/shop/files/0ca6f5e061a85247eaca78bce971d4f5fad9b9f0_v_speiche_851_reflexsilber_1_4fbaacb7-faff-4845-8a18-64bcaed2f9bb.jpg?v=1738352001',
    '853': 'https://cdn.ekris.nl/33880/conversions/Winterwielset-17-inch-Styling-851-incl_-Goodyear,-BMW-4-Serie-(G26)-responsive.jpg',
    '858M': 'https://www.recambiosyaccesoriosbmw.com/cdn/shop/files/e2ff61a7f98c74ba64c834b1c7de3effd23e14eb_m_aerodynamikrad_858_midnight_grey_glanzgedreht_2_72d76482-eb05-4e31-a061-27546064f3a7.jpg?v=1755724499',
    '859M': 'https://mediapool.bmwgroup.com/cache/P9/2021/P90416884/P90416884-bmw-4-series-gran-coupe-m-performance-parts-19-inch-m-light-alloy-wheel-y-spoke-859-m-jet-black-600px.jpg',
    '932': 'https://www.salesafter.eu/images/product_images/original_images/36115B5CFE3.webp',
    '933': 'https://mediapool.bmwgroup.com/cache/P9/2023/P90516880/P90516880-m-performance-parts-for-the-new-bmw-5-series-19-inch-triplex-wheel-933-refined-silver-08-2023-600px.jpg',
    '942M': 'https://mediapool.bmwgroup.com/cache/P9/2023/P90516880/P90516880-m-performance-parts-for-the-new-bmw-5-series-19-inch-m-y-spoke-wheel-942-m-jet-black-matt-08-2023-600px.jpg',
    '939M': 'https://mediapool.bmwgroup.com/cache/P9/2023/P90516880/P90516880-m-performance-parts-for-the-new-bmw-5-series-20-inch-m-aerodynamic-wheel-939-m-bicolor-08-2023-1999px.jpg',
    '906': 'https://mediapool.bmwgroup.com/cache/P9/2023/P90516880/P90516880-m-performance-parts-for-the-new-bmw-7-series-20-inch-m-aerodynamic-wheel-906-bicolor-gunmetal-grey-08-2023-600px.jpg',
    '911M': 'https://mediapool.bmwgroup.com/cache/P9/2023/P90516880/P90516880-m-performance-parts-for-the-new-bmw-7-series-20-inch-m-y-spoke-wheel-911-m-jet-black-matt-08-2023-600px.jpg',
    '909M': 'https://mediapool.bmwgroup.com/cache/P9/2023/P90516880/P90516880-m-performance-parts-for-the-new-bmw-7-series-21-inch-m-aerodynamic-wheel-909-m-jet-black-uni-08-2023-600px.jpg',
    '833': 'https://www.salesafter.eu/images/product_images/original_images/36115a92c70.jpeg',
    '879': 'https://www.picclickimg.com/8C0AAeSwdTVo56gE/Original-BMW-X1-iX1-U11-18-Inch-Winter.webp',
    '1041': 'https://cdn.ekris.nl/33811/conversions/BMW-X1-U11-X2-U10-styling-1040-winterbanden-responsive.jpg',
    '871M': 'https://mediapool.bmwgroup.com/cache/P9/2023/P90509796/P90509796-bmw-x1-m35i-m-frozen-pure-grey-metallic-rim-19-styling-871m-06-2023-600px.jpg',
    '872M': 'https://mediapool.bmwgroup.com/cache/P9/2023/P90509796/P90509796-bmw-x1-m35i-m-frozen-pure-grey-metallic-rim-20-styling-872m-06-2023-2250px.jpg',
    '618': 'https://djantite.bg/hpeciai/9ae10d28e39736ec7942e4de657bc6af/eng_pl_Winter-Kit-17-BMW-Wheels-618-Pirelli-Tires-Sensors-BMW-5-G30-G31-G32-7-G11-G12-14008_8.webp',
    '698M': 'https://mediapool.bmwgroup.com/cache/P9/2018/P90292747/P90292747-bmw-x3-x4-m-performance-parts-19-inch-m-light-alloy-wheels-double-spoke-style-698-m-ferric-grey-600px.jpg',
    '921': 'https://mediapool.bmwgroup.com/cache/P9/2024/P90546890/P90546890-bmw-x3-18-inch-winter-complete-wheel-y-spoke-921-refined-silver-08-2024-600px.jpg',
    '903': 'https://mediapool.bmwgroup.com/cache/P9/2024/P90546890/P90546890-bmw-x3-19-inch-winter-complete-wheel-double-spoke-903-refined-silver-08-2024-600px.jpg',
    '1035M': 'https://mediapool.bmwgroup.com/cache/P9/2024/P90546890/P90546890-bmw-x3-19-inch-m-light-alloy-wheel-y-spoke-1035-m-bicolour-midnight-grey-gloss-lathed-08-2024-600px.jpg',
    '842': 'https://cotswoldherefordparts.com/cdn/shop/files/36115A085B1_3.jpg?v=1751355755&width=1946',
    '735': 'https://buybestparts.com/hpeciai/a8f90dfeb7544d13c0086ad84bc8bb00/eng_pl_19-Winter-Kit-BMW-Wheels-Style-735-Pirelli-Tires-2021-Sensors-BMW-X5-G05-X6-G06-27065_2.webp',
    '748M': 'https://mediapool.bmwgroup.com/cache/P9/2019/P90339847/P90339847-bmw-x5-x6-m-performance-parts-20-inch-m-light-alloy-wheel-star-spoke-748-m-jet-black-matt-600px.jpg',
    '740M': 'https://buybestparts.com/hpeciai/39130291c63794ca9c38a75ed8bee1d7/eng_pl_20-Winter-Kit-BMW-Wheels-Style-740-M-Tires-Michelin-2020-Sensors-BMW-X5-G05-X6-G06-26199_8.webp',
    '741M': 'https://mediapool.bmwgroup.com/cache/P9/2019/P90339847/P90339847-bmw-x5-x6-m-performance-parts-21-inch-m-light-alloy-wheel-y-spoke-741-m-orbit-grey-gloss-lathed-600px.jpg'
}

# --- CHARGEMENT ---
@st.cache_data
def load_data():
    df = pd.read_csv(io.StringIO(csv_data), sep=";")
    df.columns = df.columns.str.strip()
    df['Pouces'] = pd.to_numeric(df['Pouces'], errors='coerce')
    df['Prix_Promo'] = pd.to_numeric(df['Prix_Promo'], errors='coerce')
    return df

df = load_data()

# --- TRI MODÈLES ---
ordre_modeles = [
    "Série 1 / Série 2 GC", "New Série 1 / Série 2 GC", "Série 2 Coupé", "Série 2 Active Tourer",
    "Série 3 / 4", "Série 4 GC / i4", "Série 5 (Thermique)", "i5 / Série 5 Hybride",
    "Série 7 / i7", "X1 / X2", "X3 / X4 (Ancien)", "X3 (Nouveau)", "iX3", "X5 / X6"
]

modeles_tries = sorted(df['Modele'].unique(), key=lambda x: ordre_modeles.index(x) if x in ordre_modeles else 999)

# --- INTERFACE ---
st.markdown("---")
choix_modele = st.selectbox("🚗 Modèle du client", modeles_tries)

kits = df[df['Modele'] == choix_modele].copy()
chassis = kits['Chassis'].iloc[0]
st.info(f"📋 Châssis : **{chassis}**")

st.markdown("---")
st.subheader("⚙️ Options")

col1, col2 = st.columns(2)
with col1:
    freins_m = st.toggle("Freins M Sport")
with col2:
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
            url = image_urls.get(row['Style'])
            if url:
                st.image(url, use_column_width=True)
            else:
                st.caption("Photo non disponible")

            st.markdown(f"**Référence :** <span class='ref-code'>{row['Ref']}</span>", unsafe_allow_html=True)
            if pd.notna(row['Note_Importante']):
                st.warning(f"⚠️ {row['Note_Importante']}")
            st.write(f"**Chainable :** {'✅ Oui' if row['Chainable'] == 'OUI' else '🚫 Non'}")
            st.write(f"**Freins M :** {'✅ Compatible' if row['Compatibilite_Freins_M'] == 'OUI' else '❌ Non'}")
            st.markdown(f"<div class='big-price'>{row['Prix_Promo']:,.0f} €</div>".replace(",", " "), unsafe_allow_html=True)
            st.caption("Prix promo −10%")

            if st.button("✅ CHOISIR CE KIT", key=row['Ref']):
                st.balloons()
                st.success("Sélectionné ! Référence copiée.")
                st.markdown(f"<script>navigator.clipboard.writeText('{row['Ref']}'); alert('Réf {row['Ref']} copiée !');</script>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.caption("Outil Bilia – Valable hiver 2025/2026")
