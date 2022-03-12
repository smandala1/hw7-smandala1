import React, { createFactory, useState } from 'react';
import './App.css';

function App() {
  const [movies, setMovies] = useState("")

  function moviesonrandom() {

    fetch('/movies')
      .then((res) => res.json())
      .then((data) => setMovies(data))
  }
  return (
    <div className="App">
      <h1>Movie </h1>
      {fact.map(review =>
        <table>
          <tr>
            <td align='center'>Movie_id: {review.Movie_id}</td>
            <td align='center'><b>Rating</b><input type="text" value={review.ratings} /></td>
            <td align='center'><b>Comments</b><input type="text" value={review.Comments} /></td>
            <td><button type="submit" onClick={deleteButton(review.id)}>Delete the review</button></td>
          </tr>
        </table>

      )}

    </div>

  );
}

export default App;
