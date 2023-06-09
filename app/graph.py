import globals
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def get_commits_by_bid(bid):
    query = f"SELECT version, last_version, time FROM commit WHERE bid = {bid}"
    globals.vc_cursor.execute(query)
    commits = globals.vc_cursor.fetchall()
    sorted_commit_list = sorted(commits, key=lambda x: x[2], reverse=True)
    sorted_commit_list = [(x[0], x[1]) for x in sorted_commit_list]
    return sorted_commit_list

# def sort_commit(tail, commit_dict):
#     sorted_commit_list = []
#     current_version = tail
#     # sorted_commit_list.append(tail)
#     while current_version:
#         if current_version in commit_dict.keys():
#             last_version = commit_dict[current_version]
#             sorted_commit_list.append((current_version, commit_dict[current_version]))
#             current_version = last_version
#         else:
#             break



def draw_branch_graph(branch_info, graph, all_commit_list):
    # Get bid and tail from branch_info
    bid = branch_info[0]
    branch_name = branch_info[1]

    # Get sorted commit list from bid
    sorted_commit_list = get_commits_by_bid(bid)

    for commit in sorted_commit_list:
        # print(commit.get)
        graph.add_node(commit[0], subset=branch_name, pos=(bid, all_commit_list.index(commit[0])*2))
        if commit[1]:
            graph.add_edge(commit[0], commit[1])

    return graph

def draw_git_graph():
    # Get all branch
    query = "SELECT * FROM branch"
    globals.vc_cursor.execute(query)
    branch_list = globals.vc_cursor.fetchall()

    # Get all commit
    query = "SELECT version FROM commit ORDER BY time"
    globals.vc_cursor.execute(query)
    all_commit_list = globals.vc_cursor.fetchall()
    all_commit_list = [x[0] for x in all_commit_list]

    # Create a directed graph
    graph = nx.DiGraph()

    # Create graph for all branches
    for branch_info in branch_list:
        graph=draw_branch_graph(branch_info, graph, all_commit_list)

    # Get merge info
    query = "SELECT * FROM merge"
    globals.vc_cursor.execute(query)
    merge_list = globals.vc_cursor.fetchall()
    for merge in merge_list:
        graph.add_edge(merge[0], merge[2])

    # Get unique subsets from the graph
    subsets = set(nx.get_node_attributes(graph, 'subset').values())

    # Generate a unique color for each subset
    subset_colors = {}
    for i, subset in enumerate(subsets):
        subset_colors[subset] = f'C{i}'

    # Get the subset attribute for each node and assign the corresponding color
    node_colors = [subset_colors[graph.nodes[node]['subset']] for node in graph.nodes]

    # Draw Graph
    pos = nx.get_node_attributes(graph,'pos')

    # Draw the nodes
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, alpha=0.7)
    nx.draw_networkx_edges(graph, pos)

    # Draw the labels
    nx.draw_networkx_labels(graph, pos, font_color='black', font_size=10)
    
    # Set the plot title
    plt.title('Version Control Graph')

    # Create a legend for subsets and their colors
    legend_handles = []
    for subset, color in subset_colors.items():
        legend_handles.append(plt.Line2D([], [], marker='o', markersize=10, color=color, label=subset))
    plt.legend(handles=legend_handles)

    # Show the graph
    plt.axis('off')
    plt.show()



if __name__ == '__main__':
    # Example usage
    draw_git_graph()
