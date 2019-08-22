import glob
import json


''' def main():

    files = glob.glob("dados/*.json")

    with open("merged_file.json", "w+", encoding='utf8') as out:
        first = True
        for each in files:

            with open(each, 'r', encoding="utf8") as f:
                data = json.load(f)
            if(first):
                out.write("{")
                first = False
            else:
                out.write(",")
            out.write(json.dumps(data, ensure_ascii=False))
        out.write("}")


def main():
    with open("merged_file.json", "r", encoding='utf8') as f:
        print(len(json.load(f)))
'''


def main():
    files = glob.glob("dados/*.json")
    size = 0
    '''
    for each in files:
        with open(each, 'r', encoding="utf8") as f:
            data = json.load(f)
            size += len(data)'''
    with open("dados/replies_1147863151054073857_1147876836011073538.json", 'r', encoding="utf8") as f:
        data = json.load(f)
        size += len(data)
    print(size)


if __name__ == "__main__":
    main()
