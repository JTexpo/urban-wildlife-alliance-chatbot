const sendBtn = document.getElementById("sendBtn");
const userInput = document.getElementById("userInput");
const chatHistory = document.getElementById("chatHistory");

let loginModal;
let conversationHistory = [{
        "role": "user",
        "content": [
            {
                "text": (
                    "You are a helpful chat assistant.\n \
                    Rules:\n \
                    - Respond naturally and conversationally\n \
                    - Do NOT describe internal reasoning or planning\n \
                    - Do NOT mention the user's message analysis\n \
                    - Do NOT say things like 'the user has greeted me'\n \
                    - Just respond directly like a human"
                )
            }
        ]
    }];
let globalUsername;
let globalPassword;

window.addEventListener("load", () => {

    loginModal = new bootstrap.Modal(
        document.getElementById("loginModal"),
        {
            backdrop: "static",
            keyboard: false
        }
    );

    loginModal.show();
});

document
    .getElementById("loginBtn")
    .addEventListener("click", authenticate);


/**
 * Authenticates the user by checking the username and password.
 * If the username or password is missing, displays an error message.
 * If an error occurs during the authentication process, displays an error message.
 *
 * @returns {Promise<void>} - A promise that resolves when the authentication process is complete.
 */
async function authenticate() {

    // Retrieve the values of the login fields
    const username =
        document.getElementById("loginUsername").value.trim();

    const password =
        document.getElementById("loginPassword").value;

    // Retrieve the error box element
    const errorBox =
        document.getElementById("loginError");

    // Check if the username or password is missing
    if (!username || !password) {
        errorBox.textContent =
            "Please enter both username and password.";
        errorBox.classList.remove("d-none");
        return;
    }

    try {
        // Send a POST request to the authentication endpoint
        const response = await fetch(
            window.APP_CONFIG.API_ENDPOINT + "/v1/health/auth?safariCachebust=" + new Date().getTime(),
            {
                method: "GET",
                headers: {
                    "Authorization": "Basic " + btoa(username + ":" + password)
                }
            }
        );
        globalUsername = username;
        globalPassword = password;
        // Attempt to hide the login modal
        loginModal.hide();
    }
    catch (error) {
        // Display an error message if the authentication fails
        errorBox.textContent =
            "Invalid username or password.";

        errorBox.classList.remove("d-none");
    }
}

/**
 * Appends a new message to the chat history element.
 *
 * @param {string} text - The text content of the message.
 * @param {string} sender - The sender of the message.
 */
function appendMessage(text, sender) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message", sender);

    // Convert markdown to HTML
    const html = DOMPurify.sanitize(
        marked.parse(text)
    );

    messageDiv.innerHTML = `
        <div class="message-bubble">
            ${html}
        </div>
    `;

    chatHistory.appendChild(messageDiv);

    chatHistory.scrollTop = chatHistory.scrollHeight;
}

async function sendMessage() {

    const prompt = userInput.value.trim();

    if (!prompt) {
        return;
    }

    appendMessage(prompt, "user");

    userInput.value = "";

    setTimeout(() => {
        fetch(window.APP_CONFIG.API_ENDPOINT + "/v1/chatbot", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Basic " + btoa(globalUsername + ":" + globalPassword)
            },
            body: JSON.stringify({
                "message": prompt,
                "conversation_history": conversationHistory
            })
        })
            .then(response => response.json())
            .then(data => {
                appendMessage(data.message, "assistant");
                conversationHistory.push(
                    {"role": "user", "content": [{"text": prompt}]}
                )
                conversationHistory.push(
                    {"role": "assistant", "content": [{"text": data.message}]}
                )
            })
            .catch(error => {
                console.error(error);
            });
    }, 500);

}

sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keydown", event => {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();
    }
});