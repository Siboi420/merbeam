import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import math

# Set the width of the layout
st.html("""
    <style>
        .stMainBlockContainer {
            max-width:58rem;
        }
    </style>
    """
)

##################################################### 
# Session State
#####################################################

st.title("Beam Design")

st.sidebar.header("Material Properties")

f_c = st.sidebar.number_input("$f_c$, MPa", value=(28.0))
f_yl = st.sidebar.number_input("$f_{yl}$, MPa", value=(420.0))
f_yt = st.sidebar.number_input("$f_{yt}$, MPa", value=(280.0))

epsilon_y = f_yl/2e5
epsilon_s = 0.005

st.sidebar.header("Beam Dimension")

b = st.sidebar.number_input("Beam Width, b (mm)", placeholder="Insert beam width", value=(250.0))
h = st.sidebar.number_input("Beam Height, h (mm)", placeholder="Insert beam height", value=(350.0))
p = st.sidebar.number_input("Concrete Cover, p (mm)", placeholder="Insert concrete cover", value=(40.0))
dl = st.sidebar.number_input("Longitudinal Bar Diameter, dl (mm)", value=(16.0))
dt = st.sidebar.number_input("Transversal Bar Diameter, dt (mm)", value=(10.0))

# Applied Moment Acting on the beam #

st.sidebar.header("Design Moment")

M_ue = st.sidebar.radio("Input maximum bending moment", 
                        ["From Beam Calculator Diagram","Manually add value"])

if M_ue == "From Beam Calculator Diagram":
    if 'max_moment' not in st.session_state:
        st.sidebar.error("Maximum bending moment has yet to be calculated!")
        M_ue = 0
    elif 'max_moment' in st.session_state:
        M_ue = st.session_state.max_moment
        st.sidebar.write ("$M_u$ =", str(round(M_ue,3)), "kN-m")
elif M_ue == "Manually add value":
    M_ue = st.sidebar.number_input('$M_u$ (kN-m)',value=(120.0))


if 'max_moment' not in st.session_state and M_ue == 0:
    st.error("Maximum bending moment has yet to be calculated")
