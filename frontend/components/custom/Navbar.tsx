import { MapPin, Sun } from "lucide-react";

export default function Navbar() {
    return (
        <div className="bg-white rounded-2xl px-6 py-4 shadow-sm flex items-center justify-between w-full">

            {/* Left empty space */}
            <div className="w-20"></div>

            {/* Center logo */}
            <div className="flex items-center gap-2 mx-auto">
                <MapPin className="text-purple-600 w-5 h-5" />

                <div className="flex flex-col leading-tight">
                    <h1 className="font-bold text-lg text-purple-600">
                        TripAI
                    </h1>

                    <p className="text-xs text-gray-500">
                        Plan Smarter, Travel Better
                    </p>
                </div>
            </div>

            {/* Right section */}
            <div className="flex items-center gap-4">
                <Sun className="text-gray-500 cursor-pointer" />

                <div className="w-10 h-10 rounded-full bg-purple-600 text-white flex items-center justify-center">
                    A
                </div>
            </div>
        </div>
    );
}