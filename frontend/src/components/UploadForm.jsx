import React, { useState } from "react";
import axios from "axios";

function UploadForm({ setRecommendations }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true); 

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload", formData);
      setRecommendations(response.data.recommendations);
    } catch (error) {
      console.error("Error uploading file:", error);
    } finally {
      setLoading(false); 
    }
  };

  return (
    <div
      className="flex flex-col items-center justify-center min-h-screen 
                 bg-cover bg-center bg-no-repeat"
      style={{ backgroundImage: "url('/bg.jpg')" }} // Change this to your actual image path
    >
      <div className="bg-white bg-opacity-10 backdrop-blur-lg p-8 rounded-2xl shadow-2xl flex flex-col items-center space-y-6 w-96">
        <h1 className="text-4xl font-bold text-white text-center drop-shadow-lg">
          Upload Your Book List
        </h1>

        <form onSubmit={handleUpload} className="flex flex-col items-center space-y-4 w-full">
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="w-full text-sm text-gray-300 border border-gray-400 rounded-lg cursor-pointer bg-gray-800 focus:outline-none p-2"
          />

          {loading ? (
            <div className="flex justify-center">
              <div className="animate-spin rounded-full h-8 w-8 border-t-4 border-blue-500"></div>
            </div>
          ) : (
            <button
              type="submit"
              className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white 
                         py-2 px-4 rounded-lg font-semibold shadow-md hover:scale-105 
                         transform transition-all hover:shadow-xl"
            >
              Get Recommendations
            </button>
          )}
        </form>
      </div>
    </div>
  );
}

export default UploadForm;
