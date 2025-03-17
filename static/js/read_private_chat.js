const messages = document.querySelectorAll('.message_your')
localStorage.setItem('current_id', '1')

for (const message of messages) {
    message.setAttribute('data-message_id', localStorage.getItem('current_id'))
    localStorage.setItem('current_id', Int16Array(localStorage.getItem(current_id))+1)
}
current_id = 1