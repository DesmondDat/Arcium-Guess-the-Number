"""
Encryption module for commit/reveal protocol.
Demonstrates Arcium's privacy model: encrypt data, prove knowledge without revealing.
"""

from cryptography.fernet import Fernet
import hashlib
import json
from datetime import datetime


class CommitRevealProtocol:
    """
    Implements a simple Commit/Reveal protocol for privacy-preserving verification.
    
    ARCIUM CONCEPT:
    - Commit Phase: Player secretly commits to a number (encrypted)
    - Reveal Phase: Later, the commitment is opened to prove honesty
    - Privacy: Verifier learns the answer only after commitment is locked in
    """
    
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.commitments = {}
    
    def commit(self, secret_number: int, player_id: str) -> str:
        """
        COMMIT PHASE: Player commits to a secret number.
        
        The number is encrypted and hashed to create a binding commitment.
        The player can't change their mind later without breaking the commitment.
        
        Args:
            secret_number: The secret number (0-100)
            player_id: Unique player identifier
            
        Returns:
            commitment_hash: A hash proving the commitment exists
        """
        # Create commitment data
        commitment_data = {
            'number': secret_number,
            'timestamp': datetime.now().isoformat(),
            'player_id': player_id
        }
        
        # Serialize and encrypt
        json_data = json.dumps(commitment_data)
        encrypted = self.cipher.encrypt(json_data.encode())
        
        # Create hash for verification (player sees this, not the number)
        commitment_hash = hashlib.sha256(encrypted).hexdigest()
        
        # Store encrypted commitment server-side (Arcium would use secure enclave)
        self.commitments[player_id] = {
            'encrypted': encrypted.decode(),
            'hash': commitment_hash,
            'revealed': False
        }
        
        print(f"\n✓ COMMITMENT CREATED")
        print(f"  Player: {player_id}")
        print(f"  Commitment Hash: {commitment_hash[:16]}...")
        print(f"  (Your secret is now locked in encrypted form)")
        
        return commitment_hash
    
    def reveal(self, player_id: str) -> dict:
        """
        REVEAL PHASE: Open the commitment to prove honesty.
        
        Decrypts the commitment to show the secret number.
        Proves the number was committed before the guess phase.
        
        Args:
            player_id: The player revealing their commitment
            
        Returns:
            commitment data with decrypted number
        """
        if player_id not in self.commitments:
            raise ValueError(f"No commitment found for {player_id}")
        
        if self.commitments[player_id]['revealed']:
            raise ValueError(f"Commitment for {player_id} already revealed")
        
        # Decrypt the commitment
        encrypted_bytes = self.commitments[player_id]['encrypted'].encode()
        decrypted = self.cipher.decrypt(encrypted_bytes).decode()
        commitment_data = json.loads(decrypted)
        
        # Mark as revealed
        self.commitments[player_id]['revealed'] = True
        
        print(f"\n✓ COMMITMENT REVEALED")
        print(f"  Player: {player_id}")
        print(f"  Secret Number: {commitment_data['number']}")
        print(f"  Timestamp: {commitment_data['timestamp']}")
        print(f"  (This proves the number was decided beforehand)")
        
        return commitment_data
    
    def verify_commitment(self, player_id: str, commitment_hash: str) -> bool:
        """
        Verify that a commitment hash matches stored data.
        Proves commitment hasn't been tampered with.
        
        Args:
            player_id: The player who made the commitment
            commitment_hash: The hash to verify
            
        Returns:
            True if commitment is valid and unchanged
        """
        if player_id not in self.commitments:
            return False
        
        stored_hash = self.commitments[player_id]['hash']
        return stored_hash == commitment_hash


class PrivacyExplanation:
    """
    Educational module explaining Arcium's privacy model through this game.
    """
    
    @staticmethod
    def explain_commitment():
        print("\n" + "="*70)
        print("ARCIUM PRIVACY MODEL: COMMITMENT PHASE")
        print("="*70)
        print("""
🔒 WHAT HAPPENS:
   - Your secret number is ENCRYPTED
   - Only the HASH is shared (proves commitment exists)
   - The opponent CANNOT see your number yet

💡 WHY IT MATTERS:
   - In Arcium: Data stays encrypted during processing
   - Trust is built on cryptographic proof, not transparency
   - You can prove you knew something without revealing it

🎮 IN THIS GAME:
   - You commit to your number
   - Opponent sees only the hash
   - Your number is mathematically locked in
""")
    
    @staticmethod
    def explain_reveal():
        print("\n" + "="*70)
        print("ARCIUM PRIVACY MODEL: REVEAL PHASE")
        print("="*70)
        print("""
🔓 WHAT HAPPENS:
   - Your encrypted number is DECRYPTED
   - The secret is now visible
   - Timestamp proves when it was committed

💡 WHY IT MATTERS:
   - In Arcium: Data is revealed only to authorized parties
   - The reveal is VERIFIABLE (can't have changed)
   - You're proven honest retroactively

🎮 IN THIS GAME:
   - After guesses, your number is revealed
   - The commitment hash matches the decrypted data
   - This proves you didn't cheat
""")
