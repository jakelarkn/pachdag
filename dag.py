from collections import defaultdict


class DAGError(RuntimeError):
    pass


class DAGInputError(DAGError):
    pass

class DAG:

    def __init__(self, text):
        self.graph = {}
        self.in_degree = defaultdict(int)
        self.out_degree = defaultdict(int)
        self._parse(text)

    # parse and validate the input text
    def _parse(self, text: str):
        text = text.strip()
        if text == "":
            raise DAGInputError("text graph input was empty")

        lines = text.split("\n")

        if not lines:
            raise DAGInputError("insert empty graph text definition")

        self.graph = {}
        self.in_degree = defaultdict(int)    # edges directed from descendants
        self.out_degree = defaultdict(int)   # edges directed to ancestors
        for line in lines:
            line_split = line.split(":")
            if len(line_split) != 2:
                raise DAGInputError("invalid input definition of line " + line)
            node_str = line_split[0].strip()

            if node_str in self.graph:
                raise DAGInputError("node is defined more than once")

            self.graph[node_str] = []
            self.in_degree[node_str] = 0
            self.out_degree[node_str] = 0

            parents_str = line_split[1].strip()
            parent_arr = parents_str.split(",")

            for parent_str in parent_arr:
                if parent_str == "":     # artifact of the behavior split   "A:\n"  will split to ["A",""]
                    continue

                parent_str = parent_str.strip()

                self.in_degree[parent_str] += 1
                self.out_degree[node_str] += 1
                if parent_str not in self.graph:
                    raise DAGInputError("node parent has not been declared")

                self.graph[node_str].append(parent_str)

    def leaves(self):
        leaves_arr = []
        for node in self.in_degree:
            if self.in_degree[node] == 0:
                leaves_arr.append(node)
        return leaves_arr

    #  by convention in my code any function starting with an underscore _ is meant to be private method
    def _roots(self) -> list[str]:
        roots_arr = []
        for node in self.out_degree:
            if self.out_degree[node] == 0:
                roots_arr.append(node)
        return roots_arr

    def _ancestors_dfs_helper(self, result, node):
        for ancestor in self.graph[node]:
            result.append(ancestor)
            self._ancestors_dfs_helper(result, ancestor)

    def ancestors(self, node) -> list[str]:
        if node not in self.graph:
            raise DAGError("node for ancestor request is not in graph")

        # all ancestors of node
        result = [node]

        # node is a root so we are done
        if self.out_degree[node] == 0:
            return result

        self._ancestors_dfs_helper(result, node)
        return result

    def bisectors(self) -> list[str]:
        num_nodes = len(self.graph)
        top_sort = self._top_sort()
        num_ancestors = {}
        for node in self._roots():
            num_ancestors[node] = 1

        for node in top_sort:
            num_ancestors[node] = len(self.graph[node]) + 1
            for anc_node in self.graph[node]:
                num_ancestors[node] += (num_ancestors[anc_node] - 1)

        maxmin_value = 0
        maxmin_nodes = []

        mm = {}

        for node in num_ancestors:
            cur_value =  min(num_ancestors[node], num_nodes - num_ancestors[node])
            mm[node] = cur_value
            if cur_value > maxmin_value:
                maxmin_value = cur_value
                maxmin_nodes = [node]
            elif cur_value == maxmin_value:
                maxmin_nodes.append(node)
        return maxmin_nodes

    #  return an array of nodes that is a topological sort of the graph
    #  algorithm time complext O(V+E)  number of nodes + number of edges
    def _top_sort(self):
        num_nodes = len(self.graph)
        visited = {}
        for node in self.graph:
            visited[node] = 0

        order = []

        for node in self.graph:
            if not self._top_sort_dfs(node, visited, order):
                return []

        return order

    # dfs helper function for topological sort
    def _top_sort_dfs(self, cur, visited, order):
        if visited[cur] == -1:
            return False
        if visited[cur] == 1:
            return True

        visited[cur] = -1
        for nxt in self.graph[cur]:

            if not self._top_sort_dfs(nxt, visited, order):
                return False

        order.append(cur)
        visited[cur] = 1
        return True







