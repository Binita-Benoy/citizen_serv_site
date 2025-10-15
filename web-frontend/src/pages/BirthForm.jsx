import { useState } from "react";
import api from "../services/apiClient";

export default function BirthForm() {
  const [form, setForm] = useState({
    applicant_name: "",
    date_of_birth: "",
    place_of_birth: "",
    father_name: "",
    mother_name: "",
    address: ""
  });
  const [message, setMessage] = useState("");

  const onChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    const res = await api.post("/applications", form);
    setMessage(`Created application #${res.data.id} (${res.data.status})`);
  };

  return (
    <form onSubmit={submit} style={{maxWidth: 520, margin: "1rem auto"}}>
      <h2>Birth Certificate Application</h2>
      <input name="applicant_name" placeholder="Applicant name" onChange={onChange} required />
      <input type="date" name="date_of_birth" onChange={onChange} required />
      <input name="place_of_birth" placeholder="Place of birth" onChange={onChange} required />
      <input name="father_name" placeholder="Father name" onChange={onChange} />
      <input name="mother_name" placeholder="Mother name" onChange={onChange} />
      <textarea name="address" placeholder="Address" onChange={onChange} />
      <button type="submit">Submit</button>
      <div>{message}</div>
    </form>
  );
}
