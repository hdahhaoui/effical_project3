# EffiCal - Calcul thermique selon DTR C3.2-4 (Chauffage)
import streamlit as st
import pandas as pd

# Initialisation du session state pour toutes les variables critiques
if 'page' not in st.session_state:
    st.session_state.page = 0
if 'nom_projet' not in st.session_state:
    st.session_state.nom_projet = ""
if 'wilaya' not in st.session_state:
    st.session_state.wilaya = "Sélectionnez wilaya"
if 'group' not in st.session_state:
    st.session_state.group = "Sélectionnez groupe"
if 'zone' not in st.session_state:
    st.session_state.zone = ""
if 'altitude' not in st.session_state:
    st.session_state.altitude = 0.0
if 'latitude' not in st.session_state:
    st.session_state.latitude = 0.0
if 'type_batiment' not in st.session_state:
    st.session_state.type_batiment = "Sélectionnez..."
if 'current_layers' not in st.session_state:
    st.session_state.current_layers = []
if 'walls' not in st.session_state:
    st.session_state.walls = {}
if 'selected_material_name' not in st.session_state:
    st.session_state.selected_material_name = ""
if 'input_thickness' not in st.session_state:
    st.session_state.input_thickness = 0.0
if 'selected_layer_index' not in st.session_state:
    st.session_state.selected_layer_index = 0
if 'edit_thickness' not in st.session_state:
    st.session_state.edit_thickness = 0.0
if 'volume' not in st.session_state:
    st.session_state.volume = 0.0
if 'infiltration_entries' not in st.session_state:
    st.session_state.infiltration_entries = []
if 'infiltration_number' not in st.session_state:
    st.session_state.infiltration_number = 0
if 'infiltration_surface' not in st.session_state:
    st.session_state.infiltration_surface = 0.0
if 'infiltration_type' not in st.session_state:
    st.session_state.infiltration_type = "Fenêtre ou porte-fenêtre"

# Préparation des clés pour chaque orientation et éléments associés
orientations = [
    ("Nord", "nord"), ("Nord-Est", "nord_est"), ("Est", "est"), ("Sud-Est", "sud_est"),
    ("Sud", "sud"), ("Sud-Ouest", "sud_ouest"), ("Ouest", "ouest"), ("Nord-Ouest", "nord_ouest"),
    ("Plancher bas (sol)", "plancher_bas"), ("Plafond/Terrasse", "plancher_terrasse")
]
for label, key in orientations:
    if f"use_{key}" not in st.session_state:
        st.session_state[f"use_{key}"] = False
    if f"{key}_wall" not in st.session_state:
        st.session_state[f"{key}_wall"] = "(choisir)"
    if f"homogeneous_{key}" not in st.session_state:
        st.session_state[f"homogeneous_{key}"] = False
    if f"area_wall_{key}" not in st.session_state:
        st.session_state[f"area_wall_{key}"] = 0.0
    if f"area_window_{key}" not in st.session_state:
        st.session_state[f"area_window_{key}"] = 0.0
    if f"area_door_{key}" not in st.session_state:
        st.session_state[f"area_door_{key}"] = 0.0
    if f"window_type_{key}" not in st.session_state:
        st.session_state[f"window_type_{key}"] = "(choisir type)"
    if f"window_material_{key}" not in st.session_state:
        st.session_state[f"window_material_{key}"] = "(choisir matériau)"
    if f"window_gap_{key}" not in st.session_state:
        st.session_state[f"window_gap_{key}"] = "(choisir écart air)"
    if f"door_contact_{key}" not in st.session_state:
        st.session_state[f"door_contact_{key}"] = "(choisir contact)"
    if f"door_type_{key}" not in st.session_state:
        st.session_state[f"door_type_{key}"] = "(choisir type de porte)"

# Clés pour un mur vers local non chauffé
if 'use_local_nc' not in st.session_state:
    st.session_state.use_local_nc = False
if 'wall_local_nc' not in st.session_state:
    st.session_state.wall_local_nc = "(choisir)"
if 'area_local_nc' not in st.session_state:
    st.session_state.area_local_nc = 0.0
if 'Tint_local_nc' not in st.session_state:
    st.session_state.Tint_local_nc = 20.0
