import { useState } from "react";

const ImageUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select an image");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const response = await fetch("http://127.0.0.1:5000/classify", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div className="flex flex-col items-center gap-4">
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} className="bg-green-500 text-white p-2 rounded">
        Upload & Classify
      </button>
      {result && (
        <div className="mt-4">
          <h2>Classification Result:</h2>
          <p className="text-xl font-semibold">{result.classification}</p>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;