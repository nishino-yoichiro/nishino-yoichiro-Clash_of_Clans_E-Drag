class Graph:
    def __init__(self):
        self.adjacency_dict = {}

    def add_node(self, node):
        """ Add a node to the graph. 
        :param node: The node to add
        :type node: Building
        """
        if node not in self.adjacency_dict:
            self.adjacency_dict[node] = set()

    def add_edge(self, node1, node2, distance):
        """ Add an edge to the graph.
        :param node1: The first node
        :param node2: The second node
        :param distance: The distance between the two nodes
        :type node1: Building
        :type node2: Building
        :type distance: float
        """
        if node1 in self.adjacency_dict and node2 in self.adjacency_dict:
            if (node2, distance) not in self.adjacency_dict[node1]:
                self.adjacency_dict[node1].add((node2, distance))
            if (node1, distance) not in self.adjacency_dict[node2]:
                self.adjacency_dict[node2].add((node1, distance))

    def get_neighbors(self, node):
        """ Get the neighbors of a node.
        :param node: The node to get the neighbors of
        :type node: Building
        :rtype set
        :return: The neighbors of the node
        """
        return self.adjacency_dict.get(node, set())
    
    def delete_node(self, node):
        """ Delete a node from the graph.
        :param node: The node to delete
        :type node: Building
        :rtype void
        :return None
        """
        if node in self.adjacency_dict:
            del self.adjacency_dict[node]
            for key in self.adjacency_dict:
                self.adjacency_dict[key] = {neighbor for neighbor in self.adjacency_dict[key] if neighbor[0] != node}

    def __repr__(self):
        return str(self.adjacency_dict)