import { useEffect, useState } from 'react'
import axios from "axios";
import './App.css';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';

function App() {
  const [images, setImages] = useState([])
  const [file, setFile] = useState()

  const submitImage =  (e) => {
    e.preventDefault();
    const formData = new FormData()
    formData.append("file", file);
    console.log(formData.get('file'))
    axios.post('/upload', formData).then((res) => {
      window.location.reload(false);
    }).catch(err => console.log(err))

  }

  useEffect(() => {
    async function getImages() {
    //initial loading of all images
      await axios.get("/images").then((res) => {
        setImages(res.data)
      })
    }
    getImages()
  }, [images])

  return (
    <div className="App">
      <div className="form-section">
      <label> Input your image</label>
        <form onSubmit={submitImage}>
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <button type="submit"> Submit Image</button>
        </form>
      </div>
      <div className="image-section">
        <ImageList sx={{width:500, height :450}} cols={3} rowHeight={164}>
            {images.map((data, idx) => (
              <ImageListItem key={idx}>
                <img src={`data:image/jpg;base64, ${data}`} />
              </ImageListItem>
            ))
      }
      </ImageList>
      </div>
    </div>
  );
}

export default App;
