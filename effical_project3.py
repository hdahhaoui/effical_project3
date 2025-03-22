import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io, csv

# Données des matériaux (conductivité en W/m.K, masse volumique en kg/m3)
materiaux = {
    "Mortier de chaux": {"conductivite": 0.87, "masse_volumique": 1800},
    "Carreaux de plâtre pleins": {"conductivite": 1.4, "masse_volumique": 950},
    "Liège Comprimé": {"conductivite": 0.1, "masse_volumique": 500},
    "Expansé pur": {"conductivite": 0.044, "masse_volumique": 130},
    "Verre": {"conductivite": 0.80, "masse_volumique": 1900},
    "Crépis": {"conductivite": 0.84, "masse_volumique": 3800},
    "Mortier de ciment": {"conductivite": 1.4, "masse_volumique": 2200},
    "Lame d'air": {"conductivite": 1.0, "masse_volumique": 1},
    "Enduit plâtre": {"conductivite": 0.35, "masse_volumique": 1300},
    "Enduit de ciment": {"conductivite": 0.87, "masse_volumique": 1400},
    "Béton lourd 1": {"conductivite": 1.75, "masse_volumique": 2350},
    "Béton plein": {"conductivite": 1.75, "masse_volumique": 2200},
    "Béton lourd 2": {"conductivite": 1.29, "masse_volumique": 2350},
    "Brique creuses": {"conductivite": 0.48, "masse_volumique": 900},
    "Brique pleine 1": {"conductivite": 0.8, "masse_volumique": 1700},
    "Brique pleine 2": {"conductivite": 1.00, "masse_volumique": 1900},
    "Brique pleine 3": {"conductivite": 1.10, "masse_volumique": 2000},
    "Carrelage": {"conductivite": 2.10, "masse_volumique": 1900},
    "Sable sec": {"conductivite": 0.60, "masse_volumique": 1300},
    "Gravillon": {"conductivite": 2.0, "masse_volumique": 1500},
    "Mousse de polyréthane 1": {"conductivite": 0.031, "masse_volumique": 29},
    "Mousse de polyréthane 2": {"conductivite": 0.034, "masse_volumique": 50},
    "Laine de roche 1": {"conductivite": 0.047, "masse_volumique": 23},
    "Laine de roche 2": {"conductivite": 0.041, "masse_volumique": 30},
    "Laine de roche 3": {"conductivite": 0.038, "masse_volumique": 58},
    "Laine de verre": {"conductivite": 0.044, "masse_volumique": 9},
    "Fer pur": {"conductivite": 72.0, "masse_volumique": 7870},
    "Acier": {"conductivite": 52.0, "masse_volumique": 7780},
    "Fonte": {"conductivite": 56.0, "masse_volumique": 7500},
    "Aluminium": {"conductivite": 230.0, "masse_volumique": 2700},
    "Cuivre": {"conductivite": 380.0, "masse_volumique": 8930},
    "Plomb": {"conductivite": 35.0, "masse_volumique": 11340}
}

