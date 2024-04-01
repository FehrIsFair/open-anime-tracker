import React from 'react';
import {BrowserRouter, Route, Routes} from 'react-router-dom'
import './App.css'

import NavHeader from './Header/nav-header';
import MainPage from './Main/main-page'
import AddAnime from './Pages/AddAnime';
import GetAnime from './Pages/GetAnime';


function App() {
  return (
  <BrowserRouter>
    <div className="content-container">
        <NavHeader/>
        <Routes>
          <Route path='/' Component={MainPage} />
          <Route path='/add-anime' Component={AddAnime} />
          <Route path='/get-anime' Component={GetAnime} />
        </Routes>
        {/* Footer */}
    </div>
  </BrowserRouter>
  );
}

export default App;
