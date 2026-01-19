# ============================================================================
# PROFESSIONAL UI COMPONENTS
# ============================================================================
import streamlit as st
from typing import Dict, List, Optional, Any
from datetime import datetime

class ProfessionalHeader:
    """Professional header component"""
    
    @staticmethod
    def display():
        """Display professional header"""
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
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
        
        with col2:
            # Quick stats
            total_products = len(st.session_state.get('products', []))
            st.markdown(f"""
            <div style="text-align: center; padding: 0.5rem;">
                <div style="font-size: 1.5rem; color: var(--primary); font-weight: 700;">
                    {total_products}
                </div>
                <div style="font-size: 0.8rem; color: var(--gray);">
                    Products Analyzed
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # User info
            st.markdown("""
            <div style="text-align: right;">
                <div style="display: inline-block; background: var(--secondary); 
                          color: white; padding: 0.5rem 1rem; border-radius: 20px;
                          font-size: 0.9rem; font-weight: 600;">
                    Professional Edition
                </div>
            </div>
            """, unsafe_allow_html=True)

class SidebarNavigation:
    """Advanced sidebar navigation"""
    
    @staticmethod
    def display() -> str:
        """Display sidebar navigation and return selected view"""
        
        with st.sidebar:
            # User profile
            st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="width: 80px; height: 80px; background: linear-gradient(135deg, var(--primary), var(--secondary)); 
                          border-radius: 50%; margin: 0 auto 1rem auto; display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-size: 2rem;">👤</span>
                </div>
                <h4 style="color: var(--dark); margin: 0;">Professional User</h4>
                <p style="color: var(--gray); font-size: 0.8rem; margin: 0.25rem 0;">
                    {organization}
                </p>
                <div style="background: var(--accent); color: white; padding: 0.25rem 0.75rem; 
                          border-radius: 12px; font-size: 0.7rem; display: inline-block; margin-top: 0.5rem;">
                    Pro License Active
                </div>
            </div>
            """.format(
                organization=st.session_state.user.get('organization', 'No Organization')
            ), unsafe_allow_html=True)
            
            st.divider()
            
            # Navigation sections
            st.markdown("### 🎯 Analysis")
            
            view = st.radio(
                "Select View",
                [
                    "📊 Dashboard",
                    "🚀 Quick Assessment", 
                    "🔬 Detailed Analysis",
                    "📈 Compare Products",
                    "🔄 Optimization",
                    "🌍 Scenario Analysis"
                ],
                label_visibility="collapsed"
            )
            
            st.divider()
            
            st.markdown("### 📈 Analytics")
            
            analytics_view = st.radio(
                "Analytics Views",
                [
                    "📊 Analytics Dashboard",
                    "📄 Reports",
                    "🔍 Database Explorer"
                ],
                label_visibility="collapsed",
                key="analytics_nav"
            )
            
            st.divider()
            
            # Quick actions
            st.markdown("### ⚡ Quick Actions")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🆕 New", use_container_width=True):
                    st.session_state.current_workflow = "quick_assessment"
                    st.rerun()
            
            with col2:
                if st.button("📤 Export", use_container_width=True):
                    st.success("Export started!")
            
            st.divider()
            
            # Settings and help
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⚙️", help="Settings", use_container_width=True):
                    return 'settings'
            
            with col2:
                if st.button("❓", help="Help", use_container_width=True):
                    st.info("Help documentation coming soon!")
        
        # Map view names
        view_mapping = {
            "📊 Dashboard": "dashboard",
            "🚀 Quick Assessment": "quick_assessment",
            "🔬 Detailed Analysis": "detailed_analysis", 
            "📈 Compare Products": "comparison",
            "🔄 Optimization": "optimization",
            "🌍 Scenario Analysis": "scenarios",
            "📊 Analytics Dashboard": "analytics",
            "📄 Reports": "reports",
            "🔍 Database Explorer": "database"
        }
        
        selected_view = view_mapping.get(view, 'dashboard')
        
        # Handle analytics views
        if analytics_view != "📊 Analytics Dashboard":
            selected_view = view_mapping.get(analytics_view, 'analytics')
        
        return selected_view

