# ============================================================================
# UNCERTAINTY ANALYSIS MODULE
# ============================================================================
import numpy as np
from typing import Dict, List, Tuple, Any
from scipy import stats
import pandas as pd

class UncertaintyAnalyzer:
    """Advanced uncertainty analysis using Monte Carlo and Bayesian methods"""
    
    def __init__(self, n_iterations: int = 10000):
        self.n_iterations = n_iterations
        self.rng = np.random.default_rng(42)  # For reproducibility
    
    def monte_carlo_analysis(self, product_spec: Dict) -> Dict[str, Any]:
        """Perform comprehensive Monte Carlo uncertainty analysis"""
        
        results = {
            'carbon_distribution': [],
            'energy_distribution': [],
            'water_distribution': [],
            'sensitivity_coefficients': {},
            'confidence_intervals': {},
            'probability_of_meeting_targets': {}
        }
        
        # Run Monte Carlo simulations
        for _ in range(self.n_iterations):
            # Sample from uncertainty distributions
            sampled_carbon = self._sample_carbon_footprint(product_spec)
            sampled_energy = self._sample_energy_use(product_spec)
            sampled_water = self._sample_water_use(product_spec)
            
            results['carbon_distribution'].append(sampled_carbon)
            results['energy_distribution'].append(sampled_energy)
            results['water_distribution'].append(sampled_water)
        
        # Calculate statistics
        results.update(self._calculate_statistics(results))
        
        # Calculate sensitivity coefficients
        results['sensitivity_coefficients'] = self._calculate_sensitivity(product_spec)
        
        # Calculate confidence intervals
        results['confidence_intervals'] = self._calculate_confidence_intervals(results)
        
        # Calculate probability of meeting targets
        results['probability_of_meeting_targets'] = self._calculate_probabilities(
            results['carbon_distribution']
        )
        
        return results
    
    def _sample_carbon_footprint(self, product_spec: Dict) -> float:
        """Sample carbon footprint from uncertainty distributions"""
        
        total_carbon = 0
        
        # Material phase uncertainty
        materials = product_spec.get('materials', [])
        for mat in materials:
            material_id = mat.get('material_id', 'PP')
            mass = mat.get('mass_kg', 0)
            
            # Get material data with uncertainty
            material_data = self._get_material_with_uncertainty(material_id)
            
            # Sample from distribution
            carbon_factor = self.rng.normal(
                material_data['carbon_mean'],
                material_data['carbon_std']
            )
            
            total_carbon += mass * carbon_factor
        
        # Manufacturing uncertainty
        processes = product_spec.get('manufacturing_processes', [])
        for proc in processes:
            process_carbon = self._sample_process_carbon(proc)
            total_carbon += process_carbon
        
        # Transport uncertainty
        transport_legs = product_spec.get('transport_legs', [])
        for leg in transport_legs:
            transport_carbon = self._sample_transport_carbon(leg)
            total_carbon += transport_carbon
        
        return max(total_carbon, 0)  # Ensure non-negative
    
    def _get_material_with_uncertainty(self, material_id: str) -> Dict:
        """Get material data with uncertainty information"""
        # In reality, this would come from the database
        material_uncertainty = {
            'PP': {'carbon_mean': 2.1, 'carbon_std': 0.21},
            'PET': {'carbon_mean': 3.2, 'carbon_std': 0.32},
            'AL': {'carbon_mean': 8.2, 'carbon_std': 0.82}
        }
        
        return material_uncertainty.get(material_id, {'carbon_mean': 2.5, 'carbon_std': 0.25})
    
    def _sample_process_carbon(self, process: Dict) -> float:
        """Sample process carbon from uncertainty distribution"""
        # Simplified implementation
        process_types = {
            'Injection Molding': {'mean': 0.15, 'std': 0.015},
            'Assembly': {'mean': 0.03, 'std': 0.003}
        }
        
        process_name = process.get('process', 'Injection Molding')
        process_data = process_types.get(process_name, {'mean': 0.1, 'std': 0.01})
        
        return self.rng.normal(process_data['mean'], process_data['std'])
    
    def _sample_transport_carbon(self, transport_leg: Dict) -> float:
        """Sample transport carbon from uncertainty distribution"""
        # Simplified implementation
        return self.rng.normal(0.1, 0.01)  # Placeholder
    
    def _calculate_statistics(self, results: Dict) -> Dict:
        """Calculate statistical measures from distributions"""
        
        stats = {}
        
        for key, distribution in results.items():
            if 'distribution' in key and distribution:
                dist_array = np.array(distribution)
                
                stats[key.replace('_distribution', '_stats')] = {
                    'mean': float(np.mean(dist_array)),
                    'median': float(np.median(dist_array)),
                    'std': float(np.std(dist_array)),
                    'cv': float(np.std(dist_array) / np.mean(dist_array) if np.mean(dist_array) > 0 else 0),
                    'skewness': float(stats.skew(dist_array)),
                    'kurtosis': float(stats.kurtosis(dist_array)),
                    'min': float(np.min(dist_array)),
                    'max': float(np.max(dist_array)),
                    'range': float(np.max(dist_array) - np.min(dist_array))
                }
        
        return stats
    
    def _calculate_sensitivity(self, product_spec: Dict) -> Dict:
        """Calculate sensitivity coefficients using Sobol indices"""
        
        # This is a simplified implementation
        # In reality, would use proper Sobol sequence or Fourier Amplitude Sensitivity Test
        
        sensitivity = {}
        
        # Material sensitivity
        materials = product_spec.get('materials', [])
        total_mass = sum(m.get('mass_kg', 0) for m in materials)
        
        for i, mat in enumerate(materials):
            mass = mat.get('mass_kg', 0)
            if total_mass > 0:
                sensitivity[f'material_{i}_mass'] = {
                    'parameter': f'Material {i} Mass',
                    'sensitivity_index': mass / total_mass,
                    'contribution_%': (mass / total_mass) * 100
                }
        
        return sensitivity
    
    def _calculate_confidence_intervals(self, results: Dict) -> Dict:
        """Calculate confidence intervals for key metrics"""
        
        intervals = {}
        
        for key, distribution in results.items():
            if 'distribution' in key and distribution:
                dist_array = np.array(distribution)
                
                intervals[key.replace('_distribution', '_ci')] = {
                    '90_ci': self._calculate_percentile_interval(dist_array, 90),
                    '95_ci': self._calculate_percentile_interval(dist_array, 95),
                    '99_ci': self._calculate_percentile_interval(dist_array, 99)
                }
        
        return intervals
    
    def _calculate_percentile_interval(self, data: np.ndarray, 
                                      confidence: float) -> Tuple[float, float]:
        """Calculate percentile-based confidence interval"""
        alpha = (100 - confidence) / 2
        lower = np.percentile(data, alpha)
        upper = np.percentile(data, 100 - alpha)
        return (float(lower), float(upper))
    
    def _calculate_probabilities(self, carbon_distribution: List[float]) -> Dict:
        """Calculate probabilities of meeting various targets"""
        
        carbon_array = np.array(carbon_distribution)
        
        # Define targets (in kg CO2e)
        targets = {
            'carbon_neutral': 0,
            'science_based_target': np.percentile(carbon_array, 20),  # Top 20%
            'industry_average': np.median(carbon_array),
            'regulatory_limit': np.percentile(carbon_array, 90)  # 90th percentile
        }
        
        probabilities = {}
        for target_name, target_value in targets.items():
            probability = np.mean(carbon_array <= target_value) * 100
            probabilities[target_name] = {
                'target_value': float(target_value),
                'probability_%': float(probability),
                'meets_target': probability >= 50
            }
        
        return probabilities
    
    def bayesian_uncertainty_propagation(self, product_spec: Dict) -> Dict:
        """Perform Bayesian uncertainty propagation"""
        
        # This would implement Bayesian methods for uncertainty propagation
        # Using Markov Chain Monte Carlo (MCMC) or Variational Inference
        
        return {
            'posterior_distributions': {},
            'credible_intervals': {},
            'model_evidence': 0,
            'convergence_metrics': {}
        }
    
    def scenario_based_uncertainty(self, product_spec: Dict, 
                                  scenarios: List[Dict]) -> Dict:
        """Perform scenario-based uncertainty analysis"""
        
        scenario_results = []
        
        for scenario in scenarios:
            # Modify product specification based on scenario
            modified_spec = self._apply_scenario(product_spec, scenario)
            
            # Calculate LCA for scenario
            scenario_carbon = self._sample_carbon_footprint(modified_spec)
            
            scenario_results.append({
                'scenario_name': scenario.get('name', 'Unnamed'),
                'scenario_description': scenario.get('description', ''),
                'carbon_kgCO2e': scenario_carbon,
                'probability': scenario.get('probability', 0.25)
            })
        
        # Calculate expected value and variance
        carbon_values = [r['carbon_kgCO2e'] for r in scenario_results]
        probabilities = [r['probability'] for r in scenario_results]
        
        expected_value = np.average(carbon_values, weights=probabilities)
        variance = np.average((carbon_values - expected_value) ** 2, weights=probabilities)
        
        return {
            'scenarios': scenario_results,
            'expected_value': expected_value,
            'variance': variance,
            'standard_deviation': np.sqrt(variance),
            'scenario_robustness': self._assess_scenario_robustness(scenario_results)
        }
    
    def _apply_scenario(self, product_spec: Dict, scenario: Dict) -> Dict:
        """Apply scenario modifications to product specification"""
        modified = product_spec.copy()
        
        # Apply scenario-specific modifications
        if 'material_change' in scenario:
            modified['materials'] = scenario['material_change']
        
        if 'efficiency_improvement' in scenario:
            processes = modified.get('manufacturing_processes', [])
            for proc in processes:
                proc['efficiency'] = min(
                    proc.get('efficiency', 0.85) * (1 + scenario['efficiency_improvement']),
                    0.95
                )
        
        return modified
    
    def _assess_scenario_robustness(self, scenario_results: List[Dict]) -> Dict:
        """Assess robustness of different scenarios"""
        
        # Calculate robustness metrics
        carbon_values = [r['carbon_kgCO2e'] for r in scenario_results]
        
        robustness = {
            'range': np.max(carbon_values) - np.min(carbon_values),
            'cv': np.std(carbon_values) / np.mean(carbon_values) if np.mean(carbon_values) > 0 else 0,
            'worst_case': np.max(carbon_values),
            'best_case': np.min(carbon_values),
            'regret': np.max(carbon_values) - np.min(carbon_values)  # Maximum regret
        }
        
        return robustness
    
    def create_uncertainty_report(self, uncertainty_results: Dict) -> str:
        """Create comprehensive uncertainty report"""
        
        report = "# Uncertainty Analysis Report\n\n"
        
        report += "## Executive Summary\n"
        report += f"Monte Carlo simulations: {self.n_iterations:,} iterations\n"
        
        if 'carbon_stats' in uncertainty_results:
            stats = uncertainty_results['carbon_stats']
            report += f"Carbon footprint: {stats['mean']:.1f} ± {stats['std']:.1f} kg CO₂e (CV: {stats['cv']:.2%})\n"
        
        report += "\n## Key Findings\n"
        
        if 'confidence_intervals' in uncertainty_results:
            ci = uncertainty_results['confidence_intervals'].get('carbon_ci', {})
            if '95_ci' in ci:
                lower, upper = ci['95_ci']
                report += f"- 95% confidence interval: [{lower:.1f}, {upper:.1f}] kg CO₂e\n"
        
        if 'probability_of_meeting_targets' in uncertainty_results:
            probs = uncertainty_results['probability_of_meeting_targets']
            report += "\n## Probability of Meeting Targets\n"
            for target, data in probs.items():
                report += f"- {target}: {data['probability_%']:.1f}% probability\n"
        
        report += "\n## Recommendations\n"
        report += "1. Focus on parameters with high sensitivity coefficients\n"
        report += "2. Consider worst-case scenarios in decision making\n"
        report += "3. Regularly update uncertainty estimates with new data\n"
        
        return report
