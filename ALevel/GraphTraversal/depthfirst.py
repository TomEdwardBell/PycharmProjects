GRAPH = {"A": ["B", "D", "E"],
         "B": ["A", "C", "D"],
         "C": ["B", "G"],
         "D": ["A", "B", "E", "F"],
         "E": ["A", "D"],
         "F": ["D"],
         "G": ["C"]}
visitedList = []
# an empty list of visited nodes

def dfs(graph, currentVertex, visited):
    # append currentVertex to list of visited nodes
    visited.append(currentVertex)
    for vertex in graph[currentVertex]:
        # check neighbours of currentVertex
        if vertex not in visited:
            dfs(graph, vertex, visited)
            # recursive call
            # stack will store return address, parameters and local variables
    return visited

# main program
traversal = dfs(GRAPH, "A", visitedList)
print("Nodes visited in this order: ", traversal)
