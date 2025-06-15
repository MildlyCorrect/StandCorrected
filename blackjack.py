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
    return random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11])

def get_hand_type(c1, c2):
    if c1 == c2:
        return "pair"
    elif 11 in (c1, c2) and c1 + c2 <= 21:
        return "soft"
    else:
        return "hard"

def get_correct_move(c1, c2, dealer_upcard):
    hand_type = get_hand_type(c1, c2)
    total = c1 + c2

    if hand_type == "pair":
        return pair_strategy.get((c1, dealer_upcard), 'H')
    elif hand_type == "soft":
        return soft_strategy.get((total, dealer_upcard), 'H')
    else:
        if (total, dealer_upcard) in surrender_strategy:
            return 'R'
        return hard_strategy.get((total, dealer_upcard), 'H')

def play_hand():
    global total_hands, correct_moves, incorrect_moves

    dealer_upcard = draw_card()
    player_card1 = draw_card()
    player_card2 = draw_card()

    display1 = display_card(player_card1)
    display2 = display_card(player_card2)
    hand_display = display1 + display2

    print(f"\nDealer shows: {display_card(dealer_upcard)}")
    print(f"Your hand: {hand_display}")

    move = input("Your move (H/S/D/P/R/Q): ").upper().strip()
    if move == 'Q':
        return 'QUIT'

    correct_move = get_correct_move(player_card1, player_card2, dealer_upcard)

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

    total_hands = 0
    correct_moves = 0
    incorrect_moves = 0

    while True:
        result = play_hand()
        if result == 'QUIT':
            break

    print("\n📊 Session Summary:")
    print(f"• Hands played:    {total_hands}")
    print(f"• Correct moves:   {correct_moves}")
    print(f"• Incorrect moves: {incorrect_moves}")
    if total_hands > 0:
        print(f"• Accuracy:        {round((correct_moves / total_hands) * 100)}%")
    print("\n👋 Thanks for training with StandCorrected!")
