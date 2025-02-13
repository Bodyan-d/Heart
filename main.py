from flask import Flask, render_template_string, make_response
import os
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import pandas as pd
import threading

app = Flask(__name__)

cached_graph = None  # Кеш графіка для швидшого завантаження

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

def draw_heart(a=9/200, b=0.01, grid=0.05, palette=['#ff0000', '#ff4444', '#ff8888']):
    global cached_graph
    if cached_graph:
        return cached_graph  # Використовуємо кешовану версію

    x = np.arange(-2, 2, grid)
    y = x
    all_triplets = [[i, j, k] for i in x for j in y for k in get_zvalue(a, b, i, j)]
    
    results = np.array(all_triplets).transpose()
    df = pd.DataFrame({'x': results[0], 'y': results[1], 'z': results[2]})

    fig = go.Figure(data=px.scatter_3d(df, x='x', y='y', z='z',
                                       color='z', color_continuous_scale=palette,
                                       template="plotly_white",
                                       size_max=10))

    fig.update(layout_coloraxis_showscale=False)
    fig.update_layout(
        autosize=True,  # Додаємо адаптивність
        paper_bgcolor='#ffe6f2',
        title={
            'text': '❤️ Люблю тебе, котусику! ❤️',
            'x': 0.5,  
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(size=24, family="Arial Black", color="#f754c9"),
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
        ))

    cached_graph = fig.to_html(full_html=False)  # Кешуємо графік
    return cached_graph

@app.route("/")
def home():
    graph_html = draw_heart()
    response = make_response(render_template_string(
        """<html>
        <head>
        <style>
            body { margin: 0; overflow: hidden; display: flex; justify-content: center; align-items: center; height: 100vh; width: 100vw; background: #ffe6f2; }
            #plotly-container { width: 100vw; height: 100vh; }
        </style>
        </head>
        <body>
            <div id="plotly-container">{{ graph | safe }}</div>
        </body>
        </html>""", graph=graph_html))
    response.headers["Cache-Control"] = "public, max-age=86400"  # Кеш на 1 день
    return response


# Фоновий рендеринг для швидкого старту
threading.Thread(target=draw_heart).start()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
