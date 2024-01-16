const username = document.querySelector('[name = username]');
const verifyName = () => {
    const p = document.querySelector('.username p');
    const reg = /^[a-zA-Z0-9-_]{4,10}/
    if (!reg.test(username.value)) {
        p.innerHTML = 'Input is not legal, please enter 4-10 digits';
        return false;
    }
    p.innerHTML = '';
    return true;
}
username.addEventListener('change', verifyName);

const password = document.querySelector('[name = pwd]');
const verifyPassword = () => {
    const p = document.querySelector('.pwd p');
    const reg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/
    if (!reg.test(password.value)) {
        p.innerHTML = 'At least 8-16 characters and contain uppercase letters, lowercase letters and numbers';
        return false;
    }
    p.innerHTML = '';
    return true;
}
password.addEventListener('change', verifyPassword);

const again = document.querySelector('[name = confirm_pwd]');
const verifyPasswordAgain = () => {
    const p = document.querySelector('.confirm_pwd p');
    if (again.value !== password.value) {
        p.innerHTML = 'The two passwords do not match';
        return false;
    }
    p.innerHTML = '';
    return true;
}
again.addEventListener('change', verifyPasswordAgain);

const email = document.querySelector('[name = email]');
const verifyEmail = () => {
    const p = document.querySelector('.email p')
    const reg = /^[a-zA-Z0-9_-]{5,}@[a-zA-Z0-9_-]{2,}(.[a-zA-Z0-9_-]+){2,}$/
    if (!reg.test(email.value)) {
        p.innerHTML = 'Please enter the correct email address';
        return false;
    }
    p.innerHTML = '';
    return true;
}
email.addEventListener('change', verifyEmail);

const phone = document.querySelector('[name = phone]');
const verifyPhone = () => {
    const p = document.querySelector('.phone p')
    const reg = /^[0-9]{8,11}$/
    if (!reg.test(phone.value)) {
        p.innerHTML = 'Please enter the correct phone number 8-11';
        return false;
    }
    p.innerHTML = '';
    return true;
}
phone.addEventListener('change', verifyPhone);

const address = document.querySelector('[name = address]');
const verifyAddress = () => {
    const p = document.querySelector('.address p')
    if (phone.value === '') {
        p.innerHTML = 'Complete the correct delivery address';
        return false;
    }
    p.innerHTML = '';
    return true;
}
address.addEventListener('change', verifyAddress);


const form = document.querySelector('.enter');
form.addEventListener('click', function (e) {
    if (!verifyName()) e.preventDefault();
    if (!verifyPassword()) e.preventDefault();
    if (!verifyPasswordAgain()) e.preventDefault();
    if (!verifyEmail()) e.preventDefault();
    if (!verifyPhone()) e.preventDefault();
    if (!verifyAddress()) e.preventDefault();

})