from collections import deque

# 상 좌 우 하
dr = [-1, 0, 0, 1]
dc = [0, -1, 1, 0]

n, m = map(int, input().split())
matrix = []
for _ in range(n):
    matrix.append(list(map(int, input().split())))

can_move = [[True] * n for _ in range(n)]
conv = []
for _ in range(m):
    r, c = map(int, input().split())
    conv.append((r - 1, c - 1))


def get_next_coord(cur_r, cur_c, dis_r, dis_c):
    visit = [[False] * n for _ in range(n)]
    queue = deque()
    queue.append((cur_r, cur_c, -1))
    visit[cur_r][cur_c] = True

    while queue:
        r, c, d = queue.popleft()

        if (r, c) == (dis_r, dis_c):
            return cur_r + dr[d], cur_c + dc[d]

        for i in range(4):
            nr = r + dr[i]
            nc = c + dc[i]
            if 0 <= nr < n and 0 <= nc < n and can_move[nr][nc] and not visit[nr][nc]:
                visit[nr][nc] = True
                nd = d
                if nd == -1:
                    nd = i
                queue.append((nr, nc, nd))


def find_closest_bcamp(dis_r, dis_c):
    visit = [[False] * n for _ in range(n)]
    queue = deque()
    queue.append((dis_r, dis_c, 0))
    visit[dis_r][dis_c] = True

    bcamps = []
    min_dist = int(1e9)

    while queue:
        r, c, dist = queue.popleft()

        if matrix[r][c] == 1 and can_move[r][c]:
            bcamps.append((r, c, dist))
            min_dist = min(min_dist, dist)
            continue

        for i in range(4):
            nr = r + dr[i]
            nc = c + dc[i]
            if 0 <= nr < n and 0 <= nc < n and can_move[nr][nc] and not visit[nr][nc]:
                visit[nr][nc] = True
                queue.append((nr, nc, dist + 1))

    closest_bcamps = []
    for bcamp in bcamps:
        if bcamp[2] == min_dist:
            closest_bcamps.append(bcamp)

    closest_bcamps.sort(key=lambda x: (x[0], x[1]))

    return closest_bcamps[0]


minutes = 1
person_in = 0
runners = []

while person_in < m:
    # 사람 모두 이동 후 편의점 도착자만 저장해놓음
    arrived_conv = []
    runner_len = len(runners)
    for i in range(runner_len):
        r, c, idx = runners[i]
        target = conv[idx]
        next_coord = get_next_coord(r, c, target[0], target[1])
        if next_coord == target:
            arrived_conv.append((next_coord[0], next_coord[1], idx))
        runners[i] = (next_coord[0], next_coord[1], idx) # 움직인 좌표로 업데이트

    # 편의점 좌표 사용 불가 & 편의점 도착자 제거 & 사람 In
    for runner in arrived_conv:
        can_move[runner[0]][runner[1]] = False
        runners.remove(runner)
        person_in += 1

    # 베이스캠프에 사람 배당 & runners에 추가
    if minutes <= m:
        dist_r, dist_c = conv[minutes - 1]
        bcamp = find_closest_bcamp(dist_r, dist_c)
        can_move[bcamp[0]][bcamp[1]] = False
        runners.append((bcamp[0], bcamp[1], minutes - 1))

    minutes += 1

print(minutes - 1)

