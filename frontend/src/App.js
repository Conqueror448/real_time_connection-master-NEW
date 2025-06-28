// ─────────────────── src/App.js ───────────────────
import React, { useEffect, useRef, useState } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const wsRef = useRef(null);

  useEffect(() => {
    /* -----------------------------------------------------------
       Build the correct WebSocket URL for any environment
       ----------------------------------------------------------- */
    const scheme   = window.location.protocol === "https:" ? "wss" : "ws";
    const host     = window.location.hostname;
    const portPart =
      // If we're on port 3000 (dev mode), connect to backend on 8000
      // If we're on port 80 or no port (prod mode), use same port (through Nginx)
      window.location.port === "3000" ? ":8000" : "";

    const socket = new WebSocket(`${scheme}://${host}${portPart}/ws/echo/`);
    wsRef.current = socket;

    socket.onopen = () => {
      console.log("🔌 WebSocket connected");
      socket.send("Frontend says hello!");      // handshake test
    };

    socket.onmessage = (event) => {
      // EchoConsumer may send plain text OR JSON; handle either
      let data = event.data;
      try {
        const parsed = JSON.parse(event.data);
        data = parsed.echo ?? JSON.stringify(parsed);
      } catch (_) {
        /* not JSON, keep raw */
      }
      setMessages((prev) => [...prev, data]);
    };

    socket.onclose  = ()  => console.log("WebSocket closed");
    socket.onerror  = (e) => console.error("WebSocket error", e);

    return () => socket.close();                // cleanup on unmount
  }, []);

  const sendPing = () => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(
        "Ping from React at " + new Date().toLocaleTimeString()
      );
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h2>Real-time WebSocket demo</h2>
        <button onClick={sendPing}>Send Ping</button>
        <ul style={{ textAlign: "left", maxWidth: 400 }}>
          {messages.map((m, i) => (
            <li key={i}>{m}</li>
          ))}
        </ul>
      </header>
    </div>
  );
}

export default App;
