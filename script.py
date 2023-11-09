import matplotlib.pyplot as plt
import networkx as nx
import uuid

level = 0


def merge_sort_trace(arr, G, pos, level, parent_id, offset=(0, 0)):
    n = len(arr)
    node_id = str(uuid.uuid4())
    G.add_node(node_id, array=arr, level=level)
    pos[node_id] = (offset[0], level)

    if parent_id is not None:
        G.add_edge(parent_id, node_id)
    if n > 1:
        mid = n // 2
        left_id, left_child, left_level = merge_sort_trace(
            arr[:mid], G, pos, level + 1, node_id, (offset[0] - 1/2**level, level+1))
        right_id, right_child, right_level = merge_sort_trace(
            arr[mid:], G, pos, level + 1, node_id, (offset[0] + 1/2**level, level+1))

        merged_array = merge(left_child, right_child)
        merged_id = str(uuid.uuid4())
        G.add_node(merged_id, array=merged_array, level=left_level)
        pos[merged_id] = (
            offset[0], (count_divisions_to_one(len(arr))/(count_divisions_to_one(len(arr)))/5)+left_level+1)

        G.add_edge(left_id, merged_id)
        G.add_edge(right_id, merged_id)

        return merged_id, merged_array, right_level+1
    else:
        return node_id, arr, level


def count_divisions_to_one(number):
    count = 0
    while number >= 1:
        number /= 2
        count += 1
    return count


def normalize_y_positions(pos):
    # Find the min and max y-values
    min_y = min(pos.values(), key=lambda x: x[1])[1]
    max_y = max(pos.values(), key=lambda x: x[1])[1]

    # Normalize y-values to have a maximum difference of 1
    for key in pos:
        normalized_y = (pos[key][1] - min_y) / (max_y - min_y)
        pos[key] = (pos[key][0], normalized_y)
    return pos


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def draw_tree(G, pos):
    # Normalize y positions before drawing
    pos = normalize_y_positions(pos)

    labels = {n: G.nodes[n]['array'] for n in G.nodes}
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=3000,
            node_color='skyblue', font_size=10, font_weight='bold', arrows=False)
    plt.gca().invert_yaxis()
    plt.show()


G = nx.DiGraph()
pos = {}
arr = [8, 3, 2, 9, 7, 1, 5, 4]
merge_sort_trace(arr, G, pos, 0, None)
draw_tree(G, pos)
