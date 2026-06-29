# Insurance Claims Analytics Dashboard
# Built with Streamlit + Pandas + Plotly

import streamlit as st
import pandas as pd
import plotly.express as px

# ============= PAGE CONFIG =============
st.set_page_config(
    page_title="Insurance Claims Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============= COLORS =============
PRIMARY = "#1f77b4"
ACCENT = "#ff7f0e"
DANGER = "#d62728"
SUCCESS = "#2ca02c"

# ============= LOAD DATA =============
@st.cache_data
def load_data():
    df = pd.read_csv("Data/insurance_claims.csv")
    df['incident_date'] = pd.to_datetime(df['incident_date'])
    return df

df = load_data()

# ============= HEADER =============
st.title("📊 Insurance Claims Analytics Dashboard")
st.markdown("##### AI-powered insights into vehicle insurance claim patterns")
st.markdown("---")

# ============= KPIs =============
st.subheader("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Claims",
        value=f"{len(df):,}"
    )

with col2:
    st.metric(
        label="Avg Claim Amount",
        value=f"${df['total_claim_amount'].mean():,.0f}"
    )

with col3:
    fraud_rate = (df['fraud_reported'] == 'Y').mean() * 100
    st.metric(
        label="Fraud Rate",
        value=f"{fraud_rate:.1f}%",
        delta=f"{(df['fraud_reported'] == 'Y').sum()} flagged",
        delta_color="inverse"
    )

with col4:
    st.metric(
        label="Avg Customer Age",
        value=f"{df['age'].mean():.0f} yrs"
    )

st.markdown("---")

# ============= CHARTS ROW 1 =============
st.subheader("🔍 Claims Breakdown")
col1, col2 = st.columns(2)

with col1:
    # Claims by Incident Type
    incident_counts = df['incident_type'].value_counts().reset_index()
    incident_counts.columns = ['Incident Type', 'Count']
    
    fig1 = px.bar(
        incident_counts,
        x='Count',
        y='Incident Type',
        orientation='h',
        title="Claims by Incident Type",
        color='Count',
        color_continuous_scale='Blues'
    )
    fig1.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Claims by Severity
    severity_counts = df['incident_severity'].value_counts().reset_index()
    severity_counts.columns = ['Severity', 'Count']
    
    fig2 = px.pie(
        severity_counts,
        values='Count',
        names='Severity',
        title="Claims by Incident Severity",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

# ============= CHARTS ROW 2 =============
st.subheader("💰 Financial Analysis")
col1, col2 = st.columns(2)

with col1:
    # Claim Amount Distribution
    fig3 = px.histogram(
        df,
        x='total_claim_amount',
        nbins=40,
        title="Distribution of Claim Amounts",
        color_discrete_sequence=[PRIMARY]
    )
    fig3.update_layout(
        xaxis_title="Claim Amount ($)",
        yaxis_title="Number of Claims",
        height=400
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # Avg Claim Amount by State
    state_claims = df.groupby('incident_state')['total_claim_amount'].mean().reset_index()
    state_claims.columns = ['State', 'Avg Claim Amount']
    state_claims = state_claims.sort_values('Avg Claim Amount', ascending=True)
    
    fig4 = px.bar(
        state_claims,
        x='Avg Claim Amount',
        y='State',
        orientation='h',
        title="Average Claim Amount by State",
        color='Avg Claim Amount',
        color_continuous_scale='Oranges'
    )
    fig4.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig4, use_container_width=True)

# ============= CHARTS ROW 3 =============
st.subheader("🚨 Fraud Insights")
col1, col2 = st.columns(2)

with col1:
    # Fraud by Incident Type
    fraud_by_type = df.groupby('incident_type')['fraud_reported'].apply(
        lambda x: (x == 'Y').mean() * 100
    ).reset_index()
    fraud_by_type.columns = ['Incident Type', 'Fraud Rate %']
    
    fig5 = px.bar(
        fraud_by_type,
        x='Incident Type',
        y='Fraud Rate %',
        title="Fraud Rate by Incident Type",
        color='Fraud Rate %',
        color_continuous_scale='Reds'
    )
    fig5.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    # Claims Over Time
    df['month'] = df['incident_date'].dt.to_period('M').astype(str)
    monthly_claims = df.groupby('month').size().reset_index()
    monthly_claims.columns = ['Month', 'Claims']
    
    fig6 = px.line(
        monthly_claims,
        x='Month',
        y='Claims',
        title="Claims Over Time (Monthly)",
        markers=True
    )
    fig6.update_traces(line_color=PRIMARY, line_width=3)
    fig6.update_layout(height=400)
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# ============= DATA PREVIEW =============
with st.expander("📋 View Raw Data Preview"):
    st.dataframe(df.head(20), use_container_width=True)

# ============= CHARTS ROW 4: CUSTOMER DEMOGRAPHICS =============
st.subheader("👥 Customer Demographics")
col1, col2, col3 = st.columns(3)

with col1:
    # Gender Distribution (Donut)
    gender_counts = df['insured_sex'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    
    fig7 = px.pie(
        gender_counts,
        values='Count',
        names='Gender',
        title="Gender Distribution",
        hole=0.5,
        color_discrete_sequence=['#1f77b4', '#ff7f0e']
    )
    fig7.update_layout(height=350)
    st.plotly_chart(fig7, use_container_width=True)

with col2:
    # Education Level
    edu_counts = df['insured_education_level'].value_counts().reset_index()
    edu_counts.columns = ['Education', 'Count']
    
    fig8 = px.bar(
        edu_counts,
        x='Count',
        y='Education',
        orientation='h',
        title="Education Level",
        color='Count',
        color_continuous_scale='Teal'
    )
    fig8.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig8, use_container_width=True)

with col3:
    # Age Distribution
    fig9 = px.histogram(
        df,
        x='age',
        nbins=20,
        title="Customer Age Distribution",
        color_discrete_sequence=['#9467bd']
    )
    fig9.update_layout(xaxis_title="Age", yaxis_title="Count", height=350)
    st.plotly_chart(fig9, use_container_width=True)

# ============= CHARTS ROW 5: VEHICLE ANALYSIS =============
st.subheader("🚗 Vehicle Analysis")
col1, col2 = st.columns(2)

with col1:
    # Top 10 Auto Makes
    top_makes = df['auto_make'].value_counts().head(10).reset_index()
    top_makes.columns = ['Make', 'Count']
    
    fig10 = px.bar(
        top_makes,
        x='Count',
        y='Make',
        orientation='h',
        title="Top 10 Vehicle Makes (by Claims)",
        color='Count',
        color_continuous_scale='Viridis'
    )
    fig10.update_layout(showlegend=False, height=400, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig10, use_container_width=True)

with col2:
    # Claim Amount by Vehicle Age
    df['vehicle_age'] = 2026 - df['auto_year']
    avg_by_vehicle_age = df.groupby('vehicle_age')['total_claim_amount'].mean().reset_index()
    avg_by_vehicle_age.columns = ['Vehicle Age (Years)', 'Avg Claim Amount']
    
    fig11 = px.line(
        avg_by_vehicle_age,
        x='Vehicle Age (Years)',
        y='Avg Claim Amount',
        title="Avg Claim Amount by Vehicle Age",
        markers=True
    )
    fig11.update_traces(line_color='#ff7f0e', line_width=3)
    fig11.update_layout(height=400)
    st.plotly_chart(fig11, use_container_width=True)

# ============= CHARTS ROW 6: TIME PATTERNS =============
st.subheader("⏰ Time Patterns")
col1, col2 = st.columns(2)

with col1:
    # Incidents by Hour of Day
    hour_counts = df.groupby('incident_hour_of_the_day').size().reset_index()
    hour_counts.columns = ['Hour', 'Incidents']
    
    fig12 = px.bar(
        hour_counts,
        x='Hour',
        y='Incidents',
        title="Incidents by Hour of Day",
        color='Incidents',
        color_continuous_scale='Sunset'
    )
    fig12.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig12, use_container_width=True)

with col2:
    # Day of Week Analysis
    df['day_of_week'] = df['incident_date'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = df['day_of_week'].value_counts().reindex(day_order).reset_index()
    day_counts.columns = ['Day', 'Claims']
    
    fig13 = px.bar(
        day_counts,
        x='Day',
        y='Claims',
        title="Claims by Day of Week",
        color='Claims',
        color_continuous_scale='Plasma'
    )
    fig13.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig13, use_container_width=True)

# ============= CHARTS ROW 7: CLAIM BREAKDOWN =============
st.subheader("💼 Claim Type Breakdown")
col1, col2 = st.columns(2)

with col1:
    # Injury vs Property vs Vehicle Claim Comparison
    claim_breakdown = pd.DataFrame({
        'Claim Type': ['Injury', 'Property', 'Vehicle'],
        'Total Amount': [
            df['injury_claim'].sum(),
            df['property_claim'].sum(),
            df['vehicle_claim'].sum()
        ]
    })
    
    fig14 = px.bar(
        claim_breakdown,
        x='Claim Type',
        y='Total Amount',
        title="Total Claim Amount by Type",
        color='Claim Type',
        color_discrete_sequence=['#d62728', '#1f77b4', '#2ca02c']
    )
    fig14.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig14, use_container_width=True)

