import React, { useState } from 'react';
import axios from 'axios';

function Crons() {
    const [link, setLink] = useState('');
    const [crontime, setCrontime] = useState('');
    const [xpaths, setXpaths] = useState([{ label: '', xpath: '' }]);
    const [linkError, setLinkError] = useState('');
  
    const handleLinkChange = (e) => {
      const inputValue = e.target.value;
      setLink(inputValue);
      // Validate the link using a regular expression
      const urlPattern = /^(https?|ftp|file)?:\/\/[-a-zA-Z0-9+&@#/%?=~_|!:,.;]+[-a-zA-Z0-9+&@#/%=~_|]$/;
      if (!urlPattern.test(inputValue)) {
        setLinkError('Please enter a valid URL');
      } else {
        setLinkError('');
      }
    };
    const handleTimeChange = (e) =>{
        const Cronstime = e.target.value;
        setCrontime(Cronstime);
    };
  
    const handleAddXPath = () => {
      setXpaths([...xpaths, { label: '', xpath: '' }]);
    };
  
    const handleRemoveXPath = (index) => {
      const updatedXpaths = [...xpaths];
      updatedXpaths.splice(index, 1);
      setXpaths(updatedXpaths);
    };
  
    const handleXPathChange = (index, field, value) => {
      const updatedXpaths = [...xpaths];
      updatedXpaths[index][field] = value;
      setXpaths(updatedXpaths);
    };
  
    const handleSubmit = () => {
      // Check if the link is valid before submitting
      if (!linkError) {
        const data = {
          link,
          xpaths,
          crontime,
          
        };
  
        axios
          .post('http://127.0.0.1:5000/api/addcrons', data)
          .then((response) => {
            alert('Data saved successfully:', response.data);
            // Add further logic here, such as displaying a success message.
          })
          .catch((error) => {
            console.error('Error saving data:', error);
            // Handle errors here, such as displaying an error message.
          });
      }
    };
  return (
    <div className="p-4">
      <h1 className="text-2xl mb-4">Web Scraper</h1>
      <div className="mb-4">
        <label htmlFor="linkInput" className="block mb-2">
          Link:
        </label>
        <input
          type="text"
          id="linkInput"
          value={link}
          onChange={handleLinkChange}
          className="w-full px-3 py-2 border rounded-lg shadow-sm focus:outline-none focus:ring focus:border-blue-300"
        />
        {linkError && <p className="text-red-600">{linkError}</p>}
        <label htmlFor="timeInput">Select a time:</label>
      <input
        type="time"
        id="crontime"
        name="crontime"
        value={crontime}
        onChange={handleTimeChange}
        className="w-full px-3 py-2 border rounded-lg shadow-sm focus:outline-none focus:ring focus:border-blue-300"
      />
      </div>
      <h2 className="text-xl mb-4">XPaths:</h2>
      {xpaths.map((xpath, index) => (
        <div key={index} className="flex items-center mb-2">
          <input
            type="text"
            value={xpath.label}
            onChange={(e) => handleXPathChange(index, 'label', e.target.value)}
            placeholder="Label"
            className="w-1/4 px-3 py-2 mr-2 border rounded-lg shadow-sm focus:outline-none focus:ring focus:border-blue-300"
          />
          <input
            type="text"
            value={xpath.xpath}
            onChange={(e) => handleXPathChange(index, 'xpath', e.target.value)}
            placeholder="XPath"
            className="w-3/4 px-3 py-2 mr-2 border rounded-lg shadow-sm focus:outline-none focus:ring focus:border-blue-300"
          />
          <button
            onClick={() => handleRemoveXPath(index)}
            className="bg-red-500 text-white px-2 py-1 rounded-md hover:bg-red-600 focus:outline-none"
          >
            -
          </button>
        </div>
      ))}
      <button
        onClick={handleAddXPath}
        className="bg-green-500 text-white px-2 py-1 rounded-md hover:bg-green-600 focus:outline-none"
      >
        +
      </button>
      <button
        onClick={handleSubmit}
        className="bg-blue-500 text-white px-2 py-1 rounded-md hover:bg-blue-600 focus:outline-none mt-4"
      >
        Submit
      </button>
      
    </div>
  )
}

export default Crons