"use client";
import React, { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const DEMO_STEPS = [
  {
    step: "1. Compare 3 Laptops",
    prompt: "Compare these three laptops under my $1,500 budget",
    badge: "Shopping Agent + TinyFish Live",
  },
  {
    step: "2. Webinar Signup (Alias Shield)",
    prompt: "Sign me up for this Agentic AI webinar",
    badge: "Web Task Agent + Fresh Alias",
  },
  {
    step: "3. Leak Alert: Loan App Spam",
    prompt: "Who leaked my email? Check recent alias activity",
    badge: "Privacy Agent: Catch the Leaker",
  },
  {
    step: "4. Live Account Deletion (2-Step)",
    prompt: "Delete me from apps I don't use",
    badge: "Privacy Agent: Data Cleanup",
  },
];

export default function ScoutBrowserApp() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<any>(null);
  const [run2Result, setRun2Result] = useState<any>(null);

  async function executePrompt(customPrompt?: string) {
    const query = customPrompt ?? prompt;
    if (!query.trim()) return;
    setPrompt(query);
    setLoading(true);
    setRun2Result(null);
    try {
      const res = await fetch(`${API_URL}/api/command`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: "demo-user-1",
          prompt: query,
          current_page_url: "https://lu.ma/agentic-ai-webinar",
        }),
      });
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function confirmRun2Deletion() {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/approve-deletion-run2`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          task_id: "task-del-1",
          user_id: "demo-user-1",
          approved: true,
        }),
      });
      const data = await res.json();
      setRun2Result(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ minHeight: "100vh", background: "#0b0f17", color: "#e2e8f0", fontFamily: "system-ui, sans-serif", padding: "24px" }}>
      {/* Top Header */}
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "1px solid #1e293b", paddingBottom: "16px", marginBottom: "20px" }}>
        <div>
          <h1 style={{ fontSize: "22px", fontWeight: 700, color: "#38bdf8", margin: 0 }}>
            SCOUT // Privacy-First AI Personal Browser
          </h1>
          <p style={{ fontSize: "13px", color: "#94a3b8", margin: "4px 0 0 0" }}>
            Scout browses for you via TinyFish, and makes sure no app can leak you without getting caught.
          </p>
        </div>
        <div style={{ background: "#064e3b", color: "#6ee7b7", padding: "6px 12px", borderRadius: "999px", fontSize: "12px", fontWeight: 600 }}>
          Privacy Agent: ACTIVE ON ALL TASKS
        </div>
      </header>

      {/* 2-Minute Demo Quick-Trigger Bar */}
      <div style={{ display: "flex", gap: "10px", flexWrap: "wrap", marginBottom: "20px" }}>
        {DEMO_STEPS.map((d) => (
          <button
            key={d.step}
            onClick={() => executePrompt(d.prompt)}
            style={{
              background: "#1e293b",
              border: "1px solid #334155",
              color: "#f8fafc",
              padding: "10px 14px",
              borderRadius: "8px",
              cursor: "pointer",
              textAlign: "left",
            }}
          >
            <div style={{ fontWeight: 600, fontSize: "13px", color: "#38bdf8" }}>{d.step}</div>
            <div style={{ fontSize: "11px", color: "#94a3b8", marginTop: "2px" }}>{d.badge}</div>
          </button>
        ))}
      </div>

      {/* Chat-Style Command Bar */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "24px" }}>
        <input
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && executePrompt()}
          placeholder="Ask Scout anything in plain language (e.g., 'Compare these three laptops', 'Sign me up for this webinar', 'Delete me from apps I don't use')..."
          style={{
            flex: 1,
            background: "#0f172a",
            border: "1px solid #334155",
            borderRadius: "8px",
            padding: "14px 16px",
            color: "#fff",
            fontSize: "15px",
          }}
        />
        <button
          onClick={() => executePrompt()}
          disabled={loading}
          style={{
            background: "#0284c7",
            color: "#fff",
            border: "none",
            borderRadius: "8px",
            padding: "0 24px",
            fontWeight: 600,
            cursor: "pointer",
          }}
        >
          {loading ? "Running..." : "Run Scout"}
        </button>
      </div>

      {/* Main Split View: Orchestrator & Agent Output (Left) + Live TinyFish Browser View (Right) */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
        {/* Left Panel: Orchestrator Plan, Alias Shield, Leak Evidence & Human-in-the-Loop */}
        <div style={{ background: "#111827", border: "1px solid #1f2937", borderRadius: "12px", padding: "20px" }}>
          <h2 style={{ fontSize: "16px", marginTop: 0, color: "#93c5fd" }}>Orchestrator & Agent Telemetry</h2>
          {!response ? (
            <p style={{ color: "#64748b", fontSize: "14px" }}>
              Select one of the 4 Demo steps above or type a plain-language request.
            </p>
          ) : (
            <div>
              <div style={{ marginBottom: "12px", fontSize: "13px" }}>
                <strong>Classified Intent:</strong> <code>{response.intent}</code>
              </div>
              <div style={{ marginBottom: "16px", fontSize: "13px" }}>
                <strong>Agents Invoked:</strong> {response.agents_invoked?.join(" → ")}
              </div>

              {/* Human-in-the-loop Confirmation Box for Deletion Run 1 -> Run 2 */}
              {response.outputs?.deletion_run_1 && !run2Result && (
                <div style={{ background: "#422006", border: "1px solid #d97706", padding: "14px", borderRadius: "8px", marginBottom: "16px" }}>
                  <div style={{ fontWeight: 700, color: "#fbbf24", marginBottom: "6px" }}>
                    HUMAN-IN-THE-LOOP: Two-Step Deletion Paused (Run 1 Complete)
                  </div>
                  <p style={{ fontSize: "13px", margin: "0 0 12px 0" }}>
                    {response.outputs.deletion_run_1.prompt_to_user}
                  </p>
                  <button
                    onClick={confirmRun2Deletion}
                    style={{ background: "#dc2626", color: "#fff", border: "none", padding: "8px 16px", borderRadius: "6px", fontWeight: 600, cursor: "pointer" }}
                  >
                    Approve Final Deletion (Execute Run 2)
                  </button>
                </div>
              )}

              {run2Result && (
                <div style={{ background: "#064e3b", border: "1px solid #10b981", padding: "14px", borderRadius: "8px", marginBottom: "16px" }}>
                  <div style={{ fontWeight: 700, color: "#6ee7b7" }}>
                    Run 2 Confirmed — Account Deleted & Route Saved to Shared Deletion Map
                  </div>
                  <p style={{ fontSize: "12px", marginTop: "6px" }}>{run2Result.grace_period_warning}</p>
                </div>
              )}

              <pre style={{ background: "#030712", padding: "14px", borderRadius: "8px", fontSize: "12px", overflowX: "auto", color: "#a7f3d0" }}>
                {JSON.stringify(run2Result || response.outputs, null, 2)}
              </pre>
            </div>
          )}
        </div>

        {/* Right Panel: Live TinyFish Browser Streaming View */}
        <div style={{ background: "#111827", border: "1px solid #1f2937", borderRadius: "12px", padding: "20px", display: "flex", flexDirection: "column" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
            <h2 style={{ fontSize: "16px", margin: 0, color: "#93c5fd" }}>Live TinyFish Browser Session (/run-sse)</h2>
            <span style={{ fontSize: "11px", color: "#38bdf8" }}>
              {response?.streaming_url || "Standby"}
            </span>
          </div>
          <div style={{ flex: 1, minHeight: "380px", background: "#030712", border: "1px dashed #334155", borderRadius: "8px", display: "flex", alignItems: "center", justifyContent: "center", padding: "20px", textAlign: "center" }}>
            {response?.streaming_url ? (
              <div>
                <div style={{ color: "#38bdf8", fontWeight: 600, marginBottom: "8px" }}>
                  LIVE TINYFISH STREAM CONNECTED
                </div>
                <code style={{ fontSize: "12px", color: "#cbd5e1", display: "block", marginBottom: "14px" }}>
                  {response.streaming_url}
                </code>
                <p style={{ fontSize: "13px", color: "#94a3b8", maxWidth: "420px" }}>
                  In production with your <code>TINYFISH_API_KEY</code>, this iframe renders the live interactive cloud browser where the user watches form fills, OTP relays, and two-step account deletions in real time.
                </p>
              </div>
            ) : (
              <p style={{ color: "#64748b", fontSize: "13px" }}>
                TinyFish Browser stream will appear here whenever an agent navigates, compares, fills a form, or walks to an account deletion screen.
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
