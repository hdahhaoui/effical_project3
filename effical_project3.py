import streamlit as st

# Configuration
st.set_page_config(page_title="Calcul Thermique DTR C3.2/4", layout="wide")

# Données de base: matériaux de construction
materiaux = {
    "Mortier de chaux": {"conductivite": 0.87, "masse_volumique": 1800},
    "Carreaux de plâtre pleins": {"conductivite": 1.4, "masse_volumique": 950},
    "Liège compressé": {"conductivite": 0.10, "masse_volumique": 500},
    "Polystyrène expansé": {"conductivite": 0.044, "masse_volumique": 130},
    "Verre": {"conductivite": 0.80, "masse_volumique": 1900},
    "Crépis": {"conductivite": 0.84, "masse_volumique": 1800},
    "Mortier de ciment": {"conductivite": 1.40, "masse_volumique": 2200},
    "Lame d'air": {"conductivite": 1.00, "masse_volumique": 1},
    "Enduit plâtre": {"conductivite": 0.35, "masse_volumique": 1300},
    "Enduit ciment": {"conductivite": 0.87, "masse_volumique": 1400},
    "Béton (lourd)": {"conductivite": 1.75, "masse_volumique": 2350},
    "Béton (pierre pleine)": {"conductivite": 1.75, "masse_volumique": 2200},
    "Béton (allégé)": {"conductivite": 1.29, "masse_volumique": 2350},
    "Brique creuse": {"conductivite": 0.48, "masse_volumique": 900},
    "Brique pleine (moyenne)": {"conductivite": 0.80, "masse_volumique": 1800},
    "Brique silico-calcaire": {"conductivite": 1.00, "masse_volumique": 1900},
    "Carrelage": {"conductivite": 2.10, "masse_volumique": 1900},
    "Sable sec": {"conductivite": 0.60, "masse_volumique": 1300},
    "Gravillon": {"conductivite": 2.00, "masse_volumique": 1500},
    "Mousse de polyuréthane (30kg/m3)": {"conductivite": 0.031, "masse_volumique": 30},
    "Laine de roche (40kg/m3)": {"conductivite": 0.038, "masse_volumique": 40},
    "Laine de verre": {"conductivite": 0.044, "masse_volumique": 9},
    # Métaux (peu utilisés en paroi mais inclus pour info)
    "Acier": {"conductivite": 52.0, "masse_volumique": 7850},
    "Aluminium": {"conductivite": 230.0, "masse_volumique": 2700},
    "Cuivre": {"conductivite": 380.0, "masse_volumique": 8930},
}

