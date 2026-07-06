const FALLBACK_EXPERIMENT_CONFIG = {
  experimentId: "lex30-original-written-v1",
  experimentVersion: "1.0.0",
  label: "Original Lex30 - written v1",
  mode: "written",
  stimulusPresentation: "text",
  stimulusSetId: "lex30-original-30",
  audioBasePath: "",
  audioExtension: "mp3",
  audioVersion: "",
  audioAutoplay: true,
  responseCount: 4,
  answerMaxLength: 30,
  singleWordPerResponse: false,
  timerSeconds: 30,
  advanceKey: "Space",
  randomizeStimuli: false,
  breaks: {
    enabled: false,
    associationAfterStimulusOrders: []
  },
  followUp: {
    enabled: false
  },
  downloadPrefix: "lex30_results",
  instructions:
    "You will see 30 English words. For each word, type up to 4 words that come to your mind. Press SPACE to go to the next word at any time, or wait 30 seconds and it will move on automatically.",
  stimuli: [
    "attack", "board", "close", "cloth", "dig", "dirty", "disease", "experience",
    "fruit", "furniture", "habit", "hold", "hope", "kick", "map", "obey",
    "pot", "potato", "real", "rest", "rice", "science", "seat", "spell",
    "substance", "stupid", "television", "tooth", "trade", "window"
  ]
};

const AUTOSAVE_PREFIX = "lex30_autosave_v2";
const AUTOSAVE_RETENTION_DAYS = 14;
const LANGUAGE_STORAGE_KEY = "lex30_interface_language";
const UI_TEXT = {
  en: {
    pageTitle: "Lex30 Test",
    participantPrompt: "Please enter your Participant ID to begin.",
    participantPlaceholder: "Enter your ID",
    submit: "Submit",
    downloadSavedBackup: "Download Saved Backup",
    clearSavedBackup: "Clear Saved Backup",
    startTest: "Start Test",
    instructionsListeningFollowup: "You will hear 30 English words. For each word, type up to 4 English words that come to your mind. Write only English words in the answer boxes. After all 30 words, you will answer short follow-up questions about the words.",
    instructionsWritten: "You will see 30 English words. For each word, type up to 4 English words that come to your mind. Write only English words in the answer boxes.",
    responsePolicySingle: "Use one English word per box.",
    responsePolicyGeneral: "Use one English response per box.",
    navigationInstruction: "Press SPACE or Next to go to the next word anytime, or wait {seconds} seconds.",
    playAudioTimer: "Play the audio. The timer starts when the audio begins.",
    answerPlaceholderSingle: "One English word",
    answerPlaceholderGeneral: "English word",
    itemLabel: "Item {number}",
    next: "Next",
    downloadBackup: "Download Backup",
    breakTitle: "Break",
    breakMessage: "You may take a short break. Continue when you are ready.",
    continue: "Continue",
    part1CompleteTitle: "Part 1 complete",
    part1CompleteMessage: "You have finished the 30 listening items. The next part asks short follow-up questions about the same words.",
    startPart2: "Start Part 2",
    followupListeningLabel: "listening check",
    followupMeaningLabel: "meaning check",
    recognitionInstruction: "Without looking back, enter the English word you think you heard for this item.",
    heardWordLabel: "What English word did you hear?",
    heardWordPlaceholder: "Type the word you heard",
    heardConfidenceLabel: "How clearly did you hear this word during the first task?",
    notClearly: "Not clearly",
    veryClearly: "Very clearly",
    semanticTitle: "Meaning and relation check",
    semanticInstruction: "Answer these follow-up questions for the cue word shown below.",
    listeningSection: "Listening check",
    meaningSection: "Meaning checks",
    relationSection: "Word relation choices",
    meaningConfidenceLabel: "How well do you know the meaning of this word?",
    responseConfidenceLabel: "How confident are you that your earlier associated words matched this cue?",
    notAtAll: "Not at all",
    veryConfident: "Very confident",
    japaneseMeaningLabel: "Write the Japanese meaning of this word.",
    japaneseMeaningPlaceholder: "Japanese meaning",
    thankYou: "Thank you for your responses!",
    autoDownloadPending: "Your result files should download automatically. If they do not, use the buttons below.",
    autoDownloadStarted: "Downloading CSV and JSON result files automatically...",
    autoDownloadDone: "Automatic download was started. If any file did not download, use the buttons below.",
    downloadResults: "Download Results",
    downloadJson: "Download JSON",
    alertParticipantId: "Please enter a valid Participant ID.",
    alertPlayAudio: "Please play the audio before moving to the next item.",
    alertOneWord: "Please type only one English word in each box, or leave the box blank.",
    alertNoBackup: "No saved backup is available for this version.",
    alertBackupParticipant: "Enter the matching Participant ID before downloading a saved backup on this device.",
    alertClearParticipant: "Enter the matching Participant ID before clearing a saved backup on this device.",
    confirmClearBackup: "Clear the saved browser backup for this participant and version on this device?",
    alertBackupCleared: "Saved browser backup cleared on this device."
  },
  ja: {
    pageTitle: "Lex30 テスト",
    participantPrompt: "参加者IDを入力してください。",
    participantPlaceholder: "IDを入力",
    submit: "送信",
    downloadSavedBackup: "保存済みバックアップをダウンロード",
    clearSavedBackup: "保存済みバックアップを削除",
    startTest: "開始",
    instructionsListeningFollowup: "これから30個の英単語を聞きます。各単語について、思い浮かんだ英単語を最大4つ入力してください。回答欄には必ず英語の単語を書いてください。30項目が終わった後、同じ単語について短い確認問題に答えます。",
    instructionsWritten: "これから30個の英単語が表示されます。各単語について、思い浮かんだ英単語を最大4つ入力してください。回答欄には必ず英語の単語を書いてください。",
    responsePolicySingle: "各ボックスには英語の単語を1語だけ入力してください。",
    responsePolicyGeneral: "各ボックスには英語の回答を1つ入力してください。",
    navigationInstruction: "準備ができたらSPACEキーまたはNextで次に進めます。{seconds}秒後には自動で進みます。",
    playAudioTimer: "音声を再生してください。音声が始まるとタイマーが開始します。",
    answerPlaceholderSingle: "英語1語",
    answerPlaceholderGeneral: "英単語",
    itemLabel: "項目 {number}",
    next: "Next",
    downloadBackup: "バックアップをダウンロード",
    breakTitle: "休憩",
    breakMessage: "短い休憩を取ることができます。準備ができたら続けてください。",
    continue: "続ける",
    part1CompleteTitle: "Part 1 終了",
    part1CompleteMessage: "30個のリスニング項目が終了しました。次は、同じ単語について短い確認問題に答えます。",
    startPart2: "Part 2 を開始",
    followupListeningLabel: "聞き取り確認",
    followupMeaningLabel: "意味確認",
    recognitionInstruction: "前の画面には戻らず、この項目で聞いたと思う英単語を入力してください。",
    heardWordLabel: "どの英単語を聞いたと思いますか？",
    heardWordPlaceholder: "聞いた英単語を入力",
    heardConfidenceLabel: "最初の課題で、この単語はどのくらいはっきり聞こえましたか？",
    notClearly: "はっきり聞こえなかった",
    veryClearly: "とてもはっきり聞こえた",
    semanticTitle: "意味と関連の確認",
    semanticInstruction: "下に表示されるcue wordについて答えてください。",
    listeningSection: "聞き取り確認",
    meaningSection: "意味確認",
    relationSection: "単語関係の選択",
    meaningConfidenceLabel: "この単語の意味をどのくらい知っていますか？",
    responseConfidenceLabel: "最初に入力した連想語は、このcueにどのくらい合っていたと思いますか？",
    notAtAll: "まったくそう思わない",
    veryConfident: "とてもそう思う",
    japaneseMeaningLabel: "この単語の日本語の意味を書いてください。",
    japaneseMeaningPlaceholder: "日本語の意味",
    thankYou: "回答ありがとうございました。",
    autoDownloadPending: "結果ファイルは自動でダウンロードされます。開始しない場合は下のボタンを使ってください。",
    autoDownloadStarted: "CSVとJSONの結果ファイルを自動でダウンロードしています...",
    autoDownloadDone: "自動ダウンロードを開始しました。保存されないファイルがある場合は下のボタンを使ってください。",
    downloadResults: "CSVをダウンロード",
    downloadJson: "JSONをダウンロード",
    alertParticipantId: "有効な参加者IDを入力してください。",
    alertPlayAudio: "次に進む前に音声を再生してください。",
    alertOneWord: "各ボックスには英語の単語を1語だけ入力してください。空欄でも構いません。",
    alertNoBackup: "このバージョンで利用できる保存済みバックアップはありません。",
    alertBackupParticipant: "この端末の保存済みバックアップをダウンロードするには、一致する参加者IDを入力してください。",
    alertClearParticipant: "この端末の保存済みバックアップを削除するには、一致する参加者IDを入力してください。",
    confirmClearBackup: "この端末に保存された、この参加者・このバージョンのブラウザバックアップを削除しますか？",
    alertBackupCleared: "この端末の保存済みバックアップを削除しました。"
  }
};

