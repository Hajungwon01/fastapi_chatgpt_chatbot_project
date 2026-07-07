// app/static/app.js

const chatIcon        = document.getElementById("chatIcon");
const chatModal       = document.getElementById("chatModal");
const closeChat       = document.getElementById("closeChat");
const chatMessages    = document.getElementById("chatMessages");
const chatForm        = document.getElementById("chatForm");
const messageInput    = document.getElementById("messageInput");
const settingsToggle  = document.getElementById("settingsToggle");
const settingsOverlay = document.getElementById("settingsPanel");
const applySettings   = document.getElementById("applySettings");

const history = [];

let settings = {
    systemInstruction: "너는 한국어로 친절하고 정확하게 답변하는 FastAPI 기반 ChatGPT 챗봇이다.",
    model: "gpt-4o-mini",
    temperature: 0.7,
    topP: 1.0,
    maxTokens: 1024,
};

// 챗봇 열기
chatIcon.addEventListener("click", () => {
    chatModal.classList.remove("hidden");
    messageInput.focus();
});

// 챗봇 닫기
closeChat.addEventListener("click", () => {
    chatModal.classList.add("hidden");
    settingsOverlay.classList.add("hidden");
});

// ⚙️ 설정 오버레이 토글 (누르면 열리고 다시 누르면 닫힘)
settingsToggle.addEventListener("click", () => {
    if (settingsOverlay.style.display === "flex") {
        settingsOverlay.style.display = "none";
    } else {
        settingsOverlay.style.display = "flex";
    }
});

// 슬라이더 실시간 값 표시
document.getElementById("temperature").addEventListener("input", (e) => {
    document.getElementById("temperatureValue").textContent = parseFloat(e.target.value).toFixed(1);
});
document.getElementById("topP").addEventListener("input", (e) => {
    document.getElementById("topPValue").textContent = parseFloat(e.target.value).toFixed(1);
});
document.getElementById("maxTokens").addEventListener("input", (e) => {
    document.getElementById("maxTokensValue").textContent = e.target.value;
});

// 적용 버튼 — 설정 저장 후 오버레이 닫기
applySettings.addEventListener("click", () => {
    settings.systemInstruction = document.getElementById("systemInstruction").value.trim();
    settings.model             = document.getElementById("modelSelect").value;
    settings.temperature       = parseFloat(document.getElementById("temperature").value);
    settings.topP              = parseFloat(document.getElementById("topP").value);
    settings.maxTokens         = parseInt(document.getElementById("maxTokens").value);

    // 오버레이 닫기
    settingsOverlay.classList.add("hidden");

    // 적용 확인 메시지
    addMessage("assistant", `✅ 설정이 적용되었습니다.\n모델: ${settings.model} | Temp: ${settings.temperature} | Top P: ${settings.topP} | Max Tokens: ${settings.maxTokens}`);
});

function addMessage(role, content) {
    const el = document.createElement("div");
    el.className = `message ${role}`;
    el.textContent = content;
    chatMessages.appendChild(el);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = messageInput.value.trim();
    if (!message) return;

    addMessage("user", message);
    history.push({ role: "user", content: message });
    messageInput.value = "";

    addMessage("assistant", "답변을 생성하는 중입니다...");
    const loadingMessage = chatMessages.lastElementChild;

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message:            message,
                history:            history.slice(0, -1),
                system_instruction: settings.systemInstruction,
                model:              settings.model,
                temperature:        settings.temperature,
                top_p:              settings.topP,
                max_tokens:         settings.maxTokens,
            }),
        });

        if (!response.ok) throw new Error(`서버 오류: ${response.status}`);

        const data = await response.json();
        loadingMessage.textContent = data.reply;
        history.push({ role: "assistant", content: data.reply });

    } catch (error) {
        loadingMessage.textContent = `오류가 발생했습니다. ${error.message}`;
    }
});