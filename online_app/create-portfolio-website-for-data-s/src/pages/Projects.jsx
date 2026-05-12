import React from 'react';

const Projects = () => {
  return (
    <section className="bg-gray-900 text-white py-20">
      <div className="container mx-auto flex flex-col items-center justify-center h-full">
        <h1 className="text-5xl font-bold mb-4">My projects</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="bg-gray-800 p-4 rounded-lg">
            <h2 className="text-2xl font-bold mb-2">Project 1</h2>
            <p className="text-lg mb-4">This is a project I worked on using machine learning and data visualization.</p>
            <button className="bg-orange-500 hover:bg-orange-700 transition duration-300 py-2 px-4 rounded-full">
              View project
            </button>
          </div>
          <div className="bg-gray-800 p-4 rounded-lg">
            <h2 className="text-2xl font-bold mb-2">Project 2</h2>
            <p className="text-lg mb-4">This is another project I worked on using machine learning and data visualization.</p>
            <button className="bg-orange-500 hover:bg-orange-700 transition duration-300 py-2 px-4 rounded-full">
              View project
            </button>
          </div>
          <div className="bg-gray-800 p-4 rounded-lg">
            <h2 className="text-2xl font-bold mb-2">Project 3</h2>
            <p className="text-lg mb-4">This is a project I worked on using machine learning and data visualization.</p>
            <button className="bg-orange-500 hover:bg-orange-700 transition duration-300 py-2 px-4 rounded-full">
              View project
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Projects;