if 'Tesp_local_nc' not in st.session_state:
    st.session_state.Tesp_local_nc = 0.0
if 'Text_local_nc' not in st.session_state:
    st.session_state.Text_local_nc = 0.0

# Clé pour température intérieure de calcul (final)
if 'temperature_int' not in st.session_state:
    st.session_state.temperature_int = 20.0

# Dictionnaire Wilaya -> Groupes -> Zone climatique (abrégé pour exemple)
wilaya_dict = {
    "1-ADRAR": {
        "Groupe 1: TINERKOUK, BORDJ BADJI MOKHTAR": "C",
        "Groupe 2: Toutes les autres communes": "D"
    },
    "2-CHLEF": {
        "Groupe 1: TENES, OUED GHOUSSINE, SIDI ABDERRAHMANE, SIDI AKKACHA": "A1",
        "Groupe 2: Toutes les autres communes": "A"
    },
    # ... (les autres wilayas et groupes seraient ajoutés ici)
}

# Base de données des matériaux (conductivité en W/m.K, masse volumique en kg/m³)
materiaux = {
    "Mortier de chaux": {"conductivite": 0.87, "masse volumique": 1800},
    "Carreaux de plâtre pleins": {"conductivite": 1.4, "masse volumique": 950},
    "Liège Comprimé": {"conductivite": 0.10, "masse volumique": 500},
    "Polystyrène expansé": {"conductivite": 0.044, "masse volumique": 30},
    "Brique creuse": {"conductivite": 0.48, "masse volumique": 900},
    "Brique pleine": {"conductivite": 0.80, "masse volumique": 1700},
    "Béton (plein)": {"conductivite": 1.75, "masse volumique": 2200},
    "Laine de verre": {"conductivite": 0.044, "masse volumique": 9},
    "Acier": {"conductivite": 52.0, "masse volumique": 7780},
    # ... (autres matériaux)
}

# Fonctions utilitaires de calcul
def get_temperature_ext(zone, altitude):
    """Température extérieure de base selon zone climatique et altitude (DTR C3.2-4)."""
    temp_ranges = {
        "A": [(300, 3), (450, 2), (600, 1), (800, 0), (float('inf'), -1.5)],
        "A1": [(300, 7), (450, 6), (600, 5), (800, 4), (float('inf'), 2.5)],
        "B": [(450, -2), (600, -3), (800, -4), (float('inf'), -5.5)],
        "C": [(300, 1), (450, 0), (600, -1), (800, -2), (float('inf'), -4.5)],
        "D": [(300, 4), (450, 3), (600, 2), (800, 1), (float('inf'), -0.5)]
    }
    if zone in temp_ranges:
        for limit, temp in temp_ranges[zone]:
            if altitude < limit:
                return temp
    return None

def calculate_wall_properties(layers, contact_type, position_type):
    """Calcule la résistance thermique totale (avec Rsi/Rse) et la masse surfacique d'une paroi."""
    R = 0.0
    M = 0.0
    for mat_name, ep in layers:
        if mat_name in materiaux:
            k = materiaux[mat_name]["conductivite"]
            rho = materiaux[mat_name]["masse volumique"]
            if k > 0:
                R += ep / k
            M += rho * ep
    # Coefficients de convection internes/externes (hivers) selon position/contact
    hi = he = 0.0
    if contact_type == "Exterieur":
        if position_type == "Lateral":      # mur vertical
            hi, he = 0.11, 0.06
        elif position_type == "Ascendant":  # toiture (inclinaison <= 60°)
            hi, he = 0.09, 0.05
        elif position_type == "Descendant": # plancher sur local ouvert
            hi, he = 0.17, 0.05
    elif contact_type == "Local":  # Local chauffé ou non chauffé
        if position_type == "Lateral":
            hi = he = 0.11
        elif position_type == "Ascendant":
            hi = he = 0.09
        elif position_type == "Descendant":
            hi = he = 0.17  # (local en dessous, même convection des deux côtés)
    # Résistance totale incluant les films d'air int/ext
    R_total = R + (1/hi if hi else 0) + (1/he if he else 0)
    return R_total, M

