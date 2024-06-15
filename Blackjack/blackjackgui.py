"""
File: blackjackgui.py
Author: Alex Gill
This program allows the user to play a game of blackjack in a
graphical user interface.
"""
from tkinter import *
from tkinter import ttk
from blackjack import Blackjack
import pathlib

# --- Global variables ---
WIDTH = 550         # The width of the window
CARD_SPACING = 5    # The spacing between the cards
SPACING = 10        # The spacing between widgets
HAND_PADDING = 10   # The padding around the cards
PADDING = 20        # The padding around the window

# --- Global variables ---
message = None              # Message to display in the message label
blackjack = None            # The Blackjack game object
hit_button = None           # The hit button
stay_button = None          # The stay button
play_again_button = None    # The play again button
player_card_labels = None   # Labels with pictures of the player's cards
dealer_card_labels = None   # Labels with pictures of the dealer's cards

def start_game(dealer_frame, player_frame):
    """Starts a new game of Blackjack."""
    global blackjack
    global dealer_card_labels
    global player_card_labels
    global message
    global stay_button
    global hit_button

    # Remove already displayed dealer cards
    if dealer_card_labels != None:
        for label in dealer_card_labels:
            label.grid_remove()

    # Remove already displayed player cards
    if player_card_labels != None:
        for label in player_card_labels:
            label.grid_remove()

    # Initialize the game
    blackjack = Blackjack()

    # Create and display the list of the dealer's cards
    dealer_card_labels = []
    for i in range(len(blackjack.dealer.cards)):
        if i == 0: blackjack.dealer.cards[i].flip()
        dealer_card_labels.append(ttk.Label(dealer_frame))
        display_card(blackjack.dealer.cards[i], dealer_card_labels[i])
        dealer_card_labels[i].grid(row=0, column=i, \
            padx=(0 if i == 0 else CARD_SPACING, 0))

    # Create and display the list of the player's cards
    player_card_labels = []
    for i in range(len(blackjack.player.cards)):
        blackjack.player.cards[i].flip()
        player_card_labels.append(ttk.Label(player_frame))
        display_card(blackjack.player.cards[i], player_card_labels[i])
        player_card_labels[i].grid(row=0, column=i, \
            padx=(0 if i == 0 else CARD_SPACING, 0))

    # Display ther player's number of points in the message
    message.set(str(blackjack.player.get_points()) + ' points')

    # Remove the play again button and display the hit and stay buttons
    play_again_button.grid_remove()
    stay_button.configure(state=NORMAL)
    stay_button.grid(row=3, column=0, padx=(0, SPACING), sticky=E)
    hit_button.configure(state=NORMAL)
    hit_button.grid(row=3, column=1, sticky=W)

    # End the game immediately if the player has blackjack
    if blackjack.player.get_points() == 21:
        end_game(blackjack)


def end_game(blackjack):
    """Perform the steps to end the game and show the results."""
    global message
    global hit_button
    global stay_button
    global play_again_button

    # Disable the buttons
    hit_button.configure(state=DISABLED)
    stay_button.configure(state=DISABLED)

    # End the game prematurely if player busted
    player_points = blackjack.player.get_points()
    if player_points > 21:
        message.set('You bust and you lose')
    # End the game prematurely if player got blackjack
    elif player_points == 21 and len(blackjack.player.cards) == 2:
        message.set('Blackjack! You win')
    else:
        # Dealer hits
        blackjack.dealer.hit(blackjack.deck)

        # Flip over and display the dealer's hidden card
        blackjack.dealer.cards[1].flip()
        display_card(blackjack.dealer.cards[1], dealer_card_labels[1])
        dealer_card_labels[1].grid(row=0, column=1)

        # Display the rest of the dealer's cards
        for i in range(2, len(blackjack.dealer.cards)):
            blackjack.dealer.cards[i].flip()
            dealer_card_labels.append(ttk.Label(dealer_card_labels[0].master))
            display_card(blackjack.dealer.cards[i], dealer_card_labels[i])
            col = len(dealer_card_labels) - 1
            dealer_card_labels[i].grid(row=0, column=col, \
                padx=(CARD_SPACING, 0))
        
        # Determine the outcome
        dealer_points = blackjack.dealer.get_points()
        if dealer_points > 21:
            message.set('Dealer busts and you win')
        elif dealer_points > player_points:
            message.set('Dealer wins')
        elif dealer_points < player_points:
            message.set('You win')
        elif dealer_points == player_points:
            if blackjack.player.has_blackjack() and \
                not blackjack.dealer.has_blackjack():
                message.set('You win')
            elif not blackjack.player.has_blackjack() and \
                    blackjack.dealer.has_blackjack():
                message.set('Dealer wins')
            else:
                message.set('There is a tie')

    # Replace the hit and stay buttons with a play again button
    hit_button.grid_remove()
    stay_button.grid_remove()
    play_again_button.grid(row=3, column=0, columnspan=2)


