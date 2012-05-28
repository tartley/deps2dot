import sys

from pydot import Cluster, Dot, Edge, Node

from .options import get_parser, parse_args


def read_file(filename):
    with open(filename) as filepointer:
        return [eval(line) for line in filepointer]


def get_node(graph, name_parts):
    '''
    Given a tree if nested dictionaries, returns the node specified by
    'name_parts', a list of keys, e.g.
        get_node({'a': {'b': {'c':0}}}, ['a', 'b'])
    returns {'c':0}
    '''
    if name_parts:
        return get_node(graph[name_parts[0]], name_parts[1:])
    else:
        return graph

def is_node(end_root, end_name):
    return end_root == end_name == None

def is_module(start_name):
    return start_name.endswith('.py')

def get_tree(deps):
    '''
    Converts the given iterable of dependencies into a tree of nested
    dictionaries, keyed by start_name, values are strings for modules,
    dictionaries for packages.
    '''
    root = {}
    for (start_root, start_name), (end_root, end_name) in deps:
        name_parts = start_name.split('/')
        short_name = name_parts[-1]
        parent = get_node(root, name_parts[:-1])
        if is_node(end_root, end_name):
            if is_module(start_name):
                parent[short_name] = None
            else:
                parent[short_name] = {}
    return root


def add_nodes(graph, tree, prefix=''):
    for key, value in tree.items():
        long_name = prefix + '/' + key if prefix else key
        if value is None:
            graph.add_node(Node(long_name, label=key))
        else:
            cluster = Cluster(
                '"%s"' % (long_name,),
                label=key,
            )
            # pydot.Cluster has a bug. Workaround by putting the 'cluster_'
            # prefix on the inside of the quotes
            cluster.obj_dict['name'] = '"cluster_%s"' % (long_name,)
            add_nodes(
                cluster,
                value,
                prefix=long_name
            )
            graph.add_subgraph(cluster)
    return graph


def main():
    # setup.py install/develop creates an executable that calls this function
    options = parse_args(get_parser(), sys.argv[1:])
    deps = list(read_file(options.input))
    graph = Dot("Dependencies", graph_type='digraph')
    graph = add_nodes(graph, get_tree(deps))
    print(graph.to_string())