# Données de base: wilayas d'Algérie avec groupes de communes et zones climatiques
wilaya = {
    "1-ADRAR": {
        "Groupe 1: TINERKOUK, BORDJ BADJI MOKHTAR": "C",
        "Groupe 2: Toutes les autres communes": "D",
    },
    "2-CHLEF": {
        "Groupe 1: TENES, OUED GHOUSSINE, SIDI ABDERRAHMANE, SIDI AKKACHA": "A1",
        "Groupe 2: Toutes les autres communes": "A",
    },
    "3-LAGHOUAT": {
        "Groupe 1: SIDI MAKHLOUF, EL ASSAFIA, LAGHOUAT, AIN MADHI, KSAR EL HIRANE, MEKHAREG, KHENEG, HASSI DHELAA, EL HAOUAITA, HASSI RMEL": "C",
        "Groupe 2: Toutes les autres communes": "B",
    },
    "4-OUM EL BOUAGHI": {
        "Toutes les communes": "B",
    },
    "5-BATNA": {
        "Groupe 1: METKAOUAK, OULED AMMAR, BARIKA, TILATOU, SEGGANA, BITAM, M'DOUKAL, TIGHARGHAR": "C",
        "Groupe 2: Toutes les autres communes": "B",
    },
    "6-BEJAIA": {
        "Groupe 1: BENI KSILA, TOUDJA, BEJAIA, EL KSEUR, TAOURIRT IGHIL, OUED GHIR, TALA HAMZA": "A1",
        "Groupe 2: Toutes les autres communes": "A",
    },
    "7-BISKRA": {
        "Groupe 1: KHANGAT SIDI NADJI": "B",
        "Groupe 2: Toutes les autres communes": "C",
    },
    "8-BECHAR": {
        "Groupe 1: BENI OUNIF, MOUGHEUL, BOUKAIS, BECHAR, LAHMAR, KENADSA, MERIDJA, TAGHIT, ERG FERRADJ, ABADLA": "C",
        "Groupe 2: Toutes les autres communes": "D",
    },
    "9-BLIDA": {
        "Toutes les communes": "A",
    },
    "10-BOUIRA": {
        "Groupe 1: MEZDOUR, BORDJ OKHRISS, RIDANE, DIRAH, MAAMORA, TAGUEDITE, HADJERA ZERGA": "B",
        "Groupe 2: Toutes les autres communes": "A",
    },
    "11-TAMANRASSET": {
        "Groupe 1: TAZROUK, TAMANRASSET, ABALESSA, TIN ZAOUATENE, IN GUEZZAM": "C",
        "Groupe 2: Toutes les autres communes": "D",
    },
    "12-TEBESSA": {
        "Groupe 1: FERKANE, NEGRINE": "C",
        "Groupe 2: Toutes les autres communes": "B",
    },
    "13-TLEMCEN": {
        "Groupe 1: AIN TALLOUT, OULED MIMOUN, OUED CHOULY, BENI SNOU, SEBDOU, AZAIL, EL GOR, SIDI DJILLALI, EL ARICHA, EL BOUIHI": "B",
        "Groupe 2: Toutes les autres communes": "A",
    },
    "14-TIARET": {
        "Toutes les communes": "B",
    },
    "15-TIZI-OUZOU": {
        "Groupe 1: MIZRANA": "A1",
        "Groupe 2: Toutes les autres communes": "A",
    },
    "16-ALGER": {
        "Toutes les communes": "A",
    },
    "17-DJELFA": {
        "Groupe 1: BENHAR, AIN OUESSARA, BIRINE, AIN FEKKA, EL KHEMIS, HASSI F'DOUL, HAD SAHARY, SIDI LAADJEL, BOUIRA LAHDAB, GUERNINI, HASSI EL EUCH, HASSI BAHBAH, ZAAFRANE, EL GUEDDID, CHAREF, BENI YAGUOB, EL IDRISSIA, DOUIS, AIN CHOUHADA": "B",
        "Groupe 2: OUM LAADHAM, GUETTARA": "D",
        "Groupe 3: Toutes les autres communes": "C",
    },
    "18-JIJEL": {
        "Toutes les communes": "A",
    },
    "19-SETIF": {
        "Groupe 1: (plusieurs communes de haute altitude)": "A",
        "Groupe 2: Toutes les autres communes": "B",
    },
    "20-SAIDA": {
        "Toutes les communes": "B",
    },
    "21-SKIKDA": {
        "Groupe 1: AIN ZOUIT, FIL FILA, SKIKDA, HAMMADI KROUMA, EL HADAIEK": "A1",
        "Groupe 2: Toutes les autres communes": "A",
    },
    "22-SIDI BEL ABBES": {
        "Groupe 1: (plusieurs communes du nord)": "A",
        "Groupe 2: Toutes les autres communes": "B",
    },
    "23-ANNABA": {
        "Toutes les communes": "A",
    },
    "24-GUELMA": {
        "Groupe 1: (quelques communes d'altitude)": "B",
        "Groupe 2: Toutes les autres communes": "A",
    },
    "25-CONSTANTINE": {
        "Groupe 1: EL KHROUB, AIN SMARA, AIN ABID, OULED RAHMOUN": "B",
        "Groupe 2: Toutes les autres communes": "A",
    },
    "26-MEDEA": {
        "Toutes les communes": "B",
    },
    "27-MOSTAGANEM": {
        "Toutes les communes": "A",
    },
    "28-MSILA": {
        "Groupe 1: (plusieurs communes de l'est)": "B",
        "Groupe 2: Toutes les autres communes": "C",
    },
    "29-MASCARA": {
        "Groupe 1: (plusieurs communes du sud-est)": "A",
        "Groupe 2: Toutes les autres communes": "B",
    },
    "30-OUARGLA": {
        "Groupe 1: EL BORMA": "C",
        "Groupe 2: Toutes les autres communes": "D",
    },
    "31-ORAN": {
        "Toutes les communes": "A",
    },
    "32-EL BAYADH": {
        "Groupe 1: BREZINA, EL ABIODH SIDI CHEIKH, EL BNOUD": "C",
        "Groupe 2: Toutes les autres communes": "B",
    },
    "33-ILLIZI": {
        "Toutes les communes": "C",
    },
    "34-BORDJ BOU ARRERIDJ": {
        "Groupe 1: (plusieurs communes du nord)": "A",
        "Groupe 2: Toutes les autres communes": "B",
    },
    "35-BOUMERDES": {
        "Groupe 1: DELLYS, SIDI DAOUD, AFIR, BEN CHOUD, BAGHLIA, OULED AÏSSA, TAOURGA": "A1",
        "Groupe 2: Toutes les autres communes": "A",
    },
    "36-EL TARF": {
        "Groupe 1: EL KALA, BERRIHANE": "A1",
        "Groupe 2: Toutes les autres communes": "A",
    },
    "37-TINDOUF": {
        "Toutes les communes": "D",
    },
    "38-TISSEMSILT": {
        "Groupe 1: LAZHARIA, LARBAA, BOUCAID, BORDJ BOUNAAMA": "A",
        "Groupe 2: Toutes les autres communes": "B",
    },
    "39-EL OUED": {
        "Groupe 1: OUM TOYOUR, EL MGHAIR, SIDI KHELLIL, TENDLA, MRARA, DJAMAA, SIDI AMRANE": "D",
        "Groupe 2: Toutes les autres communes": "C",
    },
    "40-KHENCHELA": {
        "Groupe 1: BABAR": "C",
        "Groupe 2: Toutes les autres communes": "B",
    },
    "41-SOUK AHRAS": {
        "Groupe 1: MECHROHA, AIN ZANA, OULED DRISS": "A",
        "Groupe 2: Toutes les autres communes": "B",
    },
    "42-TIPAZA": {
        "Toutes les communes": "A",
    },
    "43-MILA": {
        "Groupe 1: OUED ATHMENIA, BENYAHIA ABDERRAHMANE, OUED SEGUEN, CHELGHOUM LAID, TADJENANET, TELAGHMA, EL M'CHIRA, OULED KHELLOUF": "B",
        "Groupe 2: Toutes les autres communes": "A",
    },
    "44-AIN DEFLA": {
        "Toutes les communes": "A",
    },
    "45-NAAMA": {
        "Toutes les communes": "B",
    },
    "46-AIN TEMOUCHENT": {
        "Groupe 1: SIDI SAFI, BENI SAF, OULHACA EL GHERABA, AIN TOLBA, EL AMIR ABDELKADER": "A1",
        "Groupe 2: Toutes les autres communes": "A",
    },
    "47-GHARDAIA": {
        "Groupe 1: EL GUERRARA, ZELFANA": "D",
        "Groupe 2: Toutes les autres communes": "C",
    },
    "48-RELIZANE": {
        "Groupe 1: OUED ESSALEM": "B",
        "Groupe 2: Toutes les autres communes": "A",
    },
}

