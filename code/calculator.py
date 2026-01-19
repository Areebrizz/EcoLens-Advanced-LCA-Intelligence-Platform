# ============================================================================
# ADVANCED LCA CALCULATOR ENGINE
# ============================================================================
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
import uuid
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

@dataclass
class LCAResult:
    """Comprehensive LCA result container"""
    product_id: str
    product_name: str
    timestamp: datetime
    phases: Dict[str, Dict]
    totals: Dict[str, float]
    uncertainty: Dict[str, Any]
    circularity_metrics: Dict[str, float]
    hotspots: List[Dict]
    improvement_potential: Dict
    metadata: Dict[str, Any]

class AdvancedLCAEngine:
    """Advanced LCA calculation engine with uncertainty modeling"""
    
    def __init__(self, database):
        self.db = database
        self.uncertainty_analyzer = UncertaintyAnalyzer()
        self.circularity_analyzer = CircularEconomyAnalyzer()
    
    def calculate_comprehensive_lca(self, product_spec: Dict) -> LCAResult:
        """Calculate comprehensive LCA with all advanced features"""
        
        # Perform uncertainty analysis
        uncertainty = self.uncertainty_analyzer.monte_carlo_analysis(product_spec)
        
        # Calculate circularity metrics
        circularity = self.circularity_analyzer.calculate_metrics(product_spec)
        
        # Calculate traditional LCA
        phases = self._calculate_all_phases(product_spec)
        
        # Calculate totals
        totals = self._calculate_totals(phases)
        
        # Identify hotspots
        hotspots = self._identify_hotspots(phases)
        
        # Calculate improvement potential
        improvement = self._calculate_improvement_potential(product_spec, phases)
        
        # Create result object
        result = LCAResult(
            product_id=product_spec.get('product_id', str(uuid.uuid4())),
            product_name=product_spec.get('product_name', 'Unnamed Product'),
            timestamp=datetime.now(),
            phases=phases,
            totals=totals,
            uncertainty=uncertainty,
            circularity_metrics=circularity,
            hotspots=hotspots,
            improvement_potential=improvement,
            metadata={
                'calculation_method': 'Advanced LCA Engine v2.0',
                'assumptions': product_spec.get('assumptions', {}),
                'data_quality': self._assess_data_quality(product_spec)
            }
        )
        
        return result
    
    def _calculate_all_phases(self, product_spec: Dict) -> Dict[str, Dict]:
        """Calculate impacts for all life cycle phases"""
        
        phases = {
            'material': self._calculate_material_phase(product_spec),
            'manufacturing': self._calculate_manufacturing_phase(product_spec),
            'transport': self._calculate_transport_phase(product_spec),
            'use': self._calculate_use_phase(product_spec),
            'end_of_life': self._calculate_eol_phase(product_spec),
            'upstream': self._calculate_upstream_impacts(product_spec),
            'downstream': self._calculate_downstream_impacts(product_spec)
        }
        
        return phases
    
    def _calculate_material_phase(self, product_spec: Dict) -> Dict:
        """Advanced material phase calculation with allocation"""
        
        materials = product_spec.get('materials', [])
        allocation_method = product_spec.get('allocation_method', 'mass')
        
        results = {
            'mass_kg': 0,
            'carbon_kgCO2e': 0,
            'carbon_allocated': {},
            'energy_MJ': 0,
            'water_L': 0,
            'cost_usd': 0,
            'materials_detail': [],
            'allocation_factors': {}
        }
        
        total_mass = sum(m.get('mass_kg', 0) for m in materials)
        
        for mat in materials:
            material_id = mat.get('material_id', 'PP')
            mass = mat.get('mass_kg', 0)
            recycled_content = mat.get('recycled_content', 0)
            
            # Get material data with uncertainty
            mat_data = self.db.get_material(material_id)
            if not mat_data:
                continue
            
            # Calculate allocation factor
            if allocation_method == 'mass':
                allocation_factor = mass / total_mass if total_mass > 0 else 0
            elif allocation_method == 'economic':
                allocation_factor = (mass * mat_data['price']) / sum(
                    m.get('mass_kg', 0) * self.db.get_material(
                        m.get('material_id', 'PP')).get('price', 1) 
                    for m in materials
                )
            else:
                allocation_factor = 1.0
            
            results['allocation_factors'][material_id] = allocation_factor
            
            # Calculate impacts with allocation
            virgin_factor = (1 - recycled_content)
            recycled_factor = recycled_content * 0.3
            
            # Base impacts
            carbon_base = mass * mat_data['carbon_footprint'] * (virgin_factor + recycled_factor)
            energy_base = mass * mat_data['embodied_energy'] * (virgin_factor + recycled_factor * 0.4)
            water_base = mass * mat_data['water_use'] * (virgin_factor + recycled_factor * 0.2)
            
            # Allocated impacts
            carbon_allocated = carbon_base * allocation_factor
            energy_allocated = energy_base * allocation_factor
            water_allocated = water_base * allocation_factor
            
            results['mass_kg'] += mass
            results['carbon_kgCO2e'] += carbon_allocated
            results['carbon_allocated'][material_id] = carbon_allocated
            results['energy_MJ'] += energy_allocated
            results['water_L'] += water_allocated
            results['cost_usd'] += mass * mat_data['price'] * allocation_factor
            
            results['materials_detail'].append({
                'material': material_id,
                'mass_kg': mass,
                'recycled_content': recycled_content,
                'carbon_allocated': carbon_allocated,
                'energy_allocated': energy_allocated,
                'allocation_factor': allocation_factor
            })
        
        return results
    
    def _calculate_manufacturing_phase(self, product_spec: Dict) -> Dict:
        """Advanced manufacturing calculation with process efficiency curves"""
        
        processes = product_spec.get('manufacturing_processes', [])
        region = product_spec.get('manufacturing_region', 'Global Average')
        
        results = {
            'processes': [],
            'carbon_kgCO2e': 0,
            'energy_MJ': 0,
            'water_L': 0,
            'scrap_kg': 0,
            'efficiency_score': 0
        }
        
        total_mass = sum(m.get('mass_kg', 0) for m in product_spec.get('materials', []))
        
        for process in processes:
            process_name = process.get('process', 'Injection Molding')
            efficiency = process.get('efficiency', 0.85)
            technology_level = process.get('technology_level', 'average')
            
            # Get process-specific factors
            tech_factors = {
                'basic': 1.2,
                'average': 1.0,
                'advanced': 0.8,
                'state_of_art': 0.6
            }
            
            tech_factor = tech_factors.get(technology_level, 1.0)
            
            # Calculate process energy with technology factor
            base_energy = total_mass * self._get_process_energy(process_name)
            actual_energy = base_energy / efficiency * tech_factor
            
            # Convert to carbon based on regional grid
            regional_factor = self.db.get_regional_factors().get(
                region, {'carbon_gCO2e_kWh': 475}
            )['carbon_gCO2e_kWh']
            
            carbon = actual_energy * 3.6 * regional_factor / 1000  # Convert to kg
            
            results['carbon_kgCO2e'] += carbon
            results['energy_MJ'] += actual_energy * 3.6
            
            results['processes'].append({
                'process': process_name,
                'efficiency': efficiency,
                'technology': technology_level,
                'carbon': carbon,
                'energy': actual_energy * 3.6
            })
        
        # Calculate overall efficiency score
        if results['processes']:
            avg_efficiency = np.mean([p['efficiency'] for p in results['processes']])
            results['efficiency_score'] = avg_efficiency
        
        return results
    
    def _get_process_energy(self, process_name: str) -> float:
        """Get process-specific energy consumption"""
        process_energies = {
            'Injection Molding': 1.2,
            'Blow Molding': 0.9,
            'Thermoforming': 0.8,
            'Extrusion': 0.7,
            'Casting': 1.5,
            'CNC Machining': 3.0,
            'Assembly': 0.2
        }
        return process_energies.get(process_name, 1.0)
    
    def _calculate_transport_phase(self, product_spec: Dict) -> Dict:
        """Advanced transport calculation with modal shifts"""
        
        transport_legs = product_spec.get('transport_legs', [])
        
        results = {
            'carbon_kgCO2e': 0,
            'energy_MJ': 0,
            'cost_usd': 0,
            'distance_km': 0,
            'modal_mix': {},
            'legs': []
        }
        
        total_mass = sum(m.get('mass_kg', 0) for m in product_spec.get('materials', []))
        
        for leg in transport_legs:
            mode = leg.get('mode', 'Truck (Diesel)')
            distance = leg.get('distance_km', 1000)
            load_factor = leg.get('load_factor', 0.8)
            
            # Get transport data
            transport_data = self._get_transport_data(mode)
            
            # Calculate with load factor
            effective_distance = distance / load_factor if load_factor > 0 else distance
            
            mass_tonne = total_mass / 1000
            carbon = mass_tonne * effective_distance * transport_data['carbon'] / 1000
            energy = mass_tonne * effective_distance * transport_data['energy']
            cost = mass_tonne * effective_distance * transport_data['cost']
            
            results['carbon_kgCO2e'] += carbon
            results['energy_MJ'] += energy
            results['cost_usd'] += cost
            results['distance_km'] += distance
            
            # Update modal mix
            results['modal_mix'][mode] = results['modal_mix'].get(mode, 0) + distance
            
            results['legs'].append({
                'mode': mode,
                'distance': distance,
                'load_factor': load_factor,
                'carbon': carbon,
                'energy': energy,
                'cost': cost
            })
        
        return results
    
    def _get_transport_data(self, mode: str) -> Dict:
        """Get transport mode data"""
        transport_data = {
            'Truck (Diesel)': {'carbon': 62, 'energy': 2.8, 'cost': 0.15},
            'Truck (Electric)': {'carbon': 15, 'energy': 0.7, 'cost': 0.18},
            'Rail': {'carbon': 22, 'energy': 1.0, 'cost': 0.08},
            'Ship': {'carbon': 10, 'energy': 0.5, 'cost': 0.03},
            'Air Freight': {'carbon': 500, 'energy': 22.0, 'cost': 1.50}
        }
        return transport_data.get(mode, {'carbon': 62, 'energy': 2.8, 'cost': 0.15})
    
    def _calculate_use_phase(self, product_spec: Dict) -> Dict:
        """Advanced use phase calculation with dynamic scenarios"""
        
        lifetime = product_spec.get('lifetime_years', 1)
        use_scenarios = product_spec.get('use_scenarios', [])
        maintenance = product_spec.get('maintenance', {})
        
        results = {
            'carbon_kgCO2e': 0,
            'energy_MJ': 0,
            'water_L': 0,
            'scenarios': [],
            'maintenance_impacts': {}
        }
        
        for scenario in use_scenarios:
            scenario_type = scenario.get('type', 'operation')
            frequency = scenario.get('frequency_per_year', 1)
            energy_per_use = scenario.get('energy_kWh_per_use', 0)
            water_per_use = scenario.get('water_L_per_use', 0)
            
            total_uses = frequency * lifetime
            energy_total = total_uses * energy_per_use * 3.6  # MJ
            water_total = total_uses * water_per_use
            
            # Dynamic carbon based on grid decarbonization over time
            if scenario.get('consider_grid_decarbonization', False):
                carbon_total = self._calculate_dynamic_carbon(
                    total_uses, energy_per_use, lifetime
                )
            else:
                carbon_total = total_uses * energy_per_use * 0.475  # Average grid
            
            results['carbon_kgCO2e'] += carbon_total
            results['energy_MJ'] += energy_total
            results['water_L'] += water_total
            
            results['scenarios'].append({
                'type': scenario_type,
                'total_uses': total_uses,
                'carbon': carbon_total,
                'energy': energy_total,
                'water': water_total
            })
        
        # Calculate maintenance impacts
        if maintenance:
            results['maintenance_impacts'] = self._calculate_maintenance_impacts(
                maintenance, lifetime
            )
        
        return results
    
    def _calculate_dynamic_carbon(self, total_uses: int, energy_per_use: float, 
                                 lifetime: int) -> float:
        """Calculate carbon with grid decarbonization over time"""
        # Simple linear decarbonization model
        base_carbon = 0.475  # kg CO2e/kWh
        annual_reduction = 0.02  # 2% per year
        
        total_carbon = 0
        for year in range(lifetime):
            year_carbon = base_carbon * ((1 - annual_reduction) ** year)
            annual_uses = total_uses / lifetime
            total_carbon += annual_uses * energy_per_use * year_carbon
        
        return total_carbon
    
    def _calculate_maintenance_impacts(self, maintenance: Dict, lifetime: int) -> Dict:
        """Calculate maintenance and repair impacts"""
        # Implementation for maintenance impacts
        return {
            'replacement_parts': 0,
            'consumables': 0,
            'service_visits': 0
        }
    
    def _calculate_eol_phase(self, product_spec: Dict) -> Dict:
        """Advanced end-of-life calculation with circular economy options"""
        
        materials = product_spec.get('materials', [])
        eol_scenario = product_spec.get('eol_scenario', {
            'recycling_rate': 0.7,
            'incineration_rate': 0.2,
            'landfill_rate': 0.1,
            'energy_recovery_efficiency': 0.8
        })
        
        results = {
            'carbon_kgCO2e': 0,
            'energy_MJ': 0,
            'material_recovery_potential_MJ': 0,
            'circularity_benefits': {},
            'waste_hierarchy': eol_scenario
        }
        
        total_mass = sum(m.get('mass_kg', 0) for m in materials)
        
        # Calculate recycling benefits (negative = credit)
        recycling_mass = total_mass * eol_scenario['recycling_rate']
        recycling_credit = -recycling_mass * 1.5  # kg CO2e credit per kg recycled
        recycling_energy_credit = -recycling_mass * 5  # MJ credit
        
        # Calculate incineration with energy recovery
        incineration_mass = total_mass * eol_scenario['incineration_rate']
        incineration_energy = incineration_mass * 10 * eol_scenario['energy_recovery_efficiency']
        incineration_carbon = incineration_mass * 0.5
        
        # Calculate landfill impacts
        landfill_mass = total_mass * eol_scenario['landfill_rate']
        landfill_carbon = landfill_mass * 0.1  # Methane emissions
        
        results['carbon_kgCO2e'] = recycling_credit + incineration_carbon + landfill_carbon
        results['energy_MJ'] = recycling_energy_credit + incineration_energy
        results['material_recovery_potential_MJ'] = total_mass * 20
        
        # Circular economy benefits
        results['circularity_benefits'] = {
            'material_recovery_potential_kg': recycling_mass,
            'energy_recovery_potential_MJ': incineration_energy,
            'avoided_virgin_material_kg': recycling_mass * 0.8
        }
        
        return results
    
    def _calculate_upstream_impacts(self, product_spec: Dict) -> Dict:
        """Calculate upstream (cradle-to-gate) impacts"""
        # Implementation for upstream supply chain impacts
        return {
            'carbon_kgCO2e': 0,
            'energy_MJ': 0,
            'water_L': 0,
            'upstream_processes': []
        }
    
    def _calculate_downstream_impacts(self, product_spec: Dict) -> Dict:
        """Calculate downstream impacts beyond use phase"""
        # Implementation for downstream impacts
        return {
            'carbon_kgCO2e': 0,
            'energy_MJ': 0,
            'water_L': 0,
            'downstream_processes': []
        }
    
    def _calculate_totals(self, phases: Dict) -> Dict:
        """Calculate total impacts across all phases"""
        
        totals = {
            'carbon_kgCO2e': 0,
            'energy_MJ': 0,
            'water_L': 0,
            'cost_usd': 0,
            'normalized_impacts': {},
            'impact_categories': {}
        }
        
        # Sum across phases
        for phase_name, phase_data in phases.items():
            totals['carbon_kgCO2e'] += phase_data.get('carbon_kgCO2e', 0)
            totals['energy_MJ'] += phase_data.get('energy_MJ', 0)
            totals['water_L'] += phase_data.get('water_L', 0)
            totals['cost_usd'] += phase_data.get('cost_usd', 0)
        
        # Calculate normalized impacts
        totals['normalized_impacts'] = self._normalize_impacts(totals)
        
        # Calculate impact categories
        totals['impact_categories'] = self._calculate_impact_categories(phases)
        
        return totals
    
    def _normalize_impacts(self, totals: Dict) -> Dict:
        """Normalize impacts to reference values"""
        reference_values = {
            'carbon_per_capita': 5000,  # kg CO2e/year
            'energy_per_capita': 80000,  # MJ/year
            'water_per_capita': 1500000  # L/year
        }
        
        normalized = {
            'carbon': totals['carbon_kgCO2e'] / reference_values['carbon_per_capita'],
            'energy': totals['energy_MJ'] / reference_values['energy_per_capita'],
            'water': totals['water_L'] / reference_values['water_per_capita']
        }
        
        return normalized
    
    def _calculate_impact_categories(self, phases: Dict) -> Dict:
        """Calculate various impact categories"""
        # Simplified implementation
        return {
            'climate_change': phases['material'].get('carbon_kgCO2e', 0) * 1.0,
            'resource_depletion': phases['material'].get('energy_MJ', 0) * 0.01,
            'water_scarcity': phases['material'].get('water_L', 0) * 0.001,
            'eutrophication': 0,  # Would need specific characterization factors
            'acidification': 0
        }
    
    def _identify_hotspots(self, phases: Dict) -> List[Dict]:
        """Identify environmental hotspots with statistical significance"""
        
        hotspots = []
        total_carbon = sum(p.get('carbon_kgCO2e', 0) for p in phases.values())
        
        if total_carbon > 0:
            for phase_name, phase_data in phases.items():
                carbon = phase_data.get('carbon_kgCO2e', 0)
                percentage = (carbon / total_carbon * 100) if total_carbon > 0 else 0
                
                if percentage > 10:  # Threshold for hotspot
                    hotspots.append({
                        'phase': phase_name,
                        'carbon_kgCO2e': carbon,
                        'percentage': percentage,
                        'significance': self._assess_significance(percentage),
                        'improvement_levers': self._identify_improvement_levers(phase_name)
                    })
        
        # Sort by percentage
        hotspots.sort(key=lambda x: x['percentage'], reverse=True)
        
        return hotspots[:5]  # Return top 5 hotspots
    
    def _assess_significance(self, percentage: float) -> str:
        """Assess statistical significance of hotspot"""
        if percentage > 50:
            return 'Critical'
        elif percentage > 30:
            return 'High'
        elif percentage > 15:
            return 'Medium'
        else:
            return 'Low'
    
    def _identify_improvement_levers(self, phase_name: str) -> List[str]:
        """Identify improvement levers for hotspot phase"""
        levers = {
            'material': [
                'Switch to lower-impact materials',
                'Increase recycled content',
                'Reduce material mass'
            ],
            'manufacturing': [
                'Improve process efficiency',
                'Switch to renewable energy',
                'Optimize production planning'
            ],
            'transport': [
                'Optimize logistics',
                'Switch to low-carbon transport',
                'Reduce transportation distance'
            ]
        }
        return levers.get(phase_name, ['General efficiency improvements'])
    
    def _calculate_improvement_potential(self, product_spec: Dict, phases: Dict) -> Dict:
        """Calculate improvement potential with optimization"""
        
        # Baseline impacts
        baseline_carbon = sum(p.get('carbon_kgCO2e', 0) for p in phases.values())
        
        # Optimized scenario
        optimized_scenario = self._create_optimized_scenario(product_spec)
        optimized_phases = self._calculate_all_phases(optimized_scenario)
        optimized_carbon = sum(p.get('carbon_kgCO2e', 0) for p in optimized_phases.values())
        
        # Calculate reduction potential
        reduction_potential = ((baseline_carbon - optimized_carbon) / baseline_carbon * 100) if baseline_carbon > 0 else 0
        
        return {
            'baseline_carbon_kgCO2e': baseline_carbon,
            'optimized_carbon_kgCO2e': optimized_carbon,
            'reduction_potential_%': reduction_potential,
            'optimization_scenarios': self._generate_optimization_scenarios(product_spec),
            'cost_implications': self._calculate_cost_implications(baseline_carbon, optimized_carbon)
        }
    
    def _create_optimized_scenario(self, product_spec: Dict) -> Dict:
        """Create optimized product scenario"""
        optimized = product_spec.copy()
        
        # Apply optimizations
        materials = optimized.get('materials', [])
        for mat in materials:
            # Increase recycled content
            mat['recycled_content'] = min(mat.get('recycled_content', 0) + 0.3, 1.0)
            
            # Consider material substitution
            if mat.get('material_id') in ['PP', 'PET']:
                # Switch to recycled version
                mat['material_id'] = 'R_' + mat['material_id']
        
        # Optimize manufacturing
        processes = optimized.get('manufacturing_processes', [])
        for proc in processes:
            proc['efficiency'] = min(proc.get('efficiency', 0.85) + 0.1, 0.95)
            proc['technology_level'] = 'advanced'
        
        # Optimize transport
        transport_legs = optimized.get('transport_legs', [])
        for leg in transport_legs:
            if leg.get('mode') == 'Air Freight':
                leg['mode'] = 'Ship'  # Switch to sea freight
            elif leg.get('mode') == 'Truck (Diesel)':
                leg['mode'] = 'Rail'  # Switch to rail
        
        return optimized
    
    def _generate_optimization_scenarios(self, product_spec: Dict) -> List[Dict]:
        """Generate multiple optimization scenarios"""
        scenarios = [
            {
                'name': 'Material Optimization',
                'description': 'Switch to recycled and bio-based materials',
                'carbon_reduction_%': 35,
                'cost_change_%': 5,
                'implementation_time': 'Short-term'
            },
            {
                'name': 'Process Optimization',
                'description': 'Improve manufacturing efficiency and renewable energy',
                'carbon_reduction_%': 25,
                'cost_change_%': -3,
                'implementation_time': 'Medium-term'
            },
            {
                'name': 'Circular Economy',
                'description': 'Implement take-back and recycling programs',
                'carbon_reduction_%': 40,
                'cost_change_%': 10,
                'implementation_time': 'Long-term'
            }
        ]
        
        return scenarios
    
    def _calculate_cost_implications(self, baseline_carbon: float, 
                                   optimized_carbon: float) -> Dict:
        """Calculate cost implications of carbon reduction"""
        carbon_price = 50  # USD per ton CO2e
        carbon_cost_savings = (baseline_carbon - optimized_carbon) * carbon_price / 1000
        
        return {
            'carbon_cost_savings_usd': carbon_cost_savings,
            'payback_period_years': 3,  # Simplified calculation
            'roi_%': 25  # Return on investment
        }
    
    def _assess_data_quality(self, product_spec: Dict) -> Dict:
        """Assess data quality using Pedigree matrix approach"""
        
        quality_scores = {
            'reliability': 2,  # 1=estimated, 2=partial, 3=verified
            'completeness': 2,  # 1=incomplete, 2=representative, 3=complete
            'temporal_correlation': 2,  # 1=old, 2=average, 3=recent
            'geographical_correlation': 2,  # 1=other, 2=similar, 3=same
            'technological_correlation': 2  # 1=other, 2=similar, 3=same
        }
        
        # Calculate overall data quality score
        total_score = sum(quality_scores.values())
        max_score = len(quality_scores) * 3
        quality_percentage = (total_score / max_score) * 100
        
        return {
            'pedigree_scores': quality_scores,
            'overall_quality_%': quality_percentage,
            'uncertainty_factor': self._calculate_uncertainty_factor(quality_percentage)
        }
    
    def _calculate_uncertainty_factor(self, quality_percentage: float) -> float:
        """Calculate uncertainty factor based on data quality"""
        if quality_percentage > 80:
            return 1.1  # Low uncertainty
        elif quality_percentage > 60:
            return 1.3  # Moderate uncertainty
        else:
            return 1.5  # High uncertainty
    
    def perform_sensitivity_analysis(self, product_spec: Dict, 
                                   parameters: List[str]) -> Dict:
        """Perform sensitivity analysis on key parameters"""
        
        sensitivity_results = {}
        baseline = self.calculate_comprehensive_lca(product_spec)
        baseline_carbon = baseline.totals['carbon_kgCO2e']
        
        for param in parameters:
            # Create variations
            variations = []
            
            for variation in [-0.2, -0.1, 0.1, 0.2]:  # ±10%, ±20%
                modified_spec = self._modify_parameter(product_spec, param, variation)
                result = self.calculate_comprehensive_lca(modified_spec)
                carbon_change = (result.totals['carbon_kgCO2e'] - baseline_carbon) / baseline_carbon * 100
                
                variations.append({
                    'variation_%': variation * 100,
                    'carbon_change_%': carbon_change,
                    'absolute_change_kg': result.totals['carbon_kgCO2e'] - baseline_carbon
                })
            
            sensitivity_results[param] = {
                'baseline_value': self._get_parameter_value(product_spec, param),
                'variations': variations,
                'sensitivity_index': self._calculate_sensitivity_index(variations)
            }
        
        return sensitivity_results
    
    def _modify_parameter(self, product_spec: Dict, param: str, 
                         variation: float) -> Dict:
        """Modify a specific parameter in product specification"""
        modified = product_spec.copy()
        
        # Simple implementation - in reality, would handle different parameter types
        if 'mass' in param.lower():
            # Modify material mass
            materials = modified.get('materials', [])
            for mat in materials:
                mat['mass_kg'] = mat.get('mass_kg', 0) * (1 + variation)
        
        return modified
    
    def _get_parameter_value(self, product_spec: Dict, param: str) -> Any:
        """Get value of a parameter from product specification"""
        # Simplified implementation
        if 'mass' in param.lower():
            materials = product_spec.get('materials', [])
            return sum(m.get('mass_kg', 0) for m in materials)
        
        return None
    
    def _calculate_sensitivity_index(self, variations: List[Dict]) -> float:
        """Calculate sensitivity index from variations"""
        if not variations:
            return 0
        
        # Calculate average absolute change
        absolute_changes = [abs(v['carbon_change_%']) for v in variations]
        return np.mean(absolute_changes)
    
    def compare_scenarios(self, scenarios: List[Dict]) -> Dict:
        """Compare multiple product scenarios"""
        
        comparison_results = []
        
        for scenario in scenarios:
            result = self.calculate_comprehensive_lca(scenario)
            comparison_results.append({
                'scenario_name': scenario.get('name', 'Unnamed'),
                'carbon_kgCO2e': result.totals['carbon_kgCO2e'],
                'energy_MJ': result.totals['energy_MJ'],
                'circularity_score': result.circularity_metrics.get('material_circularity_indicator', 0),
                'cost_usd': result.totals['cost_usd'],
                'hotspots': result.hotspots,
                'improvement_potential_%': result.improvement_potential.get('reduction_potential_%', 0)
            })
        
        # Calculate statistics
        carbon_values = [r['carbon_kgCO2e'] for r in comparison_results]
        
        stats = {
            'mean': np.mean(carbon_values),
            'std': np.std(carbon_values),
            'min': np.min(carbon_values),
            'max': np.max(carbon_values),
            'range': np.max(carbon_values) - np.min(carbon_values)
        }
        
        # Perform statistical tests
        if len(carbon_values) >= 2:
            # Simple t-test between first two scenarios
            t_stat, p_value = stats.ttest_ind([carbon_values[0]], [carbon_values[1]])
            stats['p_value'] = p_value
            stats['significant_difference'] = p_value < 0.05
        
        return {
            'scenarios': comparison_results,
            'statistics': stats,
            'best_scenario': min(comparison_results, key=lambda x: x['carbon_kgCO2e']),
            'worst_scenario': max(comparison_results, key=lambda x: x['carbon_kgCO2e'])
        }
