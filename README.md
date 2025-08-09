# MindMap × LLM

Simple mind map that can query Gemini Flash 2.5.

## Features
- Uses [jsMind](https://github.com/hizzgdev/jsmind) for map rendering.
- Nodes can ask Google Gemini for answers which are added as question/answer nodes.
- Autosaves to localStorage and can import/export JSON files.
- Search box selects first matching node.
- Disables AI asking while offline.

## Usage
Open `index.html` in a modern browser. Select a node and click **Ask AI** to create a question and answer pair.

The app stores data in `localStorage` under the key `mindmap`.
