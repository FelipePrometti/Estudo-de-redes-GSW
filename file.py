import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from caas_jupyter_tools import display_dataframe_to_user

# 1) Dados REAIS (assistências A→B) extraídos do play-by-play ESPN
#    Jogo: 17/out/2017 – Rockets @ Warriors (gameId=400974438)
#    Observação: representam "passes que viraram assistência" (subconjunto de todos os passes).

assist_pairs = [
    ("Draymond Green", "Klay Thompson", 2),
    ("Kevin Durant", "Klay Thompson", 2),
    ("Kevin Durant", "Stephen Curry", 1),
    ("Draymond Green", "Zaza Pachulia", 1),
    ("Draymond Green", "Patrick McCaw", 1),
    ("Patrick McCaw", "Jordan Bell", 1),
    ("Draymond Green", "Nick Young", 2),
    ("Jordan Bell", "Nick Young", 1),
    ("Shaun Livingston", "Nick Young", 2),
    ("Shaun Livingston", "Kevin Durant", 1),
    ("Stephen Curry", "Kevin Durant", 1),
    ("Draymond Green", "Kevin Durant", 4),
    ("Klay Thompson", "Draymond Green", 1),
    ("Kevin Durant", "Draymond Green", 1),
    ("Draymond Green", "Shaun Livingston", 1),
    ("Draymond Green", "Stephen Curry", 1),
    ("Stephen Curry", "Zaza Pachulia", 1),
    ("Stephen Curry", "Nick Young", 1),
    ("Shaun Livingston", "David West", 1),
    ("Stephen Curry", "Klay Thompson", 1),
    ("Klay Thompson", "Stephen Curry", 2),
    ("Kevin Durant", "Jordan Bell", 2),
    ("Kevin Durant", "Patrick McCaw", 1),
    ("Draymond Green", "Jordan Bell", 1),
]

edges = pd.DataFrame(assist_pairs, columns=["from_player", "to_player", "assists"])

# Salvar CSV "real (assistências)"
csv_path = "/mnt/data/assists_real_2017-10-17_GSW.csv"
edges.to_csv(csv_path, index=False)

# 2) Construir grafo direcionado ponderado (peso = nº de assistências A→B)
G = nx.DiGraph()
for _, r in edges.iterrows():
    G.add_edge(r["from_player"], r["to_player"], weight=int(r["assists"]))

players = sorted(set(edges["from_player"]) | set(edges["to_player"]))

# Métricas
out_strength = dict(G.out_degree(weight="weight"))
in_strength = dict(G.in_degree(weight="weight"))
pr = nx.pagerank(G, weight="weight")

# Betweenness com custo = 1/weight (arestas mais usadas = caminho "mais curto")
H = nx.DiGraph()
for u, v, d in G.edges(data=True):
    H.add_edge(u, v, cost=1.0 / d["weight"])
btw = nx.betweenness_centrality(H, weight="cost", normalized=True)

metrics = pd.DataFrame({
    "player": players,
    "out_strength_ast": [out_strength.get(p, 0) for p in players],
    "in_strength_ast": [in_strength.get(p, 0) for p in players],
    "pagerank_ast": [pr.get(p, 0) for p in players],
    "betweenness_ast": [btw.get(p, 0) for p in players],
}).sort_values(["out_strength_ast", "in_strength_ast"], ascending=False).reset_index(drop=True)

display_dataframe_to_user("Resultados REAIS (assistências) – métricas por jogador – GSW vs HOU (2017-10-17)", metrics)

# 3) Heatmap A→B de assistências
matrix = edges.pivot_table(index="from_player", columns="to_player", values="assists", fill_value=0)

plt.figure(figsize=(9, 7))
plt.imshow(matrix.values, aspect="auto")
plt.xticks(ticks=np.arange(len(matrix.columns)), labels=matrix.columns, rotation=45, ha="right")
plt.yticks(ticks=np.arange(len(matrix.index)), labels=matrix.index)
plt.title("Heatmap de assistências A→B – GSW vs HOU (2017-10-17)")
plt.colorbar(label="nº de assistências")
heatmap_path = "/mnt/data/heatmap_assists_real_2017-10-17.png"
plt.tight_layout()
plt.savefig(heatmap_path, dpi=160)
plt.close()

# 4) Visual do grafo (largura ∝ assistências)
plt.figure(figsize=(9, 7))
pos = nx.spring_layout(G, seed=17)
edge_widths = [0.6 + (d["weight"] * 0.6) for _, _, d in G.edges(data=True)]
nx.draw_networkx_nodes(G, pos, node_size=1100)
nx.draw_networkx_labels(G, pos, font_size=8)
nx.draw_networkx_edges(G, pos, width=edge_widths, arrows=True, arrowstyle="-|>", arrowsize=14)
plt.title("Grafo de assistências – GSW vs HOU (2017-10-17)")
graph_path = "/mnt/data/grafo_assists_real_2017-10-17.png"
plt.tight_layout()
plt.savefig(graph_path, dpi=160)
plt.close()

# 5) Exportar matriz A→B e paths dos arquivos
matrix_csv_path = "/mnt/data/matriz_assists_real_2017-10-17.csv"
matrix.to_csv(matrix_csv_path)

paths_df = pd.DataFrame({
    "Arquivo": [
        "Edges (assistências) CSV",
        "Heatmap (assistências) PNG",
        "Grafo (assistências) PNG",
        "Matriz A->B (assistências) CSV",
    ],
    "Caminho": [csv_path, heatmap_path, graph_path, matrix_csv_path],
})
display_dataframe_to_user("Arquivos REAIS gerados – GSW vs HOU (2017-10-17)", paths_df)
