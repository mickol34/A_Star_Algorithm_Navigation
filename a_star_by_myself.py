import os


def create_maze_from_file(path):
    maze = []
    with open(path) as file:
        for single_line in file:
            values = [float(cost) for cost in single_line.split(',')]
            maze.append(values)
    return maze


def g_cost(maze, point, parent_g_cost):
    return parent_g_cost + maze[point[1]][point[0]]


def h_cost(point, end_point):
    return abs(end_point[0] - point[0]) + abs(end_point[1] - point[1])


def f_cost(maze, point, end_point, parent_g_cost):
    return g_cost(maze, point, parent_g_cost) + h_cost(point, end_point)


def find_path(maze, start_point, end_point):
    """
    główna pętla znajdująca ścieżkę
    """

    # Inicjalizacja algorytmu
    map_size_y = len(maze) - 1
    map_size_x = len(maze[0]) - 1
    parent_log = {}
    g_cost_log = {}
    f_cost_log = {}
    g_cost_log[start_point] = 0
    explored_points = [start_point]
    current_best = start_point

    # Pierwsi sąsiedzi
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i*j == 0 and i+j != 0:
                new_point = (start_point[0] + i, start_point[1] + j)
                parent_g_cost = g_cost_log[start_point]
                parent_log[new_point] = start_point
                g_cost_log[new_point] = g_cost(
                    maze, new_point, parent_g_cost)
                f_cost_log[new_point] = f_cost(
                    maze, new_point, end_point, parent_g_cost)

    # Główna pętla programu
    while end_point not in explored_points:
        # Wybór najlepszego punktu po najmniejszym koszcie
        current_best = min(f_cost_log, key=f_cost_log.get)
        f_cost_log.pop(current_best)
        explored_points.append(current_best)

        # Generowanie sąsiadów, obliczanie kosztów i zapisywanie do logów
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i*j == 0 and i+j != 0:

                    # Generowanie sąsiadów
                    new_point_x = current_best[0] + i
                    new_point_y = current_best[1] + j
                    if new_point_x < 0:
                        new_point_x = 0
                    if new_point_x > map_size_x:
                        new_point_x = map_size_x
                    if new_point_y + j < 0:
                        new_point_y = 0
                    if new_point_y > map_size_y:
                        new_point_y = map_size_y
                    new_point = (new_point_x, new_point_y)

                    # Sprawdzenie, czy sąsiaduje z punktem docelowym
                    if new_point not in parent_log.keys():
                        parent_log[new_point] = current_best

                    # Zapis do logów
                    if new_point not in explored_points:
                        parent_g_cost = g_cost_log[parent_log[new_point]]
                        parent_log[new_point] = current_best
                        g_cost_log[new_point] = g_cost(
                            maze, new_point, parent_g_cost)
                        f_cost_log[new_point] = f_cost(
                            maze, new_point, end_point, parent_g_cost)

    path = [end_point]
    current_in_path = end_point
    while True:
        current_in_path = parent_log[current_in_path]
        path.insert(0, current_in_path)
        if start_point == current_in_path:
            break

    return path


def main():
    dirname = os.path.dirname(__file__)
    path_to_file = os.path.join(
        dirname, 'costmap_generation/map_100_100.txt')
    maze = create_maze_from_file(path_to_file)

    print(len(maze))

    start_point = (1, 1)
    end_point = (99, 99)
    path = find_path(maze, start_point, end_point)
    print(path)


if __name__ == "__main__":
    main()
