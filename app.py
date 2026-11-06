
import streamlit as st
import matplotlib.pyplot as plt
import math
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Vector Calculator",
    page_icon="📐",
    layout="wide"
)

# Application title
st.title("📐 Calculadora de suma de vectores")
st.write(
    "Introduce los componentes de tus vectores "
    "para calcular y visualizar su resultante."
)

st.divider()

# Number of vectors
number_of_vectors = st.number_input(
    "Número de vectores",
    min_value=1,
    max_value=30,
    value=2,
    step=1
)

st.subheader("Componentes de los vectores")

vectors = []

# Input form
with st.form("vector_form"):

    for i in range(int(number_of_vectors)):

        col1, col2, col3 = st.columns([1, 2, 2])

        with col1:
            st.write(f"**Vector V{i + 1}**")

        with col2:
            x = st.number_input(
                f"Componente X - V{i + 1}",
                value=0.0,
                key=f"x_{i}"
            )

        with col3:
            y = st.number_input(
                f"Componente Y - V{i + 1}",
                value=0.0,
                key=f"y_{i}"
            )

        vectors.append((x, y))

    calculate = st.form_submit_button(
        "Calcular y graficar",
        type="primary",
        use_container_width=True
    )

# Calculations
if calculate:

    result_x = sum(x for x, y in vectors)
    result_y = sum(y for x, y in vectors)

    result_magnitude = math.hypot(
        result_x,
        result_y
    )

    result_angle = math.degrees(
        math.atan2(result_y, result_x)
    )

    # Results
    st.divider()
    st.subheader("Resultados")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Componente X",
        f"{result_x:.3f}"
    )

    col2.metric(
        "Componente Y",
        f"{result_y:.3f}"
    )

    col3.metric(
        "Magnitud resultante",
        f"{result_magnitude:.3f}"
    )

    st.info(
        f"Vector resultante: R = ({result_x:g}, {result_y:g}) "
        f"| Ángulo: {result_angle:.2f}°"
    )

    # Results table
    st.subheader("Tabla de vectores")

    table_data = []

    for i, (x, y) in enumerate(vectors, 1):

        table_data.append({
            "Vector": f"V{i}",
            "Componente X": x,
            "Componente Y": y,
            "Magnitud": math.hypot(x, y)
        })

    table_data.append({
        "Vector": "Resultante",
        "Componente X": result_x,
        "Componente Y": result_y,
        "Magnitud": result_magnitude
    })

    dataframe = pd.DataFrame(table_data)

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True
    )

    # Vector visualization
    st.subheader("Representación gráfica")

    fig, ax = plt.subplots(figsize=(9, 6))

    colors = plt.get_cmap("tab10")

    # Individual vectors
    for i, (x, y) in enumerate(vectors):

        ax.quiver(
            0, 0, x, y,
            angles="xy",
            scale_units="xy",
            scale=1,
            color=colors(i % 10),
            width=0.006,
            label=f"V{i + 1} ({x:g}, {y:g})"
        )

    # Resultant vector
    ax.quiver(
        0, 0,
        result_x,
        result_y,
        angles="xy",
        scale_units="xy",
        scale=1,
        color="red",
        width=0.010,
        label="Resultante"
    )

    # Axis limits
    all_x = [0, result_x] + [x for x, y in vectors]
    all_y = [0, result_y] + [y for x, y in vectors]

    max_value = max(
        max(abs(value) for value in all_x),
        max(abs(value) for value in all_y),
        1
    )

    limit = max_value * 1.25

    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)

    ax.set_aspect("equal", adjustable="box")

    ax.set_xlabel("Eje X")
    ax.set_ylabel("Eje Y")

    ax.set_title("Suma de vectores")

    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)

    ax.grid(True, linestyle=":", alpha=0.7)

    ax.legend(loc="best")

    fig.tight_layout()

    st.pyplot(fig)

    plt.close(fig)

else:

    st.caption(
        "Introduce los componentes y presiona "
        "'Calcular y graficar' para comenzar."
    )
    