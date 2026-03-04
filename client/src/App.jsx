import { useEffect, useMemo, useState } from 'react'
import './App.css'

const API_BASE_URL = 'http://localhost:5000'

function App() {
  const [locations, setLocations] = useState([])
  const [start, setStart] = useState('')
  const [destinations, setDestinations] = useState([])
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loadingLocations, setLoadingLocations] = useState(true)
  const [loadingRoute, setLoadingRoute] = useState(false)

  useEffect(() => {
    const fetchLocations = async () => {
      setLoadingLocations(true)
      setError('')
      try {
        const response = await fetch(`${API_BASE_URL}/locations`)
        const data = await response.json()

        if (!response.ok || !Array.isArray(data)) {
          throw new Error('Failed to load locations from server.')
        }

        setLocations(data)
      } catch (fetchError) {
        setError(fetchError.message || 'Unable to fetch locations.')
      } finally {
        setLoadingLocations(false)
      }
    }

    fetchLocations()
  }, [])

  const destinationOptions = useMemo(
    () => locations.filter((city) => city !== start),
    [locations, start],
  )

  const handleStartChange = (event) => {
    const selectedStart = event.target.value
    setStart(selectedStart)
    setDestinations((current) => current.filter((city) => city !== selectedStart))
  }

  const handleDestinationsChange = (event) => {
    const selected = Array.from(event.target.selectedOptions, (option) => option.value)
    setDestinations(selected)
  }

  const handleFindRoute = async () => {
    setError('')
    setResult(null)

    if (!start) {
      setError('Please select a start location.')
      return
    }

    if (destinations.length === 0) {
      setError('Please select at least one destination.')
      return
    }

    setLoadingRoute(true)
    try {
      const response = await fetch(`${API_BASE_URL}/route`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start, destinations }),
      })
      const data = await response.json()

      if (!response.ok || !data.success) {
        throw new Error(data.message || 'Route calculation failed.')
      }

      setResult({
        path: data.path || [],
        distance: data.distance ?? 0,
      })
    } catch (routeError) {
      setError(routeError.message || 'Unable to find route.')
    } finally {
      setLoadingRoute(false)
    }
  }

  return (
    <main className="app-shell">
      <section className="route-card">
        <h1>Goal-Based Travel Route Agent</h1>
        <p className="subtitle">Find the shortest route through one or more destinations.</p>

        {loadingLocations ? <p className="loading">Loading locations...</p> : null}

        {!loadingLocations && (
          <>
            <div className="field">
              <label htmlFor="start">Start Location</label>
              <select id="start" value={start} onChange={handleStartChange}>
                <option value="">Select start location</option>
                {locations.map((city) => (
                  <option key={city} value={city}>
                    {city}
                  </option>
                ))}
              </select>
            </div>

            <div className="field">
              <label htmlFor="destinations">Destinations (multi-select)</label>
              <select
                id="destinations"
                multiple
                value={destinations}
                onChange={handleDestinationsChange}
                size={Math.min(8, Math.max(4, destinationOptions.length))}
              >
                {destinationOptions.map((city) => (
                  <option key={city} value={city}>
                    {city}
                  </option>
                ))}
              </select>
            </div>

            <button
              type="button"
              onClick={handleFindRoute}
              disabled={loadingRoute || loadingLocations}
            >
              {loadingRoute ? 'Finding route...' : 'Find Route'}
            </button>
          </>
        )}

        {error ? <p className="message error">{error}</p> : null}

        {result ? (
          <div className="result">
            <h2>Route Result</h2>
            <p>
              <strong>Shortest Path:</strong> {result.path.join(' → ')}
            </p>
            <p>
              <strong>Total Distance:</strong> {result.distance} km
            </p>
          </div>
        ) : null}
      </section>
    </main>
  )
}

export default App
