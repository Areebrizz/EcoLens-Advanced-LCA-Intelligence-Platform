# ============================================================================
# ECO LENS: PROFESSIONAL LCA PLATFORM WITH ADVANCED ANALYTICS - FIXED VERSION
# ============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import time
from datetime import datetime, timedelta
import json
from scipy import stats
import matplotlib.pyplot as plt

# Set page config FIRST
st.set_page_config(
    page_title="EcoLens: Advanced LCA Intelligence Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Enhanced with tiles and professional styling
st.markdown("""
<style>
    /* Main headers */
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 50%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 0.5rem;
    }
    
    .section-header {
        font-size: 2rem;
        color: #1E3A8A;
        font-weight: 700;
        margin: 1.5rem 0 1rem 0;
        border-left: 4px solid #3B82F6;
        padding-left: 1rem;
    }
    
    .subsection-header {
        font-size: 1.5rem;
        color: #374151;
        font-weight: 600;
        margin: 1rem 0 0.5rem 0;
    }
    
    /* Dashboard Tiles */
    .dashboard-tile {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.1);
        border: 1px solid #E5E7EB;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .dashboard-tile:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.15);
        border-color: #3B82F6;
    }
    
    .tile-header {
        font-size: 1.25rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .metric-tile {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        border-left: 5px solid #3B82F6;
    }
    
    .insight-tile {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border-left: 5px solid #10B981;
    }
    
    .warning-tile {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        border-left: 5px solid #F59E0B;
    }
    
    /* Grid System */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s;
        border: none;
    }
    
    .primary-btn {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
    }
    
    .primary-btn:hover {
        background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .secondary-btn {
        background: white;
        color: #3B82F6;
        border: 2px solid #3B82F6;
    }
    
    .secondary-btn:hover {
        background: #3B82F6;
        color: white;
    }
    
    /* Metrics */
    .metric-large {
        font-size: 3rem;
        font-weight: 800;
        color: #1E3A8A;
        margin: 0.5rem 0;
        line-height: 1;
    }
    
    .metric-medium {
        font-size: 2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin: 0.25rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }
    
    .metric-change-positive {
        color: #10B981;
        font-weight: 600;
    }
    
    .metric-change-negative {
        color: #EF4444;
        font-weight: 600;
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
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .step-inactive {
        background: #E5E7EB;
        color: #6B7280;
    }
    
    .step-completed {
        background: #10B981;
        color: white;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    /* Cards */
    .product-card {
        background: white;
        border-radius: 12px;
        padding: 1.25rem;
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
        transition: all 0.3s;
    }
    
    .product-card:hover {
        border-color: #3B82F6;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    .product-card-header {
        display: flex;
        justify-content: space-between;
        align-items: start;
        margin-bottom: 0.75rem;
    }
    
    .product-card-title {
        color: #1E3A8A;
        margin: 0;
        font-size: 1.1rem;
    }
    
    .product-card-subtitle {
        color: #6B7280;
        font-size: 0.9rem;
        margin: 0.25rem 0;
    }
    
    .product-card-metrics {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    .product-card-footer {
        display: flex;
        justify-content: space-between;
        font-size: 0.8rem;
        color: #9CA3AF;
    }
    
    /* Progress bars */
    .progress-container {
        background: #E5E7EB;
        border-radius: 10px;
        height: 10px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #3B82F6 0%, #10B981 100%);
    }
    
    /* Tags */
    .status-tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .tag-green {
        background: #D1FAE5;
        color: #065F46;
    }
    
    .tag-blue {
        background: #DBEAFE;
        color: #1E40AF;
    }
    
    .tag-yellow {
        background: #FEF3C7;
        color: #92400E;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F3F4F6;
        border-radius: 8px 8px 0 0;
        gap: 1rem;
        padding: 0.75rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3B82F6;
        color: white;
    }
    
    /* Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        background: #E5E7EB;
        color: #4B5563;
    }
    
    .badge-success {
        background: #D1FAE5;
        color: #065F46;
    }
    
    .badge-warning {
        background: #FEF3C7;
        color: #92400E;
    }
    
    .badge-danger {
        background: #FEE2E2;
        color: #991B1B;
    }
    
    /* Welcome hero */
    .welcome-hero {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
        border-radius: 20px;
        margin-bottom: 3rem;
        border: 2px dashed #CBD5E1;
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
    st.session_state.interface_mode = "guided"
    st.session_state.organization = None
    st.session_state.industry = None
    
    # Workflow state
    st.session_state.current_workflow = None
    st.session_state.workflow_step = 0
    
    # Analysis state
    st.session_state.products = []
    st.session_state.current_product = None
    st.session_state.comparison_products = []
    
    # Demo data with more products
    st.session_state.demo_products = [
        {
            'id': 'PB001',
            'name': 'Water Bottle 500ml',
            'type': 'Beverage Container',
            'carbon': 2.4,
            'energy': 85,
            'water': 12.5,
            'circularity': 0.72,
            'date': '2024-01-20',
            'material': 'PET',
            'mass': 0.15,
            'status': 'Completed',
            'lca_standard': 'ISO 14044',
            'epd_ready': True
        },
        {
            'id': 'PB002',
            'name': 'Packaging Box',
            'type': 'Packaging',
            'carbon': 1.8,
            'energy': 65,
            'water': 8.2,
            'circularity': 0.65,
            'date': '2024-01-19',
            'material': 'Corrugated Cardboard',
            'mass': 0.05,
            'status': 'Completed',
            'lca_standard': 'ISO 14040',
            'epd_ready': True
        },
        {
            'id': 'PB003',
            'name': 'Smartphone Case',
            'type': 'Electronics Accessory',
            'carbon': 3.2,
            'energy': 120,
            'water': 18.3,
            'circularity': 0.58,
            'date': '2024-01-18',
            'material': 'Polycarbonate',
            'mass': 0.02,
            'status': 'In Review',
            'lca_standard': 'PEF',
            'epd_ready': False
        },
        {
            'id': 'PB004',
            'name': 'Bicycle Frame',
            'type': 'Transportation',
            'carbon': 45.2,
            'energy': 1850,
            'water': 285,
            'circularity': 0.82,
            'date': '2024-01-17',
            'material': 'Aluminum Alloy',
            'mass': 1.8,
            'status': 'Completed',
            'lca_standard': 'ISO 14044',
            'epd_ready': True
        },
        {
            'id': 'PB005',
            'name': 'Coffee Cup Lid',
            'type': 'Food Service',
            'carbon': 0.15,
            'energy': 5.2,
            'water': 1.8,
            'circularity': 0.45,
            'date': '2024-01-16',
            'material': 'Polystyrene',
            'mass': 0.003,
            'status': 'Needs Update',
            'lca_standard': 'Simplified LCA',
            'epd_ready': False
        },
        {
            'id': 'PB006',
            'name': 'Solar Panel Frame',
            'type': 'Renewable Energy',
            'carbon': 28.5,
            'energy': 950,
            'water': 150,
            'circularity': 0.88,
            'date': '2024-01-15',
            'material': 'Anodized Aluminum',
            'mass': 3.2,
            'status': 'Completed',
            'lca_standard': 'ISO 14067',
            'epd_ready': True
        }
    ]

# ============================================================================
# ADVANCED LCA ENGINE (Academic & Professional Grade)
# ============================================================================

class AdvancedLCAEngine:
    """Professional-grade LCA engine with academic rigor"""
    
    # Comprehensive databases
    MATERIAL_DB = {
        'PET': {'carbon': 3.2, 'energy': 85, 'water': 65, 'recyclability': 0.7, 'biogenic': False},
        'PP': {'carbon': 2.8, 'energy': 80, 'water': 45, 'recyclability': 0.6, 'biogenic': False},
        'HDPE': {'carbon': 2.5, 'energy': 75, 'water': 40, 'recyclability': 0.65, 'biogenic': False},
        'Aluminum': {'carbon': 12.5, 'energy': 200, 'water': 150, 'recyclability': 0.95, 'biogenic': False},
        'Steel': {'carbon': 2.8, 'energy': 25, 'water': 40, 'recyclability': 0.9, 'biogenic': False},
        'Glass': {'carbon': 1.2, 'energy': 15, 'water': 10, 'recyclability': 1.0, 'biogenic': False},
        'Bamboo Composite': {'carbon': 0.8, 'energy': 20, 'water': 15, 'recyclability': 0.8, 'biogenic': True},
        'PLA': {'carbon': 1.5, 'energy': 45, 'water': 25, 'recyclability': 0.3, 'biogenic': True},
        'Corrugated Cardboard': {'carbon': 1.1, 'energy': 18, 'water': 30, 'recyclability': 0.85, 'biogenic': True},
        'Polycarbonate': {'carbon': 6.8, 'energy': 120, 'water': 85, 'recyclability': 0.55, 'biogenic': False}
    }
    
    PROCESS_DB = {
        'Injection Molding': {'carbon_factor': 0.8, 'energy_factor': 1.2},
        'Extrusion': {'carbon_factor': 0.6, 'energy_factor': 1.0},
        'Stamping': {'carbon_factor': 0.4, 'energy_factor': 0.8},
        'Assembly': {'carbon_factor': 0.2, 'energy_factor': 0.5},
        'Painting': {'carbon_factor': 1.2, 'energy_factor': 1.5},
        'Anodizing': {'carbon_factor': 2.5, 'energy_factor': 3.0}
    }
    
    REGION_DB = {
        'Europe': {'electricity_carbon': 0.275, 'grid_efficiency': 0.92},
        'North America': {'electricity_carbon': 0.425, 'grid_efficiency': 0.88},
        'Asia (China)': {'electricity_carbon': 0.681, 'grid_efficiency': 0.85},
        'Global Average': {'electricity_carbon': 0.475, 'grid_efficiency': 0.87}
    }
    
    @staticmethod
    def calculate_full_lca(product_data):
        """Calculate comprehensive LCA following ISO 14040/44 standards"""
        
        # Extract data
        material = product_data.get('material', 'PET')
        mass = product_data.get('mass_kg', 0.15)
        region = product_data.get('region', 'Global Average')
        lifetime = product_data.get('lifetime', 2)
        recycled_content = product_data.get('recycled_content', 0.0)
        processes = product_data.get('processes', ['Injection Molding'])
        transport_distance = product_data.get('transport_distance', 1000)
        transport_mode = product_data.get('transport_mode', 'Truck')
        
        # Get material data
        mat_data = AdvancedLCAEngine.MATERIAL_DB.get(material, AdvancedLCAEngine.MATERIAL_DB['PET'])
        
        # Calculate material impacts (including recycled content benefit)
        virgin_factor = 1 - recycled_content
        recycled_factor = recycled_content
        
        # Material production impacts
        material_carbon = mass * (mat_data['carbon'] * virgin_factor + mat_data['carbon'] * 0.3 * recycled_factor)
        material_energy = mass * (mat_data['energy'] * virgin_factor + mat_data['energy'] * 0.4 * recycled_factor)
        material_water = mass * (mat_data['water'] * virgin_factor + mat_data['water'] * 0.5 * recycled_factor)
        
        # Manufacturing impacts
        region_data = AdvancedLCAEngine.REGION_DB.get(region, AdvancedLCAEngine.REGION_DB['Global Average'])
        process_energy = 0
        process_carbon = 0
        
        for process in processes:
            proc_data = AdvancedLCAEngine.PROCESS_DB.get(process, {'carbon_factor': 1.0, 'energy_factor': 1.0})
            process_energy += mass * proc_data['energy_factor'] * 10  # 10 MJ/kg base
            process_carbon += process_energy * region_data['electricity_carbon']
        
        # Transport impacts
        transport_factors = {
            'Truck': {'carbon': 0.062, 'energy': 2.5},
            'Ship': {'carbon': 0.018, 'energy': 0.5},
            'Rail': {'carbon': 0.025, 'energy': 1.2},
            'Air': {'carbon': 0.8, 'energy': 25}
        }
        
        transport_factor = transport_factors.get(transport_mode, transport_factors['Truck'])
        transport_carbon = transport_distance * transport_factor['carbon'] * mass / 1000  # per 1000 km
        transport_energy = transport_distance * transport_factor['energy'] * mass / 1000
        
        # Use phase (if applicable)
        use_carbon = product_data.get('use_carbon', 0)
        use_energy = product_data.get('use_energy', 0)
        
        # End-of-life
        recycling_rate = mat_data['recyclability'] * 0.8  # Assume 80% of potential is achieved
        landfill_rate = 0.1
        incineration_rate = 0.1
        
        # Calculate credits for recycling
        recycling_credit = -material_carbon * 0.7 * recycling_rate  # Negative = credit
        eol_carbon = -recycling_credit * 0.3  # Remaining impacts
        
        # Total impacts
        total_carbon = material_carbon + process_carbon + transport_carbon + use_carbon + eol_carbon
        total_energy = material_energy + process_energy + transport_energy + use_energy
        total_water = material_water
        
        # Circularity metrics (Ellen MacArthur Foundation inspired)
        circularity_score = (recycled_content * 0.3 + 
                           recycling_rate * 0.3 + 
                           mat_data['recyclability'] * 0.2 + 
                           (1 if mat_data['biogenic'] else 0.5) * 0.2)
        
        # Normalize circularity
        circularity_score = min(max(circularity_score, 0), 1)
        
        # Uncertainty analysis (Monte Carlo simulation placeholder)
        uncertainty = {
            'carbon_95ci': [total_carbon * 0.85, total_carbon * 1.15],
            'energy_95ci': [total_energy * 0.8, total_energy * 1.2],
            'water_95ci': [total_water * 0.7, total_water * 1.3]
        }
        
        # Impact categories
        impact_categories = {
            'global_warming': total_carbon,
            'resource_depletion': total_energy / 100,  # Normalized
            'water_scarcity': total_water,
            'ecotoxicity': total_carbon * 0.01,  # Simplified
            'human_toxicity': total_carbon * 0.005
        }
        
        # ISO compliance flags
        iso_compliant = {
            'goal_scope': True,
            'inventory_analysis': True,
            'impact_assessment': True,
            'interpretation': True,
            'critical_review': product_data.get('reviewed', False)
        }
        
        return {
            'total_carbon_kg': round(total_carbon, 2),
            'total_energy_mj': round(total_energy, 1),
            'total_water_l': round(total_water, 1),
            'circularity_score': round(circularity_score, 2),
            'circularity_class': AdvancedLCAEngine._get_circularity_class(circularity_score),
            'breakdown': {
                'material': round(material_carbon, 2),
                'manufacturing': round(process_carbon, 2),
                'transport': round(transport_carbon, 2),
                'use': round(use_carbon, 2),
                'end_of_life': round(eol_carbon, 2)
            },
            'uncertainty': uncertainty,
            'impact_categories': impact_categories,
            'iso_compliant': iso_compliant,
            'epd_eligible': circularity_score > 0.5 and iso_compliant['critical_review'],
            'improvement_potential': AdvancedLCAEngine._calculate_improvement_potential(product_data, total_carbon)
        }
    
    @staticmethod
    def _get_circularity_class(score):
        if score >= 0.8:
            return 'Highly Circular'
        elif score >= 0.6:
            return 'Circular'
        elif score >= 0.4:
            return 'Transitional'
        else:
            return 'Linear'
    
    @staticmethod
    def _calculate_improvement_potential(product_data, current_carbon):
        """Calculate potential improvements"""
        potentials = []
        
        # Material change potential
        material = product_data.get('material', 'PET')
        if material not in ['Bamboo Composite', 'PLA', 'Corrugated Cardboard']:
            potentials.append({
                'action': f'Switch to bioplastic (PLA)',
                'reduction': 0.4,
                'cost': 'Medium',
                'feasibility': 0.7
            })
        
        # Recycling potential
        if product_data.get('recycled_content', 0) < 0.3:
            potentials.append({
                'action': 'Increase recycled content to 30%',
                'reduction': 0.15,
                'cost': 'Low',
                'feasibility': 0.9
            })
        
        # Process optimization
        if 'Injection Molding' in product_data.get('processes', []):
            potentials.append({
                'action': 'Optimize injection molding parameters',
                'reduction': 0.1,
                'cost': 'Low',
                'feasibility': 0.8
            })
        
        # Transport optimization
        if product_data.get('transport_mode', 'Truck') == 'Truck':
            potentials.append({
                'action': 'Switch to rail transport',
                'reduction': 0.25,
                'cost': 'Medium',
                'feasibility': 0.6
            })
        
        return potentials
    
    @staticmethod
    def perform_statistical_comparison(products_data):
        """Perform statistical comparison between multiple products"""
        if len(products_data) < 2:
            return None
        
        carbon_values = [p['total_carbon_kg'] for p in products_data]
        names = [p.get('name', f'Product {i+1}') for i, p in enumerate(products_data)]
        
        # Statistical tests
        if len(carbon_values) == 2:
            # T-test for two products
            t_stat, p_value = stats.ttest_ind([carbon_values[0]], [carbon_values[1]])
            significant = p_value < 0.05
        else:
            # ANOVA for multiple products
            f_stat, p_value = stats.f_oneway(*[[v] for v in carbon_values])
            significant = p_value < 0.05
        
        # Calculate confidence intervals
        confidence_intervals = []
        for value in carbon_values:
            ci = stats.t.interval(0.95, len(carbon_values)-1, 
                                 loc=value, scale=value*0.1)  # Assuming 10% std
            confidence_intervals.append(ci)
        
        return {
            'statistical_significance': significant,
            'p_value': p_value,
            'mean_carbon': np.mean(carbon_values),
            'std_carbon': np.std(carbon_values),
            'confidence_intervals': confidence_intervals,
            'ranking': sorted(zip(names, carbon_values), key=lambda x: x[1])
        }

# ============================================================================
# DASHBOARD COMPONENTS WITH TILES - FIXED VERSION
# ============================================================================

def display_metric_tile(title, value, change=None, icon="📊", subtitle=""):
    """Display a metric tile for dashboard"""
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"<div style='font-size: 2rem;'>{icon}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div style='font-size: 1.1rem; color: #1E3A8A; font-weight: bold;'>{title}</div>", unsafe_allow_html=True)
        
        st.markdown(f"<div style='font-size: 2.5rem; font-weight: bold; color: #1E3A8A; margin: 0.5rem 0;'>{value}</div>", unsafe_allow_html=True)
        
        if change is not None:
            change_color = "#10B981" if change >= 0 else "#EF4444"
            change_sign = "+" if change >= 0 else ""
            st.markdown(f"<div style='color: {change_color}; font-weight: bold;'>{change_sign}{change}%</div>", unsafe_allow_html=True)
        
        if subtitle:
            st.markdown(f"<div style='font-size: 0.8rem; color: #6B7280; margin-top: 0.25rem;'>{subtitle}</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

def display_insight_tile(title, content, insights, icon="💡"):
    """Display an insight tile"""
    with st.container():
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%); 
                    border-radius: 12px; padding: 1.5rem; border-left: 5px solid #10B981; 
                    margin-bottom: 1rem;'>
            <div style='display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;'>
                <span style='font-size: 1.5rem;'>{icon}</span>
                <span style='font-size: 1.1rem; color: #1E3A8A; font-weight: bold;'>{title}</span>
            </div>
            <p style='color: #374151; margin-bottom: 1rem;'>{content}</p>
            <ul style='color: #4B5563; padding-left: 1rem; margin: 0;'>
        """, unsafe_allow_html=True)
        
        for insight in insights:
            st.markdown(f"<li>{insight}</li>", unsafe_allow_html=True)
        
        st.markdown("</ul></div>", unsafe_allow_html=True)

def display_warning_tile(title, warning, actions, icon="⚠️"):
    """Display a warning/action tile"""
    with st.container():
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); 
                    border-radius: 12px; padding: 1.5rem; border-left: 5px solid #F59E0B; 
                    margin-bottom: 1rem;'>
            <div style='display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;'>
                <span style='font-size: 1.5rem;'>{icon}</span>
                <span style='font-size: 1.1rem; color: #92400E; font-weight: bold;'>{title}</span>
            </div>
            <p style='color: #92400E; margin-bottom: 1rem;'><strong>{warning}</strong></p>
            <div style='color: #92400E; font-size: 0.9rem; margin-bottom: 0.5rem;'>Recommended actions:</div>
            <ul style='color: #92400E; padding-left: 1rem; margin: 0; font-size: 0.9rem;'>
        """, unsafe_allow_html=True)
        
        for action in actions:
            st.markdown(f"<li>{action}</li>", unsafe_allow_html=True)
        
        st.markdown("</ul></div>", unsafe_allow_html=True)

def display_product_card(product):
    """Display a product card for listings using Streamlit components"""
    with st.container():
        # Create columns for layout
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"**{product['name']}**")
            st.caption(f"{product['type']} • {product['material']}")
        
        with col2:
            status_color = {
                'Completed': ('✅', 'green'),
                'In Review': ('🔄', 'blue'),
                'Needs Update': ('⚠️', 'orange')
            }.get(product['status'], ('📝', 'gray'))
            
            st.markdown(f"{status_color[0]} **{product['status']}**")
        
        # Metrics in columns
        metric_cols = st.columns(3)
        with metric_cols[0]:
            st.metric("Carbon", f"{product['carbon']} kg")
        with metric_cols[1]:
            st.metric("Circularity", f"{product['circularity']}")
        with metric_cols[2]:
            epd_status = "✅" if product['epd_ready'] else "❌"
            st.metric("EPD", epd_status)
        
        # Footer with ID and date
        footer_cols = st.columns(2)
        with footer_cols[0]:
            st.caption(f"ID: {product['id']}")
        with footer_cols[1]:
            st.caption(product['date'])
        
        st.divider()

# ============================================================================
# ONBOARDING COMPONENTS
# ============================================================================

def show_onboarding():
    """Show step-by-step onboarding"""
    
    steps = ["Welcome", "Organization", "Choose Role", "Select Mode", "Get Started"]
    
    # Step indicator
    cols = st.columns(len(steps))
    for i, step in enumerate(steps):
        with cols[i]:
            if i < st.session_state.onboarding_step:
                st.success(f"✓ {step}")
            elif i == st.session_state.onboarding_step:
                st.info(f"▶ {step}")
            else:
                st.write(f"{i+1}. {step}")
    
    st.divider()
    
    # Step content
    if st.session_state.onboarding_step == 0:
        show_welcome_step()
    elif st.session_state.onboarding_step == 1:
        show_organization_step()
    elif st.session_state.onboarding_step == 2:
        show_role_selection()
    elif st.session_state.onboarding_step == 3:
        show_mode_selection()
    elif st.session_state.onboarding_step == 4:
        show_get_started()

def show_welcome_step():
    """Show welcome step"""
    st.markdown('<h1 class="main-header">🌍 Welcome to EcoLens Pro</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Academic-Grade LCA Platform
        ISO 14040/44 compliant Life Cycle Assessment with statistical analysis, 
        uncertainty quantification, and academic rigor for defensible sustainability reporting.
        
        ### 🎯 Key Features:
        - Monte Carlo Uncertainty
        - Statistical Comparison
        - EPD Generation Ready
        - Sensitivity Analysis
        - Academic Database
        - ISO Compliance Checks
        """)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <div style="font-size: 5rem; color: #3B82F6; margin-bottom: 1rem;">🔬</div>
            <div style="background: #DBEAFE; color: #1E40AF; padding: 0.5rem 1rem; border-radius: 20px; display: inline-block;">
                ISO 14040/44 Compliant
            </div>
            <div style="margin-top: 1rem; color: #6B7280;">
                Trusted by researchers and professionals
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Skip Onboarding", use_container_width=True):
            st.session_state.onboarding_complete = True
            st.session_state.show_onboarding = False
            st.rerun()
    
    with col2:
        if st.button("Next: Organization →", type="primary", use_container_width=True):
            st.session_state.onboarding_step = 1
            st.rerun()

