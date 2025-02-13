import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import pandas as pd
import chart_studio.plotly as py

def get_zvalue(a, b, x, y):
    """
    Finds the roots of the polynomial in z
    for given values of
    a, b, x, y.
    """
    constant = x ** 2 + ((1 + b) * y) ** 2 - 1
    c0 = constant ** 3
    c1 = 0.0
    c2 = 3 * (constant ** 2)
    c3 = -(a * (y ** 2) + x ** 2)
    c4 = 3 * constant
    c5 = 0.0
    c6 = 1.0

    coefficients = [c6, c5, c4, c3, c2, c1, c0]
    rts = np.roots(coefficients)
    z = rts[~np.iscomplex(rts)]

    if len(z) > 0:
        zreal = z.real
        return zreal
    else:
        return []


def draw_heart(a=9/200, b=0.01, grid=0.03, palette='viridis'):
    """
    Draws the figure
    @param a: a>0
    @param b:
    @param grid: sparsity of the scatter
    @param palette: palette
    """
    x = np.arange(-2, 2, grid)
    y = x

    all_triplets = []
    for i in x:
        for j in y:
            zaxis = get_zvalue(a, b, i, j)
            for k in zaxis:
                triplet = [i, j, k]
                all_triplets.append(triplet)
    results = np.array(all_triplets).transpose()

    # Save the triplets in a data frame
    xaxis = results[0]
    yaxis = results[1]
    zaxis = results[2]
    df = pd.DataFrame({'x': xaxis, 'y': yaxis, 'z': zaxis})

    # Draw
    fig = go.Figure(data=px.scatter_3d(df, x='x', y='y', z='z',
                                       color='z',
                                       color_continuous_scale=palette,
                                       height=800, width=800,
                                       template="plotly_white",
                                       size_max=10))

    fig.update(layout_coloraxis_showscale=False)

    fig.update_layout(
        paper_bgcolor='#ffe6f2',
        title='Люблю тебе котусику!', 
        title_x=0.5,  # Встановлюємо заголовок по центру (можна коригувати для відступу)
        title_y=0.95,  # Встановлюємо заголовок трохи вище (можна коригувати для відступу)
        font=dict(
            size=20,
            family="Arial Black",
            color="#f754c9"
        ),
        
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
        ))
    fig.show()


draw_heart(palette=['#ff0000', '#ff69b4', '#ff1493'])