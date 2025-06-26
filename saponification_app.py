
import streamlit as st
import numpy as np
from scipy.integrate import odeint
import plotly.graph_objs as go

# Page setup
st.set_page_config(page_title="🔪 Saponification Simulator", layout="wide")

# Tab layout
tab1, tab2, tab3, tab4 = st.tabs(["📘 Overview", "📐 Theory", "🧪 Simulation", "📚 References"])

# ------------------------------
# 📘 Tab 1: Overview

from PIL import Image

with tab1:
    st.header("📘 Overview")

    st.markdown("""
    **Saponification** is a chemical reaction in which **ethyl acetate** reacts with **sodium hydroxide (NaOH)** to produce:

    - **Sodium acetate (CH₃COONa)**
    - **Ethanol (C₂H₅OH)**
    """)

    st.markdown("#### Reaction (Triglyceride Saponification):")

    # Add scrollable image
    st.markdown(
        """
        <div style="overflow-x: auto; white-space: nowrap;">
            <img src="http://www.chem.latech.edu/~deddy/chem122m/SOAP01.gif" style="height: 220px;" />
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("📜 *Saponification Reaction* — Triglyceride + NaOH → Glycerol + Soap (Sodium salt of fatty acid)")

    st.markdown("""
    This simulator allows users to visualize how different parameters affect **NaOH concentration** and **reaction kinetics** during this process.
    """)



# ------------------------------
# 📐 Tab 2: Theory
from PIL import Image

with tab2:
    st.header("📐 Theory & Kinetics")

    st.markdown("""
The reaction is modeled as a **second-order** irreversible reaction with equal initial concentrations:
""")

    st.latex(r"- \frac{dC}{dt} = k C^2")

    image1 = Image.open("Integrated.png")
    st.image(image1, caption="Second-Order Integrated Rate Law", use_container_width=True)

    st.markdown("### Arrhenius Equation:")

    st.latex(r"k = A \cdot e^{\frac{-E_a}{RT}}")

    image2 = Image.open("arrhenius.png")
    st.image(image2, caption="Arrhenius Equation and Activation Energy", use_container_width=True)

    st.markdown("""
**Where:**
- \( A \): Frequency factor (1/s)  
- \( E_a \): Activation energy (J/mol)  
- \( R \): Gas constant (8.314 J/mol·K)  
- \( T \): Temperature (K)  
""")



# ------------------------------
# 🧪 Tab 3: Simulation
with tab3:
    st.header("🧪 Saponification Simulation")

    st.sidebar.header("🔧 Simulation Controls")
    parameter = st.sidebar.selectbox("Select Parameter to Analyze", ["Temperature", "Volume", "Agitation Rate", "Initial Concentration"])
    A_input = st.sidebar.number_input("Frequency Factor A (1/s)", value=0.5)
    Ea_input = st.sidebar.number_input("Activation Energy Ea (J/mol)", value=43094.0)
    T_sim = st.sidebar.number_input("Simulation Temperature (K)", value=298.0)

    R = 8.314
    k_sim = A_input * np.exp(-Ea_input / (R * T_sim))
    st.sidebar.markdown(f"<div class='metric-label'>Calculated Rate Constant (k):</div><div class='metric-value'>{k_sim:.2e} L/mol·s</div>", unsafe_allow_html=True)

    if k_sim > 1:
        st.warning("⚠️ The calculated rate constant is very high. Simulation results may drop instantly to zero. Try reducing A or Ea.")

    # ✅ Moved outside any block
    data_sets = {
        "Temperature": {
            "293K": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0333, 0.0233, 0.0178, 0.0156, 0.0144, 0.0125]),
            "303K": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0256, 0.0189, 0.0144, 0.0122, 0.0100, 0.0078]),
            "313K": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0200, 0.0133, 0.0100, 0.0083, 0.0067, 0.0061])
        },
        "Volume": {
            "1.2L": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0222, 0.0156, 0.0128, 0.0100, 0.0089, 0.0083]),
            "1.4L": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0289, 0.0222, 0.0178, 0.0156, 0.0144, 0.0133]),
            "1.8L": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.067, 0.0289, 0.0256, 0.0222, 0.0200, 0.0167])
        },
        "Agitation Rate": {
            "70rpm": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0189, 0.0133, 0.0100, 0.0078, 0.0067, 0.0056]),
            "110rpm": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0256, 0.0189, 0.0156, 0.0128, 0.0111, 0.0100]),
            "150rpm": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0333, 0.0267, 0.0222, 0.0200, 0.0178, 0.0156])
        },
        "Initial Concentration": {
            "0.025M": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0360, 0.0260, 0.0200, 0.0160, 0.0120, 0.0111]),
            "0.050M": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0389, 0.0300, 0.0244, 0.0211, 0.0189, 0.0167]),
            "0.075M": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0392, 0.0313, 0.0256, 0.0222, 0.0200, 0.0178])
        }
    }

    fig = go.Figure()
    exp_colors = ['red', 'green', 'blue']
    sim_colors = ['orange', 'lime', 'deepskyblue']

    for i, (label, (time_exp, conc_exp)) in enumerate(data_sets[parameter].items()):
        time_exp_min = np.array(time_exp) / 60
        conc_exp = np.array(conc_exp)

        # Experimental curve
        fig.add_trace(go.Scatter(
            x=time_exp_min,
            y=conc_exp,
            mode='lines+markers',
            name=f"Exp {label}",
            line=dict(color=exp_colors[i], width=2),
            marker=dict(size=6),
            hovertemplate=f"{label} Exp<br>Time: %{{x}} min<br>[NaOH]: %{{y:.4f}} mol/L<extra></extra>"
        ))

        # Simulated curve
        def ode_model(C, t, k): return -k * C**2
        C0 = conc_exp[0]
        time_sim_sec = np.array(time_exp)

        try:
            temp_val = int(label.replace("K", ""))
            k_temp = A_input * np.exp(-Ea_input / (R * temp_val))
        except:
            k_temp = k_sim

        conc_sim = odeint(ode_model, C0, time_sim_sec, args=(k_temp,))
        time_sim_min = time_sim_sec / 60

        fig.add_trace(go.Scatter(
            x=time_sim_min,
            y=conc_sim.flatten(),
            mode='lines+markers',
            name=f"Sim {label}",
            line=dict(color=sim_colors[i], width=2, dash='dash'),
            marker=dict(symbol='circle-open', size=6),
            opacity=0.85,
            hovertemplate=f"{label} Sim<br>Time: %{{x}} min<br>[NaOH]: %{{y:.4f}} mol/L<extra></extra>"
        ))

    fig.update_layout(
        title=f"[NaOH] vs Time — Effect of {parameter}",
        xaxis_title="Time (minutes)",
        yaxis_title="[NaOH] (mol/L)",
        legend_title=parameter,
        template="plotly_white",
        hovermode="x unified",
        font=dict(size=14)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""---  
    ✅ **Experimental data** from *Al Mesfer et al., 2017*  
    🔍 Hover on points to inspect values.
    """)

