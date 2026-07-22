"use client";

import { useState } from "react";
import axios from "axios";

export default function TripForm({ setItinerary }: any) {
    const [destination, setDestination] = useState("");
    const [days, setDays] = useState("");
    const [travelers, setTravelers] = useState("");
    const [budget, setBudget] = useState("");
    const [locationMessage, setLocationMessage] = useState("");

    const handleGenerateTrip = async () => {
        try {
            let latitude = null;
            let longitude = null;

            if (typeof window !== "undefined" && navigator.geolocation) {
                try {
                    const position = await new Promise<GeolocationPosition>((resolve, reject) => {
                        navigator.geolocation.getCurrentPosition(resolve, reject, {
                            enableHighAccuracy: true,
                            timeout: 10000,
                        });
                    });

                    latitude = position.coords.latitude;
                    longitude = position.coords.longitude;
                    setLocationMessage("Using your current location for the trip plan.");
                } catch {
                    setLocationMessage("Location permission denied. Please select your city manually.");
                }
            } else {
                setLocationMessage("Location services are unavailable. Please select your city manually.");
            }

            const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
            const response = await axios.post(
                `${API_BASE}/generate-trip`,
                {
                    destination,
                    days,
                    travelers,
                    budget,
                    latitude,
                    longitude,
                }
            );

            setItinerary(response.data);

        } catch (error) {
            console.log("Trip generation error:", error);
        }
    };

    return (
        <div className="bg-white p-8 rounded-3xl shadow-md mb-6">
            <h1 className="text-5xl font-bold mb-8">
                Plan Your Next Trip with{" "}
                <span className="text-purple-600">AI</span>
            </h1>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">

                <input
                    type="text"
                    placeholder="Destination"
                    value={destination}
                    onChange={(e) => setDestination(e.target.value)}
                    className="border p-4 rounded-xl"
                />

                <input
                    type="number"
                    placeholder="Days"
                    value={days}
                    onChange={(e) => setDays(e.target.value)}
                    className="border p-4 rounded-xl"
                />

                <input
                    type="number"
                    placeholder="Travelers"
                    value={travelers}
                    onChange={(e) => setTravelers(e.target.value)}
                    className="border p-4 rounded-xl"
                />

                <input
                    type="number"
                    placeholder="Budget"
                    value={budget}
                    onChange={(e) => setBudget(e.target.value)}
                    className="border p-4 rounded-xl"
                />
            </div>

            {locationMessage ? (
                <p className="text-sm text-gray-500 mb-4">{locationMessage}</p>
            ) : null}

            <button
                onClick={handleGenerateTrip}
                className="bg-purple-600 text-white px-8 py-4 rounded-xl"
            >
                Generate Trip
            </button>
        </div>
    );
}