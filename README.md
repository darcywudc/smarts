# MindMap × LLM

Simple prototype combining a mind‑map editor with Gemini Flash 2.5.

## Features

- Interactive mind map built with [React Flow](https://reactflow.dev/)
- Node types: **topic**, **question**, **answer**, **note**
- Double‑click a node to ask Gemini; question and answer nodes are added
- Auto‑saved to `localStorage`
- Search box highlights nodes by content
- Offline mode disables AI requests and shows a banner

## Development

```bash
npm install # install dependencies
npm run dev # requires GEMINI_API_KEY in your environment
# or `vercel dev` to run with serverless functions
```

No tests are provided; `npm test` prints a placeholder message.

### Environment Variables

Create a `.env` file (or set variables in your shell) containing:

```
GEMINI_API_KEY=your_key_here
```

The front‑end calls a `/api/gemini` serverless function, which reads this
variable server‑side so the key is never exposed to the browser.

### Vercel Preview Deployment

To enable preview URLs for every pull request:

1. Add `GEMINI_API_KEY` as a **GitHub Actions secret** and as a Vercel
   project environment variable (Preview and Production).
2. Connect the GitHub repository to Vercel; each PR will build a preview
   deploying the app.
3. Optionally, require the Vercel check to pass before merging to `main`.
