import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import Recommendations from "./components/Recommendations";

function App() {
  const [recommendations, setRecommendations] = useState([]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-5">
      <h1 className="text-3xl font-bold mb-4">AI Book Recommender</h1>
      <UploadForm setRecommendations={setRecommendations} />
      <Recommendations recommendations={recommendations} />
    </div>
  );
}

export default App;
