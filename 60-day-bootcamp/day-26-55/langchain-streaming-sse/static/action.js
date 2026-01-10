const queryInput = document.getElementById('query');
const tempSlider = document.getElementById('temperature');
const tokensSlider = document.getElementById('max-tokens');
const tempValue = document.getElementById('temp-value');
const tokensValue = document.getElementById('tokens-value');
const streamBtn = document.getElementById('streamBtn');
const clearBtn = document.getElementById('clearBtn');
const responseDiv = document.getElementById('response');
const metricsDiv = document.getElementById('metrics');
const statusDiv = document.getElementById('status');
const statusText = document.getElementById('statusText');
const btnText = document.getElementById('btnText');
const loadingSpinner = streamBtn.querySelector('.loading');

let isStreaming = false;
let controller = null;

// Update slider values
tempSlider.addEventListener('input', (e) => {
    tempValue.textContent = e.target.value;
});

tokensSlider.addEventListener('input', (e) => {
    tokensValue.textContent = e.target.value;
});

// Stream response
streamBtn.addEventListener('click', async () => {
    if (isStreaming) {
        stopStreaming();
        return;
    }

    const query = queryInput.value.trim();
    if (!query) {
        alert('Please enter a question');
        return;
    }

    startStreaming(query);
});

// Clear response
clearBtn.addEventListener('click', () => {
    responseDiv.textContent = 'Response will appear here...';
    metricsDiv.classList.remove('show');
    statusDiv.classList.remove('show');
    resetMetrics();
});

function resetMetrics() {
    document.getElementById('ttft').textContent = '-';
    document.getElementById('total-tokens').textContent = '-';
    document.getElementById('duration').textContent = '-';
    document.getElementById('tokens-per-sec').textContent = '-';
}

async function startStreaming(query) {
    isStreaming = true;
    streamBtn.style.background = '#dc3545';
    btnText.textContent = 'Stop Streaming';
    loadingSpinner.style.display = 'inline-block';
    responseDiv.textContent = '';
    metricsDiv.classList.remove('show');
    statusDiv.classList.add('show');
    statusText.textContent = 'Connecting...';

    const temperature = parseFloat(tempSlider.value);
    const maxTokens = parseInt(tokensSlider.value);

    controller = new AbortController();

    // DECLARE ALL VARIABLES HERE
    let startTime = Date.now();  // This was missing!
    let firstTokenTime = null;
    let tokenCount = 0;
    let buffer = '';

    try {
        const response = await fetch('/stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'text/event-stream'
            },
            body: JSON.stringify({
                query: query,
                temperature: temperature,
                max_tokens: maxTokens
            }),
            signal: controller.signal
        });

        if (!response.ok || !response.body) {
            throw new Error(`Stream error: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        statusText.textContent = 'Streaming...';

        try {
            while (true) {
                const { done, value } = await reader.read();

                if (done) {
                    console.log('Stream completed');
                    break;
                }

                // Decode the chunk
                const chunk = decoder.decode(value, { stream: true });
                buffer += chunk;

                // Process complete SSE events (separated by double newlines)
                const events = buffer.split('\n\n');
                buffer = events.pop(); // Keep incomplete event in buffer

                for (const eventData of events) {
                    if (eventData.trim() === '') continue;

                    try {
                        // Parse SSE event
                        const lines = eventData.split('\n');
                        let eventType = 'message';
                        let data = '';

                        for (const line of lines) {
                            if (line.startsWith('event:')) {
                                eventType = line.substring(6).trim();
                            } else if (line.startsWith('data:')) {
                                data = line.substring(5).trim();
                            }
                        }

                        // Process based on event type
                        if (eventType === 'message') {
                            // Parse JSON data
                            const parsed = JSON.parse(data);

                            if (parsed.type === 'token') {
                                if (!firstTokenTime && parsed.content) {
                                    firstTokenTime = Date.now() - startTime;
                                    document.getElementById('ttft').textContent =
                                        `${(firstTokenTime / 1000).toFixed(3)}s`;
                                }

                                if (parsed.content) {
                                    responseDiv.textContent += parsed.content;
                                    tokenCount++;
                                }
                            } else if (parsed.type === 'end') {
                                const duration = (Date.now() - startTime) / 1000;
                                document.getElementById('total-tokens').textContent = tokenCount;
                                document.getElementById('duration').textContent =
                                    `${duration.toFixed(2)}s`;
                                document.getElementById('tokens-per-sec').textContent =
                                    (tokenCount / duration).toFixed(1);
                                metricsDiv.classList.add('show');
                                statusText.textContent = 'Stream completed';

                                setTimeout(() => {
                                    statusDiv.classList.remove('show');
                                }, 2000);

                                stopStreaming();
                                return;
                            }
                        } else if (eventType === 'error') {
                            throw new Error(data || 'Stream error');
                        } else if (eventType === 'end') {
                            // End of stream
                            const duration = (Date.now() - startTime) / 1000;
                            document.getElementById('total-tokens').textContent = tokenCount;
                            document.getElementById('duration').textContent =
                                `${duration.toFixed(2)}s`;
                            document.getElementById('tokens-per-sec').textContent =
                                (tokenCount / duration).toFixed(1);
                            metricsDiv.classList.add('show');
                            statusText.textContent = 'Stream completed';

                            setTimeout(() => {
                                statusDiv.classList.remove('show');
                            }, 2000);

                            stopStreaming();
                            return;
                        }
                    } catch (parseError) {
                        console.warn('Failed to parse SSE event:', parseError, 'Event data:', eventData);
                    }
                }
            }
        } finally {
            reader.releaseLock();
        }

    } catch (error) {
        if (error.name === 'AbortError') {
            statusText.textContent = 'Stream stopped';
        } else {
            console.error('Stream error:', error);
            responseDiv.textContent = 'Error: ' + error.message;
            statusText.textContent = 'Error occurred';
        }
        setTimeout(() => {
            stopStreaming();
        }, 2000);
    }
}
// Helper function to parse SSE events
function parseSSEEvent(rawEvent) {
    const lines = rawEvent.split('\n');
    const event = { type: 'message', data: '' };

    for (const line of lines) {
        if (line.startsWith('event:')) {
            event.type = line.substring(6).trim();
        } else if (line.startsWith('data:')) {
            const data = line.substring(5).trim();
            try {
                event.data = JSON.parse(data);
            } catch {
                event.data = data;
            }
        }
    }

    return event;
}


function stopStreaming() {
    isStreaming = false;
    streamBtn.style.background = '#667eea';
    btnText.textContent = 'Stream Response';
    loadingSpinner.style.display = 'none';

    if (controller) {
        controller.abort();
        controller = null;
    }
}