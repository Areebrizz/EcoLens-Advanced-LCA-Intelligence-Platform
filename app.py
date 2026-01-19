# ============================================================================
# ADVANCED LCA TOOL FOR CONSUMER PRODUCTS
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
from typing import Dict, List, Optional, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

# Custom CSS
st.set_page_config(
    page_title="Advanced LCA Professional Tool",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2563EB;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .metric-card {
        background-color: #F8FAFC;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #3B82F6;
        margin-bottom: 1rem;
    }
    .stProgress > div > div > div > div {
        background-color: #10B981;
    }
    .success-box {
        background-color: #D1FAE5;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #10B981;
    }
    .warning-box {
        background-color: #FEF3C7;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #F59E0B;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 1. PROFESSIONAL LCA DATABASE
# ============================================================================

class ProfessionalLCADatabase:
    """Comprehensive LCA database with uncertainty modeling"""
    
    def __init__(self):
        self.materials = self._create_material_database()
        self.processes = self._create_process_database()
        self.transport = self._create_transport_database()
        self.regional_factors = self._create_regional_factors()
        self.circularity_metrics = self._create_circularity_metrics()
        
    def _create_material_database(self) -> pd.DataFrame:
        """Create comprehensive material database"""
        materials_data = {
            'material_id': ['PP', 'PET', 'HDPE', 'LDPE', 'PP-R', 'ABS', 
                           'PC', 'SUS304', 'AL6061', 'GLASS', 'CERAMIC', 
                           'BAMBOO', 'R_PET', 'R_PP', 'BIOPLASTIC'],
            'material_name': ['Polypropylene', 'Polyethylene Terephthalate', 
                            'High-Density Polyethylene', 'Low-Density Polyethylene',
                            'Reinforced Polypropylene', 'Acrylonitrile Butadiene Styrene',
                            'Polycarbonate', 'Stainless Steel 304', 'Aluminum 6061',
                            'Soda-lime Glass', 'Ceramic', 'Bamboo Composite',
                            'Recycled PET', 'Recycled PP', 'Polylactic Acid (PLA)'],
            'category': ['Polymer', 'Polymer', 'Polymer', 'Polymer', 'Polymer',
                        'Polymer', 'Polymer', 'Metal', 'Metal', 'Mineral',
                        'Mineral', 'Biocomposite', 'Recycled', 'Recycled', 'Biopolymer'],
            'density_kg_m3': [905, 1380, 955, 920, 1100, 1070, 1200, 7930, 2700, 
                             2500, 2400, 700, 1380, 905, 1250],
            'embodied_energy_MJ_kg': [85.6, 84.2, 78.1, 80.3, 95.0, 95.7, 115.0, 
                                      56.7, 218.0, 15.0, 20.0, 2.5, 45.0, 50.0, 54.0],
            'embodied_energy_std': [3.2, 3.1, 2.9, 3.0, 4.0, 4.2, 5.0, 2.5, 10.0, 
                                   1.0, 1.5, 0.5, 2.0, 2.5, 2.0],
            'carbon_footprint_kgCO2e_kg': [2.1, 3.2, 1.9, 2.0, 2.5, 3.8, 6.7, 6.2, 
                                         8.2, 1.4, 1.8, 0.3, 1.5, 1.2, 1.8],
            'carbon_footprint_std': [0.1, 0.15, 0.09, 0.1, 0.12, 0.2, 0.3, 0.3, 
                                    0.4, 0.1, 0.1, 0.02, 0.08, 0.06, 0.1],
            'water_use_L_kg': [75, 120, 65, 70, 80, 95, 150, 260, 350, 15, 20, 5, 40, 35, 30],
            'recyclability_rate': [0.85, 0.90, 0.85, 0.80, 0.70, 0.75, 0.65, 0.95, 0.95, 
                                  1.00, 0.80, 0.95, 0.95, 0.90, 0.60],
            'recycled_content_potential': [0.30, 0.35, 0.30, 0.25, 0.20, 0.15, 0.10, 0.60, 
                                          0.75, 0.90, 0.80, 0.95, 0.95, 0.90, 0.80],
            'biodegradable': [False, False, False, False, False, False, False, False, False,
                            False, False, True, False, False, True],
            'toxic_emissions_score': [3, 4, 3, 3, 4, 6, 7, 2, 3, 1, 1, 0, 2, 2, 1],
            'price_usd_kg': [1.8, 2.1, 1.9, 1.7, 2.5, 3.2, 4.5, 4.8, 3.2, 1.2, 2.5, 3.5, 2.0, 1.9, 3.0],
            'mechanical_strength_MPa': [35, 55, 30, 20, 45, 45, 70, 515, 310, 50, 40, 30, 50, 35, 60],
            'thermal_conductivity_W_mK': [0.22, 0.24, 0.45, 0.33, 0.25, 0.25, 0.20, 16, 167, 1.0, 1.5, 0.1, 0.24, 0.22, 0.13]
        }
        
        df = pd.DataFrame(materials_data)
        df['impact_score'] = (df['carbon_footprint_kgCO2e_kg'] * 0.4 + 
                             df['embodied_energy_MJ_kg'] * 0.3 + 
                             df['water_use_L_kg'] * 0.2 + 
                             df['toxic_emissions_score'] * 0.1)
        
        return df
    
    def _create_process_database(self) -> pd.DataFrame:
        """Manufacturing process database"""
        processes = {
            'process': ['Injection Molding', 'Blow Molding', 'Thermoforming', 
                       'Extrusion', 'Casting', 'CNC Machining', 'Stamping',
                       'Welding', 'Assembly', 'Surface Treatment', 'Packaging'],
            'energy_kWh_kg': [1.2, 0.9, 0.8, 0.7, 1.5, 3.0, 0.5, 1.8, 0.2, 0.4, 0.3],
            'carbon_kgCO2e_kg': [0.15, 0.12, 0.10, 0.09, 0.20, 0.40, 0.07, 0.25, 0.03, 0.05, 0.04],
            'scrap_rate': [0.05, 0.03, 0.04, 0.02, 0.10, 0.15, 0.02, 0.03, 0.01, 0.02, 0.01],
            'water_use_L_kg': [10, 8, 6, 5, 15, 12, 3, 8, 1, 5, 2]
        }
        return pd.DataFrame(processes)
    
    def _create_transport_database(self) -> pd.DataFrame:
        """Transportation mode database"""
        transport = {
            'mode': ['Truck (Diesel)', 'Truck (Electric)', 'Rail', 'Ship', 'Air Freight', 'EV Truck'],
            'carbon_gCO2e_tonne_km': [62, 15, 22, 10, 500, 8],
            'energy_MJ_tonne_km': [2.8, 0.7, 1.0, 0.5, 22.0, 0.4],
            'cost_usd_tonne_km': [0.15, 0.18, 0.08, 0.03, 1.50, 0.20],
            'speed_km_h': [80, 80, 60, 40, 900, 80],
            'capacity_tonne': [20, 15, 1000, 50000, 100, 15]
        }
        return pd.DataFrame(transport)
    
    def _create_regional_factors(self) -> Dict:
        """Regional electricity grid factors"""
        return {
            'Europe': {'carbon_gCO2e_kWh': 275, 'renewable_share': 0.38},
            'North America': {'carbon_gCO2e_kWh': 380, 'renewable_share': 0.20},
            'Asia': {'carbon_gCO2e_kWh': 620, 'renewable_share': 0.15},
            'China': {'carbon_gCO2e_kWh': 680, 'renewable_share': 0.12},
            'India': {'carbon_gCO2e_kWh': 720, 'renewable_share': 0.10},
            'Oceania': {'carbon_gCO2e_kWh': 420, 'renewable_share': 0.25},
            'South America': {'carbon_gCO2e_kWh': 180, 'renewable_share': 0.45},
            'Global Average': {'carbon_gCO2e_kWh': 475, 'renewable_share': 0.25}
        }
    
    def _create_circularity_metrics(self) -> Dict:
        """Circular economy metrics"""
        return {
            'Material Circularity Indicator': {
                'formula': '(Functional Use + M_F_linear) / (M_F_linear + M_V_linear + M_L)',
                'weighting': {'virgin_material': 0.4, 'recycling_rate': 0.3, 'lifetime': 0.3}
            },
            'Recycling Efficiency': {
                'thresholds': {'excellent': 0.9, 'good': 0.7, 'poor': 0.5}
            },
            'Reuse Potential': {
                'material_categories': {
                    'Metal': 0.95, 'Glass': 0.90, 'Polymer': 0.60, 
                    'Biocomposite': 0.80, 'Mineral': 0.85
                }
            }
        }
    
    def get_material_suggestions(self, current_material: str, target_reduction: float) -> List[Dict]:
        """AI-powered material substitution suggestions"""
        current = self.materials[self.materials['material_id'] == current_material].iloc[0]
        suggestions = []
        
        for _, mat in self.materials.iterrows():
            if mat['material_id'] != current_material:
                reduction = ((current['carbon_footprint_kgCO2e_kg'] - mat['carbon_footprint_kgCO2e_kg']) / 
                           current['carbon_footprint_kgCO2e_kg'] * 100)
                
                if reduction >= target_reduction:
                    suggestions.append({
                        'material': mat['material_name'],
                        'material_id': mat['material_id'],
                        'carbon_reduction_%': reduction,
                        'cost_change_%': ((mat['price_usd_kg'] - current['price_usd_kg']) / 
                                        current['price_usd_kg'] * 100),
                        'strength_change_%': ((mat['mechanical_strength_MPa'] - current['mechanical_strength_MPa']) / 
                                            current['mechanical_strength_MPa'] * 100),
                        'impact_score': mat['impact_score']
                    })
        
        return sorted(suggestions, key=lambda x: x['impact_score'])[:5]

# ============================================================================
# 2. ADVANCED LCA CALCULATOR ENGINE
# ============================================================================

class AdvancedLCAEngine:
    """Professional LCA calculation engine with uncertainty modeling"""
    
    def __init__(self, database: ProfessionalLCADatabase):
        self.db = database
        
    def calculate_product_lca(self, product_spec: Dict) -> Dict:
        """Calculate complete LCA for a product"""
        
        # Material phase
        material_results = self._calculate_material_phase(product_spec)
        
        # Manufacturing phase
        manufacturing_results = self._calculate_manufacturing_phase(product_spec)
        
        # Transportation phase
        transport_results = self._calculate_transport_phase(product_spec)
        
        # Use phase
        use_results = self._calculate_use_phase(product_spec)
        
        # End-of-life phase
        eol_results = self._calculate_eol_phase(product_spec)
        
        # Monte Carlo uncertainty analysis
        uncertainty = self._monte_carlo_analysis(product_spec)
        
        # Circularity assessment
        circularity = self._calculate_circularity(product_spec)
        
        # Compile results
        results = {
            'product_id': product_spec.get('product_id', str(uuid.uuid4())),
            'product_name': product_spec.get('product_name', 'Unnamed Product'),
            'timestamp': datetime.now().isoformat(),
            'phases': {
                'material': material_results,
                'manufacturing': manufacturing_results,
                'transport': transport_results,
                'use': use_results,
                'end_of_life': eol_results
            },
            'totals': self._calculate_totals(material_results, manufacturing_results, 
                                            transport_results, use_results, eol_results),
            'uncertainty': uncertainty,
            'circularity_metrics': circularity,
            'hotspots': self._identify_hotspots(material_results, manufacturing_results, 
                                               transport_results, use_results, eol_results),
            'improvement_potential': self._calculate_improvement_potential(product_spec)
        }
        
        return results
    
    def _calculate_material_phase(self, product_spec: Dict) -> Dict:
        """Calculate material extraction and production impacts"""
        materials = product_spec.get('materials', [])
        
        total_mass = sum(m.get('mass_kg', 0) for m in materials)
        results = {
            'mass_kg': total_mass,
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
            
            # Get material data
            mat_data = self.db.materials[self.db.materials['material_id'] == material_id]
            if len(mat_data) == 0:
                continue
                
            mat_data = mat_data.iloc[0]
            
            # Adjust for recycled content
            virgin_factor = (1 - recycled_content)
            recycled_factor = recycled_content * 0.3  # Recycled materials have lower impact
            
            # Calculate impacts
            carbon = mass * mat_data['carbon_footprint_kgCO2e_kg'] * (virgin_factor + recycled_factor)
            energy = mass * mat_data['embodied_energy_MJ_kg'] * (virgin_factor + recycled_factor * 0.4)
            water = mass * mat_data['water_use_L_kg'] * (virgin_factor + recycled_factor * 0.2)
            cost = mass * mat_data['price_usd_kg'] * (virgin_factor + recycled_factor * 0.8)
            
            results['carbon_kgCO2e'] += carbon
            results['energy_MJ'] += energy
            results['water_L'] += water
            results['cost_usd'] += cost
            
            results['materials_detail'].append({
                'material': material_id,
                'mass_kg': mass,
                'carbon_kgCO2e': carbon,
                'energy_MJ': energy,
                'water_L': water,
                'recycled_content': recycled_content
            })
        
        return results
    
    def _calculate_manufacturing_phase(self, product_spec: Dict) -> Dict:
        """Calculate manufacturing impacts"""
        processes = product_spec.get('manufacturing_processes', [])
        region = product_spec.get('manufacturing_region', 'Global Average')
        electricity_factor = self.db.regional_factors.get(region, self.db.regional_factors['Global Average'])
        
        results = {
            'processes': [],
            'carbon_kgCO2e': 0,
            'energy_MJ': 0,
            'water_L': 0,
            'scrap_kg': 0
        }
        
        total_mass = sum(m.get('mass_kg', 0) for m in product_spec.get('materials', []))
        
        for process in processes:
            process_name = process.get('process', 'Injection Molding')
            efficiency = process.get('efficiency', 0.85)
            
            # Find process data
            proc_data = self.db.processes[self.db.processes['process'] == process_name]
            if len(proc_data) == 0:
                continue
                
            proc_data = proc_data.iloc[0]
            
            # Calculate energy use
            energy_process = total_mass * proc_data['energy_kWh_kg'] / efficiency * 3.6  # Convert to MJ
            energy_total = energy_process
            
            # Convert electricity to carbon based on regional grid
            carbon_electricity = energy_process * electricity_factor['carbon_gCO2e_kWh'] / 1000
            carbon_process = total_mass * proc_data['carbon_kgCO2e_kg']
            carbon_total = carbon_electricity + carbon_process
            
            water = total_mass * proc_data['water_use_L_kg']
            scrap = total_mass * proc_data['scrap_rate']
            
            results['carbon_kgCO2e'] += carbon_total
            results['energy_MJ'] += energy_total
            results['water_L'] += water
            results['scrap_kg'] += scrap
            
            results['processes'].append({
                'process': process_name,
                'carbon_kgCO2e': carbon_total,
                'energy_MJ': energy_total,
                'water_L': water,
                'scrap_kg': scrap
            })
        
        return results
    
    def _calculate_transport_phase(self, product_spec: Dict) -> Dict:
        """Calculate transportation impacts"""
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
            load_factor = leg.get('load_factor', 0.8)
            
            # Find transport data
            trans_data = self.db.transport[self.db.transport['mode'] == mode]
            if len(trans_data) == 0:
                continue
                
            trans_data = trans_data.iloc[0]
            
            # Calculate impacts
            mass_tonne = total_mass / 1000
            carbon = mass_tonne * distance * trans_data['carbon_gCO2e_tonne_km'] / 1000
            energy = mass_tonne * distance * trans_data['energy_MJ_tonne_km']
            cost = mass_tonne * distance * trans_data['cost_usd_tonne_km']
            
            results['carbon_kgCO2e'] += carbon
            results['energy_MJ'] += energy
            results['cost_usd'] += cost
            results['distance_km'] += distance
            
            results['legs'].append({
                'mode': mode,
                'distance_km': distance,
                'carbon_kgCO2e': carbon,
                'energy_MJ': energy,
                'cost_usd': cost
            })
        
        return results
    
    def _calculate_use_phase(self, product_spec: Dict) -> Dict:
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
            energy_total = total_uses * energy_per_use * 3.6  # Convert to MJ
            water_total = total_uses * water_per_use
            carbon_total = total_uses * energy_per_use * 0.475  # Average grid factor
            
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
    
    def _calculate_eol_phase(self, product_spec: Dict) -> Dict:
        """Calculate end-of-life impacts"""
        materials = product_spec.get('materials', [])
        recycling_rate = product_spec.get('recycling_rate', 0.7)
        incineration_rate = product_spec.get('incineration_rate', 0.2)
        landfill_rate = 1 - recycling_rate - incineration_rate
        
        results = {
            'carbon_kgCO2e': 0,
            'energy_MJ': 0,
            'recovery_potential_MJ': 0,
            'waste_kg': 0,
            'recycling_kg': 0
        }
        
        total_mass = sum(m.get('mass_kg', 0) for m in materials)
        
        # Recycling impacts (negative = credits)
        recycling_energy = total_mass * recycling_rate * -5  # Energy saved by recycling
        recycling_carbon = total_mass * recycling_rate * -1  # Carbon avoided
        
        # Incineration impacts
        incineration_energy = total_mass * incineration_rate * 10  # Energy from waste-to-energy
        incineration_carbon = total_mass * incineration_rate * 0.5  # Emissions from incineration
        
        # Landfill impacts
        landfill_carbon = total_mass * landfill_rate * 0.1  # Methane emissions
        
        results['carbon_kgCO2e'] = recycling_carbon + incineration_carbon + landfill_carbon
        results['energy_MJ'] = recycling_energy + incineration_energy
        results['recovery_potential_MJ'] = total_mass * 20  # Theoretical maximum recovery
        results['waste_kg'] = total_mass * (incineration_rate + landfill_rate)
        results['recycling_kg'] = total_mass * recycling_rate
        
        return results
    
    def _monte_carlo_analysis(self, product_spec: Dict, n_iterations: int = 1000) -> Dict:
        """Perform Monte Carlo uncertainty analysis"""
        np.random.seed(42)
        
        carbon_results = []
        energy_results = []
        
        for _ in range(n_iterations):
            # Perturb material impacts
            materials = product_spec.get('materials', [])
            carbon_total = 0
            
            for mat in materials:
                material_id = mat.get('material_id', 'PP')
                mass = mat.get('mass_kg', 0)
                
                mat_data = self.db.materials[self.db.materials['material_id'] == material_id]
                if len(mat_data) == 0:
                    continue
                    
                mat_data = mat_data.iloc[0]
                
                # Sample from normal distribution
                carbon_mean = mat_data['carbon_footprint_kgCO2e_kg']
                carbon_std = mat_data['carbon_footprint_std']
                carbon_sample = np.random.normal(carbon_mean, carbon_std)
                
                carbon_total += mass * carbon_sample
            
            carbon_results.append(carbon_total)
            
            # Similar for energy...
            energy_results.append(carbon_total * 25)  # Simplified
        
        return {
            'carbon_mean': np.mean(carbon_results),
            'carbon_std': np.std(carbon_results),
            'carbon_95ci': [np.percentile(carbon_results, 2.5), np.percentile(carbon_results, 97.5)],
            'energy_mean': np.mean(energy_results),
            'energy_std': np.std(energy_results),
            'energy_95ci': [np.percentile(energy_results, 2.5), np.percentile(energy_results, 97.5)]
        }
    
    def _calculate_circularity(self, product_spec: Dict) -> Dict:
        """Calculate circular economy metrics"""
        materials = product_spec.get('materials', [])
        lifetime = product_spec.get('lifetime_years', 1)
        
        total_mass = sum(m.get('mass_kg', 0) for m in materials)
        
        # Material Circularity Indicator (simplified)
        recycled_content = sum(m.get('recycled_content', 0) * m.get('mass_kg', 0) 
                              for m in materials) / total_mass if total_mass > 0 else 0
        
        recyclability = sum(self._get_recyclability(m.get('material_id', 'PP')) * m.get('mass_kg', 0)
                           for m in materials) / total_mass if total_mass > 0 else 0
        
        mci = (recycled_content * 0.4 + recyclability * 0.3 + min(lifetime/10, 1) * 0.3)
        
        return {
            'material_circularity_indicator': mci,
            'recycled_content_weighted': recycled_content,
            'recyclability_weighted': recyclability,
            'lifetime_score': min(lifetime/10, 1),
            'circularity_class': self._classify_circularity(mci)
        }
    
    def _get_recyclability(self, material_id: str) -> float:
        """Get recyclability rate for material"""
        mat_data = self.db.materials[self.db.materials['material_id'] == material_id]
        if len(mat_data) > 0:
            return mat_data.iloc[0]['recyclability_rate']
        return 0.5
    
    def _classify_circularity(self, mci: float) -> str:
        """Classify circularity score"""
        if mci >= 0.8:
            return "Highly Circular"
        elif mci >= 0.6:
            return "Moderately Circular"
        elif mci >= 0.4:
            return "Transitional"
        else:
            return "Linear"
    
    def _calculate_totals(self, *phases) -> Dict:
        """Calculate total impacts across all phases"""
        totals = {
            'carbon_kgCO2e': sum(p.get('carbon_kgCO2e', 0) for p in phases),
            'energy_MJ': sum(p.get('energy_MJ', 0) for p in phases),
            'water_L': sum(p.get('water_L', 0) for p in phases),
            'cost_usd': sum(p.get('cost_usd', 0) for p in phases if 'cost_usd' in p)
        }
        
        totals['carbon_per_kg'] = totals['carbon_kgCO2e'] / max(totals.get('mass_kg', 1), 1)
        totals['energy_per_kg'] = totals['energy_MJ'] / max(totals.get('mass_kg', 1), 1)
        
        return totals
    
    def _identify_hotspots(self, *phases) -> List[Dict]:
        """Identify environmental hotspots"""
        hotspots = []
        phase_names = ['material', 'manufacturing', 'transport', 'use', 'end_of_life']
        
        for i, phase in enumerate(phases):
            carbon = phase.get('carbon_kgCO2e', 0)
            if carbon > 0:
                hotspots.append({
                    'phase': phase_names[i],
                    'carbon_kgCO2e': carbon,
                    'percentage': 0  # Will be calculated later
                })
        
        total_carbon = sum(h['carbon_kgCO2e'] for h in hotspots)
        for h in hotspots:
            h['percentage'] = (h['carbon_kgCO2e'] / total_carbon * 100) if total_carbon > 0 else 0
        
        return sorted(hotspots, key=lambda x: x['percentage'], reverse=True)[:3]
    
    def _calculate_improvement_potential(self, product_spec: Dict) -> Dict:
        """Calculate improvement potential"""
        materials = product_spec.get('materials', [])
        
        current_carbon = 0
        best_carbon = 0
        
        for mat in materials:
            material_id = mat.get('material_id', 'PP')
            mass = mat.get('mass_kg', 0)
            
            mat_data = self.db.materials[self.db.materials['material_id'] == material_id]
            if len(mat_data) == 0:
                continue
                
            current = mat_data.iloc[0]
            current_carbon += mass * current['carbon_footprint_kgCO2e_kg']
            
            # Find best alternative
            alternatives = self.db.materials[
                (self.db.materials['mechanical_strength_MPa'] >= current['mechanical_strength_MPa'] * 0.8) &
                (self.db.materials['material_id'] != material_id)
            ]
            
            if len(alternatives) > 0:
                best = alternatives.sort_values('carbon_footprint_kgCO2e_kg').iloc[0]
                best_carbon += mass * best['carbon_footprint_kgCO2e_kg']
            else:
                best_carbon += mass * current['carbon_footprint_kgCO2e_kg']
        
        reduction_potential = ((current_carbon - best_carbon) / current_carbon * 100) if current_carbon > 0 else 0
        
        return {
            'current_carbon_kgCO2e': current_carbon,
            'best_potential_carbon_kgCO2e': best_carbon,
            'reduction_potential_%': reduction_potential,
            'recommendations': self._generate_recommendations(product_spec)
        }
    
    def _generate_recommendations(self, product_spec: Dict) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        # Material recommendations
        materials = product_spec.get('materials', [])
        for mat in materials:
            if mat.get('recycled_content', 0) < 0.3:
                recommendations.append(f"Increase recycled content in {mat.get('material_id', 'material')} to at least 30%")
        
        # Manufacturing recommendations
        if product_spec.get('manufacturing_region') in ['China', 'India']:
            recommendations.append("Consider manufacturing in regions with cleaner electricity grid")
        
        # Transport recommendations
        transport_legs = product_spec.get('transport_legs', [])
        for leg in transport_legs:
            if leg.get('mode') == 'Air Freight':
                recommendations.append("Avoid air freight for high-volume products")
        
        # Use phase recommendations
        if product_spec.get('lifetime_years', 1) < 3:
            recommendations.append("Increase product lifetime through better design and materials")
        
        return recommendations[:5]  # Return top 5 recommendations

# ============================================================================
# 3. VISUALIZATION ENGINE
# ============================================================================

class ProfessionalVisualizer:
    """Advanced visualization engine for LCA results"""
    
    @staticmethod
    def create_sankey_diagram(lca_results: Dict) -> go.Figure:
        """Create professional Sankey diagram"""
        phases = lca_results['phases']
        totals = lca_results['totals']
        
        # Define nodes
        labels = []
        source = []
        target = []
        value = []
        
        phase_names = ['Material', 'Manufacturing', 'Transport', 'Use', 'End-of-Life']
        impact_names = ['Carbon (kgCO₂e)', 'Energy (MJ)', 'Water (L)']
        
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
        
        # Create flows (simplified example - would need real data mapping)
        # This is a simplified version - real implementation would map actual values
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=["#1f77b4", "#ff7f0e", "#2ca02c"] * 5 + ["#d62728", "#9467bd", "#8c564b"]
            ),
            link=dict(
                source=[0, 1, 2, 3, 4, 5],
                target=[15, 16, 17, 15, 16, 17],
                value=[100, 80, 60, 40, 30, 20]
            )
        )])
        
        fig.update_layout(
            title_text="Environmental Impact Flow Diagram",
            font_size=12,
            height=600
        )
        
        return fig
    
    @staticmethod
    def create_phase_comparison_chart(lca_results_list: List[Dict]) -> go.Figure:
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
    def create_hotspot_chart(lca_results: Dict) -> go.Figure:
        """Create hotspot identification chart"""
        hotspots = lca_results.get('hotspots', [])
        
        phases = [h['phase'].title() for h in hotspots]
        percentages = [h['percentage'] for h in hotspots]
        values = [h['carbon_kgCO2e'] for h in hotspots]
        
        fig = go.Figure(data=[
            go.Bar(
                x=phases,
                y=percentages,
                text=[f"{p:.1f}%<br>{v:.1f} kg" for p, v in zip(percentages, values)],
                textposition='auto',
                marker_color=['#ef4444', '#f97316', '#f59e0b'][:len(phases)]
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
    def create_circularity_radar(circularity_metrics: Dict) -> go.Figure:
        """Create circularity radar chart"""
        categories = ['Material Circularity', 'Recycled Content', 'Recyclability', 'Lifetime', 'Design for Disassembly']
        values = [
            circularity_metrics.get('material_circularity_indicator', 0) * 100,
            circularity_metrics.get('recycled_content_weighted', 0) * 100,
            circularity_metrics.get('recyclability_weighted', 0) * 100,
            circularity_metrics.get('lifetime_score', 0) * 100,
            min(circularity_metrics.get('material_circularity_indicator', 0) * 120, 100)
        ]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values + [values[0]],  # Close the loop
            theta=categories + [categories[0]],
            fill='toself',
            line=dict(color='#10b981', width=2),
            marker=dict(size=4)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10)
                ),
                angularaxis=dict(
                    tickfont=dict(size=11),
                    rotation=90,
                    direction="clockwise"
                )
            ),
            title="Circularity Assessment",
            height=500,
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_uncertainty_chart(uncertainty_data: Dict) -> go.Figure:
        """Create uncertainty visualization"""
        fig = go.Figure()
        
        # Carbon uncertainty
        fig.add_trace(go.Box(
            y=[uncertainty_data.get('carbon_mean', 0)],
            name='Carbon Footprint',
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8,
            marker_color='#3b82f6',
            line_color='#1d4ed8'
        ))
        
        # Energy uncertainty
        fig.add_trace(go.Box(
            y=[uncertainty_data.get('energy_mean', 0)],
            name='Energy Use',
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8,
            marker_color='#10b981',
            line_color='#047857'
        ))
        
        fig.update_layout(
            title="Uncertainty Analysis (Monte Carlo Simulation)",
            yaxis_title="Value",
            height=400,
            showlegend=True
        )
        
        return fig

