import pygame
from random import choice
from utils import Label

class App:
    WIDTH: int = 1080
    HEIGHT: int = 640
    PADDING: int = 50

    BALL_SIZE: int = 30
    BALL_DIRS: tuple[list[int], ...] = ([1, -1], [1, 1], [-1, 1], [-1, -1])
    BALL_SPEED: int = 1

    PADDLE_WIDTH: int = 20
    PADDLE_HEIGHT: int = 150
    PADDING_SPEED: int = 1
    
    COLORS: dict[str, tuple[int, int, int]] = {"bg": (0, 0, 0), "left_paddle": (255, 0, 0), "right_paddle": (0, 255, 0), "ball": (0, 0, 255), "fg": (255, 255, 255), "text_bg": (50, 50, 50)}

    def __init__(self, WIN: pygame.Surface) -> None:
        pygame.display.set_caption("Pong")
        self.WIN: pygame.Surface = WIN

        # self.typeface: pygame.Font = pygame.font.Font("freesansbold.ttf", int(App.SIZE*0.8))

        self.surf: pygame.Surface = pygame.Surface((App.WIDTH, App.HEIGHT))
        self.surf_rect: pygame.Rect = self.surf.get_rect()
        win_rect: pygame.Rect = WIN.get_rect()
        self.surf_rect.center = (win_rect.width//2, win_rect.height//2)

        self.ball_rect: pygame.Rect = pygame.Rect((0, 0, App.BALL_SIZE, App.BALL_SIZE))
        self.left_paddle_rect: pygame.Rect = pygame.Rect((0, 0, App.PADDLE_WIDTH, App.PADDLE_HEIGHT))
        self.left_paddle_rect.centerx = App.PADDING
        self.right_paddle_rect: pygame.Rect = pygame.Rect((0, 0, App.PADDLE_WIDTH, App.PADDLE_HEIGHT))
        self.right_paddle_rect.centerx = App.WIDTH - App.PADDING

        self.reset()
    
    def reset_ball(self) -> None:
        self.ball_rect.center = (App.WIDTH//2, App.HEIGHT//2)
        self.ball_dir: list[int] = choice(App.BALL_DIRS)
    
    def reset(self) -> None:
        self.reset_ball()
        self.left_paddle_rect.centery = App.HEIGHT//2
        self.right_paddle_rect.centery = App.HEIGHT//2
        self.score: list[int] = [0, 0]
        self.left_score_label: Label = Label('Score: 0', (0, 0), anchor = "topleft", foreground = App.COLORS["fg"], background = App.COLORS["text_bg"])
        self.right_score_label: Label = Label('Score: 0', (App.WIDTH, 0), anchor = "topright", foreground = App.COLORS["fg"], background = App.COLORS["text_bg"])

    def draw(self) -> None:
        self.surf.fill(App.COLORS["bg"])
        self.left_score_label.draw(self.surf)
        self.right_score_label.draw(self.surf)
        pygame.draw.line(self.surf, App.COLORS["fg"], (App.WIDTH//2, 0), (App.WIDTH//2, App.HEIGHT))
        pygame.draw.rect(self.surf, App.COLORS["ball"], self.ball_rect)
        pygame.draw.rect(self.surf, App.COLORS["left_paddle"], self.left_paddle_rect)
        pygame.draw.rect(self.surf, App.COLORS["right_paddle"], self.right_paddle_rect)
        self.update_win()
    
    def paddle_movement(self) -> None:
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.left_paddle_rect.y = max(self.left_paddle_rect.y - App.PADDING_SPEED, 0)
        elif pressed[pygame.K_s]:
            self.left_paddle_rect.bottom = min(self.left_paddle_rect.bottom + App.PADDING_SPEED, App.HEIGHT)
        
        if pressed[pygame.K_UP]:
            self.right_paddle_rect.y = max(self.right_paddle_rect.y - App.PADDING_SPEED, 0)
        elif pressed[pygame.K_DOWN]:
            self.right_paddle_rect.bottom = min(self.right_paddle_rect.bottom + App.PADDING_SPEED, App.HEIGHT)
    
    def ball_movement(self) -> None:
        self.ball_rect.x += App.BALL_SPEED*self.ball_dir[0]
        if self.ball_rect.x <= 0:
            self.score[0] += 1
            self.left_score_label.changeText(f"Score: {self.score[0]}")
            self.reset_ball()
        elif self.ball_rect.right > App.WIDTH:
            self.score[1] += 1
            self.right_score_label.changeText(f"Score: {self.score[1]}")
            self.reset_ball()
        if self.ball_rect.colliderect(self.left_paddle_rect):
            self.ball_rect.left = self.left_paddle_rect.right
            self.ball_dir[0] *= -1
        if self.ball_rect.colliderect(self.right_paddle_rect):
            self.ball_rect.right = self.right_paddle_rect.left
            self.ball_dir[0] *= -1
        
        self.ball_rect.y += App.BALL_SPEED*self.ball_dir[1]
        if self.ball_rect.y <= 0:
            self.ball_rect.y = 0
            self.ball_dir[1] *= -1
        elif self.ball_rect.bottom > App.HEIGHT:
            self.ball_rect.bottom = App.HEIGHT
            self.ball_dir[1] *= -1
    
    def update(self) -> None:
        self.ball_movement()
        self.paddle_movement()

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
                                self.quit()
                                return True
                            case pygame.K_RETURN | pygame.K_r:
                                self.reset()
            self.update()
            self.draw()

if __name__ == "__main__":
    pygame.init()
    WIN: pygame.Surface = pygame.display.set_mode((App.WIDTH, App.HEIGHT))
    app: App = App(WIN)
    app.mainloop()
    pygame.quit()