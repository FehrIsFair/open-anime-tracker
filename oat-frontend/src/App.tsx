import {BrowserRouter, Route, Routes, Navigate} from 'react-router-dom'
import './App.css'

import NavHeader from './Header/nav-header';
import MainPage from './Main/main-page'
import AddAnime from './Pages/AddAnime';
import GetAnime from './Pages/GetAnime';
import SignUp from './Pages/SignUp';
import SignIn from './Pages/SignIn';
import { AuthProvider } from './context/auth_context';


function App() {
  return (
  <AuthProvider>
    <BrowserRouter>
      <div className="content-container">
          <NavHeader/>
          <Routes>
            <Route path='/' Component={MainPage} />
            <Route path='/add-anime' Component={AddAnime} />
            <Route path='/get-anime' Component={GetAnime} />
            <Route path='/signup' Component={SignUp} />
            <Route path='/signin' Component={SignIn} />
            <Route 
                path='*' 
                element={<Navigate to='/login' replace />} 
            />
          </Routes>
          {/* Footer */}
      </div>
    </BrowserRouter>
  </AuthProvider>
  );
}

export default App;
