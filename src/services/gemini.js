export async function askGemini(prompt) {
  try {
    const res = await fetch('/api/gemini', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt })
    })
    const data = await res.json()
    return data.text || 'No response'
  } catch (err) {
    console.error('Gemini error', err)
    return 'Error'
  }
}
