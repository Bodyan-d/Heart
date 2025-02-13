from flask import Flask, render_template_string
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import pandas as pd
import os

app = Flask(__name__)

def get_zvalue(a, b, x, y):
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

    return z.real if len(z) > 0 else []

def draw_heart(a=9/200, b=0.01, grid=0.03, palette='viridis'):
    x = np.arange(-2, 2, grid)
    y = x

    all_triplets = []
    for i in x:
        for j in y:
            zaxis = get_zvalue(a, b, i, j)
            for k in zaxis:
                all_triplets.append([i, j, k])

    results = np.array(all_triplets).transpose()
    df = pd.DataFrame({'x': results[0], 'y': results[1], 'z': results[2]})

    fig = go.Figure(data=px.scatter_3d(df, x='x', y='y', z='z',
                                       color='z', color_continuous_scale=palette,
                                       height=800, width=800,
                                       template="plotly_white",
                                       size_max=10))

    fig.update(layout_coloraxis_showscale=False)
    fig.update_layout(paper_bgcolor='#ffe6f2', title='Люблю тебе котусику!',
                      font=dict(size=20, family="Arial Black", color="#f754c9"),
                      scene=dict(xaxis=dict(visible=False),
                                 yaxis=dict(visible=False),
                                 zaxis=dict(visible=False)))

    return fig.to_html(full_html=False)

@app.route("/")
def home():
    graph_html = draw_heart(palette=['#ff0000', '#ff69b4', '#ff1493'])
    return render_template_string("<html><body>{{ graph | safe }}</body></html>", graph=graph_html)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Використовуємо змінну середовища, або 5000 за замовчуванням
    app.run(host="0.0.0.0", port=port)