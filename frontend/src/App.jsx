import { useState } from 'react'
import './App.css'

const API_BASE = 'https://devpulse-production-fb8a.up.railway.app'

function App() {
  const [username, setUsername] = useState('')
  const [streak, setStreak] = useState(null)
  const [digest, setDigest] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSync() {
    if (!username) return
    setLoading(true)
    setError('')

    try {
      // step 1 - sync github events
      await fetch(`${API_BASE}/github/sync/${username}`, {
        method: 'POST'
      })

      // step 2 - get the streak
      const streakRes = await fetch(`${API_BASE}/stats/${username}`)
      const streakData = await streakRes.json()
      setStreak(streakData.streak)

      // step 3 - get the digest
      const digestRes = await fetch(`${API_BASE}/stats/digest/${username}`)

      if (digestRes.ok) {
        const digestData = await digestRes.json()
        setDigest(digestData.digest)
      }
      else {
        setDigest('Digest unavailable - API credits needed')
      }

    } catch (err) {
      setError('Something went wrong. Check your username and try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="dashboard">
      <h1>DevPulse</h1>
      <p>Your engineering activity at a glance</p>

      <div className="input-row">
        <input
          type="text"
          placeholder="GitHub username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <button onClick={handleSync} disabled={loading}>
          {loading ? 'Syncing...' : 'Sync'}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      {streak !== null && (
        <div className="card">
          <h2>Current Streak</h2>
          <p className="streak-number">{streak} days</p>
        </div>
      )}

      {digest && (
        <div className="card">
          <h2>Weekly Digest</h2>
          <p>{digest}</p>
        </div>
      )}
    </div>
  )
}

export default App