def get_k_door(contact, door_type):
    """Retourne le coefficient K d'une porte (W/m².K) selon son contact et son type."""
    if not contact or not door_type:
        return None
    c = contact.lower()
    d = door_type.lower()
    if "exterieur" in c or "extérieur" in c:
        if "bois" in d and "vitrage" not in d:
            return 3.5  # Porte pleine bois ext.
        if "metal" in d and "vitrage" not in d:
            return 5.8  # Porte pleine métal ext.
        if "vitrage <30" in d:
            return 4.0  # Porte bois <30% vitrage ext.
        if "vitrage entre 30" in d:
            return 4.5  # Porte bois 30-60% vitrage ext.
        if "vitrage simple" in d:
            return 5.8  # Porte métal avec vitrage simple ext.
    elif "non chauffé" in c or "non chauffe" in c:
        if "bois" in d and "vitrage" not in d:
            return 2.0  # Porte pleine bois vers local non chauffé
        if "metal" in d and "vitrage" not in d:
            return 4.5  # Porte pleine métal vers LNC
        if "vitrage <30" in d:
            return 2.4  # Porte bois <30% vitrage vers LNC
        if "vitrage entre 30" in d:
            return 2.7  # Porte bois 30-60% vitrage vers LNC
        if "vitrage simple" in d:
            return 4.5  # Porte métal + vitrage simple vers LNC
    return None

def get_k_window(win_type, frame_material, gap_option):
    """Retourne le coefficient de base d'une fenêtre (sans Rse/Rsi supplémentaires)."""
    if not win_type or not frame_material:
        return None
    t = win_type.lower()
    mat = frame_material.lower()
    if t == "simple":
        return 5.0 if mat == "bois" else 5.8
    elif t == "double":
        if not gap_option:
            return None
        g = gap_option.lower()
        # Cas particulier : "cas de fenetre double" sélectionné par erreur dans les intercalaires
        if "fenetre double" in g:
            return 2.6 if mat == "bois" else 3.0
        if mat == "bois":
            if "5 à 7" in g:
                return 3.3
            elif "8 à 9" in g:
                return 3.1
            elif "10 à 11" in g:
                return 3.0
            elif "12 à 13" in g:
                return 2.9
        else:  # métal
            if "5 à 7" in g:
                return 4.0
            elif "8 à 9" in g:
                return 3.9
            elif "10 à 11" in g:
                return 3.8
            elif "12 à 13" in g:
                return 3.7
    elif t == "fenetre double":  # fenêtre double (double châssis)
        return 2.6 if mat == "bois" else 3.0
    return None

# Rendu de l'interface multi-pages
page = st.session_state.page

# ---- Page 0: Informations du projet ----
if page == 0:
    st.title("EffiCal – Calcul thermique (DTR C3.2-4)")
    st.header("1. Informations du projet")
    st.text_input("Nom du Projet", key="nom_projet")
    # Sélection de la wilaya
    wilaya_options = ["Sélectionnez wilaya"] + list(wilaya_dict.keys())
    st.selectbox("Wilaya", options=wilaya_options, key="wilaya")
    # Sélection du groupe de communes (dépend de la wilaya)
    if st.session_state.wilaya in wilaya_dict:
        group_options = ["Sélectionnez groupe"] + list(wilaya_dict[st.session_state.wilaya].keys())
        st.selectbox("Groupe de communes", options=group_options, key="group")
        if st.session_state.group in wilaya_dict[st.session_state.wilaya]:
            # Détermination de la zone climatique automatiquement
            zone_val = wilaya_dict[st.session_state.wilaya][st.session_state.group]
            st.session_state.zone = zone_val
            st.text_input("Zone climatique", value=zone_val, disabled=True)
        else:
            st.session_state.zone = ""
    else:
        st.session_state.group = "Sélectionnez groupe"
        st.session_state.zone = ""
    # Altitude et latitude du site
    st.number_input("Altitude (m)", min_value=0.0, value=st.session_state.altitude, step=1.0, key="altitude")
    st.number_input("Latitude (°)", min_value=0.0, value=st.session_state.latitude, step=0.1, key="latitude")
    # Type de bâtiment
    type_options = ["Sélectionnez...", "Logement individuel", "Logement collectif/bureaux"]
    st.selectbox("Type de bâtiment", options=type_options, key="type_batiment")
    # Bouton Suivant avec validations
    if st.button("Suivant"):
        erreurs = []
        if st.session_state.wilaya == "Sélectionnez wilaya" or st.session_state.group == "Sélectionnez groupe":
            erreurs.append("Veuillez sélectionner la *wilaya* et le *groupe de communes*.")
        if st.session_state.zone == "":
            erreurs.append("La zone climatique n'est pas déterminée.")
        try:
            alt_val = float(st.session_state.altitude)
            if alt_val <= 0:
                erreurs.append("Altitude doit être un nombre positif.")
        except:
            erreurs.append("Veuillez renseigner une altitude valide.")
        try:
            lat_val = float(st.session_state.latitude)
            if lat_val <= 0:
                erreurs.append("Latitude doit être un nombre positif.")
        except:
            erreurs.append("Veuillez renseigner une latitude valide.")
        if st.session_state.type_batiment == "Sélectionnez...":
            erreurs.append("Veuillez choisir le type de bâtiment.")
        if erreurs:
            for e in erreurs:
                st.error(e)
        else:
            st.session_state.page = 1

