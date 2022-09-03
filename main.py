import pandas as pd
import ast
import networkx as nx
import random
import matplotlib.pyplot as plt
"""
        Mihriban Guneydas

        This program that will read the movie datas from a file. From that dataset, it creates a graph. By using that graph it finds and shows shortest path to Kevin Bacon with help of Djikstra's algorithm.
"""


# General informations about program was added
def heading():
    print("Author       : Mihriban Guneydas")
    print("Class        : CMPS 5323")
    print("Date         : Summer II 2022")
    print(
        "References I :  https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?resource=download"
    )
    print("References II : https://networkx.org\n\n")
    print("Summary of the Program:\n")
    print(
        "This program that will read the movie datas from a file. From that dataset, it creates a graph. By using that graph it finds and shows shortest path to Kevin Bacon with help of Djikstra's algorithm.\n\n"
    )
heading()

# Loading data from dataset
df = pd.read_csv('dataset.csv')
df['cast'] = df.cast.apply(ast.literal_eval)
df.head()

# Creating graph to find shortest path
G = nx.Graph()
actorList = []

def shortestPathGraph(row):
    G.add_node(row.title)
    for actor in row.cast:
        if actor['name'] not in actorList:
            G.add_node(actor['name'])
            actorList.append(actor['name'])
        G.add_edge(row.title, actor['name'])

_ = df.apply(lambda r: shortestPathGraph(r), axis=1)

# Here I chose one random actor from added_actor list
random = random.sample(actorList, 1)
random

# Finding Bacon Number of that actor
for i in random:
    path = nx.shortest_path(G, source=i, target='Kevin Bacon')
    print('{0}s Bacon Number is: {1}'.format(i, int(len(path) / 2)))
    print(path)

# Creating the graph GH
GH = nx.Graph()
size = int(len(path))

# Adding all the nodes and edges based on the shortest path
for i in range(size):
    # adding nodes
    if i % 2 == 0:
        GH.add_node(path[i])
    #a dding edges
    else:
        GH.add_edge(path[i - 1], path[i + 1], movie=path[i])

pos = nx.circular_layout(GH)

# drawing nodes
nx.draw_networkx_nodes(GH,
                       pos,
                       node_color="#ADD8E6",
                       node_shape="o",
                       node_size=4000)

# drawing edges
nx.draw_networkx_edges(GH,
                       pos,
                       arrowsize=90000,
                       width=5,
                       alpha=0.5,
                       edge_color="r")

# putting node labels
nx.draw_networkx_labels(GH, pos, font_size=10, font_family="sans-serif")

# putting edge labels
edge_labels = nx.get_edge_attributes(GH, "movie")
nx.draw_networkx_edge_labels(GH, pos, edge_labels)

ax = plt.gca()
ax.margins(0.08)
plt.axis("off")
plt.tight_layout()
plt.show()

# Main Program
if __name__ == "__main__":
    heading()
