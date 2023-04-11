import React, { useEffect } from 'react';
import Cookie from 'js-cookie';
import useNavigate from 'react-router-dom';

function AuthChecked({ children }) {
    const navigate = useNavigate();

    useEffect(() => {
        const isAuth = Cookie.get('logged_in') === 'true';
        const isAuthRedirectPaths = ['/register', '/login', '/'];
        const currentPath = window.location.pathname;


        if (!isAuth) {
            if (isAuthRedirectPaths.includes(currentPath)) {
                return;
            } else {
                navigate('/');
            }
        } else {
            if (isAuthRedirectPaths.includes(currentPath)) {
                navigate('/home');
            }
        }
    }, [navigate]);


    return <>{children}</>;
}

export default AuthChecked;
