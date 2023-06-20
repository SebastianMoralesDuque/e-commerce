import React, { useEffect, useState } from 'react';
import { getAllUsers } from './graphql/api';

function App() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const usersData = await getAllUsers();
        setUsers(usersData);
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Backend Django y Frontend React con Vite</h1>
      {users.length > 0 && (
        <ul>
          {users.map((user, i) => (
            <li key={i}>{user.email}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
