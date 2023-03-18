

import Home from './pages/Home/Home';
import Folders from './pages/Categories/Folders';
import Documents from './pages/Categories/Documents';
import Images from './pages/Categories/Images';
import Music from './pages/Categories/Music';
import Videos from './pages/Categories/Videos';
import Favorites from './pages/Favorites/Favorites';
import Removed from './pages/Removed/Removed';
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import Main from './pages/Main/Main';

const routes = [
    {
        path: '/',
        component: Main,
    },
    {
        path: '/home',
        component: Home,
    },
    {
        path: '/category/folders',
        component: Folders,
    },
    {
        path: '/category/documents',
        component: Documents,
    },
    {
        path: '/category/images',
        component: Images,
    },
    {
        path: '/category/music',
        component: Music,
    },
    {
        path: '/category/videos',
        component: Videos,
    },
    {
        path: '/favorites',
        component: Favorites,
    },
    {
        path: '/basket',
        component: Removed,
    },
    {
        path: '/register',
        component: Register,
    },
    {
        path: '/login',
        component: Login,
    },
]
export default routes;
