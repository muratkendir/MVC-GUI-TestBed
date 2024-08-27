import networkx

def compose_graphs(a, b):
    a_r = networkx.read_gexf(a, relabel=True)
    b_r = networkx.read_gexf(b, relabel=True)
    composed = networkx.compose(a_r,b_r)
    file_name = 'composed.gexf'
    networkx.write_gexf(composed, file_name)
    print(f'The graph saved as < {file_name} > !')
    return composed
