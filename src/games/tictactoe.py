import pygame
from utils import draw_grid_lines

class App:
    SIZE: int = 200
    GRID_LEN: int = 3
    
    COLORS: dict[str, tuple[int, int, int]] = {"bg": (255, 255, 255), "lines": (0, 0, 0), "fg": (0, 0, 0)}
    MARKER_IMGS: dict[int, pygame.Surface] # X, O

    def __init__(self, WIN: pygame.Surface) -> None:
        pygame.display.set_caption("Tic Tac Toe")
        self.WIN: pygame.Surface = WIN

        self.typeface: pygame.Font = pygame.font.Font("freesansbold.ttf", int(App.SIZE*0.8))
        self.load_marker_images()

        self.surf: pygame.Surface = pygame.Surface((App.GRID_LEN*App.SIZE, App.GRID_LEN*App.SIZE + App.SIZE//3))
        self.surf_rect: pygame.Rect = self.surf.get_rect()
        win_rect: pygame.Rect = WIN.get_rect()
        self.surf_rect.center = (win_rect.width//2, win_rect.height//2)

        self.reset()
    
    def load_marker_images(self) -> None:
        App.MARKER_IMGS = {}
        for i, marker in enumerate("XO", 1):
            surf: pygame.Surface = pygame.Surface((App.SIZE, App.SIZE))
            surf.fill(App.COLORS["bg"])
            text: pygame.Surface = self.typeface.render(marker, True, App.COLORS["fg"])
            text_rect: pygame.Rect = text.get_rect()
            text_rect.center = (App.SIZE//2, App.SIZE//2)
            surf.blit(text, text_rect)
            App.MARKER_IMGS[i] = surf
    
    def reset(self) -> None:
        self.reset_board()
        self.turn: int = 0

    def reset_board(self) -> None:
        self.board: list[list[int]] = [[0 for _ in range(App.GRID_LEN)] for _ in range(App.GRID_LEN)]
    
    def draw_board(self) -> None:
        self.surf.blits(
            (App.MARKER_IMGS[col], (j*App.SIZE, i*App.SIZE))
            for i, row in enumerate(self.board)
            for j, col in enumerate(row)
            if col
        )

    def draw(self) -> None:
        self.surf.fill(App.COLORS["bg"])
        self.draw_board()
        draw_grid_lines(self.surf, App.GRID_LEN, App.GRID_LEN, App.SIZE, App.COLORS["lines"], width=10)
        self.update_win()

    def update_win(self) -> None:
        pygame.display.update(self.WIN.blit(self.surf, self.surf_rect))

    def quit(self) -> None:
        pygame.display.set_caption("Games")
    
    def check_update(self, row: int, col: int, turn) -> bool:
        win_row: bool = True
        win_col: bool = True
        for i in range(self.GRID_LEN):
            if self.board[i][col] != turn:
                win_col = False
            if self.board[row][i] != turn:
                win_row = False
        return win_row or win_col or ((row + col)&1 == 0 and
            (self.board[0][0] == self.board[1][1] == self.board[2][2] == turn or
            self.board[0][2] == self.board[1][1] == self.board[2][0] == turn)
        )
    
    def on_click(self) -> bool:
        mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
        if not self.surf_rect.collidepoint(mouse_pos):
            return False
        row: int = (mouse_pos[1] - self.surf_rect.y)//self.SIZE
        col: int = (mouse_pos[0] - self.surf_rect.x)//self.SIZE
        if (self.board[row][col]):
            return False
        self.board[row][col] = self.turn + 1
        if self.check_update(row, col, self.turn + 1):
            self.reset()
            return False
        return True

    def mainloop(self) -> bool:
        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        return False

                    case pygame.MOUSEBUTTONDOWN:
                        if self.on_click():
                            self.turn = (self.turn + 1)&1

                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                self.quit()
                                return True
                            case pygame.K_RETURN | pygame.K_r:
                                self.reset()
            self.draw()

if __name__ == "__main__":
    pygame.init()
    WIN: pygame.Surface = pygame.display.set_mode((App.GRID_LEN*App.SIZE, App.GRID_LEN*App.SIZE))
    app: App = App(WIN)
    app.mainloop()
    pygame.quit()