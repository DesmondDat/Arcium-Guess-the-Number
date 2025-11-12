# Quick Start Guide

## Installation & Setup

```bash
# 1. Navigate to the game directory
cd "c:\Users\DR ESAN\Documents\ARCIUM GAME\guess-number-game"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the game
python main.py
```

## Three Ways to Experience the Game

### 🎮 Option 1: Single Player (Quick - ~5 min)
```bash
python main.py
→ Choose "1" (Single Player)
→ Guess the computer's secret number
→ See commitment/reveal in action
```

### 👥 Option 2: Two Player (Full Experience - ~10 min)
```bash
python main.py
→ Choose "2" (Two Player)
→ One player commits, one guesses
→ Experience full privacy protection
```

### 📚 Option 3: Learn Mode (Educational - ~15 min)
```bash
python main.py
→ Choose "3" (Learn About Arcium)
→ Explore commitment, reveal, verification
→ See how it applies to real Arcium
```

## See It In Action (No Installation)

```bash
python demo.py
```

This runs automated demos showing:
- Complete game flow
- Commitment protocol
- Privacy concepts
- Edge case testing

## What You'll Learn

| Concept | What You Learn |
|---------|---|
| **Commitment** | How to cryptographically prove you know something without revealing it |
| **Reveal** | How encrypted data is decrypted for authorized parties |
| **Verification** | How cryptographic hashes prove data integrity |
| **Privacy-Preserving** | How computation can happen without exposing secrets |

## Game Flow Summary

```
┌─────────────────┐
│   COMMITMENT    │  Player A encrypts secret number
│   (Encrypted)   │  Opponent sees only the hash
└────────┬────────┘
         │
┌────────▼────────┐
│    GUESSING     │  Player B makes blind guesses
│  (Sealed Data)  │  Player A gives hot/cold feedback
└────────┬────────┘
         │
┌────────▼────────┐
│  REVEAL & VER.  │  Decrypt commitment
│   (Verified!)   │  Verify hash matches
└─────────────────┘  Prove player was honest
```

## Key Files

| File | Purpose |
|------|---------|
| `main.py` | Start here - interactive CLI game |
| `demo.py` | Run demos without user interaction |
| `game.py` | Core game logic and rules |
| `encryption.py` | Cryptographic commit/reveal protocol |
| `README.md` | Complete documentation |

## Troubleshooting

**Q: "ModuleNotFoundError: No module named 'cryptography'"**
```bash
A: Run: pip install -r requirements.txt
```

**Q: "Permission denied when running python"**
```bash
A: Try: python main.py (instead of python3)
```

**Q: "Game won't run on my system"**
```bash
A: This is Python 3.7+. Check your Python version:
   python --version
```

## Next Steps After Learning

1. **Read the full code** - `encryption.py` shows cryptography in action
2. **Modify the game** - Change difficulty, add new modes
3. **Learn more** - Explore zero-knowledge proofs, multi-party computation
4. **Apply to Arcium** - Understand privacy-preserving smart contracts

---

**Questions?** Check README.md for full documentation.

**Ready?** Type: `python main.py` ✨
