import React, { useState } from 'react';
import './App.css';

function App() {
  const[ facts, setFacts] = useState("")

  function factsonradom(){

    fetch('/json')
    .then((res)=> res.json())
    .then ((data) => setFacts(data))
  }
  return (
    <div className="App">
      <button onClick={factsonradom} >Click For A Fact</button>
      <h1>{facts}</h1>
    </div>

  );
}

export default App;
