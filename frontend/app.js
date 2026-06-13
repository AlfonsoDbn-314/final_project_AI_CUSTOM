const askForm = document.querySelector("#ask-form");
const contextForm = document.querySelector("#context-form");
const answerOutput = document.querySelector("#answer-output");
const contextItems = document.querySelector("#context-items");
const ctxSaveMsg = document.querySelector("#ctx-save-msg");

const API_BASE_URL = "http://127.0.0.1:8000";

function getUserId() {
  return document.querySelector("#user-id").value.trim();
}

askForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const userId = getUserId();
  const question = document.querySelector("#question").value.trim();

  if (!userId || !question) return;

  answerOutput.innerHTML = "<p class='muted-text'>Consultando...</p>";

  try {
    const response = await fetch(`${API_BASE_URL}/api/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, question }),
    });
    const result = await response.json();
    renderAnswer(result);
    await loadContext(userId);
  } catch (error) {
    answerOutput.innerHTML = `<p class="error-text">No se pudo conectar con el backend: ${error.message}</p>`;
  }
});

contextForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const userId = getUserId();
  const key = document.querySelector("#ctx-key").value.trim();
  const value = document.querySelector("#ctx-value").value.trim();

  if (!userId || !key || !value) {
    ctxSaveMsg.textContent = "Completa todos los campos.";
    ctxSaveMsg.className = "save-msg error-text";
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/context`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, key, value }),
    });
    const result = await response.json();
    if (result.saved) {
      ctxSaveMsg.textContent = "Contexto guardado correctamente.";
      ctxSaveMsg.className = "save-msg success-text";
      document.querySelector("#ctx-key").value = "";
      document.querySelector("#ctx-value").value = "";
      await loadContext(userId);
    }
  } catch (error) {
    ctxSaveMsg.textContent = `Error: ${error.message}`;
    ctxSaveMsg.className = "save-msg error-text";
  }
});

document.querySelector("#user-id").addEventListener("change", async () => {
  await loadContext(getUserId());
});

async function loadContext(userId) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/context?user_id=${encodeURIComponent(userId)}`);
    const result = await response.json();
    renderContext(result.context || []);
  } catch (error) {
    contextItems.innerHTML = "<p class='muted-text'>El modulo CAG no esta disponible.</p>";
  }
}

function renderContext(items) {
  if (!items.length) {
    contextItems.innerHTML = "<p class='muted-text'>Sin contexto guardado para este usuario.</p>";
    return;
  }
  contextItems.innerHTML = items.map(item => `
    <div class="context-item">
      <span class="ctx-key">${item.key}</span>
      <span class="ctx-value">${item.value}</span>
    </div>
  `).join("");
}

function renderAnswer(result) {
  const contextUsed = result.context_used && result.context_used.length
    ? `<div class="context-used-badge">Contexto usado: ${result.context_used.map(k => `<span class="badge">${k}</span>`).join(" ")}</div>`
    : "";

  const sources = result.sources && result.sources.length
    ? `<div class="sources">Fuentes: ${result.sources.map(s => `<span class="badge">${s}</span>`).join(" ")}</div>`
    : "";

  answerOutput.innerHTML = `
    <p class="answer-text">${result.answer}</p>
    ${contextUsed}
    ${sources}
  `;
}

loadContext(getUserId());