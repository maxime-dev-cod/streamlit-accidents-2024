import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

st.title("Entraînement du modèle")

uploaded_file = st.file_uploader(
    "Importer un CSV",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(
        uploaded_file,
        sep=";",
        encoding="utf-8",
        low_memory=False
    )

    st.subheader("Aperçu")
    st.dataframe(df.head())

    st.subheader("Choix de la cible")

    target = st.selectbox(
        "Variable cible",
        df.columns
    )

    features = st.multiselect(
        "Variables explicatives",
        [c for c in df.columns if c != target]
    )

    if st.button("Lancer l'entraînement"):

        if len(features) == 0:
            st.warning("Choisir au moins une variable.")
        else:

            data = df[features + [target]].dropna()

            X = pd.get_dummies(data[features])
            y = data[target]

            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42
            )

            model = RandomForestClassifier()

            model.fit(X_train, y_train)

            predictions = model.predict(X_test)

            score = accuracy_score(
                y_test,
                predictions
            )

            st.success(
                f"Accuracy : {score:.2f}"
            )

            st.subheader("Importance des variables")

            importance = pd.DataFrame({
                "Variable": X.columns,
                "Importance": model.feature_importances_
            })

            importance = importance.sort_values(
                by="Importance",
                ascending=False
            )

            st.dataframe(importance)
