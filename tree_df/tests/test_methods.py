import skbio
from skbio import TreeNode
from unittest import TestCase
from tree_df.methods import treenode_to_dataframe,dataframe_to_treenode
import pandas as pd

import cProfile
import re

class unit_test_dataframe_to_treenode_85_otsu_tree(TestCase):

    def setUp(self):
        node_a = TreeNode('a')
        node_b = TreeNode('b')
        node_c = TreeNode('c')
        node_d = TreeNode('d')
        node_e = TreeNode('e')
        node_a.append(node_b)
        node_b.append(node_c)
        node_b.append(node_d)
        node_a.append(node_e)
        self.TreeRoot = node_a
        #
        #          /c
        #          |
        #      /b--|
        #      |   |
        # --a---|   \d
        #      |
        #      \e

        list_df = [{'parent': -1, 'node': 1, 'name': 'a', 'length': None},
                   {'parent': 1, 'node': 2, 'name': 'b', 'length': None},
                   {'parent': 2, 'node': 3, 'name': 'c', 'length': None},
                   {'parent': 2, 'node': 4, 'name': 'd', 'length': None},
                   {'parent': 1, 'node': 5, 'name': 'e', 'length': None}
                   ]

        self.expected_tree = skbio.TreeNode.read('../../85_otus.tree', format='newick')
        observed_tree = treenode_to_dataframe(self.expected_tree)
        self.observed_tree = dataframe_to_treenode(observed_tree)

    def test_count_tips(self):
        real_tree_tips = self.expected_tree.count(tips=True)
        test_tree_tips = self.observed_tree.count(tips=True)
        self.assertEqual(test_tree_tips, real_tree_tips)

    def test_root(self):
        real_root = self.expected_tree.root().name
        test_tree_root = self.observed_tree.root().name
        self.assertEqual(test_tree_root, real_root)

    def test_tip(self):
        real_tips = {n.name for n in self.expected_tree.tips()}
        # test_tree_tips = list(self.test_tree.tips())
        est_tree_tips = {n.name for n in self.observed_tree.tips()}
        self.assertEqual(real_tips, est_tree_tips)

        # print(self.test_tree.ascii_art())

    def test_rfd(self):
        # self.expected_tree.assign_ids()
        # print(type(self.expected_tree))
        self.assertEqual(self.expected_tree.compare_rfd(self.observed_tree), 0.0)
        # print(self.expected_tree)

    def test_tip_distance(self):
        self.expected_tree.assign_ids()
        self.assertEqual(self.expected_tree.compare_tip_distances(self.observed_tree, sample=1000), 0.0)

    def test_paths(self):
        observed_tips = {tip.name for tip in self.observed_tree.tips()}
        # expeted_tips = {expeted_tips for expeted_tips in self.expected_tree.tips()}
        # observed_tips = {observed_tips for observed_tips in self.observed_tree.tips()}
        expected_tips = {tip.name for tip in self.expected_tree.tips()}
        if expected_tips != observed_tips:
            self.assertEqual(0, 1)
        for exp_tips in expected_tips:
            e_tips = self.expected_tree.find(exp_tips)
            o_tips = self.observed_tree.find(exp_tips)
            ancestor_exp = [node.name for node in e_tips.ancestors()]
            ancestor_obs = [node.name for node in o_tips.ancestors()]
            if ancestor_exp != ancestor_obs:
                self.assertEqual(0, 1)
        self.assertEqual(1, 1)

