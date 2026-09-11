import React from 'react';
import {BrowserRouter, Route, Routes, Navigate} from 'react-router-dom'
import './App.css'

import NavHeader from './Header/nav-header';
import MainPage from './Main/main-page'
import AddAnime from './Pages/AddAnime';
import GetAnime from './Pages/GetAnime';
import KitsuImport from './Pages/KitsuImport';
import AnimeDetails from './Pages/AnimeDetails';
import SignUp from './Pages/SignUp';
import SignIn from './Pages/SignIn';
import { AuthProvider, AuthRoute, AuthContext, Auth } from './context/auth_context';


function App() {
  return (
  <AuthProvider>
    <BrowserRouter>
      <div className="content-container">
          <NavHeader/>
          <Routes>
            <Route path='/' element={<AuthRoute><MainPage /></AuthRoute>} />
            <Route path='/add-anime' element={<AuthRoute><AddAnime /></AuthRoute>} />
            <Route path='/get-anime' element={<AuthRoute><GetAnime /></AuthRoute>} />
            <Route path='/anime/:id/details' element={<AuthRoute><AnimeDetails /></AuthRoute>} />
            <Route path='/kitsu-import' element={<AuthRoute><KitsuImport /></AuthRoute>} />
            {/* Redirect authenticated users away from auth pages */}
            <Route path='/signup' element={
              <AuthRedirect>
                <SignUp />
              </AuthRedirect>
            } />
            <Route path='/signin' element={
              <AuthRedirect>
                <SignIn />
              </AuthRedirect>
            } />
            <Route 
                path='*' 
                element={<Navigate to='/signin' replace />} 
            />
          </Routes>
          {/* Footer */}
      </div>
    </BrowserRouter>
  </AuthProvider>
  );
}

// Redirect authenticated users away from public-only routes
const AuthRedirect: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, loading } = React.useContext<Auth>(AuthContext);

  if (loading) return null;
  if (user) return <Navigate to="/add-anime" replace />;

  return <>{children}</>;
};

export default App;
