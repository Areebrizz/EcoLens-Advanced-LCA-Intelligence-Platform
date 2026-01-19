# ============================================================================
# ECO LENS PRO - WORKING VERSION
# ============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

# Set page config FIRST - CRITICAL
st.set_page_config(
    page_title="EcoLens Pro | Advanced LCA Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state - SIMPLIFIED
if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.products = []
    st.session_state.current_workflow = None
    st.session_state.workflow_step = 0
    st.session_state.user_role = "engineer"
    st.session_state.view = "dashboard"

# SIMPLE CSS that works
st.markdown("""
<style>
    /* Basic styles that work */
    .main-title {
        font-size: 2.5rem;
        color: #1E40AF;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .sub-title {
        font-size: 1.2rem;
        color: #6B7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #BAE6FD;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E40AF;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6B7280;
        text-transform: uppercase;
    }
    
    .stButton > button {
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .primary-btn {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
        border: none;
    }
    
    /* Safe sidebar styling */
    .sidebar .sidebar-content {
        background: #F9FAFB;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIMPLE DATABASE (In-memory)
# ============================================================================

class SimpleDatabase:
    """Simple in-memory database for demonstration"""
    
    def __init__(self):
        self.materials = pd.DataFrame({
            'id': ['PP', 'PET', 'AL', 'STEEL', 'GLASS', 'BAMBOO', 'R_PET', 'R_PP'],
            'name': ['Polypropylene', 'PET', 'Aluminum', 'Steel', 'Glass', 'Bamboo', 'Recycled PET', 'Recycled PP'],
            'carbon_kgCO2e_per_kg': [2.1, 3.2, 8.2, 6.2, 1.4, 0.3, 1.5, 1.2],
            'energy_MJ_per_kg': [85.6, 84.2, 218.0, 56.7, 15.0, 2.5, 45.0, 50.0],
            'price_usd_per_kg': [1.8, 2.1, 3.2, 4.8, 1.2, 3.5, 2.0, 1.9],
            'recyclability': [0.85, 0.90, 0.95, 0.95, 1.00, 0.95, 0.95, 0.90]
        })
        
        self.processes = pd.DataFrame({
            'process': ['Injection Molding', 'Blow Molding', 'Thermoforming', 'Assembly'],
            'energy_kWh_per_kg': [1.2, 0.9, 0.8, 0.2],
            'carbon_kgCO2e_per_kg': [0.15, 0.12, 0.10, 0.03]
        })

# ============================================================================
# SIMPLE CALCULATOR
# ============================================================================

class SimpleLCAEngine:
    """Simple LCA calculator"""
    
    @staticmethod
    def calculate_quick_assessment(material_id, mass_kg, region="Global"):
        """Quick LCA calculation"""
        
        # Material impacts
        material_impacts = {
            'PP': {'carbon': 2.1, 'energy': 85.6},
            'PET': {'carbon': 3.2, 'energy': 84.2},
            'AL': {'carbon': 8.2, 'energy': 218.0},
            'STEEL': {'carbon': 6.2, 'energy': 56.7},
            'GLASS': {'carbon': 1.4, 'energy': 15.0}
        }
        
        # Regional factors
        region_factors = {
            'Asia': 1.2,
            'Europe': 0.9,
            'North America': 1.0,
            'Global': 1.1
        }
        
        # Get material data
        mat_data = material_impacts.get(material_id, {'carbon': 2.5, 'energy': 100})
        
        # Calculate
        carbon = mass_kg * mat_data['carbon'] * region_factors.get(region, 1.1)
        energy = mass_kg * mat_data['energy'] * 0.9
        
        # Add manufacturing (20% of material)
        carbon *= 1.2
        energy *= 1.2
        
        return {
            'carbon_kgCO2e': round(carbon, 2),
            'energy_MJ': round(energy, 1),
            'circularity': round(0.8 - (mat_data['carbon'] / 10), 2)
        }

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application"""
    
    # Initialize database and calculator
    db = SimpleDatabase()
    calculator = SimpleLCAEngine()
    
    # Sidebar navigation - SIMPLE
    with st.sidebar:
        st.markdown("## 🌍 EcoLens Pro")
        st.markdown("---")
        
        # Navigation
        view_options = {
            "🏠 Dashboard": "dashboard",
            "🚀 Quick Assessment": "quick",
            "🔬 Detailed Analysis": "detailed",
            "📊 Compare": "compare",
            "📈 Analytics": "analytics"
        }
        
        selected = st.radio(
            "Navigation",
            list(view_options.keys()),
            label_visibility="collapsed"
        )
        
        st.session_state.view = view_options[selected]
        
        st.markdown("---")
        
        # Quick stats
        st.markdown(f"**Analyses:** {len(st.session_state.products)}")
        
        if st.button("🆕 New Analysis"):
            st.session_state.view = "quick"
            st.session_state.workflow_step = 0
            st.rerun()
    
    # Main content area
    if st.session_state.view == "dashboard":
        show_dashboard(db)
    elif st.session_state.view == "quick":
        show_quick_assessment(db, calculator)
    elif st.session_state.view == "detailed":
        show_detailed_analysis()
    elif st.session_state.view == "compare":
        show_comparison()
    elif st.session_state.view == "analytics":
        show_analytics()

def show_dashboard(db):
    """Show main dashboard"""
    
    st.markdown('<h1 class="main-title">EcoLens Pro Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Advanced Life Cycle Assessment Platform</p>', unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Products Analyzed</div>
            <div class="metric-value">24</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Avg. Carbon</div>
            <div class="metric-value">2.4</div>
            <div style="font-size: 0.8rem; color: #6B7280;">kg CO₂e</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Circularity</div>
            <div class="metric-value">0.68</div>
            <div style="font-size: 0.8rem; color: #6B7280;">Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Improvement</div>
            <div class="metric-value">35%</div>
            <div style="font-size: 0.8rem; color: #6B7280;">Potential</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick start cards
    st.markdown("## 🚀 Quick Start")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.markdown("""
            <div class="card">
                <h3 style="color: #1E40AF;">Quick Assessment</h3>
                <p style="color: #6B7280;">Get instant LCA results for common products</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Start Quick Assessment", key="quick_btn", use_container_width=True):
                st.session_state.view = "quick"
                st.session_state.workflow_step = 0
                st.rerun()
    
    with col2:
        with st.container():
            st.markdown("""
            <div class="card">
                <h3 style="color: #1E40AF;">Compare Products</h3>
                <p style="color: #6B7280;">Side-by-side comparison of design alternatives</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Start Comparison", key="compare_btn", use_container_width=True):
                st.session_state.view = "compare"
                st.rerun()
    
    with col3:
        with st.container():
            st.markdown("""
            <div class="card">
                <h3 style="color: #1E40AF;">Advanced Analytics</h3>
                <p style="color: #6B7280;">Deep dive into analytics and trends</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("View Analytics", key="analytics_btn", use_container_width=True):
                st.session_state.view = "analytics"
                st.rerun()
    
    # Recent analyses
    if st.session_state.products:
        st.markdown("## 📋 Recent Analyses")
        
        for product in st.session_state.products[-3:]:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{product.get('name', 'Product')}**")
                    st.caption(f"Material: {product.get('material', 'Unknown')}")
                
                with col2:
                    st.metric("Carbon", f"{product.get('carbon', 0)} kg")
                
                with col3:
                    st.metric("Circularity", product.get('circularity', 0))
                
                st.divider()

def show_quick_assessment(db, calculator):
    """Show quick assessment workflow"""
    
    steps = ["Select Product", "Configure", "Results"]
    current_step = st.session_state.workflow_step
    
    # Progress indicator
    col1, col2, col3 = st.columns(3)
    for i, step in enumerate(steps):
        with [col1, col2, col3][i]:
            status = "🔵" if i == current_step else "✅" if i < current_step else "⚪"
            st.markdown(f"**{status} {step}**")
    
    st.divider()
    
    if current_step == 0:
        show_quick_step1(db)
    elif current_step == 1:
        show_quick_step2(db)
    elif current_step == 2:
        show_quick_step3(db, calculator)

def show_quick_step1(db):
    """Step 1: Product selection"""
    
    st.markdown("## 1. Select Your Product")
    
    product_type = st.selectbox(
        "Product Type",
        ["Water Bottle (500ml)", "Packaging Box", "Electronics Case", "Furniture Component"]
    )
    
    if product_type == "Water Bottle (500ml)":
        st.info("💡 Typical: 150g Polypropylene, Injection molding, 2-year lifespan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.view = "dashboard"
            st.rerun()
    
    with col2:
        if st.button("Next →", type="primary", use_container_width=True):
            st.session_state.workflow_step = 1
            st.session_state.product_type = product_type
            st.rerun()

def show_quick_step2(db):
    """Step 2: Configuration"""
    
    st.markdown("## 2. Configure Your Product")
    
    with st.form("config_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            material = st.selectbox(
                "Primary Material",
                db.materials['name'].tolist()
            )
            
            mass_kg = st.number_input(
                "Product Mass (kg)",
                0.01, 10.0, 0.15, 0.01
            )
        
        with col2:
            region = st.selectbox(
                "Manufacturing Region",
                ["Asia", "Europe", "North America", "Global"]
            )
            
            lifetime = st.slider(
                "Lifetime (years)",
                1, 10, 2
            )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.form_submit_button("← Back", use_container_width=True):
                st.session_state.workflow_step = 0
                st.rerun()
        
        with col3:
            if st.form_submit_button("Run Analysis →", type="primary", use_container_width=True):
                st.session_state.workflow_step = 2
                st.session_state.config = {
                    'material': material,
                    'material_id': db.materials[db.materials['name'] == material]['id'].iloc[0],
                    'mass_kg': mass_kg,
                    'region': region,
                    'lifetime': lifetime
                }
                st.rerun()

def show_quick_step3(db, calculator):
    """Step 3: Results"""
    
    st.markdown("## 3. Analysis Results")
    
    # Get configuration
    config = st.session_state.get('config', {})
    product_type = st.session_state.get('product_type', 'Product')
    
    # Calculate results
    with st.spinner("🔄 Calculating environmental impacts..."):
        time.sleep(1)  # Simulate calculation
        
        results = calculator.calculate_quick_assessment(
            config.get('material_id', 'PP'),
            config.get('mass_kg', 0.15),
            config.get('region', 'Global')
        )
    
    st.success("✅ Analysis complete!")
    
    # Display results
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Carbon Footprint",
            f"{results['carbon_kgCO2e']} kg",
            "CO₂e"
        )
    
    with col2:
        st.metric(
            "Energy Use",
            f"{results['energy_MJ']} MJ"
        )
    
    with col3:
        st.metric(
            "Circularity Score",
            f"{results['circularity']}"
        )
    
    # Visualization
    st.markdown("### 📊 Impact Breakdown")
    
    fig = go.Figure(data=[
        go.Bar(name='Material', x=['Carbon', 'Energy'], y=[
            results['carbon_kgCO2e'] * 0.6, 
            results['energy_MJ'] * 0.6
        ]),
        go.Bar(name='Manufacturing', x=['Carbon', 'Energy'], y=[
            results['carbon_kgCO2e'] * 0.3, 
            results['energy_MJ'] * 0.3
        ]),
        go.Bar(name='Transport', x=['Carbon', 'Energy'], y=[
            results['carbon_kgCO2e'] * 0.1, 
            results['energy_MJ'] * 0.1
        ])
    ])
    
    fig.update_layout(barmode='stack', height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.markdown("### 💡 Recommendations")
    
    recommendations = [
        "Switch to recycled material for 30% carbon reduction",
        "Optimize transport logistics for 20% reduction",
        "Design for longer lifespan (5+ years recommended)"
    ]
    
    for i, rec in enumerate(recommendations):
        st.info(f"{i+1}. {rec}")
    
    # Next steps
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 New Analysis", use_container_width=True):
            st.session_state.workflow_step = 0
            # Save this analysis
            st.session_state.products.append({
                'name': product_type,
                'material': config.get('material', 'Unknown'),
                'carbon': results['carbon_kgCO2e'],
                'energy': results['energy_MJ'],
                'circularity': results['circularity'],
                'date': datetime.now().strftime('%Y-%m-%d')
            })
            st.rerun()
    
    with col2:
        if st.button("📊 Compare", use_container_width=True):
            st.session_state.view = "compare"
            st.rerun()
    
    with col3:
        if st.button("🏠 Dashboard", type="primary", use_container_width=True):
            st.session_state.view = "dashboard"
            st.rerun()

def show_detailed_analysis():
    """Show detailed analysis view"""
    st.title("🔬 Detailed Analysis")
    st.info("Advanced analysis with full customization")
    
    with st.expander("📦 Materials", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Material 1", ["PP", "PET", "Aluminum", "Steel"])
            st.number_input("Mass (kg)", 0.01, 10.0, 0.15)
        
        with col2:
            st.slider("Recycled Content", 0.0, 1.0, 0.0, 0.05)
            st.number_input("Cost (USD/kg)", 0.0, 100.0, 2.0)
    
    with st.expander("🏭 Manufacturing"):
        st.multiselect("Processes", ["Injection Molding", "Assembly", "Finishing"])
        st.selectbox("Region", ["Asia", "Europe", "North America"])
    
    if st.button("Run Detailed Analysis", type="primary"):
        st.success("Analysis started!")

def show_comparison():
    """Show comparison view"""
    st.title("📊 Compare Products")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Product A")
        material_a = st.selectbox("Material A", ["PP", "PET", "Aluminum"], key="mat_a")
        mass_a = st.number_input("Mass A (kg)", 0.01, 10.0, 0.15, key="mass_a")
    
    with col2:
        st.markdown("### Product B")
        material_b = st.selectbox("Material B", ["PP", "PET", "Aluminum"], key="mat_b")
        mass_b = st.number_input("Mass B (kg)", 0.01, 10.0, 0.15, key="mass_b")
    
    if st.button("Compare", type="primary"):
        # Simple comparison
        carbon_a = mass_a * 2.1 if material_a == "PP" else mass_a * 3.2
        carbon_b = mass_b * 2.1 if material_b == "PP" else mass_b * 3.2
        
        # Display comparison
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Product A Carbon", f"{carbon_a:.2f} kg", 
                     delta=f"{((carbon_a - carbon_b)/carbon_b*100 if carbon_b > 0 else 0):.1f}%")
        
        with col2:
            st.metric("Product B Carbon", f"{carbon_b:.2f} kg")
        
        with col3:
            reduction = ((carbon_a - carbon_b) / carbon_a * 100) if carbon_a > 0 else 0
            st.metric("Reduction", f"{abs(reduction):.1f}%", 
                     delta="Better" if carbon_b < carbon_a else "Worse")

def show_analytics():
    """Show analytics view"""
    st.title("📈 Analytics Dashboard")
    
    # Sample data
    data = pd.DataFrame({
        'Product': ['Bottle A', 'Bottle B', 'Box A', 'Box B', 'Case A'],
        'Carbon (kg)': [2.4, 1.8, 1.2, 0.9, 3.2],
        'Energy (MJ)': [85, 65, 45, 35, 115],
        'Circularity': [0.72, 0.85, 0.65, 0.78, 0.58]
    })
    
    # Charts
    tab1, tab2, tab3 = st.tabs(["Carbon Analysis", "Trends", "Correlations"])
    
    with tab1:
        fig = px.bar(data, x='Product', y='Carbon (kg)', 
                     title='Carbon Footprint by Product')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = px.line(data, x='Product', y=['Carbon (kg)', 'Energy (MJ)'],
                      title='Environmental Impact Trends')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        corr_matrix = data[['Carbon (kg)', 'Energy (MJ)', 'Circularity']].corr()
        fig = px.imshow(corr_matrix, text_auto=True, 
                        title='Correlation Matrix')
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# RUN THE APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
