import React from "react";
import ReactDOM from "react-dom/client";
const Para=()=>{
    return(
        <div>
            <p className="ml-[300px]">hello world</p>
        </div>
    );
}
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Para/>)
