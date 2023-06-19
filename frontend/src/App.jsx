import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/data') // Ruta de ejemplo para obtener datos desde el backend
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.error(error));
  }, []);

  return (
    <div>
      <h1>Backend Django y Frontend React con Vite</h1>
      {data && <p>{data.message}</p>}
    </div>
  );
}

export default App;
