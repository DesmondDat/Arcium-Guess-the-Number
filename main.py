"""
Interactive CLI interface for Guess the Number with Encrypted Commit/Reveal.
Full teaching demonstration of Arcium's privacy model.
"""

from game import GuessTheNumberGame
from encryption import PrivacyExplanation
import os


class GameInterface:
    """Interactive interface for the privacy-preserving game."""
    
    def __init__(self):
        self.game = None
    
    def clear_screen(self):
        """Clear terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title):
        """Print formatted header."""
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70)
    
    def show_menu(self):
        """Show main menu."""
        self.clear_screen()
        self.print_header("GUESS THE NUMBER: Encrypted Commit/Reveal")
        print("""
This game demonstrates Arcium's privacy model through a simple game:
- One player secretly commits to a number (encrypted)
- The other player makes guesses
- After guessing, the commitment is revealed and verified

🎓 ARCIUM CONCEPTS LEARNED:
   ✓ Commitment (proving you know something without revealing it)
   ✓ Reveal (decrypting data to authorized parties)
   ✓ Verification (proving data wasn't changed)
   ✓ Privacy in computation (no peeking at encrypted data)

CHOOSE MODE:
""")
        print("1. Single Player (You guess against computer)")
        print("2. Two Player (Local game between players)")
        print("3. Learn About Arcium Privacy Model")
        print("4. Exit")
        return input("\nEnter choice (1-4): ").strip()
    
    def learn_mode(self):
        """Educational mode explaining Arcium concepts."""
        while True:
            self.clear_screen()
            self.print_header("ARCIUM PRIVACY MODEL EDUCATION")
            print("""
1. What is Commitment?
2. What is Reveal?
3. What is Verification?
4. Complete Arcium Overview
5. Back to Main Menu
""")
            choice = input("Choose (1-5): ").strip()
            
            if choice == '1':
                PrivacyExplanation.explain_commitment()
                input("\nPress Enter to continue...")
            elif choice == '2':
                PrivacyExplanation.explain_reveal()
                input("\nPress Enter to continue...")
            elif choice == '3':
                self._explain_verification()
                input("\nPress Enter to continue...")
            elif choice == '4':
                self._explain_overview()
                input("\nPress Enter to continue...")
            elif choice == '5':
                break
    
    def _explain_verification(self):
        """Explain verification concept."""
        print("\n" + "="*70)
        print("ARCIUM PRIVACY MODEL: VERIFICATION")
        print("="*70)
        print("""
✓ WHAT IS VERIFICATION?

In our game:
- Before revealing, you get a commitment HASH
- After revealing, the decrypted data creates the same hash
- If hashes match → data was never changed (verified honest)
- If hashes don't match → someone tampered (caught cheating!)

Why it matters:
- You can PROVE the data hasn't been modified
- No central authority needed - cryptography does the proving
- Arcium uses this to guarantee data integrity

In Arcium:
- Encrypted data has a cryptographic signature
- When revealed, the signature is verified
- Proves no one changed the data during processing
- Users can independently verify all computations
""")
    
    def _explain_overview(self):
        """Explain full Arcium overview."""
        print("\n" + "="*70)
        print("ARCIUM COMPLETE PRIVACY MODEL")
        print("="*70)
        print("""
🔒 THE THREE PILLARS OF ARCIUM PRIVACY:

1. ENCRYPTION (Confidentiality)
   - Data is encrypted at rest and in transit
   - Only authorized parties can decrypt
   - In our game: Your secret number is encrypted

2. COMMITMENT (Proof of Intent)
   - Prove you know something without revealing it
   - Cryptographic binding - can't change your mind later
   - In our game: You commit before guessing starts

3. VERIFICATION (Integrity)
   - Prove data hasn't been modified
   - Cryptographic signatures ensure authenticity
   - In our game: Hashes prove commitment is unchanged

🎮 HOW THE GAME DEMONSTRATES THIS:
   Step 1: Player A commits (encryption)
   Step 2: Player B guesses (sealed commitment prevents cheating)
   Step 3: Reveal & verify (proof of honesty)

This same pattern is used in Arcium for:
- Private smart contracts
- Confidential transactions
- Privacy-preserving machine learning
- Secure multi-party computation
""")
    
    def single_player_mode(self):
        """Single player game (human vs computer)."""
        self.clear_screen()
        self.print_header("SINGLE PLAYER MODE")
        print("\nYou will guess the computer's secret number")
        print("The computer's number is encrypted until the end")
        
        self.game = GuessTheNumberGame(min_num=1, max_num=100, max_guesses=10)
        
        # Computer commits to random number
        secret = __import__('random').randint(1, 100)
        commitment_hash = self.game.commit_number(secret)
        self.game.setup_game("Computer", "You")
        
        input("\n[Press Enter to start guessing...]")
        
        # Guessing loop
        while not self.game.game_state['game_over']:
            stats = self.game.get_game_stats()
            print(f"\n📊 Guesses: {stats['guesses_made']}/{self.game.max_guesses}")
            
            try:
                guess = int(input(f"\nEnter your guess ({self.game.min_num}-{self.game.max_num}): "))
                result = self.game.make_guess(guess)
                
                if not result['valid']:
                    print(f"❌ {result['message']}")
            except ValueError:
                print("❌ Please enter a valid number")
        
        # Reveal and verify
        self.game.reveal_and_verify()
        input("\n[Press Enter to continue...]")
    
    def two_player_mode(self):
        """Two player game (local multiplayer)."""
        self.clear_screen()
        self.print_header("TWO PLAYER MODE")
        
        print("\n🎮 GAME SETUP")
        player1 = input("Player 1 name (will commit to secret): ").strip() or "Player 1"
        player2 = input("Player 2 name (will guess): ").strip() or "Player 2"
        
        self.game = GuessTheNumberGame(min_num=1, max_num=100, max_guesses=10)
        self.game.setup_game(player1, player2)
        
        # Player 1 commits
        self.clear_screen()
        print(f"\n🔒 {player1}: It's your turn to commit to a secret number")
        print(f"(This will be shown on screen, but then encrypted)")
        
        while True:
            try:
                secret = int(input(f"Enter your secret number (1-100): "))
                if 1 <= secret <= 100:
                    break
                print("❌ Number must be between 1 and 100")
            except ValueError:
                print("❌ Please enter a valid number")
        
        commitment_hash = self.game.commit_number(secret)
        
        # Clear screen so guesser can't see
        input("\n[Press Enter when Player 1 has left the area...]")
        self.clear_screen()
        
        # Player 2 guesses
        print(f"\n🎯 {player2}: Time to make your guesses!")
        print(f"📝 Commitment Hash: {commitment_hash[:32]}...")
        print(f"(This hash proves your opponent committed to a number)\n")
        
        while not self.game.game_state['game_over']:
            stats = self.game.get_game_stats()
            print(f"\n📊 Guesses: {stats['guesses_made']}/{self.game.max_guesses}")
            
            try:
                guess = int(input(f"Guess {stats['guesses_made'] + 1}: "))
                result = self.game.make_guess(guess)
                
                if not result['valid']:
                    print(f"❌ {result['message']}")
            except ValueError:
                print("❌ Please enter a valid number")
        
        # Reveal and verify
        print(f"\n🔓 Time to reveal and verify!")
        self.game.reveal_and_verify()
        input("\n[Press Enter to continue...]")
    
    def run(self):
        """Main game loop."""
        while True:
            choice = self.show_menu()
            
            if choice == '1':
                self.single_player_mode()
            elif choice == '2':
                self.two_player_mode()
            elif choice == '3':
                self.learn_mode()
            elif choice == '4':
                self.clear_screen()
                print("\n👋 Thanks for learning about Arcium privacy with us!")
                print("   Remember: Privacy + Computation = Arcium\n")
                break
            else:
                print("❌ Invalid choice. Please try again.")
                input("Press Enter...")


def main():
    """Entry point."""
    interface = GameInterface()
    interface.run()


if __name__ == "__main__":
    main()
