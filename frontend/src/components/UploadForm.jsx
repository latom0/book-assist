import React, { useState } from "react";
import axios from "axios";

function UploadForm({ setRecommendations }) {
  const [file, setFile] = useState(null);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload", formData);
      setRecommendations(response.data.recommendations);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <form onSubmit={handleUpload} className="flex flex-col items-center space-y-3">
      <input type="file" onChange={(e) => setFile(e.target.files[0])} className="border p-2" />
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">Get Recommendations</button>
    </form>
  );
}

export default UploadForm;