let experimentConfig = FALLBACK_EXPERIMENT_CONFIG;
let stimuli = [];
let participantID = "";
let currentIndex = 0;
let responses = [];
let startTime = 0;
let startedAt = "";
let completedAt = "";
let autoNextTimer = null;
let testInProgress = false;
let participantSessionId = "";
let testStartMs = 0;
let currentStimulusStartedAt = "";
let currentStimulusPresentedAtMs = 0;
let currentResponseTimerStarted = false;
let currentAudioLog = emptyAudioLog();
let activePhase = "setup";
let followUpResponses = [];
let followUpIndex = 0;
let followUpStage = "recognition";
let currentFollowUpStartedAt = "";
let currentFollowUpStartedAtMs = 0;
let interfaceLanguage = "en";
let completedAssociationBreakOrders = [];
let autoDownloadTriggered = false;

document.addEventListener("DOMContentLoaded", initializeApp);

async function initializeApp() {
  try {
    experimentConfig = await loadExperimentConfig();
    interfaceLanguage = initialInterfaceLanguage();
    stimuli = buildStimulusOrder(experimentConfig);
    renderExperimentMetadata();
    renderAnswerInputs();
    setupUI();
    applyLanguage();
    pruneExpiredAutosaves();
    updateSavedBackupControl();
  } catch (error) {
    showSetupError(error);
  }
}

function initialInterfaceLanguage() {
  const params = new URLSearchParams(window.location.search);
  const requested = params.get("lang");
  if (requested === "ja" || requested === "en") {
    return requested;
  }
  try {
    const saved = localStorage.getItem(LANGUAGE_STORAGE_KEY);
    if (saved === "ja" || saved === "en") {
      return saved;
    }
  } catch (_error) {
    // Ignore storage failures; English is the stable fallback.
  }
  return "en";
}

async function loadExperimentConfig() {
  const params = new URLSearchParams(window.location.search);
  const allowDevFallback = params.get("devFallback") === "1";
  try {
    const requestedId = params.get("experiment") || params.get("version");
    const manifest = await fetchJson("experiments.json");
    const experimentId = requestedId || manifest.defaultExperimentId;
    const entry = (manifest.experiments || []).find(item => item.id === experimentId);

    if (!entry) {
      throw new Error(`Unknown experiment: ${experimentId}`);
    }

    const config = await fetchJson(entry.config);
    return normalizeConfig(config);
  } catch (error) {
    if (allowDevFallback) {
      console.warn("Using fallback Lex30 configuration because devFallback=1 was set.", error);
      return normalizeConfig(FALLBACK_EXPERIMENT_CONFIG);
    }
    throw error;
  }
}

