import axios from '../utils/axios';

async function changeEmail(newEmail, setEmail, access_token) {
    try {
        const response = await axios.patch(`settings/email/${newEmail}`, newEmail, {
            headers: {
                'Authorization': `Bearer ${access_token}`
            }
        });
        console.log(response.data)
        setEmail(newEmail);
    } catch (error) {
        console.log(error.response.data.detail);
    }
}

async function changePassword(newPassword, access_token) {
    try {
        const response = await axios.patch(`settings/password/${newPassword}`, newPassword, {
            headers: {
                'Authorization': `Bearer ${access_token}`
            }
        });
        console.log(response.data)
    } catch (error) {
        console.log(error.response.data.detail);
    }
}

  export { changeEmail, changePassword };