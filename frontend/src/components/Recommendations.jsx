import React from "react";

function Recommendations({ recommendations }) {
  return (
    <div className="max-w-2xl mx-auto mt-10">
      <h2 className="text-2xl font-bold text-gray-800 mb-4 text-center">Recommended Books</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {recommendations.length === 0 ? (
          <p className="text-gray-600 text-center">No recommendations yet. Upload a file!</p>
        ) : (
          recommendations.map((book, index) => (
            <div key={index} className="bg-white shadow-md rounded-lg p-4">
              <h3 className="text-lg font-semibold">{book}</h3>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Recommendations;

