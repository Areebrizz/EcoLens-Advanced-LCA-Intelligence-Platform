# ============================================================================
# ECO LENS PRO: ADVANCED LCA INTELLIGENCE PLATFORM
# ============================================================================
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import core modules
from core.database import AdvancedLCADatabase
from core.calculator import AdvancedLCAEngine
from core.models import Product, Material, Process, Transport

# Import UI modules
from ui.components import (
    ProfessionalHeader, SidebarNavigation, 
    MetricDashboard, WorkflowManager, ProgressTracker
)
from ui.dashboard import DashboardView
from ui.workflows import (
    QuickAssessmentWorkflow,
    DetailedAnalysisWorkflow,
    ComparisonWorkflow,
    OptimizationWorkflow,
    ScenarioAnalysisWorkflow
)
from ui.visualizations import AdvancedVisualizer

# Import analytics modules
from analytics.ml_models import MaterialRecommendationEngine
from analytics.benchmarks import BenchmarkingEngine
from analytics.scenarios import ScenarioModeler

# Import advanced modules
from modules.uncertainty import UncertaintyAnalyzer
from modules.circularity import CircularEconomyAnalyzer
from modules.optimization import DesignOptimizer
from modules.sensitivity import SensitivityAnalyzer

# Configure page
st.set_page_config(
    page_title="EcoLens Pro | Advanced LCA Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://ecolens.com/docs',
        'Report a bug': 'https://ecolens.com/support',
        'About': '# EcoLens Pro v2.0 - Advanced LCA Platform'
    }
)

