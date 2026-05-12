# TripGenie AI 🌍✈️

An AI-powered trip planning application that helps users create personalized travel itineraries, manage group expenses, and get AI assistance for travel-related questions.

## 🎯 Features

### 1. **AI Trip Planner**
- Generate customized trip itineraries based on destination, duration, budget, and number of travelers
- Detailed day-by-day activities including morning, afternoon, and evening plans
- Hotel recommendations based on budget constraints
- Support for multiple Indian destinations (Jaipur, Goa, Manali)

### 2. **Expense Manager**
- Track and manage trip expenses for group travel
- Split expenses among multiple travelers
- Categorize expenses for better organization
- Generate settlement summaries to simplify payment distribution
- Track who paid for what and settle balances efficiently

### 3. **AI Chatbot (TripGenie)**
- Get instant answers to travel-related questions
- Powered by OpenAI GPT-3.5 Turbo via OpenRouter API
- Context-aware responses for trip planning assistance

## 💻 Tech Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.x
- **API Communication**: RESTful API with CORS support
- **AI Integration**: OpenRouter API (OpenAI GPT-3.5 Turbo)
- **Database**: (Configurable - structure in place)

### Frontend
- **Framework**: Next.js 16.2.6
- **Language**: TypeScript & React 19
- **Styling**: Tailwind CSS 4
- **UI Components**: Shadcn/UI, Radix UI
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Charts**: Recharts
- **HTTP Client**: Axios
- **Build Tool**: ESLint

## 📁 Project Structure

```
tripgen-ai/
├── backend/
│   └── app/
│       ├── __init__.py
│       ├── main.py              # FastAPI application setup
│       ├── ai_service.py        # AI service utilities
│       ├── database.py          # Database configuration
│       └── routes/
│           ├── trip_routes.py   # Trip planning endpoints
│           └── chat_routes.py   # Chat/AI endpoints
│
└── frontend/
    ├── app/
    │   ├── layout.tsx           # Root layout
    │   ├── page.tsx             # Home page
    │   └── globals.css          # Global styles
    ├── components/
    │   ├── custom/
    │   │   ├── TripForm.tsx      # Trip form component
    │   │   ├── ItineraryCard.tsx # Display itinerary results
    │   │   ├── ExpenseCard.tsx   # Expense manager component
    │   │   ├── ChatbotCard.tsx   # AI chatbot interface
    │   │   └── Navbar.tsx        # Navigation bar
    │   └── ui/                  # Reusable UI components
    ├── lib/
    │   ├── api.ts               # API utilities
    │   └── utils.ts             # Helper functions
    └── public/                  # Static assets
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenRouter API Key (for AI features)

### Backend Setup

1. **Navigate to project root and activate virtual environment**:
   ```bash
   cd tripgen-ai
   .venv\Scripts\Activate.ps1  # Windows PowerShell
   ```

2. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn python-dotenv requests pydantic
   ```

3. **Set up environment variables** (create `.env` in backend):
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

4. **Run the backend server**:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run development server**:
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:3000`

## 📡 API Endpoints

### Trip Planning
- **POST** `/generate-trip`
  - Generate a customized trip itinerary
  - Request body:
    ```json
    {
      "destination": "jaipur",
      "days": 5,
      "travelers": 4,
      "budget": 50000,
      "current_location": "Delhi"
    }
    ```
  - Returns: Itinerary with daily activities and hotel recommendations

### Chat/AI
- **POST** `/chat`
  - Get AI assistance for travel questions
  - Request body:
    ```json
    {
      "message": "What should I pack for a trip to Goa?"
    }
    ```
  - Returns: AI-generated response

### Health Check
- **GET** `/`
  - Returns: `{"message": "TripAI backend running"}`

## 🔧 Configuration

### Supported Destinations
Currently supports:
- **Jaipur** - Historical & cultural sites
- **Goa** - Beach & adventure activities
- **Manali** - Mountain & adventure activities

### Budget-Based Hotel Recommendations
- Budget < ₹10,000: Budget hotels and hostels
- Budget ₹10,000 - ₹50,000: Mid-range hotels
- Budget > ₹50,000: Luxury hotels

## 🌟 Key Features in Detail

### Trip Form Component
Users input:
- Destination (select from available options)
- Number of days
- Number of travelers
- Total budget
- Starting location (defaults to Delhi)

### AI Chatbot
- Context-aware travel advice
- Powered by GPT-3.5 Turbo
- Real-time responses

### Expense Splitting
- Track individual expenses
- Automatic calculation of who owes whom
- Settlement tracking for group trips

## 🔐 Security Features
- CORS middleware enabled for API access control
- Environment variables for sensitive data
- Error handling on both frontend and backend

## 📝 Development Notes
- The backend includes comprehensive error handling and debugging logs
- Frontend uses TypeScript for type safety
- Responsive design with Tailwind CSS
- Component-based architecture for maintainability

## 🚧 Future Enhancements
- Database integration for persistent data storage
- User authentication system
- Payment gateway integration
- Multi-language support
- Real-time expense splitting notifications
- Integration with booking platforms

## 🤝 Contributing
Feel free to fork, modify, and improve this project. Make sure to test both frontend and backend changes.

## 📄 License
This project is open source and available for personal and educational use.

## 📧 Support
For issues, questions, or suggestions, please refer to the project documentation or create an issue in the repository.

---

**Happy Planning! 🎉**
