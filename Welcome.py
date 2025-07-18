import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Beam Diagram Calculator 👋")

st.sidebar.success("Select Calculator Above.")

st.markdown(
    """
    Welcome to Our app! with this app, You can calculate the bending moment, shear and support reaction for a beam! Not only that, You can also design reinforced concrete beam by using the value from the beam diagram calculator, or by manually inputing the number. To get started, You can proceed to the next page "Beam Calculator Diagram" or go straight to detailing the beam reinforced concrete.
    """
    )
