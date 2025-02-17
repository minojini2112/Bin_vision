import React from "react";
import ReactDOM from "react-dom/client";
import ImageUpload from "./Components/Homepage/ImageUpload"; // Ensure path matches your file structure

const Para = () => {
  return (
    <div>
      <ImageUpload />
    </div>
  );
};

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Para />);
