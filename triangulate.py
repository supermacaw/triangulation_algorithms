import networkx as nx

def get_elim_order_mcsm(nxgraph):
    """ Input: a networkx graph nxgraph
        Output: A minimal elimination ordering of the graph and corresponding triangulated graph
    """
    
    
def lb_triangulate(nxgraph, order):
    """Input: nxgraph, and an ordering on it
       Output: a minimal triangulation of the input graph
    """
    h = nxgraph.copy()
    for i in range(0, len(order)):
        neighbors = h.neighbors(order[i])
        neighbors.append(order[i])
        copy = h.copy()
        copy.remove_nodes_from(neighbors)
        components = nx.connected_components(copy)
        for cc in components:
            nodes_to_fill_in = [] 
            for node in cc:
                for xnode in neighbors:
                    if(xnode in nxgraph.neighbors(node)):
                        nodes_to_fill_in.append(xnode)
            for node1 in nodes_to_fill_in:
                for node2 in nodes_to_fill_in:
                    if not node1 == node2:
                        h.add_edge(node1, node2)
                
    return h 

def greedy_triangulate(nxgraph, depth, heuristic):
    """Input: nxgraph, depth of search, type of heuristic: 'fill, width, weight'
       Output: fully triangulated version of input nxgraph 
    """

    h = nxgraph.copy()
    while len(h.nodes()) > 0: 
        minCost = float("inf")
        best = None 
        for node in r: 
            cost = compute_cost(h, node, depth, heuristic)
            if cost < minCost:
                minCost = cost
                best = node
        remove_and_fill_in(h, r, best)
    return h 

def compute_cost(G, n, depth, heuristic):
    """Input: G, R are nxgraphs, n = node to remove, depth = depth of search
           
    >>> g = nx.Graph()
    >>> g.add_nodes_from([1,2,3,4])
    >>> g.add_edges_from([(1,2),(2,3),(2,4)])
    >>> compute_cost(g, 2, 1, 'fill')
    3
    >>> g.add_nodes_from([5])
    >>> g.add_edges_from([(1,5),(4,5)])
    >>> compute_cost(g, 2, 2, 'fill')
    3 
    """
    if heuristic is 'fill':
        cost = count_fill_ins(G, n)
    elif heuristic is 'width':
        cost = len(set(G.neighbors(n)) & set(G.nodes()))  
    elif heuristic is 'weight':
        node_set = set()
        node_set.add(n)
        clique = (set(G.neighbors(n)) & set(G.nodes())) - node_set
        cost = 0 #NEED TO INSERT SOMETHING HERE, SHOULD BE clique's TABLE_SIZE 
    else:
        print "INVALID HEURISTIC"
    h = G.copy()
    remove_and_fill_in(h, n)
    if depth > 1 and not (len(h.nodes()) == 0):
        minCost = float("inf")
        for node in h.nodes():
            node_cost = compute_cost(h, node, depth - 1, heuristic)
            if node_cost < minCost:
                minCost = node_cost
        cost = cost + minCost
    return cost

"""The rest are helper functions"""

def remove_and_fill_in(nxgraph, node):
    neighbors = nxgraph.neighbors(node)
    nxgraph.remove_node(node)
    for node1 in neighbors:
        for node2 in neighbors:
            if node1 != node2 and not nxgraph.has_edge(node2, node1):
                nxgraph.add_edge(node1, node2)

def count_fill_ins(G, n):
    """Input: nxgraph G, node to remove n 
    Output: number of filled in edges if n were removed from g
    
    >>> g = nx.Graph()
    >>> g.add_nodes_from([1,2,3,4])
    >>> g.add_edges_from([(1,2),(2,3),(2,4)])
    >>> count_fill_ins(g, 2)
    3
    """

    h = G.copy()
    cost = 0
    for node1 in h.neighbors(n):
        for node2 in h.neighbors(n):
            if(not (h.has_edge(node1, node2)) and node1 != node2):
                h.add_edge(node1, node2)
                cost += 1;
    return cost            
