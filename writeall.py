import glob
import json


def main():

    files = glob.glob("dadoss/*.json")

    #out = open("todos.json", "w+", encoding='utf8')
    data = []

    # for each in files:

    # with open(each, 'r', encoding="utf8") as f:
    # data.append(json.load(f))

    with open("todos.json", 'r', encoding="utf8") as f:
        data = json.load(f)
    print(len(data))
    #out.write(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    main()
