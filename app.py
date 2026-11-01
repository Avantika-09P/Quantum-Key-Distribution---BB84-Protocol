import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, mean_absolute_error, log_loss,
    confusion_matrix, classification_report, balanced_accuracy_score,
    matthews_corrcoef
)

st.set_page_config(page_title="QKD Dataset Analysis", page_icon="🔐", layout="wide")

st.markdown("""
<style>
.main {background-color: #f7f8fc;}
.block-container {padding-top: 1.6rem; padding-bottom: 2rem;}
[data-testid="stMetric"] {
    background: #1e293b;
    padding: 16px;
    border: 1px solid #334155;
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
}
div[data-testid="stTabs"] button {font-weight: 600;}
.small-muted {color: #667085; font-size: 0.9rem;}
</style>
""", unsafe_allow_html=True)

st.title("🔐 QKD Dataset Analysis Studio")
st.caption("Interactive exploratory data analysis, preprocessing and classical machine-learning evaluation.")

with st.sidebar:
    st.header("Dataset")
    uploaded = st.file_uploader("Upload your QKD CSV file", type=["csv"])
    st.divider()
    st.markdown("**Quick guide**")
    st.caption("Upload `QKD_dataset.csv` to explore the data, inspect quality, visualize patterns and train classifiers.")

if uploaded is None:
    st.info("Upload your `QKD_dataset.csv` file from the sidebar to begin.")
    st.markdown("""
    **Included in this dashboard**
    - Dataset overview, sample records and column data types
    - Missing-value and duplicate analysis
    - Descriptive statistics and interactive visualizations
    - Target-class distribution
    - Train/test split and preprocessing
    - Classical model comparison with classification metrics
    """)
    st.stop()

try:
    df = pd.read_csv(uploaded)
except Exception as e:
    st.error(f"Could not read this CSV: {e}")
    st.stop()

if df.empty:
    st.error("The uploaded CSV contains no rows.")
    st.stop()

# Header metrics
st.markdown("### Dataset overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", f"{df.shape[0]:,}")
c2.metric("Columns", f"{df.shape[1]:,}")
c3.metric("Missing cells", f"{int(df.isna().sum().sum()):,}")
c4.metric("Duplicate rows", f"{int(df.duplicated().sum()):,}")

tabs = st.tabs(["Overview", "Data quality", "Explore", "Model lab"])

with tabs[0]:
    left, right = st.columns([1.5, 1])
    with left:
        st.subheader("Data preview")
        st.dataframe(df.head(20), use_container_width=True, height=420)
    with right:
        st.subheader("Column information")
        info = pd.DataFrame({
            "Column": df.columns.astype(str),
            "Data type": [str(x) for x in df.dtypes],
            "Non-null": [int(df[c].notna().sum()) for c in df.columns],
            "Unique": [int(df[c].nunique(dropna=True)) for c in df.columns]
        })
        st.dataframe(info, use_container_width=True, height=420)
    st.subheader("Descriptive statistics")
    st.dataframe(df.describe(include="all").T, use_container_width=True)

with tabs[1]:
    st.subheader("Missing values")
    missing = df.isna().sum().rename("Missing values").to_frame()
    missing["Missing %"] = (missing["Missing values"] / len(df) * 100).round(2)
    missing = missing.sort_values("Missing values", ascending=False)
    st.dataframe(missing, use_container_width=True)
    if missing["Missing values"].sum() > 0:
        fig, ax = plt.subplots(figsize=(10, 3.8))
        plot_missing = missing[missing["Missing values"] > 0]
        ax.bar(plot_missing.index.astype(str), plot_missing["Missing values"])
        ax.set_ylabel("Count")
        ax.set_title("Missing values by column")
        ax.tick_params(axis="x", rotation=45)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.success("No missing values found.")
    st.subheader("Duplicate records")
    dup_count = int(df.duplicated().sum())
    st.write(f"**{dup_count:,}** duplicate rows detected.")
    if dup_count:
        if st.checkbox("Show duplicate rows"):
            st.dataframe(df[df.duplicated(keep=False)], use_container_width=True)
    st.subheader("Unique values by column")
    unique_df = pd.DataFrame({
        "Unique values": df.nunique(dropna=True),
        "Distinct examples": [
            ", ".join(map(str, df[c].dropna().unique()[:8])) for c in df.columns
        ]
    })
    st.dataframe(unique_df, use_container_width=True)

