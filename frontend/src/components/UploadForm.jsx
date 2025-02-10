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
    <div className="max-w-lg mx-auto bg-white shadow-lg rounded-lg p-6 mt-10">
      <h2 className="text-2xl font-semibold text-gray-700 mb-4 text-center">Upload Your Book List</h2>
      <form onSubmit={handleUpload} className="flex flex-col items-center space-y-4">
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          className="border border-gray-300 p-2 rounded w-full cursor-pointer"
        />
        <button
          type="submit"
          className={`px-4 py-2 rounded-lg text-white font-semibold transition ${
            loading ? "bg-gray-400" : "bg-blue-500 hover:bg-blue-600"
          }`}
          disabled={loading}
        >
          {loading ? "Uploading..." : "Get Recommendations"}
        </button>
      </form>
    </div>
  );
}

export default UploadForm;
