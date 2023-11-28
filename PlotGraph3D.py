import plotly.graph_objects as go
import warnings
import ast
import pandas as pd
import networkx as nx
import itertools
import ast
import networkx as nx


recipes_data = pd.read_csv("recipe_data.csv")

def add_edge(graph, ingredient_list):
    ingredients_combinations = list(itertools.combinations(ingredient_list, 2))
    for combo in ingredients_combinations:
        if graph.has_edge(combo[0], combo[1]):
            graph[combo[0]][combo[1]]["weight"] += 1
        else:
            graph.add_edge(combo[0], combo[1], weight=1)


# Initialize an undirected graph
G = nx.Graph()

# Directory containing recipe files
recipes_dir = "recipes"

# Extract ingredients from txt
txt_path = r".\recipes\aggregated_ingredients.txt"
ingredients_list = open(txt_path).readlines()
ingredients_list = [ingredient.strip() for ingredient in ingredients_list]
# ADD NODES
G.add_nodes_from(ingredients_list)
G.nodes()

for ingredients_str in recipes_data["ingredients"]:
    ingredients_list = ast.literal_eval(ingredients_str)
    add_edge(G, ingredients_list)

G.edges()

largest_component = max(nx.connected_components(G), key=len)
G_sub = G.subgraph(largest_component)

# Crea le posizioni dei nodi
pos = nx.spring_layout(G_sub, dim=3)

# Estrai le coordinate x, y e z dei nodi
node_x = [pos[k][0] for k in G_sub.nodes()]
node_y = [pos[k][1] for k in G_sub.nodes()]
node_z = [pos[k][2] for k in G_sub.nodes()]
node_text = list(G_sub.nodes())

# Crea gli archi
edge_x = []
edge_y = []
edge_z = []
weights = []
for edge in G_sub.edges():
    x0, y0, z0 = pos[edge[0]]
    x1, y1, z1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])
    edge_z.extend([z0, z1, None])
    weights.append(G_sub[edge[0]][edge[1]]['weight'])

# Crea il grafo
edge_trace = go.Scatter3d(
    x=edge_x, y=edge_y, z=edge_z,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_trace = go.Scatter3d(
    x=node_x, y=node_y, z=node_z,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        color=weights,
        size=6,
        colorbar=dict(
            thickness=15,
            title='Peso degli archi',
            xanchor='left',
            titleside='right'
        ),
        line_width=2))

# Crea il layout del grafico
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='Grafo degli ingredienti (3D)',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    annotations=[dict(
                        text="",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002)],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

# Visualizza il grafico interattivo in una nuova finestra
fig.show()
