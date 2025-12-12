import streamlit as st
import pandas as pd
import io

# --- CONFIGURATION DU SITE ---
st.set_page_config(page_title="BMW Winter Configurator", page_icon="❄️", layout="wide")

# --- DONNÉES (Ta base de données) ---
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

# --- CSS / DESIGN PREMIUM ---
# Ici on définit le style visuel : Couleurs BMW, Ombres, Cartes
st.markdown("""
    <style>
    /* Fond général plus propre */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Le Header Bleu BMW */
    .header-style {
        background-color: #1c69d4;
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Style des cartes de produits */
    .product-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .product-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.12);
        border-color: #1c69d4;
    }
    
    /* Prix */
    .price-text {
        font-size: 26px;
        color: #1c69d4;
        font-weight: 800;
    }
    .promo-label {
        background-color: #d9534f;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        text-transform: uppercase;
    }
    
    /* Bouton */
    .stButton>button {
        background-color: #222;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1c69d4;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER DE LA PAGE ---
st.markdown("""
    <div class="header-style">
        <h1 style='margin:0; font-size: 2.5rem;'>❄️ CAMPAGNE HIVER BMW</h1>
        <p style='margin:0; opacity: 0.9;'>Assistant de Vente & Magasin | Saison 2025-2026</p>
    </div>
""", unsafe_allow_html=True)

# --- CHARGEMENT ---
df = pd.read_csv(io.StringIO(csv_data), sep=";")
df.columns = df.columns.str.strip()

# --- INTERFACE PRINCIPALE (2 Colonnes) ---
col_filtres, col_resultats = st.columns([1, 3])

# --- COLONNE DE GAUCHE : LES FILTRES ---
with col_filtres:
    st.markdown("### 🔍 Configuration")
    st.markdown("Remplissez les infos pour filtrer le catalogue.")
    
    with st.container(border=True):
        # 1. Modèle
        liste_modeles = sorted(df['Modele'].unique())
        choix_modele = st.selectbox("Modèle du véhicule", liste_modeles)
        
        st.markdown("---")
        
        # 2. Options Techniques
        st.write("**Contraintes techniques :**")
        freins_m = st.checkbox("Freins M Sport (Bleu/Rouge)", value=False)
        chaine = st.checkbox("Doit être chainable", value=False)
        
        st.markdown("---")
        st.info("ℹ️ Sélectionnez le véhicule pour voir les kits compatibles.")

# --- COLONNE DE DROITE : LES RÉSULTATS ---
with col_resultats:
    # Filtrage logique
    kits = df[df['Modele'] == choix_modele].copy()
    
    if freins_m:
        kits = kits[kits['Compatibilite_Freins_M'] == "OUI"]
    if chaine:
        kits = kits[kits['Chainable'] == "OUI"]

    st.markdown(f"### 📦 {len(kits)} Kits disponibles pour : **{choix_modele}**")
    
    if len(kits) == 0:
        st.warning("⚠️ Aucun kit compatible avec ces filtres.")
    else:
        # Affichage en Grille (2 cartes par ligne)
        grid_cols = st.columns(2)
        
        for index, (idx, row) in enumerate(kits.iterrows()):
            # On alterne les colonnes pour l'affichage grille
            with grid_cols[index % 2]:
                
                # Image générique de roue (Pour faire joli en attendant les vraies)
                img_url = "https://cdn-icons-png.flaticon.com/512/5716/5716474.png" 
                
                # HTML CARD
                st.markdown(f"""
                <div class="product-card">
                    <div style="display:flex; justify-content:space-between; align-items:start;">
                        <span style="font-size:1.2rem; font-weight:bold;">Style {row['Style']}</span>
                        <span style="background:#eee; padding:2px 8px; border-radius:4px; font-weight:bold;">{row['Pouces']}"</span>
                    </div>
                    
                    <div style="display:flex; margin-top:15px; margin-bottom:15px;">
                        <div style="flex:1; display:flex; justify-content:center; align-items:center;">
                             <img src="{img_url}" width="80" style="opacity:0.6;">
                        </div>
                        <div style="flex:2; padding-left:15px; font-size:0.9rem; color:#555;">
                            <div>🔘 <b>Pneu:</b> {row['Pneu']}</div>
                            <div style="margin-top:5px; font-family:monospace; background:#f4f4f4; padding:2px; display:inline-block;">REF: {row['Ref']}</div>
                            <div style="margin-top:5px;">
                                { "✅ Chainable" if row['Chainable'] == "OUI" else "🚫 Pas de chaînes" }
                            </div>
                        </div>
                    </div>

                    <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #eee; padding-top:10px;">
                        <div>
                            <span class="promo-label">-10% PROMO</span>
                        </div>
                        <div class="price-text">{row['Prix_Promo']} €</div>
                    </div>
                    
                    <div style="margin-top:10px; color:orange; font-size:0.85rem; font-weight:bold;">
                        {f"⚠️ {row['Note_Importante']}" if pd.notna(row['Note_Importante']) else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Le bouton Streamlit doit être hors du HTML pour fonctionner en Python
                if st.button(f"Sélectionner ce kit ({row['Style']})", key=row['Ref']):
                    st.toast(f"✅ Ajouté ! Réf: {row['Ref']}")
