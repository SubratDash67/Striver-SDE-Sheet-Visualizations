import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Max Product Subarray Animation")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (169, 169, 169)
DARK_GREY = (105, 105, 105)
ORANGE = (255, 165, 0)

font = pygame.font.SysFont("comicsans", 30)
button_font = pygame.font.SysFont("comicsans", 25)

nums = [1, 2, -3, 0, -4, -5]

index = 0
dpMin = nums[0]
dpMax = nums[0]
ans = nums[0]
start_subarray, end_subarray = 0, 0  # To track subarray
animation_speed = 1000
last_update_time = pygame.time.get_ticks()
is_paused = False

dp_table = []
current_calculation = ""


def reset_animation():
    global index, dpMin, dpMax, ans, dp_table, current_calculation, start_subarray, end_subarray
    index = 0
    dpMin = nums[0]
    dpMax = nums[0]
    ans = nums[0]
    dp_table = []
    current_calculation = ""
    start_subarray, end_subarray = 0, 0


def draw_array():
    array_x, array_y = 50, 50
    box_size = 50
    for i, num in enumerate(nums):
        if start_subarray <= i <= end_subarray:
            color = ORANGE  # Highlight the subarray with maximum product
        elif i == index:
            color = BLUE  # Highlight current element being processed
        else:
            color = WHITE
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(array_x + i * (box_size + 10), array_y, box_size, box_size),
        )
        text = font.render(str(num), True, BLACK)
        screen.blit(text, (array_x + i * (box_size + 10) + 10, array_y + 10))


def draw_table():
    headers = ["Index", "Num", "prevMin", "prevMax", "dpMin", "dpMax", "Ans"]
    start_x, start_y = 50, 150
    cell_height = 40

    column_widths = []

    for i, header in enumerate(headers):
        max_width = font.size(header)[0] + 20
        for row in dp_table:
            value_width = font.size(str(row[i]))[0] + 20
            if value_width > max_width:
                max_width = value_width
        column_widths.append(max_width)

    for i, header in enumerate(headers):
        pygame.draw.rect(
            screen, GREY, pygame.Rect(start_x, start_y, column_widths[i], cell_height)
        )
        text = font.render(header, True, BLACK)
        screen.blit(text, (start_x + 5, start_y + 5))
        start_x += column_widths[i]

    for row_idx, row in enumerate(dp_table):
        start_x = 50
        for col_idx, value in enumerate(row):
            color = GREEN if value == max(row[-2:]) else WHITE
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(
                    start_x,
                    start_y + (row_idx + 1) * cell_height,
                    column_widths[col_idx],
                    cell_height,
                ),
            )
            text = font.render(str(value), True, BLACK)
            screen.blit(text, (start_x + 5, start_y + (row_idx + 1) * cell_height + 5))
            start_x += column_widths[col_idx]


def draw_calculation():
    lines = current_calculation.split("\n")
    for i, line in enumerate(lines):
        calculation_text = font.render(line, True, WHITE)
        screen.blit(calculation_text, (50, 450 + i * 40))


def draw_pause_button():
    pause_color = GREEN if not is_paused else RED
    pygame.draw.rect(
        screen, pause_color, pygame.Rect(WIDTH - 150, HEIGHT - 100, 120, 50)
    )
    text = button_font.render("Pause" if not is_paused else "Resume", True, BLACK)
    screen.blit(text, (WIDTH - 135, HEIGHT - 90))


def draw_restart_button():
    pygame.draw.rect(screen, DARK_GREY, pygame.Rect(WIDTH - 300, HEIGHT - 100, 120, 50))
    text = button_font.render("Restart", True, WHITE)
    screen.blit(text, (WIDTH - 285, HEIGHT - 90))


def update_dp_table():
    global dpMin, dpMax, ans, index, current_calculation, start_subarray, end_subarray
    if index >= len(nums):
        return
    num = nums[index]
    prevMin = dpMin
    prevMax = dpMax
    if num < 0:
        dpMin = min(prevMax * num, num)
        dpMax = max(prevMin * num, num)
        current_calculation = f"dpMin = min({prevMax} * {num}, {num})\ndpMax = max({prevMin} * {num}, {num})"
    else:
        dpMin = min(prevMin * num, num)
        dpMax = max(prevMax * num, num)
        current_calculation = f"dpMin = min({prevMin} * {num}, {num})\ndpMax = max({prevMax} * {num}, {num})"

    if dpMax > ans:
        ans = dpMax
        end_subarray = index
        start_subarray = index
        if dpMax != 0:  # Proceed only if dpMax is not zero
            for i in range(index, -1, -1):
                if nums[i] == 0:  # Stop the subarray at a zero
                    break
                start_subarray = i

    dp_table.append([index, num, prevMin, prevMax, dpMin, dpMax, ans])
    index += 1


def main():
    global last_update_time, is_paused
    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (
                    WIDTH - 150 <= mouse_x <= WIDTH - 30
                    and HEIGHT - 100 <= mouse_y <= HEIGHT - 50
                ):
                    is_paused = not is_paused
                if (
                    WIDTH - 300 <= mouse_x <= WIDTH - 180
                    and HEIGHT - 100 <= mouse_y <= HEIGHT - 50
                ):
                    reset_animation()
        draw_array()
        draw_table()
        draw_calculation()
        draw_pause_button()
        draw_restart_button()
        if not is_paused:
            current_time = pygame.time.get_ticks()
            if current_time - last_update_time > animation_speed:
                update_dp_table()
                last_update_time = current_time
        pygame.display.flip()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