async function fetchJson(path) {
  const response = await fetch(path, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Could not load ${path}: ${response.status}`);
  }
  return response.json();
}

function normalizeConfig(config) {
  const normalized = {
    ...FALLBACK_EXPERIMENT_CONFIG,
    ...config
  };

  normalized.responseCount = clampInt(normalized.responseCount, 1, 12, 4);
  normalized.answerMaxLength = clampInt(normalized.answerMaxLength, 1, 120, 30);
  normalized.singleWordPerResponse = normalized.singleWordPerResponse === true;
  normalized.timerSeconds = clampInt(normalized.timerSeconds, 5, 300, 30);
  normalized.audioExtension = String(normalized.audioExtension || "mp3").replace(/^\./, "");
  normalized.audioBasePath = String(normalized.audioBasePath || "").replace(/\/$/, "");
  normalized.audioVersion = String(normalized.audioVersion || "").trim();
  normalized.audioAutoplay = normalized.audioAutoplay !== false;
  normalized.followUp = normalizeFollowUp(normalized.followUp);
  normalized.stimuli = Array.isArray(normalized.stimuli)
    ? normalized.stimuli.map(item => String(item).trim()).filter(Boolean)
    : FALLBACK_EXPERIMENT_CONFIG.stimuli.slice();

  if (!normalized.stimuli.length) {
    normalized.stimuli = FALLBACK_EXPERIMENT_CONFIG.stimuli.slice();
  }
  normalized.breaks = normalizeBreaks(normalized.breaks, normalized.stimuli.length);

  return normalized;
}

function normalizeBreaks(breaks, stimulusCount) {
  if (!breaks || breaks.enabled !== true) {
    return { enabled: false, associationAfterStimulusOrders: [] };
  }
  const orders = Array.isArray(breaks.associationAfterStimulusOrders)
    ? breaks.associationAfterStimulusOrders
    : [];
  const normalizedOrders = Array.from(new Set(orders
    .map(value => Number.parseInt(value, 10))
    .filter(value => Number.isFinite(value) && value > 0 && value < stimulusCount)))
    .sort((a, b) => a - b);
  return {
    enabled: true,
    associationAfterStimulusOrders: normalizedOrders
  };
}

function normalizeFollowUp(followUp) {
  if (!followUp || followUp.enabled !== true) {
    return { enabled: false };
  }
  return {
    enabled: true,
    schemaVersion: String(followUp.schemaVersion || "lex30-followup-v1"),
    instructions: String(followUp.instructions || ""),
    recognition: {
      enabled: followUp.recognition?.enabled !== false,
      heardWordMaxLength: clampInt(followUp.recognition?.heardWordMaxLength, 1, 80, 40),
      confidenceLabel: String(followUp.recognition?.confidenceLabel || "How clearly did you hear this word?"),
      leftLabel: String(followUp.recognition?.leftLabel || "Not at all"),
      rightLabel: String(followUp.recognition?.rightLabel || "Very clearly")
    },
    semantic: {
      enabled: followUp.semantic?.enabled !== false,
      japaneseMeaningMaxLength: clampInt(followUp.semantic?.japaneseMeaningMaxLength, 1, 160, 80),
      meaningConfidenceLabel: String(followUp.semantic?.meaningConfidenceLabel || "How well do you know this word's meaning?"),
      responseConfidenceLabel: String(followUp.semantic?.responseConfidenceLabel || "How confident are you about your earlier associated words?"),
      leftLabel: String(followUp.semantic?.leftLabel || "Not at all"),
      rightLabel: String(followUp.semantic?.rightLabel || "Very confident")
    },
    probes: followUp.probes && typeof followUp.probes === "object" ? followUp.probes : {}
  };
}

function showSetupError(error) {
  const message = error?.message || String(error || "Unknown setup error");
  const label = document.getElementById("experiment-label");
  const errorPanel = document.getElementById("setup-error");
  const errorText = document.getElementById("setup-error-text");

  for (const id of ["participant-info", "instructions", "test-area", "result-area"]) {
    const element = document.getElementById(id);
    if (element) {
      element.style.display = "none";
    }
  }
  if (label) {
    label.textContent = "This Lex30 session could not be loaded.";
  }
  if (errorText) {
    errorText.textContent =
      `${message}. Please use the researcher page, run the preflight check, and open the participant URL from a local web server.`;
  }
  if (errorPanel) {
    errorPanel.style.display = "block";
  }
}

function clampInt(value, min, max, fallback) {
  const parsed = Number.parseInt(value, 10);
  if (!Number.isFinite(parsed)) return fallback;
  return Math.min(Math.max(parsed, min), max);
}

function buildStimulusOrder(config) {
  const ordered = config.stimuli.slice();
  if (!config.randomizeStimuli) {
    return ordered;
  }

  for (let index = ordered.length - 1; index > 0; index--) {
    const swapIndex = Math.floor(Math.random() * (index + 1));
    [ordered[index], ordered[swapIndex]] = [ordered[swapIndex], ordered[index]];
  }
  return ordered;
}

function renderExperimentMetadata() {
  const label = document.getElementById("experiment-label");
  const instructions = document.getElementById("instructions-text");
  const timerInstruction = document.getElementById("timer-instruction");

  if (label) {
    label.textContent = `${experimentConfig.label} | ${experimentConfig.mode}`;
  }
  if (instructions) {
    instructions.textContent = localizedInstructions();
  }
  if (timerInstruction) {
    timerInstruction.textContent = responseNavigationText();
  }
}

function responsePolicyText() {
  return experimentConfig.singleWordPerResponse
    ? t("responsePolicySingle")
    : t("responsePolicyGeneral");
}

function renderAnswerInputs() {
  const answersArea = document.getElementById("answers-area");
  answersArea.innerHTML = "";

  for (let index = 0; index < experimentConfig.responseCount; index++) {
    const input = document.createElement("input");
    input.type = "text";
    input.maxLength = experimentConfig.answerMaxLength;
    input.autocomplete = "off";
    input.spellcheck = false;
    answersArea.appendChild(input);
  }
  updateAnswerPlaceholders();
}

function updateAnswerPlaceholders() {
  const placeholder = experimentConfig.singleWordPerResponse
    ? t("answerPlaceholderSingle")
    : t("answerPlaceholderGeneral");
  document.querySelectorAll("#answers-area input").forEach(input => {
    input.placeholder = `${placeholder} (${interfaceLanguage === "ja" ? "任意" : "optional"})`;
  });
}

function updateProgressBar(id, current, total) {
  const bar = document.getElementById(id);
  if (!bar) {
    return;
  }
  const safeTotal = Math.max(Number(total) || 0, 1);
  const safeCurrent = Math.min(Math.max(Number(current) || 0, 0), safeTotal);
  bar.style.width = `${(safeCurrent / safeTotal) * 100}%`;
}

function t(key, params = {}) {
  const value = UI_TEXT[interfaceLanguage]?.[key] || UI_TEXT.en[key] || key;
  return Object.entries(params).reduce(
    (text, [name, replacement]) => text.replaceAll(`{${name}}`, String(replacement)),
    value
  );
}

function localizedInstructions() {
  if (interfaceLanguage === "en") {
    return experimentConfig.instructions;
  }
  if (experimentConfig.stimulusPresentation === "audio" && hasFollowUp()) {
    return t("instructionsListeningFollowup");
  }
  return t("instructionsWritten");
}

function setText(id, key, params = {}) {
  const element = document.getElementById(id);
  if (element) {
    element.textContent = t(key, params);
  }
}

function applyLanguage() {
  document.documentElement.lang = interfaceLanguage === "ja" ? "ja" : "en";
  document.title = t("pageTitle");
  for (const lang of ["en", "ja"]) {
    const button = document.getElementById(`lang-${lang}`);
    if (button) {
      const active = interfaceLanguage === lang;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", active ? "true" : "false");
    }
  }

  setText("participant-info-text", "participantPrompt");
  const participantInput = document.getElementById("participant-id");
  if (participantInput) {
    participantInput.placeholder = t("participantPlaceholder");
  }
  setText("save-participant-id", "submit");
  setText("download-saved-backup", "downloadSavedBackup");
  setText("clear-saved-backup", "clearSavedBackup");
  setText("start-btn", "startTest");
  setText("download-backup-btn", "downloadBackup");
  setText("download-followup-backup-btn", "downloadBackup");
  setText("next-btn", "next");
  setText("followup-next-btn", "next");
  setText("continue-break-btn", "continue");
  setText("start-followup-btn", "startPart2");
  setText("download-btn", "downloadResults");
  setText("download-json-btn", "downloadJson");
  setText("clear-saved-backup-result", "clearSavedBackup");
  setText("thank-you-title", "thankYou");
  setText("break-title", "breakTitle");
  setText("break-message", "breakMessage");
  setText("phase-break-title", "part1CompleteTitle");
  setText("phase-break-message", "part1CompleteMessage");
  setText("download-status", autoDownloadTriggered ? "autoDownloadDone" : "autoDownloadPending");

  renderExperimentMetadata();
  updateAnswerPlaceholders();
  if (activePhase === "association") {
    setTimerInstruction(
      experimentConfig.stimulusPresentation === "audio" && !currentResponseTimerStarted
        ? t("playAudioTimer")
        : responseNavigationText()
    );
  }
  if (activePhase === "association") {
    const firstInput = document.querySelector("#answers-area input");
    if (firstInput) {
      firstInput.focus();
    }
  }
  if (activePhase === "break") {
    setText("break-title", "breakTitle");
    setText("break-message", "breakMessage");
  }
  if (activePhase === "followup") {
    const draft = collectFollowUpFormDraft();
    showFollowUpStep({ preserveTiming: true, draft });
  }
}

function setInterfaceLanguage(language) {
  if (language !== "en" && language !== "ja") {
    return;
  }
  interfaceLanguage = language;
  try {
    localStorage.setItem(LANGUAGE_STORAGE_KEY, language);
  } catch (_error) {
    // Language switching should still work if storage is unavailable.
  }
  applyLanguage();
  persistAutosave("language_changed");
}

function responseNavigationText() {
  return `${responsePolicyText()} ${t("navigationInstruction", { seconds: experimentConfig.timerSeconds })}`;
}

function setupUI() {
  const saveIDBtn = document.getElementById("save-participant-id");
  const participantInput = document.getElementById("participant-id");
  const startBtn = document.getElementById("start-btn");
  const backupBtn = document.getElementById("download-backup-btn");
  const followUpBackupBtn = document.getElementById("download-followup-backup-btn");
  const savedBackupBtn = document.getElementById("download-saved-backup");
  const clearSavedBackupBtn = document.getElementById("clear-saved-backup");
  const clearSavedBackupResultBtn = document.getElementById("clear-saved-backup-result");
  const nextBtn = document.getElementById("next-btn");
  const continueBreakBtn = document.getElementById("continue-break-btn");
  const startFollowUpBtn = document.getElementById("start-followup-btn");
  const followUpNextBtn = document.getElementById("followup-next-btn");
  const langEnBtn = document.getElementById("lang-en");
  const langJaBtn = document.getElementById("lang-ja");
  const answersArea = document.getElementById("answers-area");
  const followUpForm = document.getElementById("followup-form");

  saveIDBtn.addEventListener("click", saveParticipantID);
  startBtn.addEventListener("click", startTest);
  if (backupBtn) {
    backupBtn.addEventListener("click", downloadCurrentBackup);
  }
  if (followUpBackupBtn) {
    followUpBackupBtn.addEventListener("click", downloadCurrentBackup);
  }
  if (savedBackupBtn) {
    savedBackupBtn.addEventListener("click", downloadLatestSavedBackup);
  }
  if (clearSavedBackupBtn) {
    clearSavedBackupBtn.addEventListener("click", clearLatestSavedBackup);
  }
  if (clearSavedBackupResultBtn) {
    clearSavedBackupResultBtn.addEventListener("click", clearLatestSavedBackup);
  }
  if (nextBtn) {
    nextBtn.addEventListener("click", () => nextStimulus("button"));
  }
  if (continueBreakBtn) {
    continueBreakBtn.addEventListener("click", continueAfterBreak);
  }
  if (startFollowUpBtn) {
    startFollowUpBtn.addEventListener("click", startFollowUp);
  }
  if (followUpNextBtn) {
    followUpNextBtn.addEventListener("click", nextFollowUpStep);
  }
  if (langEnBtn) {
    langEnBtn.addEventListener("click", () => setInterfaceLanguage("en"));
  }
  if (langJaBtn) {
    langJaBtn.addEventListener("click", () => setInterfaceLanguage("ja"));
  }
  if (answersArea) {
    answersArea.addEventListener("input", () => {
      if (activePhase === "association") {
        persistAutosave("input");
      }
    });
  }
  if (followUpForm) {
    followUpForm.addEventListener("input", () => {
      if (activePhase === "followup") {
        persistAutosave("input");
      }
    });
  }

  participantInput.addEventListener("keydown", event => {
    if (event.key === "Enter") {
      saveParticipantID();
    }
  });

  window.addEventListener("keydown", event => {
    if (activePhase === "association" && event.code === experimentConfig.advanceKey) {
      event.preventDefault();
    }
  });

  window.addEventListener("keyup", event => {
    if (activePhase === "association" && event.code === experimentConfig.advanceKey) {
      event.preventDefault();
      nextStimulus();
    }
  });

  window.addEventListener("beforeunload", event => {
    if (!testInProgress) {
      return;
    }
    persistAutosave("beforeunload");
    event.preventDefault();
    event.returnValue = "";
  });
}

function saveParticipantID() {
  const idInput = document.getElementById("participant-id");
  participantID = idInput.value.trim();

  if (!participantID) {
    alert(t("alertParticipantId"));
    return;
  }

  document.getElementById("participant-info").style.display = "none";
  document.getElementById("instructions").style.display = "block";
}

function startTest() {
  const instructions = document.getElementById("instructions");
  const testArea = document.getElementById("test-area");
  const breakArea = document.getElementById("break-area");
  const phaseBreakArea = document.getElementById("phase-break-area");
  const resultArea = document.getElementById("result-area");

  if (testInProgress) return;

  stimuli = buildStimulusOrder(experimentConfig);
  responses = [];
  followUpResponses = [];
  completedAssociationBreakOrders = [];
  autoDownloadTriggered = false;
  currentIndex = 0;
  followUpIndex = 0;
  followUpStage = "recognition";
  participantSessionId = createSessionId();
  startedAt = new Date().toISOString();
  completedAt = "";
  testStartMs = performance.now();
  testInProgress = true;
  activePhase = "association";

  instructions.style.display = "none";
  if (breakArea) {
    breakArea.style.display = "none";
  }
  if (phaseBreakArea) {
    phaseBreakArea.style.display = "none";
  }
  resultArea.style.display = "none";
  testArea.style.display = "block";

  showStimulus(currentIndex);
  persistAutosave("start");
}

function showStimulus(index) {
  clearAutoNextTimer();
  clearAudioArea();

  const stimElem = document.getElementById("stimulus");
  const progress = document.getElementById("progress");
  stimElem.textContent = stimulusLabel(stimuli[index], index);
  startTime = 0;
  currentStimulusStartedAt = "";
  currentStimulusPresentedAtMs = performance.now();
  currentResponseTimerStarted = false;
  currentAudioLog = emptyAudioLog();

  if (progress) {
    progress.textContent = `${index + 1} / ${stimuli.length}`;
  }
  updateProgressBar("association-progress-bar", index + 1, stimuli.length);

  const answersArea = document.getElementById("answers-area");
  answersArea.querySelectorAll("input").forEach(input => {
    input.value = "";
  });

  const firstInput = answersArea.querySelector("input");
  if (firstInput) {
    firstInput.focus();
  }

  if (experimentConfig.stimulusPresentation === "audio") {
    setTimerInstruction(t("playAudioTimer"));
    renderAudioStimulus(stimuli[index], index);
  } else {
    startResponseTimer("text_display");
  }
  persistAutosave("stimulus_shown");
}

function stimulusLabel(stimulus, index) {
  if (experimentConfig.stimulusPresentation === "audio") {
    return t("itemLabel", { number: index + 1 });
  }
  return stimulus;
}

function renderAudioStimulus(stimulus, index) {
  if (experimentConfig.stimulusPresentation !== "audio") {
    return;
  }

  const audioArea = document.getElementById("audio-area");
  if (!audioArea || !experimentConfig.audioBasePath) {
    return;
  }

  const audio = document.createElement("audio");
  audio.controls = true;
  audio.preload = "auto";
  const audioSrc = audioPathForStimulus(stimulus, index);
  audio.src = audioSrc;
  const audioLog = {
    ...emptyAudioLog(),
    audioFile: stripQueryString(audioSrc),
    audioSrc
  };
  currentAudioLog = audioLog;
  audio.addEventListener("loadedmetadata", () => {
    if (audioLog.audioLoadedMetadataAtMs === "") {
      audioLog.audioLoadedMetadataAtMs = elapsedSinceItemPresented();
    }
    persistAutosave("audio_loadedmetadata");
  });
  audio.addEventListener("canplay", () => {
    if (audioLog.audioCanPlayAtMs === "") {
      audioLog.audioCanPlayAtMs = elapsedSinceItemPresented();
    }
    persistAutosave("audio_canplay");
  });
  audio.addEventListener("play", () => {
    const elapsed = elapsedSinceItemPresented();
    audioLog.audioPlayCount += 1;
    if (audioLog.audioFirstPlayAtMs === "") {
      audioLog.audioFirstPlayAtMs = elapsed;
      startResponseTimer("audio_play");
    }
    audioLog.audioLastPlayAtMs = elapsed;
    persistAutosave("audio_play");
  });
  audio.addEventListener("ended", () => {
    audioLog.audioEndedCount += 1;
    audioLog.audioLastEndedAtMs = elapsedSinceItemPresented();
    persistAutosave("audio_ended");
  });
  audio.onerror = () => {
    audioLog.audioErrorAtMs = elapsedSinceItemPresented();
    audioArea.textContent = "Audio file unavailable. Please tell the researcher.";
    persistAutosave("audio_error");
  };
  audioArea.appendChild(audio);

  if (experimentConfig.audioAutoplay) {
    audio.play().catch(() => {
      const elapsed = elapsedSinceItemPresented();
      audioLog.audioAutoplayBlockedAtMs = audioLog.audioAutoplayBlockedAtMs || elapsed;
      audioLog.audioPlayFailureAtMs = audioLog.audioPlayFailureAtMs || elapsed;
      persistAutosave("audio_autoplay_blocked");
    });
  }
}

function audioPathForStimulus(stimulus, index) {
  if (experimentConfig.audioFiles && experimentConfig.audioFiles[stimulus]) {
    return versionedAudioPath(experimentConfig.audioFiles[stimulus]);
  }

  const order = String(index + 1).padStart(2, "0");
  const filePart = sanitizeFilePart(stimulus).toLowerCase();
  return versionedAudioPath(`${experimentConfig.audioBasePath}/${order}-${filePart}.${experimentConfig.audioExtension}`);
}

function versionedAudioPath(path) {
  if (!experimentConfig.audioVersion) {
    return path;
  }
  const separator = path.includes("?") ? "&" : "?";
  return `${path}${separator}v=${encodeURIComponent(experimentConfig.audioVersion)}`;
}

function clearAudioArea() {
  const audioArea = document.getElementById("audio-area");
  if (audioArea) {
    audioArea.innerHTML = "";
  }
}

function nextStimulus(advanceTrigger = "manual") {
  if (!testInProgress) return;
  if (experimentConfig.stimulusPresentation === "audio" && !currentResponseTimerStarted) {
    alert(t("alertPlayAudio"));
    persistAutosave("advance_blocked_before_audio_play");
    return;
  }

  clearAutoNextTimer();

  const endTime = performance.now();
  const stimulusEndedAt = new Date().toISOString();
  const reactionTime = endTime - startTime;
  const answersArea = document.getElementById("answers-area");
  const inputs = answersArea.querySelectorAll("input");
  const ansList = Array.from(inputs).map(input => input.value.trim());
  if (experimentConfig.singleWordPerResponse) {
    const multiwordAnswer = ansList.find(answer => lexicalWordCount(answer) > 1);
    if (multiwordAnswer) {
      alert(t("alertOneWord"));
      persistAutosave("advance_blocked_multiword_answer");
      return;
    }
  }
  const stimWord = stimuli[currentIndex];

  responses.push({
    stimulusOrder: currentIndex + 1,
    stimulus: stimWord,
    answers: ansList,
    stimulusStartedAt: currentStimulusStartedAt,
    stimulusEndedAt,
    elapsedSinceTestStartMs: Math.round(endTime - testStartMs),
    reactionTime,
    advanceTrigger,
    autoAdvanced: advanceTrigger === "timer",
    audio: { ...currentAudioLog }
  });
  persistAutosave("item_complete");

  currentIndex++;
  if (currentIndex < stimuli.length) {
    if (shouldShowAssociationBreak(currentIndex)) {
      showAssociationBreak(currentIndex);
    } else {
      showStimulus(currentIndex);
    }
  } else {
    completeAssociationTask();
  }
}

function shouldShowAssociationBreak(completedItemCount) {
  const breakOrders = experimentConfig.breaks?.associationAfterStimulusOrders || [];
  return Boolean(
    experimentConfig.breaks?.enabled &&
    breakOrders.includes(completedItemCount) &&
    !completedAssociationBreakOrders.includes(completedItemCount)
  );
}

function showAssociationBreak(completedItemCount) {
  clearAutoNextTimer();
  activePhase = "break";
  completedAssociationBreakOrders.push(completedItemCount);
  document.getElementById("test-area").style.display = "none";
  const breakArea = document.getElementById("break-area");
  if (breakArea) {
    breakArea.style.display = "block";
  }
  setText("break-title", "breakTitle");
  setText("break-message", "breakMessage");
  window.scrollTo(0, 0);
  persistAutosave("association_break");
}

function continueAfterBreak() {
  if (activePhase !== "break") {
    return;
  }
  const breakArea = document.getElementById("break-area");
  if (breakArea) {
    breakArea.style.display = "none";
  }
  activePhase = "association";
  showStimulus(currentIndex);
  persistAutosave("association_break_continue");
}

function completeAssociationTask() {
  if (hasFollowUp()) {
    showFollowUpIntro();
  } else {
    finishTest();
  }
}

function hasFollowUp() {
  const followUp = experimentConfig.followUp || {};
  return Boolean(followUp.enabled && (followUp.recognition?.enabled || followUp.semantic?.enabled));
}

function showFollowUpIntro() {
  clearAutoNextTimer();
  activePhase = "phase_break";
  document.getElementById("test-area").style.display = "none";
  document.getElementById("phase-break-area").style.display = "block";
  window.scrollTo(0, 0);
  persistAutosave("followup_intro");
}

function startFollowUp() {
  clearAutoNextTimer();
  activePhase = "followup";
  document.getElementById("test-area").style.display = "none";
  const phaseBreakArea = document.getElementById("phase-break-area");
  if (phaseBreakArea) {
    phaseBreakArea.style.display = "none";
  }
  document.getElementById("followup-area").style.display = "block";
  followUpIndex = 0;
  followUpStage = experimentConfig.followUp.recognition?.enabled ? "recognition" : "semantic";
  showFollowUpStep();
  persistAutosave("followup_start");
}

function showFollowUpStep(options = {}) {
  const stimulus = stimuli[followUpIndex];
  const progress = document.getElementById("followup-progress");
  const title = document.getElementById("followup-title");
  const instruction = document.getElementById("followup-instruction");
  const cue = document.getElementById("followup-cue");
  const form = document.getElementById("followup-form");

  if (!options.preserveTiming) {
    currentFollowUpStartedAt = new Date().toISOString();
    currentFollowUpStartedAtMs = performance.now();
  }
  form.innerHTML = "";

  if (progress) {
    const label = followUpStage === "recognition" ? t("followupListeningLabel") : t("followupMeaningLabel");
    progress.textContent = `Follow-up ${followUpIndex + 1} / ${stimuli.length} - ${label}`;
  }
  updateProgressBar("followup-progress-bar", followUpIndex + 1, stimuli.length);

  if (followUpStage === "recognition") {
    title.textContent = t("itemLabel", { number: followUpIndex + 1 });
    instruction.textContent = t("recognitionInstruction");
    cue.style.display = "none";
    cue.textContent = "";
    renderRecognitionForm(form);
  } else {
    title.textContent = t("semanticTitle");
    instruction.textContent = t("semanticInstruction");
    cue.style.display = "block";
    cue.textContent = stimulus;
    renderSemanticForm(form, stimulus);
  }

  if (options.draft) {
    restoreFollowUpFormDraft(options.draft);
  }

  const firstControl = form.querySelector("input[type='text'], input[type='radio'], input[type='range']");
  if (firstControl) {
    firstControl.focus();
  }
  window.scrollTo(0, 0);
}

function collectFollowUpFormDraft() {
  const draft = {
    text: {},
    range: {},
    radio: {}
  };
  document.querySelectorAll("#followup-form input[type='text']").forEach(input => {
    draft.text[input.id] = input.value;
  });
  document.querySelectorAll("#followup-form input[type='range']").forEach(input => {
    draft.range[input.id] = input.value;
  });
  document.querySelectorAll("#followup-form input[type='radio']:checked").forEach(input => {
    draft.radio[input.name] = input.value;
  });
  return draft;
}

function restoreFollowUpFormDraft(draft) {
  for (const [id, value] of Object.entries(draft.text || {})) {
    const input = document.getElementById(id);
    if (input) {
      input.value = value;
    }
  }
  for (const [id, value] of Object.entries(draft.range || {})) {
    const input = document.getElementById(id);
    if (input) {
      input.value = value;
    }
  }
  for (const [name, value] of Object.entries(draft.radio || {})) {
    const input = Array.from(document.querySelectorAll(`input[name="${name}"]`))
      .find(candidate => candidate.value === value);
    if (input) {
      input.checked = true;
    }
  }
}

function renderRecognitionForm(form) {
  const section = appendFollowUpSection(form, t("listeningSection"));
  appendTextField(section, {
    id: "heard-word",
    label: t("heardWordLabel"),
    maxLength: experimentConfig.followUp.recognition.heardWordMaxLength,
    placeholder: t("heardWordPlaceholder")
  });
  appendSlider(section, {
    id: "heard-confidence",
    label: t("heardConfidenceLabel"),
    leftLabel: t("notClearly"),
    rightLabel: t("veryClearly")
  });
}

function renderSemanticForm(form, stimulus) {
  const selfReportSection = appendFollowUpSection(form, t("meaningSection"));
  appendSlider(selfReportSection, {
    id: "meaning-confidence",
    label: t("meaningConfidenceLabel"),
    leftLabel: t("notAtAll"),
    rightLabel: t("veryConfident")
  });
  appendSlider(selfReportSection, {
    id: "response-confidence",
    label: t("responseConfidenceLabel"),
    leftLabel: t("notAtAll"),
    rightLabel: t("veryConfident")
  });
  appendTextField(selfReportSection, {
    id: "japanese-meaning",
    label: t("japaneseMeaningLabel"),
    maxLength: experimentConfig.followUp.semantic.japaneseMeaningMaxLength,
    placeholder: t("japaneseMeaningPlaceholder")
  });

  const probes = experimentConfig.followUp.probes?.[stimulus] || {};
  const probeSection = appendFollowUpSection(form, t("relationSection"));
  for (const type of ["collocation", "category", "synonym", "antonym"]) {
    if (probes[type]) {
      appendProbeOptions(probeSection, type, probes[type]);
    }
  }
}

function appendFollowUpSection(parent, title) {
  const section = document.createElement("section");
  section.className = "followup-section";
  const heading = document.createElement("h3");
  heading.textContent = title;
  section.appendChild(heading);
  parent.appendChild(section);
  return section;
}

function appendTextField(parent, { id, label, maxLength, placeholder }) {
  const field = document.createElement("div");
  field.className = "followup-field";
  const labelEl = document.createElement("label");
  labelEl.setAttribute("for", id);
  labelEl.textContent = label;
  const input = document.createElement("input");
  input.type = "text";
  input.id = id;
  input.maxLength = maxLength;
  input.placeholder = placeholder || "";
  input.autocomplete = "off";
  input.spellcheck = false;
  field.appendChild(labelEl);
  field.appendChild(input);
  parent.appendChild(field);
}

function appendSlider(parent, { id, label, leftLabel, rightLabel }) {
  const field = document.createElement("div");
  field.className = "followup-field";
  const labelEl = document.createElement("label");
  labelEl.setAttribute("for", id);
  labelEl.textContent = label;
  const input = document.createElement("input");
  input.type = "range";
  input.id = id;
  input.min = "0";
  input.max = "100";
  input.step = "1";
  input.value = "50";
  const labels = document.createElement("div");
  labels.className = "slider-labels";
  const left = document.createElement("span");
  left.textContent = leftLabel || "0";
  const right = document.createElement("span");
  right.textContent = rightLabel || "100";
  labels.appendChild(left);
  labels.appendChild(right);
  field.appendChild(labelEl);
  field.appendChild(input);
  field.appendChild(labels);
  parent.appendChild(field);
}

function appendProbeOptions(parent, type, probe) {
  const group = document.createElement("div");
  group.className = "followup-options";
  group.setAttribute("role", "radiogroup");
  group.setAttribute("aria-labelledby", `probe-title-${type}`);
  const title = document.createElement("div");
  title.id = `probe-title-${type}`;
  title.className = "followup-options-title";
  title.textContent = probe.prompt || type;
  group.appendChild(title);
  for (const option of normalizedProbeOptions(probe)) {
    const label = document.createElement("label");
    const input = document.createElement("input");
    input.type = "radio";
    input.name = `probe-${type}`;
    input.value = option.id;
    const optionText = document.createElement("span");
    optionText.textContent = option.label;
    label.appendChild(input);
    label.appendChild(optionText);
    group.appendChild(label);
  }
  parent.appendChild(group);
}

function normalizedProbeOptions(probe) {
  return (probe.options || []).map(option => {
    if (typeof option === "string") {
      return { id: option, label: option };
    }
    return {
      id: String(option.id || option.label || ""),
      label: String(option.label || option.id || "")
    };
  }).filter(option => option.id);
}

function nextFollowUpStep() {
  if (activePhase !== "followup") {
    return;
  }

  if (followUpStage === "recognition") {
    collectRecognitionResponse();
    if (experimentConfig.followUp.semantic?.enabled) {
      followUpStage = "semantic";
      showFollowUpStep();
      persistAutosave("followup_recognition_complete");
      return;
    }
  } else {
    collectSemanticResponse();
  }

  followUpIndex++;
  if (followUpIndex < stimuli.length) {
    followUpStage = experimentConfig.followUp.recognition?.enabled ? "recognition" : "semantic";
    showFollowUpStep();
    persistAutosave("followup_item_complete");
  } else {
    finishTest();
  }
}

function ensureFollowUpRecord() {
  const stimulusOrder = followUpIndex + 1;
  let record = followUpResponses.find(item => item.stimulusOrder === stimulusOrder);
  if (!record) {
    record = {
      stimulusOrder,
      stimulus: stimuli[followUpIndex],
      recognition: {},
      semantic: {
        probes: {}
      }
    };
    followUpResponses.push(record);
  }
  return record;
}

function collectRecognitionResponse() {
  const record = ensureFollowUpRecord();
  record.recognition = {
    startedAt: currentFollowUpStartedAt,
    endedAt: new Date().toISOString(),
    reactionTimeMs: Math.round(performance.now() - currentFollowUpStartedAtMs),
    heardWord: document.getElementById("heard-word")?.value.trim() || "",
    heardConfidence: document.getElementById("heard-confidence")?.value || ""
  };
}

function collectSemanticResponse() {
  const record = ensureFollowUpRecord();
  const probes = experimentConfig.followUp.probes?.[record.stimulus] || {};
  const semantic = {
    startedAt: currentFollowUpStartedAt,
    endedAt: new Date().toISOString(),
    reactionTimeMs: Math.round(performance.now() - currentFollowUpStartedAtMs),
    meaningConfidence: document.getElementById("meaning-confidence")?.value || "",
    responseConfidence: document.getElementById("response-confidence")?.value || "",
    japaneseMeaning: document.getElementById("japanese-meaning")?.value.trim() || "",
    probes: {}
  };

  for (const type of ["collocation", "category", "synonym", "antonym"]) {
    if (!probes[type]) {
      continue;
    }
    const choiceId = selectedRadioValue(`probe-${type}`);
    const correctId = probeCorrectId(probes[type]);
    semantic.probes[type] = {
      choiceId,
      choiceLabel: probeOptionLabel(probes[type], choiceId),
      correctOptionId: correctId,
      correctLabel: probeOptionLabel(probes[type], correctId),
      correct: Boolean(choiceId && correctId && choiceId === correctId)
    };
  }
  record.semantic = semantic;
}

function selectedRadioValue(name) {
  const checked = document.querySelector(`input[name="${name}"]:checked`);
  return checked ? checked.value : "";
}

function probeCorrectId(probe) {
  return String(probe.correctOptionId || probe.answer || probe.correct || "");
}

function probeOptionLabel(probe, id) {
  if (!id) {
    return "";
  }
  const option = normalizedProbeOptions(probe).find(item => item.id === id);
  return option ? option.label : id;
}

function finishTest() {
  testInProgress = false;
  activePhase = "complete";
  completedAt = new Date().toISOString();
  persistAutosave("complete");
  document.getElementById("test-area").style.display = "none";
  const breakArea = document.getElementById("break-area");
  if (breakArea) {
    breakArea.style.display = "none";
  }
  const phaseBreakArea = document.getElementById("phase-break-area");
  if (phaseBreakArea) {
    phaseBreakArea.style.display = "none";
  }
  document.getElementById("followup-area").style.display = "none";

  const resultArea = document.getElementById("result-area");
  resultArea.style.display = "block";

  const downloadBtn = document.getElementById("download-btn");
  downloadBtn.onclick = downloadResultsAsCSV;
  const downloadJsonBtn = document.getElementById("download-json-btn");
  if (downloadJsonBtn) {
    downloadJsonBtn.onclick = downloadResultsAsJSON;
  }
  applyLanguage();
  scheduleAutomaticDownloads();
}

function scheduleAutomaticDownloads() {
  if (autoDownloadTriggered) {
    return;
  }
  autoDownloadTriggered = true;
  setDownloadStatus(t("autoDownloadStarted"));
  window.setTimeout(() => {
    downloadResultsAsCSV();
    window.setTimeout(() => {
      downloadResultsAsJSON();
      setDownloadStatus(t("autoDownloadDone"));
    }, 500);
  }, 100);
}

function setDownloadStatus(text) {
  const status = document.getElementById("download-status");
  if (status) {
    status.textContent = text;
  }
}

function downloadResultsAsCSV() {
  const answerHeaders = Array.from(
    { length: experimentConfig.responseCount },
    (_item, index) => `Answer${index + 1}`
  );
  const header = [
    "ExperimentId",
    "ExperimentVersion",
    "Mode",
    "InterfaceLanguage",
    "StimulusPresentation",
    "StimulusSetId",
    "AudioVersion",
    "StimulusOrder",
    "StartedAt",
    "CompletedAt",
    "ParticipantSessionId",
    "Participant",
    "Stimulus",
    "StimulusStartedAt",
    "StimulusEndedAt",
    ...answerHeaders,
    "ReactionTime(ms)",
    "ElapsedSinceTestStart(ms)",
    "AdvanceTrigger",
    "AutoAdvanced",
    "AudioFile",
    "AudioPlayCount",
    "AudioEndedCount",
    "AudioFirstPlayAt(ms)",
    "AudioLastPlayAt(ms)",
    "AudioLastEndedAt(ms)",
    "AudioLoadedMetadataAt(ms)",
    "AudioCanPlayAt(ms)",
    "AudioPlayFailureAt(ms)",
    "AudioAutoplayBlockedAt(ms)",
    "AudioErrorAt(ms)",
    "AudioTimerStartedAt(ms)",
    "AudioTimerStartReason",
    "CompletedAssociationBreakOrders",
    ...followUpCsvHeaders()
  ];

  const rows = responses.map(response => [
    experimentConfig.experimentId,
    experimentConfig.experimentVersion,
    experimentConfig.mode,
    interfaceLanguage,
    experimentConfig.stimulusPresentation,
    experimentConfig.stimulusSetId,
    experimentConfig.audioVersion,
    response.stimulusOrder,
    startedAt,
    completedAt,
    participantSessionId,
    participantID,
    response.stimulus,
    response.stimulusStartedAt,
    response.stimulusEndedAt,
    ...response.answers,
    Math.round(response.reactionTime),
    response.elapsedSinceTestStartMs,
    response.advanceTrigger,
    response.autoAdvanced,
    response.audio.audioFile,
    response.audio.audioPlayCount,
    response.audio.audioEndedCount,
    response.audio.audioFirstPlayAtMs,
    response.audio.audioLastPlayAtMs,
    response.audio.audioLastEndedAtMs,
    response.audio.audioLoadedMetadataAtMs,
    response.audio.audioCanPlayAtMs,
    response.audio.audioPlayFailureAtMs,
    response.audio.audioAutoplayBlockedAtMs,
    response.audio.audioErrorAtMs,
    response.audio.audioTimerStartedAtMs,
    response.audio.audioTimerStartReason,
    completedAssociationBreakOrders.join("|"),
    ...followUpCsvValues(response)
  ]);

  const csv = [
    header.map(csvCell).join(","),
    ...rows.map(row => row.map(csvCell).join(","))
  ].join("\n");
  const fileName = `${completedExportStem()}.csv`;

  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function followUpCsvHeaders() {
  return [
    "FollowUpEnabled",
    "FollowUpCompleted",
    "FollowUpRecognitionStartedAt",
    "FollowUpRecognitionEndedAt",
    "FollowUpRecognitionRT(ms)",
    "HeardWord",
    "HeardConfidence",
    "FollowUpSemanticStartedAt",
    "FollowUpSemanticEndedAt",
    "FollowUpSemanticRT(ms)",
    "MeaningConfidence",
    "ResponseConfidence",
    "JapaneseMeaning",
    "CollocationChoice",
    "CollocationCorrect",
    "CollocationAnswer",
    "CategoryChoice",
    "CategoryCorrect",
    "CategoryAnswer",
    "SynonymChoice",
    "SynonymCorrect",
    "SynonymAnswer",
    "AntonymChoice",
    "AntonymCorrect",
    "AntonymAnswer"
  ];
}

function followUpCsvValues(response) {
  const record = followUpResponses.find(item => item.stimulusOrder === response.stimulusOrder) || {};
  const recognition = record.recognition || {};
  const semantic = record.semantic || {};
  const probes = semantic.probes || {};
  const completed = Boolean(recognition.endedAt || semantic.endedAt);

  return [
    hasFollowUp(),
    completed,
    recognition.startedAt || "",
    recognition.endedAt || "",
    recognition.reactionTimeMs || "",
    recognition.heardWord || "",
    recognition.heardConfidence || "",
    semantic.startedAt || "",
    semantic.endedAt || "",
    semantic.reactionTimeMs || "",
    semantic.meaningConfidence || "",
    semantic.responseConfidence || "",
    semantic.japaneseMeaning || "",
    probeCsvValue(probes.collocation, "choiceLabel"),
    probeCsvValue(probes.collocation, "correct"),
    probeCsvValue(probes.collocation, "correctLabel"),
    probeCsvValue(probes.category, "choiceLabel"),
    probeCsvValue(probes.category, "correct"),
    probeCsvValue(probes.category, "correctLabel"),
    probeCsvValue(probes.synonym, "choiceLabel"),
    probeCsvValue(probes.synonym, "correct"),
    probeCsvValue(probes.synonym, "correctLabel"),
    probeCsvValue(probes.antonym, "choiceLabel"),
    probeCsvValue(probes.antonym, "correct"),
    probeCsvValue(probes.antonym, "correctLabel")
  ];
}

function probeCsvValue(probe, key) {
  if (!probe) {
    return "";
  }
  return probe[key] ?? "";
}

function lexicalWordCount(value) {
  if (!value) {
    return 0;
  }
  const matches = value.match(/[A-Za-z]+(?:[-'][A-Za-z]+)*/g);
  return matches ? matches.length : 0;
}

function downloadResultsAsJSON() {
  const fileName = `${completedExportStem()}.json`;
  const payload = buildResultsPayload({ includeDraft: true, exportReason: "complete_json" });
  downloadJsonPayload(payload, fileName);
}

function downloadCurrentBackup() {
  persistAutosave("manual_backup");
  const safeParticipant = sanitizeFilePart(participantID);
  const safeExperiment = sanitizeFilePart(experimentConfig.experimentId);
  const safeSession = sanitizeFilePart(participantSessionId || "session");
  const fileName = `${experimentConfig.downloadPrefix}_${safeExperiment}_${safeParticipant}_${safeSession}_backup.json`;
  const payload = buildResultsPayload({ includeDraft: true, exportReason: "manual_backup" });
  downloadJsonPayload(payload, fileName);
}

function downloadLatestSavedBackup() {
  const saved = readLatestAutosave();
  if (!saved) {
    alert(t("alertNoBackup"));
    updateSavedBackupControl();
    return;
  }
  const typedParticipant = (
    participantID || document.getElementById("participant-id")?.value || ""
  ).trim();
  const participant = saved.payload?.participant?.participantId || "anonymous";
  if (!typedParticipant || typedParticipant !== participant) {
    alert(t("alertBackupParticipant"));
    return;
  }
  const session = saved.payload?.participant?.participantSessionId || "session";
  const experiment = saved.payload?.experiment?.experimentId || experimentConfig.experimentId;
  const fileName =
    `${experimentConfig.downloadPrefix}_${sanitizeFilePart(experiment)}_${sanitizeFilePart(participant)}_${sanitizeFilePart(session)}_saved_backup.json`;
  downloadJsonPayload(saved.payload, fileName);
}

function clearLatestSavedBackup() {
  const saved = readLatestAutosave();
  if (!saved) {
    alert(t("alertNoBackup"));
    updateSavedBackupControl();
    return;
  }
  const typedParticipant = (
    participantID || document.getElementById("participant-id")?.value || ""
  ).trim();
  const participant = saved.payload?.participant?.participantId || "anonymous";
  if (!typedParticipant || typedParticipant !== participant) {
    alert(t("alertClearParticipant"));
    return;
  }
  if (!window.confirm(t("confirmClearBackup"))) {
    return;
  }
  removeAutosaveRecord(saved.key);
  updateSavedBackupControl();
  alert(t("alertBackupCleared"));
}

function downloadJsonPayload(payload, fileName) {
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function completedExportStem() {
  const safeParticipant = sanitizeFilePart(participantID);
  const safeExperiment = sanitizeFilePart(experimentConfig.experimentId);
  const safeSession = sanitizeFilePart(participantSessionId || startedAt || "session");
  return `${experimentConfig.downloadPrefix}_${safeExperiment}_${safeParticipant}_${safeSession}`;
}

function buildResultsPayload(options = {}) {
  return {
    schemaVersion: experimentConfig.dataExportSchemaVersion || "lex30-browser-results-v2",
    exportedAt: new Date().toISOString(),
    experiment: {
      experimentId: experimentConfig.experimentId,
      experimentVersion: experimentConfig.experimentVersion,
      label: experimentConfig.label,
      mode: experimentConfig.mode,
      stimulusPresentation: experimentConfig.stimulusPresentation,
      stimulusSetId: experimentConfig.stimulusSetId,
      audioBasePath: experimentConfig.audioBasePath,
      audioExtension: experimentConfig.audioExtension,
      audioVersion: experimentConfig.audioVersion,
      responseCount: experimentConfig.responseCount,
      singleWordPerResponse: experimentConfig.singleWordPerResponse,
      breaksEnabled: Boolean(experimentConfig.breaks?.enabled),
      associationBreakAfterStimulusOrders: experimentConfig.breaks?.associationAfterStimulusOrders || [],
      timerSeconds: experimentConfig.timerSeconds,
      randomizeStimuli: experimentConfig.randomizeStimuli,
      followUpEnabled: hasFollowUp(),
      followUpSchemaVersion: experimentConfig.followUp?.schemaVersion || ""
    },
    participant: {
      participantId: participantID,
      participantSessionId,
      interfaceLanguage
    },
    timing: {
      startedAt,
      completedAt
    },
    state: {
      isComplete: Boolean(completedAt),
      testInProgress,
      currentIndex,
      completedResponseCount: responses.length,
      followUpIndex,
      followUpStage: activePhase === "followup" ? followUpStage : "",
      completedFollowUpCount: followUpResponses.filter(item => item.semantic?.endedAt || item.recognition?.endedAt).length,
      completedAssociationBreakOrders,
      totalStimuli: stimuli.length,
      exportReason: options.exportReason || ""
    },
    currentDraft: options.includeDraft ? collectCurrentDraft() : null,
    responses,
    followUpResponses
  };
}

function collectCurrentDraft() {
  if (!testInProgress) {
    return null;
  }
  if (activePhase === "followup") {
    return {
      phase: "followup",
      stimulusOrder: followUpIndex + 1,
      stimulus: stimuli[followUpIndex] || "",
      followUpStage,
      elapsedOnFollowUpStepMs: currentFollowUpStartedAtMs ? Math.round(performance.now() - currentFollowUpStartedAtMs) : ""
    };
  }
  if (activePhase === "break" || activePhase === "phase_break") {
    return {
      phase: activePhase,
      completedResponseCount: responses.length,
      nextStimulusOrder: currentIndex + 1,
      completedAssociationBreakOrders
    };
  }
  if (currentIndex >= stimuli.length) {
    return null;
  }
  const answersArea = document.getElementById("answers-area");
  const answers = answersArea
    ? Array.from(answersArea.querySelectorAll("input")).map(input => input.value.trim())
    : [];
  return {
    stimulusOrder: currentIndex + 1,
    stimulus: stimuli[currentIndex] || "",
    answers,
    stimulusStartedAt: currentStimulusStartedAt,
    elapsedOnItemMs: startTime ? Math.round(performance.now() - startTime) : "",
    elapsedSinceItemPresentedMs: elapsedSinceItemPresented(),
    responseTimerStarted: currentResponseTimerStarted,
    audio: { ...currentAudioLog }
  };
}

function persistAutosave(reason = "autosave") {
  if (!participantSessionId || !startedAt) {
    return;
  }
  try {
    const sessionKey = autosaveSessionKey();
    const payload = buildResultsPayload({ includeDraft: true, exportReason: reason });
    payload.autosave = {
      savedAt: new Date().toISOString(),
      expiresAt: autosaveExpiresAt(new Date()),
      retentionDays: AUTOSAVE_RETENTION_DAYS,
      reason,
      storageKey: sessionKey
    };
    localStorage.setItem(sessionKey, JSON.stringify(payload));
    localStorage.setItem(autosaveLatestKey(), sessionKey);
    updateSavedBackupControl();
  } catch (_error) {
    // Local browser storage can be disabled or full; data collection should continue.
  }
}

function autosaveSessionKey() {
  return `${AUTOSAVE_PREFIX}:${experimentConfig.experimentId}:${participantSessionId}`;
}

function autosaveLatestKey() {
  return `${AUTOSAVE_PREFIX}:${experimentConfig.experimentId}:latest`;
}

function readLatestAutosave() {
  try {
    const sessionKey = localStorage.getItem(autosaveLatestKey());
    if (!sessionKey) {
      return null;
    }
    const raw = localStorage.getItem(sessionKey);
    if (!raw) {
      localStorage.removeItem(autosaveLatestKey());
      return null;
    }
    const payload = JSON.parse(raw);
    if (isAutosaveExpired(payload)) {
      removeAutosaveRecord(sessionKey);
      return null;
    }
    return {
      key: sessionKey,
      payload
    };
  } catch (_error) {
    return null;
  }
}

function updateSavedBackupControl() {
  const savedBackupBtn = document.getElementById("download-saved-backup");
  const clearSavedBackupBtn = document.getElementById("clear-saved-backup");
  const clearSavedBackupResultBtn = document.getElementById("clear-saved-backup-result");
  const visible = readLatestAutosave() ? "inline-block" : "none";
  if (!savedBackupBtn) {
    return;
  }
  savedBackupBtn.style.display = visible;
  if (clearSavedBackupBtn) {
    clearSavedBackupBtn.style.display = visible;
  }
  if (clearSavedBackupResultBtn) {
    clearSavedBackupResultBtn.style.display = visible;
  }
}

function csvCell(value) {
  return `"${String(value ?? "").replace(/"/g, '""')}"`;
}

