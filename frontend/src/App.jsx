import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import Recommendations from "./components/Recommendations";

function App() {
  const [recommendations, setRecommendations] = useState([]);

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Book Assist</h1>
      <UploadForm setRecommendations={setRecommendations} />
      <Recommendations recommendations={recommendations} />
    </div>
  );
}

export default App;