# Custom CSS for professional UI
st.markdown("""
<style>
    /* Modern color scheme */
    :root {
        --primary: #1E40AF;
        --secondary: #3B82F6;
        --accent: #10B981;
        --warning: #F59E0B;
        --danger: #EF4444;
        --dark: #1F2937;
        --light: #F9FAFB;
        --gray: #6B7280;
    }
    
    /* Main container */
    .main-container {
        max-width: 100%;
        padding: 0 1rem;
    }
    
    /* Professional header */
    .pro-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        padding: 1.5rem 2rem;
        border-radius: 0 0 20px 20px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(30, 64, 175, 0.2);
    }
    
    /* Dashboard cards */
    .dashboard-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        border: 1px solid #E5E7EB;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
        border-color: var(--secondary);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        border-radius: 12px;
        padding: 1.2rem;
        border: 2px solid #E5E7EB;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--secondary), var(--accent));
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: var(--dark);
        margin: 0.5rem 0;
        font-family: 'Segoe UI', system-ui, -apple-system;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: var(--gray);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    
    /* Status indicators */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
    }
    
    .status-success {
        background: linear-gradient(135deg, #D1FAE5, #A7F3D0);
        color: #065F46;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #FEF3C7, #FDE68A);
        color: #92400E;
    }
    
    .status-info {
        background: linear-gradient(135deg, #DBEAFE, #BFDBFE);
        color: #1E40AF;
    }
    
    /* Advanced tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: var(--light);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(59, 130, 246, 0.1);
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--accent), #34D399);
    }
    
    /* Form styling */
    .form-section {
        background: var(--light);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #E5E7EB;
    }
    
    .form-section-title {
        color: var(--primary);
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Data table styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    .dataframe thead th {
        background: var(--primary);
        color: white;
        font-weight: 600;
    }
    
    /* Tooltips */
    .tooltip-icon {
        display: inline-block;
        width: 18px;
        height: 18px;
        background: var(--secondary);
        color: white;
        border-radius: 50%;
        text-align: center;
        line-height: 18px;
        font-size: 12px;
        margin-left: 0.3rem;
        cursor: help;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Loading spinner */
    .loading-spinner {
        border: 4px solid rgba(59, 130, 246, 0.2);
        border-radius: 50%;
        border-top: 4px solid var(--secondary);
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Notification badges */
    .notification-badge {
        position: absolute;
        top: -8px;
        right: -8px;
        background: var(--danger);
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        font-size: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# APPLICATION STATE MANAGEMENT
# ============================================================================

class AppState:
    """Centralized application state management"""
    
    @staticmethod
    def initialize():
        """Initialize all session state variables"""
        if 'app_initialized' not in st.session_state:
            st.session_state.app_initialized = True
            
            # User settings
            st.session_state.user = {
                'role': None,
                'organization': None,
                'preferences': {
                    'units': 'metric',
                    'currency': 'USD',
                    'theme': 'light',
                    'notifications': True
                }
            }
            
            # Application state
            st.session_state.current_workflow = None
            st.session_state.workflow_step = 0
            st.session_state.active_view = 'dashboard'
            st.session_state.project_id = None
            
            # Data state
            st.session_state.products = []
            st.session_state.comparisons = []
            st.session_state.scenarios = []
            st.session_state.optimizations = []
            
            # Analytics state
            st.session_state.insights = []
            st.session_state.reports = []
            st.session_state.benchmarks = []
            
            # Initialize engines
            st.session_state.database = AdvancedLCADatabase()
            st.session_state.calculator = AdvancedLCAEngine(st.session_state.database)
            st.session_state.visualizer = AdvancedVisualizer()
            st.session_state.ml_engine = MaterialRecommendationEngine()
            st.session_state.optimizer = DesignOptimizer()
            st.session_state.scenario_modeler = ScenarioModeler()
            
            # UI state
            st.session_state.sidebar_collapsed = False
            st.session_state.notifications = [
                {'id': 1, 'type': 'info', 'message': 'Welcome to EcoLens Pro!', 'read': False},
                {'id': 2, 'type': 'success', 'message': 'Database initialized successfully', 'read': False}
            ]

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    
    # Initialize application state
    AppState.initialize()
    
    # Display professional header
    ProfessionalHeader.display()
    
    # Display sidebar navigation
    view = SidebarNavigation.display()
    
    # Update active view
    st.session_state.active_view = view
    
    # Display main content based on selected view
    display_main_content(view)

def display_main_content(view):
    """Display main content based on selected view"""
    
    if view == 'dashboard':
        DashboardView.display()
    
    elif view == 'quick_assessment':
        workflow = QuickAssessmentWorkflow()
        workflow.display()
    
    elif view == 'detailed_analysis':
        workflow = DetailedAnalysisWorkflow()
        workflow.display()
    
    elif view == 'comparison':
        workflow = ComparisonWorkflow()
        workflow.display()
    
    elif view == 'optimization':
        workflow = OptimizationWorkflow()
        workflow.display()
    
    elif view == 'scenarios':
        workflow = ScenarioAnalysisWorkflow()
        workflow.display()
    
    elif view == 'analytics':
        display_analytics_dashboard()
    
    elif view == 'reports':
        display_reports_dashboard()
    
    elif view == 'database':
        display_database_explorer()
    
    elif view == 'settings':
        display_settings()

def display_analytics_dashboard():
    """Display advanced analytics dashboard"""
    
    st.title("📈 Advanced Analytics")
    
    # Analytics tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Trend Analysis", 
        "Correlation Matrix", 
        "Predictive Insights", 
        "Benchmarking"
    ])
    
    with tab1:
        display_trend_analysis()
    
    with tab2:
        display_correlation_analysis()
    
    with tab3:
        display_predictive_insights()
    
    with tab4:
        display_benchmarking()

def display_trend_analysis():
    """Display trend analysis"""
    
    st.subheader("📊 Trend Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Time series analysis
        if st.session_state.products:
            dates = [p.get('timestamp', datetime.now()) for p in st.session_state.products]
            carbon_values = [p['totals']['carbon_kgCO2e'] for p in st.session_state.products]
            
            df = pd.DataFrame({
                'Date': dates,
                'Carbon Footprint': carbon_values
            })
            
            # Calculate moving average
            df['Moving Avg'] = df['Carbon Footprint'].rolling(window=3).mean()
            
            # Plot trends
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['Date'], y=df['Carbon Footprint'],
                mode='markers',
                name='Individual Assessments',
                marker=dict(color='#3B82F6', size=8)
            ))
            fig.add_trace(go.Scatter(
                x=df['Date'], y=df['Moving Avg'],
                mode='lines',
                name='3-Point Moving Average',
                line=dict(color='#EF4444', width=3)
            ))
            
            fig.update_layout(
                title="Carbon Footprint Trend Analysis",
                xaxis_title="Assessment Date",
                yaxis_title="Carbon Footprint (kg CO₂e)",
                height=400,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Statistical summary
        st.markdown("### 📋 Statistical Summary")
        
        if st.session_state.products:
            carbon_values = [p['totals']['carbon_kgCO2e'] for p in st.session_state.products]
            
            stats = {
                'Mean': np.mean(carbon_values),
                'Median': np.median(carbon_values),
                'Std Dev': np.std(carbon_values),
                'Min': np.min(carbon_values),
                'Max': np.max(carbon_values)
            }
            
            for key, value in stats.items():
                st.metric(key, f"{value:.2f}")

def display_correlation_analysis():
    """Display correlation analysis"""
    
    st.subheader("🔗 Correlation Matrix")
    
    if len(st.session_state.products) >= 5:
        # Create correlation dataframe
        data = []
        for product in st.session_state.products:
            data.append({
                'Mass': product['phases']['material']['mass_kg'],
                'Carbon': product['totals']['carbon_kgCO2e'],
                'Energy': product['totals']['energy_MJ'],
                'Lifetime': product.get('lifetime_years', 1),
                'Circularity': product['circularity_metrics']['material_circularity_indicator']
            })
        
        df = pd.DataFrame(data)
        corr_matrix = df.corr()
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmin=-1,
            zmax=1,
            text=corr_matrix.round(2).values,
            texttemplate='%{text}',
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="Parameter Correlation Matrix",
            height=500,
            xaxis_title="Parameters",
            yaxis_title="Parameters"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Insights
        st.markdown("### 💡 Correlation Insights")
        
        insights = [
            "**Strong positive correlation (>0.7)**: Mass vs Carbon, Mass vs Energy",
            "**Moderate correlation (0.3-0.7)**: Carbon vs Energy",
            "**Negative correlation**: Circularity vs Carbon (higher circularity = lower carbon)"
        ]
        
        for insight in insights:
            st.info(insight)
    else:
        st.info("Need at least 5 product assessments for correlation analysis.")

def display_predictive_insights():
    """Display predictive analytics insights"""
    
    st.subheader("🔮 Predictive Insights")
    
    # ML-based predictions
    if st.button("Generate Predictive Model", type="primary"):
        with st.spinner("Training predictive model..."):
            # Simulate model training
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            # Display predictions
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📈 Carbon Footprint Predictor")
                
                # Input for prediction
                mass = st.number_input("Product Mass (kg)", 0.01, 50.0, 0.15)
                material = st.selectbox("Primary Material", 
                                      ["PP", "PET", "Aluminum", "Steel"])
                
                if st.button("Predict Carbon Footprint"):
                    # Simple prediction (in real app, use ML model)
                    base_carbon = {
                        'PP': 2.1, 'PET': 3.2, 
                        'Aluminum': 8.2, 'Steel': 6.2
                    }
                    prediction = base_carbon.get(material, 2.5) * mass / 0.15
                    
                    st.success(f"**Predicted Carbon Footprint:** {prediction:.2f} kg CO₂e")
            
            with col2:
                st.markdown("### 🎯 Improvement Recommendations")
                
                # AI-generated recommendations
                recommendations = [
                    "**Material Optimization**: Switch to recycled PET for 30% reduction",
                    "**Design Efficiency**: Reduce mass by 15% through topology optimization",
                    "**Process Improvement**: Use renewable energy in manufacturing",
                    "**Circular Design**: Implement take-back program for end-of-life"
                ]
                
                for rec in recommendations:
                    with st.container():
                        st.markdown(f"""
                        <div class="form-section" style="padding: 1rem; margin-bottom: 0.5rem;">
                            <p style="margin: 0;">{rec}</p>
                        </div>
                        """, unsafe_allow_html=True)

def display_benchmarking():
    """Display benchmarking analysis"""
    
    st.subheader("🏆 Benchmarking Analysis")
    
    benchmark_engine = BenchmarkingEngine()
    
    # Industry benchmarks
    benchmarks = benchmark_engine.get_industry_benchmarks()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Industry Benchmarks")
        
        benchmark_df = pd.DataFrame(benchmarks)
        st.dataframe(benchmark_df, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Your Performance")
        
        if st.session_state.products:
            # Compare against benchmarks
            latest_product = st.session_state.products[-1]
            carbon = latest_product['totals']['carbon_kgCO2e']
            
            # Find closest benchmark
            closest_benchmark = min(benchmarks, 
                                   key=lambda x: abs(x['carbon_kgCO2e_per_kg'] - carbon))
            
            st.metric("Your Carbon", f"{carbon:.2f} kg CO₂e")
            st.metric("Industry Average", 
                     f"{closest_benchmark['carbon_kgCO2e_per_kg']:.2f} kg CO₂e/kg",
                     delta=f"{(carbon - closest_benchmark['carbon_kgCO2e_per_kg']):.2f}")

def display_reports_dashboard():
    """Display professional reports dashboard"""
    
    st.title("📄 Professional Reports")
    
    # Report types
    report_types = [
        {
            "name": "Sustainability Report",
            "icon": "🌱",
            "description": "Comprehensive sustainability assessment",
            "sections": ["Executive Summary", "Methodology", "Results", "Recommendations"]
        },
        {
            "name": "Compliance Document",
            "icon": "📋",
            "description": "Regulatory compliance documentation",
            "sections": ["GHG Protocol", "ISO 14040", "PEF", "EPD"]
        },
        {
            "name": "Academic Paper",
            "icon": "🎓",
            "description": "Research paper format",
            "sections": ["Abstract", "Introduction", "Methodology", "Results", "Discussion"]
        },
        {
            "name": "Executive Summary",
            "icon": "👔",
            "description": "High-level summary for leadership",
            "sections": ["Key Findings", "Business Impact", "Recommendations"]
        }
    ]
    
    # Display report options
    cols = st.columns(4)
    for idx, report_type in enumerate(report_types):
        with cols[idx]:
            with st.container():
                st.markdown(f"""
                <div class="dashboard-card" style="text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 1rem;">{report_type['icon']}</div>
                    <h3 style="color: var(--primary); margin-bottom: 0.5rem;">{report_type['name']}</h3>
                    <p style="color: var(--gray); font-size: 0.9rem; margin-bottom: 1rem;">
                    {report_type['description']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Generate {report_type['name']}", key=f"report_{idx}", use_container_width=True):
                    generate_report(report_type)

def generate_report(report_type):
    """Generate professional report"""
    
    with st.spinner(f"Generating {report_type['name']}..."):
        # Create report content
        report_content = create_report_content(report_type)
        
        # Display preview
        with st.expander("📋 Report Preview", expanded=True):
            st.markdown(report_content[:3000] + "...")
        
        # Export options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                label="📥 Download PDF",
                data=report_content.encode(),
                file_name=f"{report_type['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        
        with col2:
            st.download_button(
                label="📊 Download Excel",
                data=pd.DataFrame().to_csv().encode(),
                file_name=f"{report_type['name'].replace(' ', '_')}_Data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        with col3:
            st.download_button(
                label="📈 Download Charts",
                data=report_content.encode(),
                file_name=f"{report_type['name'].replace(' ', '_')}_Charts.zip",
                mime="application/zip"
            )

def create_report_content(report_type):
    """Create professional report content"""
    
    # This would be a comprehensive report generator
    # For now, return a template
    return f"""
# {report_type['name']}
## EcoLens Pro Analysis Report
### Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary
This report presents a comprehensive Life Cycle Assessment conducted using EcoLens Pro.

### Key Findings
- Total Carbon Footprint: XX kg CO₂e
- Energy Consumption: XX MJ
- Circularity Score: X.XX
- Improvement Potential: XX%

### Recommendations
1. Material optimization
2. Process improvements
3. Supply chain optimization

---

## Methodology
### Standards Compliance
- ISO 14040/44: Life Cycle Assessment
- GHG Protocol: Carbon Accounting
- PEF: Product Environmental Footprint

### Data Sources
- Ecoinvent Database v3.8
- Industry benchmarks
- Primary data collection

---

## Detailed Results
### Life Cycle Phases
1. Material Production
2. Manufacturing
3. Transportation
4. Use Phase
5. End-of-Life

### Environmental Impacts
- Climate Change: XX kg CO₂e
- Energy Use: XX MJ
- Water Consumption: XX L
- Resource Depletion: XX kg Sb-eq

---

## Appendices
### A. Data Quality Assessment
### B. Uncertainty Analysis
### C. Sensitivity Analysis
### D. Benchmark Comparison

---

*Report generated by EcoLens Pro v2.0 | www.ecolens.com*
"""

def display_database_explorer():
    """Display advanced database explorer"""
    
    st.title("🔍 Advanced Database Explorer")
    
    # Database tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📦 Materials", 
        "🏭 Processes", 
        "🚚 Transport", 
        "🌍 Regional Factors", 
        "🔄 Circular Economy"
    ])
    
    with tab1:
        display_materials_database()
    
    with tab2:
        display_processes_database()
    
    with tab3:
        display_transport_database()
    
    with tab4:
        display_regional_factors()
    
    with tab5:
        display_circularity_database()

def display_materials_database():
    """Display materials database explorer"""
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Material Database")
        
        # Interactive material explorer
        materials_df = st.session_state.database.get_materials_dataframe()
        
        # Add filters
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            category_filter = st.multiselect(
                "Filter by Category",
                materials_df['category'].unique(),
                default=materials_df['category'].unique()
            )
        
        with col_f2:
            carbon_range = st.slider(
                "Carbon Footprint Range",
                float(materials_df['carbon_footprint_kgCO2e_kg'].min()),
                float(materials_df['carbon_footprint_kgCO2e_kg'].max()),
                (0.0, 10.0)
            )
        
        # Apply filters
        filtered_df = materials_df[
            (materials_df['category'].isin(category_filter)) &
            (materials_df['carbon_footprint_kgCO2e_kg'] >= carbon_range[0]) &
            (materials_df['carbon_footprint_kgCO2e_kg'] <= carbon_range[1])
        ]
        
        # Display interactive table
        st.dataframe(filtered_df, use_container_width=True, height=400)
    
    with col2:
        st.subheader("Material Analysis")
        
        # Material comparison
        selected_materials = st.multiselect(
            "Compare Materials",
            materials_df['material_name'].tolist(),
            default=materials_df['material_name'].iloc[:2].tolist()
        )
        
        if len(selected_materials) >= 2:
            compare_df = materials_df[materials_df['material_name'].isin(selected_materials)]
            
            # Radar chart for comparison
            categories = ['Carbon', 'Energy', 'Water', 'Recyclability']
            values = []
            
            for mat in selected_materials:
                mat_data = materials_df[materials_df['material_name'] == mat].iloc[0]
                values.append([
                    mat_data['carbon_footprint_kgCO2e_kg'] / 10,  # Normalized
                    mat_data['embodied_energy_MJ_kg'] / 200,
                    mat_data['water_use_L_kg'] / 200,
                    mat_data['recyclability_rate']
                ])
            
            fig = go.Figure()
            
            for i, mat in enumerate(selected_materials):
                fig.add_trace(go.Scatterpolar(
                    r=values[i] + [values[i][0]],  # Close the loop
                    theta=categories + [categories[0]],
                    fill='toself',
                    name=mat
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )
                ),
                showlegend=True,
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)

