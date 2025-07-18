import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def calculate_simple_supported_beam(
    length, load_position, load_magnitude, UDL_magnitude
):
    """
    Calculate reactions and bending moments for a simply supported beam.
    """
    # Reactions
    R1 = ((load_magnitude * (length - load_position)) / length) + (
        UDL_magnitude * length / 2
    )
    R2 = ((load_magnitude * load_position) / length) + (UDL_magnitude * length / 2)

    return R1, R2


def calculate_cantilever_beam(length, load_position, load_magnitude, UDL_magnitude):
    """
    reactions and bending moments for a cantilever beam.
    """
    # Reaction at the fixed support
    R = load_magnitude + (UDL_magnitude * length)
    M_react = -(
        (load_magnitude * load_position) + (UDL_magnitude * length * length / 2)
    )

    return R, M_react


def plot_shear_diagram_simple_supported(
    length, load_position, load_magnitude, R1, UDL_magnitude
):
    """
    Plot shear force diagram for a simply supported beam.
    """
    x = np.linspace(0, length, 10000)
    V = np.piecewise(
        x,
        [x < load_position, x >= load_position],
        [
            lambda x: R1 - UDL_magnitude * x,  # Shear force before the load position
            lambda x: R1
            - load_magnitude
            - UDL_magnitude * x,  # Shear force after the load position
        ],
    )

    plt.figure(figsize=(8, 5))
    plt.plot(x, V, label="Shear Force (kN)", color="orange")
    plt.fill_between(
        x,
        0,
        V,
        where=(V > 0),
        color="orange",
        alpha=0.3,
        step="pre",
        label="Positive Shear",
    )
    plt.fill_between(
        x,
        0,
        V,
        where=(V < 0),
        color="red",
        alpha=0.3,
        step="pre",
        label="Negative Shear",
    )
    plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
    plt.title("Shear Force Diagram (Simply Supported Beam)")
    plt.xlabel("Length (m)")
    plt.ylabel("Shear Force (kN)")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
    return V


def plot_shear_diagram_cantilever(
    length, load_position, load_magnitude, UDL_magnitude, R
):
    """
    Plot shear force diagram for a cantilever beam.
    """
    x = np.linspace(0, length, 10000)
    V = np.piecewise(
        x,
        [x <= load_position, x > load_position],
        [
            lambda x: R - UDL_magnitude * x,  # Shear force up to the load position
            lambda x: R
            - load_magnitude
            - UDL_magnitude * x,  # Shear force beyond the load position
        ],
    )
    print(x, V, R)

    plt.figure(figsize=(8, 5))
    plt.plot(x, V, label="Shear Force (kN)", color="orange")
    plt.fill_between(
        x,
        0,
        V,
        where=(V > 0),
        color="orange",
        alpha=0.3,
        step="pre",
        label="Positive Shear",
    )
    plt.fill_between(
        x,
        0,
        V,
        where=(V < 0),
        color="red",
        alpha=0.3,
        step="pre",
        label="Negative Shear",
    )
    plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
    plt.title("Shear Force Diagram (Cantilever Beam)")
    plt.xlabel("Length (m)")
    plt.ylabel("Shear Force (kN)")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
    return V


def plot_moment_diagram_simple_supported(
    length, load_position, load_magnitude, R1, UDL_magnitude
):
    """
    Plot moment diagram for a simply supported beam.
    """
    x = np.linspace(0, length, 10000)
    M = np.piecewise(
        x,
        [x < load_position, x >= load_position],
        [
            lambda x: (R1 * x) - (0.5 * UDL_magnitude * x**2),
            lambda x: R1 * x
            - load_magnitude * (x - load_position)
            - (0.5 * UDL_magnitude * x**2),
        ],
    )

    plt.figure(figsize=(8, 5))
    plt.plot(x, M, label="Moment (kNm)")
    plt.fill_between(
        x,
        0,
        M,
        where=(M > 0),
        color="blue",
        alpha=0.3,
        step="pre",
        label="Positive Moment",
    )
    plt.fill_between(
        x,
        0,
        M,
        where=(M < 0),
        color="red",
        alpha=0.3,
        step="pre",
        label="Negative Moment",
    )
    plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
    plt.title("Moment Diagram (Simply Supported Beam)")
    plt.xlabel("Length (m)")
    plt.ylabel("Moment (kNm)")
    plt.gca().invert_yaxis()  # Invert the y-axis
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
    return x, M