# Utiliser st.session_state pour stocker parois définies et couche en cours
if 'parois' not in st.session_state:
    st.session_state.parois = {}  # dict {paroi_name: {'R_hiver':..., 'U_hiver':..., 'mass':...}}
if 'current_layers' not in st.session_state:
    st.session_state.current_layers = []  # list of (material, thickness) for the paroi being composed

# Fonctions de calcul
def calculate_window_U(window_type, frame_material, gap_option=None):
    """Calcule le U effectif de la fenêtre (W/m².K) en fonction du type de vitrage, du matériau et de l'épaisseur de la lame d'air."""
    if window_type == 'Simple':
        kwin = 5.0 if frame_material == 'Bois' else 5.8
    elif window_type == 'Double':
        if gap_option is None:
            return None
        if frame_material == 'Bois':
            if gap_option.startswith("5"):
                kwin = 3.3
            elif gap_option.startswith("8"):
                kwin = 3.1
            elif gap_option.startswith("10"):
                kwin = 3.0
            else:
                kwin = 2.9
        else:  # Métal/PVC
            if gap_option.startswith("5"):
                kwin = 4.0
            elif gap_option.startswith("8"):
                kwin = 3.9
            elif gap_option.startswith("10"):
                kwin = 3.8
            else:
                kwin = 3.7
    elif window_type == 'Fenetre double':
        kwin = 2.6 if frame_material == 'Bois' else 3.0
    else:
        return None
    # Ajouter les résistances surface intérieure/extérieure + éventuel volet (0.025+0.03+0.16)
    R_additionnelle = 0.025 + 0.03 + 0.16
    U_effectif = 1.0 / ((1.0 / kwin) + R_additionnelle)
    return U_effectif

