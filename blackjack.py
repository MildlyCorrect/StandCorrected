import random
import os

# === Display and UI ===

def clear_screen():
    print("\033[2J\033[H", end="")

def show_banner():
    clear_screen()
    print("\n" + "=" * 50)
    print("🂡  Welcome to StandCorrected".center(50))
    print("-" * 50)
    print(" A full basic strategy blackjack trainer".center(50))
    print(" Created by MildlyCorrect".center(50))
    print("=" * 50 + "\n")
    print("▶ Respond with: H (Hit), S (Stand), D (Double), P (Split), R (Surrender), Q (Quit)")
    input("\nPress Enter to begin training...")

def display_card(value):
    if value == 11:
        return 'A'
    elif value == 10:
        return random.choice(['10', 'J', 'Q', 'K'])
    else:
        return str(value)

# === Strategy Tables ===

hard_strategy = {
    (5, d): 'H' for d in range(2, 12)
} | {
    (6, d): 'H' for d in range(2, 12)
} | {
    (7, d): 'H' for d in range(2, 12)
} | {
    (8, d): 'H' for d in range(2, 12)
} | {
    (9, d): 'D' if 3 <= d <= 6 else 'H' for d in range(2, 12)
} | {
    (10, d): 'D' if 2 <= d <= 9 else 'H' for d in range(2, 12)
} | {
    (11, d): 'D' if d != 11 else 'H' for d in range(2, 12)
} | {
    (12, d): 'S' if 4 <= d <= 6 else 'H' for d in range(2, 12)
} | {
    (13, d): 'S' if 2 <= d <= 6 else 'H' for d in range(2, 12)
} | {
    (14, d): 'S' if 2 <= d <= 6 else 'H' for d in range(2, 12)
} | {
    (15, d): 'S' if 2 <= d <= 6 else 'H' for d in range(2, 12)
} | {
    (16, d): 'S' if 2 <= d <= 6 else 'H' for d in range(2, 12)
} | {
    (17, d): 'S' for d in range(2, 12)
} | {
    (18, d): 'S' for d in range(2, 12)
} | {
    (19, d): 'S' for d in range(2, 12)
} | {
    (20, d): 'S' for d in range(2, 12)
} | {
    (21, d): 'S' for d in range(2, 12)
}

soft_strategy = {
    (13, d): 'D' if d in [5, 6] else 'H' for d in range(2, 12)
} | {
    (14, d): 'D' if d in [5, 6] else 'H' for d in range(2, 12)
} | {
    (15, d): 'D' if d in [4, 5, 6] else 'H' for d in range(2, 12)
} | {
    (16, d): 'D' if d in [4, 5, 6] else 'H' for d in range(2, 12)
} | {
    (17, d): 'D' if d in [3, 4, 5, 6] else 'H' for d in range(2, 12)
} | {
    (18, d): 'S' if d in [2, 7, 8] else ('D' if 3 <= d <= 6 else 'H') for d in range(2, 12)
} | {
    (19, d): 'S' if d != 6 else 'D' for d in range(2, 12)
} | {
    (20, d): 'S' for d in range(2, 12)
}

pair_strategy = {
    (2, d): 'P' if 2 <= d <= 7 else 'H' for d in range(2, 12)
} | {
    (3, d): 'P' if 2 <= d <= 7 else 'H' for d in range(2, 12)
} | {
    (4, d): 'P' if 5 <= d <= 6 else 'H' for d in range(2, 12)
} | {
    (5, d): 'D' if 2 <= d <= 9 else 'H' for d in range(2, 12)
} | {
    (6, d): 'P' if 2 <= d <= 6 else 'H' for d in range(2, 12)
} | {
    (7, d): 'P' if 2 <= d <= 7 else 'S' if d in [10, 11] else 'H' for d in range(2, 12)
} | {
    (8, d): 'P' for d in range(2, 12)
} | {
    (9, d): 'P' if d in [2, 3, 4, 5, 6, 8, 9] else 'S' for d in range(2, 12)
} | {
    (10, d): 'S' for d in range(2, 12)
} | {
    (11, d): 'P' for d in range(2, 12)
}

