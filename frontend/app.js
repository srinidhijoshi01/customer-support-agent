document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const loginSection = document.getElementById('login-section');
    const chatSection = document.getElementById('chat-section');
    const chatHeader = document.getElementById('chat-header');
    
    const loginForm = document.getElementById('login-form');
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    
    // Windows & Indicators
    const chatWindowMemory = document.getElementById('chat-window-memory');
    const typingIndicatorMemory = document.getElementById('typing-indicator-memory');
    
    const chatWindowNoMemory = document.getElementById('chat-window-nomemory');
    const typingIndicatorNoMemory = document.getElementById('typing-indicator-nomemory');
    
    const viewHistoryBtn = document.getElementById('view-history-btn');
    const logoutBtn = document.getElementById('logout-btn');
    
    const historyModal = document.getElementById('history-modal');
    const closeHistoryBtn = document.getElementById('close-history');
    const historyContent = document.getElementById('history-content');
    
    const displayCustomer = document.getElementById('display-customer');
    
    // State
    let currentCustomer = {
        name: '',
        id: ''
    };
    
    // API URL
    // Use relative path so it works across the local network (not just localhost)
    const API_URL = '/api';

    // Handle Login
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const nameInput = document.getElementById('customer-name').value.trim();
        const idInput = document.getElementById('customer-id').value.trim();
        
        if (nameInput && idInput) {
            currentCustomer.name = nameInput;
            currentCustomer.id = idInput;
            
            // Update Header Display
            displayCustomer.textContent = `${nameInput} (${idInput})`;
            
            // Transition UI
            loginSection.classList.add('hidden');
            chatHeader.classList.remove('hidden');
            chatSection.classList.remove('hidden');
            
            // Focus chat input
            setTimeout(() => {
                messageInput.focus();
            }, 300);
        }
    });

    // Handle Logout
    logoutBtn.addEventListener('click', () => {
        currentCustomer = { name: '', id: '' };
        document.getElementById('customer-name').value = '';
        document.getElementById('customer-id').value = '';
        
        // Reset Chat Windows
        chatWindowMemory.innerHTML = `
            <div class="message system-msg">
                <div class="msg-content">Welcome! I'm your NovaSaaS AI assistant (With Memory). I remember our past interactions!</div>
            </div>`;
        chatWindowNoMemory.innerHTML = `
            <div class="message system-msg">
                <div class="msg-content">Welcome! I'm your NovaSaaS AI assistant (Without Memory). I treat every message as a brand new conversation!</div>
            </div>`;
        
        chatHeader.classList.add('hidden');
        chatSection.classList.add('hidden');
        loginSection.classList.remove('hidden');
    });

    // Handle Sending Message
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        if (!message) return;
        
        // Trigger Send Animation
        sendBtn.classList.add('sending');
        
        // Add User Message to both UIs
        addMessageToUI(chatWindowMemory, message, 'user');
        addMessageToUI(chatWindowNoMemory, message, 'user');
        
        messageInput.value = '';
        messageInput.disabled = true;
        
        // Show Typing Indicators
        typingIndicatorMemory.classList.remove('hidden');
        typingIndicatorNoMemory.classList.remove('hidden');
        scrollToBottom(chatWindowMemory);
        scrollToBottom(chatWindowNoMemory);
        
        // Prepare payload
        const payload = {
            customer_name: currentCustomer.name,
            customer_id: currentCustomer.id,
            message: message
        };
        
        // Fetch from Both Endpoints Simultaneously
        const fetchMemory = fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        }).then(res => res.json()).catch(err => ({ error: true }));

        const fetchNoMemory = fetch(`${API_URL}/chat/no-memory`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        }).then(res => res.json()).catch(err => ({ error: true }));

        // Handle Memory Response
        fetchMemory.then(data => {
            typingIndicatorMemory.classList.add('hidden');
            if (data.error) {
                addMessageToUI(chatWindowMemory, 'Error connecting to server.', 'system');
            } else {
                addMessageToUI(chatWindowMemory, data.response, 'system');
            }
        });

        // Handle No-Memory Response
        fetchNoMemory.then(data => {
            typingIndicatorNoMemory.classList.add('hidden');
            if (data.error) {
                addMessageToUI(chatWindowNoMemory, 'Error connecting to server.', 'system');
            } else {
                addMessageToUI(chatWindowNoMemory, data.response, 'system');
            }
        });

        // Re-enable input after both finish (or timeout)
        Promise.allSettled([fetchMemory, fetchNoMemory]).then(() => {
            messageInput.disabled = false;
            sendBtn.classList.remove('sending');
            messageInput.focus();
        });
    });

    // View History Modal
    viewHistoryBtn.addEventListener('click', async () => {
        if (!currentCustomer.id) {
            alert('Please login first to view your history.');
            return;
        }
        
        historyModal.classList.remove('hidden');
        historyContent.textContent = 'Loading history...';
        
        try {
            const response = await fetch(`${API_URL}/history/${currentCustomer.id}`);
            if (!response.ok) throw new Error('API Error');
            
            const data = await response.json();
            historyContent.textContent = data.history || 'No history found.';
        } catch (error) {
            historyContent.textContent = 'Failed to load history. Make sure the backend server is running.';
        }
    });
    
    closeHistoryBtn.addEventListener('click', () => {
        historyModal.classList.add('hidden');
    });
    
    // Close modal on outside click
    historyModal.addEventListener('click', (e) => {
        if (e.target === historyModal) {
            historyModal.classList.add('hidden');
        }
    });

    // Helper Functions
    function addMessageToUI(windowElement, text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}-msg`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'msg-content';
        contentDiv.textContent = text;
        
        msgDiv.appendChild(contentDiv);
        windowElement.appendChild(msgDiv);
        
        scrollToBottom(windowElement);
    }
    
    function scrollToBottom(windowElement) {
        windowElement.scrollTop = windowElement.scrollHeight;
    }
});