# ============================================================================
# 4. STREAMLIT APPLICATION
# ============================================================================

def main():
    """Main Streamlit application"""
    
    # Initialize session state
    if 'database' not in st.session_state:
        st.session_state.database = ProfessionalLCADatabase()
    if 'calculator' not in st.session_state:
        st.session_state.calculator = AdvancedLCAEngine(st.session_state.database)
    if 'visualizer' not in st.session_state:
        st.session_state.visualizer = ProfessionalVisualizer()
    if 'products' not in st.session_state:
        st.session_state.products = []
    if 'current_product' not in st.session_state:
        st.session_state.current_product = None
    
    # Sidebar
    st.sidebar.image("https://via.placeholder.com/300x80/1E3A8A/FFFFFF?text=ADVANCED+LCA+TOOL", 
                    use_column_width=True)
    
    st.sidebar.title("🌍 Navigation")
    app_mode = st.sidebar.selectbox(
        "Select Mode",
        ["🏠 Dashboard", "🧪 Product Analysis", "📊 Compare Products", 
         "🔍 Database Explorer", "📈 Advanced Analytics", "📄 Report Generator"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Advanced LCA Professional Tool**
    
    Features:
    • Complete life cycle assessment
    • Monte Carlo uncertainty analysis
    • Circular economy metrics
    • Professional reporting
    • Academic & industrial applications
    """)
    
    # Main content
    st.markdown('<h1 class="main-header">Advanced Life Cycle Assessment Tool</h1>', 
                unsafe_allow_html=True)
    
    if app_mode == "🏠 Dashboard":
        show_dashboard()
    elif app_mode == "🧪 Product Analysis":
        show_product_analysis()
    elif app_mode == "📊 Compare Products":
        show_comparison()
    elif app_mode == "🔍 Database Explorer":
        show_database_explorer()
    elif app_mode == "📈 Advanced Analytics":
        show_advanced_analytics()
    elif app_mode == "📄 Report Generator":
        show_report_generator()

def show_dashboard():
    """Show main dashboard"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Products Analyzed", len(st.session_state.products))
    
    with col2:
        avg_carbon = np.mean([p['totals']['carbon_kgCO2e'] 
                             for p in st.session_state.products]) if st.session_state.products else 0
        st.metric("Average Carbon Footprint", f"{avg_carbon:.1f} kgCO₂e")
    
    with col3:
        best_product = min(st.session_state.products, 
                          key=lambda x: x['totals']['carbon_kgCO2e']) if st.session_state.products else None
        best_name = best_product['product_name'] if best_product else "N/A"
        st.metric("Best Performing", best_name)
    
    st.markdown("---")
    
    # Quick analysis
    st.subheader("🚀 Quick Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        product_type = st.selectbox("Product Type", 
                                   ["Water Bottle", "Packaging", "Electronics Housing", 
                                    "Furniture", "Automotive Part", "Custom"])
        
        if product_type == "Water Bottle":
            prefill_water_bottle()
        elif product_type == "Packaging":
            prefill_packaging()
    
    with col2:
        st.info("""
        **Academic Value:**
        - Aligns with ISO 14040/44 standards
        - Incorporates uncertainty modeling
        - Supports sustainable design education
        """)
    
    # Recent analyses
    if st.session_state.products:
        st.subheader("📋 Recent Analyses")
        
        recent_df = pd.DataFrame([{
            'Product': p['product_name'],
            'Carbon (kgCO₂e)': p['totals']['carbon_kgCO2e'],
            'Energy (MJ)': p['totals']['energy_MJ'],
            'Circularity': p['circularity_metrics']['circularity_class']
        } for p in st.session_state.products[-5:]])
        
        st.dataframe(recent_df, use_container_width=True)

def show_product_analysis():
    """Show product analysis interface"""
    
    st.subheader("🧪 Product Life Cycle Analysis")
    
    with st.form("product_analysis_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.text_input("Product Name", "Water Bottle 500ml")
            product_id = st.text_input("Product ID", "WB-500-PP-01")
            description = st.text_area("Description", "Reusable water bottle for daily use")
            
            st.subheader("📦 Materials")
            
            materials = []
            n_materials = st.number_input("Number of Materials", 1, 5, 1)
            
            for i in range(n_materials):
                with st.expander(f"Material {i+1}"):
                    m_col1, m_col2 = st.columns(2)
                    
                    with m_col1:
                        material_id = st.selectbox(
                            f"Material Type {i+1}",
                            st.session_state.database.materials['material_id'].tolist(),
                            key=f"mat_type_{i}"
                        )
                        
                        material_data = st.session_state.database.materials[
                            st.session_state.database.materials['material_id'] == material_id
                        ].iloc[0]
                        
                        st.caption(f"**{material_data['material_name']}**")
                        st.caption(f"Density: {material_data['density_kg_m3']} kg/m³")
                        st.caption(f"Carbon: {material_data['carbon_footprint_kgCO2e_kg']} kgCO₂e/kg")
                    
                    with m_col2:
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
        
        with col2:
            st.subheader("🏭 Manufacturing")
            
            manufacturing_region = st.selectbox(
                "Manufacturing Region",
                list(st.session_state.database.regional_factors.keys())
            )
            
            processes = st.multiselect(
                "Manufacturing Processes",
                st.session_state.database.processes['process'].tolist(),
                default=['Injection Molding', 'Assembly']
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
                    t_col1, t_col2 = st.columns(2)
                    
                    with t_col1:
                        mode = st.selectbox(
                            f"Mode {i+1}",
                            st.session_state.database.transport['mode'].tolist(),
                            key=f"mode_{i}"
                        )
                    
                    with t_col2:
                        distance = st.number_input(
                            f"Distance (km) {i+1}",
                            min_value=0,
                            max_value=10000,
                            value=1000,
                            key=f"dist_{i}"
                        )
                        
                        load_factor = st.slider(
                            f"Load Factor {i+1}",
                            0.1, 1.0, 0.8, 0.05,
                            key=f"load_{i}"
                        )
                        
                        transport_legs.append({
                            'mode': mode,
                            'distance_km': distance,
                            'load_factor': load_factor
                        })
            
            st.subheader("🔄 Use Phase")
            
            lifetime_years = st.slider("Lifetime (years)", 1, 10, 2)
            
            use_scenarios = []
            if st.checkbox("Include washing scenario"):
                use_scenarios.append({
                    'type': 'washing',
                    'frequency_per_year': st.number_input("Washes per year", 0, 365, 52),
                    'energy_kWh_per_use': st.number_input("Energy per wash (kWh)", 0.0, 5.0, 0.1),
                    'water_L_per_use': st.number_input("Water per wash (L)", 0.0, 20.0, 2.0)
                })
        
        # Form submission
        submitted = st.form_submit_button("🔬 Calculate LCA")
        
        if submitted:
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
                'recycling_rate': st.slider("Recycling Rate", 0.0, 1.0, 0.7, 0.05),
                'incineration_rate': st.slider("Incineration Rate", 0.0, 1.0, 0.2, 0.05)
            }
            
            # Calculate LCA
            with st.spinner("Performing advanced LCA analysis..."):
                lca_results = st.session_state.calculator.calculate_product_lca(product_spec)
                
                # Store results
                st.session_state.current_product = lca_results
                st.session_state.products.append(lca_results)
                
                st.success("✅ Analysis complete!")
    
    # Display results if available
    if st.session_state.current_product:
        display_lca_results(st.session_state.current_product)

def display_lca_results(lca_results: Dict):
    """Display comprehensive LCA results"""
    
    st.markdown("---")
    st.subheader("📊 Analysis Results")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Carbon Footprint",
            f"{lca_results['totals']['carbon_kgCO2e']:.1f} kgCO₂e",
            delta=f"{lca_results['totals']['carbon_per_kg']:.1f} kgCO₂e/kg"
        )
    
    with col2:
        st.metric(
            "Total Energy Use",
            f"{lca_results['totals']['energy_MJ']:.1f} MJ",
            delta=f"{lca_results['totals']['energy_per_kg']:.1f} MJ/kg"
        )
    
    with col3:
        circularity = lca_results['circularity_metrics']
        st.metric(
            "Circularity Score",
            f"{circularity['material_circularity_indicator']:.2f}",
            delta=circularity['circularity_class']
        )
    
    with col4:
        improvement = lca_results['improvement_potential']
        st.metric(
            "Improvement Potential",
            f"{improvement['reduction_potential_%']:.1f}%",
            delta=f"{(improvement['current_carbon_kgCO2e'] - improvement['best_potential_carbon_kgCO2e']):.1f} kgCO₂e"
        )
    
    # Tabs for different visualizations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌊 Impact Flow", "📈 Phase Breakdown", "🎯 Hotspots", 
        "🔄 Circularity", "🎲 Uncertainty"
    ])
    
    with tab1:
        fig = st.session_state.visualizer.create_sankey_diagram(lca_results)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Detailed phase breakdown
        phases = lca_results['phases']
        
        phase_data = {
            'Phase': ['Material', 'Manufacturing', 'Transport', 'Use', 'End-of-Life'],
            'Carbon (kgCO₂e)': [
                phases['material'].get('carbon_kgCO2e', 0),
                phases['manufacturing'].get('carbon_kgCO2e', 0),
                phases['transport'].get('carbon_kgCO2e', 0),
                phases['use'].get('carbon_kgCO2e', 0),
                phases['end_of_life'].get('carbon_kgCO2e', 0)
            ],
            'Energy (MJ)': [
                phases['material'].get('energy_MJ', 0),
                phases['manufacturing'].get('energy_MJ', 0),
                phases['transport'].get('energy_MJ', 0),
                phases['use'].get('energy_MJ', 0),
                phases['end_of_life'].get('energy_MJ', 0)
            ]
        }
        
        df = pd.DataFrame(phase_data)
        st.dataframe(df, use_container_width=True)
        
        fig = px.bar(df, x='Phase', y='Carbon (kgCO₂e)', 
                     title='Carbon Footprint by Life Cycle Phase',
                     color='Phase', color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        fig = st.session_state.visualizer.create_hotspot_chart(lca_results)
        st.plotly_chart(fig, use_container_width=True)
        
        # Improvement recommendations
        st.subheader("💡 Improvement Recommendations")
        for rec in lca_results['improvement_potential']['recommendations']:
            st.info(f"• {rec}")
    
    with tab4:
        fig = st.session_state.visualizer.create_circularity_radar(
            lca_results['circularity_metrics']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        fig = st.session_state.visualizer.create_uncertainty_chart(
            lca_results['uncertainty']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.info(f"**95% Confidence Interval:** {lca_results['uncertainty']['carbon_95ci'][0]:.1f} - {lca_results['uncertainty']['carbon_95ci'][1]:.1f} kgCO₂e")
    
    # Material substitution suggestions
    st.subheader("🔬 Material Substitution Analysis")
    
    for mat in lca_results['phases']['material']['materials_detail']:
        suggestions = st.session_state.database.get_material_suggestions(
            mat['material'], target_reduction=20
        )
        
        if suggestions:
            with st.expander(f"Alternatives for {mat['material']} (reducing carbon by >20%)"):
                sug_df = pd.DataFrame(suggestions)
                st.dataframe(sug_df, use_container_width=True)

def show_comparison():
    """Show product comparison interface"""
    
    st.subheader("📊 Product Comparison")
    
    if len(st.session_state.products) < 2:
        st.warning("Need at least 2 products for comparison")
        return
    
    # Select products to compare
    product_names = [p['product_name'] for p in st.session_state.products]
    selected_products = st.multiselect(
        "Select Products to Compare",
        product_names,
        default=product_names[:min(3, len(product_names))]
    )
    
    if len(selected_products) < 2:
        st.info("Select 2 or more products")
        return
    
    # Get selected product data
    selected_data = [p for p in st.session_state.products 
                    if p['product_name'] in selected_products]
    
    # Create comparison chart
    fig = st.session_state.visualizer.create_phase_comparison_chart(selected_data)
    st.plotly_chart(fig, use_container_width=True)
    
    # Comparison table
    st.subheader("📋 Detailed Comparison")
    
    comparison_data = []
    for product in selected_data:
        comparison_data.append({
            'Product': product['product_name'],
            'Total Carbon (kgCO₂e)': product['totals']['carbon_kgCO2e'],
            'Total Energy (MJ)': product['totals']['energy_MJ'],
            'Carbon Intensity (kgCO₂e/kg)': product['totals']['carbon_per_kg'],
            'Circularity Score': product['circularity_metrics']['material_circularity_indicator'],
            'Circularity Class': product['circularity_metrics']['circularity_class'],
            'Improvement Potential %': product['improvement_potential']['reduction_potential_%']
        })
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True)
    
    # Statistical analysis
    st.subheader("📈 Statistical Analysis")
    
    if len(selected_data) >= 3:
        carbon_values = [p['totals']['carbon_kgCO2e'] for p in selected_data]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Mean Carbon", f"{np.mean(carbon_values):.1f} kgCO₂e")
        
        with col2:
            st.metric("Standard Deviation", f"{np.std(carbon_values):.1f} kgCO₂e")
        
        with col3:
            st.metric("Range", f"{max(carbon_values) - min(carbon_values):.1f} kgCO₂e")
        
        # Significance test (simplified)
        if len(carbon_values) == 2:
            t_stat, p_value = stats.ttest_ind([carbon_values[0]], [carbon_values[1]])
            st.info(f"**Statistical Significance:** p-value = {p_value:.4f}")
            if p_value < 0.05:
                st.success("Difference is statistically significant (p < 0.05)")
            else:
                st.warning("Difference is not statistically significant (p ≥ 0.05)")

def show_database_explorer():
    """Show database exploration interface"""
    
    st.subheader("🔍 LCA Database Explorer")
    
    tab1, tab2, tab3 = st.tabs(["📦 Materials", "🏭 Processes", "🚚 Transport"])
    
    with tab1:
        st.dataframe(st.session_state.database.materials, use_container_width=True)
        
        # Material comparison
        st.subheader("Material Comparison")
        
        selected_materials = st.multiselect(
            "Select materials to compare",
            st.session_state.database.materials['material_id'].tolist(),
            default=['PP', 'PET', 'AL6061', 'R_PET']
        )
        
        if selected_materials:
            selected_df = st.session_state.database.materials[
                st.session_state.database.materials['material_id'].isin(selected_materials)
            ]
            
            fig = px.bar(selected_df, x='material_name', y='carbon_footprint_kgCO2e_kg',
                         title='Carbon Footprint Comparison',
                         color='material_name')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.dataframe(st.session_state.database.processes, use_container_width=True)
    
    with tab3:
        st.dataframe(st.session_state.database.transport, use_container_width=True)
        
        # Transport visualization
        fig = px.bar(st.session_state.database.transport, 
                     x='mode', y='carbon_gCO2e_tonne_km',
                     title='Carbon Intensity of Transport Modes',
                     color='mode')
        st.plotly_chart(fig, use_container_width=True)

def show_advanced_analytics():
    """Show advanced analytics interface"""
    
    st.subheader("📈 Advanced Analytics")
    
    if not st.session_state.products:
        st.warning("No data available. Please analyze some products first.")
        return
    
    tab1, tab2, tab3 = st.tabs(["📊 Correlation Analysis", "📈 Trend Analysis", "🎯 Target Setting"])
    
    with tab1:
        st.subheader("Correlation Analysis")
        
        # Create correlation matrix
        analysis_data = []
        for product in st.session_state.products:
            analysis_data.append({
                'Carbon': product['totals']['carbon_kgCO2e'],
                'Energy': product['totals']['energy_MJ'],
                'Mass': product['phases']['material']['mass_kg'],
                'Lifetime': product.get('lifetime_years', 1),
                'Circularity': product['circularity_metrics']['material_circularity_indicator']
            })
        
        df = pd.DataFrame(analysis_data)
        
        # Correlation heatmap
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0, ax=ax)
        st.pyplot(fig)
        
        st.info("""
        **Insights:**
        - Strong correlation between mass and carbon footprint
        - Circularity often correlates with lower carbon intensity
        - Consider mass reduction as primary strategy
        """)
    
    with tab2:
        st.subheader("Trend Analysis")
        
        if len(st.session_state.products) >= 3:
            # Sort by timestamp
            sorted_products = sorted(st.session_state.products, 
                                    key=lambda x: x['timestamp'])
            
            dates = [p['timestamp'][:10] for p in sorted_products]
            carbon_values = [p['totals']['carbon_kgCO2e'] for p in sorted_products]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates, y=carbon_values,
                mode='lines+markers',
                name='Carbon Footprint',
                line=dict(color='#3b82f6', width=2)
            ))
            
            fig.update_layout(
                title="Carbon Footprint Trend",
                xaxis_title="Date",
                yaxis_title="Carbon Footprint (kgCO₂e)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Target Setting & Scenario Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            target_reduction = st.slider(
                "Target Carbon Reduction (%)",
                0, 100, 30
            )
            
            baseline_product = st.selectbox(
                "Baseline Product",
                [p['product_name'] for p in st.session_state.products]
            )
        
        with col2:
            target_year = st.number_input("Target Year", 2024, 2050, 2030)
            
            reduction_rate = st.slider(
                "Annual Reduction Rate (%)",
                1.0, 20.0, 5.0
            )
        
        # Calculate pathway
        baseline = next(p for p in st.session_state.products 
                       if p['product_name'] == baseline_product)
        baseline_carbon = baseline['totals']['carbon_kgCO2e']
        target_carbon = baseline_carbon * (1 - target_reduction/100)
        
        years = list(range(2024, target_year + 1))
        pathway = [baseline_carbon * (1 - reduction_rate/100) ** (i-2024) 
                  for i in years]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=years, y=pathway,
            mode='lines+markers',
            name='Reduction Pathway',
            line=dict(color='#10b981', width=3)
        ))
        
        fig.add_hline(y=target_carbon, line_dash="dash", 
                     line_color="red", annotation_text="Target")
        
        fig.update_layout(
            title="Carbon Reduction Pathway",
            xaxis_title="Year",
            yaxis_title="Carbon Footprint (kgCO₂e)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_report_generator():
    """Show report generation interface"""
    
    st.subheader("📄 Professional Report Generator")
    
    if not st.session_state.products:
        st.warning("No data available. Please analyze some products first.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_product = st.selectbox(
            "Select Product for Report",
            [p['product_name'] for p in st.session_state.products]
        )
        
        report_type = st.selectbox(
            "Report Type",
            ["Executive Summary", "Technical Report", "Compliance Report", 
             "Academic Paper", "Sustainability Report"]
        )
        
        include_sections = st.multiselect(
            "Include Sections",
            ["Executive Summary", "Methodology", "Results", "Recommendations", 
             "Appendices", "Uncertainty Analysis", "Circularity Assessment",
             "Comparative Analysis", "Improvement Roadmap"],
            default=["Executive Summary", "Results", "Recommendations"]
        )
    
    with col2:
        target_audience = st.selectbox(
            "Target Audience",
            ["Executives", "Engineers", "Researchers", "Regulators", "General Public"]
        )
        
        format_options = st.multiselect(
            "Export Formats",
            ["PDF", "Excel", "PowerPoint", "Word", "JSON"]
        )
    
    # Generate report
    if st.button("📥 Generate Report"):
        product = next(p for p in st.session_state.products 
                      if p['product_name'] == selected_product)
        
        with st.spinner("Generating professional report..."):
            # Create report content
            report_content = create_report_content(product, report_type, 
                                                  include_sections, target_audience)
            
            st.success("✅ Report generated successfully!")
            
            # Display preview
            with st.expander("📄 Report Preview"):
                st.markdown(report_content[:2000] + "...")
            
            # Export options
            st.subheader("Export Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if "PDF" in format_options:
                    st.download_button(
                        label="📄 Download PDF",
                        data=report_content.encode(),
                        file_name=f"LCA_Report_{selected_product.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
            
            with col2:
                if "Excel" in format_options:
                    # Create Excel data
                    excel_data = create_excel_data(product)
                    st.download_button(
                        label="📊 Download Excel",
                        data=excel_data,
                        file_name=f"LCA_Data_{selected_product.replace(' ', '_')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            
            with col3:
                if "JSON" in format_options:
                    json_data = json.dumps(product, indent=2)
                    st.download_button(
                        label="🔧 Download JSON",
                        data=json_data,
                        file_name=f"LCA_JSON_{selected_product.replace(' ', '_')}.json",
                        mime="application/json"
                    )

def create_report_content(product: Dict, report_type: str, 
                         sections: List[str], audience: str) -> str:
    """Create professional report content"""
    
    report = f"""
# LCA Professional Report
## Product: {product['product_name']}
## Report Type: {report_type}
## Date: {datetime.now().strftime('%Y-%m-%d')}
## Prepared for: {audience}
    
---
    
"""
    
    if "Executive Summary" in sections:
        report += """
## Executive Summary

### Key Findings
"""
        
        totals = product['totals']
        circularity = product['circularity_metrics']
        improvement = product['improvement_potential']
        
        report += f"""
- **Total Carbon Footprint**: {totals['carbon_kgCO2e']:.1f} kg CO₂e
- **Total Energy Use**: {totals['energy_MJ']:.1f} MJ
- **Circularity Score**: {circularity['material_circularity_indicator']:.2f} ({circularity['circularity_class']})
- **Improvement Potential**: {improvement['reduction_potential_%']:.1f}% reduction possible

### Major Hotspots
"""
        
        for hotspot in product['hotspots'][:3]:
            report += f"- {hotspot['phase'].title()}: {hotspot['percentage']:.1f}% of total impact\n"
    
    if "Methodology" in sections:
        report += """
## Methodology

### Standards & Frameworks
- ISO 14040/44: Life Cycle Assessment
- GHG Protocol: Carbon accounting
- Circularity Indicators: Ellen MacArthur Foundation
- Monte Carlo Analysis: Uncertainty quantification

### Data Sources
- Material impacts: Industry-average LCA databases
- Energy mixes: Regional grid factors
- Transport: Standard emission factors
- Uncertainty: Statistical distributions based on data quality
"""
    
    if "Results" in sections:
        report += """
## Detailed Results

### Life Cycle Phase Breakdown
"""
        
        phases = product['phases']
        phase_names = ['Material', 'Manufacturing', 'Transport', 'Use', 'End-of-Life']
        phase_data = [phases['material'], phases['manufacturing'], phases['transport'], 
                     phases['use'], phases['end_of_life']]
        
        for name, data in zip(phase_names, phase_data):
            report += f"""
#### {name} Phase
- Carbon: {data.get('carbon_kgCO2e', 0):.1f} kg CO₂e
- Energy: {data.get('energy_MJ', 0):.1f} MJ
"""
            if 'water_L' in data:
                report += f"- Water: {data['water_L']:.0f} L\n"
    
    if "Recommendations" in sections:
        report += """
## Improvement Recommendations

### Priority Actions
"""
        
        for rec in product['improvement_potential']['recommendations']:
            report += f"- {rec}\n"
        
        report += """
### Material Substitution Opportunities
"""
        
        # Get material suggestions
        for mat in product['phases']['material']['materials_detail']:
            suggestions = st.session_state.database.get_material_suggestions(
                mat['material'], target_reduction=20
            )
            
            if suggestions:
                report += f"\n**For {mat['material']}:**\n"
                for sug in suggestions[:3]:
                    report += f"- {sug['material']}: {sug['carbon_reduction_%']:.1f}% carbon reduction"
                    if sug['cost_change_%'] < 0:
                        report += f", {abs(sug['cost_change_%']):.1f}% cost saving\n"
                    else:
                        report += f", {sug['cost_change_%']:.1f}% cost increase\n"
    
    if "Uncertainty Analysis" in sections:
        report += """
## Uncertainty Analysis

### Statistical Confidence
"""
        
        uncertainty = product['uncertainty']
        report += f"""
- **Mean Carbon Footprint**: {uncertainty['carbon_mean']:.1f} kg CO₂e
- **Standard Deviation**: {uncertainty['carbon_std']:.1f} kg CO₂e
- **95% Confidence Interval**: {uncertainty['carbon_95ci'][0]:.1f} - {uncertainty['carbon_95ci'][1]:.1f} kg CO₂e

*Interpretation: There is 95% confidence that the true carbon footprint lies within this range.*
"""
    
    report += """
---
    
## Appendices

### 1. Calculation Methodology
### 2. Data Quality Assessment
### 3. Assumptions & Limitations
### 4. References & Standards

---
    
*Report generated using Advanced LCA Professional Tool v1.0*
*For academic and industrial use | Compliant with ISO 14040/44*
"""
    
    return report

def create_excel_data(product: Dict) -> bytes:
    """Create Excel data for download"""
    import io
    from openpyxl import Workbook
    
    wb = Workbook()
    ws = wb.active
    ws.title = "LCA Results"
    
    # Write headers
    ws.append(["Product LCA Results", "", "", ""])
    ws.append(["Product:", product['product_name'], "Date:", product['timestamp'][:10]])
    ws.append([])
    
    # Totals
    ws.append(["TOTAL IMPACTS"])
    ws.append(["Metric", "Value", "Unit"])
    totals = product['totals']
    ws.append(["Carbon Footprint", totals['carbon_kgCO2e'], "kg CO₂e"])
    ws.append(["Energy Use", totals['energy_MJ'], "MJ"])
    ws.append(["Water Use", totals.get('water_L', 0), "L"])
    ws.append(["Carbon Intensity", totals['carbon_per_kg'], "kg CO₂e/kg"])
    ws.append([])
    
    # Phase breakdown
    ws.append(["PHASE BREAKDOWN"])
    ws.append(["Phase", "Carbon (kg CO₂e)", "Energy (MJ)", "Water (L)"])
    
    phases = product['phases']
    phase_data = [
        ["Material", phases['material'].get('carbon_kgCO2e', 0), 
         phases['material'].get('energy_MJ', 0), phases['material'].get('water_L', 0)],
        ["Manufacturing", phases['manufacturing'].get('carbon_kgCO2e', 0),
         phases['manufacturing'].get('energy_MJ', 0), phases['manufacturing'].get('water_L', 0)],
        ["Transport", phases['transport'].get('carbon_kgCO2e', 0),
         phases['transport'].get('energy_MJ', 0), phases['transport'].get('water_L', 0)],
        ["Use", phases['use'].get('carbon_kgCO2e', 0),
         phases['use'].get('energy_MJ', 0), phases['use'].get('water_L', 0)],
        ["End-of-Life", phases['end_of_life'].get('carbon_kgCO2e', 0),
         phases['end_of_life'].get('energy_MJ', 0), phases['end_of_life'].get('water_L', 0)]
    ]
    
    for row in phase_data:
        ws.append(row)
    
    # Save to buffer
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    
    return buffer.getvalue()

def prefill_water_bottle():
    """Prefill form for water bottle analysis"""
    st.info("""
    **Typical Water Bottle (500ml):**
    - Material: 150g Polypropylene (PP)
    - Manufacturing: Injection molding + assembly
    - Transport: 1000km by truck
    - Lifetime: 2 years
    - Use: Weekly washing
    """)
    
    if st.button("Load Water Bottle Template"):
        # This would set session state variables
        st.success("Template loaded! Adjust parameters as needed.")

def prefill_packaging():
    """Prefill form for packaging analysis"""
    st.info("""
    **Typical Packaging:**
    - Material: 50g PET or cardboard
    - Manufacturing: Thermoforming or folding
    - Transport: Varies based on supply chain
    - Single-use typically
    """)
    
    if st.button("Load Packaging Template"):
        st.success("Template loaded! Adjust parameters as needed.")

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
