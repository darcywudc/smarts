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
npm run dev
```

No tests are provided; `npm test` prints a placeholder message.