def get_door_U(door_type, contact):
    """Retourne le coefficient de transmission thermique (W/m².K) de la porte selon son type et son contact (Exterieur ou Local Non Chauffé)."""
    if contact == "Exterieur":
        if door_type == "Portes Opaques en Bois":
            return 3.5
        elif door_type == "Portes Opaques en Metal":
            return 5.8
        elif door_type == "Portes en Bois avec vitrage <30%":
            return 4.0
        elif door_type == "Portes en Bois vitrage 30% à 60%":
            return 4.5
        elif door_type == "Portes en Metal avec vitrage simple":
            return 5.8
    else:  # Local Non Chauffé
        if door_type == "Portes Opaques en Bois":
            return 2.0
        elif door_type == "Portes Opaques en Metal":
            return 4.5
        elif door_type == "Portes en Bois avec vitrage <30%":
            return 2.4
        elif door_type == "Portes en Bois vitrage 30% à 60%":
            return 2.7
        elif door_type == "Portes en Metal avec vitrage simple":
            return 4.5
    return None

# Définition des pages de l'application
pages = [
    "Page d'accueil",
    "Informations Projet",
    "Ajout de Parois",
    "Orientation Nord",
    "Orientation Sud",
    "Orientation Est",
    "Orientation Ouest",
    "Plancher & Toiture",
    "Résultats",
]
# Menu latéral de navigation
st.sidebar.title("Menu")
selected_page = st.sidebar.radio("Aller à la page:", pages, index=0, key='active_page')

# PAGE 1: Page d'accueil
if selected_page == "Page d'accueil":
    st.title("EffiCal - Calcul Thermique des Bâtiments (DTR C3.2/4)")
    st.write("""
    Bienvenue dans l'application **EffiCal** de calcul des déperditions thermiques des bâtiments 
    conformément au DTR C3.2/4. Utilisez le menu latéral pour naviguer entre les sections : 
    renseignez les informations du projet, définissez les parois du bâtiment, puis indiquez les surfaces par orientation. 
    Enfin, consultez les **résultats** détaillés (coefficients U et déperditions par orientation).
    """)
    st.write("Cliquez sur **Informations Projet** pour commencer.")
    # Pas de bouton Retour sur la première page
    if st.button("Suivant ▶️"):
        st.session_state.active_page = "Informations Projet"

# PAGE 2: Informations Projet
elif selected_page == "Informations Projet":
    st.header("Informations du Projet")
    # Formulaire d'informations
    st.text_input("Nom du projet:", key="project_name")
    st.text_input("Site d'implantation:", key="project_site")
    # Type de bâtiment
    building_types = [
        "Logement individuel",
        "Logement en immeubles collectifs, bureaux, locaux à usage d'hébergement"
    ]
    # On ajoute une option vide au début pour forcer le choix explicite (par défaut)
    type_options = ["(Sélectionner)"] + building_types
    btype = st.selectbox("Type de bâtiment:", options=type_options, key="building_type")
    # Sélecteurs de wilaya, groupe et zone
    selected_wilaya = st.selectbox("Wilaya:", options=list(wilaya.keys()), key="wilaya_choice")
    if selected_wilaya:
        group_options = list(wilaya[selected_wilaya].keys())
        selected_group = st.selectbox("Groupe de communes:", options=group_options, key="groupe_choice")
        if selected_group:
            zone_clim = wilaya[selected_wilaya][selected_group]
            st.text_input("Zone climatique:", value=zone_clim, disabled=True)
    # Boutons navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("◀️ Retour"):
            st.session_state.active_page = "Page d'accueil"
    with col2:
        if st.button("Suivant ▶️"):
            # Vérifier que le type de bâtiment est sélectionné
            if st.session_state.get("building_type", "") == "(Sélectionner)":
                st.error("Veuillez sélectionner le type de bâtiment.")
            else:
                st.session_state.active_page = "Ajout de Parois"

