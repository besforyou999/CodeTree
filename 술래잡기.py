import sys

input = sys.stdin.readline

# 상 하 좌 우
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]

n, m, h, k = map(int, input().split())

mid = n // 2 + 1

outer = True
catcher = (mid, mid)
runners = [
    [[] for _ in range(n + 1)]
    for _ in range(n + 1)
]
next_runners = []
tree = [[False] * (n + 1) for _ in range(n + 1)]
outer_move_dir = [[0] * (n + 1) for _ in range(n + 1)]
inner_move_dir = [[0] * (n + 1) for _ in range(n + 1)]

move_lengths_outer = []
move_lengths_inner = []
for i in range(1, n):
    for _ in range(2):
        move_lengths_outer.append(i)
move_lengths_outer.append(n - 1)
move_lengths_inner = list(reversed(move_lengths_outer))


for _ in range(m):
    r, c, d = map(int, input().split())
    if d == 1:
        runners[r][c].append(3)
    else:
        runners[r][c].append(1)

for _ in range(h):
    r, c = map(int, input().split())
    tree[r][c] = True


def switch_direction_outer(a):
    if a == 0:
        return 3
    elif a == 1:
        return 2
    elif a == 2:
        return 0
    else:
        return 1


def switch_direction_inner(a):
    if a == 0:
        return 2
    elif a == 1:
        return 3
    elif a == 2:
        return 1
    else:
        return 0


def init_directions():
    move_cnt = 0
    rr, cc = mid, mid
    d = 0
    outer_move_dir[rr][cc] = d
    while (rr, cc) != (1, 1):
        move_len = move_lengths_outer[move_cnt]
        for _ in range(move_len):
            rr = rr + dr[d]
            cc = cc + dc[d]
            outer_move_dir[rr][cc] = d
        d = switch_direction_outer(d)
        outer_move_dir[rr][cc] = d
        move_cnt += 1

    move_cnt = 0
    rr, cc = 1, 1
    d = 1
    inner_move_dir[rr][cc] = d
    while (rr, cc) != (mid, mid):
        move_len = move_lengths_inner[move_cnt]
        for _ in range(move_len):
            rr = rr + dr[d]
            cc = cc + dc[d]
            inner_move_dir[rr][cc] = d
        d = switch_direction_inner(d)
        inner_move_dir[rr][cc] = d
        move_cnt += 1


init_directions()


def switch_direction(a):
    if a == 0:
        return 1
    elif a == 1:
        return 0
    elif a == 2:
        return 3
    else:
        return 2


def move_runners():

    next_dirs = [[[] for _ in range(n+1)] for _ in range(n+1)]

    for r in range(1, n+1):
        for c in range(1, n+1):
            if runners[r][c]:
                if abs(r - catcher[0]) + abs(c - catcher[1]) <= 3:
                    for d in runners[r][c]:
                        nr = r + dr[d]
                        nc = c + dc[d]
                        if 1 <= nr <= n and 1 <= nc <= n:
                            if (nr, nc) == catcher:
                                next_dirs[r][c].append(d)
                            else:
                                next_dirs[nr][nc].append(d)
                        else:
                            nd = switch_direction(d)
                            nr = r + dr[nd]
                            nc = c + dc[nd]
                            if (nr, nc) == catcher:
                                next_dirs[r][c].append(nd)
                            else:
                                next_dirs[nr][nc].append(nd)
                else:
                    next_dirs[r][c] += runners[r][c]

    for r in range(1, n + 1):
        for c in range(1, n + 1):
            runners[r][c] = next_dirs[r][c]


def move_catcher():
    global outer, catcher
    r, c = catcher
    if outer:
        cd = outer_move_dir[r][c]
        r = r + dr[cd]
        c = c + dc[cd]

        if (r, c) == (1, 1):
            outer = False
    else:
        cd = inner_move_dir[r][c]
        r = r + dr[cd]
        c = c + dc[cd]
        if (r, c) == (mid, mid):
            outer = True

    catcher = (r, c)


def get_caught():
    r, c = catcher
    d = outer_move_dir[r][c]
    if not outer:
        d = inner_move_dir[r][c]

    cnt = 0

    for l in range(3):
        nr = r + dr[d] * l
        nc = c + dc[d] * l
        if 1 <= nr <= n and 1 <= nc <= n:
            if not tree[nr][nc] and runners[nr][nc]:
                cnt += len(runners[nr][nc])
                runners[nr][nc].clear()

    return cnt

ans = 0
for t in range(1, k + 1):
    move_runners()  # O(n^2)
    move_catcher()
    res = get_caught()
    ans += t * res

print(ans)

