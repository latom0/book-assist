import React from "react";

function Recommendations({ recommendations }) {
  return (
    <div className="mt-5">
      <h2 className="text-xl font-semibold">Recommended Books:</h2>
      <ul className="mt-2">
        {recommendations.map((book, index) => (
          <li key={index} className="p-2 border-b">{book}</li>
        ))}
      </ul>
    </div>
  );
}

export default Recommendations;
