# Architecture & Design

## System Architecture

```
┌─────────────────────────────────────────────────┐
│         CLI Interface (main.py)                 │
│  ┌─────────────────────────────────────────┐   │
│  │  Menu → Single/Two Player/Learn Mode    │   │
│  │  Input validation & game flow control   │   │
│  └─────────────────────────────────────────┘   │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│        Game Logic (game.py)                     │
│  ┌─────────────────────────────────────────┐   │
│  │  GuessTheNumberGame class               │   │
│  │  - Setup and state management           │   │
│  │  - Commit phase                         │   │
│  │  - Guessing phase                       │   │
│  │  - Reveal & verify phase                │   │
│  │  - Hot/cold feedback                    │   │
│  └─────────────────────────────────────────┘   │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│   Encryption & Protocol (encryption.py)        │
│  ┌─────────────────────────────────────────┐   │
│  │  CommitRevealProtocol class             │   │
│  │  - Fernet encryption                    │   │
│  │  - SHA256 hashing                       │   │
│  │  - Commitment storage                   │   │
│  │  - Verification logic                   │   │
│  │  PrivacyExplanation class               │   │
│  │  - Educational content                  │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
                   │
                   ▼
         cryptography library
         (Fernet, SHA256)
```

## Class Diagram

```
GameInterface (main.py)
    │
    ├─→ GuessTheNumberGame (game.py)
    │       │
    │       └─→ CommitRevealProtocol (encryption.py)
    │               │
    │               └─→ cryptography.fernet.Fernet
    │
    └─→ PrivacyExplanation (encryption.py)
```

## Data Flow: Single Game

```
1. INITIALIZATION
   ┌────────────────┐
   │ Game Setup     │
   │ min=1, max=100 │
   │ max_guesses=10 │
   └────────┬───────┘
            │
            ▼
   ┌────────────────────────────┐
   │ Create CommitRevealProtocol│
   │ Generate Fernet key        │
   └────────────────────────────┘

2. COMMITMENT PHASE
   ┌──────────────────────┐
   │ Player picks: 42     │
   └──────────┬───────────┘
              │
              ▼
   ┌──────────────────────────────────────┐
   │ JSON: {"number": 42, ...}            │
   │ Encrypt with Fernet key              │
   │ Result: [encrypted bytes]            │
   └──────────┬───────────────────────────┘
              │
              ▼
   ┌──────────────────────────────────────┐
   │ SHA256 hash of encrypted bytes       │
   │ Commitment hash: "a3f2e1d4..."       │
   │ Stored server-side (encrypted)       │
   └──────────────────────────────────────┘

3. GUESSING PHASE
   ┌─────────────────────────────┐
   │ Opponent guesses: 50        │
   └─────────┬───────────────────┘
             │
             ▼
   ┌─────────────────────────────────────┐
   │ Distance = |50 - 42| = 8            │
   │ Feedback: "🔥 Very close!"          │
   │ (Never decrypts commitment)         │
   └─────────────────────────────────────┘
   
   [Repeat until correct or max guesses]

4. REVEAL & VERIFY
   ┌──────────────────────────────┐
   │ Game Over                    │
   │ Decrypt commitment           │
   │ Extract: {"number": 42, ...} │
   └──────────┬───────────────────┘
              │
              ▼
   ┌──────────────────────────────────────┐
   │ Hash(decrypted) = original_hash?     │
   │ YES → Honest ✓                       │
   │ NO  → Cheated ✗                      │
   └──────────────────────────────────────┘
```

## State Machine

```
                     ┌─────────────────┐
                     │     SETUP       │
                     │ Game initialized│
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │  COMMITMENT     │
                     │  Secret encoded │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                  ┌──│  GUESSING       │◄──┐
                  │  │ Guess → Feedback│   │
                  │  └────────┬────────┘   │
                  │           │            │
                  │        Continue?       │
                  │     /         \        │
                  │   NO           YES     │
                  │    │            └──────┘
                  │    ▼
                  │  ┌──────────────────┐
                  │  │ REVEAL           │
                  │  │ Decrypt & Verify │
                  │  └────────┬─────────┘
                  │           │
                  │           ▼
                  └──→ ┌─────────────────┐
                       │   COMPLETE      │
                       │ Winner decided  │
                       └─────────────────┘
```

