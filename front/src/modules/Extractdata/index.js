import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { saveAs } from 'file-saver'; // For downloading files
import jsPDF from 'jspdf';


function ExtractData() {
  const [data, setData] = useState([]);
  const [selectedRow, setSelectedRow] = useState(null);
  const [dynamicTableData, setDynamicTableData] = useState([]);
  const [exportFormat, setExportFormat] = useState('csv'); // Default to CSV

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/get_scraped_data');
      setData(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const handleRowClick = async (id) => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/api/get_scraped_data_by_id/${id}`);

      // Filter out the "id" field before setting the dynamic table data
      const filteredData = { ...response.data };
      delete filteredData.id;

      setDynamicTableData(filteredData);
      setSelectedRow(id);
    } catch (error) {
      console.error('Error fetching dynamic data:', error);
    }
  };

  const handleDelete = (id) => {
    // Implement the delete functionality here and refresh the data after successful deletion.
    axios.delete(`http://127.0.0.1:5000/api/delete_data/${id}`)
      .then((response) => {
        // Handle the success case here
        console.log('Data deleted successfully', response.data);
        fetchData();
        // Refresh the data after successful deletion
        // You can implement a function to update your data here, e.g., fetching the updated data from the server.
        // For example, you can call a function to update the state that holds the list of items.
      })
      .catch((error) => {
        // Handle any errors that occur during the delete request
        console.error('Error deleting data', error);
      });
  };


  const handleExport = () => {
    if (exportFormat === 'csv') {
      exportToCSV();
    } else if (exportFormat === 'pdf') {
      exportToPDF();
    }
  };

  const exportToCSV = () => {
    // Generate and export CSV here
    const fileName = prompt('Enter the filename for the PDF', 'data.csv');
  if (!fileName) {
    // User canceled or didn't provide a filename
    return;
  }
  console.log(dynamicTableData)
    const csvData = 'Header,Data\n' +
      Object.entries(dynamicTableData)
        .map(([key, value]) => `"${key}","${value}"`)
        .join('\n');
      
    const blob = new Blob([csvData], { type: 'text/csv' });
    saveAs(blob, fileName);
  };

  const exportToPDF = () => {
    const fileName = prompt('Enter the filename for the PDF', 'data.pdf');
  if (!fileName) {
    // User canceled or didn't provide a filename
    return;
  }
    // Create a new jsPDF instance
    const pdfDoc = new jsPDF();
  
    // Set the title for your PDF (optional)
    pdfDoc.setProperties({
      title: 'Dynamic Data PDF Export',
    });
  
    // Define the position for the starting point of your content
    let posY = 10;
  
    // Iterate over dynamicTableData and add the data to the PDF
    Object.entries(dynamicTableData).forEach(([key, value]) => {
      // pdfDoc.text(10, posY, key);
      pdfDoc.text(6, posY, value);
      posY += 10;
    });
  
    // Save the PDF with a specific name
    pdfDoc.save(fileName);
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-semibold mb-4">Data Table</h1>
      <table className="table-auto w-full">
        <thead>
          <tr>
            <th className="px-4 py-2">ID</th>
            <th className="px-4 py-2">URL</th>
            <th className="px-4 py-2">Action</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item) => (
            <tr >
              <td key={item.id} onClick={() => handleRowClick(item.id)} className={selectedRow === item.id ? 'bg-blue-200 cursor-pointer' : 'border px-4 py-2 cursor-pointer'} >{item.id}</td>
              <td key={item.id} onClick={() => handleRowClick(item.id)} className={selectedRow === item.id ? 'bg-blue-200 cursor-pointer' : 'border px-4 py-2 cursor-pointer'}>{item.url}</td>
              <td className="border px-4 py-2">
                <button
                  onClick={() => handleDelete(item.id)}
                  className="bg-red-500 text-white px-2 py-1 rounded-lg hover-bg-red-600"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {selectedRow !== null && (
        <div>
          <h2 className="text-xl font-semibold mt-4">Dynamic Table</h2>
          <table className="table-auto w-full">
            <thead>
              <tr>
                {Object.keys(dynamicTableData).map((key) => (
                  <th key={key} className="px-4 py-2">
                    {key}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <tr>
                {Object.values(dynamicTableData).map((value, index) => (
                  <td key={index} className="border px-4 py-2">
                    {value}
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
      )}
      <div className="mt-4">
        <label className="mr-2">Export Format:</label>
        <select value={exportFormat} onChange={(e) => setExportFormat(e.target.value)}>
          <option value="csv">CSV</option>
          <option value="pdf">PDF</option>
        </select>
        <button onClick={handleExport} className="bg-blue-500 text-white px-2 py-1 rounded-lg ml-2">
          Export
        </button>
      </div>
    </div>
  );
}

export default ExtractData;