surrender_strategy = {
    (16, d): 'R' if d in [9, 10, 11] else None for d in range(2, 12)
} | {
    (15, 10): 'R'
}

# === Logic ===

def draw_card():
    return random.choice(['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'])


def card_value(card):
    if card in ['T', 'J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11
    else:
        return int(card)


def get_hand_type(c1, c2):
    v1 = card_value(c1)
    v2 = card_value(c2)

    if v1 == v2:
        return "pair"
    elif 11 in (v1, v2) and v1 + v2 <= 21:
        return "soft"
    else:
        return "hard"


def get_correct_move(c1, c2, dealer_upcard):
    v1 = card_value(c1)
    v2 = card_value(c2)
    dealer_val = card_value(dealer_upcard)

    hand_type = get_hand_type(c1, c2)
    total = v1 + v2

    if hand_type == "pair":
        return pair_strategy.get((v1, dealer_val), 'H')
    elif hand_type == "soft":
        return soft_strategy.get((total, dealer_val), 'H')
    else:
        if (total, dealer_val) in surrender_strategy:
            return 'R'
        return hard_strategy.get((total, dealer_val), 'H')


def play_hand(practice_mode):
    global total_hands, correct_moves, incorrect_moves

    dealer_upcard = draw_card()

    # Draw a player hand that matches the selected practice mode
    while True:
       c1 = draw_card()
       c2 = draw_card()
       hand_type = get_hand_type(c1, c2)


       if practice_mode == 'hard' and hand_type == 'hard':
            break
       elif practice_mode == 'soft' and hand_type == 'soft':
            break
       elif practice_mode == 'pairs' and hand_type == 'pair':
            break
       elif practice_mode == 'full':
            break



    display1 = display_card(c1)
    display2 = display_card(c2)
    hand_display = f"{display1} {display2}"

    print(f"\nDealer shows: {dealer_upcard}")
    print(f"Your hand: {hand_display}")

    print("\nWhat would you like to do?")
    print("  H - Hit")
    print("  S - Stand")
    print("  D - Double")
    print("  P - Split")
    print("  R - Surrender")
    print("  Q - Quit")

    move = input("Enter your move: ").upper().strip()

    if move == 'Q':
        return 'QUIT'

    correct_move = get_correct_move(c1, c2, dealer_upcard)

    total_hands += 1
    if move == correct_move:
        print("✅ Correct move!")
        correct_moves += 1
    else:
        print(f"❌ Incorrect. Basic strategy says to {correct_move}.")
        incorrect_moves += 1

    print(f"→ Score: {correct_moves}/{total_hands} ({round((correct_moves / total_hands) * 100)}%)")

if __name__ == "__main__":
    show_banner()

    clear_screen()
    print("Select practice mode:")
    print("1 - Full Mix")
    print("2 - Hard Hands Only")
    print("3 - Soft Hands Only")
    print("4 - Pairs Only")
    mode_choice = input("Enter choice (1–4): ").strip()

    if mode_choice == '2':
        practice_mode = 'hard'
    elif mode_choice == '3':
        practice_mode = 'soft'
    elif mode_choice == '4':
        practice_mode = 'pairs'
    else:
        practice_mode = 'full'


    total_hands = 0
    correct_moves = 0
    incorrect_moves = 0

    while True:
        result = play_hand(practice_mode)
        if result == 'QUIT':
            break

    print("\n📊 Session Summary:")
    print(f"• Hands played:    {total_hands}")
    print(f"• Correct moves:   {correct_moves}")
    print(f"• Incorrect moves: {incorrect_moves}")
    if total_hands > 0:
        print(f"• Accuracy:        {round((correct_moves / total_hands) * 100)}%")
    print("\n👋 Thanks for training with StandCorrected!")