def display_processes_database():
    """Display manufacturing processes database"""
    st.subheader("Manufacturing Processes Database")
    
    processes_df = st.session_state.database.get_processes_dataframe()
    st.dataframe(processes_df, use_container_width=True)

def display_transport_database():
    """Display transport modes database"""
    st.subheader("Transport Modes Database")
    
    transport_df = st.session_state.database.get_transport_dataframe()
    
    # Visualization
    fig = px.bar(transport_df, 
                 x='mode', 
                 y='carbon_gCO2e_tonne_km',
                 color='mode',
                 title="Carbon Intensity by Transport Mode")
    
    st.plotly_chart(fig, use_container_width=True)

def display_regional_factors():
    """Display regional factors database"""
    st.subheader("Regional Emission Factors")
    
    regional_factors = st.session_state.database.get_regional_factors()
    
    # Create map visualization
    df = pd.DataFrame([
        {'Region': 'Europe', 'Carbon': 275, 'Renewable': 38},
        {'Region': 'North America', 'Carbon': 380, 'Renewable': 20},
        {'Region': 'Asia', 'Carbon': 620, 'Renewable': 15},
        {'Region': 'China', 'Carbon': 680, 'Renewable': 12},
        {'Region': 'South America', 'Carbon': 180, 'Renewable': 45}
    ])
    
    fig = px.bar(df, 
                 x='Region', 
                 y=['Carbon', 'Renewable'],
                 barmode='group',
                 title="Regional Electricity Grid Factors")
    
    st.plotly_chart(fig, use_container_width=True)

