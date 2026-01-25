maze = [
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [1, 1, 0, 1],
    [0, 0, 0, 2]
]

def solve_dfs(y, x):
    # 미로 범위를 벗어나거나 벽(1)인 경우 종료
    if x < 0 or x >= 4 or y < 0 or y >= 4 or maze[x][y] == 1:
        return False

    # 목적지(2)에 도착한 경우
    if maze[x][y] == 2:
        print(f"목적지 도착! 위치: ({x}, {y})")
        return True

    # 현재 위치 방문 처리 (길을 1로 바꿔서 다시 안 오게 함)
    maze[y][x] = 1

    # 상, 하, 좌, 우 4방향 탐색 (재귀 호출)
    if (solve_dfs(y + 1, x) or solve_dfs(y - 1, x) or
            solve_dfs(y, x + 1) or solve_dfs(y, x - 1)):
        return True

    return False


solve_dfs(0, 0)

print(maze[2][0])