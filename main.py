from flask import Flask, render_template_string
import os
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import pandas as pd

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

def draw_heart(a=9/200, b=0.01, grid=0.05, palette=['#ff0000', '#ff69b4', '#ff1493']):
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
        autosize=True,  
        paper_bgcolor='rgba(255, 230, 242, 1)',  
        title={
            'text': '❤️ Люблю тебе котусику! ❤️',
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

    return fig.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True})

@app.route("/")
def home():
    graph_html = draw_heart()
    return render_template_string(
        """<!DOCTYPE html>
        <html lang="uk">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                html, body { 
                    width: 100vw; 
                    height: 100vh; 
                    overflow: hidden; 
                    background: #f754c9 !important; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center; 
                }
                #plotly-container { width: 100vw; height: 100vh; }
                .plotly-graph-div { width: 100% !important; height: 100% !important; }
                svg.main-svg { width: 100% !important; height: 100% !important; }
            </style>
        </head>
        <body>
            <div id="plotly-container">{{ graph | safe }}</div>
            <script>
                function resizePlotly() {
                    let graph = document.getElementById('plotly-container').getElementsByClassName('plotly-graph-div')[0];
                    if (graph) {
                        Plotly.relayout(graph, { width: window.innerWidth, height: window.innerHeight });
                    }
                }
                window.addEventListener('resize', resizePlotly);
                window.onload = resizePlotly;
            </script>
        </body>
        </html>""", graph=graph_html)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