def plot_moment_diagram_cantilever(
    length, load_position, load_magnitude, R, UDL_magnitude, M_react
):
    """
    Plot moment diagram for a cantilever beam.
    """
    x = np.linspace(0, length, 10000)
    M = np.piecewise(
        x,
        [x <= load_position, x > load_position],
        [
            lambda x: R * x - (0.5 * UDL_magnitude * x**2) + M_react,
            lambda x: (R * x)
            - (0.5 * UDL_magnitude * x**2)
            - (load_magnitude * (x - load_position))
            + M_react,
        ],
    )

    plt.figure(figsize=(8, 5))
    plt.plot(x, M, label="Moment (kNm)")
    plt.fill_between(
        x,
        0,
        M,
        where=(M > 0),
        color="blue",
        alpha=0.3,
        step="pre",
        label="Positive Moment",
    )
    plt.fill_between(
        x,
        0,
        M,
        where=(M < 0),
        color="red",
        alpha=0.3,
        step="pre",
        label="Negative Moment",
    )
    plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
    plt.title("Moment Diagram (Cantilever Beam)")
    plt.xlabel("Length (m)")
    plt.ylabel("Moment (kNm)")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
    return x, M


def plot_load_diagram_simple_supported(
    length, load_position, load_magnitude, UDL_magnitude
):
    """
    Plot a load diagram for a simply supported beam with triangular supports and an arrow for the point load.
    """
    plt.figure(figsize=(8, 5))

    # Plot the beam as a straight line
    plt.hlines(0, 0, length, color="black", linewidth=2)

    # Add triangular supports at the ends
    plt.scatter([0], [0], color="blue", s=200, marker="^", label="Support (Left)")
    plt.scatter([length], [0], color="blue", s=200, marker="^", label="Support (Right)")

    # Add the load as an arrow
    plt.arrow(
        load_position,
        load_magnitude,
        0,
        -load_magnitude * 0.9,
        head_width=0.2,
        head_length=0.5,
        fc="red",
        ec="red",
        linewidth=2,
        label="Point Load",
    )

    # Add the UDL Load
    plt.fill_between(
        [0, length], 0, UDL_magnitude, color="green", alpha=0.5, label="UDL"
    )

    # Set limits and labels
    plt.ylim(-load_magnitude - 2, load_magnitude + 2)
    plt.xlim(-0.5, length + 0.5)
    plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    plt.title("Load Diagram (Simply Supported Beam)")
    plt.xlabel("Length (m)")
    plt.ylabel("Load (kN for Point Load and kN/m for UDL)")

    # Add legend
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    st.pyplot(plt)


def plot_load_diagram_cantilevered_beam(
    length, load_position, load_magnitude, UDL_magnitude
):
    """
    Plot a load diagram for a cantilevered beam with fixed support and an arrow for the point load.
    The arrow and support are scaled with the load magnitude.
    """
    plt.figure(figsize=(8, 5))

    # Plot the beam as a straight line
    plt.hlines(0, 0, length, color="black", linewidth=2)

    # Scale the fixed support height based on load magnitude
    support_height = load_magnitude / 2  # Height of the fixed support
    plt.fill_betweenx(
        [-support_height, support_height],
        -0.2,
        0,
        color="gray",
        edgecolor="black",
        hatch="|",
        label="Fixed Support",
    )

    # Scale the arrow dimensions based on load magnitude
    head_width = 0.5  # Arrow head width scales with load magnitude
    head_length = 0.1 * load_magnitude  # Arrow head length scales with load magnitude
    arrow_length = (
        -load_magnitude + head_length
    )  # Arrow body length ensures the tip ends at y=0
    plt.arrow(
        load_position,
        load_magnitude,  # Start at the top (load magnitude)
        0,
        arrow_length,  # Arrow length ensures the tip ends at y=0
        head_width=head_width,
        head_length=head_length,
        fc="red",
        ec="red",
        linewidth=2,
        label="Point Load",
    )
    # Add the UDL Load
    plt.fill_between(
        [0, length], 0, UDL_magnitude, color="green", alpha=0.5, label="UDL"
    )

    # Set limits and labels
    plt.ylim(-load_magnitude - 2, load_magnitude + 2)
    plt.xlim(-0.5, length + 0.5)
    plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    plt.title("Load Diagram (Cantilevered Beam)")
    plt.xlabel("Length (m)")
    plt.ylabel("Load (kN)")

    # Add legend
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    st.pyplot(plt)
    return head_length


@st.cache_data
def convert_df(df: pd.DataFrame):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode("utf-8")


