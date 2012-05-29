import sys

from pydot import Cluster, Dot, Edge, Node

from .options import get_parser, parse_args


def read_file(filename):
    with open(filename) as filepointer:
        return [eval(line) for line in filepointer]


def get_tree_node(graph, name_parts):
    '''
    Given a tree if nested dictionaries, returns the node specified by
    'name_parts', a list of keys, e.g.
        get_tree_node({'a': {'b': {'c':0}}}, ['a', 'b'])
    returns {'c':0}
    '''
    if name_parts:
        return get_tree_node(graph[name_parts[0]], name_parts[1:])
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
        parent = get_tree_node(root, name_parts[:-1])
        if is_node(end_root, end_name):
            if is_module(start_name):
                parent[short_name] = None
            else:
                parent[short_name] = {}
    return root


def get_module_node(long_name, short_name):
     '''
     Return a Node representing the a module
     '''
     return Node(
        long_name,
        label=short_name,
        shape="box",
        style="filled",
        color="gold1",
        fontname='Arial',
        fontsize=16,
    )

def get_package_cluster(long_name, short_name, rank):
    '''
    Return a cluster representing a package
    '''
    cluster = Cluster(
        '"%s"' % (long_name,),
        label='""',
        style="filled",
        fontname='Arial',
        fontsize=20,
        color="grey75" if rank % 2 else "white",
    )
    # Workaround a bug in pydot.Cluster: Put the 'cluster_' prefix inside the
    # quotes around the name
    cluster.obj_dict['name'] = '"cluster_%s"' % (long_name,)

    # Add a node within the cluster to act both as a cluster label
    # and as an endpoint for edges which connect to the cluster
    cluster.add_node(get_package_node(long_name, short_name, rank))

    return cluster

def get_package_node(long_name, short_name, rank):
    '''
    Return a node which represents a package.
    
    This node acts as an endpoint for edges connecting to a package. This
    sidesteps the complications (and bugs?) in dot when connecting nodes
    to subgraphs. Using a package node within each package cluster, we only
    need edges to connect nodes to other nodes.
    
    This node also acts as a label for the containing cluster, so that
    edges connect to the package name, rather than to an invisible node within
    the package's cluster.
    '''
    return Node(
        long_name,
        label=short_name,
        shape="plaintext",
        fontname='Impact',
        fontcolor="white" if rank % 2 else "grey75",
        fontsize=24,
        width=0, height=0,
    )

def add_nodes(graph, tree, prefix='', rank=0):
    '''
    Given a pydot.Dot instance, and a tree constructed by 'get_tree', we
    create Nodes in 'graph' for each module listed in the tree, in nested
    subgraphs for each package.
    '''
    for key, value in tree.items():
        long_name = prefix + '/' + key if prefix else key
        if value is None:
            graph.add_node(get_module_node(long_name, key))
        else:
            cluster = get_package_cluster(long_name, key, rank)
            add_nodes(cluster, value, prefix=long_name, rank=rank+1)
            graph.add_subgraph(cluster)

def add_edges(graph, deps):
    '''
    Given a pydot.Dot instance containing nodes for every module, nested in
    subgraphs for each package, this function adds a pydot.Edge between the
    nodes in the graph for each dependency.
    '''
    for (start_root, start_name), (end_root, end_name) in deps:
        if end_root is not None and end_name is not None:

            # Filter out one particular edge, which provokes Dot's longstanding
            # and much-dreaded "trouble in init_rank" bug.
            if (start_name, end_name) in [
                ('esperanto/middleware.py', 'esperanto/urls/api'),
            ]:
                sys.stderr.write('skipping %s %s\n' % (start_name, end_name))
                continue

            graph.add_edge(Edge(start_name, end_name))

        else:
            assert end_root is None and end_name is None
    

def main():
    # setup.py install/develop creates an executable that calls this function
    options = parse_args(get_parser(), sys.argv[1:])
    deps = list(read_file(options.input))
    graph = Dot(
        "Dependencies",
        graph_type='digraph',
        compound=True,
        remincross=True,
        rankdir='LR',
        fontname='Arial',
    )
    add_nodes(graph, get_tree(deps))
    add_edges(graph, deps)
    print(graph.to_string())

