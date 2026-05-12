import React from 'react';

const Contact = () => {
  return (
    <section className="bg-gray-900 text-white py-20">
      <div className="container mx-auto flex flex-col items-center justify-center h-full">
        <h1 className="text-5xl font-bold mb-4">Get in touch</h1>
        <form className="flex flex-col space-y-4">
          <input type="text" placeholder="Name" className="bg-gray-800 p-2 rounded-lg" />
          <input type="email" placeholder="Email" className="bg-gray-800 p-2 rounded-lg" />
          <textarea placeholder="Message" className="bg-gray-800 p-2 rounded-lg" />
          <button className="bg-orange-500 hover:bg-orange-700 transition duration-300 py-2 px-4 rounded-full">
            Send message
          </button>
        </form>
      </div>
    </section>
  );
};

export default Contact;