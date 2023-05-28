import os
import numpy as np

M = 3  # Maximum sticks a player can choose
N = 10  # Initial number of sticks in the pile
alpha = 0.5  # Learning rate
file_name = "NIM.txt"


def initialize_array():
    return np.zeros((M, N))


def load_q():
    if os.path.exists(file_name):
        return np.loadtxt(file_name)
    else:
        return initialize_array()


def save_q(Q):
    np.savetxt(file_name, Q)
    print("Q-values saved to file.")


def play_game(Q, Won, Lost):
    sticks_left = N
    computer_turn = True
    print("Welcome to NIM!")
    while sticks_left > 0:
        print(f"Remaining Sticks: {sticks_left}")
        if computer_turn:
            if sticks_left > M:
                sticks_to_take = choose_move(Q, sticks_left, Won, Lost)
            else:
                sticks_to_take = sticks_left
            print(f"Computer took {sticks_to_take} sticks.")
            sticks_left -= sticks_to_take
        else:
            sticks_to_take = get_user_move(sticks_left)
            sticks_left -= sticks_to_take
        computer_turn = not computer_turn

    if computer_turn:
        print("You won!!!")
        Q += Lost
    else:
        print("Computer won.")
        Q += Won

    return Q


def get_user_move(sticks_left):
    while True:
        sticks_to_take = int(input(f"How many sticks would you like to take (1-{min(M, sticks_left)})? "))
        if 1 <= sticks_to_take <= M and sticks_to_take <= sticks_left:
            return sticks_to_take
        print("Invalid input. Try again.")


def choose_move(Q, sticks_left, Won, Lost):
    max_index = np.argmax(Q[:, sticks_left - 1])
    Won[max_index, sticks_left - 1] += alpha
    Lost[max_index, sticks_left - 1] -= alpha
    return max_index + 1


Q = load_q()
Won = initialize_array()
Lost = initialize_array()

play_again = True
while play_again:
    Q = play_game(Q, Won, Lost)
    response = input("Play again? (y/n): ").strip().lower()
    play_again = response == "y"
    save_q(Q)



        
