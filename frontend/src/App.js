// ─────────────────── src/App.js ───────────────────
import React, { useEffect, useRef, useState } from "react";
import "./App.css";

export default function App() {
  const [items, setItems] = useState([]);
  const wsRef = useRef(null);

  /* -----------------------------------------------------------
     1) One‑off fetch of the current inventory list
     ----------------------------------------------------------- */
  useEffect(() => {
    fetch("/api/items/")
      .then((r) => r.json())
      .then((data) => setItems(data))
      .catch((err) => console.error("Failed to load items", err));
  }, []);

  /* -----------------------------------------------------------
     2) Open WebSocket for live updates
     ----------------------------------------------------------- */
  useEffect(() => {
    const scheme   = window.location.protocol === "https:" ? "wss" : "ws";
    const host     = window.location.hostname;
    const portPart = window.location.port === "3000" ? ":8000" : "";

    const socket = new WebSocket(`${scheme}://${host}${portPart}/ws/inventory/`);
    wsRef.current = socket;

    socket.onopen = () => console.log("🔌 Inventory socket connected");
    socket.onclose = () => console.log("Inventory socket closed");
    socket.onerror = (e) => console.error("Inventory socket error", e);

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);   // {id, sku, name, qty}
        setItems((prev) => {
          const idx = prev.findIndex((i) => i.id === data.id);
          if (idx === -1) return [...prev, data];
          const clone = [...prev];
          clone[idx] = data;
          return clone;
        });
      } catch (e) {
        console.warn("Non‑JSON WS payload:", event.data);
      }
    };

    return () => socket.close();
  }, []);

  /* -----------------------------------------------------------
     3) Edit qty (very naive prompt + PATCH)
     ----------------------------------------------------------- */
  const editQty = (item) => {
    const newQtyStr = prompt(`New quantity for "${item.name}"`, item.qty);
    if (newQtyStr == null) return; // cancelled
    const newQty = parseInt(newQtyStr, 10);
    if (Number.isNaN(newQty)) return alert("Please enter a valid number.");

    fetch(`/api/items/${item.id}/`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ qty: newQty }),
    }).catch((err) => {
      console.error("Failed to patch item", err);
      alert("Failed to save change – see console.");
    });
  };

  return (
    <div className="App" style={{ padding: "2rem" }}>
      <h2>Inventory</h2>
      <table style={{ borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th style={{ textAlign: "left" }}>SKU</th>
            <th style={{ textAlign: "left" }}>Name</th>
            <th style={{ textAlign: "left" }}>Qty</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{item.sku}</td>
              <td>{item.name}</td>
              <td>{item.qty}</td>
              <td>
                <button onClick={() => editQty(item)}>Edit</button>
              </td>
            </tr>
          ))}
          {items.length === 0 && (
            <tr>
              <td colSpan={4}>No items yet.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
