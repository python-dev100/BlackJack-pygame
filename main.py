import pygame
import sqlite3
from random import randint
from datetime import datetime

pygame.init()

window = pygame.display.set_mode((800, 600))

font = pygame.font.Font("GOTHIC.ttf", 30)

pygame.display.set_caption("BlackJack!")
pygame.display.set_icon(pygame.image.load("icon.png"))


class Button:
    def __init__(self, x, y, width, height, text, outline=None, outline_size=2, color=(0, 0, 60)):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.outline = outline
        self.outline_size = outline_size
    def draw(self):
        if self.outline:
            pygame.draw.rect(window, (self.outline), (self.x - self.outline_size, self.y - self.outline_size, self.width + self.outline_size * 2, self.height + self.outline_size * 2))
        pygame.draw.rect(window, (0, 0, 60), (self.x, self.y, self.width, self.height), 0)
        button_text = font.render(self.text, True, (255, 255, 255))
        window.blit(button_text, (self.x + (self.width / 2 - button_text.get_width() / 2), self.y + (self.height / 2 - button_text.get_height() / 2)))
    def is_over(self, coordinates):
        return coordinates[0] > self.x and coordinates[0] < self.x + self.width and coordinates[1] > self.y and coordinates[1] < self.y + self.height

input_inactive = (0, 0, 60)
input_active = (60, 60, 255)

card_vals = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
number_card_vals = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
card_suits = ["clubs", "diamonds", "hearts", "spades"]

there_is_money = True

conn = sqlite3.connect("data.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS money (money INTEGER, date TEXT, new INTEGER)")
cur.execute("SELECT new FROM money")
new = cur.fetchall()
if new == []:
    cur.execute("INSERT INTO money VALUES (5000, ?, 1)", (str(datetime.now())[:10],))
    money = 10000
    cur.execute("UPDATE money SET money=?", (money,))
else:
    cur.execute("SELECT money FROM money")
    money = cur.fetchall()[0][0]
cur.execute("UPDATE money SET new=0")
cur.execute("SELECT date FROM money")
if str(datetime.now())[:10] != cur.fetchall()[0][0]:
    money += 5000
conn.commit()
conn.close()


def update_money():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("UPDATE money SET money=?", (money,))
    conn.commit()
    conn.close()

def cards(playing):
    x_reset = 80
    x = x_reset
    y = 400
    x_incr = 80
    y_incr = 1
    y_incr2 = 160
    for card in player_cards:
        if x >= 700:
            x = x_reset
            y -= y_incr2
        window.blit(card, (x, y))
        x += x_incr
        y += y_incr
    x = x_reset
    window.blit(dealer_cards[0], (160, 0))
    if playing:
        window.blit(pygame.image.load("back.png"), (500, y_incr))
    else:
        window.blit(dealer_cards[1], (500, y_incr))

def select_bet():
    x_reset = 160
    width = 160
    x = x_reset
    height = 100
    y = 80
    bet_text = font.render("Select your bet:", True, (255, 255, 255))
    window.blit(bet_text, (400 - bet_text.get_width() / 2, 30))
    global bets
    bets = []
    for i in range(10):
        bets.append(Button(x, y, width, height, str((i+1) * 100), color=(20, 20, 80), outline=(0, 0, 255)))
        if i == 9:
            bets[i].width *= 3
        bets[i].draw()
        x += width
        if x > 600:
            x = x_reset
            y += height
    
def in_bets():
    for button in bets:
        if button.is_over(pygame.mouse.get_pos()):
            return button.text
    return
        
def no_money():
    no_money_text = font.render("You don't have enough money for this bet", True, (255, 255, 255))
    nx = 400 - no_money_text.get_width() / 2
    window.blit(no_money_text, (nx, 30))
    x_space = 60
    global ok
    ok = Button(nx + x_space, 200, (no_money_text.get_width() - x_space) - nx, 80, "OK")
    ok.draw()

def bet_screen(there_is_money):
    if there_is_money:
        select_bet()
    else:
        no_money()


def show_money():
    money_font = pygame.font.Font("GOTHIC.ttf", 20)
    if money > 0 or game_on:
        money_text = money_font.render("You have $" + str(money), True, (255, 255, 255))
    else:
        money_text = money_font.render("Bankrupt!", True, (255, 255, 255))
    window.blit(money_text, (800 - money_text.get_width(), 0))

hit = Button(370, 300, 100, 50, "Hit")
stand = Button(570, 300, 100, 50, "Stand")

