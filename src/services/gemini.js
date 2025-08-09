const API_KEY = 'AIzaSyCu5hNmaeJnL3avQJxzorEv8n4UZoi-x4A'

export async function askGemini(prompt) {
  const body = {
    contents: [{ parts: [{ text: prompt }]}],
    generationConfig: { maxOutputTokens: 256 }
  }
  try {
    const res = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${API_KEY}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      }
    )
    const data = await res.json()
    return (
      data?.candidates?.[0]?.content?.parts
        ?.map((p) => p.text)
        .join('') || 'No response'
    )
  } catch (err) {
    console.error('Gemini error', err)
    return 'Error'
  }
}
