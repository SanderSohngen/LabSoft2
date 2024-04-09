import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    
    useEffect(() => {
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        }
    }, []);
    
    const login = (userCredentials) => {
        localStorage.setItem('user', JSON.stringify(userCredentials));
        setUser(userCredentials);
    };
    
    const logout = () => {
        localStorage.removeItem('user');
        setUser(null);
    };
    
    const value = {
        isLoggedIn: !!user,
        user,
        login,
        logout
    };
    
    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);