function sanitizeFilePart(value) {
  return String(value || "anonymous").replace(/[^A-Za-z0-9_-]+/g, "_").slice(0, 80);
}

function stripQueryString(value) {
  return String(value || "").split("?")[0];
}

function emptyAudioLog() {
  return {
    audioFile: "",
    audioSrc: "",
    audioPlayCount: 0,
    audioEndedCount: 0,
    audioFirstPlayAtMs: "",
    audioLastPlayAtMs: "",
    audioLastEndedAtMs: "",
    audioLoadedMetadataAtMs: "",
    audioCanPlayAtMs: "",
    audioPlayFailureAtMs: "",
    audioAutoplayBlockedAtMs: "",
    audioErrorAtMs: "",
    audioTimerStartedAtMs: "",
    audioTimerStartReason: ""
  };
}

function createSessionId() {
  const randomPart = Math.random().toString(36).slice(2, 10);
  return `${new Date().toISOString().replace(/[-:.TZ]/g, "")}_${randomPart}`;
}

function startAutoNextTimer() {
  autoNextTimer = setTimeout(() => {
    nextStimulus("timer");
  }, experimentConfig.timerSeconds * 1000);
}

function clearAutoNextTimer() {
  if (autoNextTimer) {
    clearTimeout(autoNextTimer);
    autoNextTimer = null;
  }
}

