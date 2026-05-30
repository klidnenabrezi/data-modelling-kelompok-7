import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Teen Social Media and Wellbeing Dashboard",
    layout="wide"
)


df = pd.read_excel("raw/Book2.xlsx")


df = df.drop(columns=[
    "Unnamed: 13",
    "Unnamed: 14",
    "Daily Social Media",
    "StressLevel"
])


def usage_category(hours):
    if hours < 3:
        return "Low"
    elif hours < 6:
        return "Moderate"
    else:
        return "High"

df["social_media_usage_group"] = df["daily_social_media_hours"].apply(usage_category)

df["mental_strain_score"] = df[
    ["stress_level", "anxiety_level", "addiction_level"]
].mean(axis=1)


st.title("Teen Social Media and Wellbeing Dashboard")
st.write(
    "This dashboard explores social media behavior, sleep, academic performance, "
    "and wellbeing indicators using descriptive analysis."
)

## KPI cards ##
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Records", f"{len(df):,}")
col2.metric("Avg Social Media Hours", f"{df['daily_social_media_hours'].mean():.2f}")
col3.metric("Avg Sleep Hours", f"{df['sleep_hours'].mean():.2f}")
col4.metric("Avg Mental Strain", f"{df['mental_strain_score'].mean():.2f}")
col5.metric("Depression Indicator Rate", f"{df['depression_label'].mean() * 100:.2f}%")

st.divider()

## Summary ##
usage_group_summary = df.groupby("social_media_usage_group").agg(
    records=("social_media_usage_group", "count"),
    avg_social_media_hours=("daily_social_media_hours", "mean"),
    avg_sleep_hours=("sleep_hours", "mean"),
    avg_academic_performance=("academic_performance", "mean"),
    avg_mental_strain_score=("mental_strain_score", "mean")
).round(2).reset_index()

platform_summary = df.groupby("platform_usage").agg(
    records=("platform_usage", "count"),
    avg_social_media_hours=("daily_social_media_hours", "mean"),
    avg_sleep_hours=("sleep_hours", "mean"),
    avg_academic_performance=("academic_performance", "mean"),
    avg_mental_strain_score=("mental_strain_score", "mean")
).round(2).reset_index()

depression_summary = df.groupby("depression_label").agg(
    records=("depression_label", "count"),
    avg_social_media_hours=("daily_social_media_hours", "mean"),
    avg_sleep_hours=("sleep_hours", "mean"),
    avg_stress_level=("stress_level", "mean"),
    avg_anxiety_level=("anxiety_level", "mean"),
    avg_addiction_level=("addiction_level", "mean"),
    avg_mental_strain_score=("mental_strain_score", "mean")
).round(2).reset_index()


st.header("1. Social Media Profile")

left, right = st.columns(2)

with left:
    fig_platform = px.bar(
        platform_summary,
        x="platform_usage",
        y="records",
        title="Records by Platform Usage",
        text="records"
    )
    st.plotly_chart(fig_platform, use_container_width=True)

with right:
    fig_usage = px.bar(
        usage_group_summary,
        x="social_media_usage_group",
        y="records",
        title="Records by Social Media Usage Group",
        text="records",
        category_orders={"social_media_usage_group": ["Low", "Moderate", "High"]}
    )
    st.plotly_chart(fig_usage, use_container_width=True)

st.divider()

st.header("2. Mental Strain Comparison")

left, right = st.columns(2)

with left:
    fig_usage_strain = px.bar(
        usage_group_summary,
        x="social_media_usage_group",
        y="avg_mental_strain_score",
        title="Average Mental Strain by Usage Group",
        text="avg_mental_strain_score",
        category_orders={"social_media_usage_group": ["Low", "Moderate", "High"]}
    )
    st.plotly_chart(fig_usage_strain, use_container_width=True)

with right:
    fig_platform_strain = px.bar(
        platform_summary,
        x="platform_usage",
        y="avg_mental_strain_score",
        title="Average Mental Strain by Platform",
        text="avg_mental_strain_score"
    )
    st.plotly_chart(fig_platform_strain, use_container_width=True)

st.info(
    "Mental strain scores are similar across usage groups and platform categories, "
    "suggesting that these broad social media variables do not strongly separate wellbeing outcomes."
)

st.divider()


st.header("3. Depression Label Comparison")

depression_long = depression_summary.melt(
    id_vars=["depression_label", "records"],
    value_vars=[
        "avg_social_media_hours",
        "avg_sleep_hours",
        "avg_stress_level",
        "avg_anxiety_level",
        "avg_mental_strain_score"
    ],
    var_name="metric",
    value_name="average_value"
)

metric_labels = {
    "avg_social_media_hours": "Social Media Hours",
    "avg_sleep_hours": "Sleep Hours",
    "avg_stress_level": "Stress Level",
    "avg_anxiety_level": "Anxiety Level",
    "avg_mental_strain_score": "Mental Strain Score"
}

depression_long["metric"] = depression_long["metric"].map(metric_labels)

depression_long["depression_label"] = depression_long["depression_label"].map({
    0: "No Indicator",
    1: "Indicator"
})

fig_depression = px.bar(
    depression_long,
    x="metric",
    y="average_value",
    color="depression_label",
    barmode="group",
    title="Average Indicators by Depression Label",
    labels={
        "metric": "Metric",
        "average_value": "Average Value",
        "depression_label": "Depression Label"
    }
)


st.plotly_chart(fig_depression, use_container_width=True)

st.warning(
    "The depression-indicator group contains only 31 records, compared with 1,169 non-indicator records. "
    "This comparison should be interpreted as exploratory, not causal or diagnostic."
)

st.divider()


st.header("4. Correlation View")

numeric_cols = [
    "age",
    "daily_social_media_hours",
    "sleep_hours",
    "screen_time_before_sleep",
    "academic_performance",
    "physical_activity",
    "stress_level",
    "anxiety_level",
    "addiction_level",
    "mental_strain_score"
]

corr = df[numeric_cols].corr().round(2)

fig_corr = px.imshow(
    corr,
    text_auto=True,
    title="Correlation Matrix of Numeric Variables",
    height=700
)

fig_corr.update_layout(
    margin=dict(l=80, r=80, t=80, b=80)
)

st.plotly_chart(fig_corr, use_container_width=True)

st.write(
    "Most behavioral variables show weak linear relationships with mental strain. "
    "The strongest correlations with mental strain come from stress, anxiety, and addiction levels, "
    "which is expected because mental strain score is calculated from those variables."
)