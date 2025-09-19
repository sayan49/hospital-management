import { useState, useEffect } from "react";
import axios from "axios";
import { API_URL } from "./config";

function App() {
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    axios.get(`${API_URL}/patients/`)
      .then(res => setPatients(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-6">🏥 Hospital Patient Dashboard</h1>
      <table className="table-auto w-full border-collapse border border-gray-300 bg-white shadow-md">
        <thead>
          <tr className="bg-gray-200">
            <th className="border px-4 py-2">Room No</th>
            <th className="border px-4 py-2">Name</th>
            <th className="border px-4 py-2">Condition</th>
            <th className="border px-4 py-2">Surgeries</th>
            <th className="border px-4 py-2">Medications</th>
            <th className="border px-4 py-2">Guardian</th>
          </tr>
        </thead>
        <tbody>
          {patients.map((p) => (
            <tr key={p.id} className="text-center">
              <td className="border px-4 py-2">{p.room_no}</td>
              <td className="border px-4 py-2">{p.name}</td>
              <td className="border px-4 py-2">{p.current_condition}</td>
              <td className="border px-4 py-2">{p.surgeries.map(s => s.type).join(", ")}</td>
              <td className="border px-4 py-2">{p.medications.map(m => `${m.name} (${m.dosage})`).join(", ")}</td>
              <td className="border px-4 py-2">{p.guardian_name}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
