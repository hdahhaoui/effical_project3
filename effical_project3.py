# -*- coding: utf-8 -*-
# Outil de calcul thermique des bâtiments (chauffage) selon la norme DTR C3.2-4
# Ce programme Streamlit permet de saisir les données d'un projet, de définir les parois 
# du bâtiment (composition en couches), de configurer les surfaces par orientation, 
# d'indiquer les pertes par infiltration, puis de calculer les déperditions et la puissance de chauffage.
# Les résultats sont affichés sous forme de tableaux et graphiques, avec possibilité d'export CSV/Excel.

import streamlit as st
import pandas as pd
import plotly.express as px

# Données réglementaires des wilayas d’Algérie : groupes de communes et zones climatiques (DTR C3.2-4)
wilaya_dict = {
    "1-ADRAR": {"Groupe 1: TINERKOUK, BORDJ BADJI MOKHTAR": "C",
                "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "D"},
    "2-CHLEF": {"Groupe 1: TENES, OUED GHOUSSINE, SIDI ABDERRAHMANE, SIDI AKKACHA": "A1",
                "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "3-LAGHOUAT": {"Groupe 1: SIDI MAKHLOUF, EL ASSAFIA, LAGHOUAT, AIN MADHI, KSAR EL HIRANE, MEKHAREG, KHENEG, HASSI DHELAA, EL HAOUAITA, HASSI RMEL": "C",
                   "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "4-OUM EL BOUAGHI": {"Toutes les communes": "B"},
    "5-BATNA": {"Groupe 1: METKAOUAK, OULED AMMAR, BARIKA, TILATOU, SEGGANA, BITAM, M'DOUKAL, TIGHARGHAR": "C",
                "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "6-BEJAIA": {"Groupe 1: BENI KSILA, TOUDJA, BEJAIA, EL KSEUR, TAOURIRT IGHIL, OUED GHIR, TALA HAMZA": "A1",
                 "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "7-BISKRA": {"Groupe 1: KHANGAT SIDI NADJI": "B",
                 "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "C"},
    "8-BECHAR": {"Groupe 1: BENI OUNIF, MOUGHEUL, BOUKAIS, BECHAR, LAHMAR, KENADSA, MERIDJA, TAGHIT, ERG FERRADJ, ABADLA": "C",
                 "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "D"},
    "9-BLIDA": {"Toutes les communes": "A"},
    "10-BOUIRA": {"Groupe 1: MEZDOUR, BORDJ OUKHRISS, RIDANE, DIRAH, MAAMORA, TAGUEDIT, HADJERA ZERGA": "B",
                  "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "11-TAMANRASSET": {"Groupe 1: TAZROUK, TAMANRASSET, ABALESSA, TIN ZAOUATINE, IN GUEZZAM": "C",
                       "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "D"},
    "12-TEBESSA": {"Groupe 1: FERKANE, NEGRINE": "C",
                   "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "13-TLEMCEN": {"Groupe 1: AIN TALLOUT, OULED MIMOUN, OUED CHOULY, BENI SEMIEL, TERNI BENI HEDIEL, AIN GHORABA, BENI BOUSSAID, BENI BAHDEL, BENI SNOUS, SEBDOU, AZAIS, EL GOR, SIDI DJILLALI, EL ARICHA, EL BOUIHI": "B",
                   "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "14-TIARET": {"Toutes les communes": "B"},
    "15-TIZI-OUZOU": {"Groupe 1: MIZRANA": "A1",
                      "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "16-ALGER": {"Toutes les communes": "A"},
    "17-DJELFA": {"Groupe 1: BENHAR, AIN OUESSARA, BIRINE, AIN FEKKA, EL KHEMIS, HASSI FDOUL, HAD SAHARY, SIDI LAADJEL, BOUIRA LAHDAB, GUERNINI, HASSI EL EUCH, HASSI BAHBAH, ZAAFRANE, EL GUEDDID, CHAREF, BENI YAGOUB, EL IDRISSIA, DOUIS, AIN CHOUHADA": "B",
                  "Groupe 2: OUM LAADHAM, GUETTARA": "D",
                  "Groupe 3: Toutes les communes autres que celles figurant aux groupes 1 et 2": "C"},
    "18-JIJEL": {"Toutes les communes": "A"},
    "19-SETIF": {"Groupe 1: BABOR, AIT TIZI, MZADA, AIN SEBT, SERDJ EL GHOUL, OUED EL BARED, BENI MOUHLI, BOUANDAS, BENI AZIZ, BOUSSELAM, BENI CHEBANA, TALA IFACENE, BENI OUARTILANE, TIZI N'BECHAR, DRAA KEBILA, AIN LAGRADJ, MAOUKLANE, MAAOUIA, DEHAMCHA, AMOUCHA, AIN EL KEBIRA, DJEMILA, HAMMAM GUERGOUR, AIN ROUA, HARBIL, AIN ABESSA, BOUGAA, GUENZET, TASSAMEURT, OULED ADDOUANE, BENI FOUDA, EL OURICIA, BENI HOCINE, TACHOUDA": "A",
                  "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "20-SAIDA": {"Toutes les communes": "B"},
    "21-SKIKDA": {"Groupe 1: AIN ZOUIT, FIL FILA, SKIKDA, HAMMADI KROUMA, EL HADAIEK": "A1",
                  "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "22-SIDI BEL ABBES": {"Groupe 1: MAKEDRA, AIN EL BERD, BOUDJEBAA EL BORDJ, AIN ADDEN, AIN THRID, SIDI HAMADOUCHE, TESSALA, ZEROUALA, SFISEF, SIDI BRAHIM, SEHALA THAOURA, SIDI LAHCENE, SIDI BEL ABBES, MOSTEFA BEN BRAHIM, TILMOUNI, SIDI DAHO, SIDI YACOUB, AIN KADA, BELARBI, AMARNAS, SIDI KHALED, SIDI ALI BOUSSIDI, BOUKANEFIS, LAMTAR, HASSI ZAHANA, BEDRABINE EL MOKRANI": "A",
                        "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "23-ANNABA": {"Toutes les communes": "A"},
    "24-GUELMA": {"Groupe 1: HAMMAM NBAIL, OUED CHEHAM, KHEZARA, OUED ZENATI, DAHOUARA, AIN LARBI, AIN REGGADA, BOUHACHANA, AIN SANDEL, AIN MAKHLOUF, TAMLOUKA": "B",
                  "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "25-CONSTANTINE": {"Groupe 1: EL KHROUB, AIN SMARA, AIN ABID, OULED RAHMOUN": "B",
                       "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "26-MEDEA": {"Toutes les communes": "B"},
    "27-MOSTAGANEM": {"Toutes les communes": "A"},
    "28-MSILA": {"Groupe 1: HAMMAM DHALAA, BENI ILMENE, OUENOUGHA, SIDI AISSA, TARMOUNT, MAADID, BOUTI SAYEH, OULED ADDI GUEBALA, DEHAHNA, MAGRA, BERHOUM, BELAIBA": "B",
                 "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "C"},
    "29-MASCARA": {"Groupe 1: MOCTADOUZ, EL GHOMRI, SIDI ABDELMOUMENE, ALAIMIA, RAS EL AIN AMIROUCHE, SEDJERARA, MOHAMMADIA, OGGAZ, BOUHANIFIA, EL MENAOUER, SIG, ZAHANA, EL BORDJ, AIN FARES, HACINE, EL MAMOUNIA, FERRAGUIG, SIDI ABDELDJEBAR, SEHAILI, CHORFA, EL GAADA, KHALOUIA, EL GUEITNA, TIGHENNIF, MAOUSSA, MASCARA, EL KEURT, TIZI, BOUHANIFIA": "A",
                 "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "30-OUARGLA": {"Groupe 1: EL BORMA": "C",
                   "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "D"},
    "31-ORAN": {"Toutes les communes": "A"},
    "32-EL BAYADH": {"Groupe 1: BREZINA, EL ABIODH SIDI CHEIKH, EL BNOUD": "C",
                     "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "33-ILLIZI": {"Toutes les communes": "C"},
    "34-BORDJ BOU ARRERIDJ": {"Groupe 1: EL MAIN, DJAAFRA, TAFREG, KHELIL, TESMART, BORDJ ZEMOURA, COLLA, OULED SIDI BRAHIM, OULED DAHMANE, THENIET EL ANSEUR, HARAZA": "A",
                              "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "35-BOUMERDES": {"Groupe 1: DELLYS, SIDI DAOUD, AFIR, BEN CHOUD, BAGHLIA, OULED AISSA, TAOURGA": "A1",
                     "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "36-EL TARF": {"Groupe 1: EL KALA, BERRIHANE": "A1",
                   "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "37-TINDOUF": {"Toutes les communes": "D"},
    "38-TISSEMSILT": {"Groupe 1: LAZHARIA, LARBAA, BOUCAID, BORDJ BOUNAAMA": "A",
                      "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "39-EL OUED": {"Groupe 1: OUM TIOUR, EL MGHAIR, SIDI KHELLIL, TENDLA, MRARA, DJAMAA, SIDI AMRANE": "D",
                   "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "C"},
    "40-KHENCHELA": {"Groupe 1: BABAR": "C",
                     "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "41-SOUK AHRAS": {"Groupe 1: MECHROHA, AIN ZANA, OULED DRISS": "A",
                      "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "42-TIPAZA": {"Toutes les communes": "A"},
    "43-MILA": {"Groupe 1: OUED ATHMANIA, BENYAHIA ABDERRAHMANE, OUED SEGUEN, CHELGHOUM LAID, TADJENANET, TELAGHMA, EL M'CHIRA, OULED KHELLOUF": "B",
                "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "44-AIN DEFLA": {"Toutes les communes": "A"},
    "45-NAAMA": {"Toutes les communes": "B"},
    "46-AIN TEMOUCHENT": {"Groupe 1: SIDI SAFI, BENI SAF, OULHACA EL GHARBIA, AIN EL TOLBA, EL EMIR ABDELKADER": "A1",
                          "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "47-GHARDAIA": {"Groupe 1: EL GUERRARA, ZELFANA": "D",
                    "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "C"},
    "48-RELIZANE": {"Groupe 1: OUED ESSALEM": "B",
                    "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "49-TIMIMOUN": {"Toutes les communes": "D"},
    "50-BORDJ BADJI MOKHTAR": {"Toutes les communes": "C"},
    "51-OULED DJELLAL": {"Toutes les communes": "C"},
    "52-BENI ABBES": {"Toutes les communes": "D"},
    "53-IN SALAH": {"Toutes les communes": "D"},
    "54-IN GUEZZAM": {"Toutes les communes": "C"},
    "55-TOUGGOURT": {"Toutes les communes": "D"},
    "56-DJANET": {"Toutes les communes": "C"},
    "57-EL MGHAIR": {"Toutes les communes": "D"},
    "58-EL MENIAA": {"Toutes les communes": "C"}
}

# Correspondance zone climatique -> température extérieure de base (hiver) en °C, selon altitude (m)
temp_ext_map = {
    "A": [(300, 3), (450, 2), (600, 1), (800, 0), (float('inf'), -1.5)],
    "A1": [(300, 7), (450, 6), (600, 5), (800, 4), (float('inf'), 2.5)],
    "B": [(450, -2), (600, -3), (800, -4), (float('inf'), -5.5)],
    "C": [(300, 1), (450, 0), (600, -1), (800, -2), (float('inf'), -4.5)],
    "D": [(300, 4), (450, 3), (600, 2), (800, 1), (float('inf'), -0.5)]
}

# Matériaux disponibles (conductivité thermique en W/m.K et masse volumique en kg/m³)
materials = {
    "Mortier de chaux": {"conductivite": 0.87, "masse volumique": 1800},
    "Carreaux de plâtre pleins": {"conductivite": 1.4, "masse volumique": 950},
    "Liège comprimé": {"conductivite": 0.10, "masse volumique": 500},
    "Polystyrène expansé": {"conductivite": 0.044, "masse volumique": 130},
    "Verre": {"conductivite": 0.80, "masse volumique": 1900},
    "Crépis (ciment+sable)": {"conductivite": 0.84, "masse volumique": 1800},
    "Mortier de ciment": {"conductivite": 1.40, "masse volumique": 2200},
    "Lame d'air": {"conductivite": 1.00, "masse volumique": 1},
    "Enduit plâtre": {"conductivite": 0.35, "masse volumique": 1300},
    "Enduit ciment": {"conductivite": 0.87, "masse volumique": 1400},
    "Béton (plein)": {"conductivite": 1.75, "masse volumique": 2200},
    "Brique creuse": {"conductivite": 0.48, "masse volumique": 900},
    "Brique pleine": {"conductivite": 0.80, "masse volumique": 1800},
    "Carrelage": {"conductivite": 2.10, "masse volumique": 1900},
    "Sable sec": {"conductivite": 0.60, "masse volumique": 1300},
    "Gravillon": {"conductivite": 2.00, "masse volumique": 1500},
    "Mousse de polyuréthane": {"conductivite": 0.031, "masse volumique": 30},
    "Laine de roche": {"conductivite": 0.040, "masse volumique": 40},
    "Laine de verre": {"conductivite": 0.044, "masse volumique": 20},
    "Fer (acier)": {"conductivite": 50.0, "masse volumique": 7850},
    "Aluminium": {"conductivite": 230.0, "masse volumique": 2700}
}

# Initialisation de l'état de session (sauvegarde des données entre pages)
if 'page' not in st.session_state:
    st.session_state.page = 1
    st.session_state.wall_comps = {}   # Dictionnaire des parois définies (composition)
    st.session_state.temp_layers = []  # Couches temporaires pour la paroi en cours de création

# Fonctions de navigation pour les boutons Suivant/Retour
def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1

# ----- Page 1 : Informations générales du projet -----
if st.session_state.page == 1:
    st.title("Calcul thermique - DTR C3.2-4")
    st.header("1. Informations Générales du Projet")
    # Saisie des informations de base du projet
    st.text_input("Nom du projet :", key='project_name')
    # Sélection de la wilaya et du groupe de communes
    wilaya_names = list(wilaya_dict.keys())
    selected_wilaya = st.selectbox("Wilaya", wilaya_names, key='selected_wilaya')
    group_names = list(wilaya_dict[selected_wilaya].keys())
    selected_group = st.selectbox("Groupe de communes", group_names, key='selected_group')
    # Affichage de la zone climatique correspondante
    if selected_group:
        zone = wilaya_dict[selected_wilaya][selected_group]
        st.write(f"Zone climatique : **{zone}**")
        st.session_state.zone = zone
    # Saisie de l'altitude et latitude du site
    st.number_input("Altitude du site (m)", value=0, step=1, key='altitude')
    st.number_input("Latitude du site (°)", value=0.0, step=0.1, key='latitude')
    # Type de bâtiment et type de site d'implantation
    st.selectbox("Type de bâtiment", 
                 ["Logement individuel", "Logement en immeuble collectif", "Bureaux", "Locaux à usage d'hébergement", "Autre"], 
                 key='building_type')
    st.selectbox("Site d'implantation", 
                 ["Centre des grandes villes", "Zones urbaines/industrielles/forêts", "Zones rurales arborées", "Rase campagne/aéroport", "Bord de mer"], 
                 key='site_location')
    # Bouton Suivant pour passer à la page 2
    st.button("Suivant ➞", on_click=next_page)
# ----- Page 2 : Définition des parois (composition des murs) -----
elif st.session_state.page == 2:
    st.header("2. Définition des Parois et Matériaux")
    st.write("**Créer une nouvelle paroi en ajoutant des couches de matériaux :**")
    # Nom de la paroi à créer
    st.text_input("Nom de la paroi", key='wall_name')
    # Choix d'un matériau et épaisseur de la couche à ajouter
    st.selectbox("Matériau de la couche", list(materials.keys()), key='material_selected')
    st.number_input("Épaisseur de la couche (mètres)", value=0.0, step=0.01, key='layer_thickness')
    # Bouton pour ajouter la couche à la paroi en cours
    if st.button("Ajouter la couche"):
        mat = st.session_state.material_selected
        ep = st.session_state.layer_thickness
        if mat and ep > 0:
            st.session_state.temp_layers.append((mat, ep))
        else:
            st.warning("Veuillez sélectionner un matériau et une épaisseur positive.")
    # Affichage des couches ajoutées pour la paroi en cours de création
    if st.session_state.temp_layers:
        st.write("Couches actuelles de la paroi :")
        for mat, ep in st.session_state.temp_layers:
            st.write(f"- {mat} : {ep*100:.1f} cm")
    # Bouton pour terminer la définition de la paroi (calcul R, U, masse et enregistrement)
    if st.button("Terminer la paroi"):
        if not st.session_state.wall_name:
            st.warning("Veuillez indiquer un nom pour la paroi.")
        elif not st.session_state.temp_layers:
            st.warning("Veuillez ajouter au moins une couche avant d'enregistrer la paroi.")
        else:
            # Calcul de la résistance thermique (R) et de la masse surfacique
            R_mat = 0.0
            weight = 0.0
            for mat, ep in st.session_state.temp_layers:
                k = materials[mat]["conductivite"]
                rho = materials[mat]["masse volumique"]
                R_mat += ep / k
                weight += rho * ep
            # Calcul du coefficient U (W/m²K) en supposant paroi extérieure (Rsi=0.13, Rse=0.04)
            U = 0.0
            Rsi_ref = 0.13
            Rse_ref = 0.04
            if R_mat > 0:
                U = 1.0 / (Rsi_ref + R_mat + Rse_ref)
            # Enregistrer la paroi dans le dictionnaire avec ses propriétés
            name = st.session_state.wall_name
            st.session_state.wall_comps[name] = {"R": R_mat, "U": U, "masse": weight}
            # Réinitialiser les champs pour pouvoir saisir une autre paroi
            st.session_state.temp_layers = []
            st.session_state.wall_name = ""
            st.success(f"Paroi '{name}' enregistrée.")
    # Affichage du tableau des parois déjà définies
    if st.session_state.wall_comps:
        st.subheader("Parois définies :")
        df_walls = pd.DataFrame([
            {
                "Paroi": name,
                "R (m²·K/W)": f"{data['R']:.2f}",
                "U (W/m²·K)": f"{data['U']:.2f}",
                "Masse surfacique (kg/m²)": f"{data['masse']:.1f}"
            } for name, data in st.session_state.wall_comps.items()
        ])
        st.table(df_walls)
    # Boutons de navigation Précédent/Suivant
    col1, col2 = st.columns(2)
    with col1:
        st.button("⬅️ Retour", on_click=prev_page)
    with col2:
        st.button("Suivant ➞", on_click=next_page)

# ----- Page 3 : Configuration des murs par orientation -----
elif st.session_state.page == 3:
    st.header("3. Configuration des Murs par Orientation")
    st.write("**Indiquez pour chaque orientation la paroi utilisée et les ouvertures :**")
    orientations = [("Nord", True), ("Est", True), ("Sud", True), ("Ouest", True), ("Plancher", False), ("Toiture", False)]
    for orient, is_vertical in orientations:
        st.subheader(f"Orientation {orient}")
        # Sélection du milieu extérieur ou local non chauffé pour cette paroi
        env = st.selectbox(f"Milieu en contact ({orient})", ["Extérieur", "Local non chauffé"], key=f"{orient}_env")
        if env == "Local non chauffé":
            st.number_input(f"Température du local non chauffé adjacente ({orient}) [°C]", value=10.0, step=1.0, key=f"{orient}_T_unheated")
        # Choix du type de paroi (composition) pour cette orientation
        wall_choices = list(st.session_state.wall_comps.keys())
        if wall_choices:
            st.selectbox(f"Type de paroi pour le mur {orient}", wall_choices, key=f"{orient}_wall")
        else:
            st.warning("⚠️ Aucune paroi définie. Veuillez retourner à l'étape précédente pour définir les parois.")
        # Saisie des surfaces et caractéristiques des ouvertures sur ce mur
        st.number_input(f"Surface du mur {orient} (m²)", value=0.0, step=1.0, key=f"{orient}_area_wall")
        st.number_input(f"Surface des fenêtres {orient} (m²)", value=0.0, step=1.0, key=f"{orient}_area_window")
        st.number_input(f"Coefficient U des fenêtres {orient} (W/m²·K)", value=3.0, step=0.1, key=f"{orient}_U_window")
        st.number_input(f"Surface des portes {orient} (m²)", value=0.0, step=1.0, key=f"{orient}_area_door")
        st.number_input(f"Coefficient U des portes {orient} (W/m²·K)", value=2.0, step=0.1, key=f"{orient}_U_door")
    # Boutons de navigation
    col1, col2 = st.columns(2)
    with col1:
        st.button("⬅️ Retour", on_click=prev_page)
    with col2:
        st.button("Suivant ➞", on_click=next_page)

# ----- Page 4 : Déperditions par renouvellement d'air / infiltrations -----
elif st.session_state.page == 4:
    st.header("4. Déperditions par Renouvellement d'air / Infiltrations")
    st.write("**Indiquez le volume du bâtiment et le taux de renouvellement d'air :**")
    # Volume chauffé du bâtiment
    st.number_input("Volume intérieur chauffé (m³)", value=100.0, step=10.0, key='volume')
    # Taux de renouvellement d'air (volumes par heure)
    st.number_input("Taux de renouvellement d'air (vol/h)", value=1.0, step=0.1, key='air_change_rate')
    st.caption("(Par défaut, ~1 vol/h correspond à une infiltration moyenne dans un bâtiment résidentiel.)")
    # Boutons de navigation
    col1, col2 = st.columns(2)
    with col1:
        st.button("⬅️ Retour", on_click=prev_page)
    with col2:
        st.button("Calculer ➞", on_click=next_page)

# ----- Page 5 : Résultats des déperditions et puissance de chauffage -----
elif st.session_state.page == 5:
    st.header("5. Résultats du Calcul Thermique")
    # Calcul de la température extérieure de base en fonction de la zone et de l'altitude
    zone = st.session_state.get('zone')
    alt = st.session_state.get('altitude', 0)
    Te = None
    if zone in temp_ext_map:
        for (alt_max, temp) in temp_ext_map[zone]:
            if alt <= alt_max:
                Te = temp
                break
    if Te is None:
        Te = temp_ext_map.get(zone, [(float('inf'), 0)])[0][1]  # par défaut 0 si zone non définie
    Ti = 20  # Température intérieure de calcul (par défaut 20°C)
    # Initialisation des cumuls de déperdition
    total_walls = 0.0
    total_windows = 0.0
    total_doors = 0.0
    roof_loss = 0.0
    floor_loss = 0.0
    # Calcul des déperditions par transmission pour chaque orientation
    for orient, is_vertical in [("Nord", True), ("Est", True), ("Sud", True), ("Ouest", True), ("Plancher", False), ("Toiture", False)]:
        wall_name = st.session_state.get(f"{orient}_wall")
        if wall_name:
            # R de la paroi (somme des résistances des couches)
            R_mat = st.session_state.wall_comps.get(wall_name, {}).get("R", 0.0)
            area_wall = st.session_state.get(f"{orient}_area_wall", 0.0)
            area_win = st.session_state.get(f"{orient}_area_window", 0.0)
            U_win = st.session_state.get(f"{orient}_U_window", 0.0)
            area_door = st.session_state.get(f"{orient}_area_door", 0.0)
            U_door = st.session_state.get(f"{orient}_U_door", 0.0)
            env = st.session_state.get(f"{orient}_env", "Extérieur")
            T_unh = st.session_state.get(f"{orient}_T_unheated", None)
            # Calcul du U de la paroi en fonction du milieu (extérieur ou local non chauffé)
            if env == "Extérieur":
                # Coefficients de surface int/ext selon orientation
                if is_vertical:
                    Rsi = 0.13  # paroi verticale intérieure
                    Rse = 0.04  # extérieur (vent moyen)
                else:
                    if orient == "Toiture":   # plafond (plafond chauffé, horizontal vers le haut)
                        Rsi = 0.10
                        Rse = 0.04
                    elif orient == "Plancher":  # plancher bas (chaleur vers le bas, extérieur ou sol)
                        Rsi = 0.17
                        Rse = 0.04
                    else:
                        Rsi = 0.13
                        Rse = 0.04
                U_wall = 0.0
                if R_mat >= 0:
                    U_wall = 1.0 / (Rsi + R_mat + Rse)
                Q_wall = U_wall * area_wall * (Ti - Te)
            else:
                # Paroi adjacente à un local non chauffé : deux faces internes
                if is_vertical:
                    Rsi_int = 0.13
                    Rsi_unh = 0.13
                else:
                    if orient == "Toiture":    # plafond sous comble non chauffé
                        Rsi_int = 0.10
                        Rsi_unh = 0.17
                    elif orient == "Plancher":  # plancher sur sous-sol non chauffé
                        Rsi_int = 0.17
                        Rsi_unh = 0.10
                    else:
                        Rsi_int = 0.13
                        Rsi_unh = 0.13
                U_wall = 0.0
                if R_mat >= 0:
                    U_wall = 1.0 / (Rsi_int + R_mat + Rsi_unh)
                # Température du local non chauffé (utilise la valeur fournie ou calcul du tau si non renseignée)
                if T_unh is None:
                    # Si non spécifié, on estime T_unh = (Ti + Te)/2 (approximation)
                    T_unh = (Ti + Te) / 2.0
                Q_wall = U_wall * area_wall * (Ti - T_unh)
            # Déperdition par les fenêtres et portes de cette orientation (toujours vers extérieur)
            Q_window = U_win * area_win * (Ti - Te)
            Q_door = U_door * area_door * (Ti - Te)
            # Ajout aux sommes selon le type d'élément
            if orient in ["Nord", "Sud", "Est", "Ouest"]:
                total_walls += Q_wall
                total_windows += Q_window
                total_doors += Q_door
            elif orient == "Toiture":
                roof_loss += (Q_wall + Q_window + Q_door)
            elif orient == "Plancher":
                floor_loss += (Q_wall + Q_window + Q_door)
    # Calcul de la déperdition par renouvellement d'air (infiltration)
    volume = st.session_state.get('volume', 0.0)
    air_change = st.session_state.get('air_change_rate', 0.0)
    Q_infil = 0.34 * air_change * volume * (Ti - Te)  # 0.34 W/m³K * volume * taux * ΔT
    # Total des déperditions (W)
    total_loss = total_walls + total_windows + total_doors + roof_loss + floor_loss + Q_infil
    # Résultats par type d'élément pour affichage
    losses = {
        "Murs (opaques verticaux)": total_walls,
        "Fenêtres": total_windows,
        "Portes": total_doors,
        "Toiture (plafond)": roof_loss,
        "Sol (plancher bas)": floor_loss,
        "Infiltration (air)": Q_infil
    }
    # Tableau récapitulatif des déperditions par type d'élément
    st.subheader("Déperditions par catégorie d'élément")
    df_res = pd.DataFrame([
        {"Élément": elem, "Déperdition (W)": round(val, 1), "Pourcentage": (f"{(val/total_loss*100):.1f}%" if total_loss > 0 else "0%")}
        for elem, val in losses.items()
    ])
    st.table(df_res)
    # Graphiques de répartition des déperditions
    st.subheader("Répartition des Déperditions (graphique)")
    fig_bar = px.bar(x=list(losses.keys()), y=list(losses.values()),
                     labels={"x": "Élément", "y": "Déperdition (W)"},
                     title="Déperditions par élément")
    fig_pie = px.pie(values=list(losses.values()), names=list(losses.keys()), title="Répartition des pertes thermiques")
    st.plotly_chart(fig_bar, use_container_width=True)
    st.plotly_chart(fig_pie, use_container_width=True)
    # Affichage de la puissance de chauffage estimée
    st.subheader("Puissance de Chauffage Estimée")
    st.write(f"**{total_loss/1000:.2f} kW** nécessaires pour maintenir **{Ti}°C** à l'intérieur par **{Te}°C** extérieur.")
    # ----- Export des résultats et des données d'entrée -----
    st.subheader("Exporter les résultats complets")
    # Préparation du fichier CSV
    import io
    output_csv = io.StringIO()
    # Écrire les données d'entrée dans le CSV
    output_csv.write("Paramètre,Valeur\n")
    output_csv.write(f"Nom du projet,{st.session_state.get('project_name','')}\n")
    output_csv.write(f"Wilaya,{st.session_state.get('selected_wilaya','')}\n")
    output_csv.write(f"Groupe de communes,{st.session_state.get('selected_group','')}\n")
    output_csv.write(f"Zone climatique,{st.session_state.get('zone','')}\n")
    output_csv.write(f"Altitude (m),{alt}\n")
    output_csv.write(f"Latitude (°),{st.session_state.get('latitude','')}\n")
    output_csv.write(f"Type de bâtiment,{st.session_state.get('building_type','')}\n")
    output_csv.write(f"Site d'implantation,{st.session_state.get('site_location','')}\n")
    output_csv.write(f"Température intérieure de calcul (°C),{Ti}\n")
    output_csv.write(f"Température extérieure de calcul (°C),{Te}\n")
    output_csv.write(f"Volume chauffé (m³),{volume}\n")
    output_csv.write(f"Taux de renouvellement d'air (vol/h),{air_change}\n")
    output_csv.write("\nDéperditions par élément (W)\n")
    for elem, val in losses.items():
        output_csv.write(f"{elem},{val:.1f}\n")
    output_csv.write(f"Déperdition totale (W),{total_loss:.1f}\n")
    output_csv.write(f"Puissance de chauffage estimée (kW),{total_loss/1000:.2f}\n")
    csv_data = output_csv.getvalue().encode('utf-8')
    st.download_button("Télécharger le CSV", data=csv_data, file_name="resultats_calcul_thermique.csv", mime="text/csv")
    # Préparation du fichier Excel (.xlsx)
    output_xls = io.BytesIO()
    writer = pd.ExcelWriter(output_xls, engine='xlsxwriter')
    # Feuille 1: Données d'entrée
    input_data = [
        ["Nom du projet", st.session_state.get('project_name', "")],
        ["Wilaya", st.session_state.get('selected_wilaya', "")],
        ["Groupe de communes", st.session_state.get('selected_group', "")],
        ["Zone climatique", st.session_state.get('zone', "")],
        ["Altitude (m)", alt],
        ["Latitude (°)", st.session_state.get('latitude', "")],
        ["Type de bâtiment", st.session_state.get('building_type', "")],
        ["Site d'implantation", st.session_state.get('site_location', "")],
        ["Température intérieure (°C)", Ti],
        ["Température extérieure (°C)", Te],
        ["Volume chauffé (m³)", volume],
        ["Taux de renouvellement d'air (vol/h)", air_change]
    ]
    df_input = pd.DataFrame(input_data, columns=["Paramètre", "Valeur"])
    df_input.to_excel(writer, index=False, sheet_name="Données d'entrée")
    # Feuille 2: Résultats de déperdition
    df_out = pd.DataFrame([
        [elem, round(val, 1), (f"{(val/total_loss*100):.1f}%" if total_loss > 0 else "0%")]
        for elem, val in losses.items()
    ], columns=["Élément", "Déperdition (W)", "Pourcentage"])
    # Ajouter la ligne total au tableau des résultats
    df_out = pd.concat([df_out, pd.DataFrame([["Total", round(total_loss, 1), "100%"]], columns=df_out.columns)], ignore_index=True)
    df_out.to_excel(writer, index=False, sheet_name="Résultats")
    writer.save()
    xls_data = output_xls.getvalue()
    st.download_button("Télécharger le fichier Excel", data=xls_data, file_name="resultats_calcul_thermique.xlsx", mime="application/vnd.ms-excel")