with col2:
    # Number of Vehicles Involved
    veh_counts = df['number_of_vehicles_involved'].value_counts().sort_index().reset_index()
    veh_counts.columns = ['Vehicles Involved', 'Claims']
    
    fig15 = px.bar(
        veh_counts,
        x='Vehicles Involved',
        y='Claims',
        title="Number of Vehicles Involved in Incident",
        color='Claims',
        color_continuous_scale='Magma'
    )
    fig15.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig15, use_container_width=True)

# ============= CHARTS ROW 8: OCCUPATION & LIFESTYLE =============
st.subheader("👔 Occupation & Lifestyle Insights")
col1, col2 = st.columns(2)

with col1:
    # Top 10 Occupations
    top_occ = df['insured_occupation'].value_counts().head(10).reset_index()
    top_occ.columns = ['Occupation', 'Claims']
    
    fig16 = px.bar(
        top_occ,
        x='Claims',
        y='Occupation',
        orientation='h',
        title="Top 10 Occupations (by Claims)",
        color='Claims',
        color_continuous_scale='Aggrnyl'
    )
    fig16.update_layout(showlegend=False, height=400, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig16, use_container_width=True)

with col2:
    # Top 10 Hobbies
    top_hobbies = df['insured_hobbies'].value_counts().head(10).reset_index()
    top_hobbies.columns = ['Hobby', 'Claims']
    
    fig17 = px.bar(
        top_hobbies,
        x='Claims',
        y='Hobby',
        orientation='h',
        title="Top 10 Hobbies (by Claims)",
        color='Claims',
        color_continuous_scale='Mint'
    )
    fig17.update_layout(showlegend=False, height=400, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig17, use_container_width=True)

# ============= FOOTER =============
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>"
    "Built by Manisha Samal | Data Analytics + AI"
    "</p>",
    unsafe_allow_html=True
)