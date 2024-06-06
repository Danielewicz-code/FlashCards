import random

class CardEntry:
    def __init__(self, question, answer, category) -> None:
        self.answer = answer
        self.question = question
        self.category = category

    def show_question(self):
        print(f"Question: {self.question}")
        input("Press enter to show the answer.")

    def show_answer(self):
        print(f"Answer: {self.answer}.")
        input("Press enter to continue...")

    def __str__(self) -> str:
        return f"Question: {self.question}\nAnswer: {self.answer}\nCategory: {self.category}"

class Deck:
    def __init__(self, name) -> None:
        self.deck_name = name
        self.cards = []

    def add_card(self, question, answer, category):
        card = CardEntry(question, answer, category)
        self.cards.append(card)
        print("New card added.")

    def del_flashcard(self, key):
        self.cards = [card for card in self.cards if card.question != key]

    def see_cards(self):
        for i, card in enumerate(self.cards):
            print(f"\nIndex: {i}")
            print(card)
    
    def get_random_card(self):
        return random.choice(self.cards)

class Session:
    def __init__(self, deck) -> None:
        self.deck = deck
        self.current_card = None
        self.correct = 0
        self.incorrect = 0

    def start_session(self):
        print(f"Starting session with the deck: {self.deck.deck_name}")
        random.shuffle(self.deck.cards)

    def next_card(self):
        if self.deck.cards:
            self.current_card = self.deck.get_random_card()
            self.current_card.show_question()
            self.current_card.show_answer()

    def points(self, correct):
        if correct:
            self.correct += 1
        else:
            self.incorrect += 1

    def summary(self):
        print(f"The session is over. Correct: {self.correct}, Incorrect: {self.incorrect}")

class User:
    def __init__(self, name) -> None:
        self.name = name 
        self.decks = []
        self.history = []

    def add_deck(self, deck):
        self.decks.append(deck)
        print(f"The {deck.deck_name} deck added to user {self.name}")

    def remove_deck(self, key):
        self.decks = [deck for deck in self.decks if key != deck.deck_name]

    def start_new_session(self, deck_name):
        deck = next((d for d in self.decks if d.deck_name == deck_name), None)
        if deck:
            session = Session(deck)
            self.history.append(session)
            session.start_session()
            return session
        else:
            raise ValueError("Deck name was not found")

    def view_history(self):
        for i, session in enumerate(self.history):
            print(f"Session {i + 1}\nDeck: {session.deck.deck_name}, Correct: {session.correct}, Incorrect: {session.incorrect}")

class FlashCardSimulator:
    def __init__(self, user_name) -> None:
        self.user = User(user_name)

    def create_deck(self, d_name):
        deck = Deck(d_name)
        self.user.add_deck(deck)
        return deck
    
    def add_flashcard_to_deck(self, deck_name, question, answer, category):
        deck = next((d for d in self.user.decks if d.deck_name == deck_name), None)
        if deck:
            deck.add_card(question, answer, category)
        else:
            raise ValueError("Deck not found")
        
    def start_session(self, deck_name):
        return self.user.start_new_session(deck_name)

    def view_decks(self):
        for deck in self.user.decks:
            print(f"Deck: {deck.deck_name}")
            deck.see_cards()

    def view_history(self):
        self.user.view_history()

# Example usage
simulator = FlashCardSimulator("John Doe")
geo_deck = simulator.create_deck("Geography")
simulator.add_flashcard_to_deck("Geography", "What is the capital of France?", "Paris", "Geography")
simulator.add_flashcard_to_deck("Geography", "What is the largest desert in the world?", "Sahara", "Geography")

math_deck = simulator.create_deck("Math")
simulator.add_flashcard_to_deck("Math", "What is 2 + 2?", "4", "Math")
simulator.add_flashcard_to_deck("Math", "What is the square root of 16?", "4", "Math")

simulator.view_decks()

session = simulator.start_session("Geography")
session.next_card()
session.points(correct=True)
session.next_card()
session.points(correct=False)
session.summary()

simulator.view_history()

