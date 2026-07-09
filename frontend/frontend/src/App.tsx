import { useEffect, useState } from "react";
import api from "./services/api";

function App() {
  const [status, setStatus] = useState("Checking...");

  useEffect(() => {
    api.get("/health")
      .then((response) => {
        setStatus(response.data.status);
      })
      .catch(() => {
        setStatus("Backend Not Reachable");
      });
  }, []);

  return (
    <div style={{ padding: "40px" }}>
      <h1>TwinForge</h1>
      <h2>Backend Status: {status}</h2>
    </div>
  );
}

export default App;