# PAGE 3: Ajout de Parois
elif selected_page == "Ajout de Parois":
    st.header("Définition des Parois (Murs, Planchers, Toitures)")
    st.write("Ajoutez la composition des parois (murs extérieurs, planchers bas, toitures, etc.) couche par couche.")
    # Sélection de matériau et épaisseur
    mat_list = list(materiaux.keys())
    mat_choice = st.selectbox("Matériau:", options=mat_list, key="materiau_select")
    thickness = st.number_input("Épaisseur de la couche (m):", min_value=0.0, step=0.01, format="%.3f", key="layer_thickness")
    # Boutons pour ajouter/modifier/supprimer une couche dans la composition en cours
    col_add, col_mod, col_del = st.columns([1,1,1])
    with col_add:
        if st.button("Ajouter la couche"):
            if mat_choice and thickness > 0:
                # Ajouter la couche à la liste en cours
                current = st.session_state.current_layers.copy()
                current.append((mat_choice, thickness))
                st.session_state.current_layers = current
            else:
                st.warning("Sélectionnez un matériau et une épaisseur > 0.")
    with col_mod:
        # Modification: choisir une couche existante
        if st.session_state.current_layers:
            layer_options = [f"Couche {i+1}: {name} ({thick} m)" for i, (name, thick) in enumerate(st.session_state.current_layers)]
            layer_to_mod = st.selectbox("Couche à modifier:", options=layer_options, key="layer_to_modify")
            new_thick = st.number_input("Nouvelle épaisseur (m):", min_value=0.0, step=0.01, format="%.3f", key="new_thickness")
            if st.button("Appliquer modification"):
                idx = layer_options.index(layer_to_mod)
                if new_thick > 0:
                    # Mettre à jour l'épaisseur
                    layers_copy = st.session_state.current_layers.copy()
                    material_name = layers_copy[idx][0]
                    layers_copy[idx] = (material_name, new_thick)
                    st.session_state.current_layers = layers_copy
                else:
                    st.warning("Épaisseur invalide.")
    with col_del:
        if st.session_state.current_layers:
            layer_options2 = [f"Couche {i+1}: {name} ({thick} m)" for i, (name, thick) in enumerate(st.session_state.current_layers)]
            layer_to_del = st.selectbox("Couche à supprimer:", options=layer_options2, key="layer_to_delete")
            if st.button("Supprimer la couche"):
                idx = layer_options2.index(layer_to_del)
                layers_copy = st.session_state.current_layers.copy()
                layers_copy.pop(idx)
                st.session_state.current_layers = layers_copy

    # Afficher la liste des couches actuelle
    if st.session_state.current_layers:
        st.subheader("Composition en cours:")
        for i, (name, thick) in enumerate(st.session_state.current_layers, start=1):
            st.write(f"- Couche {i}: **{name}** – {thick:.3f} m")

    # Choix du type de paroi (position et environnement)
    st.markdown("**Type de paroi et environnement**")
    # Radio pour position de la paroi
    pos = st.radio("Position de la paroi:", ["Mur (vertical)", "Toiture (surface supérieure)", "Plancher (surface inférieure)"], index=0, key="paroi_position")
    contact = st.radio("En contact avec:", ["Extérieur / espace ouvert", "Local non chauffé (combles, vide sanitaire)"], index=0, key="paroi_contact")

    # Entrer un nom pour la paroi complète
    paroi_name = st.text_input("Nom de cette paroi (ex: Mur extérieur brique+isolant):", key="new_paroi_name")
    if st.button("Enregistrer la paroi"):
        if not paroi_name:
            st.warning("Veuillez entrer un nom pour la paroi.")
        elif paroi_name in st.session_state.parois:
            st.error(f"Le nom de paroi '{paroi_name}' existe déjà.")
        elif not st.session_state.current_layers:
            st.error("Aucune couche définie pour cette paroi.")
        else:
            # Calcul de R_total et U
            # Déterminer Rsi et Rse en fonction de la position et du contact
            # Valeurs (m².K/W) selon DTR: 
            # Pour contact extérieur: vertical (Rsi=0.11, Rse=0.06), plafond (Rsi=0.09, Rse=0.05), plancher (Rsi=0.17, Rse=0.05).
            # Pour contact local non chauffé: vertical (Rsi=0.11, Rse=0.11), plafond (Rsi=0.09, Rse=0.09), plancher (Rsi=0.17, Rse=0.17).
            if pos.startswith("Mur"):
                Rsi_hiver = 0.11; Rse_hiver = 0.06 if contact.startswith("Extérieur") else 0.11
                Rsi_ete = 0.10; Rse_ete = 0.04 if contact.startswith("Extérieur") else 0.11
            elif pos.startswith("Toiture"):
                Rsi_hiver = 0.09; Rse_hiver = 0.05 if contact.startswith("Extérieur") else 0.09
                Rsi_ete = 0.16; Rse_ete = 0.04 if contact.startswith("Extérieur") else 0.17
            else:  # Plancher
                Rsi_hiver = 0.17; Rse_hiver = 0.05 if contact.startswith("Extérieur") else 0.17
                Rsi_ete = 0.08; Rse_ete = 0.04 if contact.startswith("Extérieur") else 0.09
            # Calcul R des couches
            R_layers = 0.0
            total_mass = 0.0
            for (mat, ep) in st.session_state.current_layers:
                lamb = materiaux[mat]["conductivite"]
                rho = materiaux[mat]["masse_volumique"]
                if lamb <= 0:
                    continue
                R_layers += ep / lamb
                total_mass += rho * ep  # masse volumique(kg/m3)*épaisseur(m) = kg/m2
            R_total_hiver = R_layers + Rsi_hiver + Rse_hiver
            R_total_ete = R_layers + Rsi_ete + Rse_ete
            U_hiver = 1 / R_total_hiver if R_total_hiver > 0 else None
            U_ete = 1 / R_total_ete if R_total_ete > 0 else None
            # Enregistrer la paroi
            st.session_state.parois[paroi_name] = {
                "R_hiver": R_total_hiver,
                "U_hiver": U_hiver,
                "R_ete": R_total_ete,
                "U_ete": U_ete,
                "masse": total_mass
            }
            # Réinitialiser la composition en cours
            st.session_state.current_layers = []
            st.session_state.new_paroi_name = ""
            st.success(f"Paroi '{paroi_name}' ajoutée (U = {U_hiver:.3f} W/m².K).")
    # Liste des parois déjà enregistrées
    if st.session_state.parois:
        st.subheader("Parois définies:")
        paroi_data = []
        for name, vals in st.session_state.parois.items():
            Uval = vals["U_hiver"]
            mass = vals["masse"]
            paroi_data.append({"Paroi": name, "U (W/m².K)": f"{Uval:.3f}", "Masse surfacique (kg/m²)": f"{mass:.1f}"})
        st.table(paroi_data)
    # Boutons navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("◀️ Retour", key="back_to_info"):
            st.session_state.active_page = "Informations Projet"
    with col2:
        if st.button("Suivant ▶️", key="to_orientations"):
            if not st.session_state.parois:
                st.error("Définissez au moins une paroi avant de continuer.")
            else:
                st.session_state.active_page = "Orientation Nord"

