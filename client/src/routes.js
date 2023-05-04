import Home from './pages/Home/Home';
import Profile from './pages/Profile/Profile';
import CustomCategories from './pages/Categories/CustomCategories/CustomCategories';
import Category from './components/Category/Category';
import Documents from './pages/Categories/Documents';
import Images from './pages/Categories/Images';
import Music from './pages/Categories/Music';
import Videos from './pages/Categories/Videos';
import Favorite from './pages/Favorite/Favorite';
import Basket from './pages/Basket/Basket';
import History from './pages/History/History';
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
        path: '/profile',
        component: Profile,
    },
    {
        path: '/categories/custom',
        component: CustomCategories,
    },
    {
        path: '/categories/default/documents',
        component: Documents,
    },
    {
        path: '/categories/default/images',
        component: Images,
    },
    {
        path: '/categories/default/:music',
        component: Music,
    },
    {
        path: '/categories/default/videos',
        component: Videos,
    },
    {
        path: '/categories/custom/:category_name',
        component: Category,
    },  
    {
        path: '/favorite',
        component: Favorite,
    },
    {
        path: '/basket',
        component: Basket,
    },
    {
        path: '/history',
        component: History,
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
