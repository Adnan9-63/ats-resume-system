import { useState } from 'react'

/**
 * Deliberately kept as ONE component for now, not split into many
 * small ones -- the app is still small enough that splitting would add
 * indirection without real benefit. Splitting into ResumeForm /
 * ScoreBreakdown / SuggestionsList components is reasonable future
 * work once this grows (e.g. once auth/history are added), not
 * something to do prematurely.
 */
export default function App() {
  const [resumeText, setResumeText] = useState('')
  const [jdText, setJdText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume_text: resumeText, jd_text: jdText }),
      })

      if (!response.ok) {
        const body = await response.json().catch(() => ({}))
        throw new Error(body.detail || `Request failed (${response.status})`)
      }

      setResult(await response.json())
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>AI ATS Resume Scorer</h1>
      <p className="subtitle">Paste your resume and a job description to see how well they match.</p>

      <form onSubmit={handleSubmit}>
        <label>
          Resume text
          <textarea
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            placeholder="Paste your resume text here..."
            rows={10}
            required
            minLength={10}
          />
        </label>

        <label>
          Job description
          <textarea
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            placeholder="Paste the job description here..."
            rows={10}
            required
            minLength={10}
          />
        </label>

        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze match'}
        </button>
      </form>

      {error && <div className="error">Error: {error}</div>}

      {result && (
        <div className="results">
          <h2>Match report</h2>
          <div className="score-grid">
            <ScoreCard label="Overall score" value={result.overall_score} />
            <ScoreCard label="Keyword match" value={result.keyword_match_score} />
            <ScoreCard label="Semantic fit" value={result.semantic_fit_score} />
            <ScoreCard label="Shortlist probability" value={result.predicted_shortlist_probability} />
          </div>
          <p>Matched skills: {result.matched_skill_count}</p>

          <h3>Suggestions</h3>
          <ul>
            {result.suggestions.map((tip, i) => (
              <li key={i}>{tip}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

function ScoreCard({ label, value }) {
  return (
    <div className="score-card">
      <div className="score-value">{Math.round(value * 100)}%</div>
      <div className="score-label">{label}</div>
    </div>
  )
}
