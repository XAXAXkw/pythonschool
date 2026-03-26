import random

# Maze generation using Recursive Backtracking

WIDTH = 21   # must be odd
HEIGHT = 21  # must be odd

# Directions: (dx, dy)
DIRECTIONS = [
    (0, -2),  # up
    (2, 0),   # right
    (0, 2),   # down
    (-2, 0)   # left
]


def create_grid(width, height):
    return [["#" for _ in range(width)] for _ in range(height)]


def is_in_bounds(x, y, width, height):
    return 0 < x < width - 1 and 0 < y < height - 1


def carve_passages(x, y, grid, width, height):
    directions = DIRECTIONS[:]
    random.shuffle(directions)

    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        if is_in_bounds(nx, ny, width, height) and grid[ny][nx] == "#":
            # Remove wall between
            grid[y + dy // 2][x + dx // 2] = " "
            grid[ny][nx] = " "

            carve_passages(nx, ny, grid, width, height)


def generate_maze(width, height):
    grid = create_grid(width, height)

    start_x, start_y = 1, 1
    grid[start_y][start_x] = " "

    carve_passages(start_x, start_y, grid, width, height)

    return grid


def print_maze(grid):
    for row in grid:
        print("".join(row))


if __name__ == "__main__":
    maze = generate_maze(WIDTH, HEIGHT)
    print_maze(maze)
