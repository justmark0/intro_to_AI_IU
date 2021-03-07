from copy import deepcopy
import time

n = 9
a = [0] * n
mp = []  # map
for i in range(n):
    mp.append(a.copy())

covid1 = [0, 3]
covid2 = [100, 100]
mask = [1, 3]
doctor = [3, 0]

path = []
path_ln = int(1e10)


def rec(lmp: list, lcl_path: list, covid_level, i=0, j=0, ln=0):
    global path_ln
    global path

    mp_visited = deepcopy(lmp)
    local_path = lcl_path.copy()
    if mp_visited[i][j] == 1:
        return
    ln += 1
    if ln >= path_ln:
        return
    local_path.append((i, j))
    if mp[i][j] == 2:
        if path_ln > ln:
            path = local_path
            path_ln = ln
            # print(f"Local:{local_path}")
        return
    else:
        mp_visited[i][j] = 1
        directions = [(1, 1), (-1, -1), (0, 1), (-1, 0), (0, -1), (1, 0), (-1, 1), (1, -1)]
        for d in directions:
            x, y = d
            if mask in local_path or doctor in local_path:
                if 0 <= i + x < n and 0 <= j + y < n and mp_visited[i + x][j + y] != 1:
                    rec(mp_visited, local_path, covid_level, i + x, j + y, ln)
            else:
                if 0 <= i + x < n and 0 <= j + y < n and is_covid(i + x, j + y, covid_level) and \
                        mp_visited[i + x][j + y] != 1:
                    rec(mp_visited, local_path, covid_level,  i + x, j + y, ln)


def is_covid(i, j, covid_level):
    if abs(i - covid1[0]) <= covid_level and abs(j - covid1[1]) <= covid_level:
        return True
    if abs(i - covid2[0]) <= covid_level and abs(j - covid2[1]) <= covid_level:
        return True
    return False


def main(c1, c2, ms, dc, ac, hm, n_loc=9):
    global path
    global path_ln
    global covid2
    global covid1
    global mask
    global doctor
    global n
    global a
    global mp

    n = n_loc
    a = [0] * n
    mp = []  # map
    for i in range(n):
        mp.append(a.copy())

    hx, hy = hm
    mp[hx][hy] = 2  # home
    covid1 = c1
    covid2 = c2
    mask = ms
    doctor = dc
    mp1 = deepcopy(mp)
    acx, acy = ac
    path = []
    path_ln = int(1e10)
    start = time.perf_counter()
    rec(mp1, [], acx, acy, 1)
    end = time.perf_counter()
    brute_time = start - end
    print(f"Path for map with covid level 1 covid {path}. len1={path_ln} time:{brute_time}")
    if not path:
        return None
    mp1_ans = path
    path = []
    path_ln = int(1e10)
    mp2 = deepcopy(mp)
    start = time.perf_counter()
    rec(mp2, [], acx, acy, 2)
    end = time.perf_counter()
    brute_time = start - end
    print(f"Path for map with covid level 2 covid {path}. len={path_ln} time:{brute_time}")
    if not path:
        return None
    return [mp1_ans, path]
