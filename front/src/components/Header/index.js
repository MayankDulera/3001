import React from 'react'
import { Link } from 'react-router-dom'

const navigations = [
  {
    name: 'Home',
    path: '/'
  },
  {
    name: 'Contact',
    path: '/contact'
  },
  {
    name: 'Scraper',
    path: '/scraper'
  },
  {
    name: 'Linklist',
    path: '/linklist'
  },
  {
    name: 'ExtractData', // Add an option for ExtractData
    path: '/extractdata', // Adjust the path accordingly
  },
  {
    name: 'Crons', // Add an option for ExtractData
    path: '/crons', // Adjust the path accordingly
  },
  {
    name: 'YourCrons', // Add an option for ExtractData
    path: '/yourcrons', // Adjust the path accordingly
  },
]

const Header = ({ isAuthenticated, onLogout }) => {
  console.log(isAuthenticated)
  return (
    <header className="text-gray-600 body-font shadow-lg">
      <div className="container mx-auto flex flex-wrap p-5 flex-col md:flex-row items-center">
        <Link to={'/'} className="flex cursor-pointer title-font font-medium items-center text-gray-900 mb-4 md:mb-0">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" className="w-10 h-10 text-white p-2 bg-indigo-500 rounded-full" viewBox="0 0 24 24">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
          </svg>
          <span className="ml-3 text-xl">WebScrapper</span>
        </Link>
        <nav className="md:ml-auto md:mr-auto flex flex-wrap items-center text-base justify-center">
        {navigations.map((navigation) => (
            (isAuthenticated || navigation.name !== 'Scraper' && navigation.name !== 'Linklist' && navigation.name !== 'ExtractData' && navigation.name !== 'Crons' && navigation.name !== 'YourCrons') ? (
              <Link to={navigation.path} className="mr-5 hover:text-gray-900" key={navigation.name}>
                {navigation.name}
              </Link>
            ) : null
          ))}
          {isAuthenticated ? (
          <button onClick={onLogout} className="mr-5 hover:text-gray-900">Logout</button>
        ) : null}
        </nav>
      </div>
    </header>
  )
}

export default Header
