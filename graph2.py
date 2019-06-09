import os
os.environ["PATH"] += os.pathsep + 'C:\\graphviz\\bin'
from graphviz import Graph
import json
import glob
def main():

    files = glob.glob("dados\*.json")
    g = Graph('G')

    for each in files:
    
        with open(each, 'r', encoding="utf8") as f:
            data = json.load(f)

        g.attr('node', shape='point', label='')

        for key in data:
            g.node(key)

        for key in data:
            if(key is not None):
                if(data[key]["replie_to"] is not None):
                    g.edge(key, data[key]["replie_to"])
                # if(data[key]["quoting"] is not None):
                    # g.edge(key, data[key]["quoting"], color="red")

            

    g.view()


if __name__ == "__main__":
    main()