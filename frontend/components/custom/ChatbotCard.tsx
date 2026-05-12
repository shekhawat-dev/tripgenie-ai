"use client";

import { useState } from "react";

interface ChatMessage {
    type: "user" | "bot";
    message: string;
}

export default function ChatbotCard() {
    const [userQuery, setUserQuery] = useState("");
    const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
    const [loading, setLoading] = useState(false);

    // AI response from backend
    const generateTravelResponse = async (query: string) => {
        try {
            const res = await fetch("http://127.0.0.1:8000/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    message: query,
                }),
            });

            if (!res.ok) {
                return "Bhai backend error aa gaya.";
            }

            const data = await res.json();

            console.log("Backend Response:", data);

            // FIX: backend returns { reply: "..." }
            return (
                data.reply ||
                "Bhai AI response nahi aaya properly."
            );
        } catch (error) {
            console.log("Frontend Error:", error);

            return "TripGenie AI backend se connect nahi ho paaya bhai.";
        }
    };

    const handleAsk = async () => {
        if (!userQuery.trim() || loading) return;

        const currentQuery = userQuery.trim();

        // user message add
        setChatHistory((prev) => [
            ...prev,
            {
                type: "user",
                message: currentQuery,
            },
        ]);

        setUserQuery("");
        setLoading(true);

        // bot response
        const botReply = await generateTravelResponse(currentQuery);

        setChatHistory((prev) => [
            ...prev,
            {
                type: "bot",
                message: botReply,
            },
        ]);

        setLoading(false);
    };

    return (
        <div className="bg-white rounded-2xl shadow-md mt-6 h-[600px] flex flex-col">

            {/* Header */}
            <div className="p-6 border-b">
                <h1 className="text-5xl font-bold text-purple-600">
                    TripGenie AI
                </h1>
            </div>

            {/* Chat Area */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {chatHistory.length === 0 && (
                    <div className="text-gray-500 text-center mt-20">
                        Ask anything about your trip ✈️
                    </div>
                )}

                {chatHistory.map((chat, index) => (
                    <div
                        key={index}
                        className={`flex ${chat.type === "user"
                                ? "justify-end"
                                : "justify-start"
                            }`}
                    >
                        <div
                            className={`max-w-[70%] px-5 py-3 rounded-2xl ${chat.type === "user"
                                    ? "bg-purple-600 text-white"
                                    : "bg-gray-100 text-black"
                                }`}
                        >
                            {chat.message}
                        </div>
                    </div>
                ))}

                {loading && (
                    <div className="flex justify-start">
                        <div className="bg-gray-100 text-black px-5 py-3 rounded-2xl">
                            TripGenie AI is typing...
                        </div>
                    </div>
                )}
            </div>

            {/* Input Section */}
            <div className="p-4 border-t flex gap-3">
                <input
                    type="text"
                    placeholder="Ask anything about your trip..."
                    value={userQuery}
                    onChange={(e) => setUserQuery(e.target.value)}
                    className="flex-1 border rounded-xl px-4 py-3 outline-none"
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            handleAsk();
                        }
                    }}
                />

                <button
                    onClick={handleAsk}
                    disabled={loading}
                    className="bg-purple-600 text-white px-6 py-3 rounded-xl disabled:opacity-50"
                >
                    {loading ? "..." : "Ask"}
                </button>
            </div>
        </div>
    );
}