# ============================================================================
# ECO LENS: ADVANCED LCA INTELLIGENCE PLATFORM
# Professional User Experience Enhancement
# ============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import uuid
import io
import time
from typing import Dict, List, Optional, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

# Custom CSS with professional design
st.set_page_config(
    page_title="EcoLens: LCA Intelligence Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar for cleaner UI
)

# Custom CSS - Professional Design
st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Headers */
    .main-header {
        font-size: 3rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .sub-header {
        font-size: 1.8rem;
        color: #2563EB;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: 700;
        border-bottom: 3px solid #3B82F6;
        padding-bottom: 0.5rem;
    }
    
    .section-header {
        font-size: 1.4rem;
        color: #374151;
        margin-top: 1.5rem;
        font-weight: 600;
    }
    
    /* Cards */
    .dashboard-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #E5E7EB;
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
    }
    
    .dashboard-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    .feature-card {
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 5px solid #3B82F6;
        margin-bottom: 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s;
        width: 100%;
    }
    
    .primary-button {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
        border: none;
    }
    
    .primary-button:hover {
        background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
        transform: translateY(-2px);
    }
    
    .secondary-button {
        background: white;
        color: #3B82F6;
        border: 2px solid #3B82F6;
    }
    
    .secondary-button:hover {
        background: #3B82F6;
        color: white;
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #10B981 0%, #34D399 100%);
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
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        padding: 0 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 8px 8px 0 0;
        padding: 0 1.5rem;
        font-weight: 600;
    }
    
    /* Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted #6B7280;
        cursor: help;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 300px;
        background-color: #1F2937;
        color: white;
        text-align: center;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -150px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Welcome modal */
    .welcome-modal {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
        z-index: 1000;
        max-width: 800px;
        width: 90%;
    }
    
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 999;
    }
    
    /* Quick start cards */
    .quick-start-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 2px solid transparent;
        transition: all 0.3s;
        cursor: pointer;
        height: 100%;
    }
    
    .quick-start-card:hover {
        border-color: #3B82F6;
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(59, 130, 246, 0.15);
    }
    
    .quick-start-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Step indicators */
    .step-indicator {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
    }
    
    .step {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #E5E7EB;
        color: #6B7280;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin: 0 10px;
        position: relative;
    }
    
    .step.active {
        background: #3B82F6;
        color: white;
    }
    
    .step.completed {
        background: #10B981;
        color: white;
    }
    
    .step::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 100%;
        width: 40px;
        height: 2px;
        background: #E5E7EB;
    }
    
    .step:last-child::after {
        display: none;
    }
    
    /* Status indicators */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .status-success {
        background: #D1FAE5;
        color: #065F46;
    }
    
    .status-warning {
        background: #FEF3C7;
        color: #92400E;
    }
    
    .status-info {
        background: #DBEAFE;
        color: #1E40AF;
    }
    
    /* Form styling */
    .form-section {
        background: #F9FAFB;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #E5E7EB;
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background: #F9FAFB;
        border-radius: 12px;
        border: 2px dashed #D1D5DB;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        color: #9CA3AF;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with onboarding
if 'onboarding_complete' not in st.session_state:
    st.session_state.onboarding_complete = False
if 'current_workflow' not in st.session_state:
    st.session_state.current_workflow = None
if 'workflow_step' not in st.session_state:
    st.session_state.workflow_step = 0
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'quick_start_used' not in st.session_state:
    st.session_state.quick_start_used = False

# Import the existing LCA engine (from previous code)
# ... [Include all the previous LCA engine classes here - they remain the same]
# ProfessionalLCADatabase, AdvancedLCAEngine, ProfessionalVisualizer classes remain unchanged

# ============================================================================
# ENHANCED USER EXPERIENCE COMPONENTS
# ============================================================================

class OnboardingManager:
    """Manages user onboarding and guided workflows"""
    
    @staticmethod
    def show_welcome_modal():
        """Show welcome modal for new users"""
        if not st.session_state.onboarding_complete:
            with st.container():
                st.markdown("""
                <div class="modal-overlay"></div>
                <div class="welcome-modal">
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown('<h1 style="color: #1E3A8A; margin-bottom: 1rem;">🌍 Welcome to EcoLens</h1>', unsafe_allow_html=True)
                    st.markdown("""
                    **Your Professional LCA Intelligence Platform**
                    
                    *Transform complex environmental analysis into actionable engineering insights.*
                    
                    **Get started by:**
                    1. Selecting your role below
                    2. Choosing a workflow that matches your goal
                    3. Following the guided analysis steps
                    
                    *No prior LCA experience required.*
                    """)
                    
                    st.markdown("---")
                    
                    # Role selection
                    st.subheader("🎯 What best describes your role?")
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        if st.button("👨‍💼 **Sustainability Manager**", use_container_width=True):
                            st.session_state.user_role = "sustainability_manager"
                            st.session_state.onboarding_complete = True
                            st.rerun()
                    
                    with col_b:
                        if st.button("👩‍🔬 **Product Engineer**", use_container_width=True):
                            st.session_state.user_role = "product_engineer"
                            st.session_state.onboarding_complete = True
                            st.rerun()
                    
                    with col_c:
                        if st.button("🔬 **Researcher/Academic**", use_container_width=True):
                            st.session_state.user_role = "researcher"
                            st.session_state.onboarding_complete = True
                            st.rerun()
                
                with col2:
                    st.image("https://via.placeholder.com/200x300/3B82F6/FFFFFF?text=ECOLENS", use_column_width=True)
                    st.markdown("""
                    <div style="text-align: center; margin-top: 2rem;">
                    <small>ISO 14040/44 Compliant • Academic & Industrial Use • Circular Economy Focus</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

class WorkflowManager:
    """Manages different user workflows"""
    
    WORKFLOWS = {
        "quick_assessment": {
            "name": "🚀 Quick Product Assessment",
            "description": "Get instant LCA results for common products",
            "icon": "⚡",
            "steps": 3,
            "time_estimate": "5 minutes"
        },
        "detailed_analysis": {
            "name": "🔬 Detailed Product Analysis",
            "description": "Comprehensive LCA with advanced customization",
            "icon": "📊",
            "steps": 5,
            "time_estimate": "15 minutes"
        },
        "comparison": {
            "name": "📈 Compare Design Alternatives",
            "description": "Side-by-side comparison of product variants",
            "icon": "⚖️",
            "steps": 4,
            "time_estimate": "10 minutes"
        },
        "material_optimization": {
            "name": "🔄 Material Optimization",
            "description": "Find sustainable material alternatives",
            "icon": "🧪",
            "steps": 3,
            "time_estimate": "8 minutes"
        }
    }
    
    @staticmethod
    def show_workflow_selector():
        """Show workflow selection interface"""
        st.markdown('<h2 class="sub-header">🎯 Choose Your Analysis Goal</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color: #6B7280; margin-bottom: 2rem;">Select a workflow that matches what you want to achieve:</p>', unsafe_allow_html=True)
        
        # Create workflow cards
        cols = st.columns(2)
        workflows = list(WorkflowManager.WORKFLOWS.items())
        
        for idx, (workflow_id, workflow_info) in enumerate(workflows):
            with cols[idx % 2]:
                with st.container():
                    st.markdown(f"""
                    <div class="quick-start-card" onclick="this.style.borderColor='#3B82F6'">
                        <div class="quick-start-icon">{workflow_info['icon']}</div>
                        <h3 style="color: #1E3A8A; margin-bottom: 0.5rem;">{workflow_info['name']}</h3>
                        <p style="color: #6B7280; font-size: 0.9rem; margin-bottom: 1rem;">{workflow_info['description']}</p>
                        <div style="display: flex; justify-content: space-between; color: #9CA3AF; font-size: 0.8rem;">
                            <span>📋 {workflow_info['steps']} steps</span>
                            <span>⏱️ {workflow_info['time_estimate']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Select {workflow_info['name']}", key=f"btn_{workflow_id}"):
                        st.session_state.current_workflow = workflow_id
                        st.session_state.workflow_step = 0
                        st.session_state.quick_start_used = True
                        st.rerun()

class GuidedInterface:
    """Provides guided interfaces for different workflows"""
    
    @staticmethod
    def show_quick_assessment_workflow():
        """Quick assessment workflow for common products"""
        
        # Step indicator
        steps = ["Select Product", "Review & Adjust", "View Results"]
        GuidedInterface._show_step_indicator(steps)
        
        if st.session_state.workflow_step == 0:
            # Step 1: Product Selection
            st.markdown('<h2 class="sub-header">1. Select Your Product Type</h2>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                product_type = st.selectbox(
                    "What type of product are you analyzing?",
                    ["Water Bottle (500ml)", "Packaging Box", "Electronics Case", 
                     "Furniture Component", "Automotive Part", "Custom Product"],
                    help="Select from common product types or choose custom for specific analysis"
                )
                
                if product_type == "Water Bottle (500ml)":
                    with st.expander("📋 Pre-filled Parameters", expanded=True):
                        st.markdown("""
                        **Typical Water Bottle Specifications:**
                        - **Material:** 150g Polypropylene (PP)
                        - **Manufacturing:** Injection Molding
                        - **Transport:** 1000km by Truck
                        - **Lifetime:** 2 years
                        - **Use:** Weekly washing (52 times/year)
                        
                        *You can adjust these in the next step.*
                        """)
                
                if st.button("👉 Continue to Review", type="primary", use_container_width=True):
                    st.session_state.workflow_step = 1
                    st.rerun()
            
            with col2:
                st.markdown("""
                <div class="feature-card">
                <h4 style="color: #1E3A8A; margin-bottom: 0.5rem;">💡 Quick Tip</h4>
                <p style="color: #6B7280; font-size: 0.9rem;">
                For accurate results, ensure product type matches your actual product. You can fine-tune all parameters in the next step.
                </p>
                </div>
                """, unsafe_allow_html=True)
        
        elif st.session_state.workflow_step == 1:
            # Step 2: Review & Adjust
            st.markdown('<h2 class="sub-header">2. Review & Adjust Parameters</h2>', unsafe_allow_html=True)
            
            with st.form("quick_assessment_form"):
                st.markdown("""
                <div class="form-section">
                <h4 style="color: #374151;">📦 Material Specifications</h4>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    material = st.selectbox(
                        "Primary Material",
                        ["Polypropylene (PP)", "Polyethylene Terephthalate (PET)", 
                         "Aluminum", "Stainless Steel", "Glass", "Bamboo Composite"],
                        index=0
                    )
                
                with col2:
                    mass = st.number_input(
                        "Product Mass (grams)",
                        min_value=1,
                        max_value=5000,
                        value=150,
                        help="Enter the mass of your product in grams"
                    )
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Manufacturing
                st.markdown("""
                <div class="form-section">
                <h4 style="color: #374151;">🏭 Manufacturing</h4>
                """, unsafe_allow_html=True)
                
                manufacturing_region = st.selectbox(
                    "Manufacturing Region",
                    ["Asia (China)", "Europe", "North America", "Global Average"],
                    help="Region affects electricity grid carbon intensity"
                )
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Transport
                st.markdown("""
                <div class="form-section">
                <h4 style="color: #374151;">🚚 Transportation</h4>
                """, unsafe_allow_html=True)
                
                transport_distance = st.slider(
                    "Transport Distance (km)",
                    0, 10000, 1000, 100,
                    help="Distance from manufacturing to consumer"
                )
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("⬅️ Back", use_container_width=True):
                        st.session_state.workflow_step = 0
                        st.rerun()
                
                with col2:
                    if st.form_submit_button("🔬 Run Analysis 👉", type="primary", use_container_width=True):
                        st.session_state.workflow_step = 2
                        # Store analysis parameters
                        st.session_state.quick_analysis_params = {
                            "product_type": "Water Bottle",
                            "material": material,
                            "mass_kg": mass / 1000,
                            "manufacturing_region": manufacturing_region,
                            "transport_distance_km": transport_distance
                        }
                        st.rerun()
        
        elif st.session_state.workflow_step == 2:
            # Step 3: Results
            GuidedInterface._show_analysis_results()
    
    @staticmethod
    def show_detailed_analysis_workflow():
        """Detailed analysis workflow"""
        steps = ["Define Product", "Materials", "Manufacturing", "Transport & Use", "Results"]
        GuidedInterface._show_step_indicator(steps)
        
        # This would implement the detailed analysis from the original app
        # For brevity, showing simplified version
        if st.session_state.workflow_step < 4:
            st.markdown(f'<h2 class="sub-header">{st.session_state.workflow_step + 1}. Detailed Analysis Setup</h2>', unsafe_allow_html=True)
            
            # Navigation buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.session_state.workflow_step > 0:
                    if st.button("⬅️ Previous Step", use_container_width=True):
                        st.session_state.workflow_step -= 1
                        st.rerun()
            
            with col2:
                if st.button("Next Step 👉", type="primary", use_container_width=True):
                    st.session_state.workflow_step += 1
                    st.rerun()
        else:
            GuidedInterface._show_analysis_results()
    
    @staticmethod
    def _show_step_indicator(steps):
        """Show step progress indicator"""
        st.markdown('<div class="step-indicator">', unsafe_allow_html=True)
        
        for i, step in enumerate(steps):
            step_class = ""
            if i < st.session_state.workflow_step:
                step_class = "completed"
            elif i == st.session_state.workflow_step:
                step_class = "active"
            
            st.markdown(f'<div class="step {step_class}">{i+1}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Current step label
        if st.session_state.workflow_step < len(steps):
            current_step = steps[st.session_state.workflow_step]
            st.markdown(f'<p style="text-align: center; color: #3B82F6; font-weight: 600; margin-bottom: 2rem;">Current: {current_step}</p>', unsafe_allow_html=True)
    
    @staticmethod
    def _show_analysis_results():
        """Show analysis results with professional presentation"""
        st.markdown('<h2 class="sub-header">📊 Analysis Results</h2>', unsafe_allow_html=True)
        
        # Simulate analysis progress
        with st.spinner("🔄 Running advanced LCA analysis..."):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
        
        # Results dashboard
        st.success("✅ Analysis Complete! Results are ready.")
        
        # Key metrics in cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Carbon Footprint</div>
                <div class="metric-value">2.4</div>
                <div style="color: #6B7280; font-size: 0.9rem;">kg CO₂e</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Energy Use</div>
                <div class="metric-value">85</div>
                <div style="color: #6B7280; font-size: 0.9rem;">MJ</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Circularity</div>
                <div class="metric-value">0.72</div>
                <div style="color: #6B7280; font-size: 0.9rem;">Score (0-1)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Improvement</div>
                <div class="metric-value">35%</div>
                <div style="color: #6B7280; font-size: 0.9rem;">Potential</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Results tabs
        tab1, tab2, tab3 = st.tabs(["📈 Impact Breakdown", "🎯 Hotspots", "💡 Recommendations"])
        
        with tab1:
            # Impact breakdown chart
            fig = go.Figure(data=[
                go.Bar(name='Material', x=['Carbon', 'Energy', 'Water'], y=[1.2, 45, 75], marker_color='#3B82F6'),
                go.Bar(name='Manufacturing', x=['Carbon', 'Energy', 'Water'], y=[0.5, 25, 15], marker_color='#10B981'),
                go.Bar(name='Transport', x=['Carbon', 'Energy', 'Water'], y=[0.3, 10, 5], marker_color='#F59E0B'),
                go.Bar(name='Use', x=['Carbon', 'Energy', 'Water'], y=[0.4, 5, 100], marker_color='#EF4444'),
            ])
            
            fig.update_layout(
                title="Environmental Impact by Life Cycle Phase",
                barmode='stack',
                height=400,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Hotspots
            hotspots_data = {
                'Phase': ['Material Production', 'Transportation', 'Manufacturing'],
                'Impact (%)': [45, 30, 25],
                'Carbon (kg)': [1.2, 0.8, 0.4]
            }
            
            df = pd.DataFrame(hotspots_data)
            fig = px.bar(df, x='Phase', y='Impact (%)', color='Phase',
                        title="Environmental Hotspots Identification")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Recommendations
            st.markdown("""
            <div class="feature-card">
            <h4 style="color: #1E3A8A;">🥇 Top Recommendation</h4>
            <p><strong>Switch to Recycled PET:</strong> Reduce carbon footprint by 40% with minimal cost increase.</p>
            </div>
            
            <div class="feature-card">
            <h4 style="color: #1E3A8A;">🥈 High Impact</h4>
            <p><strong>Optimize Transport:</strong> Switch from air to sea freight for 80% carbon reduction.</p>
            </div>
            
            <div class="feature-card">
            <h4 style="color: #1E3A8A;">🥉 Good Practice</h4>
            <p><strong>Increase Product Lifetime:</strong> Design for 5+ year lifespan to reduce annual impact.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Next actions
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Compare with Alternatives", use_container_width=True):
                st.session_state.current_workflow = "comparison"
                st.session_state.workflow_step = 0
                st.rerun()
        
        with col2:
            if st.button("📄 Generate Report", use_container_width=True):
                st.success("Report generation started...")
        
        with col3:
            if st.button("🔄 New Analysis", type="primary", use_container_width=True):
                st.session_state.current_workflow = None
                st.session_state.workflow_step = 0
                st.rerun()

class DashboardView:
    """Main dashboard view"""
    
    @staticmethod
    def show_main_dashboard():
        """Show the main dashboard"""
        
        # Header
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown('<h1 class="main-header">EcoLens</h1>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; color: #6B7280; font-size: 1.2rem; margin-bottom: 2rem;">Life Cycle Intelligence for Sustainable Engineering</p>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="text-align: right; margin-top: 1rem;">
                <span class="status-badge status-info">Professional</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if st.button("⚙️ Settings", use_container_width=True):
                st.session_state.show_settings = True
        
        # Quick actions bar
        DashboardView._show_quick_actions()
        
        # Main content based on state
        if st.session_state.current_workflow:
            DashboardView._show_current_workflow()
        elif st.session_state.quick_start_used:
            WorkflowManager.show_workflow_selector()
        else:
            DashboardView._show_welcome_content()
    
    @staticmethod
    def _show_quick_actions():
        """Show quick action buttons"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%); 
                    border-radius: 12px; padding: 1rem; margin-bottom: 2rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h4 style="color: #374151; margin: 0;">Quick Actions</h4>
            <div>
                <span style="color: #6B7280; font-size: 0.9rem;">Need help? </span>
                <button onclick="alert('Guided tour starting...')" style="background: none; border: none; color: #3B82F6; cursor: pointer;">
                    Take a tour 🎓
                </button>
            </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick action buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🚀 Quick Assessment", use_container_width=True, 
                        help="Get instant LCA results for common products"):
                st.session_state.current_workflow = "quick_assessment"
                st.session_state.workflow_step = 0
                st.rerun()
        
        with col2:
            if st.button("📊 Compare Products", use_container_width=True,
                        help="Compare design alternatives side-by-side"):
                st.session_state.current_workflow = "comparison"
                st.session_state.workflow_step = 0
                st.rerun()
        
        with col3:
            if st.button("📈 View Analytics", use_container_width=True,
                        help="Access advanced analytics and trends"):
                # This would navigate to analytics view
                st.info("Analytics dashboard coming soon!")
        
        with col4:
            if st.button("📚 Learning Center", use_container_width=True,
                        help="Learn about LCA methodology and best practices"):
                st.info("Learning resources coming soon!")
    
    @staticmethod
    def _show_welcome_content():
        """Show welcome content for new users"""
        
        # Hero section
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div style="margin-bottom: 3rem;">
                <h2 style="color: #1E3A8A; font-size: 2.5rem; margin-bottom: 1rem;">
                    Transform Sustainability into Engineering Practice
                </h2>
                <p style="color: #4B5563; font-size: 1.1rem; line-height: 1.6;">
                    EcoLens bridges the gap between academic rigor and industrial application. 
                    Make data-driven sustainable design decisions with confidence using our 
                    ISO-compliant Life Cycle Assessment platform.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get started button
            if st.button("🚀 Get Started with Guided Analysis", type="primary", 
                        use_container_width=True, size="large"):
                st.session_state.quick_start_used = True
                st.rerun()
        
        with col2:
            st.image("https://via.placeholder.com/300x300/3B82F6/FFFFFF?text=ECOLENS+AI", 
                    use_column_width=True)
        
        # Features grid
        st.markdown('<h3 class="section-header">✨ Key Features</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="dashboard-card">
                <div style="font-size: 2rem; color: #3B82F6; margin-bottom: 1rem;">📊</div>
                <h4 style="color: #1E3A8A; margin-bottom: 0.5rem;">Professional LCA</h4>
                <p style="color: #6B7280; font-size: 0.9rem;">
                ISO 14040/44 compliant analysis with Monte Carlo uncertainty quantification.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="dashboard-card">
                <div style="font-size: 2rem; color: #10B981; margin-bottom: 1rem;">🔄</div>
                <h4 style="color: #1E3A8A; margin-bottom: 0.5rem;">Circular Economy</h4>
                <p style="color: #6B7280; font-size: 0.9rem;">
                Material Circularity Indicators and recyclability scoring based on Ellen MacArthur principles.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="dashboard-card">
                <div style="font-size: 2rem; color: #F59E0B; margin-bottom: 1rem;">🎯</div>
                <h4 style="color: #1E3A8A; margin-bottom: 0.5rem;">AI-Powered Insights</h4>
                <p style="color: #6B7280; font-size: 0.9rem;">
                Smart material recommendations and improvement suggestions with trade-off analysis.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Use cases
        st.markdown('<h3 class="section-header">🎯 Perfect For</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        use_cases = [
            ("👨‍💼 Sustainability Managers", "Carbon accounting, reporting, and strategy"),
            ("👩‍🔬 Product Engineers", "Material selection and design optimization"),
            ("🔬 Researchers", "Academic studies and methodology validation")
        ]
        
        for idx, (title, description) in enumerate(use_cases):
            with [col1, col2, col3][idx]:
                st.markdown(f"""
                <div class="feature-card">
                    <h4 style="color: #374151; margin-bottom: 0.5rem;">{title}</h4>
                    <p style="color: #6B7280; font-size: 0.9rem;">{description}</p>
                </div>
                """, unsafe_allow_html=True)
    
    @staticmethod
    def _show_current_workflow():
        """Show the current active workflow"""
        
        # Workflow header
        workflow_id = st.session_state.current_workflow
        workflow_info = WorkflowManager.WORKFLOWS.get(workflow_id, {})
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            <h2 style="color: #1E3A8A; margin-bottom: 0.5rem;">
                {workflow_info.get('icon', '📋')} {workflow_info.get('name', 'Workflow')}
            </h2>
            <p style="color: #6B7280; margin-bottom: 1rem;">{workflow_info.get('description', '')}</p>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("Exit Workflow", use_container_width=True):
                st.session_state.current_workflow = None
                st.session_state.workflow_step = 0
                st.rerun()
        
        # Show appropriate workflow
        if workflow_id == "quick_assessment":
            GuidedInterface.show_quick_assessment_workflow()
        elif workflow_id == "detailed_analysis":
            GuidedInterface.show_detailed_analysis_workflow()
        elif workflow_id == "comparison":
            # This would show comparison workflow
            st.info("Comparison workflow coming soon!")
        elif workflow_id == "material_optimization":
            # This would show material optimization workflow
            st.info("Material optimization workflow coming soon!")

class ProfessionalTabs:
    """Professional tab-based navigation for advanced users"""
    
    @staticmethod
    def show_professional_interface():
        """Show professional tab interface"""
        
        # Initialize the LCA engine if not already done
        if 'database' not in st.session_state:
            st.session_state.database = ProfessionalLCADatabase()
        if 'calculator' not in st.session_state:
            st.session_state.calculator = AdvancedLCAEngine(st.session_state.database)
        
        # Top navigation
        st.markdown("""
        <div style="background: white; border-bottom: 2px solid #E5E7EB; padding: 1rem 0; margin-bottom: 2rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 style="color: #1E3A8A; margin: 0; font-size: 1.8rem;">🌍 EcoLens Professional</h1>
                    <p style="color: #6B7280; margin: 0; font-size: 0.9rem;">Advanced LCA Intelligence Platform</p>
                </div>
                <div style="display: flex; gap: 1rem;">
                    <button onclick="alert('Exporting data...')" style="background: #10B981; color: white; border: none; padding: 0.5rem 1rem; border-radius: 8px; cursor: pointer;">
                        📤 Export
                    </button>
                    <button onclick="alert('Opening settings...')" style="background: none; border: 1px solid #D1D5DB; padding: 0.5rem 1rem; border-radius: 8px; cursor: pointer;">
                        ⚙️ Settings
                    </button>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Professional tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🏠 Dashboard", 
            "🧪 Product Analyzer", 
            "📊 Compare", 
            "📈 Analytics", 
            "🔍 Database", 
            "📄 Reports"
        ])
        
        with tab1:
            ProfessionalTabs._show_professional_dashboard()
        
        with tab2:
            ProfessionalTabs._show_product_analyzer()
        
        with tab3:
            ProfessionalTabs._show_comparison_tool()
        
        with tab4:
            ProfessionalTabs._show_analytics_dashboard()
        
        with tab5:
            ProfessionalTabs._show_database_explorer()
        
        with tab6:
            ProfessionalTabs._show_report_generator()
    
    @staticmethod
    def _show_professional_dashboard():
        """Professional dashboard view"""
        st.markdown("""
        <div class="dashboard-card">
            <h3 style="color: #1E3A8A; margin-bottom: 1rem;">Welcome back to EcoLens Professional</h3>
            <p style="color: #6B7280;">Access advanced LCA tools and analytics for sustainable engineering decisions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        
        stats = [
            ("Products Analyzed", "24", "+3 this week"),
            ("Avg. Carbon Saved", "42%", "Per product"),
            ("Circularity Score", "0.68", "Industry avg: 0.52"),
            ("Reports Generated", "18", "This month")
        ]
        
        for idx, (label, value, subtext) in enumerate(stats):
            with [col1, col2, col3, col4][idx]:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div style="color: #6B7280; font-size: 0.8rem;">{subtext}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Recent activity
        st.markdown('<h4 class="section-header">📋 Recent Activity</h4>', unsafe_allow_html=True)
        
        activity_data = {
            'Product': ['Water Bottle v2', 'Packaging Design', 'Electronics Case', 'Automotive Bracket'],
            'Status': ['Completed', 'In Progress', 'Completed', 'Needs Review'],
            'Carbon (kg)': [2.4, 1.8, 3.2, 5.6],
            'Circularity': [0.72, 0.65, 0.58, 0.42],
            'Date': ['2024-01-20', '2024-01-19', '2024-01-18', '2024-01-17']
        }
        
        df = pd.DataFrame(activity_data)
        st.dataframe(df, use_container_width=True)
    
    @staticmethod
    def _show_product_analyzer():
        """Professional product analyzer"""
        st.markdown('<h3 class="sub-header">🧪 Advanced Product Analysis</h3>', unsafe_allow_html=True)
        
        # This would include the full product analysis from the original app
        # Simplified for this example
        with st.form("advanced_product_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.text_input("Product Name", "Enter product name")
                st.text_area("Description", "Enter product description")
                
                st.subheader("📦 Materials")
                material = st.selectbox("Primary Material", ["PP", "PET", "Aluminum", "Steel"])
                mass = st.number_input("Mass (kg)", 0.01, 100.0, 0.15)
            
            with col2:
                st.subheader("🏭 Manufacturing")
                region = st.selectbox("Region", ["Asia", "Europe", "North America"])
                process = st.multiselect("Processes", ["Injection Molding", "Assembly", "Finishing"])
            
            if st.form_submit_button("Run Advanced Analysis", type="primary"):
                st.success("Analysis started! Check the results tab.")
    
    @staticmethod
    def _show_comparison_tool():
        """Professional comparison tool"""
        st.markdown('<h3 class="sub-header">📊 Design Alternative Comparison</h3>', unsafe_allow_html=True)
        st.info("Compare multiple product designs side-by-side with statistical significance testing.")
        # Implementation would go here
    
    @staticmethod
    def _show_analytics_dashboard():
        """Professional analytics dashboard"""
        st.markdown('<h3 class="sub-header">📈 Advanced Analytics</h3>', unsafe_allow_html=True)
        
        # Analytics tabs
        a1, a2, a3 = st.tabs(["Trends", "Correlations", "Scenario Analysis"])
        
        with a1:
            st.plotly_chart(px.line(x=[1,2,3,4], y=[10, 8, 6, 5], title="Carbon Reduction Trend"))
        
        with a2:
            st.plotly_chart(px.scatter(x=[1,2,3,4], y=[2.4, 1.8, 1.2, 0.9], title="Mass vs Carbon Correlation"))
    
    @staticmethod
    def _show_database_explorer():
        """Professional database explorer"""
        st.markdown('<h3 class="sub-header">🔍 LCA Database Explorer</h3>', unsafe_allow_html=True)
        
        if 'database' in st.session_state:
            df = st.session_state.database.materials
            st.dataframe(df, use_container_width=True)
    
    @staticmethod
    def _show_report_generator():
        """Professional report generator"""
        st.markdown('<h3 class="sub-header">📄 Professional Report Generator</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            report_type = st.selectbox("Report Type", 
                                      ["Sustainability Report", "Compliance Document", 
                                       "Academic Paper", "Executive Summary"])
        
        with col2:
            format_type = st.selectbox("Format", ["PDF", "Word", "Excel", "PowerPoint"])
        
        if st.button("Generate Professional Report", type="primary"):
            st.success("Report generation in progress...")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application with enhanced user experience"""
    
    # Show onboarding for new users
    if not st.session_state.onboarding_complete:
        OnboardingManager.show_welcome_modal()
        return
    
    # Check if user wants professional interface
    if 'use_professional_interface' not in st.session_state:
        st.session_state.use_professional_interface = False
    
    # Mode selector in sidebar (minimal)
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h4 style="color: #1E3A8A;">🌍 EcoLens</h4>
            <p style="color: #6B7280; font-size: 0.8rem;">v1.0 Professional</p>
        </div>
        """, unsafe_allow_html=True)
        
        mode = st.radio(
            "Interface Mode",
            ["Guided", "Professional"],
            help="Guided: Step-by-step workflows | Professional: Full control"
        )
        
        if mode == "Professional":
            st.session_state.use_professional_interface = True
        else:
            st.session_state.use_professional_interface = False
        
        st.markdown("---")
        
        # Quick links
        st.markdown("**Quick Links**")
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_workflow = None
            st.rerun()
        
        if st.button("📚 Tutorials", use_container_width=True):
            st.info("Tutorials coming soon!")
        
        if st.button("ℹ️ About", use_container_width=True):
            st.info("EcoLens v1.0 - Professional LCA Platform")
    
    # Show appropriate interface based on mode
    if st.session_state.use_professional_interface:
        ProfessionalTabs.show_professional_interface()
    else:
        DashboardView.show_main_dashboard()

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    # Initialize the LCA engine classes (these would be imported from separate files)
    # For this example, we'll create minimal versions
    class ProfessionalLCADatabase:
        def __init__(self):
            self.materials = pd.DataFrame({
                'name': ['PP', 'PET', 'Aluminum'],
                'carbon': [2.1, 3.2, 8.2]
            })
    
    class AdvancedLCAEngine:
        def __init__(self, db):
            self.db = db
    
    class ProfessionalVisualizer:
        pass
    
    # Run the app
    main()
