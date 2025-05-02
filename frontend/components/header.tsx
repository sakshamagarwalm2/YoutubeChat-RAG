import React from 'react';
import { Youtube } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="flex justify-center items-center mb-8">
      <div className="flex items-center">
        <Youtube className="h-8 w-8 mr-2 text-red-500" />
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900">
          YouTube RAG Chat
        </h1>
        <div className="ml-2 relative">
          <span className="absolute -top-3 -right-3 text-green-400 text-lg">✨</span>
        </div>
      </div>
    </header>
  );
};

export default Header;