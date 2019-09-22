import glob
import json
from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + 'C:\\graphviz\\bin'


def main():

    g = Digraph('G')
    g.attr(size='20')
    with open("dados\\believes\\replies_238717783007977473.json", 'r', encoding="utf8") as f:
        data = json.load(f)
    g.attr('node', shape='circle', label="")
    for key in data:
        score = data[key]['sentiment']
        if(score <= -0.8):
            g.node(key, color='#67001F', style="filled")
        elif(score > -0.8 and score <= -0.6):
            g.node(key, color='#B2172B', style="filled")
        elif(score > -0.6 and score <= -0.4):
            g.node(key, color='#D6604D', style="filled")
        elif(score > -0.4 and score <= -0.2):
            g.node(key, color='#F4A582', style="filled")
        elif(score > -0.2 and score < 0):
            g.node(key, color='#FDDBC7', style="filled")
        elif(score == 0.0):
            g.node(key, color='#F8F8F8', style="filled")
        elif(score > 0.0 and score <= 0.2):
            g.node(key, color='#D1E5F0', style="filled")
        elif(score > 0.2 and score <= 0.4):
            g.node(key, color='#92C5DF', style="filled")
        elif(score > 0.4 and score <= 0.6):
            g.node(key, color='#4393C3', style="filled")
        elif(score > 0.6 and score <= 0.8):
            g.node(key, color='#2166AC', style="filled")
        elif(score > 0.8):
            g.node(key, color='#053061', style="filled")
    for key in data:
        if(key is not None):
            if(data[key]["replie_to"] is not None):
                g.edge(data[key]["replie_to"], key)
    g.view()


if __name__ == "__main__":
    main()