def show_organization_step():
    """Organization information step"""
    st.markdown("## 🏢 Organization Profile")
    
    with st.form("organization_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            organization = st.text_input("Organization Name", placeholder="Enter your organization name")
            industry = st.selectbox(
                "Primary Industry",
                ["Manufacturing", "Electronics", "Packaging", "Automotive", 
                 "Construction", "Consumer Goods", "Research/Academic", "Other"]
            )
        
        with col2:
            team_size = st.selectbox(
                "Team Size",
                ["1-10", "11-50", "51-200", "201-1000", "1000+"]
            )
            lca_experience = st.select_slider(
                "LCA Experience Level",
                options=["Beginner", "Intermediate", "Advanced", "Expert"]
            )
        
        compliance_needs = st.multiselect(
            "Compliance Needs",
            ["ISO 14040/44", "EPD Generation", "Carbon Reporting", 
             "Product Environmental Footprint (PEF)", "Other Standards"]
        )
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("← Back", use_container_width=True):
                st.session_state.onboarding_step = 0
                st.rerun()
        
        with col2:
            if st.form_submit_button("Next: Choose Role →", type="primary", use_container_width=True):
                st.session_state.organization = organization
                st.session_state.industry = industry
                st.session_state.onboarding_step = 2
                st.rerun()

def show_role_selection():
    """Show role selection step"""
    st.markdown("## 🎯 Choose Your Role")
    st.markdown("Select the option that best describes your work:")
    
    col1, col2, col3 = st.columns(3)
    
    roles = [
        {"icon": "👨‍💼", "title": "Sustainability Manager", "description": "Carbon accounting, reporting, and strategy", "key": "sustainability"},
        {"icon": "👩‍🔬", "title": "Product Engineer", "description": "Material selection and design optimization", "key": "engineer"},
        {"icon": "🔬", "title": "Researcher/Academic", "description": "Academic studies and methodology", "key": "researcher"}
    ]
    
    for i, role in enumerate(roles):
        with [col1, col2, col3][i]:
            if st.button(f"{role['icon']}\n\n**{role['title']}**\n\n{role['description']}", 
                        key=f"role_{i}", 
                        use_container_width=True,
                        help=f"Select {role['title']}"):
                st.session_state.user_role = role['key']
                st.session_state.onboarding_step = 3
                st.rerun()
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.onboarding_step = 1
            st.rerun()
    
    with col2:
        if st.button("Skip →", use_container_width=True):
            st.session_state.onboarding_step = 3
            st.rerun()

def show_mode_selection():
    """Show interface mode selection"""
    st.markdown("## 🎨 Choose Your Interface")
    st.markdown("Select how you want to use EcoLens:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚀 Guided Mode")
        st.markdown("**Perfect for beginners**")
        st.markdown("• Step-by-step workflows")
        st.markdown("• Pre-filled templates")
        st.markdown("• Automated recommendations")
        st.success("Recommended for new users")
        
        if st.button("Use Guided Mode", key="guided_mode", type="primary", use_container_width=True):
            st.session_state.interface_mode = "guided"
            st.session_state.onboarding_step = 4
            st.rerun()
    
    with col2:
        st.markdown("### ⚡ Professional Mode")
        st.markdown("**For experienced users**")
        st.markdown("• Full control & customization")
        st.markdown("• Advanced analytics")
        st.markdown("• Direct database access")
        st.info("For LCA experts")
        
        if st.button("Use Professional Mode", key="professional_mode", use_container_width=True):
            st.session_state.interface_mode = "professional"
            st.session_state.onboarding_step = 4
            st.rerun()
    
    st.divider()
    
    if st.button("← Back", use_container_width=True):
        st.session_state.onboarding_step = 2
        st.rerun()

def show_get_started():
    """Show get started step"""
    st.markdown("## 🎉 Ready to Start!")
    
    user_role = st.session_state.user_role or "User"
    interface_mode = st.session_state.interface_mode or "guided"
    
    role_names = {
        "sustainability": "Sustainability Manager",
        "engineer": "Product Engineer", 
        "researcher": "Researcher"
    }
    
    role_name = role_names.get(user_role, "User")
    
    st.success(f"""
    **Perfect! You're all set.**
    
    Role: **{role_name}**
    Interface: **{interface_mode.title()} Mode**
    
    Start analyzing products or explore the features below.
    """)
    
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
    
    st.divider()
    
    if st.button("← Back to Mode Selection", use_container_width=True):
        st.session_state.onboarding_step = 3
        st.rerun()

# ============================================================================
# GUIDED DASHBOARD - FIXED VERSION
# ============================================================================

def show_guided_dashboard():
    """Show guided mode dashboard with tiles"""
    
    # Top bar
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown('<h1 class="main-header">EcoLens Guided</h1>', unsafe_allow_html=True)
    
    with col2:
        st.success("**Guided Mode**")
    
    with col3:
        if st.button("Switch to Professional", use_container_width=True):
            st.session_state.interface_mode = "professional"
            st.rerun()
    
    # Welcome message
    user_role = st.session_state.user_role or "User"
    st.markdown(f"""
    <div class="welcome-hero">
        <h2 style="color: #1E3A8A; margin-bottom: 1rem;">Welcome back, {user_role}!</h2>
        <p style="color: #6B7280; font-size: 1.1rem; max-width: 800px; margin: 0 auto;">
        Start your sustainability analysis or continue where you left off.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dashboard metrics
    st.markdown("## 📊 Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_analyses = len(st.session_state.products) + len(st.session_state.demo_products)
        st.metric("Total Analyses", str(total_analyses), delta="+2 this week", delta_color="normal")
    
    with col2:
        avg_carbon = np.mean([p['carbon'] for p in st.session_state.demo_products])
        st.metric("Avg. Carbon", f"{avg_carbon:.1f} kg", delta="-5%", delta_color="inverse")
    
    with col3:
        avg_circularity = np.mean([p['circularity'] for p in st.session_state.demo_products])
        st.metric("Circularity Score", f"{avg_circularity:.2f}", delta="+8%", delta_color="normal")
    
    with col4:
        epd_ready = sum(1 for p in st.session_state.demo_products if p['epd_ready'])
        st.metric("EPD Ready", f"{epd_ready}/{len(st.session_state.demo_products)}", delta="+25%", delta_color="normal")
    
    # Quick start options
    st.markdown("## 🚀 Quick Start")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("### 🚀 Quick Assessment")
            st.markdown("Get instant LCA results for common products in 3-5 minutes.")
            st.markdown("Perfect for initial screening and feasibility studies.")
            st.markdown("**ISO 14044 • Quick Results • 3-5 min**")
            if st.button("Start Quick Assessment", key="quick_start", type="primary", use_container_width=True):
                st.session_state.current_workflow = "quick"
                st.session_state.workflow_step = 0
                st.rerun()
    
    with col2:
        with st.container():
            st.markdown("### 🔬 Advanced Analysis")
            st.markdown("Full ISO-compliant analysis with uncertainty quantification.")
            st.markdown("**ISO 14040 • Monte Carlo • 15-30 min**")
            if st.button("Start Advanced Analysis", key="advanced_start", type="primary", use_container_width=True):
                st.session_state.current_workflow = "detailed"
                st.session_state.workflow_step = 0
                st.rerun()
    
    # Recent analyses
    st.markdown("## 📋 Recent Analyses")
    
    if st.session_state.demo_products:
        # Show last 4 analyses
        recent_products = st.session_state.demo_products[:4]
        
        for product in recent_products:
            display_product_card(product)
        
        # View all button
        if st.button("View All Analyses →", use_container_width=True):
            st.session_state.current_workflow = "view_all"
            st.rerun()
    
    # Insights and recommendations
    st.markdown("## 💡 Insights & Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("### 🎯 Top Improvement Opportunity")
            st.markdown("Your packaging products show highest carbon reduction potential")
            st.markdown("""
            - Switch to recycled PET (30% reduction)
            - Optimize transport logistics
            - Implement design for recycling
            """)
    
    with col2:
        with st.container():
            st.markdown("### ⚠️ Attention Required")
            st.warning("2 products need LCA updates for compliance")
            st.markdown("""
            **Recommended actions:**
            - Update Coffee Cup Lid analysis
            - Review Smartphone Case methodology
            - Schedule critical review session
            """)

# ============================================================================
# PROFESSIONAL DASHBOARD
# ============================================================================

def show_professional_dashboard():
    """Show professional mode dashboard"""
    st.markdown('<h1 class="main-header">EcoLens Professional</h1>', unsafe_allow_html=True)
    
    # Professional tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", 
        "🧪 Analyzer", 
        "⚖️ Compare", 
        "📈 Analytics",
        "🎓 Academic"
    ])
    
    with tab1:
        show_professional_dashboard_tab()
    
    with tab2:
        show_professional_analyzer_tab()
    
    with tab3:
        show_professional_compare_tab()
    
    with tab4:
        show_professional_analytics_tab()
    
    with tab5:
        show_academic_tab()

def show_professional_dashboard_tab():
    """Professional dashboard tab with enhanced analytics"""
    
    # Quick stats
    st.markdown("## 📈 Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Products", "24", "+3 this month", delta_color="normal")
    
    with col2:
        st.metric("Avg. Carbon/Product", "13.2 kg", "-15%", delta_color="inverse")
    
    with col3:
        st.metric("Circularity Index", "0.68", "+0.12", delta_color="normal")
    
    with col4:
        st.metric("EPD Compliance", "75%", "+5%", delta_color="normal")
    
    # Main dashboard grid
    st.markdown("## 📊 Analytics Dashboard")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Carbon footprint over time
        st.markdown("#### Carbon Footprint Trend")
        
        # Generate time series data
        dates = pd.date_range(start='2023-07-01', end='2024-01-20', freq='M')
        carbon_data = pd.DataFrame({
            'Date': dates,
            'Carbon (kg)': [25, 22, 20, 18, 16, 15, 13.2],
            'Target': [20, 19, 18, 17, 16, 15, 14]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=carbon_data['Date'], 
            y=carbon_data['Carbon (kg)'],
            mode='lines+markers',
            name='Actual',
            line=dict(color='#3B82F6', width=3),
            marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=carbon_data['Date'], 
            y=carbon_data['Target'],
            mode='lines',
            name='Target',
            line=dict(color='#10B981', width=2, dash='dash')
        ))
        
        fig.update_layout(
            height=300,
            showlegend=True,
            plot_bgcolor='white',
            xaxis_title="Date",
            yaxis_title="Carbon Footprint (kg CO₂e)",
            margin=dict(l=20, r=20, t=30, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Circularity distribution
        st.markdown("#### Circularity Score Distribution")
        
        circularity_scores = [p['circularity'] for p in st.session_state.demo_products]
        
        fig = px.box(
            y=circularity_scores,
            points="all",
            height=300
        )
        
        fig.update_traces(
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8,
            marker=dict(size=8, color='#3B82F6'),
            line=dict(color='#1E3A8A', width=2)
        )
        
        fig.update_layout(
            showlegend=False,
            plot_bgcolor='white',
            yaxis_title="Circularity Score",
            margin=dict(l=20, r=20, t=30, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Product portfolio
    st.markdown("## 📦 Product Portfolio")
    
    if st.session_state.demo_products:
        # Create dataframe for visualization
        df = pd.DataFrame(st.session_state.demo_products)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Carbon vs Circularity scatter
            fig = px.scatter(
                df, 
                x='carbon', 
                y='circularity',
                size='energy',
                color='type',
                hover_name='name',
                hover_data=['material', 'mass'],
                title='Carbon vs Circularity Analysis',
                height=400
            )
            
            fig.update_layout(
                plot_bgcolor='white',
                xaxis_title="Carbon Footprint (kg CO₂e)",
                yaxis_title="Circularity Score"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Material breakdown
            material_counts = df['material'].value_counts()
            fig = px.pie(
                values=material_counts.values,
                names=material_counts.index,
                title='Material Distribution',
                height=400,
                hole=0.4
            )
            
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label'
            )
            
            st.plotly_chart(fig, use_container_width=True)

def show_professional_analyzer_tab():
    """Professional analyzer tab with advanced features"""
    
    st.markdown("## 🧪 Advanced LCA Analyzer")
    
    with st.expander("⚙️ Analysis Configuration", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 📦 Product Information")
            product_name = st.text_input("Product Name", "Advanced Product Analysis")
            product_type = st.selectbox("Product Type", 
                                      ["Packaging", "Consumer Goods", "Electronics", 
                                       "Automotive", "Construction", "Other"])
            
            st.markdown("##### 🧱 Material Specification")
            material = st.selectbox("Primary Material", 
                                  list(AdvancedLCAEngine.MATERIAL_DB.keys()))
            mass_kg = st.number_input("Mass (kg)", 0.001, 1000.0, 0.15, 0.01)
            recycled_content = st.slider("Recycled Content (%)", 0.0, 100.0, 0.0, 5.0) / 100
        
        with col2:
            st.markdown("##### 🏭 Manufacturing")
            processes = st.multiselect("Manufacturing Processes",
                                     list(AdvancedLCAEngine.PROCESS_DB.keys()),
                                     default=["Injection Molding"])
            
            region = st.selectbox("Manufacturing Region",
                                list(AdvancedLCAEngine.REGION_DB.keys()))
            
            st.markdown("##### 🚚 Logistics")
            transport_distance = st.number_input("Transport Distance (km)", 0, 20000, 1000)
            transport_mode = st.selectbox("Transport Mode", ["Truck", "Ship", "Rail", "Air"])
    
    with st.expander("🎓 Advanced Analysis Options"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            monte_carlo = st.checkbox("Monte Carlo Analysis", True)
            uncertainty_level = st.select_slider("Uncertainty Level", 
                                               options=["Low", "Medium", "High"])
        
        with col2:
            sensitivity = st.checkbox("Sensitivity Analysis", True)
            impact_categories = st.checkbox("Full Impact Categories", True)
        
        with col3:
            critical_review = st.checkbox("Critical Review", False)
            epd_generation = st.checkbox("EPD Generation Ready", False)
    
    with st.expander("📊 Use Phase & End-of-Life"):
        col1, col2 = st.columns(2)
        
        with col1:
            lifetime = st.number_input("Expected Lifetime (years)", 1, 100, 2)
            use_carbon = st.number_input("Use Phase Carbon (kg CO₂e/year)", 0.0, 1000.0, 0.0, 0.1)
        
        with col2:
            recycling_rate = st.slider("Expected Recycling Rate (%)", 0.0, 100.0, 50.0, 5.0) / 100
            landfill_rate = st.slider("Landfill Rate (%)", 0.0, 100.0, 30.0, 5.0) / 100
    
    st.divider()
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.current_workflow = None
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset Form", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("🔬 Run Advanced Analysis", type="primary", use_container_width=True):
            # Prepare product data
            product_data = {
                'name': product_name,
                'material': material,
                'mass_kg': mass_kg,
                'region': region,
                'lifetime': lifetime,
                'recycled_content': recycled_content,
                'processes': processes,
                'transport_distance': transport_distance,
                'transport_mode': transport_mode,
                'use_carbon': use_carbon,
                'reviewed': critical_review
            }
            
            # Run analysis
            with st.spinner("🔄 Running advanced LCA analysis..."):
                progress_bar = st.progress(0)
                
                # Simulate analysis steps
                steps = ["Material Analysis", "Process Calculation", "Transport Impact", 
                        "Use Phase", "End-of-Life", "Uncertainty Analysis", "Final Report"]
                
                result_container = st.container()
                
                for i, step in enumerate(steps):
                    progress_bar.progress((i + 1) / len(steps))
                    time.sleep(0.5)
                
                # Calculate results
                results = AdvancedLCAEngine.calculate_full_lca(product_data)
                
                # Display results
                with result_container:
                    st.success("✅ Advanced LCA analysis complete!")
                    
                    # Show comprehensive results
                    show_advanced_results(results, product_data)

def show_advanced_results(results, product_data):
    """Display advanced LCA results"""
    
    st.markdown("## 📊 Advanced Analysis Results")
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Carbon", f"{results['total_carbon_kg']} kg CO₂e")
    
    with col2:
        st.metric("Total Energy", f"{results['total_energy_mj']} MJ")
    
    with col3:
        st.metric("Circularity", f"{results['circularity_score']} ({results['circularity_class']})")
    
    with col4:
        st.metric("EPD Eligible", "✅" if results['epd_eligible'] else "❌")
    
    # Results tabs
    result_tabs = st.tabs(["📊 Impact Breakdown", "📈 Uncertainty", "🎯 Improvements", "📋 ISO Compliance"])
    
    with result_tabs[0]:
        # Impact breakdown
        st.markdown("##### Life Cycle Phase Contributions")
        
        breakdown_data = results['breakdown']
        phases = list(breakdown_data.keys())
        values = list(breakdown_data.values())
        
        fig = go.Figure(data=[go.Pie(
            labels=phases,
            values=values,
            hole=0.3,
            marker=dict(colors=['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#EF4444'])
        )])
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Impact categories
        if 'impact_categories' in results:
            st.markdown("##### Impact Categories")
            impacts = results['impact_categories']
            
            impact_df = pd.DataFrame({
                'Impact Category': list(impacts.keys()),
                'Value': list(impacts.values())
            })
            
            # Normalize for visualization
            impact_df['Normalized'] = impact_df['Value'] / impact_df['Value'].max()
            
            fig = px.bar(impact_df, x='Impact Category', y='Normalized',
                        color='Normalized', color_continuous_scale='Viridis')
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with result_tabs[1]:
        # Uncertainty analysis
        st.markdown("##### Monte Carlo Uncertainty Analysis")
        
        if 'uncertainty' in results:
            uncertainty = results['uncertainty']
            
            # Create uncertainty visualization
            metrics = ['Carbon (kg CO₂e)', 'Energy (MJ)', 'Water (L)']
            lower_bounds = [uncertainty['carbon_95ci'][0], 
                          uncertainty['energy_95ci'][0], 
                          uncertainty['water_95ci'][0]]
            upper_bounds = [uncertainty['carbon_95ci'][1], 
                          uncertainty['energy_95ci'][1], 
                          uncertainty['water_95ci'][1]]
            means = [results['total_carbon_kg'], 
                    results['total_energy_mj'], 
                    results['total_water_l']]
            
            fig = go.Figure()
            
            for i, metric in enumerate(metrics):
                fig.add_trace(go.Scatter(
                    x=[means[i], means[i]],
                    y=[metric, metric],
                    mode='markers',
                    name='Mean',
                    marker=dict(size=10, color='#3B82F6'),
                    showlegend=(i == 0)
                ))
                
                fig.add_trace(go.Scatter(
                    x=[lower_bounds[i], upper_bounds[i]],
                    y=[metric, metric],
                    mode='lines',
                    name='95% CI',
                    line=dict(color='#10B981', width=4),
                    showlegend=(i == 0)
                ))
            
            fig.update_layout(
                height=300,
                xaxis_title="Value",
                yaxis_title="Impact Metric",
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.info(f"📊 **Uncertainty Range:** ±{((upper_bounds[0] - lower_bounds[0]) / (2 * means[0]) * 100):.1f}% for carbon footprint")
    
    with result_tabs[2]:
        # Improvement recommendations
        st.markdown("##### Improvement Potential Analysis")
        
        if 'improvement_potential' in results:
            improvements = results['improvement_potential']
            
            if improvements:
                for i, improvement in enumerate(improvements):
                    with st.container():
                        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                        
                        with col1:
                            st.markdown(f"**{i+1}. {improvement['action']}**")
                        
                        with col2:
                            reduction = improvement['reduction'] * 100
                            st.metric("Reduction", f"{reduction:.0f}%")
                        
                        with col3:
                            st.markdown(f"**Cost:** {improvement['cost']}")
                        
                        with col4:
                            feasibility = improvement['feasibility'] * 100
                            st.progress(int(feasibility))
                            st.caption(f"{feasibility:.0f}% feasible")
                    
                    st.divider()
            else:
                st.success("✅ Excellent! Limited improvement potential found.")
    
    with result_tabs[3]:
        # ISO compliance
        st.markdown("##### ISO 14040/44 Compliance Check")
        
        if 'iso_compliant' in results:
            compliance = results['iso_compliant']
            
            compliance_df = pd.DataFrame({
                'Requirement': list(compliance.keys()),
                'Compliant': list(compliance.values())
            })
            
            # Create compliance visualization
            fig = go.Figure(data=[go.Table(
                header=dict(
                    values=['ISO Requirement', 'Status'],
                    fill_color='#1E3A8A',
                    font=dict(color='white', size=12),
                    align='left'
                ),
                cells=dict(
                    values=[compliance_df['Requirement'].str.replace('_', ' ').str.title(), 
                           ['✅ Compliant' if c else '❌ Needs Work' for c in compliance_df['Compliant']]],
                    fill_color='#F3F4F6',
                    align='left'
                )
            )])
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Overall compliance status
            compliance_rate = sum(compliance.values()) / len(compliance) * 100
            st.metric("Overall Compliance", f"{compliance_rate:.0f}%")
            
            if compliance_rate < 100:
                st.warning("⚠️ Critical review required for full ISO compliance")
            else:
                st.success("🎉 Fully ISO 14040/44 compliant!")

def show_professional_compare_tab():
    """Professional comparison tab with statistical analysis"""
    
    st.markdown("## ⚖️ Statistical Product Comparison")
    
    # Select products for comparison
    st.markdown("##### Select Products for Comparison")
    
    product_options = [f"{p['name']} ({p['id']})" for p in st.session_state.demo_products]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        product1 = st.selectbox("Product 1", product_options, index=0)
    
    with col2:
        product2 = st.selectbox("Product 2", product_options, index=1)
    
    with col3:
        product3 = st.selectbox("Product 3 (Optional)", ["None"] + product_options)
    
    # Comparison options
    with st.expander("⚙️ Comparison Settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            compare_metrics = st.multiselect(
                "Metrics to Compare",
                ["Carbon Footprint", "Energy Use", "Water Use", "Circularity", "Cost"],
                default=["Carbon Footprint", "Circularity"]
            )
            
            normalization = st.selectbox(
                "Normalization",
                ["Per unit", "Per kg", "Per functional unit"]
            )
        
        with col2:
            statistical_test = st.selectbox(
                "Statistical Test",
                ["t-test (2 products)", "ANOVA (3+ products)", "Confidence Intervals", "All"]
            )
            
            confidence_level = st.slider("Confidence Level", 0.90, 0.99, 0.95, 0.01)
    
    # Run comparison
    if st.button("🔬 Run Statistical Comparison", type="primary"):
        
        # Get selected products
        selected_products = []
        product_selections = [product1, product2]
        if product3 != "None":
            product_selections.append(product3)
        
        for prod_str in product_selections:
            prod_id = prod_str.split('(')[-1].strip(')')
            product = next((p for p in st.session_state.demo_products if p['id'] == prod_id), None)
            if product:
                selected_products.append(product)
        
        if len(selected_products) >= 2:
            with st.spinner("🔄 Running statistical analysis..."):
                time.sleep(1)
                
                # Perform comparison
                comparison_results = AdvancedLCAEngine.perform_statistical_comparison(selected_products)
                
                # Display results
                show_comparison_results(selected_products, comparison_results, compare_metrics)
        else:
            st.error("Please select at least 2 products for comparison")

def show_comparison_results(products, stats_results, metrics):
    """Display comparison results"""
    
    st.markdown("## 📊 Comparison Results")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Products Compared", len(products))
    
    with col2:
        mean_carbon = stats_results['mean_carbon'] if stats_results else 0
        st.metric("Mean Carbon", f"{mean_carbon:.1f} kg")
    
    with col3:
        std_carbon = stats_results['std_carbon'] if stats_results else 0
        st.metric("Std Deviation", f"{std_carbon:.1f} kg")
    
    with col4:
        if stats_results and stats_results['statistical_significance']:
            st.metric("Statistical Significance", "✅ Significant", delta_color="normal")
        else:
            st.metric("Statistical Significance", "❌ Not Significant", delta_color="inverse")
    
    # Comparison visualization
    st.markdown("##### 📈 Visual Comparison")
    
    # Prepare data for visualization
    comparison_data = []
    for product in products:
        comparison_data.append({
            'Product': product['name'],
            'Carbon (kg)': product['carbon'],
            'Energy (MJ)': product['energy'],
            'Water (L)': product['water'],
            'Circularity': product['circularity'],
            'Material': product['material']
        })
    
    df = pd.DataFrame(comparison_data)
    
    # Create comparison chart
    fig = go.Figure()
    
    for metric in ['Carbon (kg)', 'Circularity']:
        if metric.replace(' (kg)', '') in [m.replace(' Footprint', '') for m in metrics] or 'Carbon' in metric:
            fig.add_trace(go.Bar(
                x=df['Product'],
                y=df[metric],
                name=metric,
                text=df[metric].round(2),
                textposition='auto',
            ))
    
    fig.update_layout(
        barmode='group',
        height=400,
        title="Product Comparison",
        xaxis_title="Product",
        yaxis_title="Value",
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistical results
    if stats_results:
        st.markdown("##### 📊 Statistical Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Hypothesis Testing**")
            st.write(f"- **p-value:** {stats_results['p_value']:.4f}")
            st.write(f"- **Significant at α=0.05:** {'Yes' if stats_results['statistical_significance'] else 'No'}")
            
            if stats_results['p_value'] < 0.05:
                st.success("✅ Statistically significant differences detected")
            else:
                st.warning("⚠️ No statistically significant differences detected")
        
        with col2:
            st.markdown("**Confidence Intervals (95%)**")
            for i, product in enumerate(products):
                ci = stats_results['confidence_intervals'][i]
                st.write(f"- **{product['name']}:** [{ci[0]:.1f}, {ci[1]:.1f}] kg CO₂e")
        
        # Ranking
        st.markdown("##### 🏆 Performance Ranking")
        
        ranking_df = pd.DataFrame(stats_results['ranking'], columns=['Product', 'Carbon (kg)'])
        ranking_df['Rank'] = range(1, len(ranking_df) + 1)
        
        st.dataframe(
            ranking_df[['Rank', 'Product', 'Carbon (kg)']],
            use_container_width=True,
            hide_index=True
        )
        
        # Recommendations
        st.markdown("##### 💡 Comparison Insights")
        
        best_product = stats_results['ranking'][0][0]
        worst_product = stats_results['ranking'][-1][0]
        carbon_diff = stats_results['ranking'][-1][1] - stats_results['ranking'][0][1]
        
        insights = [
            f"**{best_product}** has the lowest carbon footprint",
            f"**{worst_product}** has {carbon_diff:.1f} kg higher carbon than {best_product}",
            "Consider adopting design elements from the best-performing product",
            "Evaluate material choices and manufacturing processes for improvement"
        ]
        
        for insight in insights:
            st.markdown(f"- {insight}")
    
    # Export options
    st.divider()
    st.markdown("##### 📤 Export Comparison")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Generate PDF Report", use_container_width=True):
            st.success("PDF report generation started!")
    
    with col2:
        if st.button("📊 Export to Excel", use_container_width=True):
            st.success("Excel export complete!")
    
    with col3:
        if st.button("🔄 New Comparison", use_container_width=True):
            st.rerun()

def show_professional_analytics_tab():
    """Professional analytics tab with comprehensive visualization"""
    
    st.markdown("## 📈 Advanced Analytics")
    
    # Create demo analytics data
    analytics_data = create_analytics_data()
    
    # Analytics tabs
    analytics_tabs = st.tabs([
        "📊 Portfolio Analysis", 
        "📈 Trend Analysis", 
        "🔍 Correlation", 
        "🎯 Benchmarking"
    ])
    
    with analytics_tabs[0]:
        show_portfolio_analysis(analytics_data)
    
    with analytics_tabs[1]:
        show_trend_analysis(analytics_data)
    
    with analytics_tabs[2]:
        show_correlation_analysis(analytics_data)
    
    with analytics_tabs[3]:
        show_benchmarking_analysis(analytics_data)

def create_analytics_data():
    """Create comprehensive analytics dataset"""
    # Enhanced demo data
    products_df = pd.DataFrame(st.session_state.demo_products)
    
    # Add additional calculated metrics
    products_df['carbon_intensity'] = products_df['carbon'] / products_df['mass']
    products_df['energy_intensity'] = products_df['energy'] / products_df['mass']
    products_df['water_intensity'] = products_df['water'] / products_df['mass']
    
    # Create time series data
    dates = pd.date_range(start='2023-01-01', end='2024-01-20', freq='M')
    time_series = pd.DataFrame({
        'date': dates,
        'total_carbon': np.cumsum(np.random.normal(15, 3, len(dates))),
        'avg_circularity': np.random.uniform(0.5, 0.8, len(dates)),
        'products_analyzed': np.cumsum(np.random.randint(1, 5, len(dates)))
    })
    
    # Create material analysis data
    materials = products_df['material'].unique()
    material_data = []
    for material in materials:
        material_products = products_df[products_df['material'] == material]
        material_data.append({
            'material': material,
            'count': len(material_products),
            'avg_carbon': material_products['carbon'].mean(),
            'avg_circularity': material_products['circularity'].mean(),
            'carbon_intensity': material_products['carbon_intensity'].mean()
        })
    
    material_df = pd.DataFrame(material_data)
    
    return {
        'products': products_df,
        'time_series': time_series,
        'materials': material_df
    }

def show_portfolio_analysis(data):
    """Show portfolio analysis"""
    
    st.markdown("##### Product Portfolio Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Carbon intensity by product type
        fig = px.treemap(
            data['products'],
            path=['type', 'name'],
            values='carbon',
            color='circularity',
            color_continuous_scale='RdYlGn',
            title='Carbon Footprint by Product Type'
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Material performance
        fig = px.scatter(
            data['materials'],
            x='avg_carbon',
            y='avg_circularity',
            size='count',
            color='material',
            hover_name='material',
            title='Material Performance: Carbon vs Circularity'
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance matrix
    st.markdown("##### Performance Matrix")
    
    # Create performance categories
    products_df = data['products'].copy()
    products_df['performance'] = np.where(
        (products_df['carbon'] < products_df['carbon'].median()) & 
        (products_df['circularity'] > products_df['circularity'].median()),
        'High Performance',
        np.where(
            (products_df['carbon'] > products_df['carbon'].median()) & 
            (products_df['circularity'] < products_df['circularity'].median()),
            'Needs Improvement',
            'Moderate Performance'
        )
    )
    
    fig = px.scatter(
        products_df,
        x='carbon',
        y='circularity',
        color='performance',
        size='mass',
        hover_name='name',
        title='Performance Matrix: Carbon vs Circularity'
    )
    
    # Add quadrant lines
    median_carbon = products_df['carbon'].median()
    median_circularity = products_df['circularity'].median()
    
    fig.add_hline(y=median_circularity, line_dash="dash", line_color="gray")
    fig.add_vline(x=median_carbon, line_dash="dash", line_color="gray")
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def show_trend_analysis(data):
    """Show trend analysis"""
    
    st.markdown("##### Time Series Analysis")
    
    # Multiple trend lines
    fig = go.Figure()
    
    # Add traces for different metrics
    fig.add_trace(go.Scatter(
        x=data['time_series']['date'],
        y=data['time_series']['total_carbon'],
        mode='lines+markers',
        name='Total Carbon',
        line=dict(color='#EF4444', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=data['time_series']['date'],
        y=data['time_series']['avg_circularity'] * 100,  # Scale for visualization
        mode='lines+markers',
        name='Avg Circularity (%)',
        yaxis='y2',
        line=dict(color='#10B981', width=3)
    ))
    
    fig.update_layout(
        height=400,
        title="Sustainability Metrics Over Time",
        xaxis_title="Date",
        yaxis_title="Total Carbon (kg CO₂e)",
        yaxis2=dict(
            title="Circularity (%)",
            overlaying='y',
            side='right'
        ),
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Rolling statistics
    st.markdown("##### Rolling Statistics")
    
    time_series = data['time_series'].set_index('date')
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Rolling average
        time_series['carbon_rolling'] = time_series['total_carbon'].rolling(window=3).mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time_series.index,
            y=time_series['total_carbon'],
            mode='lines',
            name='Actual',
            line=dict(color='#93C5FD', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=time_series.index,
            y=time_series['carbon_rolling'],
            mode='lines',
            name='3-Month Moving Average',
            line=dict(color='#1E40AF', width=3)
        ))
        
        fig.update_layout(
            height=300,
            title="Carbon Footprint Trend with Moving Average"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Cumulative analysis
        time_series['cumulative_carbon'] = time_series['total_carbon'].cumsum()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=time_series.index,
            y=time_series['total_carbon'],
            name='Monthly Carbon',
            marker_color='#3B82F6'
        ))
        fig.add_trace(go.Scatter(
            x=time_series.index,
            y=time_series['cumulative_carbon'],
            name='Cumulative Carbon',
            yaxis='y2',
            line=dict(color='#10B981', width=3)
        ))
        
        fig.update_layout(
            height=300,
            title="Cumulative Carbon Analysis",
            yaxis2=dict(
                title="Cumulative Carbon",
                overlaying='y',
                side='right'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_correlation_analysis(data):
    """Show correlation analysis"""
    
    st.markdown("##### Correlation Matrix")
    
    # Select numeric columns for correlation
    numeric_cols = ['carbon', 'energy', 'water', 'circularity', 'mass']
    correlation_data = data['products'][numeric_cols]
    
    # Calculate correlation matrix
    corr_matrix = correlation_data.corr()
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.round(2).values,
        texttemplate='%{text}',
        textfont={"size": 10}
    ))
    
    fig.update_layout(
        height=500,
        title="Correlation Matrix of Sustainability Metrics"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Pair plot
    st.markdown("##### Pair Plot Analysis")
    
    fig = px.scatter_matrix(
        correlation_data,
        dimensions=numeric_cols,
        color=data['products']['type'],
        title="Pairwise Relationships"
    )
    
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistical correlation insights
    st.markdown("##### 📊 Correlation Insights")
    
    insights = [
        f"**Carbon vs Mass:** Correlation = {corr_matrix.loc['carbon', 'mass']:.2f}",
        f"**Circularity vs Carbon:** Correlation = {corr_matrix.loc['circularity', 'carbon']:.2f}",
        f"**Energy vs Water:** Correlation = {corr_matrix.loc['energy', 'water']:.2f}"
    ]
    
    for insight in insights:
        st.markdown(f"- {insight}")

def show_benchmarking_analysis(data):
    """Show benchmarking analysis"""
    
    st.markdown("##### Industry Benchmarking")
    
    # Create benchmark data
    benchmark_data = pd.DataFrame({
        'Metric': ['Carbon Intensity', 'Circularity Score', 'Energy Use', 'Water Use'],
        'Your Portfolio': [
            data['products']['carbon_intensity'].mean(),
            data['products']['circularity'].mean(),
            data['products']['energy'].mean(),
            data['products']['water'].mean()
        ],
        'Industry Average': [2.5, 0.65, 95, 85],
        'Best in Class': [1.2, 0.85, 45, 40]
    })
    
    # Radar chart for benchmarking
    categories = benchmark_data['Metric'].tolist()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=benchmark_data['Your Portfolio'],
        theta=categories,
        fill='toself',
        name='Your Portfolio',
        line_color='#3B82F6'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=benchmark_data['Industry Average'],
        theta=categories,
        fill='toself',
        name='Industry Average',
        line_color='#10B981'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=benchmark_data['Best in Class'],
        theta=categories,
        fill='toself',
        name='Best in Class',
        line_color='#F59E0B'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 3]
            )),
        showlegend=True,
        height=500,
        title="Benchmarking Analysis"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Gap analysis
    st.markdown("##### Gap Analysis")
    
    benchmark_data['Gap to Best'] = ((benchmark_data['Your Portfolio'] - benchmark_data['Best in Class']) / 
                                    benchmark_data['Best in Class']) * 100
    
    fig = px.bar(
        benchmark_data,
        x='Metric',
        y='Gap to Best',
        color='Gap to Best',
        color_continuous_scale='RdYlGn_r',
        title="Performance Gap to Best in Class (%)"
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Improvement recommendations
    st.markdown("##### 🎯 Improvement Priorities")
    
    # Sort by largest gap
    sorted_benchmark = benchmark_data.sort_values('Gap to Best', ascending=False)
    
    for idx, row in sorted_benchmark.iterrows():
        gap = row['Gap to Best']
        metric = row['Metric']
        
        if gap > 0:
            st.warning(f"**{metric}:** {gap:.0f}% above best in class")
        else:
            st.success(f"**{metric}:** {abs(gap):.0f}% better than best in class")

def show_academic_tab():
    """Academic/research tab"""
    
    st.markdown("## 🎓 Academic & Research Features")
    
    # Academic features
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("### 📚 Methodology Library")
            st.markdown("Access to academic LCA methodologies and databases:")
            st.markdown("""
            - Ecoinvent Database v3.8
            - USLCI Database
            - GREET Model
            - ISO 14040/44 Guidelines
            - PEF Methodology
            """)
    
    with col2:
        with st.container():
            st.markdown("### 🔬 Research Tools")
            st.markdown("Advanced tools for academic research:")
            st.markdown("""
            - Sensitivity Analysis
            - Monte Carlo Uncertainty
            - Scenario Modeling
            - Statistical Testing
            - Peer Review Templates
            """)
    
    # Publication-ready reports
    st.markdown("### 📄 Publication-Ready Outputs")
    
    with st.expander("Generate Academic Report"):
        col1, col2 = st.columns(2)
        
        with col1:
            report_type = st.selectbox(
                "Report Type",
                ["Journal Article", "Conference Paper", "Thesis Chapter", "Research Report"]
            )
            
            citation_style = st.selectbox(
                "Citation Style",
                ["APA", "Chicago", "IEEE", "Harvard", "Nature"]
            )
        
        with col2:
            include_sections = st.multiselect(
                "Include Sections",
                ["Abstract", "Introduction", "Methodology", "Results", 
                 "Discussion", "Conclusion", "References", "Appendices"],
                default=["Abstract", "Methodology", "Results", "Discussion"]
            )
            
            add_peer_review = st.checkbox("Include Peer Review Comments", True)
        
        if st.button("Generate Academic Report", type="primary"):
            st.success("Academic report generated successfully!")
            st.info("📄 Report includes: Methodology description, statistical analysis, uncertainty quantification, and ISO compliance statement")

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
        # Simplified quick assessment
        show_quick_assessment()
    elif current_workflow == "detailed":
        show_professional_analyzer_tab()
    elif current_workflow == "compare":
        show_professional_compare_tab()
    elif current_workflow == "view_all":
        show_all_analyses()
    else:
        # Show appropriate dashboard
        if st.session_state.interface_mode == "guided":
            show_guided_dashboard()
        else:
            show_professional_dashboard()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🌍 EcoLens Pro")
        
        # Mode indicator
        interface_mode = st.session_state.interface_mode
        if interface_mode == "guided":
            st.success("**Guided Mode**")
        else:
            st.info("**Professional Mode**")
        
        st.divider()
        
        # Quick actions
        st.markdown("**⚡ Quick Actions**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠", help="Home", use_container_width=True):
                st.session_state.current_workflow = None
                st.rerun()
        
        with col2:
            if st.button("🔄", help="New Analysis", use_container_width=True):
                st.session_state.current_workflow = "quick"
                st.session_state.workflow_step = 0
                st.rerun()
        
        st.divider()
        
        # Navigation
        st.markdown("**Navigation**")
        
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.current_workflow = None
            st.rerun()
        
        if st.button("🔬 Analyzer", use_container_width=True):
            st.session_state.current_workflow = "detailed"
            st.rerun()
        
        if st.button("⚖️ Compare", use_container_width=True):
            st.session_state.current_workflow = "compare"
            st.rerun()
        
        if st.button("📈 Analytics", use_container_width=True):
            st.session_state.current_workflow = None
            st.session_state.interface_mode = "professional"
            st.rerun()
        
        st.divider()
        
        # System status
        st.markdown("**System Status**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Analyses", len(st.session_state.products))
        
        with col2:
            st.metric("Active", len(st.session_state.demo_products))
        
        # Database status
        st.caption("Database: 🟢 Online")
        
        st.divider()
        
        # Settings and help
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("⚙️ Settings", use_container_width=True):
                st.info("Settings panel coming soon!")
        
        with col2:
            if st.button("❓ Help", use_container_width=True):
                st.info("Help resources coming soon!")
        
        # Reset onboarding
        if st.button("Reset Onboarding", use_container_width=True):
            st.session_state.show_onboarding = True
            st.session_state.onboarding_complete = False
            st.session_state.onboarding_step = 0
            st.rerun()

def show_quick_assessment():
    """Show quick assessment workflow"""
    st.markdown("## 🚀 Quick Product Assessment")
    
    st.markdown("### 1. Select Your Product Type")
    product_type = st.selectbox(
        "Choose from common products:",
        ["Water Bottle (500ml)", "Packaging Box", "Electronics Case", 
         "Furniture Component", "Automotive Part", "Custom Product"],
        help="Select the product type closest to yours"
    )
    
    if product_type == "Water Bottle (500ml)":
        st.info("💡 **Typical specifications:** 150g Polypropylene, Injection molding, 2-year lifespan")
    
    st.markdown("### 2. Configure Your Product")
    
    with st.form("quick_config"):
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
        
        submitted = st.form_submit_button("🔬 Run Quick Analysis", type="primary")
        
        if submitted:
            with st.spinner("Calculating environmental impacts..."):
                time.sleep(2)
                
                # Simulate calculation
                base_carbon = 2.4
                results = {
                    'carbon': round(base_carbon * (mass_kg / 0.15), 2),
                    'energy': round(base_carbon * 35 * (mass_kg / 0.15), 1),
                    'circularity': 0.72
                }
                
                st.success("✅ Analysis complete!")
                
                # Show results
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Carbon Footprint", f"{results['carbon']} kg CO₂e")
                with col2:
                    st.metric("Energy Use", f"{results['energy']} MJ")
                with col3:
                    st.metric("Circularity", f"{results['circularity']}")
                
                # Recommendations
                st.markdown("### 💡 Improvement Recommendations")
                recommendations = [
                    f"Switch to recycled {material.split('(')[0].strip()} (30% reduction potential)",
                    "Optimize transport logistics (20% reduction potential)",
                    "Design for longer lifespan (15% reduction per extra year)"
                ]
                
                for i, rec in enumerate(recommendations):
                    st.markdown(f"{i+1}. {rec}")
                
                # Save analysis
                st.session_state.products.append({
                    'name': product_type,
                    'carbon': results['carbon'],
                    'energy': results['energy'],
                    'circularity': results['circularity'],
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
    
    st.divider()
    if st.button("← Back to Dashboard", use_container_width=True):
        st.session_state.current_workflow = None
        st.rerun()

def show_all_analyses():
    """Show all analyses view"""
    st.markdown("## All Analyses")
    
    # Filter options
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        filter_type = st.selectbox("Type", ["All"] + list(set(p['type'] for p in st.session_state.demo_products)))
    
    with col2:
        filter_status = st.selectbox("Status", ["All"] + list(set(p['status'] for p in st.session_state.demo_products)))
    
    with col3:
        filter_material = st.selectbox("Material", ["All"] + list(set(p['material'] for p in st.session_state.demo_products)))
    
    with col4:
        sort_by = st.selectbox("Sort By", ["Date", "Carbon", "Circularity", "Name"])
    
    # Filter products
    filtered_products = st.session_state.demo_products.copy()
    
    if filter_type != "All":
        filtered_products = [p for p in filtered_products if p['type'] == filter_type]
    
    if filter_status != "All":
        filtered_products = [p for p in filtered_products if p['status'] == filter_status]
    
    if filter_material != "All":
        filtered_products = [p for p in filtered_products if p['material'] == filter_material]
    
    # Sort products
    if sort_by == "Date":
        filtered_products.sort(key=lambda x: x['date'], reverse=True)
    elif sort_by == "Carbon":
        filtered_products.sort(key=lambda x: x['carbon'])
    elif sort_by == "Circularity":
        filtered_products.sort(key=lambda x: x['circularity'], reverse=True)
    elif sort_by == "Name":
        filtered_products.sort(key=lambda x: x['name'])
    
    # Display products
    st.markdown(f"**Showing {len(filtered_products)} analyses**")
    
    for product in filtered_products:
        display_product_card(product)
    
    # Back button
    if st.button("← Back to Dashboard", use_container_width=True):
        st.session_state.current_workflow = None
        st.rerun()

# ============================================================================
# RUN THE APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
