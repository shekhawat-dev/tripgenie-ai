"use client";

import { useState } from "react";

import TripForm from "@/components/custom/TripForm";
import ItineraryCard from "@/components/custom/ItineraryCard";
import ChatbotCard from "@/components/custom/ChatbotCard";
import ExpenseManager from "@/components/custom/ExpenseCard";

export default function Home() {
  const [activeTab, setActiveTab] = useState("trip");
  const [itinerary, setItinerary] = useState<any>(null);

  console.log("Current itinerary state:", itinerary);

  return (
    <main className="min-h-screen bg-gray-100 p-6">

      {/* Top Trip Form */}
      <TripForm setItinerary={setItinerary} />

      {/* Tabs */}
      <div className="flex flex-wrap gap-4 mt-6 mb-6">
        <button
          onClick={() => setActiveTab("trip")}
          className={`px-6 py-3 rounded-xl font-semibold ${activeTab === "trip"
            ? "bg-purple-600 text-white"
            : "bg-white"
            }`}
        >
          AI Trip Planner
        </button>

        <button
          onClick={() => setActiveTab("expense")}
          className={`px-6 py-3 rounded-xl font-semibold ${activeTab === "expense"
            ? "bg-purple-600 text-white"
            : "bg-white"
            }`}
        >
          Expense Manager
        </button>

        <button
          onClick={() => setActiveTab("chat")}
          className={`px-6 py-3 rounded-xl font-semibold ${activeTab === "chat"
            ? "bg-purple-600 text-white"
            : "bg-white"
            }`}
        >
          AI Travel Assistant
        </button>
      </div>

      {/* Trip Planner Section */}
      {activeTab === "trip" && (
        <ItineraryCard itinerary={itinerary} />
      )}

      {/* Expense Section */}
      {activeTab === "expense" && (
        <ExpenseManager />
      )}

      {/* Chat Section */}
      {activeTab === "chat" && (
        <ChatbotCard />
      )}
    </main>
  );
}