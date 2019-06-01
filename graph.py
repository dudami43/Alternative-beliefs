import networkx as nx
import json
import matplotlib.pyplot as plt


def main():
    with open("replies.json", 'r') as f:
        data = json.load(f)
    G = nx.Graph()

    for key in data:
        G.add_node(key)

    for key in data:
        G.add_edge(key, data[key]["replie_to"])

    nx.draw(G, with_labels=False, font_weight='bold')
    plt.show()


if __name__ == "__main__":
    main()
