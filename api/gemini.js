export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' })
    return
  }
  const { prompt, maxOutputTokens = 256 } =
    typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {}
  const body = {
    contents: [{ parts: [{ text: prompt }] }],
    generationConfig: { maxOutputTokens }
  }
  try {
    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${process.env.GEMINI_API_KEY}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      }
    )
    const data = await response.json()
    const text =
      data?.candidates?.[0]?.content?.parts?.map((p) => p.text).join('') ||
      'No response'
    res.status(200).json({ text })
  } catch (err) {
    console.error('Gemini error', err)
    res.status(500).json({ error: 'Gemini request failed' })
  }
}
