import React, { useState, useEffect } from 'react';
import axios from 'axios';

const LinkList = () => {
  const [savedLinks, setSavedLinks] = useState([]);
  const [selectedLinks, setSelectedLinks] = useState([]);
  const [selectAll, setSelectAll] = useState(false); // Track the "Select All" checkbox state

  // Function to fetch saved links from the API
  const fetchSavedLinks = () => {
    axios
      .get('http://127.0.0.1:5000/api/savedlinks') // Replace with your Flask API endpoint
      .then((response) => {
        console.log(response)
        setSavedLinks(response.data); // Assuming the API returns an array of saved links
      })
      .catch((error) => {
        console.error('Error fetching saved links:', error);
      });
  };

  useEffect(() => {
    fetchSavedLinks();
  }, []); // Fetch saved links when the component mounts

  // Function to handle checkbox changes
  const handleCheckboxChange = (event, link) => {
    if (event.target.checked) {
      setSelectedLinks([...selectedLinks, link]);
    } else {
      setSelectedLinks(selectedLinks.filter((selectedLink) => selectedLink !== link));
    }
  };


// Function to handle "Select All" checkbox
const handleSelectAllChange = (event) => {
  const isChecked = event.target.checked;
  setSelectAll(isChecked);

  if (isChecked) {
    setSelectedLinks([...savedLinks]);
  } else {
    setSelectedLinks([]);
  }
};

  // Function to perform an action when the button is clicked
  const handleButtonClick = () => {
    // Do something with the selected links (selectedLinks array)
    console.log('Selected Links:', selectedLinks);
    const flaskEndpoint = 'http://127.0.0.1:5000/api/process_selected_links';

    axios
      .post(flaskEndpoint, { selectedLinks })
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
    const flaskEndpoint = 'http://127.0.0.1:5000/api/delete_selected_links';

    axios
      .post(flaskEndpoint, { selectedLinks })
      .then((response) => {
        console.log('Deleted Links:', selectedLinks);
        console.log('API Response:', response.data);
        // Handle the response from the Flask API as needed
        fetchSavedLinks(); // Refresh the list of saved links after deletion
      })
      .catch((error) => {
        console.error('Error calling the Flask API for deletion:', error);
      });
  };
  return (
    <div className="p-4">
      <h1 className="text-2xl mb-4">Saved Links</h1>
      <label>
        <input
          type="checkbox"
          checked={selectAll}
          onChange={handleSelectAllChange}
        /> Select All
      </label>
      <ul>
        {savedLinks.map((links) => (
          <li key={links.id}><input
          type="checkbox"
          onChange={(event) => handleCheckboxChange(event, links)}
          checked={selectedLinks.includes(links)}
        />{links.links}</li>
        ))}
      </ul>
      <button
        onClick={handleButtonClick}
        className="bg-blue-500 text-white px-2 py-1 rounded-md hover:bg-blue-600 focus:outline-none mt-4"
      >
        Perform Action
      </button>
      <button
        onClick={handleDeleteSelected}
        className="bg-red-500 text-white px-2 py-1 rounded-md hover:bg-red-600 focus:outline-none mt-4"
      >
        Delete Selected
      </button>
      <button
        onClick={fetchSavedLinks}
        className="bg-blue-500 text-white px-2 py-1 rounded-md hover:bg-blue-600 focus:outline-none mt-4"
      >
        Refresh Links
      </button>
      {/* Add a button to call the web scraping API here */}
    </div>
  );
};

export default LinkList;
