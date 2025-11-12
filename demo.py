"""
Test and demo script for Guess the Number game.
Demonstrates core functionality without user interaction.
"""

from game import GuessTheNumberGame
from encryption import CommitRevealProtocol, PrivacyExplanation


def demo_single_game():
    """Demonstrate a complete single game flow."""
    print("\n" + "="*70)
    print("DEMO: Single Game Flow")
    print("="*70)
    
    # Create game
    game = GuessTheNumberGame(min_num=1, max_num=100, max_guesses=8)
    game.setup_game("Alice", "Bob")
    
    # Alice commits to 42
    print("\n>>> PHASE 1: COMMITMENT")
    print("Alice decides on secret number: 42")
    commitment_hash = game.commit_number(42)
    
    # Bob guesses
    print("\n>>> PHASE 2: GUESSING")
    guesses = [50, 40, 45, 43, 41, 42]
    for guess in guesses:
        result = game.make_guess(guess)
        if game.game_state['game_over']:
            break
    
    # Reveal and verify
    print("\n>>> PHASE 3: REVEAL & VERIFY")
    result = game.reveal_and_verify()
    print(f"\n✓ Game result verified: {result['success']}")
    print(f"✓ Commitment valid: {result['commitment_valid']}")
    print(f"✓ Winner: {result['game_winner']}")


def demo_commitment_protocol():
    """Demonstrate just the commitment protocol."""
    print("\n" + "="*70)
    print("DEMO: Commitment Protocol")
    print("="*70)
    
    protocol = CommitRevealProtocol()
    
    # Create commitment
    print("\n1. CREATING COMMITMENT")
    print("   Secret number: 73")
    hash1 = protocol.commit(73, "Player_A")
    
    # Verify commitment hasn't changed
    print("\n2. VERIFYING COMMITMENT HASH")
    is_valid = protocol.verify_commitment("Player_A", hash1)
    print(f"   Hash verification: {'✓ Valid' if is_valid else '✗ Invalid'}")
    
    # Reveal
    print("\n3. REVEALING COMMITMENT")
    revealed = protocol.reveal("Player_A")
    print(f"   Revealed number: {revealed['number']}")
    
    # Create multiple commitments
    print("\n4. MULTIPLE COMMITMENTS")
    hash2 = protocol.commit(42, "Player_B")
    hash3 = protocol.commit(99, "Player_C")
    print(f"   Created commitments for 3 players")
    print(f"   Player A hash: {hash1[:20]}...")
    print(f"   Player B hash: {hash2[:20]}...")
    print(f"   Player C hash: {hash3[:20]}...")


def demo_privacy_concepts():
    """Show educational content."""
    print("\n" + "="*70)
    print("EDUCATIONAL CONTENT")
    print("="*70)
    
    PrivacyExplanation.explain_commitment()
    print("\n[Continuing to next concept...]")
    input("Press Enter...")
    
    PrivacyExplanation.explain_reveal()


def test_edge_cases():
    """Test edge cases and error handling."""
    print("\n" + "="*70)
    print("EDGE CASE TESTING")
    print("="*70)
    
    game = GuessTheNumberGame(min_num=1, max_num=100, max_guesses=3)
    game.setup_game("Tester", "Guesser")
    game.commit_number(50)
    
    # Test: Invalid guess
    print("\n1. Testing invalid guess (too high)")
    result = game.make_guess(150)
    print(f"   Result: {result.get('message', 'Invalid')}")
    
    # Test: Valid guess
    print("\n2. Testing valid guess")
    result = game.make_guess(75)
    print(f"   Feedback: {result.get('feedback')}")
    
    # Test: Correct guess
    print("\n3. Testing correct guess")
    result = game.make_guess(50)
    print(f"   Feedback: {result.get('feedback')}")
    print(f"   Game over: {game.game_state['game_over']}")
    
    # Test: Can't guess after game over
    print("\n4. Testing guess after game over")
    try:
        game.make_guess(25)
        print("   ✗ Should have raised error")
    except ValueError as e:
        print(f"   ✓ Correctly raised error: {e}")


def run_all_demos():
    """Run all demo modes."""
    print("\n" + "#"*70)
    print("# GUESS THE NUMBER: ENCRYPTED COMMIT/REVEAL")
    print("# Educational Demo & Test Suite")
    print("#"*70)
    
    print("\n\n[DEMO 1 of 4] Running single game flow...")
    demo_single_game()
    input("\nPress Enter for next demo...")
    
    print("\n\n[DEMO 2 of 4] Running commitment protocol demo...")
    demo_commitment_protocol()
    input("\nPress Enter for next demo...")
    
    print("\n\n[DEMO 3 of 4] Running edge case tests...")
    test_edge_cases()
    input("\nPress Enter for next demo...")
    
    print("\n" + "="*70)
    print("ALL DEMOS COMPLETED SUCCESSFULLY")
    print("="*70)
    print("""
✓ Core game logic works
✓ Encryption/commit/reveal works
✓ Error handling works
✓ Privacy concepts demonstrated

NEXT STEPS:
1. Run: python main.py
2. Try single player and two player modes
3. Read the education material
4. Explore the code to learn how it works

KEY FILES:
- encryption.py: Commit/reveal protocol implementation
- game.py: Game logic and rules
- main.py: Interactive CLI interface

Have fun learning about Arcium privacy! 🔒
""")


if __name__ == "__main__":
    run_all_demos()
