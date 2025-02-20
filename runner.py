import pygame #library
import sys
import time

import tictactoe as ttt
#initial state for pygame and select size for dispaly
pygame.init()
size = width, height = 600, 400

# Colors for display and init for front
black = (0, 0, 0)
white = (255, 255, 255)
screen = pygame.display.set_mode(size)
mediumFont = pygame.font.Font(None, 28)
largeFont = pygame.font.Font(None, 40)
moveFont = pygame.font.Font(None, 60)

#Initializing variables for user choice, the game board, and a flag indicating whether it's the AI's turn.
user = None
board = ttt.initial_state()
ai_turn = False

#loop for game
while True:

    #Handling Pygame events. If the user clicks the close button, the program exits.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    # اعبي الشاشة لون اسود
    screen.fill(black)

    # Let user choose a player.
    if user is None: #عشان اا اليوزر اذا ما اختار اكس او اوو فيخليه يختار

        # Draw title الريكت عشان العنوان اللي بالنص
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed() #بستقبل يسار او يمين او بالنص ع الفارة
        if click == 1: #اذا كبست الفارة من اليسار معناها رح تكزن الكليك 1 واذا كبست من اليمين معناها بتكون 0
            mouse = pygame.mouse.get_pos() #بستقبل الضغطة
            if playXButton.collidepoint(mouse): #اذا اليوزر كبس ع زر الاكس
                time.sleep(0.2) #الوقت المستغرق لحتى يفكر وهو بلعب
                user = ttt.X #معناه اليوزر رح يلعي ك اكس والوكيل بلعب ب او
            elif playOButton.collidepoint(mouse): #العكس
                time.sleep(0.2)
                user = ttt.O

    else:

        # Draw game board
        tile_size = 80 # حجم الهيكل المربع المقسوم ل 9 أجزاء
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)#الرقم الاخير هو غلظ كل مستطيل

                if board[i][j] != ttt.EMPTY: #لما أجي العب ب اكس او اووووو يتحكم بالخط
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        # Show title
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            title = f"Play as {user}"
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False

    pygame.display.flip()