# Dictionnaire des wilayas et zones climatiques (DTR C3.2-4)
wilaya = {
    "1-ADRAR": {"Groupe 1: TINERKOUK, BORDJ BADJI MOKHTAR": "C", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "D"},
    "2-CHLEF": {"Groupe 1: TENES, OUED GHOUSSINE, SIDI ABDERRAHMANE, SIDI AKKACHA": "A1", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "3-LAGHOUAT": {"Groupe 1: SIDI MAKHLOUF, EL ASSAFIA, LAGHOUAT, AIN MADHI, KSAR EL HIRANE, MEKHAREG, KHENEG, HASSI DHELAA, EL HAOUAITA, HASSI RMEL": "C", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "4-OUM EL BOUAGHI": {"Toutes les communes": "B"},
    "5-BATNA": {"Groupe 1: METKAOUAK, OULED AMMAR, BARIKA, TILATOU, SEGGANA, BITAM, MDOUKAL, TIGHARGHAR": "C", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "6-BEJAIA": {"Groupe 1: BENI KSILA, TOUDJA, BEJAIA, EL KSEUR, TAOURIRT IGHIL, OUED GHIR, TALA HAMZA": "A1", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "7-BISKRA": {"Groupe 1: KHANGAT SIDI NADJI": "B", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "C"},
    "8-BECHAR": {"Groupe 1: BENI OUNIF, MOUGHEUL, BOUKAIS, BECHAR, LAHMAR, KENADSA, MERIDJA, TAGHIT, ERG FERRADJ, ABADLA": "C", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "D"},
    "9-BLIDA": {"Toutes les communes": "A"},
    "10-BOUIRA": {"Groupe 1: MEZDOUR, BORDJ OUKHRISS, RIDANE, DIRAH, MAAMORA, TAGUEDIT, HADJERA ZERGA": "B", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "11-TAMANRASSET": {"Groupe 1: TAZROUK, TAMANRASSET, ABALESSA, TIN ZAOUATINE, IN GUEZZAM": "C", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "D"},
    "12-TEBESSA": {"Groupe 1: FERKANE, NEGRINE": "C", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "13-TLEMCEN": {"Groupe 1: AIN TALLOUT, OULED MIMOUN, OUED CHOULY, BENI SEMIEL, TERNI BENI HEDIEL, AIN GHORABA, BENI BOUSSAID, BENI BAHDEL, BENI SNOUS, SEBDOU, AZAILS, EL GOR, SIDI DJILLALI, EL ARICHA, EL BOUIHI": "B", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "14-TIARET": {"Toutes les communes": "B"},
    "15-TIZI-OUZOU": {"Groupe 1: MIZRANA": "A1", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "16-ALGER": {"Toutes les communes": "A"},
    "17-DJELFA": {"Groupe 1: BENHAR, AIN OUESSARA, BIRINE, AIN FEKKA, EL KHEMIS, HASSI FDOUL, HAD SAHARY, SIDI LAADJEL, BOUIRA LAHDAB, GUERNINI, HASSI EL EUCH, HASSI BAHBAH, ZAAFRANE, EL GUEDDID, CHAREF, BENI YAGOUB, EL IDRISSIA, DOUIS, AIN CHOUHADA": "B", "Groupe 2: OUM LAADHAM, GUETTARA": "D", "Groupe 3: Toutes les communes autres que celles figurant aux groupes 1 et 2": "C"},
    "18-JIJEL": {"Toutes les communes": "A"},
    "19-SETIF": {"Groupe 1: BABOR, AIT TIZI, MZADA, AIN SEBT, SERDJ EL GHOUL, OUED EL BARED, BENI MOUHLI, BOUANDAS, BENI AZIZ, BOUSSELAM, BENI CHEBANA, TALA IFACENE, BENI OUARTILANE, TIZI N'BECHAR, DRAA KEBILA, AIN LAGRADJ, MAOUKLANE, MAAOUIA, DEHAMCHA, AMOUCHA, AIN EL KEBIRA, DJEMILA, HAMMAM GUERGOUR, AIN ROUA, HARBIL, AIN ABESSA, BOUGAA, GUENZET, TASSAMERT, OULED ADDOUANE, BENI FOUDA, EL OURICIA, BENI HOCINE, TACHOUDA": "A", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "20-SAIDA": {"Toutes les communes": "B"},
    "21-SKIKDA": {"Groupe 1: AIN ZOUIT, FIL FILA, SKIKDA, HAMMADI KROUMA, EL HADAIEK": "A1", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "22-SIDI BEL ABBES": {"Groupe 1: MAKEDRA, AIN EL BERD, BOUDJEBAA EL BORDJ, AIN ADDEN, AIN THRID, SIDI HAMADOUCHE, TESSALA, ZEROUALA, SFISEF, IDI BRAHIM, SEHALA THAOURA, SIDI LAHCENE, SIDI BEL ABBES, MOSTEFA BEN BRAHIM, TILMOUNI, SIDI DAHO, SIDI YACOUB, AIN KADA, BELARBI, AMARNAS, SIDI KHALED, SIDI ALI BOUSSIDI, BOUKANEFIS, LAMTAR, HASSI ZAHANA, BEDRABINE EL MOKRANI": "A", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "23-ANNABA": {"Toutes les communes": "A"},
    "24-GUELMA": {"Groupe 1: HAMMAM NBAIL, OUED CHEHAM, KHEZARA, OUED ZENATE, DAHOUARA, AIN LARBI, AIN REGGADA, BOUHACHANA, AIN SANDEL, AIN MAKHLOUF, TAMLOUKA": "B", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "25-CONSTANTINE": {"Groupe 1: EL KHROUB, AIN SMARA, AIN ABID, OULED RAHMOUN": "B", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "26-MEDEA": {"Toutes les communes": "B"},
    "27-MOSTAGANEM": {"Toutes les communes": "A"},
    "28-MSILA": {"Groupe 1: HAMMAM DHALAA, BENI ILMENE, OUENOUGHA, SIDI AISSA, TARMOUNT, MAADID, BOUTI SAYEH, OULED ADDI GUEBALA, DEHAHNA, MAGRA, BERHOUM, BELAIBA": "B", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "C"},
    "29-MASCARA": {"Groupe 1: MOCTADOUZ, EL GHOMRI, SIDI ABDELMOUMENE, ALAIMIA, RAS EL AIN AMIROUCHE, SEDJERARA, MOHAMMADIA, OGGAZ, BOUHENNI, EL MENAOUER, SIG, ZAHANA, EL BORDJ, AIN FARES, HACINE, EL MAMOUNIA, FERRAGUIG, SIDI ABDELDJEBAR, SEHAILI, CHORFA, EL GAADA, KHALOUIA, EL GUEITNA, TIGHENNIF, MAOUSSA, MASCARA, EL KEURT, TIZI, BOUHANIFIA": "A", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "30-OUARGLA": {"Groupe 1: EL BORMA": "C", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "D"},
    "31-ORAN": {"Toutes les communes": "A"},
    "32-EL BAYADH": {"Groupe 1: BREZINA, EL ABIODH SIDI CHEIKH, EL BNOUD": "C", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "33-ILLIZI": {"Toutes les communes": "C"},
    "34-BORDJ BOU ARRERIDJ": {"Groupe 1: EL MAIN, DJAAFRA, TAFREG, KHELIL, TESMART, BORDJ ZEMOURA, COLLA, OULED SIDI BRAHIM, OULED DAHMANE, THENIET EL ANSEUR, HARAZA": "A", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "35-BOUMERDES": {"Groupe 1: DELLYS, SIDI DAOUD, AFIR, BEN CHOUD, BAGHLIA, OULED AISSA, TAOURGA": "A1", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "36-EL TARF": {"Groupe 1: EL KALA, BERRIHANE": "A1", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "37-TINDOUF": {"Toutes les communes": "D"},
    "38-TISSEMSILT": {"Groupe 1: LAZHARIA, LARBAA, BOUCAID, BORDJ EL EMIR ABDELKADER": "A", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "39-EL OUED": {"Groupe 1: OUM TIOUR, EL MGHAIR, SIDI KHELLIL, TENDLA, MRARA, DJAMAA, SIDI AMRANE": "D", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "C"},
    "40-KHENCHELA": {"Groupe 1: BABAR": "C", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "41-SOUK AHRAS": {"Groupe 1: MECHROHA, AIN ZANA, OULED DRISS": "A", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "B"},
    "42-TIPAZA": {"Toutes les communes": "A"},
    "43-MILA": {"Groupe 1: OUED ATHMANIA, BENYAHIA ABDERRAHMANE, OUED SEGUEN, CHELGHOUM LAID, TADJENANET, TELAGHMA, EL MCHIRA, OULED KHELLOUF": "B", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "44-AIN DEFLA": {"Toutes les communes": "A"},
    "45-NAAMA": {"Toutes les communes": "B"},
    "46-AIN TEMOUCHENT": {"Groupe 1: SIDI SAFI, BENI SAF, OULHACA EL GHERABA, AIN TOLBA, EL EMIR ABDELKADER": "A1", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"},
    "47-GHARDAIA": {"Groupe 1: EL GUERRARA, ZELFANA": "D", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "C"},
    "48-RELIZANE": {"Groupe 1: OUED ESSALEM": "B", "Groupe 2: Toutes les communes autres que celles figurant aux groupes de communes 1": "A"}
}

# Listes pour types de fenêtres et portes avec coefficients U (W/m².K)
fenetres_options = {
    "Simple vitrage": 5.7,
    "Double vitrage": 2.9,
    "Double vitrage performant": 1.8,
    "Triple vitrage": 0.9
}
portes_options = {
    "Porte standard (non isolée)": 3.0,
    "Porte isolée": 1.5
}

# Fonction pour obtenir la température extérieure de base (°C) selon zone climatique et altitude (m)
def get_temperature_exterieure(zone: str, altitude: float) -> float:
    temp_ranges = {
        "A": [(300, 3.0), (450, 2.0), (600, 1.0), (800, 0.0), (float('inf'), -1.5)],
        "A1": [(300, 7.0), (450, 6.0), (600, 5.0), (800, 4.0), (float('inf'), 2.5)],
        "B": [(450, -2.0), (600, -3.0), (800, -4.0), (float('inf'), -5.5)],
        "C": [(300, 1.0), (450, 0.0), (600, -1.0), (800, -2.0), (float('inf'), -4.5)],
        "D": [(300, 4.0), (450, 3.0), (600, 2.0), (800, 1.0), (float('inf'), -0.5)]
    }
    if zone not in temp_ranges:
        return None
    for (limit, temp) in temp_ranges[zone]:
        if altitude < limit:
            return temp
    # Par défaut, renvoyer la dernière valeur
    return temp_ranges[zone][-1][1]

# Initialisation de l'état de session pour stocker les données persistantes
if "current_page" not in st.session_state:
    st.session_state.current_page = "Informations du projet"
# Inputs du projet
for key, default in [("project_name", ""), ("wilaya_selected", None), ("group_selected", None), ("zone", ""), ("altitude", 0.0), ("building_type", ""), ("site", "")]:
    if key not in st.session_state:
        st.session_state[key] = default
# Données des parois définies et couches en cours
if "parois" not in st.session_state:
    st.session_state.parois = {}  # dict of {name: {"layers": [(mat, ep), ...], "R": value}}
if "current_layers" not in st.session_state:
    st.session_state.current_layers = []
if "paroi_name_input" not in st.session_state:
    st.session_state.paroi_name_input = ""
# Inputs pour ajout de couche
if "selected_material" not in st.session_state:
    st.session_state.selected_material = list(materiaux.keys())[0]
if "layer_thickness" not in st.session_state:
    st.session_state.layer_thickness = 0.0
# Inputs par orientation
orientation_keys = ["north", "south", "east", "west", "floor", "roof"]
for ori in orientation_keys:
    type_key = f"{ori}_wall_type" if ori in ["north", "south", "east", "west"] else f"{ori}_type"
    area_key = f"{ori}_wall_area" if ori in ["north", "south", "east", "west"] else f"{ori}_area"
    if type_key not in st.session_state:
        st.session_state[type_key] = None
    if area_key not in st.session_state:
        st.session_state[area_key] = 0.0
    if ori in ["north", "south", "east", "west"]:
        if f"{ori}_window_type" not in st.session_state:
            st.session_state[f"{ori}_window_type"] = list(fenetres_options.keys())[1]  # défaut "Double vitrage"
        if f"{ori}_window_area" not in st.session_state:
            st.session_state[f"{ori}_window_area"] = 0.0
        if f"{ori}_door_type" not in st.session_state:
            st.session_state[f"{ori}_door_type"] = list(portes_options.keys())[0]
        if f"{ori}_door_area" not in st.session_state:
            st.session_state[f"{ori}_door_area"] = 0.0

# Barre latérale de navigation
pages = ["Informations du projet", "Définition des parois", "Configuration par orientation", "Résultats"]
st.sidebar.title("Menu")
st.sidebar.radio("Pages", pages, index=pages.index(st.session_state.current_page), key="current_page")

# Affichage de la page correspondant à st.session_state.current_page
if st.session_state.current_page == "Informations du projet":
    st.title("Informations du projet")
    st.text_input("Nom du projet", key="project_name")
    # Sélection de la wilaya et détermination de la zone climatique
    wilaya_list = list(wilaya.keys())
    wilaya_list.sort(key=lambda x: int(x.split('-')[0]))
    chosen_wilaya = st.selectbox("Wilaya", wilaya_list, key="wilaya_selected")
    if chosen_wilaya:
        groupe_dict = wilaya[chosen_wilaya]
        if len(groupe_dict) == 1:
            # Une seule zone (Toutes les communes)
            zone_val = list(groupe_dict.values())[0]
            st.session_state.zone = zone_val
            st.text_input("Zone climatique", value=zone_val, key="zone", disabled=True)
        else:
            chosen_groupe = st.selectbox("Groupe de communes", list(groupe_dict.keys()), key="group_selected")
            if chosen_groupe:
                st.session_state.zone = groupe_dict[chosen_groupe]
                st.text_input("Zone climatique", value=st.session_state.zone, key="zone", disabled=True)
    st.number_input("Altitude du site (m)", min_value=0.0, key="altitude")
    building_types = ["Logement individuel", "Logement en immeuble collectif / Bureaux / Hébergement"]
    st.selectbox("Type de bâtiment", building_types, key="building_type")
    site_choices = ["Centre des grandes villes", "Zones urbaines / industrielles / forêts", "Zones rurales arborées (haies, forêts clairsemées)", "Rase campagne / Aéroport", "Bord de mer"]
    st.selectbox("Site d'implantation", site_choices, key="site")
    col1, col2 = st.columns([1,1])
    with col1:
        st.button("Retour", disabled=True)
    with col2:
        if st.button("Suivant"):
            st.session_state.current_page = "Définition des parois"

elif st.session_state.current_page == "Définition des parois":
    st.title("Définition des parois")
    st.markdown("Ajoutez ici les différents types de parois opaques (murs, plancher bas, toiture) avec leur composition en couches.")
    st.subheader("Nouvelle paroi")
    st.text_input("Nom de la paroi", key="paroi_name_input")
    st.selectbox("Matériau (couche à ajouter)", list(materiaux.keys()), key="selected_material")
    st.number_input("Épaisseur de la couche (m)", min_value=0.0, step=0.01, key="layer_thickness")
    add_col, list_col = st.columns([1, 3])
    with add_col:
        if st.button("Ajouter la couche"):
            mat = st.session_state.selected_material
            ep = st.session_state.layer_thickness
            if mat and ep and ep > 0:
                st.session_state.current_layers.append((mat, ep))
            else:
                st.warning("Veuillez sélectionner un matériau et une épaisseur valide.")
    with list_col:
        if st.session_state.current_layers:
            st.markdown("**Couches de la paroi en cours :**")
            total_R = 0.0
            for i, (mat, ep) in enumerate(st.session_state.current_layers):
                k_value = materiaux[mat]["conductivite"]
                R_layer = ep / k_value if k_value != 0 else 0.0
                total_R += R_layer
                layer_col1, layer_col2 = st.columns([4, 1])
                layer_col1.write(f"- {mat} : {ep:.3f} m (R = {R_layer:.3f} m²·K/W)")
                if layer_col2.button("❌", key=f"remove_layer_{i}"):
                    st.session_state.current_layers.pop(i)
                    break
            if total_R > 0:
                st.write(f"**R total (sans résistances superficielles)** = {total_R:.3f} m²·K/W")
    if st.button("Enregistrer la paroi"):
        name = st.session_state.paroi_name_input.strip()
        if not name:
            st.error("Veuillez saisir un nom pour la paroi.")
        elif name in st.session_state.parois:
            st.error(f"Le paroi '{name}' existe déjà.")
        elif not st.session_state.current_layers:
            st.error("Aucune couche définie pour cette paroi.")
        else:
            R_layers = 0.0
            for mat, ep in st.session_state.current_layers:
                k = materiaux[mat]["conductivite"]
                if k != 0:
                    R_layers += ep / k
            st.session_state.parois[name] = {"layers": list(st.session_state.current_layers), "R": R_layers}
            st.success(f"Paroi '{name}' ajoutée.")
            st.session_state.current_layers = []
            st.session_state.paroi_name_input = ""
    if st.session_state.parois:
        st.subheader("Parois définies")
        for pname, pdata in st.session_state.parois.items():
            R_val = pdata["R"]
            U_val = 1.0 / (R_val + 0.17) if R_val > 0 else 0.0
            comp_str = " + ".join([f"{mat} ({ep:.3f} m)" for mat, ep in pdata["layers"]])
            st.write(f"**{pname}** – R = {R_val:.3f} m²·K/W, U ≈ {U_val:.3f} W/m²·K. Composition : {comp_str}")
            if st.button(f"Supprimer {pname}", key=f"delete_paroi_{pname}"):
                del st.session_state.parois[pname]
                st.experimental_rerun()
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Retour"):
            st.session_state.current_page = "Informations du projet"
    with col2:
        if st.button("Suivant"):
            if not st.session_state.parois:
                st.warning("Veuillez définir au moins une paroi avant de continuer.")
            else:
                st.session_state.current_page = "Configuration par orientation"

elif st.session_state.current_page == "Configuration par orientation":
    st.title("Configuration par orientation")
    if not st.session_state.parois:
        st.error("Veuillez d'abord définir des parois dans l'étape précédente.")
    else:
        st.markdown("Indiquez, pour chaque orientation, les surfaces des parois et ouvertures correspondantes, ainsi que les types de parois utilisées.")
        paroi_names = list(st.session_state.parois.keys())
        for ori in ["north","south","east","west"]:
            key = f"{ori}_wall_type"
            if st.session_state[key] is None:
                st.session_state[key] = paroi_names[0] if paroi_names else None
        for ori in ["floor","roof"]:
            key = f"{ori}_type"
            if st.session_state[key] is None:
                st.session_state[key] = paroi_names[0] if paroi_names else None

        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader("Nord")
            st.selectbox("Type de mur nord", paroi_names, key="north_wall_type")
            st.number_input("Surface du mur nord (m²)", min_value=0.0, key="north_wall_area")
            st.selectbox("Type de fenêtres (nord)", list(fenetres_options.keys()), key="north_window_type")
            st.number_input("Surface des fenêtres nord (m²)", min_value=0.0, key="north_window_area")
            st.selectbox("Type de porte (nord)", list(portes_options.keys()), key="north_door_type")
            st.number_input("Surface des portes nord (m²)", min_value=0.0, key="north_door_area")
            st.subheader("Sud")
            st.selectbox("Type de mur sud", paroi_names, key="south_wall_type")
            st.number_input("Surface du mur sud (m²)", min_value=0.0, key="south_wall_area")
            st.selectbox("Type de fenêtres (sud)", list(fenetres_options.keys()), key="south_window_type")
            st.number_input("Surface des fenêtres sud (m²)", min_value=0.0, key="south_window_area")
            st.selectbox("Type de porte (sud)", list(portes_options.keys()), key="south_door_type")
            st.number_input("Surface des portes sud (m²)", min_value=0.0, key="south_door_area")
        with col_right:
            st.subheader("Est")
            st.selectbox("Type de mur est", paroi_names, key="east_wall_type")
            st.number_input("Surface du mur est (m²)", min_value=0.0, key="east_wall_area")
            st.selectbox("Type de fenêtres (est)", list(fenetres_options.keys()), key="east_window_type")
            st.number_input("Surface des fenêtres est (m²)", min_value=0.0, key="east_window_area")
            st.selectbox("Type de porte (est)", list(portes_options.keys()), key="east_door_type")
            st.number_input("Surface des portes est (m²)", min_value=0.0, key="east_door_area")
            st.subheader("Ouest")
            st.selectbox("Type de mur ouest", paroi_names, key="west_wall_type")
            st.number_input("Surface du mur ouest (m²)", min_value=0.0, key="west_wall_area")
            st.selectbox("Type de fenêtres (ouest)", list(fenetres_options.keys()), key="west_window_type")
            st.number_input("Surface des fenêtres ouest (m²)", min_value=0.0, key="west_window_area")
            st.selectbox("Type de porte (ouest)", list(portes_options.keys()), key="west_door_type")
            st.number_input("Surface des portes ouest (m²)", min_value=0.0, key="west_door_area")
        st.subheader("Plancher bas")
        st.selectbox("Type de plancher bas", paroi_names, key="floor_type")
        st.number_input("Surface du plancher bas (m²)", min_value=0.0, key="floor_area")
        st.subheader("Toiture")
        st.selectbox("Type de toiture", paroi_names, key="roof_type")
        st.number_input("Surface de la toiture (m²)", min_value=0.0, key="roof_area")
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Retour"):
            st.session_state.current_page = "Définition des parois"
    with col2:
        if st.button("Suivant"):
            if not st.session_state.parois:
                st.session_state.current_page = "Définition des parois"
            else:
                st.session_state.current_page = "Résultats"

elif st.session_state.current_page == "Résultats":
    st.title("Résultats du calcul thermique")
    if not st.session_state.parois:
        st.error("Aucune paroi définie. Veuillez revenir aux étapes précédentes.")
    else:
        zone = st.session_state.zone
        altitude = st.session_state.altitude
        T_ext = get_temperature_exterieure(zone, altitude) if zone else None
        if T_ext is None:
            st.warning("Zone climatique non définie correctement.")
            T_ext = 0.0
        T_int = 20.0  # Température intérieure de consigne (°C)
        deltaT = T_int - T_ext
        Rsi_wall = 0.13
        Rse_wall = 0.04
        Rsi_roof = 0.10
        Rse_roof = 0.04
        Rsi_floor = 0.17
        Rse_floor = 0.0
        total_loss = 0.0
        sum_wall_loss = 0.0
        sum_window_loss = 0.0
        sum_door_loss = 0.0
        roof_loss = 0.0
        floor_loss = 0.0
        orientation_results = []
        orientations = [("Nord", "north"), ("Est", "east"), ("Sud", "south"), ("Ouest", "west")]
        for (label, ori) in orientations:
            wall_type = st.session_state[f"{ori}_wall_type"]
            wall_area = st.session_state[f"{ori}_wall_area"]
            window_type = st.session_state[f"{ori}_window_type"]
            window_area = st.session_state[f"{ori}_window_area"]
            door_type = st.session_state[f"{ori}_door_type"]
            door_area = st.session_state[f"{ori}_door_area"]
            R_layers = st.session_state.parois[wall_type]["R"] if wall_type in st.session_state.parois else 0.0
            U_wall = 1.0 / (R_layers + Rsi_wall + Rse_wall) if R_layers > 0 else 0.0
            wall_loss = U_wall * wall_area * deltaT
            U_window = fenetres_options.get(window_type, 0.0)
            window_loss = U_window * window_area * deltaT
            U_door = portes_options.get(door_type, 0.0)
            door_loss = U_door * door_area * deltaT
            sum_wall_loss += wall_loss
            sum_window_loss += window_loss
            sum_door_loss += door_loss
            orientation_total = wall_loss + window_loss + door_loss
            total_loss += orientation_total
            orientation_results.append({
                "Orientation": label,
                "Pertes parois opaques (W)": wall_loss,
                "Pertes fenêtres (W)": window_loss,
                "Pertes portes (W)": door_loss,
                "Total (W)": orientation_total
            })
        floor_type = st.session_state["floor_type"]
        floor_area = st.session_state["floor_area"]
        R_layers_floor = st.session_state.parois[floor_type]["R"] if floor_type in st.session_state.parois else 0.0
        U_floor = 1.0 / (R_layers_floor + Rsi_floor + Rse_floor) if R_layers_floor > 0 else 0.0
        floor_loss = U_floor * floor_area * deltaT
        total_loss += floor_loss
        orientation_results.append({
            "Orientation": "Plancher bas",
            "Pertes parois opaques (W)": floor_loss,
            "Pertes fenêtres (W)": 0.0,
            "Pertes portes (W)": 0.0,
            "Total (W)": floor_loss
        })
        roof_type = st.session_state["roof_type"]
        roof_area = st.session_state["roof_area"]
        R_layers_roof = st.session_state.parois[roof_type]["R"] if roof_type in st.session_state.parois else 0.0
        U_roof = 1.0 / (R_layers_roof + Rsi_roof + Rse_roof) if R_layers_roof > 0 else 0.0
        roof_loss = U_roof * roof_area * deltaT
        total_loss += roof_loss
        orientation_results.append({
            "Orientation": "Toiture",
            "Pertes parois opaques (W)": roof_loss,
            "Pertes fenêtres (W)": 0.0,
            "Pertes portes (W)": 0.0,
            "Total (W)": roof_loss
        })
        df_orient = pd.DataFrame(orientation_results)
        df_orient.set_index("Orientation", inplace=True)
        st.subheader("Déperditions par orientation")
        st.table(df_orient.style.format("{:.1f}"))
        elements_data = [
            ["Murs extérieurs (verticals)", sum_wall_loss],
            ["Fenêtres", sum_window_loss],
            ["Portes", sum_door_loss],
            ["Plancher bas", floor_loss],
            ["Toiture", roof_loss],
            ["Total général", total_loss]
        ]
        df_elem = pd.DataFrame(elements_data, columns=["Élément", "Déperdition (W)"])
        df_elem.set_index("Élément", inplace=True)
        st.subheader("Déperditions par type d'élément")
        st.table(df_elem.style.format("{:.1f}"))
        st.subheader("Diagramme: Déperditions par orientation")
        st.bar_chart(df_orient["Total (W)"])
        st.subheader("Diagramme: Répartition par type d'élément")
        labels = ["Murs", "Fenêtres", "Portes", "Plancher", "Toiture"]
        sizes = [sum_wall_loss, sum_window_loss, sum_door_loss, floor_loss, roof_loss]
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax.axis('equal')
        st.pyplot(fig)
        st.subheader("Export des résultats")
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Informations du projet"])
        writer.writerow(["Nom du projet", st.session_state.project_name])
        writer.writerow(["Wilaya", st.session_state.wilaya_selected])
        writer.writerow(["Zone climatique", st.session_state.zone])
        writer.writerow(["Altitude (m)", st.session_state.altitude])
        writer.writerow(["Type de bâtiment", st.session_state.building_type])
        writer.writerow(["Site d'implantation", st.session_state.site])
        writer.writerow([])
        writer.writerow(["Parois définies"])
        writer.writerow(["Nom de paroi", "R (m².K/W)", "U approximatif (W/m².K)", "Composition (couches)"])
        for pname, pdata in st.session_state.parois.items():
            Rval = pdata["R"]
            Uapp = 1.0/(Rval + 0.17) if Rval > 0 else 0.0
            comp = " + ".join([f"{mat} ({ep:.3f} m)" for mat, ep in pdata["layers"]])
            writer.writerow([pname, f"{Rval:.3f}", f"{Uapp:.3f}", comp])
        writer.writerow([])
        writer.writerow(["Surfaces par orientation et types"])
        writer.writerow(["Orientation", "Type de paroi", "Surface paroi (m²)", "Type de fenêtres", "Surface fenêtres (m²)", "Type de portes", "Surface portes (m²)"])
        for label, ori in [("Nord","north"), ("Est","east"), ("Sud","south"), ("Ouest","west")]:
            writer.writerow([label,
                             st.session_state[f"{ori}_wall_type"], f'{st.session_state[f"{ori}_wall_area"]:.2f}',
                             st.session_state[f"{ori}_window_type"], f'{st.session_state[f"{ori}_window_area"]:.2f}',
                             st.session_state[f"{ori}_door_type"], f'{st.session_state[f"{ori}_door_area"]:.2f}'])
        writer.writerow(["Plancher bas",
                         st.session_state["floor_type"], f'{st.session_state["floor_area"]:.2f}',
                         "", "", "", ""])
        writer.writerow(["Toiture",
                         st.session_state["roof_type"], f'{st.session_state["roof_area"]:.2f}',
                         "", "", "", ""])
        writer.writerow([])
        writer.writerow(["Déperditions par orientation (W)"])
        writer.writerow(["Orientation", "Parois opaques", "Fenêtres", "Portes", "Total"])
        for row in orientation_results:
            writer.writerow([row["Orientation"],
                             f'{row["Pertes parois opaques (W)"]:.1f}',
                             f'{row["Pertes fenêtres (W)"]:.1f}',
                             f'{row["Pertes portes (W)"]:.1f}',
                             f'{row["Total (W)"]:.1f}'])
        writer.writerow(["Total", f"{sum_wall_loss:.1f}", f"{sum_window_loss:.1f}", f"{sum_door_loss:.1f}", f"{total_loss:.1f}"])
        writer.writerow([])
        writer.writerow(["Déperditions par type d'élément (W)"])
        writer.writerow(["Élément", "Déperdition"])
        writer.writerow(["Murs extérieurs", f"{sum_wall_loss:.1f}"])
        writer.writerow(["Fenêtres", f"{sum_window_loss:.1f}"])
        writer.writerow(["Portes", f"{sum_door_loss:.1f}"])
        writer.writerow(["Plancher bas", f"{floor_loss:.1f}"])
        writer.writerow(["Toiture", f"{roof_loss:.1f}"])
        writer.writerow(["Total général", f"{total_loss:.1f}"])
        csv_data = output.getvalue()
        st.download_button(label="📥 Télécharger les résultats (CSV)", data=csv_data.encode('utf-8'), file_name="resultats_calcul_thermique.csv", mime="text/csv")
