import networkx as nx
import plotly.graph_objects as go

def visualize(network, path, start_node, end_node):
    # Create a directed graph
    G = nx.DiGraph(network)
    # Use automatic layout
    pos = nx.spring_layout(G)

    # Extract node coordinates from the layout
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]

    # Create edges
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    # Create nodes
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        text=list(G.nodes()),
        mode='markers+text',  
        hoverinfo='text',
        marker=dict(
            showscale=True,
            color="purple",
            size=20,  

        ),
        textfont=dict(size=10), 
        fillcolor="white"
    )

    # Highlight path
    path_edges_x = []
    path_edges_y = []

    for i in range(len(path) - 1):
        source_node = path[i]
        target_node = path[i + 1]
        x0, y0 = pos[source_node]
        x1, y1 = pos[target_node]
        path_edges_x += [x0, x1, None]
        path_edges_y += [y0, y1, None]


    path_trace = go.Scatter(
        x=path_edges_x,
        y=path_edges_y,
        line=dict(width=1, color='orange'),  
        hoverinfo='none',
        mode='lines'
    )

    # Highlight the start and end nodes
    start_end_trace = go.Scatter(
        x=[pos[start_node][0], pos[end_node][0]],
        y=[pos[start_node][1], pos[end_node][1]],
        mode='markers',
        marker=dict(
            color='orange',
            size=20,
            line=dict(color='black', width=2)
        ),
        text=[start_node, end_node],
        hoverinfo='text'
    )

    fig = go.Figure(data=[edge_trace, path_trace, node_trace, start_end_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    ))

    fig.show()