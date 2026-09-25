const state = { task: "qa" };

const taskButtons = document.querySelectorAll(".task-btn");
const panels = {
    qa: document.getElementById("qa-panel"),
    explain: document.getElementById("explain-panel"),
    summarize: document.getElementById("summarize-panel"),
    quiz: document.getElementById("quiz-panel"),
    learn: document.getElementById("learn-panel"),
};

const submitButton = document.getElementById("submit-btn");
const statusBox = document.getElementById("status");
const resultCard = document.getElementById("result-card");
const resultBox = document.getElementById("result");
const copyButton = document.getElementById("copy-btn");

taskButtons.forEach((button) => {
    button.addEventListener("click", () => {
        state.task = button.dataset.task;

        taskButtons.forEach((item) => item.classList.remove("active"));
        button.classList.add("active");

        Object.entries(panels).forEach(([name, panel]) => {
            panel.classList.toggle("hidden", name !== state.task);
        });

        const labels = {
            qa: "Ask EduGenie",
            explain: "Explain Topic",
            summarize: "Summarize",
            quiz: "Generate Quiz",
            learn: "Build Learning Path",
        };
        submitButton.textContent = labels[state.task];
        clearResult();
    });
});

function clearResult() {
    resultCard.classList.add("hidden");
    resultBox.innerHTML = "";
    statusBox.textContent = "";
}

function setLoading(loading) {
    submitButton.disabled = loading;
    statusBox.textContent = loading ? "EduGenie is thinking..." : "";
}

function showError(message) {
    resultCard.classList.remove("hidden");
    resultBox.innerHTML = `<div class="error">${escapeHtml(message)}</div>`;
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function renderText(text) {
    resultBox.innerHTML = `
        <div class="result-content">
            <pre>${escapeHtml(text)}</pre>
        </div>
    `;
    resultCard.classList.remove("hidden");
}

function renderQuiz(data) {
    let html = `<div class="result-content"><h3>${escapeHtml(data.title)}</h3>`;

    data.questions.forEach((q, index) => {
        html += `
            <div class="quiz-question">
                <strong>${index + 1}. ${escapeHtml(q.question)}</strong>
                ${q.options.map((option) =>
                    `<div class="option">${escapeHtml(option)}</div>`
                ).join("")}
                <details>
                    <summary>Show answer</summary>
                    <p><strong>Correct:</strong> ${escapeHtml(q.correct_answer)}</p>
                    <p>${escapeHtml(q.explanation)}</p>
                </details>
            </div>
        `;
    });

    html += "</div>";
    resultBox.innerHTML = html;
    resultCard.classList.remove("hidden");
}

function renderLearningPath(data) {
    let html = `
        <div class="result-content">
            <h3>${escapeHtml(data.topic)}</h3>
            <p><strong>Level:</strong> ${escapeHtml(data.level)}</p>
            <p><strong>Goal:</strong> ${escapeHtml(data.goal)}</p>
    `;

    data.steps.forEach((step, index) => {
        html += `
            <div class="learning-step">
                <h4>${index + 1}. ${escapeHtml(step.stage)}</h4>
                <p><strong>Estimated time:</strong> ${escapeHtml(step.estimated_time)}</p>
                <p><strong>Topics:</strong> ${step.topics.map(escapeHtml).join(", ")}</p>
                <p><strong>Resources:</strong> ${step.resources.map(escapeHtml).join(", ")}</p>
            </div>
        `;
    });

    html += "<h3>Study tips</h3><ul>";
    data.study_tips.forEach((tip) => {
        html += `<li>${escapeHtml(tip)}</li>`;
    });
    html += "</ul></div>";

    resultBox.innerHTML = html;
    resultCard.classList.remove("hidden");
}

async function postJson(url, payload) {
    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Request failed.");
    }

    return data;
}

submitButton.addEventListener("click", async () => {
    clearResult();
    setLoading(true);

    try {
        if (state.task === "qa") {
            const question = document.getElementById("qa-input").value.trim();
            if (!question) throw new Error("Enter a question.");
            const data = await postJson("/qa", { question });
            renderText(data.result);
        }

        if (state.task === "explain") {
            const topic = document.getElementById("explain-input").value.trim();
            const level = document.getElementById("explain-level").value;
            if (!topic) throw new Error("Enter a topic.");
            const data = await postJson("/explain", { topic, level });
            renderText(data.result);
        }

        if (state.task === "summarize") {
            const text = document.getElementById("summary-input").value.trim();
            if (!text) throw new Error("Paste some study material.");
            const data = await postJson("/summarize", { text });
            renderText(data.result);
        }

        if (state.task === "quiz") {
            const text = document.getElementById("quiz-input").value.trim();
            const question_count = Number(document.getElementById("quiz-count").value);
            if (!text) throw new Error("Paste study material.");
            const data = await postJson("/quiz", { text, question_count });
            renderQuiz(data);
        }

        if (state.task === "learn") {
            const topic = document.getElementById("learn-topic").value.trim();
            const level = document.getElementById("learn-level").value;
            const goal = document.getElementById("learn-goal").value.trim();
            if (!topic) throw new Error("Enter a topic.");
            const data = await postJson("/learn/recommendations", { topic, level, goal });
            renderLearningPath(data);
        }
    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false);
    }
});

copyButton.addEventListener("click", async () => {
    const text = resultBox.innerText.trim();
    if (!text) return;
    await navigator.clipboard.writeText(text);
    copyButton.textContent = "Copied";
    setTimeout(() => (copyButton.textContent = "Copy"), 1200);
});
