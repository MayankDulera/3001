import React, { useState, useEffect } from 'react';
import axios from 'axios';

function YourCrons() {
  const [savedCrons, setSavedCrons] = useState([]);
  const [selectedCrons, setSelectedCrons] = useState([]);
  const [selectAll, setSelectAll] = useState(false); // Track the "Select All" checkbox state

     // Function to fetch saved links from the API
  const fetchSavedCrons = () => {
    axios
      .get('http://127.0.0.1:5000/api/savedcrons') // Replace with your Flask API endpoint
      .then((response) => {
        console.log(response)
        setSavedCrons(response.data); // Assuming the API returns an array of saved links
      })
      .catch((error) => {
        console.error('Error fetching saved links:', error);
      });
  };

  useEffect(() => {
    fetchSavedCrons();
  }, []); // Fetch saved links when the component mounts


  // Function to handle "Select All" checkbox
const handleSelectAllChange = (event) => {
    const isChecked = event.target.checked;
    setSelectAll(isChecked);
  
    if (isChecked) {
      setSelectedCrons([...savedCrons]);
    } else {
        setSelectedCrons([]);
    }
  };


    // Function to handle checkbox changes
    const handleCheckboxChange = (event, link) => {
        if (event.target.checked) {
          setSelectedCrons([...selectedCrons, link]);
        } else {
          setSelectedCrons(selectedCrons.filter((selectedCrons) => selectedCrons !== link));
        }
      };



       // Function to perform an action when the button is clicked
  const handleButtonClick = () => {
    // Do something with the selected links (selectedLinks array)
    console.log('Selected Links:', selectedCrons);
    const flaskEndpoint = 'http://127.0.0.1:5000/api/process_selected_links';

    axios
      .post(flaskEndpoint, { selectedCrons })
      .then((response) => {
        console.log('API Response:', response.data);
        // Handle the response from the Flask API as needed
      })
      .catch((error) => {
        console.error('Error calling the Flask API:', error);
      });
  };


   // Function to handle deletion of selected links
   const handleDeleteSelected = () => {
    const flaskEndpoint = 'http://127.0.0.1:5000/api/delete_selected_crons';

    axios
      .post(flaskEndpoint, { selectedCrons })
      .then((response) => {
        console.log('Deleted Links:', selectedCrons);
        console.log('API Response:', response.data);
        // Handle the response from the Flask API as needed
        fetchSavedCrons(); // Refresh the list of saved links after deletion
      })
      .catch((error) => {
        console.error('Error calling the Flask API for deletion:', error);
      });
  };
  return (
    <div className="p-4">
    <h1 className="text-2xl mb-4">Saved Crons</h1>
    <label>
      <input
        type="checkbox"
        checked={selectAll}
        onChange={handleSelectAllChange}
      /> Select All
    </label>
    <ul>
      {savedCrons.map((links) => (
        <li key={links.id}><input
        type="checkbox"
        onChange={(event) => handleCheckboxChange(event, links)}
        checked={selectedCrons.includes(links)}
      />{links.domain}{links.time}</li>
      
      ))}
    </ul>
    {/* <button
      onClick={handleButtonClick}
      className="bg-blue-500 text-white px-2 py-1 rounded-md hover:bg-blue-600 focus:outline-none mt-4"
    >
      Perform Action
    </button> */}
    <button
      onClick={handleDeleteSelected}
      className="bg-red-500 text-white px-2 py-1 rounded-md hover:bg-red-600 focus:outline-none mt-4"
    >
      Delete Selected
    </button>
    <button
      onClick={fetchSavedCrons}
      className="bg-blue-500 text-white px-2 py-1 rounded-md hover:bg-blue-600 focus:outline-none mt-4"
    >
      Refresh Links
    </button>
    {/* Add a button to call the web scraping API here */}
  </div>
  )
}

export default YourCrons