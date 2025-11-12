# Guess the Number: Encrypted Commit/Reveal

A small, clean, and educational game that teaches **Arcium's privacy model** through interactive gameplay.

## 🎮 What is This Game?

A privacy-preserving number guessing game where:
1. **Player A** secretly commits to a number (encrypted with cryptographic binding)
2. **Player B** makes guesses to find the number
3. Each guess gets feedback (hot/cold)
4. After guessing, **Player A** reveals and proves they were honest
5. The commitment hash **verifies** no cheating occurred

## 🔐 Arcium Concepts Demonstrated

### 1. **Commitment** (Cryptographic Binding)
- Player commits to a number by encrypting it
- The commitment is locked in with a cryptographic hash
- Can't change the number without breaking the hash
- **Arcium Use**: Proves what data you possess before computation starts

### 2. **Reveal** (Authorized Decryption)
- After game ends, the encrypted commitment is decrypted
- The secret is revealed to verify the claim
- **Arcium Use**: Results are only revealed to authorized parties

### 3. **Verification** (Integrity Proof)
- The commitment hash is verified against decrypted data
- Proves the data hasn't been tampered with
- If hashes match → Player was honest
- If hashes don't match → Someone cheated
- **Arcium Use**: Cryptographic signatures guarantee data integrity

## 📁 Project Structure

```
guess-number-game/
├── main.py              # Interactive CLI interface
├── game.py              # Game logic and rules
├── encryption.py        # Commit/reveal protocol
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Running the Game

```bash
python main.py
```

## 📚 Learning Path

The game has multiple modes to learn Arcium concepts:

### 1. **Single Player Mode**
- You guess against the computer
- Computer's number is encrypted
- Learn commitment/reveal in action
- **Duration**: ~5-10 minutes

### 2. **Two Player Mode**
- Local multiplayer between two people
- Player 1 commits, Player 2 guesses
- Full experience of privacy protection
- **Duration**: ~10-15 minutes

### 3. **Education Mode**
- Deep dive into Arcium concepts
- Learn commitment, reveal, verification separately
- See how they apply to real Arcium use cases

## 🔍 How It Works: Technical Details

### Commitment Phase
```
Player creates secret: 42
    ↓
JSON-serialize: {"number": 42, "timestamp": "...", "player": "..."}
    ↓
Encrypt with Fernet: [encrypted bytes]
    ↓
Create SHA256 hash: "a3f2e1d4..."
    ↓
Send hash to opponent (they see ONLY this)
```

**Key Point**: Opponent can see the hash but NOT the number. The commitment is cryptographically bound.

### Guessing Phase
```
Opponent guesses: 50
    ↓
Compare: abs(50 - 42) = 8
    ↓
Feedback: "🔥 Very close!"
    ↓
Encrypted commitment stays SEALED
    ↓
Opponent can't modify it or see it
```

**Key Point**: The encrypted commitment prevents cheating. No peeking!

### Reveal Phase
```
Game over (guesses exhausted or correct)
    ↓
Decrypt commitment: {"number": 42, ...}
    ↓
Verify hash: SHA256(encrypted) == original_hash
    ↓
If match → Honest ✓
If no match → Cheated ✗
```

**Key Point**: Cryptographic verification proves honesty mathematically.

## 🎓 Teaching Moments

### What Students Learn:

1. **Encryption is not enough** - You also need commitment binding
2. **Hash functions are one-way** - Can't reverse from hash to number
3. **Timestamps matter** - Proves when decision was made
4. **Verification is mathematical** - Not based on trust
5. **Privacy ≠ Secrecy** - You can prove things without revealing them

### Real-World Arcium Applications:

| Game Concept | Arcium Use Case |
|---|---|
| Player commits to number | User sends encrypted data to Arcium network |
| Opponent guesses blindly | Computation happens on encrypted data |
| Reveal & verify | Results decrypted and verified by authorized party |
| Can't cheat mid-game | Smart contracts can't be modified during execution |

## 🏗️ Code Architecture

### `encryption.py`
- `CommitRevealProtocol`: Core commit/reveal implementation
- `PrivacyExplanation`: Educational messages
- Uses `cryptography.fernet` for AES-128 encryption

### `game.py`
- `GuessTheNumberGame`: Game state and rules
- Implements hot/cold feedback algorithm
- Tracks commitment integrity

### `main.py`
- `GameInterface`: Interactive CLI
- Menu system and game modes
- Educational content delivery

## 🔐 Security Notes

This is an **educational demo**, not production security. In a real system:

- Keys would be stored in secure enclaves (Arcium's model)
- Communication would be over TLS/DTLS
- Commitment would use zero-knowledge proofs
- Verification would involve cryptographic signatures

But the **core concepts** are the same:
✓ Encrypt before revealing  
✓ Commit before guessing  
✓ Verify before trusting  

## 🎯 Use Cases for Education

### University Courses
- Cryptography fundamentals
- Privacy-preserving computation
- Applied game theory
- Blockchain security

### Arcium Onboarding
- New users understanding privacy model
- Developers learning commit/reveal pattern
- Privacy advocates seeing it in action

### Security Training
- Interactive learning
- Hands-on cryptography
- Practical privacy concepts

## 📖 Further Learning

After this game, explore:
1. **Zero-Knowledge Proofs** - Prove something without revealing it
2. **Multi-Party Computation** - Multiple players, shared computation
3. **Smart Contracts** - Programs that execute privately
4. **Blockchain Privacy** - Arcium's full platform

## 🤝 Contributing

This is an educational prototype. To extend:

1. **Add more modes**:
   - Tournament mode (multiple rounds)
   - Difficulty levels
   - Leaderboards

2. **Improve graphics**:
   - Web-based UI
   - Visual commitment/reveal animations
   - Real-time verification display

3. **Add complexity**:
   - Multiple simultaneous games
   - Distributed verification
   - Zero-knowledge proof version

## 📝 License

This educational game is provided as a teaching tool for Arcium concepts.

---

**Remember**: In Arcium, your data stays encrypted during computation. This game shows why that matters. 🔒
