import glob
import json
from graphviz import Graph
import os
os.environ["PATH"] += os.pathsep + 'C:\\graphviz\\bin'


def main():

    files = glob.glob("dados/*.json")
    quotes_trump = glob.glob("dados/replies_238717783007977473_*.json")
    g = Graph('G')

    for each in quotes_trump:

        try:
            with open(each, 'r', encoding="utf8") as f:
                data = json.load(f)

            g.attr('node')

            for key in data:
                g.node(key)

            for key in data:
                if(key is not None):
                    if(data[key]["replie_to"] is not None):
                        g.edge(key, data[key]["replie_to"])
                    # if(data[key]["quoting"] is not None):
                        # g.edge(key, data[key]["quoting"], color="red")
        except:
            print("each")

    g.view()


if __name__ == "__main__":
    main()