## Commitment Data Structure

```json
{
  "encrypted": "gAAAAABjZeF_xxxx...[base64 encrypted]...xxxx",
  "hash": "a3f2e1d4c8b9f2e1d4c8b9f2e1d4c8b9f2e1d4c8",
  "revealed": false
}

Inside encrypted:
{
  "number": 42,
  "timestamp": "2025-11-12T10:30:45.123456",
  "player_id": "Alice"
}
```

## Key Algorithm: Hot/Cold Feedback

```python
def get_feedback(guess, secret):
    distance = abs(guess - secret)
    
    if distance == 0:
        return "🎯 CORRECT!"
    elif distance <= 5:
        return "🔥 Very close!"
    elif distance <= 15:
        return "🌡️ Getting warmer"
    elif distance <= 30:
        return "🧊 Getting colder"
    else:
        return "❄️ Very cold"
```

## Security Considerations

### What's Protected
✓ Secret number encrypted until reveal
✓ Commitment hash prevents mid-game changes
✓ Timestamp proves decision timing
✓ Verification proves honesty

### What's Not Protected (Educational Demo)
- Key stored in memory (would use secure enclave in Arcium)
- No network encryption (would use TLS in production)
- Single session (no persistence)
- Local storage (no distributed ledger)

### How Arcium Improves This
1. **Secure Enclaves** - Keys protected by hardware
2. **Distributed Verification** - Multiple nodes verify
3. **Zero-Knowledge Proofs** - Prove without revealing
4. **Smart Contracts** - Automated verification
5. **Privacy-Preserving ML** - Compute on encrypted data

## Module Responsibilities

### encryption.py
**Purpose**: Cryptographic operations
**Exports**:
- `CommitRevealProtocol` class
  - `commit(secret, player_id)` → hash
  - `reveal(player_id)` → decrypted data
  - `verify_commitment(player_id, hash)` → bool
- `PrivacyExplanation` class
  - Educational content methods

### game.py
**Purpose**: Game rules and logic
**Exports**:
- `GuessTheNumberGame` class
  - `setup_game(committer, guesser)`
  - `commit_number(secret)` → hash
  - `make_guess(guess)` → feedback
  - `reveal_and_verify()` → result
  - `get_game_stats()` → stats

### main.py
**Purpose**: User interface
**Exports**:
- `GameInterface` class
  - `run()` - Main game loop
  - `single_player_mode()`
  - `two_player_mode()`
  - `learn_mode()`

### demo.py
**Purpose**: Automated testing
**Functions**:
- `demo_single_game()`
- `demo_commitment_protocol()`
- `test_edge_cases()`
- `run_all_demos()`

## Dependency Graph

```
main.py
  ├─→ game.py
  │     └─→ encryption.py
  │           └─→ cryptography.fernet
  └─→ encryption.py

game.py
  └─→ encryption.py
       └─→ cryptography.fernet

demo.py
  ├─→ game.py
  │     └─→ encryption.py
  └─→ encryption.py

External:
  cryptography (Fernet for encryption)
  hashlib (SHA256 - built-in)
  json (serialization - built-in)
  datetime (timestamps - built-in)
  random (for computer player - built-in)
```

## Extension Points

To modify or extend:

1. **New Game Modes**
   - Modify `GameInterface.show_menu()` in main.py
   - Add new game variant in game.py

2. **Different Encryption**
   - Replace Fernet with RSA, AES-GCM in encryption.py
   - Game logic stays the same

3. **Network Play**
   - Add client/server in main.py
   - Use same game.py logic
   - Send state over network

4. **Web UI**
   - Flask/Django backend using game.py
   - React frontend using API
   - Same encryption.py logic

5. **Smart Contracts**
   - Export game logic to Solidity/Cairo
   - Use Arcium for privacy-preserving version
   - Keep commit/reveal pattern

---

This architecture ensures:
- **Modularity** - Each module has clear purpose
- **Testability** - Can test encryption, game, UI separately
- **Extensibility** - Easy to add new features
- **Maintainability** - Changes in one layer don't break others
- **Educational Value** - Each layer demonstrates a concept
