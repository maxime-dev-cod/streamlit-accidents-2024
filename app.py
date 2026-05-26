import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Accidents de la route en France - 2024",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Analyse des accidents de la route en France (2024)")
st.markdown("Données issues du fichier BAAC - ONISR / data.gouv.fr")


@st.cache_data
def load_data():

    df = pd.read_csv(
        "accidents_2024.csv",
        sep=";",
        encoding="utf-8",
        low_memory=False
    )

    return df


try:
    df = load_data()
except:
    st.error(
        "Le fichier accidents_2024.csv est introuvable. "
    )
    st.stop()


st.subheader("📄 Aperçu des données")
st.dataframe(df.head())

st.write(f"Nombre de lignes : {df.shape[0]}")
st.write(f"Nombre de colonnes : {df.shape[1]}")


st.sidebar.header("⚙️ Filtres")


if "dep" in df.columns:
    departements = sorted(df["dep"].dropna().astype(str).unique())

    selected_dep = st.sidebar.multiselect(
        "Choix des départements",
        departements,
        default=departements[:5],
    )

    df_filtered = df[df["dep"].astype(str).isin(selected_dep)]
else:
    df_filtered = df


st.subheader("📊 Indicateurs clés")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Nombre d'accidents",
        len(df_filtered)
    )

with col2:
    if "lum" in df_filtered.columns:
        nuit = len(df_filtered[df_filtered["lum"] == 5])
        st.metric(
            "Accidents de nuit",
            nuit
        )
    else:
        st.metric("Accidents de nuit", "N/A")


if "dep" in df_filtered.columns:

    st.subheader("🗺️ Accidents par département")

    dep_count = (
        df_filtered["dep"]
        .astype(str)
        .value_counts()
        .reset_index()
    )

dep_count.columns = ["Département", "Nombre d'accidents"]

# 🔥 IMPORTANT : on fixe l’ordre EXACT des départements sélectionnés
dep_count = dep_count[dep_count["Département"].isin(selected_dep)]

fig_dep = px.bar(
    dep_count,
    x="Nombre d'accidents",
    y="Département",
    orientation="h",
    text="Nombre d'accidents",
    category_orders={
        "Département": selected_dep
    },
    title="Accidents par département"
)

fig_dep.update_layout(
    yaxis=dict(
        type="category",   # 🔥 clé du problème
        categoryorder="array",
        categoryarray=selected_dep
    ),
    height=400
)

fig_dep.update_traces(textposition="outside")

st.plotly_chart(fig_dep, use_container_width=True)


if "lum" in df_filtered.columns:

    st.subheader("🌙 Répartition des accidents selon la luminosité")

    lum_mapping = {
        1: "Plein jour",
        2: "Crépuscule",
        3: "Nuit sans éclairage",
        4: "Nuit avec éclairage non allumé",
        5: "Nuit avec éclairage allumé"
    }

    lum_count = (
        df_filtered["lum"]
        .map(lum_mapping)
        .value_counts()
        .reset_index()
    )

    lum_count.columns = ["Condition", "Nombre"]

    fig_lum = px.pie(
        lum_count,
        names="Condition",
        values="Nombre",
        title="Répartition des accidents selon la luminosité"
    )

    st.plotly_chart(fig_lum, use_container_width=True)


if "atm" in df_filtered.columns:

    st.subheader("🌧️ Conditions météo")

    meteo_mapping = {
        1: "Normale",
        2: "Pluie légère",
        3: "Pluie forte",
        4: "Neige / grêle",
        5: "Brouillard",
        6: "Vent fort",
        7: "Temps éblouissant",
        8: "Temps couvert",
        9: "Autre"
    }

    meteo_count = (
        df_filtered["atm"]
        .map(meteo_mapping)
        .value_counts()
        .reset_index()
    )

    meteo_count.columns = ["Météo", "Nombre"]

    fig_meteo = px.bar(
        meteo_count,
        x="Météo",
        y="Nombre",
        title="Accidents selon la météo"
    )

    st.plotly_chart(fig_meteo, use_container_width=True)


if "col" in df_filtered.columns:

    st.subheader("💥 Types de collision")

    collision_mapping = {
        1: "2 véhicules - frontale",
        2: "2 véhicules - arrière",
        3: "2 véhicules - côté",
        4: "3 véhicules et + en chaîne",
        5: "3 véhicules et + collisions multiples",
        6: "Autre collision",
        7: "Sans collision"
    }

    collision_count = (
        df_filtered["col"]
        .map(collision_mapping)
        .value_counts()
        .reset_index()
    )

    collision_count.columns = ["Collision", "Nombre"]

    fig_collision = px.bar(
        collision_count,
        x="Collision",
        y="Nombre",
        title="Types de collisions"
    )

    st.plotly_chart(fig_collision, use_container_width=True)


if "hrmn" in df_filtered.columns:

    st.subheader("⏰ Répartition des accidents par heure")

    df_filtered["heure"] = (
        df_filtered["hrmn"]
        .astype(str)
        .str[:2]
    )

    heure_count = (
        df_filtered["heure"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    heure_count.columns = ["Heure", "Nombre"]

    fig_hour = px.line(
        heure_count,
        x="Heure",
        y="Nombre",
        markers=True,
        title="Nombre d'accidents par heure"
    )

    st.plotly_chart(fig_hour, use_container_width=True)


st.subheader("📋 Données filtrées")
st.dataframe(df_filtered)