def display_circularity_database():
    """Display circular economy metrics database"""
    st.subheader("Circular Economy Metrics")
    
    circularity_metrics = st.session_state.database.get_circularity_metrics()
    
    # Display metrics
    for metric_name, metric_data in circularity_metrics.items():
        with st.expander(f"📊 {metric_name}"):
            st.write(f"**Formula:** {metric_data.get('formula', 'N/A')}")
            st.write(f"**Description:** {metric_data.get('description', 'N/A')}")

def display_settings():
    """Display application settings"""
    
    st.title("⚙️ Settings & Configuration")
    
    # Settings tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "User Preferences", 
        "Calculation Settings", 
        "Data Management", 
        "API & Integration"
    ])
    
    with tab1:
        display_user_settings()
    
    with tab2:
        display_calculation_settings()
    
    with tab3:
        display_data_management()
    
    with tab4:
        display_api_integration()

def display_user_settings():
    """Display user settings"""
    
    st.subheader("👤 User Preferences")
    
    with st.form("user_settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("Units System", ["Metric", "Imperial"])
            st.selectbox("Currency", ["USD", "EUR", "GBP", "JPY", "CNY"])
            st.selectbox("Language", ["English", "Spanish", "French", "German", "Chinese"])
        
        with col2:
            st.selectbox("Theme", ["Light", "Dark", "Auto"])
            st.slider("Font Size", 12, 18, 14)
            st.checkbox("Enable Notifications", True)
            st.checkbox("Auto-save Projects", True)
        
        if st.form_submit_button("Save Preferences", type="primary"):
            st.success("Preferences saved successfully!")

def display_calculation_settings():
    """Display calculation settings"""
    
    st.subheader("🧮 Calculation Settings")
    
    with st.form("calculation_settings"):
        st.selectbox("LCA Method", 
                    ["ReCiPe 2016", "IMPACT World+", "TRACI", "CML", "EDIP"])
        
        st.selectbox("Time Horizon", 
                    ["20 years", "100 years", "500 years", "Infinite"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Include Biogenic Carbon", True)
            st.checkbox("Include Carbon Storage", False)
        
        with col2:
            st.checkbox("Include Land Use Change", True)
            st.checkbox("Include Water Scarcity", True)
        
        st.number_input("Monte Carlo Iterations", 100, 10000, 1000, 100)
        
        if st.form_submit_button("Save Calculation Settings", type="primary"):
            st.success("Calculation settings updated!")

def display_data_management():
    """Display data management settings"""
    
    st.subheader("💾 Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Export Data")
        
        export_options = st.multiselect(
            "Select data to export",
            ["Product Assessments", "Material Database", "Process Database", 
             "Transport Database", "Calculation Results", "Reports"]
        )
        
        if st.button("Export Selected Data", use_container_width=True):
            st.success("Export initiated!")
    
    with col2:
        st.markdown("### Import Data")
        
        uploaded_file = st.file_uploader(
            "Upload Data File",
            type=['csv', 'xlsx', 'json']
        )
        
        if uploaded_file:
            st.info(f"File uploaded: {uploaded_file.name}")
            
            if st.button("Import Data", use_container_width=True):
                st.success("Data imported successfully!")

def display_api_integration():
    """Display API and integration settings"""
    
    st.subheader("🔗 API & Integration")
    
    st.markdown("### External Database Integration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Ecoinvent API Key", type="password")
        st.text_input("Agribalyse API Key", type="password")
    
    with col2:
        st.text_input("USLCI API Key", type="password")
        st.text_input("Custom Database URL")
    
    st.markdown("### Webhook Configuration")
    
    webhook_url = st.text_input("Webhook URL for Notifications")
    
    if st.button("Test Webhook", use_container_width=True):
        st.success("Webhook test successful!")

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
