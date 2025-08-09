import React, { useState, useCallback, useEffect } from 'react'
import ReactFlow, { addEdge, Background, Controls, MiniMap, useReactFlow } from 'reactflow'
import 'reactflow/dist/style.css'
import { askGemini } from '../services/gemini.js'

const defaultNode = {
  id: 'root',
  type: 'topic',
  data: { label: 'Root' },
  position: { x: 0, y: 0 }
}

const load = () => {
  try {
    const stored = JSON.parse(localStorage.getItem('mindmap') || '{"nodes":[],"edges":[]}')
    if (!stored.nodes.length) stored.nodes = [defaultNode]
    return stored
  } catch {
    return { nodes: [defaultNode], edges: [] }
  }
}

export default function MindMap({ search, online }) {
  const store = load()
  const [nodes, setNodes] = useState(store.nodes)
  const [edges, setEdges] = useState(store.edges)
  const instance = useReactFlow()

  useEffect(() => {
    localStorage.setItem('mindmap', JSON.stringify({ nodes, edges }))
  }, [nodes, edges])

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    []
  )

  const addQuestion = async (node) => {
    if (!online) return
    const questionId = `q_${Date.now()}`
    const answerId = `a_${Date.now()}`
    setNodes((nds) => nds.concat(
      { id: questionId, type: 'question', data: { label: '...' }, position: { x: node.position.x + 200, y: node.position.y } },
      { id: answerId, type: 'answer', data: { label: '...' }, position: { x: node.position.x + 400, y: node.position.y } }
    ))
    setEdges((eds) => eds.concat(
      { id: `e${node.id}-${questionId}`, source: node.id, target: questionId },
      { id: `e${questionId}-${answerId}`, source: questionId, target: answerId }
    ))
    const reply = await askGemini(node.data.label)
    setNodes((nds) => nds.map((n) => (n.id === answerId ? { ...n, data: { label: reply } } : n)))
  }

  const highlight = search.trim().toLowerCase()
  const styleFor = (n) =>
    highlight && n.data.label.toLowerCase().includes(highlight)
      ? { border: '2px solid orange' }
      : {}

  useEffect(() => {
    if (!highlight) return
    const match = nodes.find((n) => n.data.label.toLowerCase().includes(highlight))
    if (match) instance.fitView({ nodes: [match], duration: 400 })
  }, [highlight, nodes, instance])

  const nodeTypes = {
    topic: (props) => (
      <div style={{ padding: 10, ...styleFor(props) }} onDoubleClick={() => addQuestion(props)}>
        {props.data.label}
      </div>
    ),
    question: (props) => (
      <div style={{ padding: 10, background: '#eef', ...styleFor(props) }}>{props.data.label}</div>
    ),
    answer: (props) => (
      <div style={{ padding: 10, background: '#efe', ...styleFor(props) }}>{props.data.label}</div>
    ),
    note: (props) => (
      <div style={{ padding: 10, background: '#ffd', ...styleFor(props) }}>{props.data.label}</div>
    ),
  }

  return (
    <div style={{ width: '100%', height: '90vh' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={setNodes}
        onEdgesChange={setEdges}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        fitView
      >
        <MiniMap />
        <Controls />
        <Background />
      </ReactFlow>
    </div>
  )
}
