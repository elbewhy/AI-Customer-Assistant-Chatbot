const chatEl = document.getElementById('chat');
const form = document.getElementById('chat-form');
const input = document.getElementById('input');

function appendMessage(role, text){
    const div = document.createElement('div');
    div.className = role === 'user' ? 'text-right' : 'text-left';
    div.innerHTML = `<div class="inline-block max-w-full md:max-w-[70%] p-3 rounded ${role==='user' ? 'bg-blue-100' : 'bg-gray-100'}">${text}</div>`;
    chatEl.appendChild(div);
    chatEl.scrollTop = chatEl.scrollHeight;
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = input.value.trim();
    if(!message) return;
    appendMessage('user', message);
    input.value = '';
    appendMessage('assistant', 'Thinking...');

    try {
        const resp = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({message})
        });
        const data = await resp.json();
        // Remove the 'Thinking...' (last assistant message)
        chatEl.removeChild(chatEl.lastChild);
        if(data.reply){
            appendMessage('assistant', data.reply);
        } else {
            appendMessage('assistant', 'No reply received.');
        }
    } catch (err) {
        chatEl.removeChild(chatEl.lastChild);
        appendMessage('assistant', 'Error contacting server.');
    }
});
