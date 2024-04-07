import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    
    useEffect(() => {
        const user = localStorage.getItem('user');
        setIsLoggedIn(!!user);
    }, []);
    
    const login = (userCredentials) => {
        localStorage.setItem('user', JSON.stringify(userCredentials));
        setIsLoggedIn(true);
    };
    
    const logout = () => {
        localStorage.removeItem('user');
        setIsLoggedIn(false);
    };
    
    const value = {
        isLoggedIn,
        login,
        logout
    };
    
    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);