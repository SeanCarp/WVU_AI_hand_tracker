import random as rand
import time

def game_update(computer, player):
    # CHECK IF GAME OVER
    if sum(computer) == 0 or sum(player) == 0:
        print("GAME OVER!!")
        return False
    
    print("Computer")
    print(f'{computer[0]}   {computer[1]}\n')

    print("Player")
    print(f'{player[0]}   {player[1]}\n')
    return True

def game_logic(attacker, defender):
    if defender == 0: # Not supposed to be able to attack that hand
        return 0

    defender += attacker
    if defender == 5:
        defender = 0
    elif defender > 5:
        defender -= 4
    return defender

# Game Loop
while(True):
    computer = [1,1]
    player = [1,1]
    while(True):

        
        # GAME UPDATE
        if not game_update(computer, player):
            break
        time.sleep(2)


        #
        #   PLAYER SIDE
        #
        ran = False
        while(not ran):
            player_hand = input("Left or Right (L/R)[Player]?").lower()
            player_attack = input("Left or Right (L/R)[Computer]?").lower()

            attacker = player[0 if player_hand == 'l' else 1]
            defender = computer[0 if player_attack == 'l' else 1]

            if not(attacker == 0 or defender == 0):
                computer[0 if player_attack == 'l' else 1] = game_logic(attacker, defender)
                ran = True

        # GAME UPDATE
        if not game_update(computer, player):
            break

        time.sleep(2)
        
        #
        #   COMPUTER SIDE
        #
        ran = False
        while(not ran):
            defender_flag = rand.randint(0,1) == 1

            attacker = computer[0 if rand.randint(0,1) == 1 else 1]
            defender = player[0 if defender_flag else 1]

            if not(attacker == 0 or defender == 0):
                player[0 if defender_flag else 1] = game_logic(attacker, defender)
                ran = True
        
