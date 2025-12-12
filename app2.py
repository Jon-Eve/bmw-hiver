import streamlit as st
import pandas as pd
import io

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="BMW Bilia - Kits Hiver 2025/26", page_icon="❄️", layout="centered")

# --- 2. DONNÉES EMBARQUÉES (tout est ici, pas de fichier externe) ---
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

# --- 3. STYLE CSS ---
st.markdown("""
<style>
    .big-price {font-size: 30px !important; color: #d9534f; font-weight: bold; text-align: center;}
    .ref-code {font-family: monospace; font-size: 18px; background:#f0f2f6; padding:8px 12px; border-radius:6px;}
    .stButton>button {width:100%; background:#1c69d4; color:white; font-weight:bold; height:55px; font-size:18px; border-radius:8px;}
    .stButton>button:hover {background:#1452a6;}
</style>
""", unsafe_allow_html=True)

# --- 4. EN-TÊTE ---
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("🔵 **Bilia**")
with col2:
    st.title("Kits Pneus Hiver 2025/2026")
st.caption("Outil rapide pour les conseillers BMW – Prix remisés −10%")

# --- 5. CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    df = pd.read_csv(io.StringIO(csv_data), sep=";")
    df.columns = df.columns.str.strip()
    df['Pouces'] = pd.to_numeric(df['Pouces'], errors='coerce')
    df['Prix_Promo'] = pd.to_numeric(df['Prix_Promo'], errors='coerce')
    return df

df = load_data()

# --- 6. TRI DES MODÈLES DANS L'ORDRE LOGIQUE ---
ordre_modeles = [
    "Série 1 / Série 2 GC", "New Série 1 / Série 2 GC", "Série 2 Coupé", "Série 2 Active Tourer",
    "Série 3 / 4", "Série 4 GC / i4", "Série 5 (Thermique)", "i5 / Série 5 Hybride",
    "Série 7 / i7", "X1 / X2", "X3 / X4 (Ancien)", "X3 (Nouveau)", "iX3", "X5 / X6"
]

modeles_tries = sorted(df['Modele'].unique(), key=lambda x: ordre_modeles.index(x) if x in ordre_modeles else 999)

# --- 7. INTERFACE ---
st.markdown("---")
choix_modele = st.selectbox("🚗 Sélectionnez le modèle du client", modeles_tries)

kits = df[df['Modele'] == choix_modele].copy()
chassis = kits['Chassis'].iloc[0]
st.info(f"📋 Châssis : **{chassis}**")

st.markdown("---")
st.subheader("⚙️ Options du véhicule")

col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    freins_m = st.toggle("Freins M Sport", help="Étriers bleus ou rouges")
with col2:
    chainable = st.toggle("Doit être chainable")
with col3:
    if st.button("🔄 Reset"):
        st.experimental_rerun()

# Filtrage
filtered = kits.copy()
if freins_m:
    filtered = filtered[filtered['Compatibilite_Freins_M'] == "OUI"]
if chainable:
    filtered = filtered[filtered['Chainable'] == "OUI"]

# Tri des résultats : par taille de jante puis prix
filtered = filtered.sort_values(by=['Pouces', 'Prix_Promo'])

# --- 8. AFFICHAGE DES RÉSULTATS ---
st.markdown("---")
st.subheader(f"📦 {len(filtered)} kit(s) compatible(s)")

if len(filtered) == 0:
    st.error("⛔ Aucun kit ne correspond à ces critères.")
    st.write("💡 Essayez de désactiver un filtre.")
else:
    for _, row in filtered.iterrows():
        with st.expander(f"🛞 {row['Pouces']}\" - Style {row['Style']} | {row['Pneu']}", expanded=False):
            col_g, col_d = st.columns([2, 1])
            with col_g:
                st.markdown(f"**Référence :** <span class='ref-code'>{row['Ref']}</span>", unsafe_allow_html=True)
                if pd.notna(row['Note_Importante']):
                    st.warning(f"⚠️ {row['Note_Importante']}")
                st.write(f"**Chainable :** {'✅ Oui' if row['Chainable'] == 'OUI' else '🚫 Non'}")
                st.write(f"**Freins M :** {'✅ Compatible' if row['Compatibilite_Freins_M'] == 'OUI' else '❌ Non'}")
            with col_d:
                st.markdown(f"<div class='big-price'>{row['Prix_Promo']:,.0f} €</div>".replace(",", " "), unsafe_allow_html=True)
                st.caption("Prix promo −10%")
                if st.button("✅ CHOISIR CE KIT", key=row['Ref']):
                    st.balloons()
                    st.success("Kit sélectionné !")
                    # Copie automatique dans le presse-papier
                    st.markdown(f"""
                    <script>
                    navigator.clipboard.writeText("{row['Ref']}");
                    alert("Référence {row['Ref']} copiée dans le presse-papier !");
                    </script>
                    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Outil développé pour les conseillers Bilia – Hiver 2025/2026")
