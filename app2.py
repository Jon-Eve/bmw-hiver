import streamlit as st
import pandas as pd
import io

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="BMW Bilia Hiver 2025/26", page_icon="❄️", layout="centered")

# --- 2. DONNÉES EMBARQUÉES ---
csv_data = """Modele;Chassis;Style;Pouces;Ref;Pneu;Prix_Promo;Compatibilite_Freins_M;Chainable;Note_Importante
Série 1 / Série 2 GC;F40 / F44;474;16;36 11 5 A92 C63;Continental TS860S;1549;NON;OUI;
Série 1 / Série 2 GC;F40 / F44;489;17;36 11 2 471 501;Pirelli Snowcontrol 3;2158;NON;OUI;
... (le reste de tes données exactement comme avant) ...
"""

# --- 3. STYLE CSS ---
st.markdown("""
    <style>
    .big-price {
        font-size: 28px !important;
        color: #d9534f;
        font-weight: bold;
        text-align: center;
        margin: 10px 0;
    }
    .ref-code {
        font-family: monospace;
        font-size: 18px;
        background-color: #f0f2f6;
        padding: 8px 12px;
        border-radius: 6px;
        display: inline-block;
        margin: 10px 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1c69d4;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 55px;
        font-size: 18px;
    }
    .stButton>button:hover {
        background-color: #1452a6;
    }
    div[data-testid="stExpander"] details summary {
        font-size: 18px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. HEADER ---
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("🔵 **Bilia**")
with col2:
    st.title("Kits Pneus Hiver 2025/2026")

st.caption("👋 Outil rapide pour trouver le bon kit hiver BMW – Prix remisés -10%")

# --- 5. CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    df = pd.read_csv(io.StringIO(csv_data), sep=";")
    df.columns = df.columns.str.strip()
    
    # Conversion numérique
    df['Pouces'] = pd.to_numeric(df['Pouces'], errors='ignore')
    df['Prix_Promo'] = pd.to_numeric(df['Prix_Promo'], errors='ignore')
    
    # Ordre naturel des modèles (personnalisable)
    ordre_modeles = [
        "Série 1 / Série 2 GC", "New Série 1 / Série 2 GC", "Série 2 Coupé", "Série 2 Active Tourer",
        "Série 3 / 4", "Série 4 GC / i4", "Série 5 (Thermique)", "i5 / Série 5 Hybride",
        "Série 7 / i7", "X1 / X2", "X3 / X4 (Ancien)", "X3 (Nouveau)", "iX3", "X5 / X6"
    ]
    df['Modele_order'] = pd.categorical(df['Modele'], categories=ordre_modeles, ordered=True)
    return df

df = load_data()

# --- 6. SÉLECTION DU MODÈLE ---
st.markdown("---")
modeles_uniques = df.sort_values('Modele_order')['Modele'].unique()
choix_modele = st.selectbox("🚗 Sélectionnez le modèle du client", modeles_uniques)

kits = df[df['Modele'] == choix_modele].copy()

# Affichage du châssis pour info
chassis = kits['Chassis'].iloc[0]
st.info(f"📋 Châssis concerné(s) : **{chassis}**")

# --- 7. FILTRES TECHNIQUES ---
st.markdown("---")
st.subheader("⚙️ Options du véhicule")

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    freins_m = st.toggle("Freins M Sport", help="Étriers bleus ou rouges")
with col2:
    chaine = st.toggle("Doit être chainable")
with col3:
    if st.button("🔄 Réinitialiser les filtres"):
        st.experimental_rerun()

# Application des filtres
filtered_kits = kits.copy()

if freins_m:
    filtered_kits = filtered_kits[filtered_kits['Compatibilite_Freins_M'] == "OUI"]

if chaine:
    filtered_kits = filtered_kits[filtered_kits['Chainable'] == "OUI"]

# Tri logique : d'abord par pouces croissant, puis par prix
filtered_kits = filtered_kits.sort_values(by=['Pouces', 'Prix_Promo'])

# --- 8. RÉSULTATS ---
st.markdown("---")
nb_resultats = len(filtered_kits)
st.subheader(f"📦 {nb_resultats} kit(s) compatible(s) trouvé(s)")

if nb_resultats == 0:
    st.error("⛔ Aucun kit ne correspond à ces critères.")
    st.write("💡 Essayez de désactiver un des filtres (freins M ou chainage).")
else:
    for _, row in filtered_kits.iterrows():
        with st.expander(f"🛡️ Kit {row['Pouces']}\" - Style {row['Style']} | {row['Pneu']}", expanded=False):
            col_left, col_right = st.columns([2, 1])

            with col_left:
                st.markdown(f"**Référence :** <span class='ref-code'>{row['Ref']}</span>", unsafe_allow_html=True)
                
                if pd.notna(row['Note_Importante']):
                    st.warning(f"⚠️ {row['Note_Importante']}")

                st.markdown(f"**Chainable :** {'✅ Oui' if row['Chainable'] == 'OUI' else '🚫 Non'}")
                st.markdown(f"**Freins M :** {'✅ Compatible' if row['Compatibilite_Freins_M'] == 'OUI' else '❌ Non compatible'}")

            with col_right:
                st.markdown(f"<div class='big-price'>{row['Prix_Promo']:,.0f} €</div>".replace(',', ' '), unsafe_allow_html=True)
                st.caption("Prix promo hiver (−10 %)")

                if st.button("✅ CHOISIR CE KIT", key=f"btn_{row['Ref']}"):
                    st.balloons()
                    st.success(f"Kit sélectionné ! Référence **{row['Ref']}** prête à commander.")
                    # Copie automatique dans le presse-papier (via petit script JS)
                    st.markdown(f"""
                    <script>
                    navigator.clipboard.writeText("{row['Ref']}");
                    </script>
                    <p style='color: green; font-size: 14px;'>📋 Référence copiée dans le presse-papier !</p>
                    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("🚀 Outil développé pour les conseillers Bilia – Données valables hiver 2025/2026")