function startResponseTimer(reason) {
  if (currentResponseTimerStarted) {
    return;
  }
  startTime = performance.now();
  currentStimulusStartedAt = new Date().toISOString();
  currentResponseTimerStarted = true;
  if (experimentConfig.stimulusPresentation === "audio") {
    currentAudioLog.audioTimerStartedAtMs = elapsedSinceItemPresented();
    currentAudioLog.audioTimerStartReason = reason;
  }
  setTimerInstruction(responseNavigationText());
  startAutoNextTimer();
  persistAutosave(`timer_started_${reason}`);
}

function elapsedSinceItemPresented() {
  if (!currentStimulusPresentedAtMs) {
    return "";
  }
  return Math.round(performance.now() - currentStimulusPresentedAtMs);
}

function setTimerInstruction(text) {
  const timerInstruction = document.getElementById("timer-instruction");
  if (timerInstruction) {
    timerInstruction.textContent = text;
  }
}

function autosaveExpiresAt(savedAt) {
  const savedTime = savedAt instanceof Date ? savedAt.getTime() : new Date(savedAt).getTime();
  if (!Number.isFinite(savedTime)) {
    return "";
  }
  return new Date(savedTime + AUTOSAVE_RETENTION_DAYS * 24 * 60 * 60 * 1000).toISOString();
}