with tabs[2]:
    st.subheader("Univariate exploration")
    col_a, col_b = st.columns(2)
    with col_a:
        selected = st.selectbox("Choose a column", df.columns, key="univariate_col")
    with col_b:
        chart_type = st.selectbox("Visualization", ["Auto", "Histogram", "Bar chart"], key="chart_type")
    series = df[selected].dropna()
    fig, ax = plt.subplots(figsize=(8, 4))
    if pd.api.types.is_numeric_dtype(series) and chart_type != "Bar chart":
        bins = st.slider("Histogram bins", 5, 60, 25)
        ax.hist(series, bins=bins, edgecolor="white")
        ax.set_xlabel(selected)
        ax.set_ylabel("Frequency")
    else:
        counts = series.astype(str).value_counts().head(30)
        ax.bar(counts.index, counts.values)
        ax.set_ylabel("Count")
        ax.tick_params(axis="x", rotation=45)
    ax.set_title(f"Distribution of {selected}")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Numeric feature relationships")
    numeric = df.select_dtypes(include=np.number)
    if numeric.shape[1] >= 2:
        corr = numeric.corr(numeric_only=True)
        fig, ax = plt.subplots(figsize=(9, 6))
        im = ax.imshow(corr, aspect="auto", vmin=-1, vmax=1)
        ax.set_xticks(range(len(corr.columns)), corr.columns, rotation=60, ha="right")
        ax.set_yticks(range(len(corr.index)), corr.index)
        ax.set_title("Pearson correlation matrix")
        fig.colorbar(im, ax=ax, label="Correlation")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("At least two numeric columns are required for a correlation matrix.")

