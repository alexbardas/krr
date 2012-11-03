def back(k, n, st, values):
    for i in range(2):
        st[k] = i
        if (k < n-1):
            back(k+1, n, st, values)
        if k == n-1:
            values.append(list(st))

class FTree(object):
    """
    Tree data structure which stores a formula, making it easier to be evaluated

    Storage mode: all propositions must be leaves, `not` operator has only one
    left leaf (design choice) and the other operators have two leaves.
    """
    def __init__(self, operator, left=None, right=None, propositions=None):
        assert operator != None

        self.val = operator
        self.left = left # operator or proposition
        self.right = right # operator or proposition
        self.propositions = propositions

    def eval(self):
        if self.propositions:
            # every proposition can be true or false
            # generate all possible combinations of
            # truth values for propositions
            length = len(self.propositions)
            proposition_values = []
            back(0, length, [0]*length, proposition_values)
            for values in proposition_values:
                mappings = {k:v for k, v in zip(self.propositions, values)}
                print mappings
                print FTree.compute(self, mappings)
            print '\n'

    @staticmethod
    def compute(node, mappings):
        """
        Computes the truth value of the formula
        """
        # if the node is a proposition,
        if node.val in ['p', 'q', 'r', 's', 't', 'u', 'v']:
            return mappings[node.val]
        if node.val == 'not':
            return not FTree.compute(node.left, mappings)
        if node.val == 'and':
            return FTree.compute(node.left, mappings) and FTree.compute(node.right, mappings)
        if node.val == 'or':
            return FTree.compute(node.left, mappings) or FTree.compute(node.right, mappings)
        if node.val == '<->':
            return FTree.compute(node.left, mappings) == FTree.compute(node.right, mappings)
        if node.val == '->':
            return True

    def __str__(self):
        """
        Returns an inorder tree traversal
        """
        def print_tree(tree):
            if tree == None: return ' '
            return print_tree(tree.left) + tree.val + print_tree(tree.right)

        return print_tree(self)

    @staticmethod
    def compare(ftree1, ftree2):
        """
        Tests if the 2 ftrees are identical
        """
        if ftree1 == None or ftree2 == None:
            if ftree1 == ftree2: return True
            return False

        return ftree1.val == ftree2.val and  FTree.compare(ftree1.left, ftree2.left) and \
            FTree.compare(ftree1.right, ftree2.right)