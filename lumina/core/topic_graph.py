from collections import deque

def build_topic_graph(dataset):
    """
    Automatically builds a simple topic graph from dataset topics.
    """
    topic_graph = {}
    for entry in dataset:
        topic = entry["topic"]
        intent = entry["intent"]
        if topic not in topic_graph:
            topic_graph[topic] = []
        topic_graph[topic].append(intent)
    return topic_graph


class SearchNavigationModule:
    """
    Handles academic topic exploration using BFS and DFS traversals.
    """
    def __init__(self, topic_graph):
        self.topic_graph = topic_graph

    def bfs_traverse(self, start_topic):
        visited = []
        queue = deque([start_topic])
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.append(node)
                queue.extend(self.topic_graph.get(node, []))
        return visited

    def dfs_traverse(self, start_topic):
        visited = []
        def dfs(node):
            if node not in visited:
                visited.append(node)
                for neighbor in self.topic_graph.get(node, []):
                    dfs(neighbor)
        dfs(start_topic)
        return visited

    def get_related_topics(self, topic, method="bfs"):
        if topic not in self.topic_graph:
            return ["Topic not found in knowledge graph."]
        if method == "dfs":
            return self.dfs_traverse(topic)
        return self.bfs_traverse(topic)
