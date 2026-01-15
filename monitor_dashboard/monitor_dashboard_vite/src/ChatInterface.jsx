import React, { useState, useEffect, useRef } from "react";
import useSovereignChat from "./useSovereignChat";

export default function ChatInterface() {
  const { messages, loading, sendMessage } = useSovereignChat();
  const [input, setInput] = useState("");
  const [isSpeaking, setIsSpeaking] = useState(false);
  const bottomRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Fluid Audio: Speak new AI messages
  useEffect(() => {
    if (messages.length > 0) {
      const lastMsg = messages[messages.length - 1];
      if (lastMsg.role === "model" && !isSpeaking) {
        // Simple deduplication logic could be added here
        speak(lastMsg.content);
      }
    }
  }, [messages]);

  const speak = (text) => {
    if (!window.speechSynthesis) return;
    
    // Cancel any current speech to ensure fluid response
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    // Attempt to pick a decent voice (Google US English or similar)
    const voices = window.speechSynthesis.getVoices();
    const preferredVoice = voices.find(v => v.name.includes("Google US English") || v.name.includes("Samantha"));
    if (preferredVoice) utterance.voice = preferredVoice;

    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    
    window.speechSynthesis.speak(utterance);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    sendMessage(input);
    setInput("");
  };

  return (
    <div className="card" style={{ height: '600px', display: 'flex', flexDirection: 'column', marginTop: '20px' }}>
      <div style={{ flex: 1, overflowY: 'auto', padding: '10px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
        {loading && <div style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>Initializing Neural Bridge...</div>}
        
        {messages.map((msg) => (
          <div key={msg.id} style={{
            alignSelf: msg.role === "user" ? 'flex-end' : 'flex-start',
            background: msg.role === "user" ? 'rgba(6, 182, 212, 0.2)' : 'rgba(255, 255, 255, 0.05)',
            padding: '10px 15px',
            borderRadius: '12px',
            maxWidth: '80%',
            border: msg.role === "user" ? '1px solid var(--accent-pulse)' : '1px solid var(--glass-border)',
            color: 'var(--text-primary)'
          }}>
            <div style={{ fontSize: '0.7em', color: 'var(--text-secondary)', marginBottom: '4px' }}>
              {msg.role === "user" ? "YOU" : "SARAH"}
            </div>
            {msg.content}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <form onSubmit={handleSubmit} style={{ borderTop: '1px solid var(--glass-border)', padding: '15px' }}>
        <div style={{ display: 'flex', gap: '10px' }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Speak freely..."
            style={{
              flex: 1,
              background: 'rgba(0,0,0,0.3)',
              border: '1px solid var(--glass-border)',
              borderRadius: '8px',
              padding: '12px',
              color: 'var(--text-primary)',
              fontFamily: 'var(--monitor-font)',
              fontSize: '16px' // Prevents zoom on iOS
            }}
          />
          <button 
            type="submit"
            style={{
              background: 'var(--accent-pulse)',
              border: 'none',
              borderRadius: '8px',
              padding: '0 20px',
              color: '#000',
              fontWeight: 'bold',
              cursor: 'pointer'
            }}
          >
            SEND
          </button>
        </div>
        <div style={{ textAlign: 'center', marginTop: '10px', fontSize: '0.8em', color: 'var(--text-secondary)' }}>
          {isSpeaking ? "🔊 Speaking..." : "Listening..."}
        </div>
      </form>
    </div>
  );
}
