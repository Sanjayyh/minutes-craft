let selectedAudioFile = null;
let statusInterval = null;

document.addEventListener("DOMContentLoaded", () => {

    updateStatus("online", "System Ready");
    loadRoles();

    const transcriptText = document.getElementById("transcriptText");

    if (transcriptText) {
        transcriptText.addEventListener("input", () => {
            document.getElementById("transcriptCount").textContent =
                transcriptText.value.length + " characters";
        });
    }

    const audioInput = document.getElementById("audioFile");

    if (audioInput) {
        audioInput.addEventListener("change", function () {

            if (this.files.length === 0) return;

            selectedAudioFile = this.files[0];

            document.getElementById("audioPreview").classList.remove("hidden");
            document.getElementById("audioFileName").textContent = selectedAudioFile.name;
        });
    }

});

function startStatusPolling() {

    const popup = document.getElementById("loadingPopup");

    const statusText =
        document.getElementById("statusText");

    popup.classList.remove("hidden");

    const interval = setInterval(async () => {

        const response =
            await fetch("/status");

        const data =
            await response.json();

        statusText.textContent =
            data.status;

    }, 1000);

    return interval;
}

// STATUS 

function updateStatus(status, text) {
    const dot = document.getElementById("statusDot");
    const label = document.getElementById("statusLabel");

    if (dot) dot.className = "status-dot " + status;
    if (label) label.textContent = text;
}

// REMOVE FILE 

function removeFile(type) {
    if (type === "audio") {
        document.getElementById("audioFile").value = "";
        document.getElementById("audioPreview").classList.add("hidden");
        selectedAudioFile = null;
    }
}

// ROLES 

function loadRoles() {

    const roles = [
        { name: "Principal", icon: "🎓", focus: "High level decisions and policy updates" },
        { name: "Teachers", icon: "📚", focus: "Academic planning and classroom activities" },
        { name: "Office Staff", icon: "🏢", focus: "Administrative tasks and scheduling" },
        { name: "Support Staff", icon: "🛠️", focus: "Operational responsibilities" }
    ];

    const grid = document.getElementById("rolesGrid");

    if (!grid) return;

    grid.innerHTML = "";

    roles.forEach(role => {

        const card = document.createElement("div");
        card.className = "role-card";

        card.innerHTML = `
            <div class="role-card-icon">${role.icon}</div>
            <div class="role-card-content">
                <div class="role-card-name">${role.name}</div>
                <div class="role-card-focus">${role.focus}</div>
            </div>
            <div class="role-check">✓</div>
        `;

        card.addEventListener("click", () => {
            card.classList.toggle("selected");
        });

        grid.appendChild(card);

    });
}

// ===== ROLE HELPERS =====

function selectAllRoles() {
    document.querySelectorAll(".role-card").forEach(card => card.classList.add("selected"));
}

function clearAllRoles() {
    document.querySelectorAll(".role-card").forEach(card => card.classList.remove("selected"));
}

// TRANSCRIBE AUDIO 

async function transcribeAudio(event) {

    if (event) event.preventDefault();

    if (!selectedAudioFile) {
        alert("Please upload an audio file first.");
        return;
    }

    const generateBtn = document.getElementById("generateBtn");

    // Disable generate button during transcription
    if (generateBtn) {
        generateBtn.disabled = true;
    }

    updateStatus("online", "Transcribing audio...");
    statusInterval = startStatusPolling();
    

    document.getElementById("transcribeBtn").disabled = true;
    document.getElementById("transcribeBtn").innerText = "Transcribing...";

    const formData = new FormData();
    formData.append("audio", selectedAudioFile);

    try {

        const response = await fetch("/transcribe", {
            method: "POST",
            body: formData,
            cache: "no-cache"
        });

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            updateStatus("offline", "Transcription failed");
            return;
        }

        document.getElementById("transcriptText").value = data.transcript;

        updateStatus("online", "Transcription completed");
        

        // Enable generate button AFTER transcription finishes
        if (generateBtn) {
            generateBtn.disabled = false;
        }

        alert("Transcription completed successfully!");

        clearInterval(statusInterval);

        document
            .getElementById("loadingPopup")
            .classList.add("hidden");

    } catch (error) {


        clearInterval(statusInterval);

        document
            .getElementById("loadingPopup")
            .classList.add("hidden");
        console.error("Upload error:", error);

        updateStatus("offline", "Transcription failed");

        alert("Upload failed.");

    }   finally {
        document.getElementById("transcribeBtn").disabled = false;
        document.getElementById("transcribeBtn").innerHTML =
        '<span class="btn-icon">🔊</span> Transcribe Audio';
    }

    selectedAudioFile = null;

    document.getElementById("audioFile").value = "";
}
// GENERATE MINUTES 

