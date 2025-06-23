const serviceRegion = "eastus";
const speechConfig = SpeechSDK.SpeechConfig.fromSubscription(speechKey, serviceRegion);
speechConfig.speechRecognitionLanguage = "de-DE";

const ttsConfig = SpeechSDK.SpeechConfig.fromSubscription(speechKey, serviceRegion);
ttsConfig.speechSynthesisLanguage = "de-DE";
ttsConfig.speechSynthesisVoiceName = "de-DE-KatjaNeural";
ttsConfig.speechSynthesisOutputFormat = SpeechSDK.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3;

let recognizer;
let directLine;
let store;
let synthesizer;
let audioConfig;

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const muteBtn = document.getElementById("muteBtn");
const output = document.getElementById("output");
let isMuted = false;

muteBtn.onclick = () => {
    isMuted = !isMuted;
    muteBtn.innerHTML = isMuted ? "🔇 Stummschaltung aktiv" : "🔊 Stumm schalten";
    muteBtn.classList.toggle('bg-yellow-500', !isMuted);
    muteBtn.classList.toggle('bg-gray-600', isMuted);
    
    if (isMuted && synthesizer) {
        synthesizer.close();
        synthesizer = null;
    }
};

startBtn.onclick = () => {
    startBtn.disabled = true;
    stopBtn.disabled = false;
    output.innerText = "🎤 Aufnahme läuft...";
    
    const audioConfig = SpeechSDK.AudioConfig.fromDefaultMicrophoneInput();
    recognizer = new SpeechSDK.SpeechRecognizer(speechConfig, audioConfig);
    
    recognizer.recognizeOnceAsync(result => {
        if (result.reason === SpeechSDK.ResultReason.RecognizedSpeech) {
            output.innerText = "📝 " + result.text;
            sendMessageToBot(result.text);
        } else {
            output.innerText = "❌ Nichts erkannt oder Fehler";
        }
        
        startBtn.disabled = false;
        stopBtn.disabled = true;
        recognizer.close();
    });
};

stopBtn.onclick = () => {
    if (recognizer) {
        recognizer.stopContinuousRecognitionAsync(() => {
            output.innerText = "⏹️ Aufnahme gestoppt.";
            recognizer.close();
            startBtn.disabled = false;
            stopBtn.disabled = true;
        });
    }
};

function speakText(text) {
    if (!text || text.trim() === '' || isMuted) return;
    
    const cleanText = text
        .replace(/<[^>]*>/g, '') 
        .replace(/\*\*(.*?)\*\*/g, '$1') 
        .replace(/\*(.*?)\*/g, '$1') 
        .replace(/`(.*?)`/g, '$1') 
        .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
        .trim();
    
    if (cleanText.length === 0) return;
    
    try {
        if (synthesizer) {
            synthesizer.close();
        }
        
        audioConfig = SpeechSDK.AudioConfig.fromDefaultSpeakerOutput();
        synthesizer = new SpeechSDK.SpeechSynthesizer(ttsConfig, audioConfig);
        
        synthesizer.synthesisStarted = (s, e) => console.log("🔊 Azure TTS gestartet");
        synthesizer.synthesisCompleted = (s, e) => console.log("✅ Azure TTS beendet");
        synthesizer.SynthesisCanceled = (s, e) => console.log("⏹️ Azure TTS abgebrochen:", e.reason);
        
        synthesizer.speakTextAsync(
            cleanText,
            result => {
                console.log("📊 TTS Result:", result.reason);
                if (result.reason === SpeechSDK.ResultReason.Canceled) {
                    const cancellation = SpeechSDK.CancellationDetails.fromResult(result);
                    console.error("❌ TTS abgebrochen:", cancellation.reason, cancellation.errorDetails);
                }
                if (synthesizer) {
                    synthesizer.close();
                    synthesizer = null;
                }
            },
            error => {
                console.error("❌ Azure TTS Fehler:", error);
                if (synthesizer) {
                    synthesizer.close();
                    synthesizer = null;
                }
            }
        );
        
    } catch (error) {
        console.error("❌ TTS Initialisierung fehlgeschlagen:", error);
        if (synthesizer) {
            synthesizer.close();
            synthesizer = null;
        }
    }
}

function sendMessageToBot(text) {
    if (store && text.trim()) {
        store.dispatch({
            type: 'WEB_CHAT/SEND_MESSAGE',
            payload: {
                text: text
            }
        });
        console.log("Nachricht gesendet:", text);
    } else {
        console.log("Store nicht bereit oder leerer Text");
    }
}

// === BotFramework WebChat initialisieren ===
async function initWebChat() {
    try {
        const tokenResponse = await fetch('https://directline.botframework.com/v3/directline/tokens/generate', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + botToken,
                'Content-Type': 'application/json'
            }
        });

        if (!tokenResponse.ok) {
            throw new Error('Token-Anfrage fehlgeschlagen (' + tokenResponse.status + ')');
        }

        const tokenData = await tokenResponse.json();
        
        directLine = window.WebChat.createDirectLine({
            token: tokenData.token
        });

        const webchatContainer = document.getElementById('webchat');
        store = window.WebChat.createStore();
        
        let lastSpokenActivityId = null;

        store.subscribe(() => {
            const state = store.getState();
            const activities = state.activities || [];
            
            if (activities.length > 0) {
                const lastActivity = activities[activities.length - 1];
                if (lastActivity && 
                    lastActivity.from && 
                    lastActivity.from.role === 'bot' && 
                    lastActivity.text && 
                    lastActivity.id !== lastSpokenActivityId) {
                    
                    console.log("🤖 Bot-Antwort empfangen:", lastActivity.text);
                    speakText(lastActivity.text);
                    lastSpokenActivityId = lastActivity.id; // Markiere als (versucht) gesprochen
                }
            }
        });
        
        window.WebChat.renderWebChat(
            {
                directLine: directLine,
                store: store,
                styleSet: window.WebChat.createStyleSet({
                    backgroundColor: 'white',
                    bubbleBackground: '#f1f5f9', // slate-100
                    bubbleFromUserBackground: '#3b82f6', // blue-500
                    bubbleFromUserTextColor: 'white',
                })
            },
            webchatContainer
        );

        console.log("WebChat initialisiert");
        
    } catch (error) {
        console.error('Fehler beim Initialisieren:', error);
        document.getElementById('webchat').innerHTML = '<div class="p-4 text-red-600 bg-red-100 rounded-lg"><strong>Fehler:</strong> ' + error.message + '</div>';
    }
}

window.addEventListener('load', initWebChat);