document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('toggleAI');
    const aiChat = document.getElementById('aiChat');
    const aiForm = document.getElementById('aiForm');
    const chatMessages = document.getElementById('chatMessages');
    
    toggleBtn.addEventListener('click', function() {
        aiChat.style.display = aiChat.style.display === 'none' ? 'block' : 'none';
        if (aiChat.style.display === 'block' && chatMessages.children.length === 0) {
            appendMessage('assistant', 'Hi! How can I help you with your learning journey?');
        }
    });
    
    aiForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const input = document.getElementById('userInput');
        const message = input.value.trim();
        
        if (!message) return;
        
        input.value = '';
        appendMessage('user', message);
        
        try {
            const response = await fetch('/paths/ai-assistant/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: `message=${encodeURIComponent(message)}`
            });
            
            const data = await response.json();
            appendMessage('assistant', data.response);
            
        } catch (error) {
            appendMessage('error', 'Sorry, I could not process your request.');
        }
    });
    
    function appendMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${role} mb-2 p-2 rounded`;
        messageDiv.innerHTML = `
            <div class="d-flex align-items-start gap-2">
                <i class="fas ${role === 'user' ? 'fa-user' : 'fa-robot'} mt-1"></i>
                <div style="white-space: pre-line">${content}</div>
            </div>
        `;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}); 