class MetricDashboard:
    """Professional metric dashboard component"""
    
    @staticmethod
    def display_metrics(metrics: Dict[str, Any], layout: str = 'grid'):
        """Display metrics in professional format"""
        
        if layout == 'grid':
            cols = st.columns(len(metrics))
            
            for idx, (metric_name, metric_data) in enumerate(metrics.items()):
                with cols[idx]:
                    MetricDashboard._display_single_metric(metric_name, metric_data)
        
        elif layout == 'cards':
            for metric_name, metric_data in metrics.items():
                MetricDashboard._display_metric_card(metric_name, metric_data)
    
    @staticmethod
    def _display_single_metric(name: str, data: Dict):
        """Display single metric"""
        
        value = data.get('value', 0)
        unit = data.get('unit', '')
        change = data.get('change', None)
        trend = data.get('trend', 'neutral')
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{name}</div>
            <div class="metric-value">{value:,.1f}</div>
            <div style="color: var(--gray); font-size: 0.9rem;">{unit}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if change is not None:
            change_color = 'var(--accent)' if change >= 0 else 'var(--danger)'
            change_icon = '↗️' if change >= 0 else '↘️'
            st.caption(f"{change_icon} {change:+.1f}%")
    
    @staticmethod
    def _display_metric_card(name: str, data: Dict):
        """Display metric in card format"""
        
        value = data.get('value', 0)
        unit = data.get('unit', '')
        description = data.get('description', '')
        icon = data.get('icon', '📊')
        
        with st.container():
            st.markdown(f"""
            <div class="dashboard-card">
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <div style="font-size: 1.5rem; margin-right: 0.75rem;">{icon}</div>
                    <h3 style="color: var(--primary); margin: 0;">{name}</h3>
                </div>
                <div class="metric-value">{value:,.1f}</div>
                <div style="color: var(--gray); margin-bottom: 0.5rem;">{unit}</div>
                <p style="color: var(--gray); font-size: 0.9rem; margin: 0;">{description}</p>
            </div>
            """, unsafe_allow_html=True)

class WorkflowManager:
    """Workflow management component"""
    
    def __init__(self, workflow_name: str, steps: List[str]):
        self.workflow_name = workflow_name
        self.steps = steps
        self.current_step = st.session_state.get('workflow_step', 0)
    
    def display_header(self):
        """Display workflow header"""
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            <h2 style="color: var(--primary); margin-bottom: 0.5rem;">
                {self.workflow_name}
            </h2>
            <p style="color: var(--gray);">
                Step {self.current_step + 1} of {len(self.steps)}
            </p>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("Exit Workflow", use_container_width=True):
                st.session_state.current_workflow = None
                st.session_state.workflow_step = 0
                st.rerun()
    
    def display_progress(self):
        """Display progress indicator"""
        
        st.markdown('<div class="step-container">', unsafe_allow_html=True)
        
        cols = st.columns(len(self.steps))
        
        for i, step in enumerate(self.steps):
            with cols[i]:
                if i < self.current_step:
                    status = "completed"
                    icon = "✅"
                elif i == self.current_step:
                    status = "active"
                    icon = "⏳"
                else:
                    status = "inactive"
                    icon = "○"
                
                st.markdown(f"""
                <div class="step">
                    <div class="step-circle step-{status}">
                        {icon if i != self.current_step else i+1}
                    </div>
                    <div style="font-size: 0.9rem; color: {'var(--primary)' if i == self.current_step else 'var(--gray)'}">
                        {step}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.divider()
    
    def display_navigation(self, allow_back: bool = True):
        """Display navigation buttons"""
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if allow_back and self.current_step > 0:
                if st.button("← Back", use_container_width=True):
                    st.session_state.workflow_step -= 1
                    st.rerun()
        
        with col2:
            if self.current_step < len(self.steps) - 1:
                if st.button("Next →", use_container_width=True):
                    st.session_state.workflow_step += 1
                    st.rerun()
            else:
                if st.button("Finish", type="primary", use_container_width=True):
                    # Finish workflow
                    st.session_state.current_workflow = None
                    st.session_state.workflow_step = 0
                    st.rerun()
        
        with col3:
            # Save progress
            if st.button("💾 Save Progress", use_container_width=True):
                st.success("Progress saved!")

class ProgressTracker:
    """Progress tracking component"""
    
    @staticmethod
    def display_progress_bar(current: int, total: int, label: str = ""):
        """Display progress bar"""
        
        progress = current / total if total > 0 else 0
        
        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: var(--dark); font-weight: 600;">{label}</span>
                <span style="color: var(--gray);">{current}/{total} ({progress:.0%})</span>
            </div>
            <div style="height: 8px; background: var(--light); border-radius: 4px; overflow: hidden;">
                <div style="height: 100%; width: {progress * 100}%; 
                          background: linear-gradient(90deg, var(--secondary), var(--accent));">
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def display_status_indicator(status: str, message: str):
        """Display status indicator"""
        
        status_colors = {
            'success': 'var(--accent)',
            'warning': 'var(--warning)',
            'error': 'var(--danger)',
            'info': 'var(--secondary)'
        }
        
        status_icons = {
            'success': '✅',
            'warning': '⚠️',
            'error': '❌',
            'info': 'ℹ️'
        }
        
        color = status_colors.get(status, 'var(--gray)')
        icon = status_icons.get(status, '❓')
        
        st.markdown(f"""
        <div style="background: {color}10; border: 1px solid {color}30; 
                  border-radius: 10px; padding: 1rem; margin: 1rem 0;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="font-size: 1.2rem;">{icon}</div>
                <div style="color: var(--dark);">{message}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
