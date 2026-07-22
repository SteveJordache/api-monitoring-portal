const monitorForm = document.querySelector("#monitor-form");
const formMessage = document.querySelector("#form-message");
const monitorsContainer = document.querySelector("#monitors-container");
const refreshButton = document.querySelector("#refresh-monitors");
const resultsPanel = document.querySelector("#results-panel");
const resultsTitle = document.querySelector("#results-title");
const resultsContainer = document.querySelector("#results-container");
const closeResultsButton = document.querySelector("#close-results");


function setFormMessage(message, type = "") {
    formMessage.textContent = message;
    formMessage.className = "message";

    if (type) {
        formMessage.classList.add(type);
    }
}


function formatDateTime(value) {
    if (!value) {
        return "-";
    }

    const date = new Date(value);

    return date.toLocaleString();
}


function getStatusBadge(result, isActive) {
    if (!isActive) {
        return '<span class="status-badge status-inactive">INACTIVE</span>';
    }

    if (!result) {
        return '<span class="status-badge status-unknown">NOT CHECKED</span>';
    }

    if (result.success) {
        return '<span class="status-badge status-up">UP</span>';
    }

    return '<span class="status-badge status-down">DOWN</span>';
}


async function getLatestResult(monitorId) {
    const response = await fetch(`/monitors/${monitorId}/results`);

    if (!response.ok) {
        return null;
    }

    const results = await response.json();

    return results.length > 0 ? results[0] : null;
}


async function loadMonitors() {
    monitorsContainer.innerHTML = "<p>Loading monitors...</p>";

    try {
        const response = await fetch("/monitors");

        if (!response.ok) {
            throw new Error("Could not load monitors.");
        }

        const monitors = await response.json();

        if (monitors.length === 0) {
            monitorsContainer.innerHTML = `
                <div class="empty-state">
                    No monitors have been created yet.
                </div>
            `;
            return;
        }

        const monitorCards = await Promise.all(
            monitors.map(async (monitor) => {
                const latestResult = await getLatestResult(monitor.id);
                const statusBadge = getStatusBadge(
                    latestResult,
                    monitor.is_active,
                );

                const latestCheck = latestResult
                    ? formatDateTime(latestResult.checked_at)
                    : "Never";

                return `
                    <article class="monitor-card">
                        <div class="monitor-card-header">
                            <div>
                                <h3>${monitor.name}</h3>
                                <p class="monitor-url">${monitor.url}</p>
                            </div>

                            ${statusBadge}
                        </div>

                        <div class="monitor-details">
                            <span class="detail-badge">
                                ${monitor.method}
                            </span>

                            <span class="detail-badge">
                                Expected: ${monitor.expected_status}
                            </span>

                            <span class="detail-badge">
                                Interval: ${monitor.interval_seconds}s
                            </span>

                            <span class="detail-badge">
                                Last check: ${latestCheck}
                            </span>
                        </div>

                        <div class="monitor-actions">
                            <button
                                type="button"
                                data-action="run"
                                data-monitor-id="${monitor.id}"
                            >
                                Run now
                            </button>

                            <button
                                type="button"
                                class="secondary-button"
                                data-action="results"
                                data-monitor-id="${monitor.id}"
                                data-monitor-name="${monitor.name}"
                            >
                                View results
                            </button>
                        </div>
                    </article>
                `;
            }),
        );

        monitorsContainer.innerHTML = `
            <div class="monitor-list">
                ${monitorCards.join("")}
            </div>
        `;
    } catch (error) {
        monitorsContainer.innerHTML = `
            <p class="message error">
                ${error.message}
            </p>
        `;
    }
}


