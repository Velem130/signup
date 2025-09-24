// frontend/src/pages/Home.jsx

import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <h1 className="text-4xl font-bold mb-4">Welcome to the Registration Portal</h1>
      <Link to="/register" className="px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-700">
        Register
      </Link>
    </div>
  );
}

export default Home;
