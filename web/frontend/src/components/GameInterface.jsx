import React, { useState } from 'react';
import './GameInterface.css';

export default function GameInterface() {
  const [gameState, setGameState] = useState('menu');
  const [gameId, setGameId] = useState(null);
  const [mode, setMode] = useState(null);
  const [secretNumber, setSecretNumber] = useState('');
  const [guess, setGuess] = useState('');
  const [feedback, setFeedback] = useState('');
  const [guesses, setGuesses] = useState([]);
  const [commitmentHash, setCommitmentHash] = useState('');
  const [gameResult, setGameResult] = useState(null);
  const [stats, setStats] = useState(null);
  const [player1Name, setPlayer1Name] = useState('You');
  const [player2Name, setPlayer2Name] = useState('Computer');
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  const createGame = async (selectedMode) => {
    try {
      const response = await fetch(`${API_URL}/api/game/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mode: selectedMode,
          player1: selectedMode === 'single' ? 'You' : player1Name,
          player2: selectedMode === 'single' ? 'Computer' : player2Name
        })
      });

      const data = await response.json();
      if (data.success) {
        setGameId(data.game_id);
        setMode(selectedMode);
        setGameState(selectedMode === 'single' ? 'commitment' : 'commitment');
        setGuesses([]);
        setFeedback('');
      }
    } catch (error) {
      console.error('Error creating game:', error);
      alert('Failed to create game');
    }
  };

  const commitSecret = async () => {
    if (!secretNumber || secretNumber < 1 || secretNumber > 100) {
      alert('Please enter a number between 1 and 100');
      return;
    }

    try {
      const response = await fetch(`${API_URL}/api/game/${gameId}/commit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ secret: parseInt(secretNumber) })
      });

      const data = await response.json();
      if (data.success) {
        setCommitmentHash(data.commitment_hash);
        setSecretNumber('');
        setGameState('guessing');
        setFeedback('✓ Secret committed and encrypted!');
      }
    } catch (error) {
      console.error('Error committing:', error);
      alert('Failed to commit secret');
    }
  };

  const makeGuess = async () => {
    if (!guess || guess < 1 || guess > 100) {
      alert('Please enter a number between 1 and 100');
      return;
    }

    try {
      const response = await fetch(`${API_URL}/api/game/${gameId}/guess`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ guess: parseInt(guess) })
      });

      const data = await response.json();
      if (data.success) {
        setGuesses([...guesses, data.guess]);
        setFeedback(data.feedback);
        setGuess('');

        if (data.game_over) {
          setGameState('reveal');
        }
      } else {
        alert(data.error);
      }
    } catch (error) {
      console.error('Error making guess:', error);
      alert('Failed to make guess');
    }
  };

  const revealAnswer = async () => {
    try {
      const response = await fetch(`${API_URL}/api/game/${gameId}/reveal`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });

      const data = await response.json();
      if (data.success) {
        setGameResult(data);
        setGameState('result');
      }
    } catch (error) {
      console.error('Error revealing:', error);
      alert('Failed to reveal answer');
    }
  };

  const handleKeyPress = (e, action) => {
    if (e.key === 'Enter') {
      action();
    }
  };

  const resetGame = () => {
    setGameState('menu');
    setGameId(null);
    setMode(null);
    setSecretNumber('');
    setGuess('');
    setFeedback('');
    setGuesses([]);
    setCommitmentHash('');
    setGameResult(null);
  };

  return (
    <div className="game-container">
      <header className="game-header">
        <h1>🔐 Guess the Number: Encrypted Commit/Reveal</h1>
        <p>Learn Arcium's Privacy Model Through Game</p>
      </header>

      {gameState === 'menu' && (
        <div className="game-menu">
          <div className="menu-box">
            <h2>Choose Game Mode</h2>
            <button onClick={() => createGame('single')} className="btn btn-primary">
              👤 Single Player
              <br />
              <small>You vs Computer</small>
            </button>
            <button onClick={() => createGame('two')} className="btn btn-primary">
              👥 Two Player
              <br />
              <small>Local Multiplayer</small>
            </button>
            <button onClick={() => setGameState('learn')} className="btn btn-secondary">
              📚 Learn Mode
              <br />
              <small>Understand Concepts</small>
            </button>
          </div>
        </div>
      )}

      {gameState === 'commitment' && (
        <div className="game-screen">
          <div className="phase-box">
            <h2>🔒 COMMITMENT PHASE</h2>
            <p>Your secret number will be encrypted and cryptographically bound.</p>
            <p>Your opponent cannot see it during the guessing phase.</p>
            
            <div className="input-group">
              <input
                type="number"
                min="1"
                max="100"
                value={secretNumber}
                onChange={(e) => setSecretNumber(e.target.value)}
                onKeyPress={(e) => handleKeyPress(e, commitSecret)}
                placeholder="Enter secret number (1-100)"
                className="input-field"
              />
              <button onClick={commitSecret} className="btn btn-primary">
                Commit Secret
              </button>
            </div>
            <p className="hint">Your number will be encrypted - click to lock it in!</p>
          </div>
        </div>
      )}

      {gameState === 'guessing' && (
        <div className="game-screen">
          <div className="phase-box">
            <h2>🎯 GUESSING PHASE</h2>
            <div className="commitment-display">
              <p>📝 Commitment Hash: <code>{commitmentHash.substring(0, 32)}...</code></p>
              <p className="hint">(This proves the secret is locked in encrypted form)</p>
            </div>

            <div className="stats-box">
              <p>Guesses Made: <strong>{guesses.length}</strong> / 10</p>
              <p>Remaining: <strong>{10 - guesses.length}</strong></p>
            </div>

            {feedback && (
              <div className={`feedback ${getFeedbackClass(feedback)}`}>
                {feedback}
              </div>
            )}

            <div className="input-group">
              <input
                type="number"
                min="1"
                max="100"
                value={guess}
                onChange={(e) => setGuess(e.target.value)}
                onKeyPress={(e) => handleKeyPress(e, makeGuess)}
                placeholder="Make a guess (1-100)"
                className="input-field"
              />
              <button onClick={makeGuess} className="btn btn-primary">
                Guess
              </button>
            </div>

            {guesses.length > 0 && (
              <div className="guesses-history">
                <p><strong>Your Guesses:</strong> {guesses.join(', ')}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {gameState === 'reveal' && (
        <div className="game-screen">
          <div className="phase-box">
            <h2>🔓 REVEAL & VERIFY</h2>
            <p>Game over! Time to reveal and verify the commitment.</p>
            <p className="hint">
              The encrypted commitment will be decrypted and verified using the cryptographic hash.
            </p>
            
            <button onClick={revealAnswer} className="btn btn-primary btn-large">
              Reveal & Verify Commitment
            </button>
            
            <p className="hint">
              ✓ If the commitment hash matches the decrypted data, the player was honest!
            </p>
          </div>
        </div>
      )}

      {gameState === 'result' && gameResult && (
        <div className="game-screen">
          <div className="result-box">
            <h2>🏁 GAME RESULT</h2>
            
            <div className="result-content">
              <div className="result-secret">
                <p>Secret Number: <strong className="secret-number">{gameResult.secret_number}</strong></p>
              </div>

              <div className={gameResult.commitment_valid ? 'result-valid' : 'result-invalid'}>
                {gameResult.commitment_valid ? '✓ VERIFIED' : '✗ INVALID'}
              </div>

              <p className="result-message">{gameResult.result}</p>

              <div className="result-stats">
                <p>Guesses Made: <strong>{gameResult.guesses_made}</strong></p>
                <p>Committed At: <strong>{new Date(gameResult.timestamp).toLocaleString()}</strong></p>
                <p>Commitment: <strong>{gameResult.commitment_valid ? 'Honest ✓' : 'Cheated ✗'}</strong></p>
              </div>

              <div className="result-explanation">
                <h3>🔐 What Happened</h3>
                <p>
                  Your secret was encrypted and stored as a hash. During guessing, this commitment
                  stayed sealed. Now it's been decrypted and verified - proving you either were
                  honest (if hashes match) or cheated (if they don't).
                </p>
                <p>
                  <strong>This is how Arcium's privacy model works:</strong> Data stays encrypted
                  during computation, and only reveals to authorized parties with cryptographic proof.
                </p>
              </div>
            </div>

            <button onClick={resetGame} className="btn btn-primary">
              Play Again
            </button>
          </div>
        </div>
      )}

      {gameState === 'learn' && (
        <div className="game-screen">
          <div className="learn-box">
            <h2>📚 Learning Mode</h2>
            
            <div className="concept">
              <h3>🔒 Commitment</h3>
              <p>
                Your secret number is encrypted using cryptography. A hash is created to prove
                the commitment exists without revealing the number. You cannot change your secret
                without breaking the commitment.
              </p>
              <strong>Arcium Use:</strong> Data is committed before computation starts.
            </div>

            <div className="concept">
              <h3>🔓 Reveal</h3>
              <p>
                After the game, your encrypted commitment is decrypted to reveal the secret.
                A timestamp proves when the decision was made. Only authorized parties see the data.
              </p>
              <strong>Arcium Use:</strong> Results are revealed only to authorized users.
            </div>

            <div className="concept">
              <h3>✓ Verification</h3>
              <p>
                The commitment hash is verified against the decrypted data. If they match,
                you were honest. If not, you cheated. Cryptography proves this mathematically
                without needing a central authority.
              </p>
              <strong>Arcium Use:</strong> Cryptographic signatures guarantee data integrity.
            </div>

            <button onClick={resetGame} className="btn btn-primary">
              Back to Menu
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

function getFeedbackClass(feedback) {
  if (feedback.includes('CORRECT')) return 'feedback-correct';
  if (feedback.includes('Very close')) return 'feedback-hot';
  if (feedback.includes('warmer')) return 'feedback-warm';
  if (feedback.includes('colder')) return 'feedback-cold';
  return 'feedback-very-cold';
}
