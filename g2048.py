import pygame
from utils import draw_grid_lines
from random import randrange, choice
class App:
    SIZE: int = 100
    ROWS: int = 4
    COLS: int = 4
    
    COLORS: dict[str|int: tuple[int]] = {"bg": (205, 193, 181), "lines": (191, 175, 159), "dark_fg": (121, 111, 101), "light_fg": (247, 247, 237), 2: (238, 228, 218), 4: (236, 224, 202), 8: (242, 176, 121), 16: (245, 149, 101), 32: (245, 124, 95), 64: (245, 97, 59), 128: (237, 206, 113), 256: (237, 204, 99), 512: (236, 197, 60), 1024: (255, 190, 40), 2048: (255, 185, 0)}
    MOVE_DIRS: dict[str, tuple[int]] = {"UP": (-1, 0), "RIGHT": (0, 1), "DOWN": (1, 0), "LEFT": (0, -1)}
    NUM_IMGS: dict[str: pygame.Surface]

    def __init__(self, WIN: pygame.Surface) -> None:
        pygame.display.set_caption("2048")
        self.WIN: pygame.Surface = WIN

        self.typeface: pygame.Font = pygame.font.Font("freesansbold.ttf", App.SIZE//3)
        self.load_num_images()

        self.surf: pygame.Surface = pygame.Surface((App.COLS*App.SIZE, App.ROWS*App.SIZE))
        self.surf_rect: pygame.Rect = self.surf.get_rect()
        win_rect: pygame.Rect = WIN.get_rect()
        self.surf_rect.center = (win_rect.width//2, win_rect.height//2)

        self.reset()
    
    def load_num_images(self) -> None:
        App.NUM_IMGS = {2**i: pygame.Surface((App.SIZE, App.SIZE)) for i in range(1, 12)}
        for num, surf in App.NUM_IMGS.items():
            surf.fill(App.COLORS[num])
            text: pygame.Surface = self.typeface.render(str(num), True, App.COLORS["light_fg" if num > 4 else "dark_fg"])
            text_rect: pygame.Rect = text.get_rect()
            text_rect.center = (App.SIZE//2, App.SIZE//2)
            surf.blit(text, text_rect)
    
    def reset(self) -> None:
        self.reset_board()
        self.place_random()
        self.place_random()

    def reset_board(self) -> None:
        self.board: list[list[int]] = [[0 for _ in range(App.COLS)] for _ in range(App.ROWS)]
    
    def draw_board(self) -> None:
        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                if col:
                    self.surf.blit(App.NUM_IMGS[col], (j*App.SIZE, i*App.SIZE))

    def draw(self) -> None:
        self.surf.fill(App.COLORS["bg"])
        self.draw_board()
        draw_grid_lines(self.surf, App.ROWS, App.COLS, App.SIZE, App.COLORS["lines"], width=10)
        self.update_win()
    
    def place_random(self) -> None:
        num: int = (randrange(0, 10)//9 + 1)*2
        row, col = choice(tuple((i, j) for i in range(App.ROWS) for j in range(App.COLS) if not self.board[i][j]))
        self.board[row][col] = num
    
    def move_num(self, row: int, col: int, dir: str) -> bool:
        moved: bool = False
        if self.board[row][col] == 0: return moved
        v: tuple[int] = App.MOVE_DIRS[dir]
        while True:
            new_row, new_col = row + v[0], col + v[1]
            if not (0 <= new_row < App.ROWS and 0 <= new_col < App.COLS):
                return moved
            elif self.board[new_row][new_col] == 0:
                self.board[new_row][new_col], self.board[row][col] = self.board[row][col], self.board[new_row][new_col]
                moved = True
            elif self.board[new_row][new_col] == self.board[row][col]:
                self.board[row][col] = 0
                self.board[new_row][new_col] *= 2
                moved = True
                return moved
            row, col = new_row, new_col

    def move(self, dir: str) -> None:
        match dir:
            case "UP":
                for i in range(1, App.ROWS):
                    for j in range(App.COLS):
                        moved = self.move_num(i, j, dir)
            case "DOWN":
                for i in range(App.ROWS - 2, -1, -1):
                    for j in range(App.COLS):
                        moved: bool = self.move_num(i, j, dir)
            case "LEFT":
                for j in range(1, App.COLS):
                    for i in range(App.ROWS):
                        moved: bool = self.move_num(i, j, dir)
            case "RIGHT":
                for j in range(App.COLS - 2, -1, -1):
                    for i in range(App.ROWS):
                        moved: bool = self.move_num(i, j, dir)
        if moved:
            if self.check_empty():
                self.place_random()
            else:
                self.reset()
    
    def check_empty(self) -> bool:
        return not all(j for i in self.board for j in i)

    def update_win(self) -> None:
        pygame.display.update(self.WIN.blit(self.surf, self.surf_rect))

    def quit(self) -> None:
        pygame.display.set_caption("Games")

    def mainloop(self) -> bool:
        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        return False

                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                return True
                            case pygame.K_RETURN:
                                self.reset()
                            case pygame.K_UP:
                                self.move("UP")
                            case pygame.K_DOWN:
                                self.move("DOWN")
                            case pygame.K_LEFT:
                                self.move("LEFT")
                            case pygame.K_RIGHT:
                                self.move("RIGHT")
            self.draw()

if __name__ == "__main__":
    pygame.init()
    WIN: pygame.Surface = pygame.display.set_mode((App.COLS*App.SIZE, App.ROWS*App.SIZE))
    app: App = App(WIN)
    app.mainloop()
    pygame.quit()