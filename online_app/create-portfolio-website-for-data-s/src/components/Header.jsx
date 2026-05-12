import React from 'react';
import { NavLink } from 'react-router-dom';
import { HiMenu } from 'react-icons/hi';

const Header = () => {
  return (
    <nav className="bg-gray-900 text-white py-4">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-2xl font-bold">Data Scientist Portfolio</h1>
        <ul className="flex items-center space-x-4">
          <li>
            <NavLink to="/" className="hover:text-gray-400 transition duration-300">
              Home
            </NavLink>
          </li>
          <li>
            <NavLink to="/about" className="hover:text-gray-400 transition duration-300">
              About
            </NavLink>
          </li>
          <li>
            <NavLink to="/projects" className="hover:text-gray-400 transition duration-300">
              Projects
            </NavLink>
          </li>
          <li>
            <NavLink to="/contact" className="hover:text-gray-400 transition duration-300">
              Contact
            </NavLink>
          </li>
        </ul>
        <button className="lg:hidden flex justify-center w-8 h-8 bg-gray-800 hover:bg-gray-700 transition duration-300 rounded-full">
          <HiMenu size={24} className="text-white" />
        </button>
      </div>
    </nav>
  );
};

export default Header;