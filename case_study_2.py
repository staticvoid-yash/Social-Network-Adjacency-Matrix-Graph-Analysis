"""
============================================================
 Case Study: Social Network using Adjacency Matrix
 Representing friendship connections among millions of users
============================================================
"""

from collections import deque
import numpy as np


class SocialNetwork:
    def __init__(self, num_users):
        """Initialize network with n users (0-indexed)."""
        self.n = num_users
        self.users = {}                 # id -> name
        # Adjacency Matrix (n x n) - 0 = no friendship, 1 = friends
        self.matrix = np.zeros((num_users, num_users), dtype=int)

    # ---------- USER MANAGEMENT ----------
    def add_user(self, uid, name):
        self.users[uid] = name

    def name(self, uid):
        return self.users.get(uid, f"User{uid}")

    # ---------- 1. ADD / REMOVE FRIENDSHIP ----------
    def add_friendship(self, u, v):
        """Undirected edge: friendship is mutual."""
        self.matrix[u][v] = 1
        self.matrix[v][u] = 1
        print(f"  ✔ {self.name(u)} ↔ {self.name(v)} are now friends")

    def remove_friendship(self, u, v):
        self.matrix[u][v] = 0
        self.matrix[v][u] = 0
        print(f"  ✘ {self.name(u)} ✗ {self.name(v)} unfriended")

    # ---------- 2. CHECK FRIENDSHIP ----------
    def are_friends(self, u, v):
        return self.matrix[u][v] == 1

    # ---------- 3. MUTUAL FRIENDS ----------
    def mutual_friends(self, u, v):
        friends = []
        for i in range(self.n):
            if self.matrix[u][i] == 1 and self.matrix[v][i] == 1:
                friends.append(self.name(i))
        return friends

    # ---------- 4. FRIEND RECOMMENDATION ----------
    def recommend_friends(self, u, top_k=5):
        """Suggest friends-of-friends, ranked by mutual count."""
        scores = {}
        for i in range(self.n):
            if i == u or self.matrix[u][i] == 1:
                continue
            mutual = 0
            for j in range(self.n):
                if self.matrix[u][j] == 1 and self.matrix[i][j] == 1:
                    mutual += 1
            if mutual > 0:
                scores[i] = mutual
        ranked = sorted(scores.items(), key=lambda x: -x[1])[:top_k]
        return [(self.name(k), v) for k, v in ranked]

    # ---------- 5. DEGREE CENTRALITY ----------
    def degree_centrality(self):
        degrees = self.matrix.sum(axis=1)
        result = [(self.name(i), int(degrees[i])) for i in range(self.n)]
        return sorted(result, key=lambda x: -x[1])

    # ---------- 6. BFS TRAVERSAL ----------
    def bfs(self, start):
        visited = [False] * self.n
        order, queue = [], deque([start])
        visited[start] = True

        while queue:
            node = queue.popleft()
            order.append(self.name(node))
            for i in range(self.n):
                if self.matrix[node][i] == 1 and not visited[i]:
                    visited[i] = True
                    queue.append(i)
        return order

    # ---------- 7. DFS TRAVERSAL ----------
    def dfs(self, start):
        visited = [False] * self.n
        order = []

        def _dfs(node):
            visited[node] = True
            order.append(self.name(node))
            for i in range(self.n):
                if self.matrix[node][i] == 1 and not visited[i]:
                    _dfs(i)

        _dfs(start)
        return order

    # ---------- 8. SHORTEST PATH (Degrees of Separation) ----------
    def shortest_path(self, src, dst):
        if src == dst:
            return [self.name(src)]

        visited = [False] * self.n
        parent = [-1] * self.n
        queue = deque([src])
        visited[src] = True

        while queue:
            node = queue.popleft()
            for i in range(self.n):
                if self.matrix[node][i] == 1 and not visited[i]:
                    visited[i] = True
                    parent[i] = node
                    if i == dst:
                        path = []
                        cur = dst
                        while cur != -1:
                            path.append(self.name(cur))
                            cur = parent[cur]
                        return path[::-1]
                    queue.append(i)
        return None    # Not connected

    # ---------- 9. CONNECTED COMPONENTS ----------
    def connected_components(self):
        visited = [False] * self.n
        components = []

        for i in range(self.n):
            if not visited[i]:
                comp = []
                queue = deque([i])
                visited[i] = True
                while queue:
                    node = queue.popleft()
                    comp.append(self.name(node))
                    for j in range(self.n):
                        if self.matrix[node][j] == 1 and not visited[j]:
                            visited[j] = True
                            queue.append(j)
                components.append(comp)
        return components

    # ---------- 10. TRIANGLE DETECTION ----------
    def count_triangles(self):
        count = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.matrix[i][j]:
                    for k in range(j + 1, self.n):
                        if self.matrix[i][k] and self.matrix[j][k]:
                            count += 1
        return count

    # ---------- 11. COMMUNITY DETECTION (Simple) ----------
    def communities(self):
        """For demo, just returns connected components."""
        return self.connected_components()

    # ---------- 12. FRIEND-OF-FRIEND COUNT ----------
    def fof_count(self, u):
        fof = set()
        for i in range(self.n):
            if self.matrix[u][i] == 1:
                for j in range(self.n):
                    if self.matrix[i][j] == 1 and j != u and self.matrix[u][j] == 0:
                        fof.add(j)
        return [self.name(x) for x in fof]

    # ---------- DISPLAY MATRIX ----------
    def show_matrix(self):
        print("\nAdjacency Matrix:")
        header = "     " + " ".join(f"{self.name(i)[:3]:>3}" for i in range(self.n))
        print(header)
        for i in range(self.n):
            row = " ".join(f"{self.matrix[i][j]:>3}" for j in range(self.n))
            print(f"{self.name(i)[:3]:>3}  {row}")


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    print("=" * 65)
    print("  SOCIAL NETWORK — ADJACENCY MATRIX CASE STUDY")
    print("=" * 65)

    sn = SocialNetwork(8)
    names = ["Alice", "Bob", "Carol", "Dave", "Eve", "Frank", "Grace", "Heidi"]
    for i, n in enumerate(names):
        sn.add_user(i, n)

    # Build friendships
    edges = [(0,1),(0,2),(1,2),(1,3),(2,4),(3,4),(3,5),(4,5),(5,6),(6,7)]
    print("\nBuilding friendships:")
    for u, v in edges:
        sn.add_friendship(u, v)

    sn.show_matrix()

    print("\n--- 2. Are Alice & Bob friends? ---")
    print(" ", sn.are_friends(0, 1))

    print("\n--- 3. Mutual friends of Alice & Dave ---")
    print(" ", sn.mutual_friends(0, 3))

    print("\n--- 4. Friend Recommendations for Alice ---")
    for name, score in sn.recommend_friends(0):
        print(f"  → {name}  ({score} mutual friends)")

    print("\n--- 5. Degree Centrality (Most Popular Users) ---")
    for name, deg in sn.degree_centrality():
        print(f"  {name:<7} : {deg} friends")

    print("\n--- 6. BFS from Alice ---")
    print(" ", sn.bfs(0))

    print("\n--- 7. DFS from Alice ---")
    print(" ", sn.dfs(0))

    print("\n--- 8. Shortest Path: Alice → Heidi ---")
    print(" ", " → ".join(sn.shortest_path(0, 7)))

    print("\n--- 9. Connected Components ---")
    for i, comp in enumerate(sn.connected_components(), 1):
        print(f"  Component {i}: {comp}")

    print("\n--- 10. Total Triangles (Close Friend Circles) ---")
    print("  Count:", sn.count_triangles())

    print("\n--- 11. Communities ---")
    for i, comm in enumerate(sn.communities(), 1):
        print(f"  Community {i}: {comm}")

    print("\n--- 12. Friends-of-Friends of Alice ---")
    print(" ", sn.fof_count(0))