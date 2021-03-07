from node import Node
from copy import deepcopy
import time


def astar(maze, start, last, m_or_d):
    root = Node(None, start)
    root.g = root.h = root.f = 0
    last = Node(None, last)
    last.g = last.h = last.f = 0

    lopen = []
    lclosed = []

    lopen.append(root)

    while len(lopen) > 0:

        cur = lopen[0]
        cur_id = 0
        for index, item in enumerate(lopen):
            if item.f < cur.f:
                cur = item
                cur_id = index

        lopen.pop(cur_id)
        lclosed.append(cur)

        path = []
        current = cur
        while current is not None:
            path.append(current.position)
            current = current.parent
        path = path[::-1]

        if cur == last:
            return path

        children = []
        for np in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

            pos_node = (cur.position[0] + np[0], cur.position[1] + np[1])

            if pos_node[0] > (len(maze) - 1) or pos_node[0] < 0 or \
                    pos_node[1] > (len(maze[len(maze)-1]) - 1) or pos_node[1] < 0:
                continue

            if not (m_or_d[0] in path or m_or_d[1] in path):
                if maze[pos_node[0]][pos_node[1]] != 0:
                    continue

            newnode = Node(cur, pos_node)
            children.append(newn)

        for child in children:
            for closed_child in lclosed:
                if child == closed_child:
                    continue
            child.g = cur.g + 1
            child.h = ((child.position[0] - last.position[0]) ** 2) + ((child.position[1] - last.position[1]) ** 2)
            child.f = child.g + child.h

            for open_node in lopen:
                if child == open_node and child.g > open_node.g:
                    continue

            lopen.append(child)


def get_map(mp_l, n, covid1, covid2, covid_level=1):
    for i in range(n):
        for j in range(n):
            if abs(i - covid1[0]) <= covid_level and abs(j - covid1[1]) <= covid_level and mp_l[i][j] == 0:
                mp_l[i][j] = 1
            if abs(i - covid2[0]) <= covid_level and abs(j - covid2[1]) <= covid_level and mp_l[i][j] == 0:
                mp_l[i][j] = 1
    return mp_l


def main(c1, c2, ms, dc, ac, hm, n_loc=9):
    n = n_loc
    a = [0] * n
    mp = []  # map
    for i in range(n):
        mp.append(a.copy())

    hx, hy = hm
    mp[hx][hy] = 2  # home
    mp1 = get_map(deepcopy(mp), n, c1, c2)
    start = time.perf_counter()
    path = astar(mp1, ac, hm, m_or_d=[ms, dc])
    end = time.perf_counter()
    if path is None:
        return
    print(f"Path for map with covid level 1 covid {path}. len1={len(path)}. time {end - start}")
    mp1_ans = path
    mp2 = get_map(deepcopy(mp),  n, c1, c2, covid_level=2)
    start = time.perf_counter()
    path = astar(mp2, ac, hm, m_or_d=[ms, dc])
    end = time.perf_counter()
    if path is None:
        return
    print(f"Path for map with covid level 2 covid {path}. len={len(path)}. time {end - start}")
    return [mp1_ans, path]
