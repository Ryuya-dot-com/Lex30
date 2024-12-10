const stimuli = [
  "attack", "board", "close", "cloth", "dig", "dirty", "disease", "experience", 
  "fruit", "furniture", "habit", "hold", "hope", "kick", "map", "obey", 
  "pot", "potato", "real", "rest", "rice", "science", "seat", "spell", 
  "substance", "stupid", "television", "tooth", "trade", "window"
];

let participantID = "";
let currentIndex = 0;
let responses = {}; // {stimulus: {answers:[], reactionTime: number}}
let startTime = 0;
let autoNextTimer = null;
let testInProgress = false;

document.addEventListener('DOMContentLoaded', () => {
setupUI();
});

function setupUI() {
const saveIDBtn = document.getElementById('save-participant-id');
saveIDBtn.addEventListener('click', saveParticipantID);

const startBtn = document.getElementById('start-btn');
startBtn.addEventListener('click', startTest);

window.addEventListener('keydown', (e) => {
  if (testInProgress && e.code === 'Space') {
    e.preventDefault();
  }
});

window.addEventListener('keyup', (e) => {
  if (testInProgress && e.code === 'Space') {
    e.preventDefault();
    nextStimulus();
  }
});
}

function saveParticipantID() {
const idInput = document.getElementById('participant-id');
participantID = idInput.value.trim();

if (!participantID) {
  alert("Please enter a valid Participant ID.");
  return;
}

document.getElementById('participant-info').style.display = 'none';
document.getElementById('instructions').style.display = 'block';
}

function startTest() {
const instructions = document.getElementById('instructions');
const testArea = document.getElementById('test-area');
const resultArea = document.getElementById('result-area');

if (testInProgress) return;

instructions.style.display = 'none';
resultArea.style.display = 'none';
testArea.style.display = 'block';

currentIndex = 0;
testInProgress = true;
showStimulus(currentIndex);
}

function showStimulus(index) {
clearAutoNextTimer();

const stimElem = document.getElementById('stimulus');
stimElem.textContent = stimuli[index];

const answersArea = document.getElementById('answers-area');
answersArea.querySelectorAll('input').forEach(input => input.value = '');

startTime = performance.now();
startAutoNextTimer();
}

function nextStimulus() {
if (!testInProgress) return;

clearAutoNextTimer();

const endTime = performance.now();
const reactionTime = endTime - startTime;

const answersArea = document.getElementById('answers-area');
const inputs = answersArea.querySelectorAll('input');
let ansList = Array.from(inputs).map(input => input.value.trim());

const stimWord = stimuli[currentIndex];
responses[stimWord] = {
  answers: ansList,
  reactionTime: reactionTime
};

currentIndex++;
if (currentIndex < stimuli.length) {
  showStimulus(currentIndex);
} else {
  finishTest();
}
}

function finishTest() {
testInProgress = false;
document.getElementById('test-area').style.display = 'none';

const resultArea = document.getElementById('result-area');
resultArea.style.display = 'block';

const downloadBtn = document.getElementById('download-btn');
downloadBtn.onclick = downloadResultsAsCSV;
}

function downloadResultsAsCSV() {
let csv = "Participant,Stimulus,Answer1,Answer2,Answer3,Answer4,ReactionTime(ms)\n";

for (let stim of stimuli) {
  const data = responses[stim];
  const answers = data.answers.map(ans => `"${ans}"`).join(",");
  csv += `${participantID},${stim},${answers},${data.reactionTime}\n`;
}

const fileName = `lex30_results_${participantID}.csv`;

const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
const url = URL.createObjectURL(blob);

const link = document.createElement("a");
link.href = url;
link.download = fileName;
document.body.appendChild(link);
link.click();
document.body.removeChild(link);
}

function startAutoNextTimer() {
autoNextTimer = setTimeout(() => {
  nextStimulus();
}, 30000);
}

function clearAutoNextTimer() {
if (autoNextTimer) {
  clearTimeout(autoNextTimer);
  autoNextTimer = null;
}
}