# ------------------------------
# 📚 Tab 4: References
with tab4:
    st.header("📚 References")
    st.markdown("""
    - Al Mesfer, M. K. (2017). *Experimental Study of Batch Reactor Performance for Ethyl Acetate Saponification*, International Journal of Chemical Reactor Engineering. [DOI:10.1515/ijcre-2016-0174](https://doi.org/10.1515/ijcre-2016-0174)
    - Fogler, H. S. (2006). *Elements of Chemical Reaction Engineering*.
    - Bursali, N., Ertunc, S., & Akay, B. (2006). *Chem. Eng. Process*, 45, 980–989.
    """)
st.subheader("📝 Summary Highlights")
st.markdown("""
- **Al Mesfer (2017)**: Studied ethyl acetate saponification in a batch reactor using NaOH.
- Found temperature has a strong inverse effect on NaOH concentration over time.
- Used conductivity to track NaOH consumption and validated second-order kinetics.
""")

st.markdown(
    """
    <hr style="margin-top: 3em; margin-bottom: 1em;">
    <div style='text-align: center; font-size: 14px; color: grey;'>
        Made with ❤️ by <b>Akshad Gajapure</b> & <b>Mahesh Reddy </b> | NIT Raipur
    </div>
    """,
    unsafe_allow_html=True
)