# ---- Page 1: Définition des parois ----
if page == 1:
    st.header("2. Définition des parois (composition des murs)")
    # Formulaire d'ajout d'une nouvelle paroi
    st.subheader("Ajouter une nouvelle paroi")
    st.text_input("Nom de la paroi", key="wall_name_input")
    st.radio("Position de la paroi", ["Lateral (Mur) α>60", "Ascendant (Toiture) α<=60", "Descendant (Plancher)"], key="position_wall")
    st.radio("En contact avec", ["Exterieur / espace ouvert", "Local (non chauffé ou chauffé)"], key="contact_type")
    # Recherche et sélection de matériaux
    search = st.text_input("Rechercher un matériau")
    mat_list = [m for m in materiaux if search.lower() in m.lower()] if search else list(materiaux.keys())
    selected_mat = st.selectbox("Matériau", options=mat_list, key="selected_material_name")
    if selected_mat:
        info = materiaux[selected_mat]
        st.write(f"λ = {info['conductivite']} W/m·K, ρ = {info['masse volumique']} kg/m³")
    st.number_input("Épaisseur de la couche (m)", min_value=0.0, step=0.001, format="%.3f", key="input_thickness")
    if st.button("Ajouter cette couche"):
        if selected_mat and st.session_state.input_thickness > 0:
            st.session_state.current_layers.append((selected_mat, st.session_state.input_thickness))
            st.session_state.input_thickness = 0.0  # réinitialiser l'épaisseur saisie
        else:
            st.error("Veuillez sélectionner un matériau et une épaisseur positive.")
    # Affichage des couches actuelles de la paroi en cours de création
    if st.session_state.current_layers:
        st.markdown("*Composition actuelle* :")
        for i, (mat, ep) in enumerate(st.session_state.current_layers, start=1):
            st.write(f"{i}. **{mat}** – {ep:.3f} m")
        # Options de modification/suppression d'une couche ajoutée
        idx_options = list(range(len(st.session_state.current_layers)))
        idx_select = st.selectbox("Sélectionner une couche à modifier", options=idx_options, format_func=lambda i: f"{i+1}. {st.session_state.current_layers[i][0]}")
        st.number_input("Nouvelle épaisseur (m) pour la couche sélectionnée", min_value=0.0,
                        value=st.session_state.current_layers[idx_select][1], step=0.001, format="%.3f", key="edit_thickness")
        col1, col2 = st.columns(2)
        if col1.button("Mettre à jour épaisseur"):
            if st.session_state.edit_thickness > 0:
                mat_name = st.session_state.current_layers[idx_select][0]
                st.session_state.current_layers[idx_select] = (mat_name, st.session_state.edit_thickness)
        if col2.button("Supprimer cette couche"):
            st.session_state.current_layers.pop(idx_select)
    # Validation et ajout de la paroi complète
    if st.button("Ajouter la paroi aux éléments du projet"):
        name = st.session_state.wall_name_input.strip()
        if not name:
            st.error("Veuillez donner un nom à cette paroi.")
        elif name in st.session_state.walls:
            st.error(f"Une paroi nommée **{name}** existe déjà.")
        elif not st.session_state.current_layers:
            st.error("Ajoutez au moins une couche de matériau à la paroi.")
        else:
            # Détermine le type de contact et position pour le calcul
            contact = "Exterieur" if st.session_state.contact_type.startswith("Exterieur") else "Local"
            pos = "Lateral"
            if st.session_state.position_wall.startswith("Ascendant"):
                pos = "Ascendant"
            elif st.session_state.position_wall.startswith("Descendant"):
                pos = "Descendant"
            # Calcule la résistance et la masse surfacique
            R_total, M_total = calculate_wall_properties(st.session_state.current_layers, contact, pos)
            U_hiver = 1 / R_total if R_total != 0 else 0.0
            # Enregistre la paroi
            st.session_state.walls[name] = {'R': R_total, 'mass': M_total, 'U': U_hiver}
            st.success(f"Paroi **{name}** ajoutée – U = {U_hiver:.3f} W/m²K, masse = {M_total:.1f} kg/m²")
            # Réinitialise le formulaire pour une éventuelle paroi suivante
            st.session_state.wall_name_input = ""
            st.session_state.position_wall = "Lateral (Mur) α>60"
            st.session_state.contact_type = "Exterieur / espace ouvert"
            st.session_state.current_layers = []
    # Tableau des parois déjà créées
    if st.session_state.walls:
        st.subheader("Parois créées")
        df_walls = pd.DataFrame([
            {"Paroi": nom, "U (W/m²·K)": props["U"], "Masse (kg/m²)": props["mass"]}
            for nom, props in st.session_state.walls.items()
        ])
        st.table(df_walls.style.format({"U (W/m²·K)": "{:.3f}", "Masse (kg/m²)": "{:.1f}"}))
        # Suppression d'une paroi existante si besoin
        wall_names = list(st.session_state.walls.keys())
        choix_suppr = st.selectbox("Supprimer une paroi", options=[""] + wall_names)
        if st.button("Supprimer la paroi sélectionnée"):
            if choix_suppr in st.session_state.walls:
                del st.session_state.walls[choix_suppr]
                st.info(f"Paroi **{choix_suppr}** supprimée.")
    # Boutons de navigation
    col_prev, col_next = st.columns([1, 1])
    if col_prev.button("← Retour"):
        st.session_state.page = 0
    if col_next.button("Suivant →"):
        if not st.session_state.walls:
            st.error("Définissez au moins une paroi avant de continuer.")
        else:
            st.session_state.page = 2

