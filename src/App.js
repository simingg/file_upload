import { useEffect, useState } from 'react'
import axios from "axios";
import './App.css';

function App() {
  const [images, setImages] = useState([])
  const [file, setFile] = useState()

  function getImage(filename) {
    axios({
      method: "GET",
      url: "/serve-image/<filename>",
      data: filename
    }).then((response) => {
      const res = response.data
      setImages([...images, res])
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
      }
    })
  }
  const submitImage = () => {
    const formData = new FormData()
    formData.append("file", file);
    axios.post('/upload', formData).then((res) => {
       console.log(res)
    }).catch(err => console.log(err))
  }

  useEffect(() => {
    //initial loading of all images
    axios.post("/images").then ((res) => {
      setImages(res);
    })
  }, [])

  return (
    <div className="App">
      <div className="form-section">
        <form>
          <label> Input your image</label>
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <button onClick={submitImage}> Submit Image</button>
        </form>
      </div>
      <div className="image-secion">
        {images.map((image) => {
          <a href="image">
            <img src="image" />
          </a>
        })}

      </div>
    </div>
  );
}

export default App;
