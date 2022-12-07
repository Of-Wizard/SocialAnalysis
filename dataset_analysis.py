import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


def dataset_to_graph(data_path):
    """
    读取txt文件生成节点关注列表
    :param data_path
    :return:
    """
    with open(data_path, "r") as f:
        data = f.readlines()
    print('原始数据长度：%d ' % len(data))
    edges_list = []
    for line in data:
        follow_edge = line.split()
        follow_edge = np.array(follow_edge).astype('int')
        edges_list.append(tuple(follow_edge))
    return edges_list


def graph_analysis(G, graphml_flag=False, png_flag=False):
    """
    根据输入的图进行分析
    :param G:
    :param png_flag:
    :param graphml_flag:
    :return:
    """
    if graphml_flag:
        nx.write_graphml(G, "follow_relationships.graphml")
    # 获取图的基本属性： 节点数、边数、图的密度
    node_num = G.number_of_nodes()
    edge_num = G.number_of_edges()
    graph_density = nx.density(G)
    if png_flag:
        nx.draw(G, "follow_relationships.png")
    print('节点数：%d' % node_num)
    print('边数：%d' % edge_num)
    print('图的密度：%f' % graph_density)
    # 计算图的传递性
    transitivity = nx.transitivity(G)
    print('图的传递性：%f' % transitivity)
    # # 计算强连通子图和弱连通子图
    # largest_scc = max(nx.strongly_connected_components(G), key=len)
    # largest_wcc = max(nx.weakly_connected_components(G), key=len)
    # print('最大的强连通子图节点个数：%d' % len(largest_scc))
    # G_scc = nx.subgraph(G, largest_scc)
    # print('最大的强连通子图边数：%d 比例是： %f' % (nx.number_of_edges(G_scc), nx.number_of_edges(G_scc) / edge_num))
    # print('最大的弱连通子图节点个数：%d ' % len(largest_wcc))
    # G_wcc = nx.subgraph(G, largest_wcc)
    # print('最大的弱连通子图边数：%d 比例是：%f' % (nx.number_of_edges(G_wcc), nx.number_of_edges(G_wcc) / edge_num))

    in_degree_top_nodes = sorted(G.in_degree(), key=lambda x: x[1], reverse=True)
    print('top10被关注人数最多的节点：')
    for i in range(10):
        print(in_degree_top_nodes[i])

    degree_sum = sum([d for n, d in G.degree()])
    print('平均度数：%f' % (degree_sum / node_num))
    degree_sum = sum([d for n, d in G.out_degree()])
    print('平均关注数：%f' % (degree_sum / node_num))
    degree_sum = sum([d for n, d in G.in_degree()])
    print('平均被关注数：%f' % (degree_sum / node_num))
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签SimHei
    fig, ax = plt.subplots()
    x_axis = [x[0] for x in G.in_degree()]
    y_axis = sorted([x[1] for x in G.in_degree()])
    ax.scatter(x_axis, y_axis)  # 画散点图
    ax.set_xlabel('节点编号')
    ax.set_ylabel('被关注人数')
    plt.savefig('dataset_analysis.png')
    plt.show()


edges = dataset_to_graph('./dataset.txt')
G = nx.DiGraph()
G.add_edges_from(edges)
graph_analysis(G, graphml_flag=True)
# from pagerank import pagerank
nx.leaderrank
# result = pagerank(G)
# result = sorted(result.items(), key=lambda x: x[1], reverse=True)
