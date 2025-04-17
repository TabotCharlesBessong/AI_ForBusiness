import networkx as nx
import plotly.graph_objects as go

class GraphVisualization:
    def __init__(self, graph, pos):
        self.graph = graph
        self.pos = pos

    def create_figure(self, height=600, width=600, showlabel=True):
        edge_x = []
        edge_y = []

        # Extract coordinates for edges
        for edge in self.graph.edges():
            x0, y0 = self.pos[edge[0]]
            x1, y1 = self.pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines'
        )

        node_x = []
        node_y = []
        text = []

        for node in self.graph.nodes():
            x, y = self.pos[node]
            node_x.append(x)
            node_y.append(y)
            text.append(str(node))

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text' if showlabel else 'markers',
            text=text if showlabel else None,
            hoverinfo='text',
            marker=dict(
                showscale=False,
                color='skyblue',
                size=10,
                line=dict(width=2)
            )
        )

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='Network Graph',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            xaxis=dict(showgrid=False, zeroline=False),
                            yaxis=dict(showgrid=False, zeroline=False),
                            height=height,
                            width=width
                        ))

        return fig
