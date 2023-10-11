import copy, sys
from collections import deque

N, M, K = map(int, input().split())

# 우/하/좌/상
dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

# 주위 8칸. 0, 45, 90, 135, 180, 225, 270, 315
d8r = [-1, -1, 0, 1, 1, 1, 0, -1]
d8c = [0, 1, 1, 1, 0, -1, -1, -1]

towers = [[(0, 0)] * M for _ in range(N)]

attack_involved = [[False] * M for _ in range(N)]

for r in range(N):
    line = list(map(int, input().split()))
    for c in range(M):
        towers[r][c] = (line[c], 0)


def get_alive_towers():
    alive = []

    for r in range(N):
        for c in range(M):
            power, recent = towers[r][c]
            if power > 0:
                alive.append((r, c, power, recent))
    
    return alive


def get_attacker(arr):
    arr.sort(key=lambda x: (x[2], -x[3], -(x[0] + x[1]), -x[1]))
    return arr[0]


def get_hit_tower(arr):
    arr.sort(key=lambda x: (-x[2], x[3], (x[0] + x[1]), x[1]))
    return arr[0]


def get_lazer_route(attacker, hit):
    sr, sc, power, rec = attacker
    visit = [[False] * M for _ in range(N)]
    visit[sr][sc] = True
    queue = deque()
    queue.append((sr, sc, []))

    while queue:
        r, c, route = queue.popleft()

        if (r, c) == (hit[0], hit[1]):
            return route
        
        for i in range(4):
            nr = (r + dr[i]) % N
            nc = (c + dc[i]) % M

            if towers[nr][nc][0] > 0 and not visit[nr][nc]:
                visit[nr][nc] = True
                new_route = copy.deepcopy(route)
                new_route.append((nr, nc))
                queue.append((nr, nc, new_route))

    return []


# 주위 8개 영역. 부서진 포탑은 제외
def get_bombed_area(attacker, hit):
    
    area = []
    r, c, power, recent = hit
    
    for i in range(8):

        nr = (r + d8r[i]) % N
        nc = (c + d8c[i]) % M

        if towers[nr][nc][0] > 0 and (nr, nc) != (attacker[0], attacker[1]):
            area.append((nr, nc))
    
    return area


def restore_tower():
    for r in range(N):
        for c in range(M):
            power, recent = towers[r][c]
            if power > 0 and not attack_involved[r][c]:
                towers[r][c] = (power + 1, recent)


for k in range(K):
    alive_towers = get_alive_towers()
    # 살아있는 타워 1개면 즉시 종료
    if len(alive_towers) == 1:
        print(alive_towers[0][2])
        sys.exit(0)

    # 공격자 선정
    attacker = get_attacker(alive_towers)
    # 피격자 선정
    hit_tower = get_hit_tower(alive_towers)
    
    # 휘말린 타워 탐색
    lazer = True
    involed_towers = []
    involed_towers = get_lazer_route(attacker, hit_tower)
    if not involed_towers:
        lazer = False
        involed_towers = get_bombed_area(attacker, hit_tower)
    
    if lazer:
        involed_towers.pop()

    # 공격 관련자 배열 초기화
    attack_involved = [[False] * M for _ in range(N)]

    # 공격자 강화 & 최근 공격 업데이트
    r, c, power, recent = attacker
    towers[r][c] = (power + N + M, k + 1)
    attack_involved[r][c] = True

    # 공격 데미지
    hit_point = power + N + M 

    # 피격자 공격
    r, c, power, recent = hit_tower
    towers[r][c] = (power - hit_point, recent)
    attack_involved[r][c] = True

    # 휘말린 타워
    for r, c in involed_towers:
        attack_involved[r][c] = True
        power, recent = towers[r][c]
        towers[r][c] = (power - (hit_point // 2), recent)
    
    # 포탑 정비
    restore_tower()

alive_towers = get_alive_towers()
alive_towers.sort(key= lambda x: -x[2])
print(alive_towers[0][2])

