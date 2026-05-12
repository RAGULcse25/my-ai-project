import React from 'react';

const About = () => {
  return (
    <section className="bg-gray-900 text-white py-20">
      <div className="container mx-auto flex flex-col items-center justify-center h-full">
        <h1 className="text-5xl font-bold mb-4">About me</h1>
        <p className="text-lg mb-8">I'm a data scientist with a passion for machine learning and data visualization. I have experience working with various tools and technologies, including Python, R, and SQL.</p>
        <button className="bg-orange-500 hover:bg-orange-700 transition duration-300 py-2 px-4 rounded-full">
          Contact me
        </button>
      </div>
    </section>
  );
};

export default About;