# ---- Page 2: Saisie des surfaces par orientation ----
if page == 2:
    st.header("3. Surfaces et ouvertures par orientation")
    st.write("Cochez les orientations présentes et renseignez les surfaces correspondantes :")
    for label, key in orientations:
        if key in ["plancher_bas", "plancher_terrasse"]:  # cas du plancher bas / toit
            st.checkbox(f"{label} ?", key=f"use_{key}")
            if st.session_state[f"use_{key}"]:
                st.selectbox(f"Paroi utilisée pour {label}", options=["(choisir)"] + list(st.session_state.walls.keys()), key=f"{key}_wall")
                st.number_input(f"Surface {label} (m²)", min_value=0.0, step=0.1, key=f"area_wall_{key}")
        else:
            st.checkbox(f"Mur {label} ?", key=f"use_{key}")
            if st.session_state[f"use_{key}"]:
                st.selectbox(f"Paroi pour {label}", options=["(choisir)"] + list(st.session_state.walls.keys()), key=f"{key}_wall")
                st.checkbox("Mur homogène (sans ouvertures)", key=f"homogeneous_{key}")
                if st.session_state[f"homogeneous_{key}"]:
                    st.number_input(f"Surface du mur {label} (m²)", min_value=0.0, step=0.1, key=f"area_wall_{key}")
                else:
                    st.number_input(f"Surface du mur {label} (m²)", min_value=0.0, step=0.1, key=f"area_wall_{key}")
                    st.number_input(f"Surface des fenêtres {label} (m²)", min_value=0.0, step=0.1, key=f"area_window_{key}")
                    st.selectbox("Type de vitrage", options=["(choisir type)", "Simple", "Double", "Fenetre double"], key=f"window_type_{key}")
                    st.selectbox("Matériau de la fenêtre", options=["(choisir matériau)", "Bois", "Metal"], key=f"window_material_{key}")
                    if st.session_state[f"window_type_{key}"] == "Double":
                        st.selectbox("Épaisseur de la lame d'air", 
                                     options=["(choisir écart air)", "5 à 7", "8 à 9", "10 à 11", "12 à 13", "cas de fenetre double"],
                                     key=f"window_gap_{key}")
                    st.number_input(f"Surface des portes {label} (m²)", min_value=0.0, step=0.1, key=f"area_door_{key}")
                    if st.session_state[f"area_door_{key}"] > 0:
                        st.selectbox("Contact de la porte", options=["(choisir contact)", "Exterieur", "Local Non Chauffé"], key=f"door_contact_{key}")
                        st.selectbox("Type de porte", options=[
                            "(choisir type de porte)", "Portes Opaques en Bois", "Portes Opaques en Metal", 
                            "Portes en Bois avec une proportion de vitrage <30%", 
                            "Portes en Bois avec une proportion de vitrage entre 30% et 60%", 
                            "Portes en Metal équipées de vitrage simple"
                        ], key=f"door_type_{key}")
    # Section pour un local non chauffé attenant
    st.subheader("Local non chauffé attenant")
    st.checkbox("Présence d'un mur vers un local non chauffé ?", key="use_local_nc")
    if st.session_state.use_local_nc:
        st.selectbox("Paroi séparant le local non chauffé", options=["(choisir)"] + list(st.session_state.walls.keys()), key="wall_local_nc")
        st.number_input("Surface de cette paroi (m²)", min_value=0.0, step=0.1, key="area_local_nc")
        st.number_input("Température intérieure (°C)", value=st.session_state.Tint_local_nc, key="Tint_local_nc")
        # Température extérieure de référence (calculée automatiquement d'après la zone)
        if st.session_state.zone and (st.session_state.Text_local_nc == 0 or st.session_state.Text_local_nc is None):
            st.session_state.Text_local_nc = get_temperature_ext(st.session_state.zone, float(st.session_state.altitude))
        st.number_input("Température extérieure (°C)", value=st.session_state.Text_local_nc if st.session_state.Text_local_nc is not None else 0.0, key="Text_local_nc")
        st.number_input("Température dans le local non chauffé (°C)", value=st.session_state.Tesp_local_nc, key="Tesp_local_nc")
    # Boutons de navigation avec validations
    col_prev, col_next = st.columns([1, 1])
    if col_prev.button("← Retour"):
        st.session_state.page = 1
    if col_next.button("Suivant →"):
        erreurs = []
        for label, key in orientations:
            if st.session_state.get(f"use_{key}"):
                if st.session_state.get(f"{key}_wall") in [None, "", "(choisir)"]:
                    erreurs.append(f"Choisissez une paroi pour **{label}**.")
                if key not in ["plancher_bas", "plancher_terrasse"]:
                    if st.session_state.get(f"homogeneous_{key}", False):
                        if st.session_state.get(f"area_wall_{key}", 0.0) <= 0:
                            erreurs.append(f"Surface du mur **{label}** manquante.")
                    else:
                        wall_area = st.session_state.get(f"area_wall_{key}", 0.0)
                        if wall_area <= 0:
                            erreurs.append(f"Surface du mur **{label}** invalide.")
                        win_area = st.session_state.get(f"area_window_{key}", 0.0)
                        if win_area > 0:
                            if st.session_state.get(f"window_type_{key}") in [None, "", "(choisir type)"] \
                               or st.session_state.get(f"window_material_{key}") in [None, "", "(choisir matériau)"]:
                                erreurs.append(f"Précisez le **type de vitrage** et le **matériau** de la fenêtre ({label}).")
                            if st.session_state.get(f"window_type_{key}") == "Double" and \
                               st.session_state.get(f"window_gap_{key}") in [None, "", "(choisir écart air)"]:
                                erreurs.append(f"Précisez l'**épaisseur d'air** pour le vitrage double ({label}).")
                        door_area = st.session_state.get(f"area_door_{key}", 0.0)
                        if door_area > 0:
                            if st.session_state.get(f"door_contact_{key}") in [None, "", "(choisir contact)"] or \
                               st.session_state.get(f"door_type_{key}") in [None, "", "(choisir type de porte)"]:
                                erreurs.append(f"Précisez le **type de porte** pour {label}.")
        if st.session_state.use_local_nc:
            if st.session_state.wall_local_nc in [None, "", "(choisir)"]:
                erreurs.append("Choisissez la paroi pour le local non chauffé.")
            if st.session_state.area_local_nc <= 0:
                erreurs.append("Surface du mur local non chauffé invalide.")
        if erreurs:
            for e in erreurs:
                st.error(e)
        else:
            st.session_state.page = 3