elif M_ue > 0 or 'max_moment' in st.session_state:
        

    st.subheader("Calculate " r"$\beta_1$")

    if f_c >= 55:
        beta_1 = 0.65
        st.latex(r"""
                f_c' \geq 55 \; \therefore \; \beta_1 = 0.65
                """)
    elif f_c > 28 and f_c < 55:
        beta_1 = np.round(0.85-(0.05*(f_c-28)/7),2)
        st.latex(r" 28 < f_c' < 55 \; \therefore \; \beta_1 = 0.85 - \frac{0.05 \cdot (f_c'-28)}{7} ")
        st.latex(r" \beta_1 = \; 0.85 - \frac{0.05 \cdot (" + str(f_c) + r" - 28)}{7} = "+ str(beta_1) +r" ")
    elif f_c <= 28:
        beta_1 = 0.85
        st.latex(r"""
                16 \leq f_c' \leq 28 \; \therefore \; \beta_1 = 0.85\\
                """)

    ##################################################### 
    # Steel Reinforcement Limit
    #####################################################

    y = dl + 25
    d = h-(p + dt + dl/2)
    d_prime = (p+dt+dl/2)

    A_smin1 = 0.25 * np.sqrt(f_c) / f_yl * b * d
    A_smin2 = 1.4/f_yl * b * d
    A_smin = max(A_smin1, A_smin2)

    st.subheader("Calculate " r"$A_{s,min}$")

    st.write("According to ACI Code, minimum reinforcement shall be calculated as below: ")

    MINIMUM_SPACING = 25

    st.latex(r'''
        A_{s,min} = \; \text{Greater of} 
            \begin{cases}
                \frac{0.25 \sqrt{f_c'}}{f_y}b_wd \\
                \frac{1.4}{f_y}b_w d
            \end{cases}
        ''')

    st.write("We acquire the minimum area value as: ")
    st.latex(r" A_{s.min1} = \frac{0.25 \sqrt{"+ str(f_c) +r"}}{"+ str(f_yl) +r"} \cdot "+ str(b) +r" \cdot "+ str(d) +r" = "+ str(round(A_smin1,3)) +r" \; \text{mm}^2 ")
    st.latex(r" A_{s,min2} = \frac{1.4}{"+ str(f_yl) +r"} \cdot "+ str(b) +r" \cdot "+ str(d) +r" = "+ str(round(A_smin2,3)) +r" \; \text{mm}^2")

    st.write("Therefore the required minimum area of steel is:")
    st.latex(r''' A_{s,min} = ''' rf''' {A_smin:.3f} ''' ''' \; \\text{mm}^2 ''') 

    st.subheader("Calculate the Required Reinforcement")

    # Maximum steel reinforcement

    A_sbal = 0.85 * f_c * beta_1 * (0.003/(0.003+epsilon_y))*d
    A_smax = 0.75 * A_sbal

    st.write("The maximum amount of reinforcement is taken as 75\% of $A_{s,balance}$. which are calculated as:")
    st.latex(r"""
            \begin{align*}
            A_{s,balance} &= \frac{1}{f_y} \left(0.85 \cdot f_c' \cdot \beta_1 \cdot \frac{\epsilon_{cu}}{\epsilon_{cu}+\epsilon_y} \cdot d \right) \\
            &= \frac{1}{"""+ str(round(f_yl,3)) +r"""} \cdot \left(0.85 \cdot """+ str(round(f_c)) +r""" \cdot """+ str(round(beta_1,3)) +r""" \cdot \frac{0.003}{0.003+ """+ str(round(epsilon_y,3)) +r"""} \right) \\
            &= """+ str(round(A_sbal,3)) +r""" \; \text{mm}^2
            \end{align*}
            """)
    st.write("Therefore the maximum area of reinforcement is:")
    st.latex(r"A_{s,max} = 0.75 \cdot A_{s,balance} = "+str(round(A_smax,3))+r" \; \text{mm}^2") 

    ##################################################### 
    # Design
    #####################################################

    # Section Design

    st.subheader('Nominal Flexural Strength')

    st.write('Distance to steel tension reinforcement')
    st.latex(r"d = "+ str(round(d,3)) +r" \; \text{mm}")

    st.write('Distance to steel compression reinforcement')
    st.latex(r"d' = "+ str(round(d_prime,3)) +r" \; \text{mm}")

    st.write('Tension reinforcement strain')
    st.latex(r" \epsilon_s = "+ str(round(epsilon_s,5)) +r" \longrightarrow \; \text{tension reinforcement has yielded}")

    # Assume the value of c
    c = d / (epsilon_s+0.003) * 0.003
    st.write("Calculate the nominal moment provided by beam with compression reinforcement, assume:")
    st.latex(r'c = \frac{d}{\epsilon_s+\epsilon_c} \cdot 0.003 = \frac{'+ str(round(d,3)) +r'}{'+ str(round(epsilon_s,3)) +r' + 0.003} \cdot 0.003 = ' rf'{c:0.2f}' '\; \\text{mm}')

    # Calculate a
    a = c*beta_1
    st.write('Calculate the concrete stress block')
    st.latex(r" a = c \cdot \beta_1 = "+ str(round(c,3)) +r" \cdot "+ str(round(beta_1,3)) +r" = "+ str(round(a,3)) +r" \; \text{mm}")

    ##################################################### 
    # Function Assign
    #####################################################
    A_s = 0.85*f_c*b/f_yl * (d-np.sqrt(d**2 - (2*M_ue*1e6)/(0.85*f_c*b*0.9)))
    if math.isnan(A_s) is True:
        st.error("The section dimension needs to be increased")
    else:
        st.write("Calculate te required steel area:")
        st.latex(r"""
                \begin{align*}
                A_s &= \frac{0.85 \cdot f_c \cdot b}{f_y} \cdot \left( d - \sqrt{d^2 - \frac{2M_u}{0.85 \cdot f_c \cdot b \cdot 0.9}} \right)\\
                &= \frac{0.85 \cdot """+ str(round(f_c,3)) +r""" \cdot """+ str(b) +r"""}{"""+ str(round(f_yl,3)) +r"""} \cdot \left( """+ str(round(d,3)) +r""" - \sqrt{"""+ str(round(d,3)) +r"""^2 - \frac{2 \cdot """+ str(round(M_ue,3)) +r""" \cdot 10^6}{0.85 \cdot """+ str(round(f_c,3)) +r""" \cdot """+ str(b) +r""" \cdot 0.9}} \right)\\
                &= """+ str(round(A_s,3)) +r""" \; \text{mm}^2
                \end{align*}
                """)
    
        M_n = f_yl * A_s * (d - (A_s*f_yl/(2*(0.85*f_c)*b)))
        fM_n = M_n*0.9+1e-6
        st.write("The corresponding nominal moment is: ")
        # st.write(fM_n)
        st.latex(r"""
                \begin{align*}
                M_n &= f_y \cdot A_s\cdot \left( d - \frac{A_s * f_y}{2(0.85 \cdot f_c' \cdot b)} \right)\\
                &= """+ str(round(f_yl)) +r""" \cdot """+ str(round(A_s,3)) +r""" \left( """+ str(round(d,3)) +r""" - \frac{"""+ str(round(A_s,3)) +r""" \cdot """+ str(round(f_yl,3)) +r"""}{2 \cdot 0.85 \cdot """+ str(round(f_c,3)) +r""" \cdot """+ str(b) +r"""} \right)\\
                &= """+ str(round(M_n)) +r""" \; \text{N-mm}
                \end{align*}
                """)
        st.write("Since the steel reinforcement is in tension, therefore the reduction factor, $\; \phi$, is equal to 0.9, therefore")

        st.latex(r"""
                \begin{align*} 
                \phi M_n &= 0.9 \cdot """+ str(round(M_n,3)) +r""" = """+ str(round(fM_n,3)) +r""" \; \text{Nmm} \\
                &= """+ str(round(fM_n/1e6,3)) +r""" \; \text{kNm}
                \end{align*}
                """)
        if fM_n < M_ue*1e6:
            st.error("The nominal moment is insufficient, increase the section dimension or add compression reinforcement to increase the amount of tension reinforcement enough to achieve sufficient strength required")
        elif fM_n >= M_ue*1e6:
            n = np.ceil(A_s / (dl**2 * np.pi / 4))
            n_prime = np.ceil(max(2, A_smin / (dl**2 * np.pi / 4), 2))
            A_s = n * dl**2 * np.pi /4
            A_sp = n_prime * dl**2 * np.pi / 4

            st.write("The design capacity ratio is:")

            st.latex(r"""
            \begin{align*}
            \phi M_n &= """+ str(round(fM_n/1e6,3)) +r""" \; \text{kN-m} \\
            M_u &= """+ str(round(M_ue,3)) +r""" \; \text{kN-m} \\
            DCR &= \frac{M_u}{\phi M_n} = \frac{"""+ str(round(M_ue,3)) +r"""}{"""+ str(round(fM_n/1e6,3)) +r"""} = """+ str(round(M_ue/(fM_n/1e6),3)) +r"""
            \end{align*}
            """)

            if A_s >= A_smax:
                st.error("The reinforcement area $A_s = "+ str(round(A_s)) +r" \; \text{mm}^2$, exceed the maximum of $A_{s,max} = "+ str(round(A_smax)) +r" \; \text{mm}^2$. Increase the section dimension!")
            else: 
                st.write("The section is safe")
                st.subheader("Reinforcement Limits")

                st.write("Tension bar check")
                st.write("$A_s = "+str(round(A_s,3))+r" \; \text{mm}^2 < A_{s,max} = "+str(round(A_smax,3))+r" \; \text{mm}^2 \rightarrow$ The reinforcement is not overcrowded \
                        $A_s = "+str(round(A_s,3))+r" \; \text{mm}^2 > A_{s,min} = "+str(round(A_smin,3))+r" \; \text{mm}^2 \rightarrow$ The reinforcement is sufficient")
                st.write("Compression bar check")
                st.write("$A_s' = "+str(round(A_sp,3))+r" \text{mm}^2$")

                # Section Drawing

                st.subheader("Section Preview")

                # Calculate rebar positions and handle layering
                xx_dis = (b - 2 * p - dt * 2 - dl) / (n - 1) if n > 1 else 0  # Distance between tension bars
                layering_required = xx_dis < MINIMUM_SPACING if n > 1 else False

                tension_bars_layer1 = []
                tension_bars_layer2 = []
                yy_tension1 = []
                yy_tension2 = []

                # Compression Bars
                compression_bars = np.linspace((p+dt+dl/2), (b-(p+dt+dl/2)), int(n_prime)).tolist()
                yy_compression = np.repeat((h-d_prime), int(n_prime))

                first_bar_position = p + dt + dl/2
                last_bar_position = b - (p + dt + dl/2)
                first_layer_spacing = (last_bar_position - first_bar_position)/(np.ceil(n/2)-1) if np.ceil(n/2)>1 else 0 #Spacing of the top bar is dependent on the amount of tension needed.

                if layering_required:
                    num_bars_layer1 = int(np.ceil(n / 2)-1) #Number of Bars in Top layer
                    num_bars_layer2 = int(n - num_bars_layer1)  # Correctly calculates the remaining bars
                    
                    #Layer 1 linspace has same starting position as compression bar
                    xx1 = np.linspace(first_bar_position, last_bar_position, num_bars_layer1) #layer 1 uses a single linspace call

                    #Bottom layer uses a linear space, but has correct # of bars and positions within its space.
                    xx2 = np.linspace(first_bar_position,(b - (p + dt + dl / 2)),num_bars_layer2) if num_bars_layer2 >0 else [] #Bottom Layer's left most side will have same first bar position as compression
                    xx2_dis=(b - ((2*p) + (dt*2) + dl))/(num_bars_layer2-1)

                    #Convert values to List
                    tension_bars_layer1 = xx1.tolist()
                    tension_bars_layer2 = xx2.tolist()

                    #create repeating List
                    yy_tension1= np.repeat((h-d + dl + 25), len(tension_bars_layer1)) if len(tension_bars_layer1) > 0 else []
                    yy_tension2 = np.repeat((h-d), len(tension_bars_layer2)) if len(tension_bars_layer2) > 0 else [] #20 mm assumed here

                else: #NO Layering
                    xx = np.linspace((p+dt+dl/2), (b-(p+dt+dl/2)), int(n))
                    tension_bars_layer1 = xx.tolist()
                    yy_tension1 = np.repeat((h-d), int(n)) #yy_tension can just equal to n since it does not affect the length of another tensor

                fig, ax = plt.subplots(figsize=(3,3))
                ax.set_xticks([])
                ax.set_yticks([])
                ax.plot(
                    [0, b, b, 0, 0],
                    [0, 0, h ,h, 0])

                # Plot compression bars with positions that don't change
                ax.scatter(compression_bars, yy_compression, label=r"Compression bar") # Plot Compression

                # Plot tension bars based on layering strategy
                if layering_required:
                    ax.scatter(tension_bars_layer1, yy_tension1, label=r"Tension bar Layer 2") #Plot layer 1. tension bars (list).
                    ax.scatter(tension_bars_layer2, yy_tension2, label=r"Tension bar Layer 1")
                else:
                    ax.scatter(tension_bars_layer1, yy_tension1, label=r"Tension bar") #Plot tension bars layer 1
                ax.set_xlim(-100, b+50)
                ax.set_ylim(-100, h+50)
                ax.legend(loc='lower left', fontsize=5, markerscale=0.5)
                st.pyplot(fig, use_container_width=False)

                if layering_required:
                    st.write("The distance between tension bar is", str(round(xx2_dis,3)), "$\\text{mm}$")
                else:
                    st.write(r"The distance between tension bar is", str(round(xx_dis,3)),  "$\\text{mm}$") 

                xxp_dis = (b-2*p - dt*2 - dl) / (n_prime-1)


                st.write("The distance between compression bar is =", str(round(xxp_dis,3)), "$\\text{mm}$")
                st.write("Number of tension reinforcement =", str(round(n)))
                st.write("Number of compression reinforcement =", str(round(n_prime)))