new_game = Button(160, 140, 300, 40, "Bet!")
exit_game = Button(160, 200, 300, 40, "Exit")

running = True
game_on = False
menu_on = True
gameover = False
played = False

while running:
    window.fill((0, 0, 0))
    show_money()
    update_money()
    if game_on:
        if not played:
            player_cards = [None, None]
            player_vals = [None, None]
            player_strings = [None, None]
            dealer_cards = [None, None]
            dealer_vals = [None, None]
            dealer_strings = [None, None]
            game_text = font.render("What's your next move?", True, (255, 255, 255))
            for i in range(4):
                if i < 2:
                    while player_cards[int(not bool(i))] == player_cards[i] or not player_cards[i]:
                        n = (randint(0, len(card_vals) - 1), randint(0, len(card_suits) - 1))
                        player_strings[i] = str(card_vals[n[0]]) + " of " + card_suits[n[1]] + ".png"
                        player_cards[i] = pygame.image.load(player_strings[i])
                        player_vals[i] = number_card_vals[n[0]]
                else:
                    while dealer_cards[i % 2] in player_cards or dealer_cards[int(not bool(i % 2))] == dealer_cards[i % 2] or not dealer_cards[i % 2]:
                        n = (randint(0, len(card_vals) - 1), randint(0, len(card_suits) - 1))
                        dealer_strings[i % 2] = str(card_vals[n[0]]) + " of " + card_suits[n[1]] + ".png"
                        dealer_cards[i % 2] = pygame.image.load(dealer_strings[i % 2])
                        dealer_vals[i % 2] = number_card_vals[n[0]]
            if sum(dealer_vals) > 21:
                dealer_vals[0] -= 10
            played = True
        else:
            cards(not gameover)
            if not gameover:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if hit.is_over(pygame.mouse.get_pos()):
                                n = (randint(0, len(card_vals) - 1), randint(0, len(card_suits) - 1))
                                while str(card_vals[n[0]]) + " of " + card_suits[n[1]] + ".png" in player_strings:
                                    n = (randint(0, len(card_vals) - 1), randint(0, len(card_suits) - 1))
                                player_cards.append(pygame.image.load(str(card_vals[n[0]]) + " of " + card_suits[n[1]] + ".png"))
                                player_vals.append(number_card_vals[n[0]])
                                player_strings.append(str(card_vals[n[0]]) + " of " + card_suits[n[1]] + ".png")
                            if stand.is_over(pygame.mouse.get_pos()):
                                gameover = True
                    if sum(player_vals) == 21:
                        gameover = True
                    if sum(player_vals) > 21:
                        while 11 in player_vals:
                            player_vals[player_vals.index(11)] -= 10
                        if sum(player_vals) > 21:
                            gameover = True
                    
                window.blit(game_text, (350, 200))
                hit.draw()
                stand.draw()    
            else:
                if sum(player_vals) == 21:
                    game_text = font.render("BlackJack!", True, (255, 255, 255))
                    take = bet * 2
                elif sum(player_vals) > 21:
                    game_text = font.render("Busted...", True, (255, 255, 255))
                    take = 0
                elif sum(player_vals) == sum(dealer_vals):
                    game_text = font.render("Push", True, (255, 255, 255))
                    take = bet
                elif sum(player_vals) > sum(dealer_vals):
                    game_text = font.render("You Win!", True, (255, 255, 255))
                    take = bet * 2
                elif sum(player_vals) < sum(dealer_vals):
                    game_text = font.render("You Lose...", True, (255, 255, 255))
                    take = 0
                window.blit(game_text, (400 + game_text.get_width() / 2, 200))
                cont = Button(370, 300, 300, 50, "Continue")
                cont.draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        money += take
                        running = False
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if cont.is_over(pygame.mouse.get_pos()):
                            money += take
                            game_on = False        
    else:
        if menu_on:
            new_game.draw()
            exit_game.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:    
                        if new_game.is_over(pygame.mouse.get_pos()):
                            there_is_money = True
                            menu_on = False
                        if exit_game.is_over(pygame.mouse.get_pos()):
                            running = False
                            pygame.quit()
        else:
            bet_screen(there_is_money)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if in_bets() and there_is_money:
                            bet = int(in_bets())
                            money -= bet
                            if money < 0:
                                money += bet
                                there_is_money = False
                            else:
                                gameover = False
                                game_on = True
                                menu_on = True
                                played = False
                        elif not there_is_money:
                            if ok.is_over(pygame.mouse.get_pos()):
                                menu_on = True

    pygame.display.update()
