from globals import vc_cursor
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

"""
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

def get_tail_by_bid(bid):
    query = f"SELECT tail FROM branch WHERE bid = {bid}"
    vc_cursor.execute(query)
    result = vc_cursor.fetchone()
    if result:
        return result[0]
    return None

def get_commits_by_bid(bid):
    query = f"SELECT version, last_version FROM commit WHERE bid = {bid}"
    vc_cursor.execute(query)
    return vc_cursor.fetchall()

def create_git_graph(commits):
    G = nx.DiGraph()

    while commits:
        version = commits.pop()
        G.add_node(version)

        query = f"SELECT last_version FROM commit WHERE version = '{version}'"
        vc_cursor.execute(query)
        result = vc_cursor.fetchone()

        if result:
            last_version = result[0]
            if last_version:
                G.add_edge(last_version, version)
                commits.append(last_version)

    return G

def draw_git_graph(bid):
    tail = get_tail_by_bid(bid)
    if not tail:
        print("Branch not found.")
        return

    commits = get_commits_by_bid(bid)
    print(commits)
    if not commits:
        print("No commits found for the branch.")
        return

    G = create_git_graph(commits)

    # pos = nx.spring_layout(G, seed=42)
    # fig, ax = plt.subplots(figsize=(10, 6))
    # nx.draw(G, pos, ax=ax, with_labels=True, node_size=500, node_color='skyblue', font_size=8, edge_color='gray')
    # plt.title("Git Graph")
    # plt.tight_layout()

    # root = tk.Tk()
    # canvas = FigureCanvasTkAgg(fig, master=root)
    # canvas.draw()
    # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # tk.mainloop()
"""

def get_tail_by_bid(bid):
    query = f"SELECT tail FROM branch WHERE bid = {bid}"
    vc_cursor.execute(query)
    result = vc_cursor.fetchone()
    if result:
        return result[0]
    return None


def get_commits_by_bid(bid):
    print(f'bid: {bid}')
    query = f"SELECT version, last_version, time, bid FROM commit WHERE bid = {bid}"
    vc_cursor.execute(query)
    commits = vc_cursor.fetchall()
    print(commits)
    return 

def sort_commit(tail, commit_dict):
    sorted_commit_list = []
    current_version = tail
    # sorted_commit_list.append(tail)
    while current_version:
        if current_version in commit_dict.keys():
            last_version = commit_dict[current_version]
            sorted_commit_list.append((current_version, commit_dict[current_version]))
            current_version = last_version
        else:
            break


    return sorted_commit_list

# def draw_branch_graph(bid, graph):
#     tail = get_tail_by_bid(bid)
#     tail = '892e87c4'
#     commit_list = get_commits_by_bid(bid)
#     commit_dict = {commit[0]: commit[1] for commit in commit_list}

#     commit_dict = {'892e87c4': 'b658fa8d', 'a534e40e': None, '6e2d91cc': '57a37594', '07d4ddd9': 'a534e40e', '57a37594': '07d4ddd9', 'b658fa8d': '6e2d91cc'}
#     print(f'commit_list: {commit_dict}')

#     sorted_commit_list = sort_commit(tail, commit_dict)
#     print(f'sorted_commit_list: {sorted_commit_list}')

#     for commit in sorted_commit_list:
#         # print(commit.get)
#         graph.add_node(commit[0], subset=bid)
#         if commit[1]:
#             graph.add_edge(commit[0], commit[1])

#     return graph

def draw_branch_graph(branch_info, graph):
    # Get bid and tail from branch_info
    bid = branch_info[0]
    tail = branch_info[2]

    # Get sorted commit list from bid
    commit_list = get_commits_by_bid(bid)
    # commit_dict = {commit[0]: commit[1] for commit in commit_list}

    # commit_dict = {'2567554e': '73961160', '73961160': 'b658fa8d'}
    # print(f'commit_list: {commit_dict}')

    # sorted_commit_list = sort_commit(tail, commit_dict)
    # print(f'sorted_commit_list: {sorted_commit_list}')

    # for commit in sorted_commit_list:
    #     # print(commit.get)
    #     graph.add_node(commit[0], subset=bid)
    #     if commit[1]:
    #         graph.add_edge(commit[0], commit[1])

    return graph

def draw_git_graph():
    # Get all branch
    query = "SELECT * FROM branch"
    vc_cursor.execute(query)
    branch_list = vc_cursor.fetchall()
    print(branch_list)

    # Create a directed graph
    graph = nx.DiGraph()

    # Create graph for all branches
    for branch_info in branch_list:
        graph=draw_branch_graph(branch_info, graph)
"""
    bid_list = [1, 2]
     
    # Create a directed graph
    graph = nx.DiGraph()
    
    graph=draw_branch_graph(bid_list[0], graph)
    graph=draw_branch_graph_2(bid_list[1], graph)
   
    # Add nodes and edges based on the data
    # for bid, name, tail in branch_data:
    #     graph.add_node(bid, name=name, tail=tail, subset='branch')

    # for version, bid, last_version, time, uid, msg in commit_data:
    #     graph.add_node(version, bid=bid, last_version=last_version, time=time, uid=uid, msg=msg, subset='commit')
    #     if last_version is not None:
    #         graph.add_edge(last_version, version)

    # for merged_version, main_branch_version, target_branch_version in merge_data:
    #     graph.add_edge(main_branch_version, merged_version)
    #     graph.add_edge(target_branch_version, merged_version)

    # Generate the graph layout
    pos = nx.multipartite_layout(graph, subset_key='subset')

    # Draw the nodes
    nx.draw_networkx_nodes(graph, pos, node_color='lightblue', alpha=0.7)

    # Draw the edges
    # edge_colors = []
    # for edge in graph.edges():
    #     if edge[0] in branch_data and edge[1] in branch_data:
    #         edge_colors.append('orange')  # Edge between branches
    #     else:
    #         edge_colors.append('gray')  # Edge within the same branch
    nx.draw_networkx_edges(graph, pos)

    # Draw the labels
    nx.draw_networkx_labels(graph, pos, font_color='black', font_size=10)

    # Set the plot title
    plt.title('Version Control Graph')

    # Show the graph
    plt.axis('off')
    plt.show()
    """


if __name__ == '__main__':
    # Example usage
    draw_git_graph()
