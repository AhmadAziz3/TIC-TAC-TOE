import pygame
from pygame.locals import *


pygame.init()

width = 600
height = 600
BOARD_ROWS = 3
BOARD_COLUMNS = 3
SQUARE_SIZE = 100
CIRCLE_RADIUS = 48
CIRCLE_WIDTH = 7
CROSS_WIDTH = 8
CROSS_COLOR = (255, 87, 34)
CIRCLE_COLOR =  (255, 193, 37)
BOARD_COLOR= (210, 220, 225)
BG_COLOR=(102, 194, 255)
TEXT_COLOR=(70,70,70)
HIGHLIGHT_CELL_COLOR=(173, 216, 230)
BLUE=BG_COLOR#(50, 150, 255)
WHITE=(245,245,245)
HIGHLIGHT_BUTTON_COLOR=(255, 230, 100)
click_vsx=pygame.mixer.Sound("game_click.wav")

class Board:
    def __init__(self, board_pos, board_width, board_height) -> None:
        self.board_pos = board_pos
        self.board_width = board_width
        self.board_height = board_height
        self.board_rect = pygame.Rect(self.board_pos[0], self.board_pos[1], self.board_width, self.board_height)

    def draw_board(self):
        pygame.draw.rect(screen,BOARD_COLOR, self.board_rect)

    def draw_lines(self):
        topleft = self.board_rect.topleft
        topright = self.board_rect.topright
        bottomleft = self.board_rect.bottomleft
        color = (40,40,40)
        width = 5
        self.space = self.board_rect.width // 3
        for row in range(2):
            pygame.draw.line(screen, color, (topleft[0], topleft[1] + self.space),
                             (topright[0], topright[1] + self.space), width)
            pygame.draw.line(screen, color, (topleft[0] + self.space, topleft[1]),
                             (bottomleft[0] + self.space, bottomleft[1]), width)
            self.space += self.space

    def board_cells(self):
        self.cells = []
        self.cell_size = self.board_rect.width // 3
        incrementx, incrementy = 0, 0
        for i in range(3):  # for columns
            for j in range(3):  # for rows
                self.cell_rect = pygame.Rect(self.board_rect.topleft[0] + incrementx,
                                             self.board_rect.topleft[1] + incrementy,
                                             self.cell_size, self.cell_size)
                incrementx += self.cell_size
                self.cells.append(self.cell_rect)
            incrementx = 0  # for 2nd and 3rd row because it should start from 0
            incrementy += self.cell_size  # for becoming columns long for row 2 and 3

    def draw_cross(self, cell_number):
        self.space_cross = (self.board_rect.width // 3) * (70 / 100)
        self.cell_size = self.board_rect.width // 3
        self.cross_offset = (self.cell_size - self.space_cross) / 2
        x = self.cells[cell_number].topleft[0] + self.cross_offset
        y = self.cells[cell_number].topleft[1] + self.cross_offset
        pygame.draw.line(screen, CROSS_COLOR, (x, y), (x + self.space_cross, y + self.space_cross), CROSS_WIDTH)
        pygame.draw.line(screen, CROSS_COLOR, (x, y + self.space_cross), (x + self.space_cross, y), CROSS_WIDTH)

    def draw_circle(self, cell_number):
        self.circle_center = self.cells[cell_number].center
        pygame.draw.circle(screen, CIRCLE_COLOR, self.circle_center, CIRCLE_RADIUS, CIRCLE_WIDTH)

    def check_winner(self):
        winner_combinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

        for combination in winner_combinations:
            if board_state[combination[0]] == board_state[combination[1]] == board_state[combination[2]] and board_state[combination[0]] is not None:
                return board_state[combination[0]]  # winner

        return None  # No Winner
    
def display_winner(winner):
    global highlight_button,actual_game
    screen.fill(BG_COLOR)
    
    # Winner message
    font = pygame.font.Font(None, 120)  # Create font object with size 120
    text = font.render(winner, True, TEXT_COLOR)  # Render the text
    screen.blit(text, (160, 150))  # Display the text on the screen
    
    restart_button_rect = pygame.Rect(165, 280, 280, 95)
    
    # Restart message
    font_1 = pygame.font.Font(None, 80)  # Create font object with size 80
    restart_message = "RESTART"
    text_1 = font_1.render(restart_message, True, BG_COLOR)  # Render the text
    
    pygame.display.update()  # Update the screen with initial elements
    
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEMOTION:
                # Set the highlight based on the mouse position
                mouse_position = event.pos
                highlight_button = restart_button_rect.collidepoint(mouse_position)
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting_for_input = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                click_vsx.play()
                # Check if Start button is clicked
                if restart_button_rect.collidepoint(mouse_pos):
                    actual_game=True
        
        # Draw the button with the appropriate border radius
        if not highlight_button:
            pygame.draw.rect(screen, WHITE, restart_button_rect, border_radius=80)  # Normal button  
        else:
             pygame.draw.rect(screen, HIGHLIGHT_BUTTON_COLOR, restart_button_rect, border_radius=20)  # Highlighted button
            
        
        # Display the restart message
        screen.blit(text_1, (175, 300))
        pygame.display.update()

def reset_game():
    global current_player,board_state,game_over,actual_game,highlight_cell
    current_player = 'X'  
    board_state = [None for _ in range(9)]
    game_over=False
    # Reset the highlight_cell (no cell is highlighted at the start)
    highlight_cell = None
    # Reset game-related flag (whether we're in the game or showing the restart menu)
    actual_game = True

def welcome_screen():
    global welcome,game_over,highlight_button
    screen.fill(BLUE)
   
    # Draw welcome
    font1=pygame.font.Font(None, 100)
    welcome_text=font1.render('WELCOME',True,WHITE)
    screen.blit(welcome_text,(120,100))
   
    # Draw title
    font2=pygame.font.Font(None, 70)
    title_text=font2.render("TIC-TAC-TOE",False,WHITE)
    screen.blit(title_text,(150,220))
    
    # Start and exit button rectangles
    start_button_rect = pygame.Rect(230,300, 150, 80)
    exit_button_rect = pygame.Rect(230,400, 150, 80)

    # Highlighting buttons
   
    buttons=[start_button_rect,exit_button_rect]
    for i, button in enumerate(buttons):
        if highlight_button == i:
            pygame.draw.rect(screen, HIGHLIGHT_BUTTON_COLOR, button,border_radius=20)  # Highlight button
           
        else:
            pygame.draw.rect(screen, WHITE, button,border_radius=50)  # Normal button

    # Start button
    start_text=font2.render("Start",True,BLUE)
    screen.blit(start_text, (start_button_rect.x + start_button_rect.width // 2 - start_text.get_width() // 2,
                             start_button_rect.y + start_button_rect.height // 2 - start_text.get_height() // 2))
    
     # Exit button
    exit_text=font2.render("Exit",True,BLUE)
    screen.blit(exit_text, (exit_button_rect.x + exit_button_rect.width // 2 - exit_text.get_width() // 2,
                             exit_button_rect.y + exit_button_rect.height // 2 - exit_text.get_height() // 2))
    
    for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                click_vsx.play()
                # Check if Start button is clicked
                if start_button_rect.collidepoint(mouse_pos):
                    print("Start Game!")
                    game_over=False
                    welcome=False
                    
                # Check if Exit button is clicked
                elif exit_button_rect.collidepoint(mouse_pos):
                    game_over = True
                    pygame.quit()
            
            if event.type == pygame.MOUSEMOTION:
                # Set the highlight based on the mouse position
                mouse_position = event.pos
                highlight_button = None  # Reset highlight
                for i, button in enumerate(buttons):
                    if button.collidepoint(mouse_position):
                        highlight_button = i  # Set which button is highlighted
    pygame.display.update()

# Initialize the board and pygame window
board = Board((100, 100), 400, 400)
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Tic-Tac-Toe")

clock = pygame.time.Clock()
fps = 100
current_player = 'X'  # 'X' starts the game
board_state = [None for _ in range(9)]  # Track board state (9 cells)
game_over = False  # Game state flag to track if the game is over
highlight_cell=None
highlight_button=None
actual_game=True
welcome=True

while not game_over:

    if welcome:
        welcome_screen()
        
    if not welcome:
        if actual_game is True:
            screen.fill(BG_COLOR)
            board.draw_board()
            board.draw_lines()
            board.board_cells()

            # HIGHLIGHTING CELL IF MOUSE IS ON CELL 
            if highlight_cell is not None:
                cell_rect=board.cells[highlight_cell]
                pygame.draw.rect(screen,HIGHLIGHT_CELL_COLOR,cell_rect)
    
            # Drawing the board according to the current state
            for i in range(9):
                if board_state[i] == 'X':
                    board.draw_cross(i)
                elif board_state[i] == 'O':
                    board.draw_circle(i)

        for event in pygame.event.get():

            if event.type == QUIT:
                game_over = True  # Quit the game
                pygame.quit()
            
            if actual_game:
                if event.type == pygame.MOUSEMOTION:
                    # HIGHLIGHT CELL CODE
                    mouse_position = event.pos
                    for i, cell in enumerate(board.cells):
                        if cell.collidepoint(mouse_position) and board_state[i] is None:
                            highlight_cell=i
                
                elif event.type == pygame.VIDEORESIZE:
                  screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                
                if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    mouse_position = event.pos
                    for i, cell in enumerate(board.cells):
                        if cell.collidepoint(mouse_position) and board_state[i] is None:

                            # Place the current player's mark
                            click_vsx.play()
                            if current_player == 'X':
                                board_state[i] = 'X'
                            else:
                                board_state[i] = 'O'
                            # Draw the current move immediately
                            if current_player == 'X':
                                board.draw_cross(i)
                            else:
                                board.draw_circle(i)

                            # Switch the turn
                            if current_player == 'X':
                                current_player = 'O'
                            else:
                                current_player = 'X'

                # Check for a winner immediately after the move
                winner = board.check_winner()
                if winner:
                    display_winner(f"{winner} Wins!")  # Display the winner
                    actual_game=False

                # After checking for a winner, check for a tie if all cells are filled
                if None not in board_state:  # If there is no `None` in board_state, all cells are filled
                    if not board.check_winner():  # If there's no winner
                        display_winner("   Tie !  ")  # Display tie message
                        actual_game=False
                          
            if actual_game is False:
                reset_game()
                game_over=False
                actual_game=True

    pygame.display.update()  # Update the display with the current state of the game
    clock.tick(fps)  # Maintain the FPS

