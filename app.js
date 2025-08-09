const API_KEY = 'AIzaSyCu5hNmaeJnL3avQJxzorEv8n4UZoi-x4A';

const jm = new jsMind({
  container: 'jsmind_container',
  editable: true,
  theme: 'primary'
});

function load() {
  const saved = localStorage.getItem('mindmap');
  if (saved) {
    jm.show(JSON.parse(saved));
  } else {
    const mind = {
      meta: { name: 'MindMap' },
      format: 'node_tree',
      data: { id: 'root', topic: 'Root' }
    };
    jm.show(mind);
  }
}

function save() {
  const data = jm.get_data('node_tree');
  localStorage.setItem('mindmap', JSON.stringify(data));
}

load();

window.addEventListener('beforeunload', save);
document.getElementById('save').onclick = save;

document.getElementById('ask').onclick = async () => {
  if (!navigator.onLine) {
    alert('Offline: asking disabled');
    return;
  }
  const selected = jm.get_selected_node();
  if (!selected) return;
  const prompt = selected.topic;
  const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ contents: [{ parts: [{ text: prompt }]}] })
  });
  const data = await res.json();
  const text = data.candidates?.[0]?.content?.parts?.[0]?.text || 'No answer';
  const qNode = jm.add_node(selected, 'q_' + Date.now(), 'Q: ' + prompt, {type:'question'});
  jm.add_node(qNode, 'a_' + Date.now(), 'A: ' + text, {type:'answer'});
  save();
};

document.getElementById('search').addEventListener('input', e => {
  const q = e.target.value.toLowerCase();
  jm.select_clear();
  if (!q) return;
  const nodes = jm.mind.nodes;
  for (const id in nodes) {
    const n = nodes[id];
    if (n.topic.toLowerCase().includes(q)) {
      jm.select_node(n);
      break;
    }
  }
});

document.getElementById('import').addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = ev => {
    const mind = JSON.parse(ev.target.result);
    jm.show(mind);
    save();
  };
  reader.readAsText(file);
});

document.getElementById('export_json').onclick = () => {
  const data = jm.get_data('node_tree');
  const blob = new Blob([JSON.stringify(data)], {type: 'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'mind.json';
  a.click();
};

window.addEventListener('online', () => {
  document.getElementById('ask').disabled = false;
});
window.addEventListener('offline', () => {
  document.getElementById('ask').disabled = true;
});

document.getElementById('ask').disabled = !navigator.onLine;
