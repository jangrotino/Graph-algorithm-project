#Igor Jangrot 414640 gr.6

from data import runtests
from queue import deque
import heapq
import copy


#graph representation
class Node:
    def __init__(self,idx, nei):
        self.idx=idx
        self.out=nei

    def connect_to(self,v):
        self.out.add(v)


def create_graph(graph, V):
    G: list[Node] = [Node(i, graph[i]) for i in range(0, V)]  
    return G


def lex_BFS(G):
    n=len(G)
    visited=[]
    starting_set=set([i for i in range(1,n)])
    to_be_visited=deque([starting_set,set([0])])

    while len(visited)<n:
        visited_vertex=to_be_visited[-1].pop()
        if not to_be_visited[-1]:
            to_be_visited.pop()
        visited.append(visited_vertex)
        new_to_be_visited=deque()
        for i in range(len(to_be_visited)-1,-1,-1):
            Y=set()
            for v in to_be_visited[i]:
                if visited_vertex in G[v].out:
                    Y.add(v)
            to_be_visited[i]-=Y
            if Y:
                new_to_be_visited.appendleft(Y)
            if to_be_visited[i]:
                new_to_be_visited.appendleft(to_be_visited[i])
        to_be_visited=new_to_be_visited
    return visited


def make_graph_weighted(edge_list, N):
    adjacency_list = [[] for _ in range(N)]
    for elem in edge_list:
        adjacency_list[elem[0]-1].append((elem[1]-1, elem[2]))
        adjacency_list[elem[1]-1].append((elem[0]-1, elem[2]))
    return adjacency_list


def dfs(adjacency_list, lord, loard_num, mutual_places, N):
    stack = []
    visited = [False for _ in range(N)] 
    parent = [-1 for _ in range(N)]
    weight = [0 for _ in range(N)]
    start = lord[0] - 1
    visited[start] = True
    mutual_places[start].add(loard_num)
    stack.append(start)
    protected = 0

    while len(stack) > 0:
        curr = stack[-1]
        stack.pop()
        for elem in adjacency_list[curr]:
            child, w = elem
            if not visited[child]:
                parent[child] = curr
                weight[child] = w
                visited[child] = True
                stack.append(child)

    for i in range(1, len(lord)):
        curr = lord[i] - 1 
        while curr != -1:
            mutual_places[curr].add(loard_num)
            protected += weight[curr]
            weight[curr] = 0
            curr = parent[curr]

    return protected


def prim(adjacency_list, vertex_num, start):
    processed = [False for _ in range(vertex_num)]
    key = [float('inf') for _ in range(vertex_num)]
    parent = [-1 for _ in range(vertex_num)]
    edge_list = []
    q = []
    heapq.heappush(q, (0, start))
    key[start] = 0

    while q:
        u_w, u = heapq.heappop(q)

        if processed[u]:
            continue
        
        processed[u] = True

        if parent[u] != -1:
            edge_list.append((parent[u] + 1, u + 1, u_w))

        for v, v_w in adjacency_list[u]:
            if not processed[v] and v_w < key[v]:
                parent[v] = u
                key[v] = v_w
                heapq.heappush(q, (v_w, v))

    return edge_list


def create_chordal_graph(mutual_places, L):
    chordal_graph = [set() for _ in range(L)]

    for i in range(L):
        for j in range(len(mutual_places)):
            if i in mutual_places[j]:
                for elem in mutual_places[j]:
                    if elem != i:
                        chordal_graph[i].add(elem)
    
    return chordal_graph


def optimal_sol(chordal_graph, lord_street_len):
    pom = copy.deepcopy(lord_street_len)
    visited = [False for _ in range(len(chordal_graph))]
    lords_color = [-1 for _ in range(len(chordal_graph))]
    order = lex_BFS(create_graph(chordal_graph, len(chordal_graph)))
    res = 0

    for i in range(len(order)-1, -1, -1):
        visited[order[i]] = True
        if lord_street_len[order[i]] > 0:
            lords_color[order[i]] = 1
            for elem in chordal_graph[order[i]]:
                if not visited[elem]:
                    lord_street_len[elem] = lord_street_len[elem] - lord_street_len[order[i]]
                    if lord_street_len[elem] < 0:
                        lord_street_len[elem] = 0
            lord_street_len[order[i]] = 0  
           
    for i in order: 
        if lords_color[i] == 1:
            flag = True
            for elem in chordal_graph[i]:
                if lords_color[elem] == 0:
                    flag = False
                    break
            if flag:
                res += pom[i]
                lords_color[i] = 0
    
    return res


def my_solve(N, streets, lords):
    print(f"Place: {N}, ulice: {len(streets)}, lordowie: {len(lords)}")

    adjacency_list = make_graph_weighted(streets, N)

    edge_list = prim(adjacency_list, N, 0)
    adjacency_list = make_graph_weighted(edge_list, N)

    mutual_places = [set() for _ in range(N)]
    lords_streets_len = [0 for _ in range(len(lords))]

    for i in range(len(lords)):
        lords_streets_len[i] = dfs(adjacency_list, lords[i], i, mutual_places, N)

    chordal_graph = create_chordal_graph(mutual_places, len(lords))

    return optimal_sol(chordal_graph, lords_streets_len)


runtests(my_solve)