import React from 'react';
import AuthForm from '../../components/AuthForm/AuthForm';
import styles from './Auth.module.scss';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Register = () => {

    const inputConfigs = [
        { title: "Адрес электронной почты", type: 'email', name: 'email' },
        { title: "Придумайте пароль", type: 'password', name: 'password' },
        { title: "Повтоите пароль", type: 'password', name: 'password_repeat' },
    ]

    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault();
        const email = e.target.email.value;
        const password = e.target.password.value;
        const password_repeat = e.target.password_repeat.value;
        try {
          const response = await axios.post('http://127.0.0.1:8000/api/register', { email, password, password_repeat });
          if (response.data) {
            navigate('/login')
          }
        } catch (error) {
          console.error(error.response.data.detail);
        }
      };
    return (
        <div className={styles.registration}>
            <div className={`title ${styles.title}`}>Регистрация</div>
            <div className={styles.registrationForm}>
                <AuthForm
                    inputConfigs={inputConfigs}
                    buttonTitle='Зарегестрироваться'
                    authHelpText='Есть аккаунт?'
                    onSubmit={handleSubmit}
                    authHelpLink='Вход'
                    link='/login'
                />
            </div>
        </div>
    )
}

export default Register
