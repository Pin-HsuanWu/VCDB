from globals import vc_cursor
import networkx as nx
import matplotlib.pyplot as plt

def graph():
    vc_cursor.execute("SELECT bid, tail FROM branch")
    branch_rows = vc_cursor.fetchall()

    dag = {}  # Dictionary to store the DAG relationships
    for branch_row in branch_rows:
        bid, tail = branch_row
        vc_cursor.execute(f"SELECT version, last_version FROM commit WHERE bid = {bid} AND version = '{tail}'")
        commit_row = vc_cursor.fetchone()
        if commit_row:
            version, last_version = commit_row
            dag[tail] = last_version

    G = nx.DiGraph(dag)
    pos = nx.spring_layout(G)  # Determine node positions
    nx.draw_networkx_nodes(G, pos, node_size=2000)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    plt.show()

if __name__ == '__main__':
    graph()
