const wrapper = document.querySelector('.wrapper');
const registroLink = document.querySelector('.registro-link');
const loginLink = document.querySelector('.login-link');

registroLink.onclick = () => {
    wrapper.classList.add('active');
}

loginLink.onclick = () => {
    wrapper.classList.remove('active');
}