# ============================================================================
# ECO LENS PRO - COMPLETE SINGLE-FILE VERSION
# Advanced LCA Intelligence Platform
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
import warnings
from typing import Dict, List, Optional, Tuple, Any
import hashlib
from scipy import stats
import itertools
warnings.filterwarnings('ignore')

# Set page config FIRST
st.set_page_config(
    page_title="EcoLens Pro | Advanced LCA Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS FOR PROFESSIONAL UI
# ============================================================================
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
        color: white;
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
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: var(--gray);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    
    /* Status badges */
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
    
    /* Tabs */
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
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
def initialize_session_state():
    """Initialize all session state variables"""
    if 'app_initialized' not in st.session_state:
        st.session_state.app_initialized = True
        
        # User settings
        st.session_state.user = {
            'role': 'engineer',
            'organization': 'EcoLens Professional',
            'preferences': {
                'units': 'metric',
                'currency': 'USD',
                'theme': 'light'
            }
        }
        
        # Application state
        st.session_state.current_view = 'dashboard'
        st.session_state.current_workflow = None
        st.session_state.workflow_step = 0
        st.session_state.project_id = str(uuid.uuid4())[:8]
        
        # Data storage
        st.session_state.products = []
        st.session_state.comparisons = []
        st.session_state.scenarios = []
        st.session_state.analytics = []
        
        # UI state
        st.session_state.sidebar_expanded = True
        st.session_state.notifications = [
            {'id': 1, 'type': 'info', 'message': 'Welcome to EcoLens Pro!', 'read': False},
            {'id': 2, 'type': 'success', 'message': 'System initialized successfully', 'read': False}
        ]

# ============================================================================
# ADVANCED LCA DATABASE
# ============================================================================
class AdvancedLCADatabase:
    """Comprehensive LCA database with uncertainty modeling"""
    
    def __init__(self):
        self.materials = self._create_material_database()
        self.processes = self._create_process_database()
        self.transport = self._create_transport_database()
        self.regional_factors = self._create_regional_factors()
        self.circularity_metrics = self._create_circularity_metrics()
    
    def _create_material_database(self):
        """Create comprehensive material database"""
        data = {
            'id': ['PP', 'PET', 'HDPE', 'AL6061', 'SUS304', 'GLASS', 'R_PET', 'R_PP', 'BIOPLA', 'BAMBOO'],
            'name': ['Polypropylene', 'Polyethylene Terephthalate', 'High-Density Polyethylene',
                    'Aluminum 6061', 'Stainless Steel 304', 'Soda-lime Glass', 'Recycled PET',
                    'Recycled PP', 'Polylactic Acid (PLA)', 'Bamboo Composite'],
            'category': ['Polymer', 'Polymer', 'Polymer', 'Metal', 'Metal', 'Mineral',
                        'Recycled', 'Recycled', 'Biopolymer', 'Biocomposite'],
            'density_kg_m3': [905, 1380, 955, 2700, 7930, 2500, 1380, 905, 1250, 700],
            'carbon_kgCO2e_kg': [2.1, 3.2, 1.9, 8.2, 6.2, 1.4, 1.5, 1.2, 1.8, 0.3],
            'carbon_std': [0.1, 0.15, 0.09, 0.4, 0.3, 0.1, 0.08, 0.06, 0.1, 0.02],
            'energy_MJ_kg': [85.6, 84.2, 78.1, 218.0, 56.7, 15.0, 45.0, 50.0, 54.0, 2.5],
            'water_L_kg': [75, 120, 65, 350, 260, 15, 40, 35, 30, 5],
            'recyclability': [0.85, 0.90, 0.85, 0.95, 0.95, 1.00, 0.95, 0.90, 0.60, 0.95],
            'price_usd_kg': [1.8, 2.1, 1.9, 3.2, 4.8, 1.2, 2.0, 1.9, 3.0, 3.5],
            'strength_MPa': [35, 55, 30, 310, 515, 50, 50, 35, 60, 30],
            'impact_score': [5.2, 6.8, 4.9, 9.5, 7.8, 3.1, 3.8, 3.5, 4.2, 1.2]
        }
        return pd.DataFrame(data)
    
    def _create_process_database(self):
        """Create manufacturing process database"""
        data = {
            'process': ['Injection Molding', 'Blow Molding', 'Thermoforming', 'Extrusion',
                       'Casting', 'CNC Machining', 'Assembly', 'Surface Treatment'],
            'energy_kWh_kg': [1.2, 0.9, 0.8, 0.7, 1.5, 3.0, 0.2, 0.4],
            'carbon_kgCO2e_kg': [0.15, 0.12, 0.10, 0.09, 0.20, 0.40, 0.03, 0.05],
            'scrap_rate': [0.05, 0.03, 0.04, 0.02, 0.10, 0.15, 0.01, 0.02],
            'water_L_kg': [10, 8, 6, 5, 15, 12, 1, 5]
        }
        return pd.DataFrame(data)
    
    def _create_transport_database(self):
        """Create transport mode database"""
        data = {
            'mode': ['Truck (Diesel)', 'Truck (Electric)', 'Rail', 'Ship', 'Air Freight'],
            'carbon_gCO2e_tonne_km': [62, 15, 22, 10, 500],
            'energy_MJ_tonne_km': [2.8, 0.7, 1.0, 0.5, 22.0],
            'cost_usd_tonne_km': [0.15, 0.18, 0.08, 0.03, 1.50],
            'speed_km_h': [80, 80, 60, 40, 900]
        }
        return pd.DataFrame(data)
    
    def _create_regional_factors(self):
        """Create regional electricity grid factors"""
        return {
            'Europe': {'carbon_gCO2e_kWh': 275, 'renewable_share': 0.38},
            'North America': {'carbon_gCO2e_kWh': 380, 'renewable_share': 0.20},
            'Asia': {'carbon_gCO2e_kWh': 620, 'renewable_share': 0.15},
            'China': {'carbon_gCO2e_kWh': 680, 'renewable_share': 0.12},
            'Global Average': {'carbon_gCO2e_kWh': 475, 'renewable_share': 0.25}
        }
    
    def _create_circularity_metrics(self):
        """Create circular economy metrics"""
        return {
            'Material Circularity Indicator': {
                'formula': 'MCI = (Functional Use + M_F_linear) / (M_F_linear + M_V_linear + M_L)',
                'weighting': {'virgin_material': 0.4, 'recycling_rate': 0.3, 'lifetime': 0.3}
            },
            'Recycling Efficiency': {
                'thresholds': {'excellent': 0.9, 'good': 0.7, 'poor': 0.5}
            }
        }
    
    def get_material_suggestions(self, current_material, target_reduction=20):
        """Get material substitution suggestions"""
        current = self.materials[self.materials['id'] == current_material]
        if len(current) == 0:
            return []
        
        current = current.iloc[0]
        suggestions = []
        
        for _, mat in self.materials.iterrows():
            if mat['id'] != current_material:
                reduction = ((current['carbon_kgCO2e_kg'] - mat['carbon_kgCO2e_kg']) / 
                           current['carbon_kgCO2e_kg'] * 100)
                
                if reduction >= target_reduction:
                    suggestions.append({
                        'material': mat['name'],
                        'id': mat['id'],
                        'carbon_reduction_%': reduction,
                        'carbon_kgCO2e_kg': mat['carbon_kgCO2e_kg'],
                        'cost_change_%': ((mat['price_usd_kg'] - current['price_usd_kg']) / 
                                        current['price_usd_kg'] * 100),
                        'impact_score': mat['impact_score']
                    })
        
        return sorted(suggestions, key=lambda x: x['impact_score'])[:5]

# ============================================================================
# ADVANCED LCA CALCULATOR
# ============================================================================
class AdvancedLCAEngine:
    """Advanced LCA calculation engine with uncertainty modeling"""
    
    def __init__(self, database):
        self.db = database
    
    def calculate_product_lca(self, product_spec):
        """Calculate comprehensive LCA for a product"""
        
        # Calculate all phases
        material_results = self._calculate_material_phase(product_spec)
        manufacturing_results = self._calculate_manufacturing_phase(product_spec)
        transport_results = self._calculate_transport_phase(product_spec)
        use_results = self._calculate_use_phase(product_spec)
        eol_results = self._calculate_eol_phase(product_spec)
        
        # Calculate totals
        totals = self._calculate_totals(material_results, manufacturing_results,
                                       transport_results, use_results, eol_results)
        
        # Perform uncertainty analysis
        uncertainty = self._monte_carlo_analysis(product_spec)
        
        # Calculate circularity metrics
        circularity = self._calculate_circularity(product_spec)
        
        # Identify hotspots
        hotspots = self._identify_hotspots(material_results, manufacturing_results,
                                          transport_results, use_results, eol_results)
        
        # Calculate improvement potential
        improvement = self._calculate_improvement_potential(product_spec)
        
        # Compile results
        results = {
            'product_id': product_spec.get('product_id', str(uuid.uuid4())[:8]),
            'product_name': product_spec.get('product_name', 'Unnamed Product'),
            'timestamp': datetime.now().isoformat(),
            'phases': {
                'material': material_results,
                'manufacturing': manufacturing_results,
                'transport': transport_results,
                'use': use_results,
                'end_of_life': eol_results
            },
            'totals': totals,
            'uncertainty': uncertainty,
            'circularity_metrics': circularity,
            'hotspots': hotspots,
            'improvement_potential': improvement,
            'specification': product_spec
        }
        
        return results
    
    def _calculate_material_phase(self, product_spec):
        """Calculate material phase impacts"""
        materials = product_spec.get('materials', [])
        
        results = {
            'mass_kg': 0,
            'carbon_kgCO2e': 0,
            'energy_MJ': 0,
            'water_L': 0,
            'cost_usd': 0,
            'materials_detail': []
        }
        
        for mat in materials:
            material_id = mat.get('material_id', 'PP')
            mass = mat.get('mass_kg', 0)
            recycled_content = mat.get('recycled_content', 0)
            
            material_data = self.db.materials[self.db.materials['id'] == material_id]
            if len(material_data) == 0:
                continue
            
            material_data = material_data.iloc[0]
            
            # Adjust for recycled content
            virgin_factor = (1 - recycled_content)
            recycled_factor = recycled_content * 0.3
            
            carbon = mass * material_data['carbon_kgCO2e_kg'] * (virgin_factor + recycled_factor)
            energy = mass * material_data['energy_MJ_kg'] * (virgin_factor + recycled_factor * 0.4)
            water = mass * material_data['water_L_kg'] * (virgin_factor + recycled_factor * 0.2)
            cost = mass * material_data['price_usd_kg'] * (virgin_factor + recycled_factor * 0.8)
            
            results['mass_kg'] += mass
            results['carbon_kgCO2e'] += carbon
            results['energy_MJ'] += energy
            results['water_L'] += water
            results['cost_usd'] += cost
            
            results['materials_detail'].append({
                'material': material_id,
                'mass_kg': mass,
                'carbon_kgCO2e': carbon,
                'recycled_content': recycled_content
            })
        
        return results
    
    def _calculate_manufacturing_phase(self, product_spec):
        """Calculate manufacturing phase impacts"""
        processes = product_spec.get('manufacturing_processes', [])
        region = product_spec.get('manufacturing_region', 'Global Average')
        electricity_factor = self.db.regional_factors.get(region, 
                                                         self.db.regional_factors['Global Average'])
        
        results = {
            'carbon_kgCO2e': 0,
            'energy_MJ': 0,
            'water_L': 0,
            'processes': []
        }
        
        total_mass = sum(m.get('mass_kg', 0) for m in product_spec.get('materials', []))
        
        for process in processes:
            process_name = process.get('process', 'Injection Molding')
            efficiency = process.get('efficiency', 0.85)
            
            process_data = self.db.processes[self.db.processes['process'] == process_name]
            if len(process_data) == 0:
                continue
            
            process_data = process_data.iloc[0]
            
            energy_process = total_mass * process_data['energy_kWh_kg'] / efficiency * 3.6
            carbon_electricity = energy_process * electricity_factor['carbon_gCO2e_kWh'] / 1000
            carbon_process = total_mass * process_data['carbon_kgCO2e_kg']
            carbon_total = carbon_electricity + carbon_process
            
            water = total_mass * process_data['water_L_kg']
            
            results['carbon_kgCO2e'] += carbon_total
            results['energy_MJ'] += energy_process
            results['water_L'] += water
            
            results['processes'].append({
                'process': process_name,
                'carbon_kgCO2e': carbon_total,
                'energy_MJ': energy_process
            })
        
        return results
    
    def _calculate_transport_phase(self, product_spec):
        """Calculate transport phase impacts"""
        transport_legs = product_spec.get('transport_legs', [])
        
        results = {
            'carbon_kgCO2e': 0,
            'energy_MJ': 0,
            'cost_usd': 0,
            'distance_km': 0,
            'legs': []
        }
        
        total_mass = sum(m.get('mass_kg', 0) for m in product_spec.get('materials', []))
        
        for leg in transport_legs:
            mode = leg.get('mode', 'Truck (Diesel)')
            distance = leg.get('distance_km', 1000)
            
            transport_data = self.db.transport[self.db.transport['mode'] == mode]
            if len(transport_data) == 0:
                continue
            
            transport_data = transport_data.iloc[0]
            
            mass_tonne = total_mass / 1000
            carbon = mass_tonne * distance * transport_data['carbon_gCO2e_tonne_km'] / 1000
            energy = mass_tonne * distance * transport_data['energy_MJ_tonne_km']
            cost = mass_tonne * distance * transport_data['cost_usd_tonne_km']
            
            results['carbon_kgCO2e'] += carbon
            results['energy_MJ'] += energy
            results['cost_usd'] += cost
            results['distance_km'] += distance
            
            results['legs'].append({
                'mode': mode,
                'distance_km': distance,
                'carbon_kgCO2e': carbon,
                'energy_MJ': energy
            })
        
        return results
    
    def _calculate_use_phase(self, product_spec):
        """Calculate use phase impacts"""
        lifetime_years = product_spec.get('lifetime_years', 1)
        use_scenarios = product_spec.get('use_scenarios', [])
        
        results = {
            'carbon_kgCO2e': 0,
            'energy_MJ': 0,
            'water_L': 0,
            'scenarios': []
        }
        
        for scenario in use_scenarios:
            scenario_type = scenario.get('type', 'washing')
            frequency = scenario.get('frequency_per_year', 52)
            energy_per_use = scenario.get('energy_kWh_per_use', 0)
            water_per_use = scenario.get('water_L_per_use', 0)
            
            total_uses = frequency * lifetime_years
            energy_total = total_uses * energy_per_use * 3.6
            water_total = total_uses * water_per_use
            carbon_total = total_uses * energy_per_use * 0.475
            
            results['carbon_kgCO2e'] += carbon_total
            results['energy_MJ'] += energy_total
            results['water_L'] += water_total
            
            results['scenarios'].append({
                'type': scenario_type,
                'total_uses': total_uses,
                'carbon_kgCO2e': carbon_total,
                'energy_MJ': energy_total,
                'water_L': water_total
            })
        
        return results
    
    def _calculate_eol_phase(self, product_spec):
        """Calculate end-of-life phase impacts"""
        materials = product_spec.get('materials', [])
        recycling_rate = product_spec.get('recycling_rate', 0.7)
        incineration_rate = product_spec.get('incineration_rate', 0.2)
        landfill_rate = 1 - recycling_rate - incineration_rate
        
        total_mass = sum(m.get('mass_kg', 0) for m in materials)
        
        # Recycling benefits (negative = credit)
        recycling_energy = -total_mass * recycling_rate * 5
        recycling_carbon = -total_mass * recycling_rate * 1
        
        # Incineration with energy recovery
        incineration_energy = total_mass * incineration_rate * 10
        incineration_carbon = total_mass * incineration_rate * 0.5
        
        # Landfill impacts
        landfill_carbon = total_mass * landfill_rate * 0.1
        
        return {
            'carbon_kgCO2e': recycling_carbon + incineration_carbon + landfill_carbon,
            'energy_MJ': recycling_energy + incineration_energy,
            'material_recovery_potential_MJ': total_mass * 20,
            'recycling_kg': total_mass * recycling_rate,
            'waste_kg': total_mass * (incineration_rate + landfill_rate)
        }
    
    def _monte_carlo_analysis(self, product_spec, n_iterations=1000):
        """Perform Monte Carlo uncertainty analysis"""
        np.random.seed(42)
        
        carbon_results = []
        
        for _ in range(n_iterations):
            carbon_total = 0
            
            # Material uncertainty
            materials = product_spec.get('materials', [])
            for mat in materials:
                material_id = mat.get('material_id', 'PP')
                mass = mat.get('mass_kg', 0)
                
                material_data = self.db.materials[self.db.materials['id'] == material_id]
                if len(material_data) == 0:
                    continue
                
                material_data = material_data.iloc[0]
                carbon_mean = material_data['carbon_kgCO2e_kg']
                carbon_std = material_data.get('carbon_std', carbon_mean * 0.1)
                
                carbon_sample = np.random.normal(carbon_mean, carbon_std)
                carbon_total += mass * carbon_sample
            
            carbon_results.append(carbon_total)
        
        return {
            'carbon_mean': np.mean(carbon_results),
            'carbon_std': np.std(carbon_results),
            'carbon_95ci': [np.percentile(carbon_results, 2.5), 
                           np.percentile(carbon_results, 97.5)],
            'iterations': n_iterations
        }
    
    def _calculate_circularity(self, product_spec):
        """Calculate circular economy metrics"""
        materials = product_spec.get('materials', [])
        lifetime = product_spec.get('lifetime_years', 1)
        
        total_mass = sum(m.get('mass_kg', 0) for m in materials)
        
        if total_mass == 0:
            return {
                'material_circularity_indicator': 0,
                'recycled_content_weighted': 0,
                'recyclability_weighted': 0,
                'circularity_class': 'Linear'
            }
        
        recycled_content = sum(m.get('recycled_content', 0) * m.get('mass_kg', 0) 
                              for m in materials) / total_mass
        
        recyclability = 0
        for mat in materials:
            material_id = mat.get('material_id', 'PP')
            mass = mat.get('mass_kg', 0)
            
            material_data = self.db.materials[self.db.materials['id'] == material_id]
            if len(material_data) > 0:
                recyclability += material_data.iloc[0]['recyclability'] * mass
        
        recyclability_weighted = recyclability / total_mass
        lifetime_score = min(lifetime / 10, 1)
        
        mci = (recycled_content * 0.4 + recyclability_weighted * 0.3 + lifetime_score * 0.3)
        
        if mci >= 0.8:
            circularity_class = "Highly Circular"
        elif mci >= 0.6:
            circularity_class = "Moderately Circular"
        elif mci >= 0.4:
            circularity_class = "Transitional"
        else:
            circularity_class = "Linear"
        
        return {
            'material_circularity_indicator': mci,
            'recycled_content_weighted': recycled_content,
            'recyclability_weighted': recyclability_weighted,
            'lifetime_score': lifetime_score,
            'circularity_class': circularity_class
        }
    
    def _calculate_totals(self, *phases):
        """Calculate total impacts across all phases"""
        totals = {
            'carbon_kgCO2e': sum(p.get('carbon_kgCO2e', 0) for p in phases),
            'energy_MJ': sum(p.get('energy_MJ', 0) for p in phases),
            'water_L': sum(p.get('water_L', 0) for p in phases),
            'cost_usd': sum(p.get('cost_usd', 0) for p in phases if 'cost_usd' in p)
        }
        
        total_mass = phases[0].get('mass_kg', 0) if phases else 0
        if total_mass > 0:
            totals['carbon_per_kg'] = totals['carbon_kgCO2e'] / total_mass
            totals['energy_per_kg'] = totals['energy_MJ'] / total_mass
        
        return totals
    
    def _identify_hotspots(self, *phases):
        """Identify environmental hotspots"""
        hotspots = []
        phase_names = ['material', 'manufacturing', 'transport', 'use', 'end_of_life']
        
        for i, phase in enumerate(phases):
            carbon = phase.get('carbon_kgCO2e', 0)
            if carbon > 0:
                hotspots.append({
                    'phase': phase_names[i],
                    'carbon_kgCO2e': carbon,
                    'percentage': 0
                })
        
        total_carbon = sum(h['carbon_kgCO2e'] for h in hotspots)
        for h in hotspots:
            h['percentage'] = (h['carbon_kgCO2e'] / total_carbon * 100) if total_carbon > 0 else 0
        
        return sorted(hotspots, key=lambda x: x['percentage'], reverse=True)[:3]
    
    def _calculate_improvement_potential(self, product_spec):
        """Calculate improvement potential"""
        materials = product_spec.get('materials', [])
        
        current_carbon = 0
        best_carbon = 0
        
        for mat in materials:
            material_id = mat.get('material_id', 'PP')
            mass = mat.get('mass_kg', 0)
            
            material_data = self.db.materials[self.db.materials['id'] == material_id]
            if len(material_data) == 0:
                continue
            
            current = material_data.iloc[0]
            current_carbon += mass * current['carbon_kgCO2e_kg']
            
            # Find best alternative
            alternatives = self.db.materials[
                (self.db.materials['strength_MPa'] >= current['strength_MPa'] * 0.8) &
                (self.db.materials['id'] != material_id)
            ]
            
            if len(alternatives) > 0:
                best = alternatives.sort_values('carbon_kgCO2e_kg').iloc[0]
                best_carbon += mass * best['carbon_kgCO2e_kg']
            else:
                best_carbon += mass * current['carbon_kgCO2e_kg']
        
        reduction_potential = ((current_carbon - best_carbon) / current_carbon * 100) if current_carbon > 0 else 0
        
        return {
            'current_carbon_kgCO2e': current_carbon,
            'best_potential_carbon_kgCO2e': best_carbon,
            'reduction_potential_%': reduction_potential,
            'recommendations': self._generate_recommendations(product_spec)
        }
    
    def _generate_recommendations(self, product_spec):
        """Generate improvement recommendations"""
        recommendations = []
        
        # Material recommendations
        materials = product_spec.get('materials', [])
        for mat in materials:
            if mat.get('recycled_content', 0) < 0.3:
                recommendations.append(f"Increase recycled content in {mat.get('material_id')} to at least 30%")
        
        # Manufacturing recommendations
        if product_spec.get('manufacturing_region') in ['China', 'Asia']:
            recommendations.append("Consider manufacturing in regions with cleaner electricity grid")
        
        # Transport recommendations
        transport_legs = product_spec.get('transport_legs', [])
        for leg in transport_legs:
            if leg.get('mode') == 'Air Freight':
                recommendations.append("Avoid air freight for high-volume products")
        
        return recommendations[:5]

# ============================================================================
# ADVANCED VISUALIZATION ENGINE
# ============================================================================
class AdvancedVisualizer:
    """Advanced visualization engine for LCA results"""
    
    @staticmethod
    def create_sankey_diagram(lca_results):
        """Create professional Sankey diagram"""
        phases = lca_results['phases']
        
        # Define nodes
        labels = []
        source = []
        target = []
        value = []
        
        phase_names = ['Material', 'Manufacturing', 'Transport', 'Use', 'End-of-Life']
        impact_names = ['Carbon', 'Energy']
        
        node_index = 0
        node_mapping = {}
        
        # Add phase nodes
        for i, phase_name in enumerate(phase_names):
            for impact in impact_names:
                node_label = f"{phase_name}<br>{impact}"
                node_mapping[(phase_name, impact)] = node_index
                labels.append(node_label)
                node_index += 1
        
        # Add total nodes
        for impact in impact_names:
            node_label = f"Total<br>{impact}"
            node_mapping[('Total', impact)] = node_index
            labels.append(node_label)
            node_index += 1
        
        # Create flows (simplified for example)
        # Material Carbon to Total Carbon
        source.append(node_mapping[('Material', 'Carbon')])
        target.append(node_mapping[('Total', 'Carbon')])
        value.append(phases['material'].get('carbon_kgCO2e', 0))
        
        # Manufacturing Carbon to Total Carbon
        source.append(node_mapping[('Manufacturing', 'Carbon')])
        target.append(node_mapping[('Total', 'Carbon')])
        value.append(phases['manufacturing'].get('carbon_kgCO2e', 0))
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"] * 2
            ),
            link=dict(
                source=source,
                target=target,
                value=value
            )
        )])
        
        fig.update_layout(
            title_text="Environmental Impact Flow",
            font_size=12,
            height=500
        )
        
        return fig
    
    @staticmethod
    def create_phase_comparison_chart(lca_results_list):
        """Create comparison chart for multiple products"""
        products = []
        material_impacts = []
        manufacturing_impacts = []
        transport_impacts = []
        use_impacts = []
        eol_impacts = []
        
        for result in lca_results_list:
            products.append(result['product_name'])
            phases = result['phases']
            
            material_impacts.append(phases['material'].get('carbon_kgCO2e', 0))
            manufacturing_impacts.append(phases['manufacturing'].get('carbon_kgCO2e', 0))
            transport_impacts.append(phases['transport'].get('carbon_kgCO2e', 0))
            use_impacts.append(phases['use'].get('carbon_kgCO2e', 0))
            eol_impacts.append(phases['end_of_life'].get('carbon_kgCO2e', 0))
        
        fig = go.Figure(data=[
            go.Bar(name='Material', x=products, y=material_impacts, marker_color='#1f77b4'),
            go.Bar(name='Manufacturing', x=products, y=manufacturing_impacts, marker_color='#ff7f0e'),
            go.Bar(name='Transport', x=products, y=transport_impacts, marker_color='#2ca02c'),
            go.Bar(name='Use', x=products, y=use_impacts, marker_color='#d62728'),
            go.Bar(name='End-of-Life', x=products, y=eol_impacts, marker_color='#9467bd')
        ])
        
        fig.update_layout(
            title="Carbon Footprint Comparison by Life Cycle Phase",
            xaxis_title="Product",
            yaxis_title="Carbon Footprint (kg CO₂e)",
            barmode='stack',
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    @staticmethod
    def create_hotspot_chart(lca_results):
        """Create hotspot identification chart"""
        hotspots = lca_results.get('hotspots', [])
        
        phases = [h['phase'].title() for h in hotspots]
        percentages = [h['percentage'] for h in hotspots]
        
        fig = go.Figure(data=[
            go.Bar(
                x=phases,
                y=percentages,
                marker_color=['#ef4444', '#f97316', '#f59e0b'][:len(phases)],
                text=[f"{p:.1f}%" for p in percentages],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title="Environmental Hotspots",
            xaxis_title="Life Cycle Phase",
            yaxis_title="Contribution to Total Impact (%)",
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_circularity_radar(circularity_metrics):
        """Create circularity radar chart"""
        categories = ['Material Circularity', 'Recycled Content', 'Recyclability', 'Lifetime']
        values = [
            circularity_metrics.get('material_circularity_indicator', 0) * 100,
            circularity_metrics.get('recycled_content_weighted', 0) * 100,
            circularity_metrics.get('recyclability_weighted', 0) * 100,
            circularity_metrics.get('lifetime_score', 0) * 100
        ]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            line=dict(color='#10b981', width=2)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title="Circularity Assessment",
            height=400,
            showlegend=False
        )
        
        return fig

# ============================================================================
# UI COMPONENTS
# ============================================================================
def display_header():
    """Display professional header"""
    st.markdown("""
    <div class="pro-header">
        <h1 style="color: white; margin: 0; font-size: 2.5rem;">
            🌍 EcoLens Pro
        </h1>
        <p style="color: rgba(255, 255, 255, 0.9); margin: 0.5rem 0 0 0;">
            Advanced Life Cycle Assessment Platform
        </p>
    </div>
    """, unsafe_allow_html=True)

def display_sidebar():
    """Display sidebar navigation"""
    with st.sidebar:
        # User info
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="width: 60px; height: 60px; background: linear-gradient(135deg, var(--primary), var(--secondary)); 
                      border-radius: 50%; margin: 0 auto 1rem auto; display: flex; align-items: center; justify-content: center;">
                <span style="color: white; font-size: 1.5rem;">👤</span>
            </div>
            <h4 style="color: var(--dark); margin: 0;">Professional User</h4>
            <p style="color: var(--gray); font-size: 0.8rem; margin: 0.25rem 0;">
                {organization}
            </p>
        </div>
        """.format(organization=st.session_state.user['organization']), unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation
        st.markdown("### 🎯 Navigation")
        
        view_options = {
            "📊 Dashboard": "dashboard",
            "🚀 Quick Assessment": "quick_assessment",
            "🔬 Detailed Analysis": "detailed_analysis",
            "📈 Compare Products": "comparison",
            "📊 Analytics": "analytics",
            "🔍 Database": "database",
            "⚙️ Settings": "settings"
        }
        
        selected_view = st.radio(
            "Select View",
            list(view_options.keys()),
            label_visibility="collapsed"
        )
        
        st.session_state.current_view = view_options[selected_view]
        
        st.divider()
        
        # Quick stats
        st.markdown("### 📈 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Products", len(st.session_state.products))
        with col2:
            st.metric("Projects", 1)
        
        st.divider()
        
        # Quick actions
        if st.button("🆕 New Analysis", use_container_width=True):
            st.session_state.current_view = "quick_assessment"
            st.rerun()
        
        if st.button("📤 Export Data", use_container_width=True):
            st.success("Export functionality coming soon!")

# ============================================================================
# MAIN VIEWS
# ============================================================================
def display_dashboard():
    """Display main dashboard"""
    st.title("📊 Dashboard")
    
    # Welcome message
    st.markdown("""
    <div class="dashboard-card">
        <h3 style="color: var(--primary); margin-bottom: 1rem;">Welcome to EcoLens Pro</h3>
        <p style="color: var(--gray);">
        Advanced Life Cycle Assessment platform for sustainable engineering decisions.
        Start a new analysis or explore existing projects.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Products Analyzed</div>
            <div class="metric-value">{}</div>
        </div>
        """.format(len(st.session_state.products)), unsafe_allow_html=True)
    
    with col2:
        avg_carbon = np.mean([p['totals']['carbon_kgCO2e'] 
                             for p in st.session_state.products]) if st.session_state.products else 0
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Avg Carbon</div>
            <div class="metric-value">{:.1f}</div>
            <div style="color: var(--gray); font-size: 0.9rem;">kg CO₂e</div>
        </div>
        """.format(avg_carbon), unsafe_allow_html=True)
    
    with col3:
        avg_circularity = np.mean([p['circularity_metrics']['material_circularity_indicator']
                                  for p in st.session_state.products]) if st.session_state.products else 0
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Avg Circularity</div>
            <div class="metric-value">{:.2f}</div>
        </div>
        """.format(avg_circularity), unsafe_allow_html=True)
    
    with col4:
        total_reduction = sum([p['improvement_potential']['reduction_potential_%']
                              for p in st.session_state.products]) if st.session_state.products else 0
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Improvement</div>
            <div class="metric-value">{:.0f}%</div>
            <div style="color: var(--gray); font-size: 0.9rem;">Potential</div>
        </div>
        """.format(total_reduction / max(len(st.session_state.products), 1)), unsafe_allow_html=True)
    
    # Recent analyses
    if st.session_state.products:
        st.subheader("📋 Recent Analyses")
        
        recent_df = pd.DataFrame([{
            'Product': p['product_name'],
            'Carbon (kg)': p['totals']['carbon_kgCO2e'],
            'Energy (MJ)': p['totals']['energy_MJ'],
            'Circularity': f"{p['circularity_metrics']['material_circularity_indicator']:.2f}",
            'Date': p['timestamp'][:10]
        } for p in st.session_state.products[-5:]])
        
        st.dataframe(recent_df, use_container_width=True)
    
    # Quick start cards
    st.subheader("🚀 Quick Start")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.markdown("""
            <div class="dashboard-card" style="text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">⚡</div>
                <h3 style="color: var(--primary); margin-bottom: 0.5rem;">Quick Assessment</h3>
                <p style="color: var(--gray); font-size: 0.9rem;">
                Get instant LCA results for common products
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Start Quick Assessment", key="quick_start", use_container_width=True):
                st.session_state.current_view = "quick_assessment"
                st.rerun()
    
    with col2:
        with st.container():
            st.markdown("""
            <div class="dashboard-card" style="text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔬</div>
                <h3 style="color: var(--primary); margin-bottom: 0.5rem;">Detailed Analysis</h3>
                <p style="color: var(--gray); font-size: 0.9rem;">
                Comprehensive LCA with advanced customization
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Start Detailed Analysis", key="detailed_start", use_container_width=True):
                st.session_state.current_view = "detailed_analysis"
                st.rerun()
    
    with col3:
        with st.container():
            st.markdown("""
            <div class="dashboard-card" style="text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📈</div>
                <h3 style="color: var(--primary); margin-bottom: 0.5rem;">Compare Products</h3>
                <p style="color: var(--gray); font-size: 0.9rem;">
                Side-by-side comparison of design alternatives
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Start Comparison", key="compare_start", use_container_width=True):
                st.session_state.current_view = "comparison"
                st.rerun()

def display_quick_assessment():
    """Display quick assessment workflow"""
    st.title("🚀 Quick Product Assessment")
    
    # Step indicator
    steps = ["Select Product", "Configure", "Results"]
    current_step = st.session_state.get('workflow_step', 0)
    
    cols = st.columns(3)
    for i, step in enumerate(steps):
        with cols[i]:
            status = "🔵" if i == current_step else "✅" if i < current_step else "⚪"
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{status}</div>
                <div style="color: {'var(--primary)' if i == current_step else 'var(--gray)'}; 
                          font-weight: {'bold' if i == current_step else 'normal'}">
                    {step}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    if current_step == 0:
        display_quick_step1()
    elif current_step == 1:
        display_quick_step2()
    elif current_step == 2:
        display_quick_step3()

def display_quick_step1():
    """Step 1: Product selection"""
    st.subheader("1. Select Your Product Type")
    
    product_type = st.selectbox(
        "Choose from common products:",
        ["Water Bottle (500ml)", "Packaging Box", "Electronics Case", 
         "Furniture Component", "Custom Product"]
    )
    
    if product_type == "Water Bottle (500ml)":
        st.info("💡 **Typical specifications:** 150g Polypropylene, Injection molding, 2-year lifespan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.current_view = "dashboard"
            st.session_state.workflow_step = 0
            st.rerun()
    
    with col2:
        if st.button("Next: Configure →", type="primary", use_container_width=True):
            st.session_state.workflow_step = 1
            st.session_state.quick_product_type = product_type
            st.rerun()

def display_quick_step2():
    """Step 2: Configuration"""
    st.subheader("2. Configure Your Product")
    
    with st.form("quick_config_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            material = st.selectbox(
                "Primary Material",
                ["Polypropylene (PP)", "Polyethylene Terephthalate (PET)", 
                 "Aluminum", "Stainless Steel", "Glass"]
            )
            
            mass_kg = st.number_input(
                "Product Mass (kg)",
                min_value=0.01,
                max_value=10.0,
                value=0.15,
                step=0.01
            )
        
        with col2:
            manufacturing_region = st.selectbox(
                "Manufacturing Region",
                ["Asia (China)", "Europe", "North America", "Global Average"]
            )
            
            lifetime_years = st.slider(
                "Expected Lifetime (years)",
                1, 10, 2
            )
        
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

def display_quick_step3():
    """Step 3: Results"""
    st.subheader("3. Analysis Results")
    
    # Get configuration
    product_type = st.session_state.get('quick_product_type', 'Custom Product')
    config = st.session_state.get('quick_config', {})
    
    # Create product specification
    material_id_map = {
        "Polypropylene (PP)": "PP",
        "Polyethylene Terephthalate (PET)": "PET",
        "Aluminum": "AL6061",
        "Stainless Steel": "SUS304",
        "Glass": "GLASS"
    }
    
    material_id = material_id_map.get(config.get('material', "Polypropylene (PP)"), "PP")
    
    product_spec = {
        'product_name': product_type,
        'materials': [{
            'material_id': material_id,
            'mass_kg': config.get('mass_kg', 0.15),
            'recycled_content': 0.0
        }],
        'manufacturing_region': config.get('region', 'Global Average'),
        'manufacturing_processes': [{'process': 'Injection Molding', 'efficiency': 0.85}],
        'transport_legs': [{'mode': 'Truck (Diesel)', 'distance_km': 1000}],
        'lifetime_years': config.get('lifetime', 2),
        'use_scenarios': [{
            'type': 'washing',
            'frequency_per_year': 52,
            'energy_kWh_per_use': 0.1,
            'water_L_per_use': 2.0
        }],
        'recycling_rate': 0.7,
        'incineration_rate': 0.2
    }
    
    # Calculate LCA
    database = AdvancedLCADatabase()
    calculator = AdvancedLCAEngine(database)
    visualizer = AdvancedVisualizer()
    
    with st.spinner("🔄 Running advanced LCA analysis..."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        
        lca_results = calculator.calculate_product_lca(product_spec)
    
    st.success("✅ Analysis Complete!")
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Carbon Footprint",
            f"{lca_results['totals']['carbon_kgCO2e']:.1f} kg CO₂e"
        )
    
    with col2:
        st.metric(
            "Energy Use", 
            f"{lca_results['totals']['energy_MJ']:.1f} MJ"
        )
    
    with col3:
        circularity = lca_results['circularity_metrics']
        st.metric(
            "Circularity Score",
            f"{circularity['material_circularity_indicator']:.2f}",
            circularity['circularity_class']
        )
    
    with col4:
        improvement = lca_results['improvement_potential']
        st.metric(
            "Improvement Potential",
            f"{improvement['reduction_potential_%']:.1f}%"
        )
    
    # Visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Impact Flow", "📈 Phase Breakdown", "🎯 Hotspots", "🔄 Circularity"])
    
    with tab1:
        fig = visualizer.create_sankey_diagram(lca_results)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        phases = lca_results['phases']
        phase_data = {
            'Phase': ['Material', 'Manufacturing', 'Transport', 'Use', 'End-of-Life'],
            'Carbon (kg CO₂e)': [
                phases['material'].get('carbon_kgCO2e', 0),
                phases['manufacturing'].get('carbon_kgCO2e', 0),
                phases['transport'].get('carbon_kgCO2e', 0),
                phases['use'].get('carbon_kgCO2e', 0),
                phases['end_of_life'].get('carbon_kgCO2e', 0)
            ]
        }
        
        df = pd.DataFrame(phase_data)
        fig = px.bar(df, x='Phase', y='Carbon (kg CO₂e)', 
                     title='Carbon Footprint by Life Cycle Phase',
                     color='Phase')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        fig = visualizer.create_hotspot_chart(lca_results)
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.subheader("💡 Improvement Recommendations")
        for rec in lca_results['improvement_potential']['recommendations']:
            st.info(f"• {rec}")
    
    with tab4:
        fig = visualizer.create_circularity_radar(lca_results['circularity_metrics'])
        st.plotly_chart(fig, use_container_width=True)
    
    # Material suggestions
    st.subheader("🔬 Material Substitution Analysis")
    
    for mat in lca_results['phases']['material']['materials_detail']:
        suggestions = database.get_material_suggestions(mat['material'], target_reduction=20)
        
        if suggestions:
            with st.expander(f"Alternatives for {mat['material']}"):
                sug_df = pd.DataFrame(suggestions)
                st.dataframe(sug_df[['material', 'carbon_reduction_%', 'carbon_kgCO2e_kg']], 
                            use_container_width=True)
    
    # Next steps
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Compare with Alternatives", use_container_width=True):
            st.session_state.current_view = "comparison"
            st.session_state.workflow_step = 0
            st.rerun()
    
    with col2:
        if st.button("📄 Generate Report", use_container_width=True):
            st.success("Report generation started!")
    
    with col3:
        if st.button("🔄 New Analysis", type="primary", use_container_width=True):
            # Save current analysis
            st.session_state.products.append(lca_results)
            st.session_state.current_view = "dashboard"
            st.session_state.workflow_step = 0
            st.rerun()

def display_detailed_analysis():
    """Display detailed analysis workflow"""
    st.title("🔬 Detailed Product Analysis")
    
    st.info("""
    **Advanced LCA Analysis Features:**
    - Multiple materials and processes
    - Complex transport logistics
    - Detailed use phase scenarios
    - Advanced uncertainty modeling
    """)
    
    with st.form("detailed_analysis_form"):
        st.subheader("📦 Product Definition")
        
        col1, col2 = st.columns(2)
        with col1:
            product_name = st.text_input("Product Name", "Advanced Product")
            product_id = st.text_input("Product ID", f"PROD-{str(uuid.uuid4())[:6]}")
        
        with col2:
            description = st.text_area("Description", "Detailed product description")
        
        st.subheader("📦 Materials")
        
        n_materials = st.number_input("Number of Materials", 1, 5, 1)
        materials = []
        
        for i in range(n_materials):
            with st.expander(f"Material {i+1}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    material_id = st.selectbox(
                        f"Material Type {i+1}",
                        ["PP", "PET", "HDPE", "AL6061", "SUS304", "GLASS", "R_PET", "R_PP"],
                        key=f"mat_type_{i}"
                    )
                
                with col2:
                    mass_kg = st.number_input(
                        f"Mass (kg) {i+1}",
                        min_value=0.01,
                        max_value=10.0,
                        value=0.15,
                        step=0.01,
                        key=f"mass_{i}"
                    )
                    
                    recycled_content = st.slider(
                        f"Recycled Content {i+1}",
                        0.0, 1.0, 0.0, 0.05,
                        key=f"recycled_{i}"
                    )
                
                materials.append({
                    'material_id': material_id,
                    'mass_kg': mass_kg,
                    'recycled_content': recycled_content
                })
        
        st.subheader("🏭 Manufacturing")
        
        manufacturing_region = st.selectbox(
            "Manufacturing Region",
            ["Europe", "North America", "Asia", "China", "Global Average"]
        )
        
        processes = st.multiselect(
            "Manufacturing Processes",
            ["Injection Molding", "Blow Molding", "Assembly", "Surface Treatment"],
            default=["Injection Molding", "Assembly"]
        )
        
        manufacturing_processes = []
        for proc in processes:
            manufacturing_processes.append({
                'process': proc,
                'efficiency': st.slider(
                    f"Efficiency for {proc}",
                    0.5, 1.0, 0.85, 0.05,
                    key=f"eff_{proc}"
                )
            })
        
        st.subheader("🚚 Transportation")
        
        n_legs = st.number_input("Number of Transport Legs", 0, 5, 1)
        transport_legs = []
        
        for i in range(n_legs):
            with st.expander(f"Transport Leg {i+1}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    mode = st.selectbox(
                        f"Mode {i+1}",
                        ["Truck (Diesel)", "Truck (Electric)", "Rail", "Ship", "Air Freight"],
                        key=f"mode_{i}"
                    )
                
                with col2:
                    distance = st.number_input(
                        f"Distance (km) {i+1}",
                        0, 10000, 1000,
                        key=f"dist_{i}"
                    )
                
                transport_legs.append({
                    'mode': mode,
                    'distance_km': distance
                })
        
        st.subheader("🔄 Use Phase")
        
        lifetime_years = st.slider("Lifetime (years)", 1, 20, 5)
        
        use_scenarios = []
        if st.checkbox("Include use phase scenarios"):
            n_scenarios = st.number_input("Number of Use Scenarios", 0, 3, 1)
            
            for i in range(n_scenarios):
                with st.expander(f"Use Scenario {i+1}"):
                    scenario_type = st.selectbox(
                        f"Scenario Type {i+1}",
                        ["Washing", "Charging", "Operation", "Maintenance"],
                        key=f"scenario_type_{i}"
                    )
                    
                    frequency = st.number_input(
                        f"Frequency per year {i+1}",
                        0, 365, 52,
                        key=f"freq_{i}"
                    )
                    
                    energy_per_use = st.number_input(
                        f"Energy per use (kWh) {i+1}",
                        0.0, 10.0, 0.1,
                        key=f"energy_{i}"
                    )
                    
                    use_scenarios.append({
                        'type': scenario_type.lower(),
                        'frequency_per_year': frequency,
                        'energy_kWh_per_use': energy_per_use
                    })
        
        st.subheader("♻️ End-of-Life")
        
        recycling_rate = st.slider("Recycling Rate", 0.0, 1.0, 0.7, 0.05)
        incineration_rate = st.slider("Incineration Rate", 0.0, 1.0, 0.2, 0.05)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.form_submit_button("Cancel", use_container_width=True):
                st.session_state.current_view = "dashboard"
                st.rerun()
        
        with col2:
            if st.form_submit_button("Run Advanced Analysis", type="primary", use_container_width=True):
                # Create product specification
                product_spec = {
                    'product_id': product_id,
                    'product_name': product_name,
                    'description': description,
                    'materials': materials,
                    'manufacturing_region': manufacturing_region,
                    'manufacturing_processes': manufacturing_processes,
                    'transport_legs': transport_legs,
                    'lifetime_years': lifetime_years,
                    'use_scenarios': use_scenarios,
                    'recycling_rate': recycling_rate,
                    'incineration_rate': incineration_rate
                }
                
                # Calculate LCA
                database = AdvancedLCADatabase()
                calculator = AdvancedLCAEngine(database)
                
                with st.spinner("Running comprehensive LCA analysis..."):
                    lca_results = calculator.calculate_product_lca(product_spec)
                
                # Save results
                st.session_state.products.append(lca_results)
                
                # Display success
                st.success("✅ Analysis complete! Results saved.")
                
                # Show quick summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Carbon", f"{lca_results['totals']['carbon_kgCO2e']:.1f} kg")
                with col2:
                    st.metric("Energy", f"{lca_results['totals']['energy_MJ']:.0f} MJ")
                with col3:
                    st.metric("Circularity", f"{lca_results['circularity_metrics']['material_circularity_indicator']:.2f}")
                
                if st.button("View Detailed Results"):
                    display_lca_results(lca_results)

def display_lca_results(lca_results):
    """Display detailed LCA results"""
    st.subheader("📊 Detailed Results")
    
    visualizer = AdvancedVisualizer()
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Overview", "🌊 Impact Flow", "🎯 Hotspots", 
        "🔄 Circularity", "🎲 Uncertainty"
    ])
    
    with tab1:
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Carbon",
                f"{lca_results['totals']['carbon_kgCO2e']:.1f} kg CO₂e",
                f"{lca_results['totals'].get('carbon_per_kg', 0):.1f} kg/kg"
            )
        
        with col2:
            st.metric(
                "Total Energy",
                f"{lca_results['totals']['energy_MJ']:.0f} MJ",
                f"{lca_results['totals'].get('energy_per_kg', 0):.0f} MJ/kg"
            )
        
        with col3:
            circularity = lca_results['circularity_metrics']
            st.metric(
                "Circularity",
                f"{circularity['material_circularity_indicator']:.2f}",
                circularity['circularity_class']
            )
        
        with col4:
            uncertainty = lca_results['uncertainty']
            st.metric(
                "Uncertainty",
                f"±{uncertainty['carbon_std']:.1f} kg",
                f"{uncertainty['carbon_std']/uncertainty['carbon_mean']*100:.1f}% CV"
            )
    
    with tab2:
        fig = visualizer.create_sankey_diagram(lca_results)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        fig = visualizer.create_hotspot_chart(lca_results)
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.subheader("💡 Improvement Recommendations")
        for rec in lca_results['improvement_potential']['recommendations']:
            st.info(f"• {rec}")
    
    with tab4:
        fig = visualizer.create_circularity_radar(lca_results['circularity_metrics'])
        st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        uncertainty = lca_results['uncertainty']
        
        # Create uncertainty visualization
        fig = go.Figure()
        
        # Add box plot
        fig.add_trace(go.Box(
            y=[uncertainty['carbon_mean']],
            name='Carbon Footprint',
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8,
            marker_color='#3b82f6'
        ))
        
        fig.update_layout(
            title=f"Uncertainty Analysis (95% CI: {uncertainty['carbon_95ci'][0]:.1f} - {uncertainty['carbon_95ci'][1]:.1f} kg CO₂e)",
            yaxis_title="Carbon Footprint (kg CO₂e)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

def display_comparison():
    """Display product comparison view"""
    st.title("📈 Product Comparison")
    
    if len(st.session_state.products) < 2:
        st.warning("You need at least 2 products to compare. Please run some analyses first.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Run Quick Assessment", use_container_width=True):
                st.session_state.current_view = "quick_assessment"
                st.rerun()
        with col2:
            if st.button("🔬 Run Detailed Analysis", use_container_width=True):
                st.session_state.current_view = "detailed_analysis"
                st.rerun()
        
        return
    
    # Select products to compare
    product_names = [p['product_name'] for p in st.session_state.products]
    selected_products = st.multiselect(
        "Select products to compare",
        product_names,
        default=product_names[-2:] if len(product_names) >= 2 else product_names
    )
    
    if len(selected_products) < 2:
        st.info("Please select at least 2 products to compare")
        return
    
    # Get selected product data
    selected_data = [p for p in st.session_state.products 
                    if p['product_name'] in selected_products]
    
    visualizer = AdvancedVisualizer()
    
    # Create comparison chart
    fig = visualizer.create_phase_comparison_chart(selected_data)
    st.plotly_chart(fig, use_container_width=True)
    
    # Comparison table
    st.subheader("📋 Detailed Comparison")
    
    comparison_data = []
    for product in selected_data:
        comparison_data.append({
            'Product': product['product_name'],
            'Total Carbon (kg)': product['totals']['carbon_kgCO2e'],
            'Total Energy (MJ)': product['totals']['energy_MJ'],
            'Circularity Score': product['circularity_metrics']['material_circularity_indicator'],
            'Circularity Class': product['circularity_metrics']['circularity_class'],
            'Improvement Potential %': product['improvement_potential']['reduction_potential_%']
        })
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True)
    
    # Statistical analysis
    st.subheader("📊 Statistical Analysis")
    
    carbon_values = [p['totals']['carbon_kgCO2e'] for p in selected_data]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Mean Carbon", f"{np.mean(carbon_values):.1f} kg")
    
    with col2:
        st.metric("Standard Deviation", f"{np.std(carbon_values):.1f} kg")
    
    with col3:
        st.metric("Range", f"{max(carbon_values) - min(carbon_values):.1f} kg")
    
    # Best and worst performers
    st.subheader("🏆 Performance Summary")
    
    best_product = min(selected_data, key=lambda x: x['totals']['carbon_kgCO2e'])
    worst_product = max(selected_data, key=lambda x: x['totals']['carbon_kgCO2e'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <h3 style="color: var(--accent); margin-bottom: 0.5rem;">🥇 Best Performer</h3>
            <p style="font-size: 1.2rem; font-weight: bold;">{}</p>
            <p style="color: var(--gray);">Carbon: {:.1f} kg CO₂e</p>
            <p style="color: var(--gray);">Circularity: {:.2f}</p>
        </div>
        """.format(
            best_product['product_name'],
            best_product['totals']['carbon_kgCO2e'],
            best_product['circularity_metrics']['material_circularity_indicator']
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <h3 style="color: var(--danger); margin-bottom: 0.5rem;">⚠️ Improvement Needed</h3>
            <p style="font-size: 1.2rem; font-weight: bold;">{}</p>
            <p style="color: var(--gray);">Carbon: {:.1f} kg CO₂e</p>
            <p style="color: var(--gray);">Improvement Potential: {:.1f}%</p>
        </div>
        """.format(
            worst_product['product_name'],
            worst_product['totals']['carbon_kgCO2e'],
            worst_product['improvement_potential']['reduction_potential_%']
        ), unsafe_allow_html=True)

def display_analytics():
    """Display analytics dashboard"""
    st.title("📊 Advanced Analytics")
    
    if len(st.session_state.products) == 0:
        st.info("No data available. Please run some analyses first.")
        return
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🔗 Correlations", "🎯 Insights", "📋 Summary"])
    
    with tab1:
        # Trend analysis
        st.subheader("📈 Carbon Footprint Trends")
        
        if len(st.session_state.products) >= 3:
            dates = [p['timestamp'][:10] for p in st.session_state.products]
            carbon_values = [p['totals']['carbon_kgCO2e'] for p in st.session_state.products]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates, y=carbon_values,
                mode='lines+markers',
                name='Carbon Footprint',
                line=dict(color='#3b82f6', width=3),
                marker=dict(size=8)
            ))
            
            # Add moving average
            window = min(3, len(carbon_values))
            moving_avg = pd.Series(carbon_values).rolling(window=window).mean()
            fig.add_trace(go.Scatter(
                x=dates, y=moving_avg,
                mode='lines',
                name=f'{window}-Point Moving Average',
                line=dict(color='#ef4444', width=2, dash='dash')
            ))
            
            fig.update_layout(
                title="Carbon Footprint Trend Over Time",
                xaxis_title="Date",
                yaxis_title="Carbon Footprint (kg CO₂e)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 3 analyses for trend analysis")
    
    with tab2:
        # Correlation analysis
        st.subheader("🔗 Parameter Correlations")
        
        if len(st.session_state.products) >= 5:
            # Create correlation matrix
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
                texttemplate='%{text}'
            ))
            
            fig.update_layout(
                title="Parameter Correlation Matrix",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Insights
            st.subheader("💡 Correlation Insights")
            
            if abs(corr_matrix.loc['Mass', 'Carbon']) > 0.7:
                st.info("**Strong correlation between mass and carbon footprint.** Consider lightweight design strategies.")
            
            if corr_matrix.loc['Circularity', 'Carbon'] < -0.5:
                st.info("**Higher circularity correlates with lower carbon footprint.** Focus on circular design principles.")
        else:
            st.info("Need at least 5 analyses for correlation analysis")
    
    with tab3:
        # Insights
        st.subheader("🎯 Key Insights")
        
        if st.session_state.products:
            # Calculate averages
            avg_carbon = np.mean([p['totals']['carbon_kgCO2e'] for p in st.session_state.products])
            avg_circularity = np.mean([p['circularity_metrics']['material_circularity_indicator'] 
                                      for p in st.session_state.products])
            
            # Identify patterns
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="dashboard-card">
                    <h3 style="color: var(--primary); margin-bottom: 1rem;">📊 Overall Performance</h3>
                    <p style="color: var(--gray);">Average Carbon Footprint: <strong>{:.1f} kg CO₂e</strong></p>
                    <p style="color: var(--gray);">Average Circularity: <strong>{:.2f}</strong></p>
                    <p style="color: var(--gray);">Total Analyses: <strong>{}</strong></p>
                </div>
                """.format(avg_carbon, avg_circularity, len(st.session_state.products)), 
                unsafe_allow_html=True)
            
            with col2:
                # Find most common hotspot
                hotspots = []
                for product in st.session_state.products:
                    if product['hotspots']:
                        hotspots.append(product['hotspots'][0]['phase'])
                
                if hotspots:
                    most_common = max(set(hotspots), key=hotspots.count)
                    st.markdown("""
                    <div class="dashboard-card">
                        <h3 style="color: var(--primary); margin-bottom: 1rem;">🎯 Common Hotspot</h3>
                        <p style="color: var(--gray);">Most frequent environmental hotspot:</p>
                        <p style="font-size: 1.2rem; font-weight: bold; color: var(--danger);">{}</p>
                        <p style="color: var(--gray);">Focus improvement efforts here</p>
                    </div>
                    """.format(most_common.title()), unsafe_allow_html=True)
    
    with tab4:
        # Summary statistics
        st.subheader("📋 Summary Statistics")
        
        if st.session_state.products:
            carbon_values = [p['totals']['carbon_kgCO2e'] for p in st.session_state.products]
            energy_values = [p['totals']['energy_MJ'] for p in st.session_state.products]
            circularity_values = [p['circularity_metrics']['material_circularity_indicator'] 
                                 for p in st.session_state.products]
            
            stats_df = pd.DataFrame({
                'Metric': ['Carbon (kg CO₂e)', 'Energy (MJ)', 'Circularity'],
                'Mean': [np.mean(carbon_values), np.mean(energy_values), np.mean(circularity_values)],
                'Std Dev': [np.std(carbon_values), np.std(energy_values), np.std(circularity_values)],
                'Min': [np.min(carbon_values), np.min(energy_values), np.min(circularity_values)],
                'Max': [np.max(carbon_values), np.max(energy_values), np.max(circularity_values)]
            })
            
            st.dataframe(stats_df, use_container_width=True)

def display_database():
    """Display database explorer"""
    st.title("🔍 Database Explorer")
    
    database = AdvancedLCADatabase()
    
    tab1, tab2, tab3, tab4 = st.tabs(["📦 Materials", "🏭 Processes", "🚚 Transport", "🌍 Regional"])
    
    with tab1:
        st.subheader("Material Database")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category_filter = st.multiselect(
                "Filter by Category",
                database.materials['category'].unique(),
                default=database.materials['category'].unique()
            )
        
        with col2:
            carbon_range = st.slider(
                "Carbon Footprint Range (kg CO₂e/kg)",
                float(database.materials['carbon_kgCO2e_kg'].min()),
                float(database.materials['carbon_kgCO2e_kg'].max()),
                (0.0, 10.0)
            )
        
        with col3:
            recyclability_min = st.slider(
                "Minimum Recyclability",
                0.0, 1.0, 0.0, 0.1
            )
        
        # Apply filters
        filtered_df = database.materials[
            (database.materials['category'].isin(category_filter)) &
            (database.materials['carbon_kgCO2e_kg'] >= carbon_range[0]) &
            (database.materials['carbon_kgCO2e_kg'] <= carbon_range[1]) &
            (database.materials['recyclability'] >= recyclability_min)
        ]
        
        st.dataframe(filtered_df, use_container_width=True, height=400)
        
        # Material comparison chart
        st.subheader("📊 Material Comparison")
        
        selected_materials = st.multiselect(
            "Select materials to compare",
            database.materials['name'].tolist(),
            default=database.materials['name'].iloc[:3].tolist()
        )
        
        if len(selected_materials) >= 2:
            compare_df = database.materials[database.materials['name'].isin(selected_materials)]
            
            fig = go.Figure()
            
            metrics = ['carbon_kgCO2e_kg', 'energy_MJ_kg', 'price_usd_kg', 'recyclability']
            metric_names = ['Carbon (kg CO₂e/kg)', 'Energy (MJ/kg)', 'Price (USD/kg)', 'Recyclability']
            
            for i, (metric, name) in enumerate(zip(metrics, metric_names)):
                fig.add_trace(go.Bar(
                    name=name,
                    x=compare_df['name'],
                    y=compare_df[metric],
                    visible=True if i == 0 else False
                ))
            
            # Create buttons for each metric
            buttons = []
            for i, name in enumerate(metric_names):
                visible = [False] * len(metric_names)
                visible[i] = True
                buttons.append(dict(
                    label=name,
                    method="update",
                    args=[{"visible": visible}]
                ))
            
            fig.update_layout(
                updatemenus=[dict(
                    active=0,
                    buttons=buttons,
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.1,
                    yanchor="top"
                )],
                title="Material Property Comparison",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Manufacturing Processes")
        st.dataframe(database.processes, use_container_width=True)
    
    with tab3:
        st.subheader("Transport Modes")
        st.dataframe(database.transport, use_container_width=True)
        
        # Transport visualization
        fig = px.bar(database.transport, 
                     x='mode', 
                     y='carbon_gCO2e_tonne_km',
                     color='mode',
                     title="Carbon Intensity by Transport Mode")
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Regional Factors")
        
        regional_df = pd.DataFrame([
            {'Region': region, 
             'Carbon Intensity (g CO₂e/kWh)': factors['carbon_gCO2e_kWh'],
             'Renewable Share (%)': factors['renewable_share'] * 100}
            for region, factors in database.regional_factors.items()
        ])
        
        st.dataframe(regional_df, use_container_width=True)

def display_settings():
    """Display settings view"""
    st.title("⚙️ Settings")
    
    tab1, tab2, tab3 = st.tabs(["User Preferences", "Calculation Settings", "Data Management"])
    
    with tab1:
        st.subheader("👤 User Preferences")
        
        with st.form("user_preferences"):
            col1, col2 = st.columns(2)
            
            with col1:
                units = st.selectbox("Units System", ["Metric", "Imperial"])
                currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "JPY"])
            
            with col2:
                theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
                auto_save = st.checkbox("Auto-save analyses", True)
            
            if st.form_submit_button("Save Preferences", type="primary"):
                st.session_state.user['preferences'] = {
                    'units': units,
                    'currency': currency,
                    'theme': theme
                }
                st.success("Preferences saved successfully!")
    
    with tab2:
        st.subheader("🧮 Calculation Settings")
        
        with st.form("calculation_settings"):
            lca_method = st.selectbox(
                "LCA Method",
                ["ReCiPe 2016", "IMPACT World+", "TRACI", "CML", "EDIP"]
            )
            
            time_horizon = st.selectbox(
                "Time Horizon",
                ["20 years", "100 years", "500 years", "Infinite"]
            )
            
            col1, col2 = st.columns(2)
            with col1:
                include_biogenic = st.checkbox("Include biogenic carbon", True)
                include_land_use = st.checkbox("Include land use change", True)
            
            with col2:
                include_water = st.checkbox("Include water scarcity", True)
                monte_carlo_iterations = st.number_input("Monte Carlo iterations", 100, 10000, 1000)
            
            if st.form_submit_button("Save Calculation Settings", type="primary"):
                st.success("Calculation settings updated!")
    
    with tab3:
        st.subheader("💾 Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Export Data")
            
            export_options = st.multiselect(
                "Select data to export",
                ["Product Analyses", "Material Database", "Calculation Results"]
            )
            
            if st.button("Export Selected", use_container_width=True):
                st.success("Export started! (Simulated)")
        
        with col2:
            st.markdown("### Import Data")
            
            uploaded_file = st.file_uploader(
                "Upload data file",
                type=['csv', 'json']
            )
            
            if uploaded_file is not None:
                st.info(f"File uploaded: {uploaded_file.name}")
                
                if st.button("Import Data", use_container_width=True):
                    st.success("Data imported successfully! (Simulated)")

# ============================================================================
# MAIN APPLICATION
# ============================================================================
def main():
    """Main application function"""
    
    # Initialize session state
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Display sidebar
    display_sidebar()
    
    # Display main content based on current view
    current_view = st.session_state.current_view
    
    if current_view == "dashboard":
        display_dashboard()
    elif current_view == "quick_assessment":
        display_quick_assessment()
    elif current_view == "detailed_analysis":
        display_detailed_analysis()
    elif current_view == "comparison":
        display_comparison()
    elif current_view == "analytics":
        display_analytics()
    elif current_view == "database":
        display_database()
    elif current_view == "settings":
        display_settings()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: var(--gray); font-size: 0.8rem;">
        <p>🌍 EcoLens Pro v2.0 | Advanced LCA Intelligence Platform</p>
        <p>For academic and industrial use | Compliant with ISO 14040/44</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# RUN APPLICATION
# ============================================================================
if __name__ == "__main__":
    main()
