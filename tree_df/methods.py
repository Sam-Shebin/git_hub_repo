import pandas as pd
import skbio
from skbio import TreeNode

def treenode_to_dataframe(tree_node):
    rows_for_dataframe = []
    tree_node.assign_ids()
    for node in tree_node.traverse(include_self=True):
        '''
        if node.parent == None:
            parent_id = -1
        else:
            parent_id = node.parent

        node_id = node.id
        node_name = node.name
        node_length = node.length

        rows_for_dataframe.append({'parent':parent_id,'node':node_id,'name':node_name,'length':node_length})
        '''
        # if node.nazme == 'None':

        rows_for_dataframe.append(
            {'parent': node.parent.id if node.parent is not None else -1, "node": node.id, 'name': node.name,
             'length': node.length})
        # add in name of the node and edge length of the node
    df = pd.DataFrame(rows_for_dataframe)
    return df


def dataframe_to_treenode(dataframe):
    # if 'node' not in dataframe.columns:
    # df[column_name] = default_value
    root_id = dataframe.loc[dataframe["parent"] == -1, "node"].values[0]
    root_name = dataframe.loc[dataframe["parent"] == -1, "name"].values[0]

    root = TreeNode(name=root_name) if root_name != 'None' else TreeNode()
    root.id = root_id
    dictionary_1 = {root.id: root}

    list_1 = dataframe['parent'].unique()
    list_2 = []

    for x in list_1:
        if x == -1:
            continue
        else:
            l2 = dataframe.loc[dataframe.parent == x, ['parent', 'node', 'name', 'length']].values.tolist()
            for y in l2:
                if y[2] != 'None':  # name does not equal None
                    node_name = y[2]
                    if pd.isna(y[3]):  # if length does not equal Nan
                        node = TreeNode(name=node_name)
                        node.id = y[1]
                        dictionary_1[node.id] = node
                        # print(dictionary_1[y[0]])
                        dictionary_1[y[0]].append(node)
                    else:
                        node_length = float(y[3])
                        node = TreeNode(name=node_name, length=node_length)
                        node.id = y[1]
                        dictionary_1[node.id] = node
                        # print(dictionary_1[y[0]])
                        dictionary_1[y[0]].append(node)
                else:  # if name = None
                    if pd.isna(y[3]):  # if length = Nan
                        node = TreeNode()
                        node.id = y[1]
                        dictionary_1[node.id] = node
                        # print(dictionary_1[y[0]])
                        dictionary_1[y[0]].append(node)
                    else:  # if length does not equal Nan
                        node_length = float(y[3])
                        node = TreeNode(length=node_length)
                        node.id = y[1]
                        dictionary_1[node.id] = node
                        # print(dictionary_1[y[0]])
                        dictionary_1[y[0]].append(node)

    return root