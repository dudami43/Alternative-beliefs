import os
os.environ["PATH"] += os.pathsep + 'C:\\graphviz\\bin'
from graphviz import Graph
import json

def main():
    with open("replies_trump.json", 'r', encoding="utf8") as f:
        data = json.load(f)
    g = Graph('G')
    g.attr('node', shape='point', label='')

    for key in data:
        g.node(key)

    for key in data:
        if(key is not None and data[key]["replie_to"] is not None):
            g.edge(key, data[key]["replie_to"])

    g.view()


if __name__ == "__main__":
    main()