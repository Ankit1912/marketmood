import React from 'react';
import Header from './components/Header';
import StockData from './components/StockData';
import NewsData from './components/NewsData';

const App = () => {
  return (
    <div>
      <Header />
      <div style={{ display: 'flex', justifyContent: 'space-around', marginTop: '20px' }}>
        <StockData />
        <NewsData />
      </div>
    </div>
  );
};

export default App;