def display_card(card, widget):
    """Displays an image of a card on a widget."""
    # Do nothing if no card was passed
    if card == None:
        return

    # Convert the card to the corresponding filename and path
    if card.faceup:
        filename = str(card.rank) + card.suit[0].lower() + '.gif'
    else:
        filename = 'b.gif'
    path = str(pathlib.Path(__file__).parent.resolve()) + '\\DECK\\' + filename

    # Set the image field of the widget to the corresponding image
    imageobj = PhotoImage(file=path)
    widget.configure(image=imageobj)
    widget.photo = imageobj


def hit(blackjack, player_frame):
    """Adds a new card to the player's hand and displays it."""
    global player_card_labels

    # Hit and flip the new card right-side up
    blackjack.player.hit(blackjack.deck.deal())
    blackjack.player.cards[-1].flip()

    # Add a new label and display an image on it.
    player_card_labels.append(ttk.Label(player_frame))
    display_card(blackjack.player.cards[-1], player_card_labels[-1])
    col = len(blackjack.player.cards) - 1
    player_card_labels[-1].grid(row=0, column=col, padx=(CARD_SPACING, 0))
    global message
    if blackjack.player.get_points() > 21:
        message.set('You busted')
        end_game(blackjack)
    else:
        message.set(str(blackjack.player.get_points()) + ' points')


def stay(blackjack):
    """To be called when the user clicks the stay button."""
    end_game(blackjack)


def set_window_resize(window):
    """Centers the window and prevents it from being resized past its
    default size."""
    window.update_idletasks()
    width = WIDTH
    frm_width = window.winfo_rootx() - window.winfo_x()
    win_width = width + frm_width * 2
    height = window.winfo_height()
    tlb_height = window.winfo_rooty() - window.winfo_y()
    win_height = height + tlb_height + frm_width
    x = window.winfo_screenwidth() // 2 - win_width // 2
    y = window.winfo_screenheight() // 2 - win_height // 2
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    window.minsize(width=width, height=height)


def main():
    global message
    global blackjack
    global hit_button
    global stay_button
    global play_again_button

    # Create the root
    root = Tk()
    root.title('Blackjack')
    root.configure(padx=PADDING, pady=PADDING)

    # Set the resize configuration of the columns and rows
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)
    root.rowconfigure(3, weight=1)

    # Create a frame for the dealer's cards
    dealer_frame = ttk.LabelFrame(root, text='Dealer', padding=HAND_PADDING)
    dealer_frame.grid(row=0, column=0, columnspan=2, pady=(0, SPACING))

    # Create a frame for the player's cards
    player_frame = ttk.LabelFrame(root, text='You', padding=HAND_PADDING)
    player_frame.grid(row=1, column=0, columnspan=2, pady=(0, SPACING))

    # Create the message label
    message = StringVar(root)
    message_label = ttk.Label(root, textvariable=message)
    message_label.grid(row=2, column=0, columnspan=2, pady=(0, SPACING))

    # Create the stay button
    stay_button = ttk.Button(root, text='Stay', \
        command=lambda: stay(blackjack))

    # Create the hit button
    hit_button = ttk.Button(root, text='Hit', \
        command=lambda: hit(blackjack, player_frame))

    # Create the play again button
    play_again_button = ttk.Button(root, text='Play again', \
        command=lambda: start_game(dealer_frame, player_frame))

    # Start the game
    start_game(dealer_frame, player_frame)

    # Set the root window's resize properties
    set_window_resize(root)
    
    # Start the event loop
    root.mainloop()


if __name__ == '__main__':
    main()