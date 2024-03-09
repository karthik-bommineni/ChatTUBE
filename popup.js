document.addEventListener('DOMContentLoaded', function () {
    const chatOutput = document.getElementById('chat-output');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
  
    sendBtn.addEventListener('click', sendMessage);
  
    userInput.addEventListener('keydown', function (event) {
      if (event.key === 'Enter') {
        event.preventDefault();  // Prevents the default behavior of Enter key in a text area
        sendMessage();
      }
    });
  
    function sendMessage() {
      const userMessage = userInput.value;
         appendMessage(userMessage, 'user-message');
          getOpenAIResponse(userMessage);
        userInput.value = '';
    }
  
    function appendMessage(message, messageClass) {
        const messageElement = document.createElement('div');
      
        if (messageClass === 'user-message') {
          messageElement.classList.add('message', 'user-message');
          const userBubble = document.createElement('div');
          userBubble.textContent = message;
          userBubble.classList.add('user-bubble');
          messageElement.appendChild(userBubble);
        } else if (messageClass === 'bot-message') {
          messageElement.classList.add('message', 'bot-message');
          const botBubble = document.createElement('div');
          botBubble.textContent = message;
          botBubble.classList.add('bot-bubble');
          messageElement.appendChild(botBubble);
        }
      
        chatOutput.appendChild(messageElement);
        chatOutput.scrollTop = chatOutput.scrollHeight;
    }

    function getOpenAIResponse(userMessage) {
        const apiKey = 'ng-z0E45NH0iumvObnSpUt5BAeboEWw1';
        const apiUrl = 'https://api.naga.ac/v1/chat/completions';
      
        fetch(apiUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
          },
          body: JSON.stringify({
            model: 'gpt-3.5-turbo',  // Set the desired model name
            messages: [
              { role: 'system', content: 'You are a helpful assistant.' },
              { role: 'user', content: userMessage }
            ]
          })
        })
        .then(response => response.json())
        .then(data => {
          const botResponse = data.choices[0].message.content.trim();
          appendMessage(botResponse, 'bot-message');
        })
        .catch(error => console.error('Error:', error));
    }
});