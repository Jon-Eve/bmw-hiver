import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="BMW Bilia Hiver", page_icon="❄️", layout="centered")

# CSS pour faire joli (Style BMW)
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #1c69d4;
        color: white;
        font-weight: bold;
    }
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    .price-tag {
        font-size: 24px;
        color: #d9534f;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Titre
st.title("❄️ Sélecteur Kits Hiver BMW")
st.markdown("### Garage Bilia - Saison 2025/2026")

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    try:
        # On lit le fichier CSV avec le séparateur point-virgule
        df = pd.read_csv("kits_bmw.csv", sep=";")
        return df
    except FileNotFoundError:
        st.error("ERREUR : Le fichier 'kits_bmw.csv' est introuvable.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- ETAPE 1 : CHOIX DU VÉHICULE ---
    st.markdown("---")
    st.header("1. Quel véhicule ?")
    
    # Liste des modèles triés
    liste_modeles = sorted(df['Modele'].unique())
    choix_modele = st.selectbox("Sélectionnez le modèle vendu :", liste_modeles)

    # Filtrer les données pour ce modèle
    kits_compatibles = df[df['Modele'] == choix_modele].copy()

    # --- ETAPE 2 : FILTRES INTELLIGENTS ---
    st.markdown("---")
    st.header("2. Options du véhicule")
    
    col1, col2 = st.columns(2)
    
    with col1:
        freins_m = st.checkbox("Pack M / Freins Sport (Etriers Bleus/Rouges) ?", value=False)
    
    with col2:
        chaine_required = st.checkbox("Le client veut absolument chaîner ?", value=False)

    # Application des filtres
    if freins_m:
        # On garde ceux qui sont compatibles OU ceux où ce n'est pas spécifié
        kits_compatibles = kits_compatibles[kits_compatibles['Compatibilite_Freins_M'] == "OUI"]
        st.info("ℹ️ Filtre activé : Kits incompatibles avec gros freins masqués.")

    if chaine_required:
        kits_compatibles = kits_compatibles[kits_compatibles['Chainable'] == "OUI"]
        st.info("ℹ️ Filtre activé : Uniquement les kits chainables.")

    # --- ETAPE 3 : RÉSULTATS ---
    st.markdown("---")
    st.header(f"3. Résultats ({len(kits_compatibles)} kits disponibles)")

    if len(kits_compatibles) == 0:
        st.error("⛔ Aucun kit ne correspond à cette configuration. Vérifiez les freins M ou l'option chainable.")
    else:
        for index, row in kits_compatibles.iterrows():
            with st.expander(f"🛞 Style {row['Style']} - {row['Pouces']} pouces", expanded=True):
                c1, c2 = st.columns([2, 1])
                
                with c1:
                    st.markdown(f"**Pneu :** {row['Pneu']}")
                    st.markdown(f"**Référence :** `{row['Ref']}`")
                    
                    # Gestion des notes importantes
                    if pd.notna(row['Note_Importante']):
                        st.warning(f"⚠️ {row['Note_Importante']}")
                    
                    if row['Chainable'] == "NON":
                        st.caption("❌ Non chainable")
                    else:
                        st.caption("✅ Chainable")

                with c2:
                    st.markdown(f"<div class='price-tag'>{row['Prix_Promo']} €</div>", unsafe_allow_html=True)
                    st.caption("Prix Promo (-10%)")
                    
                    # Bouton d'action (Simulation)
                    if st.button(f"Sélectionner", key=row['Ref']):
                        st.success(f"✅ Kit {row['Style']} sélectionné ! Réf copiée.")

else:
    st.warning("En attente du fichier de données...")