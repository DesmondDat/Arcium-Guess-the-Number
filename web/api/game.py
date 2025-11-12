"""
Game logic for "Guess the Number with Encrypted Commit/Reveal"
Demonstrates privacy-preserving game mechanics using Arcium principles.
"""

from encryption import CommitRevealProtocol, PrivacyExplanation
import random


class GuessTheNumberGame:
    """
    A privacy-preserving number guessing game using commit/reveal.
    
    GAME FLOW:
    1. Player A commits to a secret number (encrypted)
    2. Player B makes guesses (no peeking at commitment)
    3. Each guess gets feedback (hot/cold)
    4. After guesses, Player A reveals commitment
    5. Verify Player A was honest (commitment hash matches)
    """
    
    def __init__(self, min_num=1, max_num=100, max_guesses=10):
        self.min_num = min_num
        self.max_num = max_num
        self.max_guesses = max_guesses
        self.protocol = CommitRevealProtocol()
        self.game_state = {
            'phase': 'setup',
            'committer': None,
            'guesser': None,
            'commitment_hash': None,
            'secret_number': None,
            'guesses': [],
            'game_over': False,
            'winner': None
        }
    
    def setup_game(self, committer_name: str, guesser_name: str):
        """Initialize game with two players."""
        self.game_state['committer'] = committer_name
        self.game_state['guesser'] = guesser_name
        self.game_state['phase'] = 'commitment'
    
    def commit_number(self, secret_number: int) -> str:
        """
        COMMITMENT PHASE:
        Player secretly commits to their number using encryption.
        """
        if not (self.min_num <= secret_number <= self.max_num):
            raise ValueError(f"Number must be between {self.min_num} and {self.max_num}")
        
        self.game_state['secret_number'] = secret_number
        
        # Create encrypted commitment
        commitment_hash = self.protocol.commit(secret_number, self.game_state['committer'])
        self.game_state['commitment_hash'] = commitment_hash
        self.game_state['phase'] = 'guessing'
        
        return commitment_hash
    
    def make_guess(self, guess: int) -> dict:
        """
        GUESSING PHASE:
        Guesser makes a guess and gets feedback.
        The commitment remains encrypted during this phase.
        """
        if self.game_state['phase'] != 'guessing':
            raise ValueError("Game is not in guessing phase")
        
        if guess < self.min_num or guess > self.max_num:
            return {
                'valid': False,
                'message': f"Guess must be between {self.min_num} and {self.max_num}"
            }
        
        secret = self.game_state['secret_number']
        self.game_state['guesses'].append(guess)
        
        # Provide feedback (hot/cold)
        if guess == secret:
            feedback = "🎯 CORRECT!"
            self.game_state['game_over'] = True
            self.game_state['winner'] = self.game_state['guesser']
        elif abs(guess - secret) <= 5:
            feedback = "🔥 Very close!"
        elif abs(guess - secret) <= 15:
            feedback = "🌡️ Getting warmer"
        elif abs(guess - secret) <= 30:
            feedback = "🧊 Getting colder"
        else:
            feedback = "❄️ Very cold"
        
        result = {
            'valid': True,
            'guess': guess,
            'feedback': feedback,
            'attempt': len(self.game_state['guesses']),
            'remaining': self.max_guesses - len(self.game_state['guesses'])
        }
        
        if len(self.game_state['guesses']) >= self.max_guesses:
            self.game_state['game_over'] = True
            self.game_state['phase'] = 'reveal'
        
        return result
    
    def reveal_and_verify(self) -> dict:
        """
        REVEAL PHASE:
        Reveal the encrypted commitment and verify honesty.
        Show Arcium's privacy model in action.
        """
        if not self.game_state['game_over']:
            return {
                'success': False,
                'message': 'Game still in progress'
            }
        
        # Reveal the commitment
        revealed = self.protocol.reveal(self.game_state['committer'])
        
        # Verify commitment integrity
        original_hash = self.game_state['commitment_hash']
        is_valid = self.protocol.verify_commitment(
            self.game_state['committer'],
            original_hash
        )
        
        # Calculate game result
        secret = revealed['number']
        guesses_made = len(self.game_state['guesses'])
        
        if secret in self.game_state['guesses']:
            position = self.game_state['guesses'].index(secret) + 1
            result_msg = f"✓ FOUND in {position} guesses!"
        else:
            result_msg = f"✗ Not found in {guesses_made} guesses. Secret was {secret}"
        
        result = {
            'success': True,
            'secret_number': secret,
            'commitment_valid': is_valid,
            'guesses_made': guesses_made,
            'result': result_msg,
            'game_winner': self.game_state['winner'],
            'timestamp': revealed['timestamp']
        }
        
        return result
    
    def get_game_stats(self) -> dict:
        """Get current game statistics."""
        return {
            'phase': self.game_state['phase'],
            'guesses_made': len(self.game_state['guesses']),
            'guesses_remaining': max(0, self.max_guesses - len(self.game_state['guesses'])),
            'game_over': self.game_state['game_over'],
            'recent_guesses': self.game_state['guesses'][-5:] if self.game_state['guesses'] else []
        }
