
import pandas as pd
import re
#function to deal with the given data, deleting unexpected symbols in article's outlinks
def deal(row):
    r=set()
    for x in row:
       x=re.findall(r'[0-9a-zA-Z]+', x)
       x=''.join(map(str, x))
       r.add(x)
    return r

store = pd.HDFStore('store.h5')
df2=store['df2']
df2.name=df2.name.apply(lambda x: re.findall(r'[0-9a-zA-Z]+', x))
df2.name=df2.name.apply(lambda x: ''.join(map(str, x)))
df2["out_links"]=df2["out_links"].apply(deal)
df2["out_links"]=df2["out_links"].apply(set)
df2.set_index('name')['out_links'].to_dict()
my_graph= dict(zip(df2.name, df2.out_links))

def bfs_shortest_path(graph, start_node, end_node):
    queue = [[start_node]]
    visited = set()
    while queue:
        #first path in the queue
        path = queue.pop(0)
        #last node in the path
        vertex = path[-1]
        #Checks if we got to the end
        if vertex == end_node:
            return len(path)-1
        elif vertex not in visited:
            #enumerate all adjacent nodes, construct a new path and push it into the queue
            for current_neighbour in graph.get(vertex, []):
                new_path = list(path)
                new_path.append(current_neighbour)
                queue.append(new_path)
            #Mark the vertex as visited
            visited.add(vertex)

def diameter(graph):
   #shortest path for each note to another
   shortest_path_node=[]
   #eccentricity of each node,which is the max of shortest paths
   eccentricity_of_node =[]
   for key in my_graph.keys():
       shortest_path_node=[bfs_shortest_path(my_graph, key, key1) for key1 in my_graph.keys()]
       ecc=max(shortest_path_node)
       eccentricity_of_node.append(ecc)
    #diameter is the max of eccentricity of each node
   diam = max(eccentricity_of_node)
   return diam

#call the function diameter

    


