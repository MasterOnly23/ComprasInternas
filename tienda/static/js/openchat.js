const chatbotOpen = document.querySelector('#chatbot')
const closeButton = document.querySelector('.chatbot-header-close');

chatbotOpen.addEventListener('click', () => {
    document.querySelector('.chatbot-container')
    .classList.toggle('show');
    document.querySelector('#chatbot')
    .classList.toggle('hidden');
})

closeButton.addEventListener('click', (event) => {
    document.querySelector('.chatbot-container').classList.remove('show');
    chatbotOpen.classList.remove('hidden');
    event.stopPropagation(); 
});