function isAutosaveExpired(payload) {
  const autosave = payload?.autosave || {};
  const expiresAt = autosave.expiresAt;
  if (expiresAt) {
    const expiry = new Date(expiresAt).getTime();
    return Number.isFinite(expiry) && Date.now() > expiry;
  }
  const savedAt = autosave.savedAt || payload?.exportedAt;
  if (!savedAt) {
    return false;
  }
  const savedTime = new Date(savedAt).getTime();
  if (!Number.isFinite(savedTime)) {
    return false;
  }
  return Date.now() - savedTime > AUTOSAVE_RETENTION_DAYS * 24 * 60 * 60 * 1000;
}

function removeAutosaveRecord(sessionKey) {
  try {
    localStorage.removeItem(sessionKey);
    if (localStorage.getItem(autosaveLatestKey()) === sessionKey) {
      localStorage.removeItem(autosaveLatestKey());
    }
  } catch (_error) {
    // Local storage may be unavailable; the visible control will simply remain hidden or stale.
  }
}

function pruneExpiredAutosaves() {
  try {
    const prefix = `${AUTOSAVE_PREFIX}:${experimentConfig.experimentId}:`;
    const keys = [];
    for (let index = 0; index < localStorage.length; index++) {
      const key = localStorage.key(index);
      if (key && key.startsWith(prefix) && !key.endsWith(":latest")) {
        keys.push(key);
      }
    }
    for (const key of keys) {
      const raw = localStorage.getItem(key);
      if (!raw) {
        removeAutosaveRecord(key);
        continue;
      }
      if (isAutosaveExpired(JSON.parse(raw))) {
        removeAutosaveRecord(key);
      }
    }
  } catch (_error) {
    // Expired browser backups are best-effort cleanup only.
  }
}