with tabs[3]:
    st.subheader("Train and compare classical classifiers")
    st.caption("The notebook's model set is retained: Random Forest, Extra Trees, Logistic Regression, SVC, KNN and MLP.")
    if len(df.columns) < 2:
        st.warning("At least one feature column and one target column are required.")
        st.stop()

    default_target = "label" if "label" in df.columns else str(df.columns[-1])
    target = st.selectbox("Target column", df.columns, index=list(df.columns).index(default_target))
    feature_options = [c for c in df.columns if c != target]
    features = st.multiselect("Feature columns", feature_options, default=feature_options)
    test_size = st.slider("Test set proportion", 0.10, 0.40, 0.20, 0.05)
    random_state = st.number_input("Random state", min_value=0, max_value=99999, value=42, step=1)
    stratify = st.checkbox("Use stratified split (recommended for classification)", value=True)
    chosen_models = st.multiselect(
        "Models to train",
        ["Random Forest", "Extra Trees", "Logistic Regression", "SVC", "KNN", "MLP"],
        default=["Random Forest", "Extra Trees", "Logistic Regression", "SVC", "KNN", "MLP"]
    )

    if not features:
        st.warning("Select at least one feature column.")
        st.stop()

    working = df[features + [target]].dropna(subset=[target]).copy()
    X = working[features]
    y_raw = working[target].astype(str)
    class_counts = y_raw.value_counts()
    st.write(f"**Rows available for modelling:** {len(working):,}  |  **Classes:** {y_raw.nunique()}")
    st.dataframe(class_counts.rename_axis("Class").reset_index(name="Count"), use_container_width=True)

    if len(chosen_models) == 0:
        st.info("Choose at least one model.")
    elif st.button("🚀 Run model comparison", type="primary", use_container_width=True):
        if y_raw.nunique() < 2:
            st.error("The selected target has fewer than two classes.")
            st.stop()
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y_raw)
        numeric_features = X.select_dtypes(include=np.number).columns.tolist()
        categorical_features = [c for c in features if c not in numeric_features]

        numeric_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])
        categorical_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ])
        transformers = []
        if numeric_features:
            transformers.append(("num", numeric_pipe, numeric_features))
        if categorical_features:
            transformers.append(("cat", categorical_pipe, categorical_features))
        preprocess = ColumnTransformer(transformers=transformers)

        stratify_y = y if stratify and class_counts.min() >= 2 else None
        if stratify and stratify_y is None:
            st.warning("Stratification was disabled because at least one class has fewer than two records.")
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=int(random_state), stratify=stratify_y
            )
        except ValueError as e:
            st.error(f"Could not create train/test split: {e}")
            st.stop()

        model_map = {
            "Random Forest": RandomForestClassifier(n_estimators=300, random_state=int(random_state), class_weight="balanced"),
            "Extra Trees": ExtraTreesClassifier(n_estimators=300, random_state=int(random_state), class_weight="balanced"),
            "Logistic Regression": LogisticRegression(max_iter=2000, class_weight="balanced"),
            "SVC": SVC(probability=True, class_weight="balanced", random_state=int(random_state)),
            "KNN": KNeighborsClassifier(n_neighbors=max(1, min(5, len(X_train)))),
            "MLP": MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=600, random_state=int(random_state), early_stopping=True)
        }

        rows, fitted = [], {}
        progress = st.progress(0)
        status = st.empty()
        for i, name in enumerate(chosen_models):
            status.write(f"Training {name}...")
            pipe = Pipeline([("preprocess", preprocess), ("model", model_map[name])])
            try:
                pipe.fit(X_train, y_train)
                pred = pipe.predict(X_test)
                row = {
                    "Model": name,
                    "Accuracy": accuracy_score(y_test, pred),
                    "Precision": precision_score(y_test, pred, average="weighted", zero_division=0),
                    "Recall": recall_score(y_test, pred, average="weighted", zero_division=0),
                    "F1-score": f1_score(y_test, pred, average="weighted", zero_division=0),
                    "Balanced accuracy": balanced_accuracy_score(y_test, pred),
                    "MCC": matthews_corrcoef(y_test, pred),
                    "MSE": mean_squared_error(y_test, pred),
                    "MAE": mean_absolute_error(y_test, pred)
                }
                try:
                    probs = pipe.predict_proba(X_test)
                    row["Log loss"] = log_loss(y_test, probs, labels=np.arange(len(label_encoder.classes_)))
                except Exception:
                    row["Log loss"] = np.nan
                rows.append(row)
                fitted[name] = (pipe, pred)
            except Exception as e:
                st.error(f"{name} failed: {e}")
            progress.progress((i + 1) / len(chosen_models))

        status.empty()
        progress.empty()
        if not rows:
            st.error("No model completed successfully.")
        else:
            results = pd.DataFrame(rows).sort_values("F1-score", ascending=False).reset_index(drop=True)
            st.session_state["qkd_results"] = results
            st.session_state["qkd_fitted"] = fitted
            st.session_state["qkd_y_test"] = y_test
            st.session_state["qkd_classes"] = label_encoder.classes_
            st.session_state["qkd_target"] = target
            st.success("Model comparison completed.")

    if "qkd_results" in st.session_state:
        results = st.session_state["qkd_results"]
        st.subheader("Model comparison")
        display_results = results.copy()
        metric_cols = display_results.select_dtypes(include=np.number).columns
        display_results[metric_cols] = display_results[metric_cols].round(4)
        st.dataframe(display_results, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Download metrics as CSV",
            data=results.to_csv(index=False).encode("utf-8"),
            file_name="qkd_model_comparison.csv",
            mime="text/csv"
        )

        metric_to_plot = st.selectbox("Compare metric", ["Accuracy", "Precision", "Recall", "F1-score", "Balanced accuracy", "MCC"])
        fig, ax = plt.subplots(figsize=(9, 4))
        ax.bar(results["Model"], results[metric_to_plot])
        ax.set_ylim(min(0, float(results[metric_to_plot].min()) - 0.05), 1.05 if metric_to_plot != "MCC" else 1.05)
        ax.set_ylabel(metric_to_plot)
        ax.set_title(f"Model comparison — {metric_to_plot}")
        ax.tick_params(axis="x", rotation=25)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        fitted = st.session_state["qkd_fitted"]
        selected_model = st.selectbox("Inspect model predictions", list(fitted.keys()))
        pipe, pred = fitted[selected_model]
        y_test = st.session_state["qkd_y_test"]
        classes = st.session_state["qkd_classes"]
        cm = confusion_matrix(y_test, pred, labels=np.arange(len(classes)))
        fig, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(cm)
        ax.set_xticks(range(len(classes)), classes, rotation=45, ha="right")
        ax.set_yticks(range(len(classes)), classes)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        ax.set_title(f"Confusion matrix — {selected_model}")
        for (r, c), value in np.ndenumerate(cm):
            ax.text(c, r, str(value), ha="center", va="center")
        fig.colorbar(im, ax=ax)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        report = classification_report(
            y_test, pred, labels=np.arange(len(classes)), target_names=[str(x) for x in classes],
            zero_division=0, output_dict=True
        )
        st.subheader("Classification report")
        st.dataframe(pd.DataFrame(report).T.round(4), use_container_width=True)

st.divider()
st.caption("Note: Metrics are calculated from the uploaded dataset and selected train/test split. They are not hard-coded results; use a separate validation strategy before making research or deployment claims.")
