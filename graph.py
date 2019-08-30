import glob
import json
from graphviz import Graph
import os
os.environ["PATH"] += os.pathsep + 'C:\\graphviz\\bin'


def main():

    files = glob.glob("dados/*.json")
    g = Graph('G')

    # for each in files:

    try:
        with open("dados/replies_1065400254151954432.json", 'r', encoding="utf8") as f:
            data = json.load(f)

        g.attr('node', label='')

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
