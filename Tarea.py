import streamlit as st
import schemdraw
schemdraw.use('matplotlib')
import schemdraw.elements as elm
import schemdraw.logic as log
import matplotlib.pyplot as plt

# ==========================================
# CONFIGURACIÓN E IDENTIDAD INSTITUCIONAL
# ==========================================
TEC_GREEN = '#006B3F'
TEC_RED = '#B22222'
st.set_page_config(page_title="Simulador HMI-PLC - Tecmilenio", layout="wide")

st.markdown(f"""
    <style>
    .main-title {{ color: {TEC_GREEN}; font-family: 'serif'; font-size: 28px; font-weight: bold; text-align: center; }}
    .section-header {{ color: {TEC_GREEN}; font-family: 'serif'; font-size: 20px; font-weight: bold; border-bottom: 1.5px solid {TEC_GREEN}; padding-bottom: 5px; margin-top: 20px; }}
    .alert-box {{ padding: 15px; background-color: #f8f9fa; border-left: 6px solid {TEC_GREEN}; border-radius: 4px; font-weight: bold; color: #333; font-family: 'serif';}}
    .alert-box-off {{ padding: 15px; background-color: #f8f9fa; border-left: 6px solid {TEC_RED}; border-radius: 4px; font-weight: bold; color: #333; font-family: 'serif';}}
    .truth-table {{ width: 100%; border-collapse: collapse; font-family: 'serif'; text-align: center; margin-top: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
    .truth-table th {{ background-color: {TEC_GREEN}; color: white; padding: 10px; border: 1px solid #ddd; }}
    .truth-table td {{ padding: 10px; border: 1px solid #ddd; font-weight: bold; color: #333; }}
    .active-row {{ background-color: #e6f0eb; border: 2px solid {TEC_GREEN} !important; color: {TEC_GREEN} !important; font-size: 1.1em; }}
    .formula-box {{ padding: 15px; background-color: #e6f0eb; border-left: 6px solid {TEC_GREEN}; border-radius: 4px; font-family: 'serif'; font-size: 18px; font-weight: bold; text-align: center; margin: 10px 0; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">Simulador Logico y de Escalera — Circuito Combinacional</p>', unsafe_allow_html=True)
st.markdown(
    '<div class="formula-box">Q0.0 = (I0.0 AND I0.1) OR (NOT I0.2)</div>',
    unsafe_allow_html=True
)

# ==========================================
# FUNCIÓN DE LÓGICA COMBINACIONAL
# Q0.0 = (I0.0 AND I0.1) OR (NOT I0.2)
# Compuertas: AND, NOT, OR (3 en cascada)
# ==========================================
def evaluar_circuito(a, b, c):
    parte1 = a and b       # Compuerta AND
    parte2 = not c         # Compuerta NOT
    salida = parte1 or parte2  # Compuerta OR
    return salida, parte1, parte2

# ==========================================
# BARRA LATERAL: ENTRADAS DEL OPERADOR
# ==========================================
st.sidebar.header("Panel de Operador")
st.sidebar.caption("Active o desactive las señales fisicas:")

val_i0 = st.sidebar.toggle("Sensor I0.0 (Input 1)")
val_i1 = st.sidebar.toggle("Sensor I0.1 (Input 2)")
val_i2 = st.sidebar.toggle("Sensor I0.2 (Input 3)")

st.sidebar.markdown("---")
st.sidebar.caption("Universidad Tecmilenio")

# Evaluación del circuito
q0, and_result, not_result = evaluar_circuito(val_i0, val_i1, val_i2)

# ==========================================
# LAYOUT PRINCIPAL
# ==========================================
col_ctrl, col_vis = st.columns([1, 2])

with col_ctrl:
    st.markdown('<p class="section-header">Estado de Entradas</p>', unsafe_allow_html=True)
    st.write(f"**I0.0:** {'🟢 ON' if val_i0 else '🔴 OFF'}")
    st.write(f"**I0.1:** {'🟢 ON' if val_i1 else '🔴 OFF'}")
    st.write(f"**I0.2:** {'🟢 ON' if val_i2 else '🔴 OFF'}")

    st.markdown('<p class="section-header">Estados Internos</p>', unsafe_allow_html=True)
    st.write(f"**AND (I0.0 · I0.1):** {'🟢 1' if and_result else '🔴 0'}")
    st.write(f"**NOT (I0.2):** {'🟢 1' if not_result else '🔴 0'}")

    st.markdown('<p class="section-header">Salida Q0.0</p>', unsafe_allow_html=True)
    if q0:
        st.markdown('<div class="alert-box">✅ ENERGIZADA (1 Logico)</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-box-off">❌ DESENERGIZADA (0 Logico)</div>', unsafe_allow_html=True)

color_on = TEC_GREEN
color_off = 'gray'

with col_vis:

    # ---------------------------------------------------------
    # 1. DIAGRAMA DE ESCALERA (LADDER)
    # ---------------------------------------------------------
    st.markdown('<p class="section-header">1. Diagrama de Escalera (Ladder)</p>', unsafe_allow_html=True)

    with schemdraw.Drawing(show=False) as d_elec:
        d_elec.config(fontsize=10, lw=2, font='serif')

        d_elec += elm.Line().down().length(1).color(color_on)
        d_elec += elm.Line().right().length(0.5).color(color_on)

        # Rama superior: I0.0 AND I0.1 (contactos en serie)
        d_elec.push()
        d_elec += elm.Line().up().length(1.5).color(color_on)
        d_elec += elm.Switch(action='close' if val_i0 else 'open').right().length(3).label('I0.0 (NO)').color(color_on if val_i0 else color_off)
        d_elec += elm.Switch(action='close' if val_i1 else 'open').right().length(3).label('I0.1 (NO)').color(color_on if and_result else color_off)
        d_elec += elm.Line().down().length(1.5).color(color_on if and_result else color_off)

        # Rama inferior: NOT I0.2 (contacto normalmente cerrado)
        d_elec.pop()
        d_elec += elm.Line().down().length(1.5).color(color_on)
        d_elec += elm.Switch(action='open' if val_i2 else 'close').right().length(6).label('I0.2 (NC)').color(color_on if not_result else color_off)
        d_elec += elm.Line().up().length(1.5).color(color_on if not_result else color_off)

        # Bobina de salida
        d_elec += elm.Line().right().length(0.5).color(color_on if q0 else color_off)
        d_elec += elm.Lamp().right().length(2).label('Q0.0').color(color_on if q0 else color_off)
        d_elec += elm.Line().right().length(0.5).color(color_off)
        d_elec += elm.Line().down().length(1).color(color_off)

    fig_elec = plt.gcf()
    fig_elec.patch.set_alpha(0.0)
    st.pyplot(fig_elec)
    plt.close(fig_elec)

    # ---------------------------------------------------------
    # 2. ESQUEMA LÓGICO
    # ---------------------------------------------------------
    st.markdown('<p class="section-header">2. Esquema Logico (Compuertas en Cascada)</p>', unsafe_allow_html=True)

    with schemdraw.Drawing(show=False) as d_log:
        d_log.config(fontsize=12, lw=2, font='serif')

        c_i0 = color_on if val_i0 else color_off
        c_i1 = color_on if val_i1 else color_off
        c_i2 = color_on if val_i2 else color_off
        c_and = color_on if and_result else color_off
        c_not = color_on if not_result else color_off
        c_out = color_on if q0 else color_off

        # Compuerta AND
        G_and = d_log.add(log.And().label('AND', 'center'))
        d_log.add(elm.Line().left().at(G_and.in1).length(2).color(c_i0).label('I0.0', 'left'))
        d_log.add(elm.Line().left().at(G_and.in2).length(2).color(c_i1).label('I0.1', 'left'))

        # Línea de salida AND hacia OR
        and_out_line = d_log.add(elm.Line().right().at(G_and.out).length(1.5).color(c_and))

        # Compuerta OR
        G_or = d_log.add(log.Or().label('OR', 'center').at(and_out_line.end).right())

        # Compuerta NOT
        G_not = d_log.add(log.Not().label('NOT', 'center').at(G_and.in2).down().length(3))
        d_log.add(elm.Line().left().at(G_not.in1).length(2).color(c_i2).label('I0.2', 'left'))

        # Conectar NOT al in2 de OR
        not_out_line = d_log.add(elm.Line().right().at(G_not.out).length(1).color(c_not))
        d_log.add(elm.Line().at(not_out_line.end).toy(G_or.in2).color(c_not))

        # Salida OR
        d_log.add(elm.Line().right().at(G_or.out).length(2).color(c_out).label('Q0.0', 'right'))

    fig_log = plt.gcf()
    fig_log.patch.set_alpha(0.0)
    st.pyplot(fig_log)
    plt.close(fig_log)

    # ---------------------------------------------------------
    # 3. TABLA DE VERDAD (8 FILAS — 2³)
    # ---------------------------------------------------------
    st.markdown('<p class="section-header">3. Tabla de Verdad (8 Estados)</p>', unsafe_allow_html=True)

    html_table = '''<table class="truth-table">
        <tr>
            <th>I0.0</th>
            <th>I0.1</th>
            <th>I0.2</th>
            <th>AND (I0.0·I0.1)</th>
            <th>NOT (I0.2)</th>
            <th>Q0.0 (Salida)</th>
        </tr>'''

    for a in [False, True]:
        for b in [False, True]:
            for c in [False, True]:
                out, and_r, not_r = evaluar_circuito(a, b, c)
                is_active = (val_i0 == a and val_i1 == b and val_i2 == c)
                row_class = "active-row" if is_active else ""
                html_table += (
                    f"<tr class='{row_class}'>"
                    f"<td>{int(a)}</td>"
                    f"<td>{int(b)}</td>"
                    f"<td>{int(c)}</td>"
                    f"<td>{int(and_r)}</td>"
                    f"<td>{int(not_r)}</td>"
                    f"<td>{int(out)}</td>"
                    f"</tr>"
                )

    html_table += "</table>"
    st.markdown(html_table, unsafe_allow_html=True)