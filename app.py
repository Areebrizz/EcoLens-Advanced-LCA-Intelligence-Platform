# ============================================================================
# ECO LENS: STREAMLIT-NATIVE ONBOARDING FLOW
# ============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
from datetime import datetime
import json

# Set page config FIRST
st.set_page_config(
    page_title="EcoLens: LCA Intelligence Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Simplified and working
st.markdown("""
<style>
    /* Main headers */
    .main-header {
        font-size: 3rem;
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Cards */
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .primary-btn {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
        border: none;
    }
    
    .primary-btn:hover {
        background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
    }
    
    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #BAE6FD;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Steps */
    .step-container {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
        gap: 2rem;
    }
    
    .step {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .step-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .step-active {
        background: #3B82F6;
        color: white;
    }
    
    .step-inactive {
        background: #E5E7EB;
        color: #6B7280;
    }
    
    .step-completed {
        background: #10B981;
        color: white;
    }
    
    /* Welcome hero */
    .welcome-hero {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
        border-radius: 20px;
        margin-bottom: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

# Initialize ALL session state variables
if 'app_initialized' not in st.session_state:
    st.session_state.app_initialized = True
    
    # Onboarding state
    st.session_state.onboarding_complete = False
    st.session_state.show_onboarding = True
    st.session_state.onboarding_step = 0
    
    # User preferences
    st.session_state.user_role = None
    st.session_state.interface_mode = "guided"  # guided or professional
    
    # Workflow state
    st.session_state.current_workflow = None
    st.session_state.workflow_step = 0
    
    # Analysis state
    st.session_state.products = []
    st.session_state.current_product = None
    
    # Demo data
    st.session_state.demo_products = [
        {
            'name': 'Water Bottle 500ml',
            'carbon': 2.4,
            'energy': 85,
            'circularity': 0.72,
            'date': '2024-01-20'
        },
        {
            'name': 'Packaging Box',
            'carbon': 1.8,
            'energy': 65,
            'circularity': 0.65,
            'date': '2024-01-19'
        }
    ]

# ============================================================================
# SIMPLIFIED LCA ENGINE (For demo)
# ============================================================================

class SimpleLCAEngine:
    """Simplified LCA engine for demonstration"""
    
    @staticmethod
    def calculate_quick_assessment(product_type, mass_kg, material, region):
        """Quick assessment calculation"""
        # Base values
        base_carbon = {
            'Water Bottle': 2.4,
            'Packaging': 1.8,
            'Electronics Case': 3.2,
            'Custom': 2.0
        }
        
        # Material factors
        material_factors = {
            'Polypropylene (PP)': 1.0,
            'Polyethylene Terephthalate (PET)': 1.3,
            'Aluminum': 2.5,
            'Stainless Steel': 3.0,
            'Bamboo Composite': 0.7
        }
        
        # Region factors
        region_factors = {
            'Asia (China)': 1.2,
            'Europe': 0.9,
            'North America': 1.0,
            'Global Average': 1.1
        }
        
        # Calculate
        base = base_carbon.get(product_type, 2.0)
        mat_factor = material_factors.get(material, 1.0)
        reg_factor = region_factors.get(region, 1.0)
        mass_factor = mass_kg / 0.15  # Normalize to 150g
        
        carbon = base * mat_factor * reg_factor * mass_factor
        energy = carbon * 35  # Approximate conversion
        circularity = 0.8 - (mat_factor - 1) * 0.1  # Better materials = better circularity
        
        return {
            'carbon_kg': round(carbon, 2),
            'energy_mj': round(energy, 1),
            'circularity_score': round(circularity, 2),
            'circularity_class': 'Highly Circular' if circularity > 0.7 else 'Moderately Circular' if circularity > 0.5 else 'Transitional'
        }

# ============================================================================
# ONBOARDING COMPONENTS
# ============================================================================

def show_onboarding():
    """Show step-by-step onboarding"""
    
    steps = [
        "Welcome",
        "Choose Role", 
        "Select Mode",
        "Get Started"
    ]
    
    # Step indicator
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]
    
    for i, step in enumerate(steps):
        with cols[i]:
            circle_class = "step-completed" if i < st.session_state.onboarding_step else "step-active" if i == st.session_state.onboarding_step else "step-inactive"
            st.markdown(f"""
            <div class="step">
                <div class="step-circle {circle_class}">{i+1}</div>
                <div style="font-size: 0.9rem; color: {'#3B82F6' if i == st.session_state.onboarding_step else '#6B7280'}">
                    {step}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Step content
    if st.session_state.onboarding_step == 0:
        show_welcome_step()
    elif st.session_state.onboarding_step == 1:
        show_role_selection()
    elif st.session_state.onboarding_step == 2:
        show_mode_selection()
    elif st.session_state.onboarding_step == 3:
        show_get_started()

def show_welcome_step():
    """Show welcome step"""
    st.markdown('<h1 class="main-header">🌍 Welcome to EcoLens</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style="padding: 2rem 0;">
            <h2 style="color: #1E3A8A;">Professional LCA Made Simple</h2>
            <p style="font-size: 1.1rem; color: #4B5563; line-height: 1.6;">
                Transform complex environmental analysis into actionable engineering insights 
                with our ISO-compliant Life Cycle Assessment platform.
            </p>
            <p style="font-size: 1rem; color: #6B7280;">
                <strong>Perfect for:</strong> Sustainability Managers • Product Engineers • Researchers
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Simple image or icon
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <div style="font-size: 4rem; color: #3B82F6;">📊</div>
            <p style="color: #6B7280;">ISO 14040/44 Compliant</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Skip Onboarding", use_container_width=True):
            st.session_state.onboarding_complete = True
            st.session_state.show_onboarding = False
            st.rerun()
    
    with col2:
        if st.button("Next: Choose Your Role →", type="primary", use_container_width=True):
            st.session_state.onboarding_step = 1
            st.rerun()

def show_role_selection():
    """Show role selection step"""
    st.markdown('<h2 style="color: #1E3A8A; text-align: center;">🎯 Choose Your Role</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6B7280; margin-bottom: 3rem;">Select the option that best describes your work:</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    roles = [
        {
            "icon": "👨‍💼",
            "title": "Sustainability Manager",
            "description": "Carbon accounting, reporting, and strategy",
            "key": "sustainability"
        },
        {
            "icon": "👩‍🔬", 
            "title": "Product Engineer",
            "description": "Material selection and design optimization",
            "key": "engineer"
        },
        {
            "icon": "🔬",
            "title": "Researcher/Academic",
            "description": "Academic studies and methodology",
            "key": "researcher"
        }
    ]
    
    for i, role in enumerate(roles):
        with [col1, col2, col3][i]:
            with st.container():
                st.markdown(f"""
                <div class="feature-card" style="cursor: pointer; text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">{role['icon']}</div>
                    <h3 style="color: #1E3A8A; margin-bottom: 0.5rem;">{role['title']}</h3>
                    <p style="color: #6B7280; font-size: 0.9rem;">{role['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Select {role['title']}", key=f"role_{i}", use_container_width=True):
                    st.session_state.user_role = role['key']
                    st.session_state.onboarding_step = 2
                    st.rerun()
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.onboarding_step = 0
            st.rerun()
    
    with col2:
        if st.button("Skip →", use_container_width=True):
            st.session_state.onboarding_step = 2
            st.rerun()

def show_mode_selection():
    """Show interface mode selection"""
    st.markdown('<h2 style="color: #1E3A8A; text-align: center;">🎨 Choose Your Interface</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6B7280; margin-bottom: 3rem;">Select how you want to use EcoLens:</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card" style="text-align: center; height: 100%;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🚀</div>
            <h3 style="color: #1E3A8A;">Guided Mode</h3>
            <p style="color: #6B7280; font-size: 0.9rem;">
            <strong>Perfect for beginners</strong><br>
            Step-by-step workflows<br>
            Pre-filled templates<br>
            Automated recommendations
            </p>
            <div style="margin-top: 1rem; padding: 0.5rem; background: #D1FAE5; border-radius: 8px;">
                <small>Recommended for new users</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Use Guided Mode", key="guided_mode", type="primary", use_container_width=True):
            st.session_state.interface_mode = "guided"
            st.session_state.onboarding_step = 3
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card" style="text-align: center; height: 100%;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
            <h3 style="color: #1E3A8A;">Professional Mode</h3>
            <p style="color: #6B7280; font-size: 0.9rem;">
            <strong>For experienced users</strong><br>
            Full control & customization<br>
            Advanced analytics<br>
            Direct database access
            </p>
            <div style="margin-top: 1rem; padding: 0.5rem; background: #DBEAFE; border-radius: 8px;">
                <small>For LCA experts</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Use Professional Mode", key="professional_mode", use_container_width=True):
            st.session_state.interface_mode = "professional"
            st.session_state.onboarding_step = 3
            st.rerun()
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.onboarding_step = 1
            st.rerun()

def show_get_started():
    """Show get started step"""
    st.markdown('<h2 style="color: #1E3A8A; text-align: center;">🎉 Ready to Start!</h2>', unsafe_allow_html=True)
    
    user_role = st.session_state.user_role or "User"
    interface_mode = st.session_state.interface_mode or "guided"
    
    role_names = {
        "sustainability": "Sustainability Manager",
        "engineer": "Product Engineer", 
        "researcher": "Researcher"
    }
    
    role_name = role_names.get(user_role, "User")
    
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;">
        <div style="font-size: 4rem; color: #10B981; margin-bottom: 1rem;">✅</div>
        <h3 style="color: #1E3A8A;">Perfect! You're all set.</h3>
        <p style="color: #6B7280; font-size: 1.1rem;">
        Role: <strong>{role_name}</strong><br>
        Interface: <strong>{interface_mode.title()} Mode</strong>
        </p>
        <p style="color: #6B7280; margin-top: 2rem;">
        Start analyzing products or explore the features below.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick start options
    st.markdown("### 🚀 Quick Start Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Quick Assessment", type="primary", use_container_width=True):
            st.session_state.current_workflow = "quick"
            st.session_state.onboarding_complete = True
            st.session_state.show_onboarding = False
            st.rerun()
    
    with col2:
        if st.button("Explore Features", use_container_width=True):
            st.session_state.onboarding_complete = True
            st.session_state.show_onboarding = False
            st.rerun()
    
    with col3:
        if st.button("View Tutorial", use_container_width=True):
            st.info("Tutorial coming soon!")
    
    st.markdown("---")
    
    if st.button("← Back to Mode Selection", use_container_width=True):
        st.session_state.onboarding_step = 2
        st.rerun()

# ============================================================================
# MAIN INTERFACE COMPONENTS
# ============================================================================

def show_guided_dashboard():
    """Show guided mode dashboard"""
    
    # Top bar
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown('<h1 class="main-header">EcoLens</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #6B7280; margin-bottom: 2rem;">Life Cycle Intelligence for Sustainable Engineering</p>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <div style="background: #DBEAFE; color: #1E40AF; padding: 0.5rem 1rem; border-radius: 20px; display: inline-block;">
                Guided Mode
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("Switch to Professional", use_container_width=True):
            st.session_state.interface_mode = "professional"
            st.rerun()
    
    # Hero section
    st.markdown("""
    <div class="welcome-hero">
        <h2 style="color: #1E3A8A; margin-bottom: 1rem;">Start Your Sustainability Journey</h2>
        <p style="color: #6B7280; font-size: 1.1rem; max-width: 800px; margin: 0 auto;">
        Choose a workflow below to begin analyzing your product's environmental impact.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Workflow selection
    st.markdown("### 🎯 Choose Your Analysis Type")
    
    col1, col2 = st.columns(2)
    
    workflows = [
        {
            "title": "🚀 Quick Product Assessment",
            "description": "Get instant LCA results for common products",
            "time": "3-5 minutes",
            "key": "quick"
        },
        {
            "title": "🔬 Detailed Product Analysis", 
            "description": "Full customization and advanced options",
            "time": "10-15 minutes",
            "key": "detailed"
        },
        {
            "title": "📊 Compare Alternatives",
            "description": "Side-by-side comparison of design options",
            "time": "5-8 minutes", 
            "key": "compare"
        },
        {
            "title": "🔄 Material Optimization",
            "description": "Find sustainable material alternatives",
            "time": "5-7 minutes",
            "key": "material"
        }
    ]
    
    for i, workflow in enumerate(workflows):
        with [col1, col2][i % 2]:
            with st.container():
                st.markdown(f"""
                <div class="feature-card">
                    <h3 style="color: #1E3A8A; margin-bottom: 0.5rem;">{workflow['title']}</h3>
                    <p style="color: #6B7280; font-size: 0.9rem; margin-bottom: 1rem;">
                    {workflow['description']}
                    </p>
                    <div style="display: flex; justify-content: space-between; color: #9CA3AF; font-size: 0.8rem;">
                        <span>⏱️ {workflow['time']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Start {workflow['title'].split()[0]}", key=f"workflow_{i}", use_container_width=True):
                    st.session_state.current_workflow = workflow['key']
                    st.session_state.workflow_step = 0
                    st.rerun()
    
    # Recent analyses (if any)
    if st.session_state.products:
        st.markdown("### 📋 Recent Analyses")
        
        for product in st.session_state.products[-3:]:  # Show last 3
            with st.container():
                st.markdown(f"""
                <div class="feature-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="color: #1E3A8A; margin: 0;">{product.get('name', 'Unnamed')}</h4>
                        <span style="background: #D1FAE5; color: #065F46; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.8rem;">
                            {product.get('carbon', 0)} kg CO₂e
                        </span>
                    </div>
                    <p style="color: #6B7280; font-size: 0.9rem; margin: 0.5rem 0;">
                    Analyzed on {product.get('date', 'Unknown')}
                    </p>
                    <div style="display: flex; gap: 1rem; margin-top: 0.5rem;">
                        <span style="color: #6B7280; font-size: 0.8rem;">📊 View</span>
                        <span style="color: #6B7280; font-size: 0.8rem;">📄 Report</span>
                        <span style="color: #6B7280; font-size: 0.8rem;">🔄 Compare</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

def show_quick_assessment_workflow():
    """Show quick assessment workflow"""
    
    st.markdown('<h2 style="color: #1E3A8A;">🚀 Quick Product Assessment</h2>', unsafe_allow_html=True)
    
    # Step indicator
    steps = ["Select Product", "Configure", "Results"]
    current_step = st.session_state.workflow_step
    
    cols = st.columns(3)
    for i, step in enumerate(steps):
        with cols[i]:
            status = "🔵" if i == current_step else "✅" if i < current_step else "⚪"
            color = "#3B82F6" if i == current_step else "#10B981" if i < current_step else "#9CA3AF"
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{status}</div>
                <div style="color: {color}; font-weight: {'bold' if i == current_step else 'normal'}">
                    {step}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Step content
    if current_step == 0:
        show_quick_step1()
    elif current_step == 1:
        show_quick_step2()
    elif current_step == 2:
        show_quick_results()

def show_quick_step1():
    """Step 1: Product selection"""
    st.markdown("### 1. Select Your Product Type")
    
    product_type = st.selectbox(
        "Choose from common products:",
        ["Water Bottle (500ml)", "Packaging Box", "Electronics Case", 
         "Furniture Component", "Automotive Part", "Custom Product"],
        help="Select the product type closest to yours"
    )
    
    if product_type == "Water Bottle (500ml)":
        st.info("💡 **Typical specifications:** 150g Polypropylene, Injection molding, 2-year lifespan")
    elif product_type == "Packaging Box":
        st.info("💡 **Typical specifications:** 50g Cardboard/PET, Folding/forming, Single-use")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.current_workflow = None
            st.rerun()
    
    with col2:
        if st.button("Next: Configure →", type="primary", use_container_width=True):
            st.session_state.quick_product_type = product_type
            st.session_state.workflow_step = 1
            st.rerun()

def show_quick_step2():
    """Step 2: Configuration"""
    st.markdown("### 2. Configure Your Product")
    
    with st.form("quick_config_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            material = st.selectbox(
                "Primary Material",
                ["Polypropylene (PP)", "Polyethylene Terephthalate (PET)", 
                 "Aluminum", "Stainless Steel", "Glass", "Bamboo Composite"],
                index=0
            )
            
            mass_kg = st.number_input(
                "Product Mass (kg)",
                min_value=0.01,
                max_value=50.0,
                value=0.15,
                step=0.01,
                help="Enter the mass of your product in kilograms"
            )
        
        with col2:
            manufacturing_region = st.selectbox(
                "Manufacturing Region",
                ["Asia (China)", "Europe", "North America", "Global Average"],
                help="Affects electricity grid carbon intensity"
            )
            
            lifetime_years = st.slider(
                "Expected Lifetime (years)",
                1, 10, 2,
                help="How long the product will be used"
            )
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.form_submit_button("← Back", use_container_width=True):
                st.session_state.workflow_step = 0
                st.rerun()
        
        with col2:
            if st.form_submit_button("Skip to Results", use_container_width=True):
                st.session_state.workflow_step = 2
                st.session_state.quick_config = {
                    'material': material,
                    'mass_kg': mass_kg,
                    'region': manufacturing_region,
                    'lifetime': lifetime_years
                }
                st.rerun()
        
        with col3:
            if st.form_submit_button("🔬 Run Analysis →", type="primary", use_container_width=True):
                st.session_state.workflow_step = 2
                st.session_state.quick_config = {
                    'material': material,
                    'mass_kg': mass_kg,
                    'region': manufacturing_region,
                    'lifetime': lifetime_years
                }
                st.rerun()

def show_quick_results():
    """Step 3: Results"""
    st.markdown("### 3. Analysis Results")
    
    # Simulate calculation
    with st.spinner("🔄 Calculating environmental impacts..."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
    
    # Get product type and config
    product_type = st.session_state.get('quick_product_type', 'Custom Product')
    config = st.session_state.get('quick_config', {})
    
    # Calculate results
    results = SimpleLCAEngine.calculate_quick_assessment(
        product_type.split('(')[0].strip(),
        config.get('mass_kg', 0.15),
        config.get('material', 'Polypropylene (PP)'),
        config.get('region', 'Global Average')
    )
    
    st.success("✅ Analysis complete!")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Carbon Footprint</div>
            <div class="metric-value">{results['carbon_kg']}</div>
            <div style="color: #6B7280; font-size: 0.9rem;">kg CO₂e</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Energy Use</div>
            <div class="metric-value">{results['energy_mj']}</div>
            <div style="color: #6B7280; font-size: 0.9rem;">MJ</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Circularity</div>
            <div class="metric-value">{results['circularity_score']}</div>
            <div style="color: #6B7280; font-size: 0.9rem;">{results['circularity_class']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Results visualization
    st.markdown("### 📊 Impact Breakdown")
    
    # Simple bar chart
    fig = go.Figure(data=[
        go.Bar(name='Material', x=['Carbon', 'Energy'], y=[results['carbon_kg'] * 0.6, results['energy_mj'] * 0.6], marker_color='#3B82F6'),
        go.Bar(name='Manufacturing', x=['Carbon', 'Energy'], y=[results['carbon_kg'] * 0.3, results['energy_mj'] * 0.3], marker_color='#10B981'),
        go.Bar(name='Transport', x=['Carbon', 'Energy'], y=[results['carbon_kg'] * 0.1, results['energy_mj'] * 0.1], marker_color='#F59E0B')
    ])
    
    fig.update_layout(
        barmode='stack',
        height=300,
        showlegend=True,
        title="Environmental Impact by Life Cycle Phase"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.markdown("### 💡 Improvement Recommendations")
    
    recommendations = [
        f"Switch to recycled {config.get('material', 'material')} content (30% reduction potential)",
        "Optimize transport logistics (20% reduction potential)",
        "Design for longer lifespan (15% reduction per extra year)",
        "Consider alternative material: Bamboo Composite (40% lower carbon)"
    ]
    
    for i, rec in enumerate(recommendations):
        st.markdown(f"""
        <div class="feature-card" style="padding: 1rem; margin-bottom: 0.5rem;">
            <div style="display: flex; align-items: start; gap: 1rem;">
                <div style="background: {'#3B82F6' if i == 0 else '#10B981' if i == 1 else '#F59E0B'}; 
                            color: white; width: 24px; height: 24px; border-radius: 50%; 
                            display: flex; align-items: center; justify-content: center; font-weight: bold;">
                    {i+1}
                </div>
                <div>
                    <p style="margin: 0; color: #374151;">{rec}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Next steps
    st.markdown("---")
    st.markdown("### 📈 Next Steps")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Compare Alternatives", use_container_width=True):
            st.session_state.current_workflow = "compare"
            st.session_state.workflow_step = 0
            st.rerun()
    
    with col2:
        if st.button("📄 Generate Report", use_container_width=True):
            st.success("Report generated successfully!")
    
    with col3:
        if st.button("🔄 New Analysis", type="primary", use_container_width=True):
            st.session_state.current_workflow = None
            st.session_state.workflow_step = 0
            # Save this analysis
            st.session_state.products.append({
                'name': product_type,
                'carbon': results['carbon_kg'],
                'energy': results['energy_mj'],
                'circularity': results['circularity_score'],
                'date': datetime.now().strftime('%Y-%m-%d')
            })
            st.rerun()

def show_professional_dashboard():
    """Show professional mode dashboard"""
    st.markdown('<h1 class="main-header">EcoLens Professional</h1>', unsafe_allow_html=True)
    
    # Professional tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Dashboard", 
        "🧪 Analyzer", 
        "📊 Compare", 
        "📈 Analytics"
    ])
    
    with tab1:
        show_professional_dashboard_tab()
    
    with tab2:
        show_professional_analyzer_tab()
    
    with tab3:
        show_professional_compare_tab()
    
    with tab4:
        show_professional_analytics_tab()

def show_professional_dashboard_tab():
    """Professional dashboard tab"""
    st.markdown("### 📊 Professional Dashboard")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Products Analyzed", "24", "+3")
    
    with col2:
        st.metric("Avg. Carbon", "2.4 kg", "-15%")
    
    with col3:
        st.metric("Circularity", "0.68", "+0.12")
    
    with col4:
        st.metric("Reports", "18", "+5")
    
    # Recent activity
    st.markdown("### 📋 Recent Analyses")
    
    if st.session_state.demo_products:
        for product in st.session_state.demo_products:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**{product['name']}**")
                    st.caption(f"Analyzed: {product['date']}")
                
                with col2:
                    st.metric("Carbon", f"{product['carbon']} kg")
                
                with col3:
                    st.metric("Circularity", product['circularity'])
                
                st.divider()
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("New Analysis", type="primary", use_container_width=True):
            st.session_state.current_workflow = "detailed"
            st.session_state.workflow_step = 0
            st.rerun()
    
    with col2:
        if st.button("Import Data", use_container_width=True):
            st.info("Import feature coming soon!")
    
    with col3:
        if st.button("Export All", use_container_width=True):
            st.success("Export started!")

def show_professional_analyzer_tab():
    """Professional analyzer tab"""
    st.markdown("### 🧪 Advanced Product Analyzer")
    
    with st.form("professional_analyzer"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Product Name", "Enter product name")
            st.text_area("Description", "Detailed product description")
            
            st.subheader("📦 Materials")
            material = st.selectbox("Primary Material", 
                                  ["PP", "PET", "HDPE", "AL", "Steel", "Glass"])
            mass = st.number_input("Mass (kg)", 0.01, 100.0, 0.15)
            recycled_content = st.slider("Recycled Content", 0.0, 1.0, 0.0, 0.05)
        
        with col2:
            st.subheader("🏭 Manufacturing")
            region = st.selectbox("Region", ["Asia", "Europe", "NA", "Global"])
            processes = st.multiselect("Processes", 
                                     ["Injection", "Assembly", "Finishing", "Packaging"])
            
            st.subheader("🚚 Transport")
            distance = st.number_input("Distance (km)", 0, 10000, 1000)
            mode = st.selectbox("Mode", ["Truck", "Ship", "Rail", "Air"])
        
        st.subheader("⚙️ Advanced Options")
        col1, col2 = st.columns(2)
        with col1:
            monte_carlo = st.checkbox("Monte Carlo Uncertainty", True)
            circularity = st.checkbox("Circularity Metrics", True)
        
        with col2:
            sensitivity = st.checkbox("Sensitivity Analysis", False)
            export_format = st.selectbox("Export Format", ["PDF", "Excel", "JSON"])
        
        if st.form_submit_button("Run Advanced Analysis", type="primary"):
            st.success("Advanced analysis started!")
            # Here you would call the actual LCA engine

def show_professional_compare_tab():
    """Professional compare tab"""
    st.markdown("### 📊 Design Comparison")
    st.info("Compare multiple product designs with statistical analysis")
    
    # Comparison interface would go here
    st.write("Comparison feature coming soon!")

def show_professional_analytics_tab():
    """Professional analytics tab"""
    st.markdown("### 📈 Advanced Analytics")
    
    # Sample analytics chart
    data = pd.DataFrame({
        'Product': ['Bottle A', 'Bottle B', 'Box A', 'Box B', 'Case A'],
        'Carbon': [2.4, 1.8, 1.2, 0.9, 3.2],
        'Energy': [85, 65, 45, 35, 115],
        'Circularity': [0.72, 0.85, 0.65, 0.78, 0.58]
    })
    
    fig = px.scatter(data, x='Carbon', y='Circularity', size='Energy',
                     hover_name='Product', title='Carbon vs Circularity Analysis')
    
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# MAIN APPLICATION FLOW
# ============================================================================

def main():
    """Main application flow"""
    
    # Show onboarding if not complete
    if st.session_state.show_onboarding and not st.session_state.onboarding_complete:
        show_onboarding()
        return
    
    # Check current workflow
    current_workflow = st.session_state.current_workflow
    
    if current_workflow == "quick":
        show_quick_assessment_workflow()
    elif current_workflow == "detailed":
        # Would show detailed workflow
        st.info("Detailed analysis workflow coming soon!")
        if st.button("Back to Dashboard"):
            st.session_state.current_workflow = None
            st.rerun()
    elif current_workflow == "compare":
        # Would show compare workflow
        st.info("Comparison workflow coming soon!")
        if st.button("Back to Dashboard"):
            st.session_state.current_workflow = None
            st.rerun()
    else:
        # Show appropriate dashboard
        if st.session_state.interface_mode == "guided":
            show_guided_dashboard()
        else:
            show_professional_dashboard()
    
    # Sidebar (always visible)
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h3 style="color: #1E3A8A;">🌍 EcoLens</h3>
            <p style="color: #6B7280; font-size: 0.9rem;">
                {mode} Mode • {role}
            </p>
        </div>
        """.format(
            mode=st.session_state.interface_mode.title(),
            role=st.session_state.user_role or "User"
        ), unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation
        st.markdown("**Navigation**")
        
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_workflow = None
            st.session_state.workflow_step = 0
            st.rerun()
        
        if st.button("🔄 Switch Mode", use_container_width=True):
            st.session_state.interface_mode = "professional" if st.session_state.interface_mode == "guided" else "guided"
            st.rerun()
        
        if st.button("⚙️ Settings", use_container_width=True):
            st.info("Settings panel coming soon!")
        
        if st.button("📚 Help & Tutorials", use_container_width=True):
            st.info("Help resources coming soon!")
        
        st.divider()
        
        # Quick stats
        st.markdown("**Quick Stats**")
        st.metric("Analyses", len(st.session_state.products))
        st.metric("Demo Items", len(st.session_state.demo_products))
        
        st.divider()
        
        # Reset onboarding
        if st.button("Reset Onboarding", use_container_width=True):
            st.session_state.show_onboarding = True
            st.session_state.onboarding_complete = False
            st.session_state.onboarding_step = 0
            st.rerun()

# ============================================================================
# RUN THE APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
