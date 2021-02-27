from random import randint

score_computer = 0
score_player = 0


def compute():
    random = randint(1,3)
    if random == 1:
        choice = 'r'
    elif random == 2:
        choice = 'p'
    else:
        choice = 's'
    return choice


def decode(choice):
    if choice == 'r':
        return 'rock'
    elif choice == 's':
        return 'scissors'
    elif choice == 'p':
        return 'paper'


def decide_winner(player, computer):
    global score_computer, score_player
    print(decode(player), 'vs',decode(computer))
    if player == computer:
        print('DRAW!')
    elif player == 'p' and computer == 's':
        print('YOU LOSE!')
        score_computer += 1
    elif player == 'p' and computer == 'r':
        print('YOU WIN!')
        score_player += 1
    elif player == 's' and computer == 'r':
        print('YOU LOSE!')
        score_computer += 1
    elif player == 's' and computer == 'p':
        print('YOU WIN!')
        score_player += 1
    elif player == 'r' and computer == 'p':
        print('YOU LOSE!')
        score_computer += 1
    elif player == 'r' and computer == 's':
        print('YOU WIN!')
        score_player += 1
    else:
        print('bug')


def is_valid_choice(choice):
    return choice == 'r' or choice == 'p' or choice == 's'


def play():
    player = input('Enter rock (r), paper (p), scissors (s) or quit (q) to stop the game:')
    if player == 'q':
        print('Thanks!  See you later!')
        return False
    if not is_valid_choice(player):
        print (player,'is not a valid choice!')
        play()
        return True
    computer = compute()
    decide_winner(player, computer)
    return True


keep_playing = True
while keep_playing:
    keep_playing = play()
    print (f'Score: player: {score_player} - computer: {score_computer}')