# PAGES 4-7: Orientations cardinales
elif selected_page in ["Orientation Nord", "Orientation Sud", "Orientation Est", "Orientation Ouest"]:
    orientation = selected_page.split()[1]  # "Nord", "Sud", etc.
    st.header(f"Orientation {orientation}")
    st.write(f"Indiquez les surfaces pour la façade **{orientation}**:")
    if not st.session_state.parois:
        st.warning("Veuillez d'abord définir des parois dans la section 'Ajout de Parois'.")
    else:
        # Présence de cette orientation
        present_key = f"{orientation.lower()}_present"
        st.checkbox(f"Présence d'une paroi vers {orientation}", value=True, key=present_key)
        if st.session_state.get(present_key):
            # Sélection du type de paroi pour ce mur
            paroi_options = list(st.session_state.parois.keys())
            paroi_key = f"{orientation.lower()}_paroi"
            st.selectbox(f"Paroi de la façade {orientation}:", options=paroi_options, key=paroi_key)
            area_key = f"{orientation.lower()}_area"
            st.number_input(f"Surface du mur {orientation} (m²):", min_value=0.0, step=1.0, key=area_key)
            # Fenêtres sur cette orientation
            window_area_key = f"{orientation.lower()}_window_area"
            st.number_input(f"Surface totale des fenêtres {orientation} (m²):", min_value=0.0, step=1.0, key=window_area_key)
            if st.session_state.get(window_area_key, 0.0) and st.session_state[window_area_key] > 0:
                # Si surface fenêtre >0, afficher choix du type de fenêtre
                window_type_key = f"{orientation.lower()}_window_type"
                st.selectbox(f"Type de vitrage {orientation}:", ["Simple", "Double", "Fenetre double"], key=window_type_key)
                window_mat_key = f"{orientation.lower()}_window_material"
                st.selectbox(f"Matériau de fenêtre {orientation}:", ["Bois", "Métal"], key=window_mat_key)
                # Si double vitrage, demander l'épaisseur de la lame d'air
                if st.session_state[window_type_key] == "Double":
                    gap_key = f"{orientation.lower()}_gap"
                    st.selectbox("Épaisseur de la lame d'air (mm):", ["5 à 7", "8 à 9", "10 à 11", "12 à 13"], key=gap_key)
            # Portes sur cette orientation
            door_area_key = f"{orientation.lower()}_door_area"
            st.number_input(f"Surface totale des portes {orientation} (m²):", min_value=0.0, step=1.0, key=door_area_key)
            if st.session_state.get(door_area_key, 0.0) and st.session_state[door_area_key] > 0:
                # Choix du type de porte et du contact
                door_type_key = f"{orientation.lower()}_door_type"
                door_types = [
                    "Portes Opaques en Bois",
                    "Portes Opaques en Metal",
                    "Portes en Bois avec vitrage <30%",
                    "Portes en Bois vitrage 30% à 60%",
                    "Portes en Metal avec vitrage simple"
                ]
                st.selectbox(f"Type de porte {orientation}:", options=door_types, key=door_type_key)
                door_cont_key = f"{orientation.lower()}_door_contact"
                st.selectbox(f"Contact de la porte {orientation}:", ["Exterieur", "Local Non Chauffé"], key=door_cont_key)
    # Boutons navigation
    col1, col2 = st.columns(2)
    with col1:
        # Retour: aller à page précédente dans l'ordre du menu
        prev_index = pages.index(selected_page) - 1
        if st.button("◀️ Retour"):
            st.session_state.active_page = pages[prev_index]
    with col2:
        next_index = pages.index(selected_page) + 1
        if st.button("Suivant ▶️"):
            st.session_state.active_page = pages[next_index]