class unit_test_dataframe_to_treenode_simple_tree(TestCase):
    def setUp(self):
        node_a = TreeNode('a')
        node_b = TreeNode(name = 'b',length =2)
        node_c = TreeNode('c')
        node_d = TreeNode(name = 'd',length =1 )
        node_e = TreeNode('e')
        node_a.append(node_b)
        node_b.append(node_c)
        node_b.append(node_d)
        node_a.append(node_e)
        self.TreeRoot = node_a
        #
        #          /c
        #          |
        #      /b--|
        #      |   |
        # --a---|   \d
        #      |
        #      \e

        list_df = [{'parent': -1, 'node': 1, 'name': 'a', 'length': None},
                   {'parent': 1, 'node': 2, 'name': 'b', 'length': 2},
                   {'parent': 2, 'node': 3, 'name': 'c', 'length': None},
                   {'parent': 2, 'node': 4, 'name': 'd', 'length': 1},
                   {'parent': 1, 'node': 5, 'name': 'e', 'length': None}
                   ]
        observed_tree = pd.DataFrame(list_df)
        self.observed_tree = dataframe_to_treenode(observed_tree)

    def test_count_tips(self):
        real_tree_tips = self.TreeRoot.count(tips=True)
        test_tree_tips = self.observed_tree.count(tips=True)
        self.assertEqual(test_tree_tips, real_tree_tips)

    def test_root(self):
        real_root = self.TreeRoot.root().name
        test_tree_root = self.observed_tree.root().name
        self.assertEqual(test_tree_root, real_root)

    def test_tip(self):
        real_tips = {n.name for n in self.TreeRoot.tips()}
        # test_tree_tips = list(self.test_tree.tips())
        est_tree_tips = {n.name for n in self.observed_tree.tips()}
        self.assertEqual(real_tips, est_tree_tips)

        # print(self.test_tree.ascii_art())

    def test_rfd(self):
        # self.expected_tree.assign_ids()
        # print(type(self.expected_tree))
        self.assertEqual(self.TreeRoot.compare_rfd(self.observed_tree), 0.0)
        # print(self.expected_tree)

    def test_tip_distance(self):
        self.TreeRoot.assign_ids()
        self.assertEqual(self.TreeRoot.compare_tip_distances(self.observed_tree), 0.0) # comes out nan if no length is provided

    def test_paths(self):
        observed_tips = {tip.name for tip in self.observed_tree.tips()}
        # expeted_tips = {expeted_tips for expeted_tips in self.expected_tree.tips()}
        # observed_tips = {observed_tips for observed_tips in self.observed_tree.tips()}
        expected_tips = {tip.name for tip in self.TreeRoot.tips()}
        if expected_tips != observed_tips:
            self.assertEqual(0, 1)
        for exp_tips in expected_tips:
            e_tips = self.TreeRoot.find(exp_tips)
            o_tips = self.observed_tree.find(exp_tips)
            ancestor_exp = [node.name for node in e_tips.ancestors()]
            ancestor_obs = [node.name for node in o_tips.ancestors()]
            if ancestor_exp != ancestor_obs:
                self.assertEqual(0, 1)
        self.assertEqual(1, 1)



class unit_test_treenode_to_dataframe(TestCase):

    def setUp(self):
        node_a = TreeNode('a')
        self.test_tree = node_a
        node_b = TreeNode('b')
        node_c = TreeNode('c')
        node_d = TreeNode('d')
        node_e = TreeNode('e')
        node_a.append(node_b)
        node_b.append(node_c)
        node_b.append(node_d)
        node_a.append(node_e)
        self.TreeRoot = node_a
        #
        #          /c
        #          |
        #      /b--|
        #      |   |
        # --a---|   \d
        #      |
        #      \e

        node_a.assign_ids()
        self.data_frame = treenode_to_dataframe(node_a)

        self.parent_list = []
        self.node_list = []
        for node in node_a.traverse(include_self=True):
            self.parent_list.append(node.parent.id if node.parent is not None else -1)
            self.node_list.append(node.id)

    def test_parent(self):
        test_parent_list = [x for x in self.data_frame['parent']]
        self.assertEqual(test_parent_list, self.parent_list)

    def test_node(self):
        test_node_list = [y for y in self.data_frame['node']]
        self.assertEqual(self.node_list, test_node_list)

    def test_parent_size(self):
        parent_len = len(self.data_frame['parent'])
        self.assertEqual(parent_len, 5)

    def test_node_size(self):
        node_len = len(self.data_frame['node'])
        self.assertEqual(node_len, 5)