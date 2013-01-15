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
    def __init__(self, operator, left=None, right=None):
        assert operator != None

        self.val = operator
        self.left = left # operator or proposition
        self.right = right # operator or proposition

    def is_operator(self):
        """ Check of the current node is an operator or a proposition """
        if self.val in ['~', '<>', '[]', '&', '|', '->', '<->']:
            return True

    def compute(self, world):
        """
        Computes the truth value of the formula
        """

        # if the node is a proposition,
        if not self.is_operator():
            return world in FTree.truth and self.val in FTree.truth[world]
        if self.val == '~':
            return not self.left.compute(world)
        # The formula <>p is true at a world w_0 if there exists a world w_i, accessible from w_0,
        # such that p holds at w_i. The formula <>p is false if p is false at all worlds w_ij
        # accessible from w_0.
        if self.val == '<>':
            if not world in FTree.next: return False
            return any((self.left.compute(w) for w in FTree.next[world]))

        # The formula []p is true at a world w_0 if p is true at all worlds w_ij accessible from w_0.
        # The formula []p is false if there exists a world w_i such that p is false at w_i.
        if self.val == '[]':
            if not world in FTree.next: return True
            return all((self.left.compute(w) for w in FTree.next[world]))
        if self.val == '&':
            return self.left.compute(world) and self.right.compute(world)
        if self.val == '|':
            return self.left.compute(world) or self.right.compute(world)
        if self.val == '<->':
            return self.left.compute(world) == self.right.compute(world)
        if self.val == '->':
            left_truth = self.left.compute(world)
            right_truth = self.right.compute(world)
            if not left_truth or right_truth: return True
            return False

    def justify(self, world, steps, current_step=0):
        if current_step <= steps or steps == -1:
            print '%s is %s at %s' % ('  ' * current_step + '* ' + str(self), self.compute(world), world)
            if self.left:
                self.left.justify(world, steps, current_step+1)
            if self.right:
                self.right.justify(world, steps, current_step+1)

    def __str__(self):
        """
        Returns an inorder tree traversal
        """
        def print_tree(tree):
            if tree:
                if not tree.left and not tree.right:
                    return '%s' % tree.val
                elif tree.left and not tree.right:
                    return '(%s %s)' % (tree.val, print_tree(tree.left))
                else:
                    return '(%s %s %s)' % (print_tree(tree.left), tree.val, print_tree(tree.right))

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