# PAGE 8: Plancher & Toiture
elif selected_page == "Plancher & Toiture":
    st.header("Autres Parois: Plancher bas et Toiture")
    st.write("Indiquez les surfaces de déperdition vers le bas (plancher) et vers le haut (toiture) :")
    if not st.session_state.parois:
        st.warning("Veuillez d'abord définir des parois dans 'Ajout de Parois'.")
    else:
        # Plancher bas
        st.checkbox("Plancher bas présent (vers sol ou volume non chauffé)", value=True, key="floor_present")
        if st.session_state.floor_present:
            st.selectbox("Paroi du plancher bas:", options=list(st.session_state.parois.keys()), key="floor_paroi")
            st.number_input("Surface du plancher bas (m²):", min_value=0.0, step=1.0, key="floor_area")
        # Toiture / Plafond
        st.checkbox("Toiture ou plafond haut présent", value=True, key="roof_present")
        if st.session_state.roof_present:
            st.selectbox("Paroi de la toiture/plafond:", options=list(st.session_state.parois.keys()), key="roof_paroi")
            st.number_input("Surface de la toiture/plafond (m²):", min_value=0.0, step=1.0, key="roof_area")
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("◀️ Retour", key="back_from_autres"):
            st.session_state.active_page = "Orientation Ouest"
    with col2:
        if st.button("Suivant ▶️", key="to_results"):
            st.session_state.active_page = "Résultats"

