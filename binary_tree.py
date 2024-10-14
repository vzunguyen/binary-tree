import matplotlib.pyplot as plt
import networkx as nx
import time

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.graph = nx.Graph()  # Graph to store nodes and edges
        self.pos = {}  # To store positions of nodes for visualization
        self.permanent_color = {}  # To keep track of nodes that should stay green when found

    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)
        self._update_graph()  # Update the graph after insertion
    
    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)
    
    def search(self, value):
        """Public method to search for a value with visualization."""
        found = self._search_recursive(self.root, value)
        if found:
            print(f"Number {value} found!")
        else:
            print(f"Number {value} not found!")
        return found

    def _search_recursive(self, node, value):
        """Private recursive method for searching a value with visualization."""
        if node is None:
            self._update_graph(visited=None)  # No match found
            return False
        
        self._update_graph(visited=node.value)  # Update graph at each step of the search
        time.sleep(1)  # Pause to show the traversal path
        
        if node.value == value:
            self.permanent_color[node.value] = 'green'  # Mark the found node to be green permanently
            self._update_graph(visited=node.value)
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

    def inorder_traversal(self):
        """Performs inorder traversal and visualizes it."""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        """Helper function for inorder traversal."""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._update_graph(visited=node.value)  # Update graph during traversal
            time.sleep(1)  # Pause to visualize step-by-step traversal
            self._inorder_recursive(node.right, result)
    
    def _update_graph(self, visited=None):
        """Helper function to update the graph with the current state of the tree."""
        self.graph.clear()
        self._add_edges(self.root)
        self._visualize(visited)
    
    def _add_edges(self, node, parent=None):
        """Recursively adds nodes and edges to the graph."""
        if node:
            self.graph.add_node(node.value)
            if parent:
                self.graph.add_edge(parent.value, node.value)
            self._add_edges(node.left, node)
            self._add_edges(node.right, node)
    
    def _get_tree_layout(self, node, x=0, y=0, layer_gap=1.5, x_offset=1):
        """Computes the layout for the tree visualization."""
        if node is None:
            return {}
        
        pos = {node.value: (x, y)}
        if node.left:
            pos.update(self._get_tree_layout(node.left, x - x_offset, y - layer_gap, layer_gap, x_offset / 2))
        if node.right:
            pos.update(self._get_tree_layout(node.right, x + x_offset, y - layer_gap, layer_gap, x_offset / 2))
        
        return pos
    
    def _visualize(self, visited=None):
        """Visualizes the BST using matplotlib and networkx with node highlighting during traversal."""
        plt.clf()  # Clear the plot for updating
        self.pos = self._get_tree_layout(self.root)  # Get layout based on tree structure

        # Determine node colors: permanent colors (green for found nodes) and visited colors (orange for current)
        node_colors = []
        for node in self.graph.nodes():
            if node in self.permanent_color:
                node_colors.append(self.permanent_color[node])  # Use green if the node is found
            elif node == visited:
                node_colors.append("orange")  # Highlight the currently visited node
            else:
                node_colors.append("lightblue")  # Default color for unvisited nodes

        nx.draw(self.graph, self.pos, with_labels=True, node_color=node_colors, node_size=2000, font_size=12, font_weight="bold")
        plt.pause(0.5)  # Pause to visualize each step
    
    def visualize(self):
        """Static visualization of the BST."""
        self._visualize()

# Example usage
bst = BinarySearchTree()
bst.insert(5)
bst.insert(3)
bst.insert(7)
bst.insert(1)
bst.insert(10)
bst.insert(8)
bst.insert(4)
bst.insert(2)

# Visualize the search for an element
print("Searching for 7:")
bst.search(7)  # This will visualize the search path and change the node color to green if found

print("Searching for 4:")
bst.search(4)  # Visualize search for a non-existent value
