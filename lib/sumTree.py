import collections
import numpy as np
class TreeNode:
    def __init__(self, left=None, right=None, parent=None, data=None, weight=0.0):
        self.left = left
        self.right = right
        self.parent = parent
        self.data = data
        self.weight = weight
        self.is_leaf_node = False

    def update(self, data, weight):
        self.data = data
        self.weight = weight

    def set_is_leaf_node(self):
        if self.left is None and self.right is None:
            self.is_leaf_node = True
        else:
            self.is_leaf_node = False
        return self.is_leaf_node

class SumTree:
    def __init__(self, capacity=1000):
        self.capacity_ = capacity
        self.cursor_ = 0
        self.node_map_ = {}
        self.tree_ = self.build()
        self.eps_ = np.finfo(np.float64).eps.item()

    def build(self):

        def build_tree(idx_min, idx_max, parent=None) -> TreeNode or None:
            """

            :param idx_min: the index left bound, inclusive
            :param idx_max: the index right bound, inclusive
            :return:
            """
            n_num = idx_max - idx_min + 1
            if n_num < 1:
                return None
            elif n_num == 1:
                self.node_map_[idx_min] = TreeNode(parent=parent)
                self.node_map_[idx_min].set_is_leaf_node()
                return self.node_map_[idx_min]
            left_num = n_num // 2
            right_num = n_num - left_num
            left_start = idx_min
            left_end = left_start + left_num - 1
            right_end = idx_max
            right_start = right_end - right_num +1

            root = TreeNode()

            left_node = build_tree(left_start, left_end, parent=root)
            right_node = build_tree(right_start, right_end, parent=root)

            root.left = left_node
            root.right = right_node
            root.parent = parent
            root.set_is_leaf_node()
            return root

        return build_tree(0, self.capacity_-1, parent=None)

    def update_node_by_instance(self, node: TreeNode, data, weight):
        """
        Update the node data/weight given the node instance
        :param node: node instance --TreeNode
        :param data: any
        :param weight: float
        :return:
        """
        assert weight >= 0.0
        delta = weight - node.weight
        node.data = data
        node.update(data=data, weight=weight)
        node = node.parent
        while node is not None:
            node.weight += delta
            node = node.parent
        
    def add_new_data(self, data, weight):
        """
        For RL agent. Only need to use this method to add new data
        :param data:
        :param weight:
        :return:
        """
        node = self.node_map_[self.cursor_]
        self.update_node_by_instance(node=node, data=data, weight=weight)
        self.cursor_ += 1
        if self.cursor_ >= self.capacity_:
            self.cursor_ = 0

    def bfs_traverse(self):
        """
        This method is to view the data in the bfs tree
        :return:
        """
        node = self.tree_
        q = collections.deque()
        q.append(node)
        res = []
        while q:
            layer = []
            for _ in range(len(q)):
                node = q.popleft()
                layer.append(node.weight)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            res.append(layer)
        return res

    def _locate_leaf_node(self, weight):
        root = self.tree_
        assert weight < root.weight
        while not root.is_leaf_node:
            if weight < root.left.weight:
                root = root.left
            else:
                weight = weight - root.left.weight
                root = root.right

        return root

    def sample(self, n_sample):
        weights = np.random.uniform(
            low=0.0,
            high=self.tree_.weight - self.eps_,
            size=n_sample)
        res = []
        for w in weights:
            res.append(self._locate_leaf_node(w))
        return res