# ---- Page 3: Renouvellement d'air (infiltrations) ----
if page == 3:
    st.header("4. Déperditions par renouvellement d'air")
    st.number_input("Volume chauffé du bâtiment (m³)", min_value=0.0, step=1.0, key="volume")
    st.markdown("*Ajoutez les ouvertures contribuant aux infiltrations (facultatif)* :")
    P0_vals = {"Fenêtre ou porte-fenêtre": 4.0, "Porte avec seuil et joint": 1.2, "Porte": 6.0, "Double fenêtre": 2.4}
    inf_options = list(P0_vals.keys())
    st.selectbox("Type d'ouverture", options=inf_options, key="infiltration_type")
    st.number_input("Nombre d'éléments", min_value=0, step=1, key="infiltration_number")
    st.number_input("Surface totale de ces éléments (m²)", min_value=0.0, step=0.1, key="infiltration_surface")
    if st.button("Ajouter cette ouverture"):
        if st.session_state.infiltration_number > 0 and st.session_state.infiltration_surface > 0:
            st.session_state.infiltration_entries.append((
                st.session_state.infiltration_type,
                st.session_state.infiltration_number,
                st.session_state.infiltration_surface
            ))
            st.session_state.infiltration_number = 0
            st.session_state.infiltration_surface = 0.0
        else:
            st.error("Veuillez indiquer un nombre et une surface valides.")
    if st.session_state.infiltration_entries:
        st.text_area("Ouvertures ajoutées :", 
                     "\n".join(f"{n}× {typ}, {surf} m²" for typ, n, surf in st.session_state.infiltration_entries), 
                     height=100)
    # Boutons de navigation
    col_prev, col_next = st.columns([1, 1])
    if col_prev.button("← Retour"):
        st.session_state.page = 2
    if col_next.button("Calculer →"):
        if st.session_state.volume <= 0:
            st.error("Veuillez renseigner le volume chauffé.")
        else:
            st.session_state.page = 4

