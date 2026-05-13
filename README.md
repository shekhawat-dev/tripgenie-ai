# TripGenie AI 🌍✈️

> An AI-powered trip planning app with smart itineraries, budget tracking, hotel recommendations, and a travel chatbot.

🔗 **Live Demo**: [tripgenie-ai-i4nd.vercel.app](https://tripgenie-ai-i4nd.vercel.app)

---

## Features

### 🗺️ AI Trip Planner
Generate personalized day-by-day itineraries based on your destination, duration, budget, and number of travelers. Includes morning, afternoon, and evening activity suggestions along with hotel recommendations tailored to your budget.

### 💸 Expense Manager
Track and split group travel expenses effortlessly. Categorize spending, see who paid for what, and get automatic settlement summaries so no one ends up out of pocket.

### 🤖 AI Travel Assistant (TripGenie)
Chat with an AI travel assistant powered by GPT-3.5 Turbo for instant, context-aware answers to all your travel questions.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16, React 19, TypeScript |
| Styling | Tailwind CSS 4, Shadcn/UI, Framer Motion |
| Charts | Recharts |
| Backend | FastAPI, Python 3.11 |
| AI | OpenRouter API (GPT-3.5 Turbo) |
| Deployment | Vercel (frontend) + Render (backend) |

---

## Project Structure

```
tripgenie-ai/
├── backend/
│   └── app/
│       ├── main.py              # FastAPI app & CORS setup
│       ├── ai_service.py        # AI service utilities
│       ├── database.py          # Database configuration
│       └── routes/
│           ├── trip_routes.py   # Trip planning endpoints
│           └── chat_routes.py   # Chatbot endpoints
│
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── custom/
│   │   │   ├── TripForm.tsx
│   │   │   ├── ItineraryCard.tsx
│   │   │   ├── ExpenseCard.tsx
│   │   │   ├── ChatbotCard.tsx
│   │   │   └── Navbar.tsx
│   │   └── ui/
│   └── lib/
│       ├── api.ts
│       └── utils.ts
│
├── requirements.txt
└── render.yaml
```

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 16+
- OpenRouter API Key → [openrouter.ai](https://openrouter.ai)

### Backend Setup

```bash
# From project root
pip install -r requirements.txt

# Create .env file inside backend/
echo "OPENROUTER_API_KEY=your_key_here" > backend/.env

# Start the server
cd backend
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Install and run
npm install
npm run dev
```

Frontend runs at `http://localhost:3000`

---

## API Endpoints

### `POST /generate-trip`
Generate a trip itinerary.
```json
{
  "destination": "jaipur",
  "days": 5,
  "travelers": 4,
  "budget": 50000,
  "current_location": "Delhi"
}
```

### `POST /chat`
Chat with the AI travel assistant.
```json
{
  "message": "What should I pack for Goa in December?"
}
```

### `GET /`
Health check → `{"message": "TripAI backend running"}`

---

## Supported Destinations

| Destination | Highlights |
|---|---|
| 🏰 Jaipur | Historical & cultural sites |
| 🏖️ Goa | Beaches & nightlife |
| 🏔️ Manali | Mountains & adventure |

### Budget-Based Hotel Recommendations
- Under ₹10,000 → Budget hotels & hostels
- ₹10,000 – ₹50,000 → Mid-range hotels
- Above ₹50,000 → Luxury hotels

---

## Deployment

| Service | Platform | URL |
|---|---|---|
| Frontend | Vercel | [tripgenie-ai-i4nd.vercel.app](https://tripgenie-ai-i4nd.vercel.app) |
| Backend | Render | [tripgenie-ai-09dw.onrender.com](https://tripgenie-ai-09dw.onrender.com) |

> **Note:** The backend is hosted on Render's free tier and may take 30–60 seconds to wake up after inactivity.

---

## Roadmap

- [ ] Database integration for persistent storage
- [ ] User authentication
- [ ] More Indian destinations
- [ ] Real-time expense notifications
- [ ] Booking platform integration
- [ ] Multi-language support

---

## Contributing

Fork the repo, make your changes, and open a pull request. Please test both frontend and backend before submitting.

---

## License

Open source — free for personal and educational use.

---

Made with ❤️ by [shekhawat-dev](https://github.com/shekhawat-dev)
