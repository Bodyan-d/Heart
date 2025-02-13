from flask import Flask, render_template_string, make_response
import os
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import pandas as pd
import threading

app = Flask(__name__)

# Кеш для графіка, щоб не будувати щоразу
cached_graph = None

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

def draw_heart(a=9/200, b=0.01, grid=0.05, palette=['#ff0000', '#ff4444', '#ff1493']):
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
                                       height=800, width=800,
                                       template="plotly_white",
                                       size_max=10))

    fig.update(layout_coloraxis_showscale=False)
    fig.update_layout(
        paper_bgcolor='#ffe6f2',  # Колір фону
        title={
            'text': '❤️ Люблю тебе, котусику! ❤️',
            'x': 0.5,  # Центруємо заголовок
            'y': 0.95,  # Трохи вище, щоб гарніше виглядало
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
        "<html><body style='text-align: center; background: #ff1493;'>{{ graph | safe }}</body></html>", graph=graph_html))
    response.headers["Cache-Control"] = "public, max-age=86400"  # Кеш на 1 день
    return response

# Фоновий рендеринг, щоб прискорити перший запит
threading.Thread(target=draw_heart).start()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)