# ---- Page 4: Résultats finaux ----
if page == 4:
    st.header("5. Résultats des déperditions thermiques")
    # Calcul des déperditions par transmission pour chaque orientation
    resultats = []
    total_transmissions = 0.0
    for label, key in orientations:
        if st.session_state.get(f"use_{key}"):
            nom_paroi = st.session_state.get(f"{key}_wall")
            if not nom_paroi or nom_paroi == "(choisir)":
                continue
            U_wall = st.session_state.walls[nom_paroi]['U'] if nom_paroi in st.session_state.walls else 0.0
            if key in ["plancher_bas", "plancher_terrasse"]:
                # Plancher bas / Toiture : toujours homogène, pas d'ouvertures
                area = st.session_state.get(f"area_wall_{key}", 0.0)
                perte = U_wall * area
                resultats.append({"Élément": label, "Déperdition (W/°C)": perte})
                total_transmissions += perte
            else:
                if st.session_state.get(f"homogeneous_{key}", False):
                    area = st.session_state.get(f"area_wall_{key}", 0.0)
                    perte = U_wall * area
                    resultats.append({"Élément": label, "Déperdition (W/°C)": perte})
                    total_transmissions += perte
                else:
                    # Partie opaque du mur
                    wall_area = st.session_state.get(f"area_wall_{key}", 0.0)
                    perte_mur = U_wall * wall_area
                    # Fenêtres
                    perte_fen = 0.0
                    fen_area = st.session_state.get(f"area_window_{key}", 0.0)
                    if fen_area and fen_area > 0:
                        type_fen = st.session_state.get(f"window_type_{key}")
                        mat_fen = st.session_state.get(f"window_material_{key}")
                        gap = st.session_state.get(f"window_gap_{key}") if type_fen == "Double" else None
                        k_fen_base = get_k_window(type_fen, mat_fen, gap)
                        if k_fen_base:
                            # Ajout des résistances surface int/ext pour la fenêtre
                            R_fen = (1 / k_fen_base) + 0.215  # 0.025+0.03+0.16 = 0.215
                            U_fen = 1 / R_fen if R_fen != 0 else 0.0
                            perte_fen = U_fen * fen_area
                    # Portes
                    perte_por = 0.0
                    por_area = st.session_state.get(f"area_door_{key}", 0.0)
                    if por_area and por_area > 0:
                        contact = st.session_state.get(f"door_contact_{key}")
                        type_por = st.session_state.get(f"door_type_{key}")
                        k_por = get_k_door(contact, type_por)
                        if k_por:
                            perte_por = k_por * por_area
                    # Somme des pertes orientation
                    perte_orient = perte_mur + perte_fen + perte_por
                    resultats.append({"Élément": label, "Déperdition (W/°C)": perte_orient})
                    total_transmissions += perte_orient
    # Mur vers local non chauffé
    perte_local_nc = 0.0
    if st.session_state.use_local_nc and st.session_state.wall_local_nc and st.session_state.wall_local_nc != "(choisir)":
        nom_paroi_nc = st.session_state.wall_local_nc
        if nom_paroi_nc in st.session_state.walls:
            U_nc = st.session_state.walls[nom_paroi_nc]['U']
            area_nc = st.session_state.area_local_nc
            Tint = st.session_state.Tint_local_nc
            Tesp = st.session_state.Tesp_local_nc
            Text = st.session_state.Text_local_nc if st.session_state.Text_local_nc is not None else 0.0
            # Calcul du facteur Tau
            Tau = (Tint - Tesp) / (Tint - Text) if (Tint - Text) != 0 else 0.0
            perte_local_nc = Tau * U_nc * area_nc
            resultats.append({"Élément": "Mur local non chauffé", "Déperdition (W/°C)": perte_local_nc})
            total_transmissions += perte_local_nc
    # Calcul des déperditions par renouvellement d'air (infiltrations)
    debit_total = 0.0
    for typ, n, surf in st.session_state.infiltration_entries:
        P0 = P0_vals.get(typ, 0.0)
        debit_total += n * P0 * surf
    qv = 0.6 * st.session_state.volume
    perte_air = 0.34 * (debit_total + qv)
    resultats.append({"Élément": "Renouvellement d'air", "Déperdition (W/°C)": perte_air})
    # Total général
    total = total_transmissions + perte_air
    resultats.append({"Élément": "Total", "Déperdition (W/°C)": total})
    # Affichage du tableau de résultats
    df_res = pd.DataFrame(resultats)
    st.table(df_res.set_index("Élément").style.format({"Déperdition (W/°C)": "{:.3f}"}))
    # Calcul et affichage de la puissance de chauffage requise
    if st.session_state.zone:
        t_ext = get_temperature_ext(st.session_state.zone, float(st.session_state.altitude))
    else:
        t_ext = None
    st.number_input("Température intérieure de calcul (°C)", value=st.session_state.temperature_int, key="temperature_int")
    if t_ext is None:
        t_ext = 0.0
        st.number_input("Température extérieure de calcul (°C)", value=t_ext, key="ext_temp_input")
        t_ext = st.session_state.ext_temp_input
    else:
        st.write(f"Température extérieure de référence : **{t_ext}°C** (Zone {st.session_state.zone})")
    T_int = st.session_state.temperature_int
    T_ext = t_ext if t_ext is not None else 0.0
    Q_w = total * (T_int - T_ext)  # en W
    st.write(f"**Puissance de chauffage estimée :** {Q_w/1000:.2f} kW " +
             f"(ΔT = {T_int - T_ext:.1f}°C)")
    # Export CSV des résultats
    csv = df_res.to_csv(index=False, float_format="%.3f")
    st.download_button("💾 Exporter les résultats en CSV", data=csv, file_name="deperditions_thermiques.csv", mime="text/csv")
    # Diagramme en barres des déperditions par catégorie (hors total)
    df_chart = df_res[df_res["Élément"] != "Total"].set_index("Élément")
    st.bar_chart(df_chart)
    # Bouton pour réinitialiser/recommencer
    if st.button("↻ Recommencer la saisie"):
        st.session_state.page = 0
