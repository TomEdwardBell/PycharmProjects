graph = {
    "A": {"B": 7, "D": 3},
    "B": {"A": 7, "C": 3, "D": 2, "E": 6},
    "C": {"B": 3, "D": 4, "E": 1},
    "D": {"A": 3, "B": 2, "C": 4, "E": 7},
    "E": {"C": 1, "D": 7}
}


def dijkstra(graph, start, end):
    weights = {}
    for key in graph:
        weights[key] = 9999
    weights[start] = 0

def sort_dict(dictionary):
    old = dictionary
    new = {}
    smallestvalue = 99999
    smallestkey = ""
    for item in old:
        if old[item] < smallestvalue:
            smallestkey = item
            smallestvalue = old[item]
    del old[smallestkey]
    new = old
    new = new[item] + sort_dict(old)
    return new


print(sort_dict({"A":999, "B":2, "C":10, "D":0}))