async function generateMinutes() {

    const generateBtn = document.getElementById("generateBtn");

    try {

        updateStatus("online", "Generating meeting minutes...");

        const progressCard = document.getElementById("progressCard");

        progressCard.classList.remove("hidden");

        document.getElementById("progressTitle").innerText =
        "Generating AI Meeting Minutes...";

        const steps = document.getElementById("progressSteps");

        steps.innerHTML = `
        <div class="progress-step active">
            <span class="progress-step-icon">🎙️</span>
            Processing transcript
        </div>

        <div class="progress-step active">
            <span class="progress-step-icon">🤖</span>
            Generating role-based minutes
        </div>

        <div class="progress-step active">
            <span class="progress-step-icon">📄</span>
            Preparing downloads
        </div>
        `;

        if (generateBtn) {
            generateBtn.disabled = true;
            generateBtn.innerText = "Generating...";
        }

        updateStatus("online", "Generating meeting minutes...");

        statusInterval = startStatusPolling();

        document.getElementById("popupTitle").innerText =
            "Generating Meeting Minutes...";

        const response = await fetch("/generate", {
            method: "POST"
        });

        const data = await response.json();

        if (data.error) {

            alert(data.error);

            updateStatus("offline", "Generation failed");

            return;
        }

        showResults(data.files);

        updateStatus("online", "Minutes generated successfully");

        clearInterval(statusInterval);

document
    .getElementById("loadingPopup")
    .classList.add("hidden");
        

    } catch (error) {

        clearInterval(statusInterval);

document
    .getElementById("loadingPopup")
    .classList.add("hidden");
        console.error(error);

        updateStatus("offline", "Generation failed");

        alert("Generation failed");

    } finally {

        if (generateBtn) {
            generateBtn.disabled = false;
            generateBtn.innerText = "Generate Minutes";
        }
        progressCard.classList.add("hidden");
    }
}

// SHOW RESULTS 

function showResults(files) {

    const resultsCard = document.getElementById("resultsCard");
    const list = document.getElementById("resultsList");

    if (!list) return;

    list.innerHTML = "";

    files.forEach(file => {

        const item = document.createElement("div");
        item.className = "result-item";

        item.innerHTML = `
            <div class="result-role">${file}</div>

            <div class="result-actions">

                <button class="result-btn download"
                    onclick="downloadFile('${file}')">
                    Download
                </button>

            </div>
        `;

        list.appendChild(item);

    });

    resultsCard.classList.remove("hidden");

    resultsCard.scrollIntoView({
    behavior: "smooth"
});
}

// DOWNLOAD FILE 

function downloadFile(filename) {
    window.location.href = "/data/" + filename;
}

// CLEAR SESSION

function clearSession() {

    document.getElementById("transcriptText").value = "";

    document.getElementById("resultsCard").classList.add("hidden");

    document.getElementById("audioPreview").classList.add("hidden");

    document.getElementById("audioFile").value = "";

    document.getElementById("generateBtn").disabled = true;

    selectedAudioFile = null;

    updateStatus("online", "System Ready");
}