# PAGE 9: Résultats
elif selected_page == "Résultats":
    st.header("Résultats Finaux")
    # Récapitulatif projet
    st.subheader("Paramètres du projet")
    proj_name = st.session_state.get("project_name", "")
    proj_site = st.session_state.get("project_site", "")
    proj_type = st.session_state.get("building_type", "(non spécifié)")
    if proj_type == "(Sélectionner)":
        proj_type = "(non spécifié)"
    proj_wilaya = st.session_state.get("wilaya_choice", "")
    proj_group = st.session_state.get("groupe_choice", "")
    zone = wilaya[proj_wilaya][proj_group] if proj_wilaya and proj_group else ""
    st.write(f"**Projet**: {proj_name}  \n**Site**: {proj_site}  \n**Type de bâtiment**: {proj_type}")
    st.write(f"**Localisation climatique**: {proj_wilaya} – {proj_group} – Zone {zone}")
    # Vérifier si toutes les données nécessaires sont présentes
    if not st.session_state.parois:
        st.error("Aucune paroi définie.")
    else:
        # Calculer les déperditions pour chaque catégorie
        pertes = {}  # stocker pertes (W) par orientation/élément
        # Fonction auxiliaire pour récupérer U d'une paroi donnée
        def U_paroi(nom):
            return st.session_state.parois[nom]["U_hiver"] if nom in st.session_state.parois else 0.0
        # Cardinales
        for orientation in ["nord", "sud", "est", "ouest"]:
            present_flag = st.session_state.get(f"{orientation}_present", False)
            if present_flag:
                paroi_nom = st.session_state.get(f"{orientation}_paroi")
                surface_mur = st.session_state.get(f"{orientation}_area", 0.0)
                surface_fen = st.session_state.get(f"{orientation}_window_area", 0.0)
                surface_port = st.session_state.get(f"{orientation}_door_area", 0.0)
                # Calcul perte mur
                U_wall = U_paroi(paroi_nom) if paroi_nom else 0.0
                perte_mur = U_wall * surface_mur
                # Fenêtres
                perte_fen = 0.0
                if surface_fen and surface_fen > 0:
                    win_type = st.session_state.get(f"{orientation}_window_type")
                    win_mat = st.session_state.get(f"{orientation}_window_material")
                    gap = st.session_state.get(f"{orientation}_gap", None)
                    Ufen = calculate_window_U(win_type, win_mat, gap if win_type == "Double" else None)
                    perte_fen = Ufen * surface_fen if Ufen else 0.0
                # Portes
                perte_port = 0.0
                if surface_port and surface_port > 0:
                    door_type = st.session_state.get(f"{orientation}_door_type")
                    door_contact = st.session_state.get(f"{orientation}_door_contact", "Exterieur")
                    k_port = get_door_U(door_type, door_contact)
                    perte_port = k_port * surface_port if k_port else 0.0
                pertes[orientation.capitalize()] = perte_mur + perte_fen + perte_port
        # Plancher bas
        if st.session_state.get("floor_present", False):
            paroi_plancher = st.session_state.get("floor_paroi")
            surface_plancher = st.session_state.get("floor_area", 0.0)
            U_plancher = U_paroi(paroi_plancher) if paroi_plancher else 0.0
            pertes["Plancher bas"] = U_plancher * surface_plancher
        # Toiture
        if st.session_state.get("roof_present", False):
            paroi_toit = st.session_state.get("roof_paroi")
            surface_toit = st.session_state.get("roof_area", 0.0)
            U_toit = U_paroi(paroi_toit) if paroi_toit else 0.0
            pertes["Toiture"] = U_toit * surface_toit
        # Affichage des résultats sous forme de tableau
        st.subheader("Déperditions thermiques")
        if not pertes:
            st.write("Aucune déperdition calculée (vérifiez les saisies).")
        else:
            total = 0.0
            result_rows = []
            for elem, perte in pertes.items():
                total += perte
                result_rows.append({"Élément": elem, "Pertes thermiques (W)": f"{perte:.1f}"})
            result_rows.append({"Élément": "Total", "Pertes thermiques (W)": f"{total:.1f}"})
            st.table(result_rows)
            # Diagramme des pertes par élément (hors total)
            st.subheader("Diagramme des pertes par élément")
            try:
                # Utiliser st.bar_chart
                data = {elem: perte for elem, perte in pertes.items()}
                st.bar_chart(data=data)
            except Exception as e:
                st.write("(Diagramme non disponible)")

    # Bouton Retour (permet de revenir pour modifier si besoin)
    if st.button("◀️ Retour (modifier les données)"):
        st.session_state.active_page = "Plancher & Toiture"