def main():
    st.title("Beam Calculator with Moment and Shear Force Diagrams (Bar Chart)")
    st.sidebar.image("./imgs/logo_polinema.png", width=100)
    st.sidebar.header("Beam Type")

    beam_type = st.sidebar.radio(
        "Select the type of beam:", ("Simply Supported Beam", "Cantilever Beam")
    )
    if beam_type == "Simply Supported Beam":
        st.image("./imgs/moment.png", caption="Simply Supported Beam")
    else:
        st.image("./imgs/Cantilever.jpg", caption="Cantilevered Beam")

    st.sidebar.header("Beam Parameters")
    length = st.sidebar.number_input(
        "The total length of the beam, L (m):", min_value=0.0, step=0.1
    )
    load_position = st.sidebar.number_input(
        "The position of the point load, x (m):", min_value=0.0, step=0.1
    )
    load_magnitude = st.sidebar.number_input(
        "The magnitude of the point load, P (kN):", min_value=0.0, step=0.1
    )
    UDL_magnitude = st.sidebar.number_input(
        "The magnitude of the UDL, w (kN/m):", min_value=0.0, step=0.1
    )

    if st.sidebar.button("Calculate"):
        if load_position > length or length == 0:
            st.error("The load position cannot exceed the beam length or the length must be greater than 0.")
        else:
            if beam_type == "Simply Supported Beam":
                R1, R2 = calculate_simple_supported_beam(
                    length, load_position, load_magnitude, UDL_magnitude
                )
                st.subheader("Simply Supported Beam Results")
                st.write(f"Reaction at left support (R1): {R1:.2f} kN")
                st.write(f"Reaction at right support (R2): {R2:.2f} kN")

                st.subheader("Moment Diagram")
                x, M = plot_moment_diagram_simple_supported(
                    length, load_position, load_magnitude, R1, UDL_magnitude
                )
                max_bending_moment = np.max(M)
                max_bending_location = x[np.argmax(M)]
                st.write(f"**Maximum Bending Moment: {max_bending_moment:.2f} kNm**")
                st.write(
                    f"**Location of Maximum Bending Moment: {max_bending_location:.2f} m**"
                )

                st.subheader("Shear Force Diagram")
                V = plot_shear_diagram_simple_supported(
                    length, load_position, load_magnitude, R1, UDL_magnitude
                )
                max_shear_force = np.max(np.abs(V))
                st.write(f"**Maximum shear force: {max_shear_force:.2f} kN**")

                st.subheader("Load Diagram")
                plot_load_diagram_simple_supported(
                    length, load_position, load_magnitude, UDL_magnitude
                )
                df = pd.DataFrame(
                    {"Position (m)": x, "Moment (kNm)": M, "Shear (kN)": V}
                )

                if 'max_moment' not in st.session_state:
                    st.session_state.max_moment = max_bending_moment
                elif 'max_moment' in st.session_state:
                    st.session_state.max_moment = max_bending_moment

            elif beam_type == "Cantilever Beam":
                R, M_react = calculate_cantilever_beam(
                    length, load_position, load_magnitude, UDL_magnitude
                )
                st.subheader("Cantilever Beam Results")
                st.write(f"Reaction at the fixed support (R): {R:.2f} kN")
                st.write(f"Moment at the fixed support: {M_react:.2f} kNm")

                st.subheader("Moment Diagram")
                x, M = plot_moment_diagram_cantilever(
                    length, load_position, load_magnitude, R, UDL_magnitude, M_react
                )
                max_bending_moment = np.max(np.abs(M))
                max_bending_location = x[np.argmax(np.abs(M))]
                st.write(f"**Minimum Bending Moment: {max_bending_moment:.2f} kNm**")

                st.subheader("Shear Force Diagram")
                V = plot_shear_diagram_cantilever(
                    length, load_position, load_magnitude, UDL_magnitude, R
                )
                max_shear_force = np.max(V)
                st.write(f"**Maximum shear force: {max_shear_force:.2f} kN**")

                st.subheader("Load Diagram")
                plot_load_diagram_cantilevered_beam(
                    length, load_position, load_magnitude, UDL_magnitude
                )
                df = pd.DataFrame(
                    {"Position (m)": x, "Moment (kNm)": M, "Shear (kN)": V}
                )

                if 'max_moment' not in st.session_state:
                    st.session_state.max_moment = max_bending_moment
                elif 'max_moment' in st.session_state:
                    st.session_state.max_moment = max_bending_moment

            if df is None:
                st.write("No data to download.")
            else:
                data = convert_df(df)
                st.download_button(
                    label="Download data as CSV",
                    data=data,
                    file_name="moment_shear_data.csv",
                    mime="text/csv",
                )


if __name__ == "__main__":
    main()
