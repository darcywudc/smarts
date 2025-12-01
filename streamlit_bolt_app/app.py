import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from physics import BoltPhysics
import streamlit.components.v1 as components

st.set_page_config(page_title="Advanced Bolt FEA Simulation", layout="wide", page_icon="🔩")

# --- Custom CSS ---
st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
    }
    .metric-card {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: #00f2ff; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Configuration ---
st.sidebar.title("⚙️ Configuration")

selected_material = st.sidebar.selectbox("Material", list(BoltPhysics.MATERIALS.keys()))
mat_props = BoltPhysics.MATERIALS[selected_material]

st.sidebar.subheader("Dimensions")
diameter = st.sidebar.slider("Diameter (M-size) [mm]", 5, 50, 20)
length = st.sidebar.slider("Total Length [mm]", 20, 200, 100)
shank_length = st.sidebar.slider("Shank Length [mm]", 0, int(length*0.8), int(length*0.4))

st.sidebar.subheader("Load Conditions")
force = st.sidebar.number_input("Tensile Force [N]", 0, 1000000, 50000, step=1000)

# --- Calculations ---
nominal_stress = BoltPhysics.calculate_stress(diameter, force)
deformation = BoltPhysics.calculate_deformation(length, nominal_stress, mat_props['E'])
yield_strength = mat_props['Yield']
safety_factor = yield_strength / nominal_stress if nominal_stress > 0 else 999

# Simulated FEA Profile
y_pos, stress_dist = BoltPhysics.simulate_stress_distribution(length, shank_length, nominal_stress)
max_stress = np.max(stress_dist) if len(stress_dist) > 0 else 0


# --- Tabs ---
tab1, tab2 = st.tabs(["📊 Analysis Dashboard", "🧊 3D Simulation"])

with tab1:
    st.title("🔩 Bolt Structural Analysis")

    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Applied Load", f"{force/1000:.1f} kN")
    with col2:
        st.metric("Nominal Stress", f"{nominal_stress:.1f} MPa")
    with col3:
        st.metric("Deformation", f"{deformation:.3f} mm")
    with col4:
        delta = safety_factor - 1.0
        color = "normal" if safety_factor > 1.2 else "inverse"
        st.metric("Safety Factor", f"{safety_factor:.2f}", delta_color=color)

    # Status Alert
    if safety_factor < 1.0:
        st.error(f"⚠️ FAILURE PREDICTED! Stress ({max_stress:.1f} MPa peak) exceeds Yield Strength ({yield_strength} MPa).")
    elif safety_factor < 1.2:
        st.warning("⚠️ CRITICAL ZONE! Low Safety Factor.")
    else:
        st.success("✅ SAFE DESIGN.")

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Stress Distribution (Simulated FEA)")
        df_stress = pd.DataFrame({"Position (mm)": y_pos, "Stress (MPa)": stress_dist})

        fig_stress = go.Figure()
        fig_stress.add_trace(go.Scatter(x=df_stress["Position (mm)"], y=df_stress["Stress (MPa)"],
                                      mode='lines', name='Von Mises Stress',
                                      line=dict(color='red', width=3)))
        # Yield Line
        fig_stress.add_hline(y=yield_strength, line_dash="dash", line_color="orange", annotation_text="Yield Limit")

        fig_stress.update_layout(
            title="Axial Stress Profile",
            xaxis_title="Position along Bolt (mm)",
            yaxis_title="Stress (MPa)",
            template="plotly_dark",
            height=400
        )
        st.plotly_chart(fig_stress, use_container_width=True)

    with col_chart2:
        st.subheader("Material Stress-Strain Curve")
        strain_limit = 0.02 # 2%
        strain_points = np.linspace(0, strain_limit, 50)
        # Bilinear model roughly
        stress_points = np.minimum(strain_points * mat_props['E'], mat_props['Yield'] + (strain_points - (mat_props['Yield']/mat_props['E'])) * (mat_props['E']*0.05))
        stress_points = [min(s, mat_props['Tensile']) for s in stress_points]

        current_strain = nominal_stress / mat_props['E']

        fig_ss = go.Figure()
        fig_ss.add_trace(go.Scatter(x=strain_points*100, y=stress_points, mode='lines', name='Material Response'))
        fig_ss.add_trace(go.Scatter(x=[current_strain*100], y=[nominal_stress], mode='markers', marker=dict(color='red', size=10), name='Current State'))

        fig_ss.update_layout(
            title=f"{selected_material} Response",
            xaxis_title="Strain (%)",
            yaxis_title="Stress (MPa)",
            template="plotly_dark",
            height=400
        )
        st.plotly_chart(fig_ss, use_container_width=True)

with tab2:
    st.header("Real-time 3D Simulation")
    # We embed the HTML/JS for Three.js here
    # We pass the dynamic values into the HTML string

    # Calculate colors for 3D viz based on stress
    # Normalized stress for visualization (0 to 1 based on yield)
    stress_ratio = min(max_stress / (yield_strength * 1.5), 1.0)

    bolt_color_hex = mat_props['Color'].replace('#', '0x')

    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ margin: 0; overflow: hidden; background-color: #0e1117; }}
            canvas {{ width: 100%; height: 600px; }}
        </style>
        <script type="importmap">
            {{
                "imports": {{
                    "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
                    "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
                }}
            }}
        </script>
    </head>
    <body>
        <div id="container"></div>
        <script type="module">
            import * as THREE from 'three';
            import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js';

            // Parameters from Streamlit
            const params = {{
                headRadius: {diameter * 0.9},
                headHeight: {diameter * 0.6},
                shankRadius: {diameter / 2},
                length: {length},
                shankLength: {shank_length},
                stressRatio: {stress_ratio},
                deformation: {deformation * 20}, // Exaggerated for viz
                baseColor: {bolt_color_hex}
            }};

            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0e1117);

            const camera = new THREE.PerspectiveCamera(45, window.innerWidth / 600, 0.1, 1000);
            camera.position.set(params.length * 1.5, params.length * 1.2, params.length * 1.5);
            camera.lookAt(0, -params.length/2, 0);

            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(window.innerWidth, 600);
            document.getElementById('container').appendChild(renderer.domElement);

            const controls = new OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;

            // Lights
            const ambient = new THREE.AmbientLight(0x404040, 2);
            scene.add(ambient);
            const dirLight = new THREE.DirectionalLight(0xffffff, 2);
            dirLight.position.set(50, 50, 50);
            scene.add(dirLight);

            // Material
            // We use vertex colors for stress map
            const material = new THREE.MeshStandardMaterial({{
                color: 0xffffff,
                vertexColors: true,
                metalness: 0.6,
                roughness: 0.4
            }});

            // Geometry construction
            // Head
            const headGeo = new THREE.CylinderGeometry(params.headRadius, params.headRadius, params.headHeight, 6);
            headGeo.translate(0, params.headHeight/2, 0);

            // Shaft (Shank + Thread)
            // High segmentation for color mapping
            const shaftGeo = new THREE.CylinderGeometry(params.shankRadius, params.shankRadius, params.length, 32, 64, true);
            shaftGeo.translate(0, -params.length/2, 0);

            // Color Mapping Logic
            const pos = shaftGeo.attributes.position;
            const colors = [];
            const color = new THREE.Color();

            // Define stress zones
            const threadStart = -params.shankLength;

            for(let i=0; i < pos.count; i++){
                const y = pos.getY(i);

                let localStress = 0;

                // FEA Simulation approximation logic for visuals
                if (y > threadStart + 2) {{
                    localStress = params.stressRatio * 0.3; // Low stress in shank
                }} else if (y > threadStart - (params.length * 0.1)) {{
                    // Concentration zone
                    localStress = params.stressRatio; // Peak
                }} else {{
                    localStress = params.stressRatio * 0.5; // Threads
                }}

                // Add noise
                localStress += (Math.random()-0.5) * 0.05 * params.stressRatio;
                localStress = Math.min(Math.max(localStress, 0), 1);

                // Map to Blue -> Red
                const hue = (1.0 - localStress) * 0.66; // Blue is 0.66
                color.setHSL(hue, 1.0, 0.5);

                colors.push(color.r, color.g, color.b);
            }

            shaftGeo.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

            // Head color (uniform low stress usually)
            const headColors = [];
            for(let i=0; i < headGeo.attributes.position.count; i++){
                headColors.push(0.2, 0.2, 0.8); // Blueish
            }
            headGeo.setAttribute('color', new THREE.Float32BufferAttribute(headColors, 3));


            const headMesh = new THREE.Mesh(headGeo, material);
            const shaftMesh = new THREE.Mesh(shaftGeo, material);

            // Apply deformation scale
            // Simple Y stretch
            const stretch = 1 + (params.deformation / params.length);
            shaftMesh.scale.setY(stretch);
            // Move shaft down slightly to keep attached to head?
            // Head is at 0 upwards. Shaft is 0 downwards.
            // If we stretch shaft, it grows downwards, which is correct.

            scene.add(headMesh);
            scene.add(shaftMesh);

            function animate() {{
                requestAnimationFrame(animate);
                controls.update();
                renderer.render(scene, camera);
            }}
            animate();

            // Handle Resize
             window.addEventListener('resize', () => {{
                camera.aspect = window.innerWidth / 600;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, 600);
            }});
        </script>
    </body>
    </html>
    """

    components.html(html_code, height=600)