async function createMonitor(event) {
    event.preventDefault();

    setFormMessage("Creating monitor...");

    const payload = {
        name: document.querySelector("#name").value.trim(),
        url: document.querySelector("#url").value.trim(),
        method: document.querySelector("#method").value,
        expected_status: Number(
            document.querySelector("#expected-status").value,
        ),
        interval_seconds: Number(
            document.querySelector("#interval-seconds").value,
        ),
        is_active: document.querySelector("#is-active").checked,
    };

    try {
        const response = await fetch("/monitors", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            const errorData = await response.json();

            throw new Error(
                errorData.detail
                    ? JSON.stringify(errorData.detail)
                    : "Could not create monitor.",
            );
        }

        monitorForm.reset();
        document.querySelector("#method").value = "GET";
        document.querySelector("#expected-status").value = "200";
        document.querySelector("#interval-seconds").value = "60";
        document.querySelector("#is-active").checked = true;

        setFormMessage(
            "Monitor created successfully.",
            "success",
        );

        await loadMonitors();
    } catch (error) {
        setFormMessage(
            error.message,
            "error",
        );
    }
}


async function runMonitor(monitorId, button) {
    const originalText = button.textContent;

    button.disabled = true;
    button.textContent = "Running...";

    try {
        const response = await fetch(
            `/monitors/${monitorId}/run`,
            {
                method: "POST",
            },
        );

        if (!response.ok) {
            throw new Error("Monitor execution failed.");
        }

        const result = await response.json();

        const statusText = result.success ? "UP" : "DOWN";

        window.alert(
            `Result: ${statusText}\n` +
            `Actual status: ${result.actual_status ?? "-"}\n` +
            `Expected status: ${result.expected_status}\n` +
            `Response time: ${result.response_time_ms} ms\n` +
            `Error: ${result.error_message ?? "-"}`,
        );

        await loadMonitors();
    } catch (error) {
        window.alert(error.message);
    } finally {
        button.disabled = false;
        button.textContent = originalText;
    }
}


async function showResults(monitorId, monitorName) {
    resultsTitle.textContent = `Execution history: ${monitorName}`;
    resultsContainer.innerHTML = "<p>Loading results...</p>";
    resultsPanel.classList.remove("hidden");

    try {
        const response = await fetch(
            `/monitors/${monitorId}/results`,
        );

        if (!response.ok) {
            throw new Error("Could not load execution history.");
        }

        const results = await response.json();

        if (results.length === 0) {
            resultsContainer.innerHTML = `
                <div class="empty-state">
                    This monitor has no execution results yet.
                </div>
            `;
            return;
        }

        const rows = results.map((result) => {
            const statusBadge = result.success
                ? '<span class="status-badge status-up">UP</span>'
                : '<span class="status-badge status-down">DOWN</span>';

            return `
                <tr>
                    <td>${statusBadge}</td>
                    <td>${result.actual_status ?? "-"}</td>
                    <td>${result.expected_status}</td>
                    <td>${result.response_time_ms} ms</td>
                    <td>${formatDateTime(result.checked_at)}</td>
                    <td>${result.error_message ?? "-"}</td>
                </tr>
            `;
        });

        resultsContainer.innerHTML = `
            <div class="results-table-wrapper">
                <table class="results-table">
                    <thead>
                        <tr>
                            <th>Status</th>
                            <th>Actual</th>
                            <th>Expected</th>
                            <th>Response time</th>
                            <th>Checked at</th>
                            <th>Error</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${rows.join("")}
                    </tbody>
                </table>
            </div>
        `;
    } catch (error) {
        resultsContainer.innerHTML = `
            <p class="message error">
                ${error.message}
            </p>
        `;
    }
}


monitorForm.addEventListener("submit", createMonitor);

refreshButton.addEventListener("click", loadMonitors);

closeResultsButton.addEventListener("click", () => {
    resultsPanel.classList.add("hidden");
});

monitorsContainer.addEventListener("click", async (event) => {
    const button = event.target.closest("button");

    if (!button) {
        return;
    }

    const action = button.dataset.action;
    const monitorId = button.dataset.monitorId;

    if (action === "run") {
        await runMonitor(monitorId, button);
    }

    if (action === "results") {
        await showResults(
            monitorId,
            button.dataset.monitorName,
        );
    }
});


loadMonitors();
