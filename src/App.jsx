import React, { useState, useEffect } from 'react'
import MindMap from './components/MindMap.jsx'

export default function App() {
  const [query, setQuery] = useState('')
  const [online, setOnline] = useState(navigator.onLine)

  useEffect(() => {
    const update = () => setOnline(navigator.onLine)
    window.addEventListener('online', update)
    window.addEventListener('offline', update)
    return () => {
      window.removeEventListener('online', update)
      window.removeEventListener('offline', update)
    }
  }, [])

  return (
    <div>
      {!online && <div className="offline-banner">⚠ Offline: AI disabled</div>}
      <input
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Search"
      />
      <MindMap search={query} online={online} />
    </div>
  )
}
