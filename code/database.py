# ============================================================================
# ADVANCED LCA DATABASE
# ============================================================================
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import json
from datetime import datetime
import sqlite3
from pathlib import Path
import hashlib

class AdvancedLCADatabase:
    """Advanced LCA database with multiple data sources and uncertainty modeling"""
    
    def __init__(self, db_path: str = "data/lca_database.db"):
        self.db_path = db_path
        self._initialize_database()
        self._load_databases()
        
    def _initialize_database(self):
        """Initialize SQLite database"""
        Path("data").mkdir(exist_ok=True)
        
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._create_tables()
    
    def _create_tables(self):
        """Create database tables"""
        cursor = self.conn.cursor()
        
        # Materials table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS materials (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            density_kg_m3 REAL,
            embodied_energy_MJ_kg REAL,
            embodied_energy_std REAL,
            carbon_footprint_kgCO2e_kg REAL,
            carbon_footprint_std REAL,
            water_use_L_kg REAL,
            recyclability_rate REAL,
            recycled_content_potential REAL,
            price_usd_kg REAL,
            mechanical_strength_MPa REAL,
            thermal_conductivity_W_mK REAL,
            source TEXT,
            uncertainty_level INTEGER,
            last_updated TIMESTAMP
        )
        ''')
        
        # Processes table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS processes (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            energy_kWh_kg REAL,
            carbon_kgCO2e_kg REAL,
            scrap_rate REAL,
            water_use_L_kg REAL,
            efficiency_range_min REAL,
            efficiency_range_max REAL,
            source TEXT
        )
        ''')
        
        # Transport table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transport (
            id TEXT PRIMARY KEY,
            mode TEXT NOT NULL,
            carbon_gCO2e_tonne_km REAL,
            energy_MJ_tonne_km REAL,
            cost_usd_tonne_km REAL,
            speed_km_h REAL,
            capacity_tonne REAL,
            technology TEXT,
            source TEXT
        )
        ''')
        
        # Regional factors
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS regional_factors (
            region TEXT PRIMARY KEY,
            carbon_gCO2e_kWh REAL,
            renewable_share REAL,
            grid_mix_json TEXT,
            year INTEGER,
            source TEXT
        )
        ''')
        
        self.conn.commit()
    
    def _load_databases(self):
        """Load comprehensive LCA databases"""
        self._load_materials_database()
        self._load_processes_database()
        self._load_transport_database()
        self._load_regional_factors()
        self._load_circularity_metrics()
    
    def _load_materials_database(self):
        """Load comprehensive materials database"""
        materials_data = [
            # Polymers
            {
                'id': 'PP', 'name': 'Polypropylene', 'category': 'Polymer',
                'density': 905, 'embodied_energy': 85.6, 'embodied_energy_std': 3.2,
                'carbon': 2.1, 'carbon_std': 0.1, 'water': 75,
                'recyclability': 0.85, 'recycled_potential': 0.30,
                'price': 1.8, 'strength': 35, 'conductivity': 0.22,
                'source': 'Ecoinvent 3.8'
            },
            # Add 50+ more materials...
        ]
        
        for mat in materials_data:
            self.add_material(mat)
    
    def add_material(self, material_data: Dict):
        """Add material to database"""
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO materials VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            material_data['id'],
            material_data['name'],
            material_data.get('category', 'Unknown'),
            material_data.get('density', 0),
            material_data.get('embodied_energy', 0),
            material_data.get('embodied_energy_std', 0),
            material_data.get('carbon', 0),
            material_data.get('carbon_std', 0),
            material_data.get('water', 0),
            material_data.get('recyclability', 0.5),
            material_data.get('recycled_potential', 0),
            material_data.get('price', 0),
            material_data.get('strength', 0),
            material_data.get('conductivity', 0),
            material_data.get('source', 'Unknown'),
            material_data.get('uncertainty_level', 2),
            datetime.now()
        ))
        self.conn.commit()
    
    def get_material(self, material_id: str) -> Optional[Dict]:
        """Get material by ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM materials WHERE id = ?', (material_id,))
        row = cursor.fetchone()
        
        if row:
            return {
                'id': row[0], 'name': row[1], 'category': row[2],
                'density': row[3], 'embodied_energy': row[4], 'embodied_energy_std': row[5],
                'carbon_footprint': row[6], 'carbon_std': row[7], 'water_use': row[8],
                'recyclability': row[9], 'recycled_potential': row[10],
                'price': row[11], 'strength': row[12], 'conductivity': row[13]
            }
        return None
    
    def search_materials(self, 
                        category: Optional[str] = None,
                        max_carbon: Optional[float] = None,
                        min_recyclability: Optional[float] = None,
                        max_price: Optional[float] = None) -> List[Dict]:
        """Search materials with filters"""
        query = "SELECT * FROM materials WHERE 1=1"
        params = []
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if max_carbon:
            query += " AND carbon_footprint_kgCO2e_kg <= ?"
            params.append(max_carbon)
        
        if min_recyclability:
            query += " AND recyclability_rate >= ?"
            params.append(min_recyclability)
        
        if max_price:
            query += " AND price_usd_kg <= ?"
            params.append(max_price)
        
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        
        materials = []
        for row in cursor.fetchall():
            materials.append({
                'id': row[0], 'name': row[1], 'category': row[2],
                'carbon': row[6], 'recyclability': row[9], 'price': row[11]
            })
        
        return materials
    
    def get_materials_dataframe(self) -> pd.DataFrame:
        """Get all materials as DataFrame"""
        query = """
        SELECT 
            id, name, category, 
            density_kg_m3, 
            embodied_energy_MJ_kg, 
            carbon_footprint_kgCO2e_kg,
            water_use_L_kg,
            recyclability_rate,
            price_usd_kg,
            mechanical_strength_MPa
        FROM materials
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_similar_materials(self, material_id: str, n: int = 5) -> List[Dict]:
        """Find similar materials based on properties"""
        target = self.get_material(material_id)
        if not target:
            return []
        
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM materials WHERE id != ?', (material_id,))
        
        similarities = []
        for row in cursor.fetchall():
            mat = {
                'id': row[0], 'name': row[1], 'category': row[2],
                'density': row[3], 'embodied_energy': row[4], 'carbon': row[6],
                'recyclability': row[9], 'price': row[11], 'strength': row[12]
            }
            
            # Calculate similarity score
            score = self._calculate_material_similarity(target, mat)
            similarities.append((mat, score))
        
        # Sort by similarity and return top n
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [mat for mat, _ in similarities[:n]]
    
    def _calculate_material_similarity(self, mat1: Dict, mat2: Dict) -> float:
        """Calculate similarity between two materials"""
        # Weighted similarity based on key properties
        weights = {
            'category': 0.3,
            'strength': 0.25,
            'density': 0.15,
            'price': 0.15,
            'carbon': 0.15
        }
        
        score = 0
        
        if mat1['category'] == mat2['category']:
            score += weights['category']
        
        # Normalize and compare numerical properties
        strength_diff = abs(mat1.get('strength', 0) - mat2.get('strength', 0))
        if strength_diff > 0:
            strength_sim = 1 / (1 + strength_diff / 100)
            score += weights['strength'] * strength_sim
        
        density_diff = abs(mat1.get('density', 0) - mat2.get('density', 0))
        if density_diff > 0:
            density_sim = 1 / (1 + density_diff / 100)
            score += weights['density'] * density_sim
        
        return score
    
    def get_processes_dataframe(self) -> pd.DataFrame:
        """Get all processes as DataFrame"""
        query = "SELECT * FROM processes"
        return pd.read_sql_query(query, self.conn)
    
    def get_transport_dataframe(self) -> pd.DataFrame:
        """Get all transport modes as DataFrame"""
        query = "SELECT * FROM transport"
        return pd.read_sql_query(query, self.conn)
    
    def get_regional_factors(self) -> Dict:
        """Get regional emission factors"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM regional_factors')
        
        factors = {}
        for row in cursor.fetchall():
            factors[row[0]] = {
                'carbon_gCO2e_kWh': row[1],
                'renewable_share': row[2],
                'grid_mix': json.loads(row[3]) if row[3] else {},
                'year': row[4],
                'source': row[5]
            }
        return factors
    
    def get_circularity_metrics(self) -> Dict:
        """Get circular economy metrics"""
        return {
            'Material Circularity Indicator (MCI)': {
                'formula': 'MCI = (Functional Use + M_F_linear) / (M_F_linear + M_V_linear + M_L)',
                'description': 'Ellen MacArthur Foundation metric',
                'weighting': {'virgin_material': 0.4, 'recycling_rate': 0.3, 'lifetime': 0.3},
                'thresholds': {'linear': 0, 'transitional': 0.5, 'circular': 1}
            },
            'Recycling Efficiency': {
                'formula': 'E_recycle = (Mass_recycled / Mass_total) * Efficiency_factor',
                'description': 'Efficiency of recycling process',
                'thresholds': {'poor': 0.5, 'good': 0.7, 'excellent': 0.9}
            },
            'Reuse Potential': {
                'description': 'Potential for product/components to be reused',
                'factors': ['Modularity', 'Durability', 'Ease of disassembly']
            }
        }
    
    def import_external_database(self, file_path: str, db_type: str):
        """Import external LCA database"""
        # Implementation for importing Ecoinvent, Agribalyse, etc.
        pass
    
    def export_database(self, format: str = 'csv') -> Dict[str, pd.DataFrame]:
        """Export database in specified format"""
        tables = {
            'materials': self.get_materials_dataframe(),
            'processes': self.get_processes_dataframe(),
            'transport': self.get_transport_dataframe()
        }
        
        return tables
