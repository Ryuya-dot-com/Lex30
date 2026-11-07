const FALLBACK_EXPERIMENT_CONFIG = {
  experimentId: "lex30-original-written-v1",
  experimentVersion: "1.0.0",
  label: "Original Lex30 - written v1",
  mode: "written",
  stimulusPresentation: "text",
  responseModality: "written",
  spokenTaskStyle: "",
  discreteAdvanceMode: "vad_and_key",
  associationInstructionStyle: "free",
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
const PRACTICE_STIMULI = ["book", "water"];
const MATCHED_SPLIT_HALVES = {
  "updated-easycue-posbalanced-pilot-30-v0.3": {
    form_a: [
      "center", "garden", "doctor", "listen", "people",
      "early", "travel", "father", "school", "nature",
      "black", "member", "think", "begin", "report"
    ],
    form_b: [
      "health", "white", "course", "number", "office",
      "ground", "letter", "answer", "useful", "person",
      "mother", "family", "appear", "system", "return"
    ]
  }
};
const UI_TEXT = {
  en: {
    pageTitle: "Lex30 Test",
    participantPrompt: "Please enter your Participant ID to begin.",
    participantPlaceholder: "Enter your ID",
    submit: "Submit",
    downloadSavedBackup: "Download Saved Backup",
    clearSavedBackup: "Clear Saved Backup",
    startTest: "Start Test",
    instructionsListeningFollowup: "You will hear 30 English words. For each word, add up to 4 English words that come to your mind, one word at a time. Write only English words. After all 30 words, you will answer short follow-up questions about the words.",
    instructionsWritten: "You will see 30 English words. For each word, add up to 4 English words that come to your mind, one word at a time. Write only English words.",
    responsePolicySingle: "Enter one English word at a time. You can add up to {count} words.",
    responsePolicyGeneral: "Enter one response at a time. You can add up to {count} responses.",
    navigationInstruction: "Press SPACE or Next to go to the next word anytime, or wait {seconds} seconds.",
    playAudioTimer: "Play the audio. The timer starts when the audio begins.",
    answerPlaceholderSingle: "One English word",
    answerPlaceholderGeneral: "English word",
    addAnswer: "Add",
    answerCount: "{count} / {total}",
    answerLimitReached: "Maximum added",
    removeAnswer: "Remove",
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
    downloadZip: "Download Audio ZIP",
    micCheckTitle: "Microphone Check",
    micCheckText: "This version records your spoken English responses (16 kHz WAV). Please use headphones in a quiet room, enable your microphone, and test your voice level before starting.",
    micEnable: "Enable Microphone",
    micTest: "Record 2s Test",
    micContinue: "Continue",
    micNotConnected: "Microphone not connected yet.",
    micCalibrating: "Measuring room noise level... stay quiet for 1 second.",
    micReady: "Microphone ready (noise floor: {rms}). Speak to verify the green bar moves, or record a 2s test.",
    micTesting: "Recording 2-second test clip... speak now.",
    micTestDone: "Test clip ready. Play it back if needed, then click Continue.",
    micError: "Could not access microphone: {message}",
    instructionsSpokenContinuousText: "You will see 30 English words. For each word, speak up to 4 English words that come to your mind aloud within 30 seconds. Speak clearly in English only.",
    instructionsSpokenContinuousAudio: "You will hear 30 English words. After each word plays, speak up to 4 English words that come to your mind aloud within 30 seconds. Speak clearly in English only (headphones recommended).",
    instructionsSpokenDiscreteText: "You will see 30 English words. For each word, speak up to 4 English words aloud one word at a time as slots 1 to 4 advance. Speak clearly in English only.",
    instructionsSpokenDiscreteAudio: "You will hear 30 English words. After each word plays, speak up to 4 English words aloud one word at a time as slots 1 to 4 advance. Speak clearly in English only (headphones recommended).",
    instructionStarSuffix: "Always associate directly from the presented cue word itself, not by chaining from your previous answers.",
    spokenPolicyContinuous: "Speak up to {count} English words clearly. Press SPACE or Next when finished ({seconds}s limit).",
    spokenPolicyDiscreteVad: "Slot {slot} / {count}: Speak 1 English word clearly, then pause briefly (or press Enter/SPACE) for the next slot. Click Next to skip remaining slots.",
    spokenPolicyDiscreteKey: "Slot {slot} / {count}: Speak 1 English word clearly, then press Enter/SPACE for the next slot. Click Next to skip remaining slots.",
    spokenRecWaiting: "Waiting for cue audio",
    spokenRecActive: "Recording",
    spokenRecSpeaking: "Voice detected",
    spokenSlotActive: "Speaking slot",
    spokenSlotWaiting: "Waiting",
    spokenSlotRecorded: "Recorded ({ms} ms)",
    spokenNextSlotBtn: "Lock Word / Next Slot (Enter)",
    autoDownloadSpokenStarted: "Packaging CSV, JSON, and 16 kHz WAV recordings into a single ZIP download...",
    autoDownloadSpokenDone: "Automatic ZIP download started. Use the buttons below if you need to download again.",
    alertMicRequired: "Please enable your microphone before starting the spoken test.",
    alertParticipantId: "Please enter a valid Participant ID.",
    alertPlayAudio: "Please play the audio before moving to the next item.",
    alertOneWord: "Please add only one English word at a time.",
    alertAnswerLimit: "You can add up to {count} responses for this word.",
    alertNoBackup: "No saved backup is available for this version.",
    alertBackupParticipant: "Enter the matching Participant ID before downloading a saved backup on this device.",
    alertClearParticipant: "Enter the matching Participant ID before clearing a saved backup on this device.",
    confirmClearBackup: "Clear the saved browser backup for this participant and version on this device?",
    alertBackupCleared: "Saved browser backup cleared on this device.",
    practiceInstructionSuffix: "You will start with {count} un-scored practice items before the main items.",
    practiceProgress: "Practice {current} / {total} (not scored)",
    practiceAudioLabel: "Practice Item {number}",
    practiceCompleteTitle: "Practice Complete",
    practiceCompleteMessage: "Practice is finished. Click Continue to begin the {count} main items.",
    timerWaitingAudio: "Waiting for audio",
    replayAudio: "Replay",
    savedBackupSummary: "Saved backup on this device ({done} / {total} items). Enter matching ID to download or clear.",
    followupProgressPrefix: "Follow-up {current} / {total} - {stage}",
    dontKnowOption: "I don't know",
    audioUnavailable: "Audio file unavailable. Please tell the researcher.",
    setupErrorTitle: "Setup Error",
    setupErrorLabel: "This Lex30 session could not be loaded.",
    setupErrorHint: "{message}. Please use the researcher page, run the preflight check, and open the participant URL from a local web server."
  },
  ja: {
    pageTitle: "Lex30 テスト",
    participantPrompt: "参加者IDを入力してください。",
    participantPlaceholder: "IDを入力",
    submit: "送信",
    downloadSavedBackup: "保存済みバックアップをダウンロード",
    clearSavedBackup: "保存済みバックアップを削除",
    startTest: "開始",
    instructionsListeningFollowup: "これから30個の英単語を聞きます。各単語について、思い浮かんだ英単語を1語ずつ、最大4語まで追加してください。回答は必ず英語の単語にしてください。30項目が終わった後、同じ単語について短い確認問題に答えます。",
    instructionsWritten: "これから30個の英単語が表示されます。各単語について、思い浮かんだ英単語を1語ずつ、最大4語まで追加してください。回答は必ず英語の単語にしてください。",
    responsePolicySingle: "英語の単語を1語ずつ入力して追加してください。最大{count}語まで追加できます。",
    responsePolicyGeneral: "回答を1つずつ入力して追加してください。最大{count}個まで追加できます。",
    navigationInstruction: "準備ができたらSPACEキーまたはNextで次に進めます。{seconds}秒後には自動で進みます。",
    playAudioTimer: "音声を再生してください。音声が始まるとタイマーが開始します。",
    answerPlaceholderSingle: "英語1語",
    answerPlaceholderGeneral: "英単語",
    addAnswer: "追加",
    answerCount: "{count} / {total}",
    answerLimitReached: "上限まで追加済み",
    removeAnswer: "削除",
    itemLabel: "項目 {number}",
    next: "次へ",
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
    downloadZip: "音声ZIPをダウンロード",
    micCheckTitle: "マイク確認",
    micCheckText: "このバージョンでは英語の音声回答を録音します（16 kHz WAV）。静かな環境でヘッドホン・イヤホンを装着し、マイクを有効にして入力レベルを確認してください。",
    micEnable: "マイクを有効にする",
    micTest: "2秒テスト録音",
    micContinue: "次へ進む",
    micNotConnected: "マイクがまだ接続されていません。",
    micCalibrating: "周囲のノイズレベルを測定中です…1秒間静かにしてください。",
    micReady: "マイク準備完了（環境ノイズ: {rms}）。声を出して緑のバーが動くか確認するか、2秒テスト録音を試してください。",
    micTesting: "2秒間のテスト録音中…声を出してください。",
    micTestDone: "テスト録音が完了しました。必要に応じて再生確認し、「次へ進む」を押してください。",
    micError: "マイクにアクセスできませんでした: {message}",
    instructionsSpokenContinuousText: "これから30個の英単語が表示されます。各単語について、思い浮かんだ英単語を30秒以内に最大4語まで声に出して答えてください。回答は必ず英語の単語にしてください。",
    instructionsSpokenContinuousAudio: "これから30個の英単語を聞きます。各単語が再生されたら、思い浮かんだ英単語を30秒以内に最大4語まで声に出して答えてください。回答は必ず英語の単語にしてください（ヘッドホン推奨）。",
    instructionsSpokenDiscreteText: "これから30個の英単語が表示されます。各単語について、枠1〜4の順番に1語ずつ、思い浮かんだ英単語を最大4語まで声に出して答えてください。回答は必ず英語の単語にしてください。",
    instructionsSpokenDiscreteAudio: "これから30個の英単語を聞きます。各単語が再生されたら、枠1〜4の順番に1語ずつ、思い浮かんだ英単語を最大4語まで声に出して答えてください。回答は必ず英語の単語にしてください（ヘッドホン推奨）。",
    instructionStarSuffix: "前の自分の回答から連想をつなげるのではなく、常に提示された単語そのものから連想してください。",
    spokenPolicyContinuous: "英語で最大{count}語まで発話してください。終わったらSPACEキーまたは「次へ」で次の単語に進めます（制限時間{seconds}秒）。",
    spokenPolicyDiscreteVad: "枠 {slot} / {count}：英単語を1語発話して少し間を置く（またはEnter/SPACEを押す）と次の枠に進みます。残りを飛ばす場合は「次へ」を押してください。",
    spokenPolicyDiscreteKey: "枠 {slot} / {count}：英単語を1語発話し、EnterまたはSPACEキーを押して次の枠に進んでください。残りを飛ばす場合は「次へ」を押してください。",
    spokenRecWaiting: "音声再生待ち",
    spokenRecActive: "録音中",
    spokenRecSpeaking: "発話検出中",
    spokenSlotActive: "現在の回答枠",
    spokenSlotWaiting: "待機中",
    spokenSlotRecorded: "記録済 ({ms} ms)",
    spokenNextSlotBtn: "この語を確定 / 次の枠へ (Enter)",
    autoDownloadSpokenStarted: "CSV・JSON・16 kHz WAV音声を1つのZIPにまとめて自動ダウンロードしています...",
    autoDownloadSpokenDone: "ZIPの自動ダウンロードを開始しました。保存されない場合は下のボタンを使ってください。",
    alertMicRequired: "音声テストを開始する前にマイクを有効にしてください。",
    alertParticipantId: "有効な参加者IDを入力してください。",
    alertPlayAudio: "次に進む前に音声を再生してください。",
    alertOneWord: "英語の単語を1語ずつ追加してください。",
    alertAnswerLimit: "この単語には最大{count}個まで回答を追加できます。",
    alertNoBackup: "このバージョンで利用できる保存済みバックアップはありません。",
    alertBackupParticipant: "この端末の保存済みバックアップをダウンロードするには、一致する参加者IDを入力してください。",
    alertClearParticipant: "この端末の保存済みバックアップを削除するには、一致する参加者IDを入力してください。",
    confirmClearBackup: "この端末に保存された、この参加者・このバージョンのブラウザバックアップを削除しますか？",
    alertBackupCleared: "この端末の保存済みバックアップを削除しました。",
    practiceInstructionSuffix: "本番の前に、採点対象外の練習を{count}項目行います。",
    practiceProgress: "練習 {current} / {total}（採点対象外）",
    practiceAudioLabel: "練習項目 {number}",
    practiceCompleteTitle: "練習完了",
    practiceCompleteMessage: "練習が終わりました。「続ける」を押すと本番の{count}項目が始まります。",
    timerWaitingAudio: "音声再生待ち",
    replayAudio: "再生し直す",
    savedBackupSummary: "この端末に保存済みバックアップがあります（{done} / {total} 項目）。一致するIDを入力するとダウンロード・削除できます。",
    followupProgressPrefix: "確認問題 {current} / {total} - {stage}",
    dontKnowOption: "わからない",
    audioUnavailable: "音声ファイルを読み込めませんでした。実施担当者にお知らせください。",
    setupErrorTitle: "読み込みエラー",
    setupErrorLabel: "Lex30 セッションを読み込めませんでした。",
    setupErrorHint: "{message}。研究者設定ページ（researcher.html）でプリフライト確認を実行し、ローカルWebサーバーまたは配信URLから開いてください。"
  }
};

let experimentConfig = FALLBACK_EXPERIMENT_CONFIG;
let stimuli = [];
let practiceStimuli = [];
let practiceIndex = 0;
let practiceResponses = [];
let participantID = "";
let currentIndex = 0;
let responses = [];
let startTime = 0;
let startedAt = "";
let completedAt = "";
let autoNextTimer = null;
let timerTickInterval = null;
let inlineNoticeTimer = null;
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
let currentSlotOnsetMs = [];
let currentSlotCompletedMs = [];
let lastSetupErrorMessage = "";

const SPOKEN_TARGET_SAMPLE_RATE = 16000;
const SPOKEN_IDB_NAME = "lex30_spoken_autosave_v1";
const SPOKEN_IDB_STORE = "item_audio";
let micStream = null;
let audioContext = null;
let micSourceNode = null;
let micProcessorNode = null;
let micZeroGainNode = null;
let micTrackSettings = {};
let micNoiseFloorRms = 0.008;
let micReady = false;
let micCalibrating = false;
let micCalibrationSamples = [];
let micTestRecording = false;
let micTestChunks = [];
let isRecordingItem = false;
let itemPcmChunks = [];
let itemPeakRms = 0;
let isStimulusAudioPlaying = false;
let stimulusAudioEndedPerfMs = 0;
let currentSpokenSlot = 0;
let slotSpeechActive = false;
let slotSpeechAboveSinceMs = 0;
let slotSilenceSinceMs = 0;
let vadBursts = [];
let continuousSpeechActive = false;
let continuousBurstStartMs = 0;
let continuousSilenceSinceMs = 0;
let recordedItemWavs = new Map();

document.addEventListener("DOMContentLoaded", initializeApp);

async function initializeApp() {
  interfaceLanguage = initialInterfaceLanguage();
  setupLanguageToggleButtons();
  const toggleWrap = document.querySelector(".language-toggle");
  if (toggleWrap) {
    const params = new URLSearchParams(window.location.search);
    toggleWrap.style.display = params.get("langLock") === "1" ? "none" : "";
  }
  try {
    experimentConfig = await loadExperimentConfig();
    lastSetupErrorMessage = "";
    stimuli = buildStimulusOrder(experimentConfig);
    renderExperimentMetadata();
    renderAnswerInputs();
    setupUI();
    applyLanguage();
    pruneExpiredAutosaves();
    updateSavedBackupControl();
  } catch (error) {
    applyLanguage();
    showSetupError(error);
  }
}

function setupLanguageToggleButtons() {
  const langEnBtn = document.getElementById("lang-en");
  const langJaBtn = document.getElementById("lang-ja");
  if (langEnBtn && !langEnBtn.dataset.boundLang) {
    langEnBtn.dataset.boundLang = "1";
    langEnBtn.addEventListener("click", () => setInterfaceLanguage("en"));
  }
  if (langJaBtn && !langJaBtn.dataset.boundLang) {
    langJaBtn.dataset.boundLang = "1";
    langJaBtn.addEventListener("click", () => setInterfaceLanguage("ja"));
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
    // Ignore storage failures; fall through to browser locale or English.
  }
  if (typeof navigator !== "undefined" && /^ja\b/i.test(String(navigator.language || ""))) {
    return "ja";
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
  normalized.responseModality = normalized.responseModality === "spoken" ? "spoken" : "written";
  normalized.spokenTaskStyle = normalized.responseModality === "spoken"
    ? (normalized.spokenTaskStyle === "discrete_naming" ? "discrete_naming" : "continuous_4")
    : "";
  const params = new URLSearchParams(window.location.search);
  const advanceParam = params.get("advance");
  normalized.discreteAdvanceMode = advanceParam === "key_only" || advanceParam === "vad_and_key"
    ? advanceParam
    : (normalized.discreteAdvanceMode === "key_only" ? "key_only" : "vad_and_key");
  const instructionParam = params.get("instruction");
  normalized.associationInstructionStyle = instructionParam === "star_no_chaining" || instructionParam === "free"
    ? instructionParam
    : (normalized.associationInstructionStyle === "star_no_chaining" ? "star_no_chaining" : "free");
  const practiceParam = params.get("practice");
  normalized.practiceCount = practiceParam === "0" || practiceParam === "2"
    ? Number.parseInt(practiceParam, 10)
    : (normalized.responseModality === "spoken" ? 2 : 0);
  const subsetParam = params.get("subset");
  normalized.stimulusSubset = subsetParam === "form_a" || subsetParam === "form_b" ? subsetParam : "all";
  const orderParam = params.get("order");
  normalized.stimulusOrderPolicy = orderParam === "counterbalanced_ba" || orderParam === "random" || orderParam === "fixed"
    ? orderParam
    : (normalized.randomizeStimuli ? "random" : "fixed");
  normalized.followUp = normalizeFollowUp(normalized.followUp);
  normalized.stimuli = Array.isArray(normalized.stimuli)
    ? normalized.stimuli.map(item => String(item).trim()).filter(Boolean)
    : FALLBACK_EXPERIMENT_CONFIG.stimuli.slice();

  if (!normalized.stimuli.length) {
    normalized.stimuli = FALLBACK_EXPERIMENT_CONFIG.stimuli.slice();
  }
  normalized.canonicalStimuli = normalized.stimuli.slice();
  if (normalized.stimulusSubset === "form_a" || normalized.stimulusSubset === "form_b") {
    const matched = MATCHED_SPLIT_HALVES[normalized.stimulusSetId];
    if (matched && Array.isArray(matched[normalized.stimulusSubset])) {
      const allowed = new Set(matched[normalized.stimulusSubset]);
      normalized.stimuli = normalized.canonicalStimuli.filter(item => allowed.has(item));
    } else {
      const parity = normalized.stimulusSubset === "form_a" ? 0 : 1;
      normalized.stimuli = normalized.canonicalStimuli.filter((_item, idx) => idx % 2 === parity);
    }
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
  lastSetupErrorMessage = message;
  const label = document.getElementById("experiment-label");
  const errorPanel = document.getElementById("setup-error");
  const errorTitle = document.getElementById("setup-error-title");
  const errorText = document.getElementById("setup-error-text");

  for (const id of ["participant-info", "mic-check-area", "instructions", "test-area", "result-area"]) {
    const element = document.getElementById(id);
    if (element) {
      element.style.display = "none";
    }
  }
  if (errorTitle) {
    errorTitle.textContent = t("setupErrorTitle");
  }
  if (label) {
    label.textContent = t("setupErrorLabel");
  }
  if (errorText) {
    errorText.textContent = t("setupErrorHint", { message });
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
  const orderPolicy = config.stimulusOrderPolicy || (config.randomizeStimuli ? "random" : "fixed");
  if (orderPolicy === "fixed") {
    return ordered;
  }
  if (orderPolicy === "counterbalanced_ba") {
    const matched = MATCHED_SPLIT_HALVES[config.stimulusSetId];
    if ((config.stimulusSubset || "all") === "all" && matched) {
      const setB = new Set(matched.form_b);
      const partB = ordered.filter(item => setB.has(item));
      const partA = ordered.filter(item => !setB.has(item));
      return [...partB, ...partA];
    }
    const mid = Math.floor(ordered.length / 2);
    return [...ordered.slice(mid), ...ordered.slice(0, mid)];
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

function isSpokenMode() {
  return experimentConfig.responseModality === "spoken";
}

function isAssociationOrPracticePhase() {
  return activePhase === "association" || activePhase === "practice";
}

function isDiscreteNamingMode() {
  return isSpokenMode() && experimentConfig.spokenTaskStyle === "discrete_naming";
}

function isVadAdvanceEnabled() {
  return isDiscreteNamingMode() && experimentConfig.discreteAdvanceMode !== "key_only";
}

function resetItemSlotTimings() {
  currentSlotOnsetMs = Array.from({ length: experimentConfig.responseCount }, () => "");
  currentSlotCompletedMs = Array.from({ length: experimentConfig.responseCount }, () => "");
}

function responsePolicyText() {
  return experimentConfig.singleWordPerResponse
    ? t("responsePolicySingle", { count: experimentConfig.responseCount })
    : t("responsePolicyGeneral", { count: experimentConfig.responseCount });
}

function renderAnswerInputs() {
  const answersArea = document.getElementById("answers-area");
  answersArea.innerHTML = "";
  const spoken = isSpokenMode();

  const entry = document.createElement("div");
  entry.className = "association-entry";
  entry.hidden = spoken;

  const input = document.createElement("input");
  input.id = "association-answer-input";
  input.className = "association-answer-input";
  input.type = "text";
  input.maxLength = experimentConfig.answerMaxLength;
  input.autocomplete = "off";
  input.spellcheck = false;

  const addButton = document.createElement("button");
  addButton.id = "add-answer-btn";
  addButton.className = "secondary-button add-answer-button";
  addButton.type = "button";

  entry.append(input, addButton);
  answersArea.appendChild(entry);

  const count = document.createElement("div");
  count.id = "answer-count";
  count.className = "answer-count";
  count.hidden = spoken;
  answersArea.appendChild(count);

  const list = document.createElement("ol");
  list.id = "association-answer-list";
  list.className = "association-answer-list";
  list.hidden = spoken;
  answersArea.appendChild(list);

  const slots = document.createElement("div");
  slots.id = "association-answer-slots";
  slots.hidden = true;
  for (let index = 0; index < experimentConfig.responseCount; index++) {
    const slot = document.createElement("input");
    slot.type = "hidden";
    slot.dataset.answerSlot = String(index);
    slots.appendChild(slot);
  }
  answersArea.appendChild(slots);

  const spokenPanel = document.createElement("div");
  spokenPanel.id = "spoken-panel";
  spokenPanel.className = "spoken-panel";
  spokenPanel.hidden = !spoken;

  const statusRow = document.createElement("div");
  statusRow.className = "spoken-status-row";
  const badge = document.createElement("span");
  badge.id = "spoken-rec-badge";
  badge.className = "rec-badge";
  const slotSummary = document.createElement("span");
  slotSummary.id = "spoken-slot-summary";
  statusRow.append(badge, slotSummary);

  const meterTrack = document.createElement("div");
  meterTrack.className = "mic-meter-track";
  const meterFill = document.createElement("div");
  meterFill.id = "spoken-meter-fill";
  meterFill.className = "mic-meter-fill";
  meterTrack.appendChild(meterFill);

  const slotsGrid = document.createElement("div");
  slotsGrid.id = "spoken-slots-grid";
  slotsGrid.className = "spoken-slots-grid";
  for (let index = 0; index < experimentConfig.responseCount; index++) {
    const card = document.createElement("div");
    card.className = "spoken-slot-card";
    card.dataset.spokenSlot = String(index);
    card.innerHTML = `<span>#${index + 1}</span><small data-spoken-slot-status="${index}">-</small>`;
    slotsGrid.appendChild(card);
  }

  const slotBtnWrap = document.createElement("div");
  slotBtnWrap.style.marginTop = "12px";
  slotBtnWrap.style.textAlign = "center";
  slotBtnWrap.hidden = !isDiscreteNamingMode();
  const slotBtn = document.createElement("button");
  slotBtn.id = "spoken-slot-btn";
  slotBtn.type = "button";
  slotBtn.className = "secondary-button";
  slotBtnWrap.appendChild(slotBtn);

  spokenPanel.append(statusRow, meterTrack, slotsGrid, slotBtnWrap);
  answersArea.appendChild(spokenPanel);

  resetItemSlotTimings();
  updateAnswerPlaceholders();
  renderCommittedAnswers();
  updateSpokenUi(false);
}

function updateAnswerPlaceholders() {
  const placeholder = experimentConfig.singleWordPerResponse
    ? t("answerPlaceholderSingle")
    : t("answerPlaceholderGeneral");
  const input = document.getElementById("association-answer-input");
  if (input) {
    input.placeholder = `${placeholder} (${interfaceLanguage === "ja" ? "任意" : "optional"})`;
  }
  setText("add-answer-btn", "addAnswer");
  renderCommittedAnswers();
}

function associationAnswerSlots() {
  return Array.from(document.querySelectorAll("#answers-area input[data-answer-slot]"));
}

function currentAssociationInput() {
  return document.getElementById("association-answer-input");
}

function committedAssociationAnswers() {
  return associationAnswerSlots().map(input => input.value.trim());
}

function collectAssociationAnswers(options = {}) {
  const answers = committedAssociationAnswers();
  if (options.includePending) {
    const pending = currentAssociationInput()?.value.trim() || "";
    if (pending) {
      const emptyIndex = answers.findIndex(answer => !answer);
      if (emptyIndex >= 0) {
        answers[emptyIndex] = pending;
      }
    }
  }
  while (answers.length < experimentConfig.responseCount) {
    answers.push("");
  }
  return answers.slice(0, experimentConfig.responseCount);
}

function setAssociationAnswers(answers) {
  const compacted = Array.from({ length: experimentConfig.responseCount }, (_item, index) => {
    return answers[index] ? String(answers[index]).trim() : "";
  });
  associationAnswerSlots().forEach((slot, index) => {
    slot.value = compacted[index] || "";
  });
  renderCommittedAnswers();
}

function clearAssociationAnswers() {
  const input = currentAssociationInput();
  if (input) {
    input.value = "";
  }
  resetItemSlotTimings();
  setAssociationAnswers([]);
}

function addAssociationAnswerFromInput(options = {}) {
  if (isSpokenMode()) {
    return true;
  }
  const input = currentAssociationInput();
  if (!input) {
    return true;
  }
  const value = input.value.trim();
  if (!value) {
    if (!options.silentIfEmpty) {
      input.focus();
    }
    return true;
  }
  if (experimentConfig.singleWordPerResponse && lexicalWordCount(value) > 1) {
    showInlineNotice("task-inline-notice", t("alertOneWord"), "error");
    persistAutosave("advance_blocked_multiword_answer");
    input.focus();
    return false;
  }

  const answers = committedAssociationAnswers();
  const emptyIndex = answers.findIndex(answer => !answer);
  if (emptyIndex < 0) {
    showInlineNotice("task-inline-notice", t("alertAnswerLimit", { count: experimentConfig.responseCount }), "warn");
    input.focus();
    return false;
  }
  clearInlineNotices();
  if (currentResponseTimerStarted && startTime > 0) {
    const relMs = Math.max(0, Math.round(performance.now() - startTime));
    if (currentSlotOnsetMs[emptyIndex] === "" || currentSlotOnsetMs[emptyIndex] === undefined) {
      currentSlotOnsetMs[emptyIndex] = relMs;
    }
    currentSlotCompletedMs[emptyIndex] = relMs;
  }
  answers[emptyIndex] = value;
  input.value = "";
  setAssociationAnswers(answers);
  persistAutosave("answer_added");
  const nextInput = currentAssociationInput();
  if (nextInput && !nextInput.disabled) {
    nextInput.focus();
  }
  return true;
}

function removeAssociationAnswer(index) {
  const prevAnswers = committedAssociationAnswers();
  const keptIndices = [];
  prevAnswers.forEach((ans, idx) => {
    if (idx !== index && ans) {
      keptIndices.push(idx);
    }
  });
  const answers = keptIndices.map(idx => prevAnswers[idx]);
  currentSlotOnsetMs = Array.from(
    { length: experimentConfig.responseCount },
    (_item, i) => (i < keptIndices.length ? currentSlotOnsetMs[keptIndices[i]] ?? "" : "")
  );
  currentSlotCompletedMs = Array.from(
    { length: experimentConfig.responseCount },
    (_item, i) => (i < keptIndices.length ? currentSlotCompletedMs[keptIndices[i]] ?? "" : "")
  );
  setAssociationAnswers(answers);
  const input = currentAssociationInput();
  if (input) {
    input.focus();
  }
  persistAutosave("answer_removed");
}

function renderCommittedAnswers() {
  const list = document.getElementById("association-answer-list");
  const count = document.getElementById("answer-count");
  const input = currentAssociationInput();
  const addButton = document.getElementById("add-answer-btn");
  const answers = committedAssociationAnswers().filter(Boolean);
  const isFull = answers.length >= experimentConfig.responseCount;

  if (count) {
    count.textContent = isFull
      ? `${t("answerCount", { count: answers.length, total: experimentConfig.responseCount })} - ${t("answerLimitReached")}`
      : t("answerCount", { count: answers.length, total: experimentConfig.responseCount });
  }
  if (input) {
    input.disabled = isFull;
    if (isFull) {
      input.placeholder = t("answerLimitReached");
    } else {
      const placeholder = experimentConfig.singleWordPerResponse
        ? t("answerPlaceholderSingle")
        : t("answerPlaceholderGeneral");
      input.placeholder = `${placeholder} (${interfaceLanguage === "ja" ? "任意" : "optional"})`;
    }
  }
  if (addButton) {
    addButton.disabled = isFull;
  }
  if (!list) {
    return;
  }
  list.innerHTML = "";
  answers.forEach((answer, index) => {
    const item = document.createElement("li");
    const word = document.createElement("span");
    word.className = "association-answer-word";
    word.textContent = answer;

    const removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.className = "answer-remove-button";
    removeButton.dataset.answerIndex = String(index);
    removeButton.textContent = "x";
    removeButton.setAttribute("aria-label", `${t("removeAnswer")} ${answer}`);

    item.append(word, removeButton);
    list.appendChild(item);
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
  let base = "";
  if (interfaceLanguage === "en") {
    base = experimentConfig.instructions;
  } else if (isSpokenMode()) {
    if (isDiscreteNamingMode()) {
      base = experimentConfig.stimulusPresentation === "audio"
        ? t("instructionsSpokenDiscreteAudio")
        : t("instructionsSpokenDiscreteText");
    } else {
      base = experimentConfig.stimulusPresentation === "audio"
        ? t("instructionsSpokenContinuousAudio")
        : t("instructionsSpokenContinuousText");
    }
  } else if (experimentConfig.stimulusPresentation === "audio" && hasFollowUp()) {
    base = t("instructionsListeningFollowup");
  } else {
    base = t("instructionsWritten");
  }
  const targetCount = Array.isArray(experimentConfig.stimuli) ? experimentConfig.stimuli.length : 30;
  if (targetCount !== 30) {
    base = base
      .replace(/\b30(?=\s+(?:English\s+words|words|listening\s+items|items)\b)/g, String(targetCount))
      .replaceAll("30個", `${targetCount}個`)
      .replaceAll("30項目", `${targetCount}項目`);
  }
  const parts = [base];
  if (experimentConfig.associationInstructionStyle === "star_no_chaining") {
    parts.push(t("instructionStarSuffix"));
  }
  if ((experimentConfig.practiceCount || 0) > 0) {
    parts.push(t("practiceInstructionSuffix", { count: experimentConfig.practiceCount }));
  }
  return parts.join(" ");
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
  setText("download-zip-btn", "downloadZip");
  setText("mic-check-title", "micCheckTitle");
  setText("mic-check-text", "micCheckText");
  setText("mic-enable-btn", "micEnable");
  setText("mic-test-btn", "micTest");
  setText("mic-continue-btn", "micContinue");
  setText("spoken-slot-btn", "spokenNextSlotBtn");
  if (!micReady && !micCalibrating) {
    setText("mic-check-status", "micNotConnected");
  } else if (micReady && !micTestRecording) {
    setText("mic-check-status", "micReady", { rms: micNoiseFloorRms.toFixed(4) });
  }
  setText("clear-saved-backup-result", "clearSavedBackup");
  setText("thank-you-title", "thankYou");
  setText("break-title", "breakTitle");
  setText("break-message", "breakMessage");
  setText("phase-break-title", "part1CompleteTitle");
  const phaseBreakMessage = document.getElementById("phase-break-message");
  if (phaseBreakMessage) {
    const targetCount = Array.isArray(experimentConfig.stimuli) ? experimentConfig.stimuli.length : 30;
    phaseBreakMessage.textContent = targetCount !== 30
      ? t("part1CompleteMessage")
          .replace(/\b30(?=\s+(?:listening\s+items|items)\b)/g, String(targetCount))
          .replaceAll("30個", `${targetCount}個`)
      : t("part1CompleteMessage");
  }
  setText(
    "download-status",
    autoDownloadTriggered
      ? (isSpokenMode() ? "autoDownloadSpokenDone" : "autoDownloadDone")
      : "autoDownloadPending"
  );

  renderExperimentMetadata();
  if (lastSetupErrorMessage) {
    setText("setup-error-title", "setupErrorTitle");
    setText("experiment-label", "setupErrorLabel");
    setText("setup-error-text", "setupErrorHint", { message: lastSetupErrorMessage });
  }
  updateAnswerPlaceholders();
  updateSavedBackupControl();
  updateSpokenUi(false);
  if (isAssociationOrPracticePhase()) {
    if (!currentResponseTimerStarted) {
      resetItemTimerVisual();
    }
    setTimerInstruction(
      experimentConfig.stimulusPresentation === "audio" && !currentResponseTimerStarted
        ? t("playAudioTimer")
        : responseNavigationText()
    );
    const stimElem = document.getElementById("stimulus");
    if (stimElem && experimentConfig.stimulusPresentation === "audio") {
      stimElem.textContent = activePhase === "practice"
        ? t("practiceAudioLabel", { number: practiceIndex + 1 })
        : stimulusLabel(stimuli[currentIndex], currentIndex);
    }
    const replayBtn = document.querySelector("#audio-area .audio-replay-btn");
    if (replayBtn) {
      replayBtn.textContent = t("replayAudio");
    }
    if (activePhase === "practice") {
      const progress = document.getElementById("progress");
      if (progress) {
        progress.textContent = t("practiceProgress", {
          current: practiceIndex + 1,
          total: practiceStimuli.length
        });
      }
    }
  }
  if (isAssociationOrPracticePhase()) {
    const firstInput = currentAssociationInput();
    if (firstInput) {
      firstInput.focus();
    }
  }
  if (activePhase === "break") {
    setText("break-title", "breakTitle");
    setText("break-message", "breakMessage");
  } else if (activePhase === "practice_complete") {
    setText("break-title", "practiceCompleteTitle");
    setText("break-message", "practiceCompleteMessage", { count: stimuli.length });
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
  if (isSpokenMode()) {
    if (isDiscreteNamingMode()) {
      const slot = Math.min(currentSpokenSlot + 1, experimentConfig.responseCount);
      return isVadAdvanceEnabled()
        ? t("spokenPolicyDiscreteVad", { slot, count: experimentConfig.responseCount })
        : t("spokenPolicyDiscreteKey", { slot, count: experimentConfig.responseCount });
    }
    return t("spokenPolicyContinuous", {
      count: experimentConfig.responseCount,
      seconds: experimentConfig.timerSeconds
    });
  }
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
  const micEnableBtn = document.getElementById("mic-enable-btn");
  const micTestBtn = document.getElementById("mic-test-btn");
  const micContinueBtn = document.getElementById("mic-continue-btn");
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
  setupLanguageToggleButtons();
  if (micEnableBtn) {
    micEnableBtn.addEventListener("click", enableMicrophone);
  }
  if (micTestBtn) {
    micTestBtn.addEventListener("click", recordMicTestClip);
  }
  if (micContinueBtn) {
    micContinueBtn.addEventListener("click", continueFromMicCheck);
  }
  if (answersArea) {
    answersArea.addEventListener("input", event => {
      if (isAssociationOrPracticePhase()) {
        if (!isSpokenMode() && event.target?.id === "association-answer-input" && currentResponseTimerStarted && startTime > 0) {
          const val = currentAssociationInput()?.value.trim() || "";
          if (val) {
            const emptyIndex = committedAssociationAnswers().findIndex(ans => !ans);
            if (emptyIndex >= 0 && (currentSlotOnsetMs[emptyIndex] === "" || currentSlotOnsetMs[emptyIndex] === undefined)) {
              currentSlotOnsetMs[emptyIndex] = Math.max(0, Math.round(performance.now() - startTime));
            }
          }
        }
        persistAutosave("input");
      }
    });
    answersArea.addEventListener("keydown", event => {
      if (!isAssociationOrPracticePhase() || event.target?.id !== "association-answer-input") {
        return;
      }
      if (event.key === "Enter" || event.code === "Space") {
        event.preventDefault();
        addAssociationAnswerFromInput();
      }
    });
    answersArea.addEventListener("click", event => {
      const target = event.target;
      if (!(target instanceof HTMLElement)) {
        return;
      }
      if (target.id === "spoken-slot-btn") {
        advanceSpokenSlot("button");
        return;
      }
      if (target.id === "add-answer-btn") {
        addAssociationAnswerFromInput();
        return;
      }
      const removeButton = target.closest(".answer-remove-button");
      if (removeButton) {
        const index = Number.parseInt(removeButton.dataset.answerIndex || "", 10);
        if (Number.isFinite(index)) {
          removeAssociationAnswer(index);
        }
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
    if (event.target?.id === "association-answer-input") {
      return;
    }
    if (isAssociationOrPracticePhase() && (event.code === experimentConfig.advanceKey || (isDiscreteNamingMode() && event.key === "Enter"))) {
      event.preventDefault();
    }
  });

  window.addEventListener("keyup", event => {
    if (event.target?.id === "association-answer-input") {
      return;
    }
    if (!isAssociationOrPracticePhase()) {
      return;
    }
    if (isDiscreteNamingMode() && (event.code === experimentConfig.advanceKey || event.key === "Enter")) {
      event.preventDefault();
      advanceSpokenSlot("key");
      return;
    }
    if (event.code === experimentConfig.advanceKey) {
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
    showInlineNotice("participant-inline-notice", t("alertParticipantId"), "error");
    idInput.focus();
    return;
  }
  clearInlineNotices();

  document.getElementById("participant-info").style.display = "none";
  if (isSpokenMode() && !micReady) {
    const micCheckArea = document.getElementById("mic-check-area");
    if (micCheckArea) {
      micCheckArea.style.display = "block";
      return;
    }
  }
  document.getElementById("instructions").style.display = "block";
}

function continueFromMicCheck() {
  if (isSpokenMode() && !micReady) {
    showInlineNotice("mic-inline-notice", t("alertMicRequired"), "error");
    return;
  }
  clearInlineNotices();
  const micCheckArea = document.getElementById("mic-check-area");
  if (micCheckArea) {
    micCheckArea.style.display = "none";
  }
  document.getElementById("instructions").style.display = "block";
}

function startTest() {
  const instructions = document.getElementById("instructions");
  const testArea = document.getElementById("test-area");
  const breakArea = document.getElementById("break-area");
  const phaseBreakArea = document.getElementById("phase-break-area");
  const resultArea = document.getElementById("result-area");

  if (testInProgress) return;
  if (isSpokenMode() && !micReady) {
    showInlineNotice("mic-inline-notice", t("alertMicRequired"), "error");
    return;
  }
  if (audioContext && audioContext.state === "suspended") {
    audioContext.resume().catch(() => {});
  }

  stimuli = buildStimulusOrder(experimentConfig);
  practiceStimuli = PRACTICE_STIMULI.slice(0, experimentConfig.practiceCount || 0);
  practiceIndex = 0;
  practiceResponses = [];
  responses = [];
  followUpResponses = [];
  completedAssociationBreakOrders = [];
  recordedItemWavs = new Map();
  autoDownloadTriggered = false;
  currentIndex = 0;
  followUpIndex = 0;
  followUpStage = "recognition";
  participantSessionId = createSessionId();
  startedAt = new Date().toISOString();
  completedAt = "";
  testStartMs = performance.now();
  testInProgress = true;

  instructions.style.display = "none";
  if (breakArea) {
    breakArea.style.display = "none";
  }
  if (phaseBreakArea) {
    phaseBreakArea.style.display = "none";
  }
  resultArea.style.display = "none";
  testArea.style.display = "block";

  if (practiceStimuli.length > 0) {
    activePhase = "practice";
    showPracticeStimulus(0);
  } else {
    activePhase = "association";
    showStimulus(currentIndex);
  }
  persistAutosave("start");
}

function showPracticeStimulus(index) {
  clearAutoNextTimer();
  clearAudioArea();
  clearInlineNotices();

  const stimWord = practiceStimuli[index];
  const stimElem = document.getElementById("stimulus");
  const stimCard = document.getElementById("stimulus-card");
  const progress = document.getElementById("progress");
  if (stimCard) {
    stimCard.classList.add("practice-mode");
  }
  stimElem.textContent = experimentConfig.stimulusPresentation === "audio"
    ? t("practiceAudioLabel", { number: index + 1 })
    : stimWord;
  startTime = 0;
  currentStimulusStartedAt = "";
  currentStimulusPresentedAtMs = performance.now();
  currentResponseTimerStarted = false;
  currentAudioLog = emptyAudioLog();

  if (progress) {
    progress.textContent = t("practiceProgress", {
      current: index + 1,
      total: practiceStimuli.length
    });
  }
  updateProgressBar("association-progress-bar", index + 1, practiceStimuli.length);
  resetItemTimerVisual();

  clearAssociationAnswers();
  resetSpokenItemState();
  const answerInput = currentAssociationInput();
  if (answerInput && !isSpokenMode()) {
    answerInput.focus();
  }

  if (experimentConfig.stimulusPresentation === "audio") {
    setTimerInstruction(t("playAudioTimer"));
    updateSpokenUi(false);
    renderAudioStimulus(stimWord, index);
  } else {
    startResponseTimer("text_display");
  }
  persistAutosave("practice_shown");
}

function showStimulus(index) {
  clearAutoNextTimer();
  clearAudioArea();
  clearInlineNotices();

  const stimElem = document.getElementById("stimulus");
  const stimCard = document.getElementById("stimulus-card");
  const progress = document.getElementById("progress");
  if (stimCard) {
    stimCard.classList.remove("practice-mode");
  }
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
  resetItemTimerVisual();

  clearAssociationAnswers();
  resetSpokenItemState();
  const answerInput = currentAssociationInput();
  if (answerInput && !isSpokenMode()) {
    answerInput.focus();
  }

  if (experimentConfig.stimulusPresentation === "audio") {
    setTimerInstruction(t("playAudioTimer"));
    updateSpokenUi(false);
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
  const audioSrc = activePhase === "practice"
    ? audioPathForPracticeStimulus(stimulus, index)
    : audioPathForStimulus(stimulus, index);
  if (!audioArea || !audioSrc) {
    return;
  }

  const audio = document.createElement("audio");
  audio.controls = true;
  audio.preload = "auto";
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
    isStimulusAudioPlaying = true;
    const elapsed = elapsedSinceItemPresented();
    audioLog.audioPlayCount += 1;
    if (audioLog.audioFirstPlayAtMs === "") {
      audioLog.audioFirstPlayAtMs = elapsed;
      startResponseTimer("audio_play");
    }
    audioLog.audioLastPlayAtMs = elapsed;
    persistAutosave("audio_play");
  });
  audio.addEventListener("pause", () => {
    isStimulusAudioPlaying = false;
  });
  audio.addEventListener("ended", () => {
    isStimulusAudioPlaying = false;
    stimulusAudioEndedPerfMs = performance.now();
    audioLog.audioEndedCount += 1;
    audioLog.audioLastEndedAtMs = elapsedSinceItemPresented();
    persistAutosave("audio_ended");
  });
  audio.onerror = () => {
    audioLog.audioErrorAtMs = elapsedSinceItemPresented();
    audioArea.textContent = t("audioUnavailable");
    persistAutosave("audio_error");
  };
  const replayBtn = document.createElement("button");
  replayBtn.type = "button";
  replayBtn.className = "backup-button audio-replay-btn";
  replayBtn.textContent = t("replayAudio");
  replayBtn.addEventListener("click", () => {
    audio.currentTime = 0;
    audio.play().catch(() => {});
  });
  audioArea.append(audio, replayBtn);

  if (experimentConfig.audioAutoplay) {
    audio.play().catch(() => {
      const elapsed = elapsedSinceItemPresented();
      audioLog.audioAutoplayBlockedAtMs = audioLog.audioAutoplayBlockedAtMs || elapsed;
      audioLog.audioPlayFailureAtMs = audioLog.audioPlayFailureAtMs || elapsed;
      persistAutosave("audio_autoplay_blocked");
    });
  }
}

function audioPathForPracticeStimulus(stimulus, index) {
  const order = String(index + 1).padStart(2, "0");
  const filePart = sanitizeFilePart(stimulus).toLowerCase();
  return `audio/practice/${order}-${filePart}.mp3`;
}

function audioPathForStimulus(stimulus, index) {
  if (experimentConfig.audioFiles && experimentConfig.audioFiles[stimulus]) {
    return versionedAudioPath(experimentConfig.audioFiles[stimulus]);
  }
  if (!experimentConfig.audioBasePath) {
    return "";
  }
  const canonical = Array.isArray(experimentConfig.canonicalStimuli)
    ? experimentConfig.canonicalStimuli
    : experimentConfig.stimuli;
  const canonicalIdx = Array.isArray(canonical) ? canonical.indexOf(stimulus) : -1;
  const order = String((canonicalIdx >= 0 ? canonicalIdx : index) + 1).padStart(2, "0");
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
  isStimulusAudioPlaying = false;
  const audioArea = document.getElementById("audio-area");
  if (audioArea) {
    const activeAudio = audioArea.querySelector("audio");
    if (activeAudio) {
      activeAudio.pause();
    }
    audioArea.innerHTML = "";
  }
}

function nextStimulus(advanceTrigger = "manual") {
  if (!testInProgress) return;
  if (experimentConfig.stimulusPresentation === "audio" && !currentResponseTimerStarted) {
    showInlineNotice("task-inline-notice", t("alertPlayAudio"), "warn");
    persistAutosave("advance_blocked_before_audio_play");
    return;
  }

  if (advanceTrigger !== "timer") {
    if (!addAssociationAnswerFromInput({ silentIfEmpty: true })) {
      return;
    }
    const candidateAnswers = collectAssociationAnswers({ includePending: false });
    if (!isSpokenMode() && experimentConfig.singleWordPerResponse) {
      const multiwordAnswer = candidateAnswers.find(answer => lexicalWordCount(answer) > 1);
      if (multiwordAnswer) {
        showInlineNotice("task-inline-notice", t("alertOneWord"), "error");
        persistAutosave("advance_blocked_multiword_answer");
        return;
      }
    }
  } else if (!isSpokenMode()) {
    const pendingVal = currentAssociationInput()?.value.trim() || "";
    if (pendingVal && (!experimentConfig.singleWordPerResponse || lexicalWordCount(pendingVal) <= 1)) {
      addAssociationAnswerFromInput({ silentIfEmpty: true });
    }
  }

  clearAutoNextTimer();
  clearInlineNotices();

  const endTime = performance.now();
  const stimulusEndedAt = new Date().toISOString();
  const reactionTime = endTime - startTime;
  const ansList = collectAssociationAnswers({ includePending: false });
  if (activePhase === "practice") {
    isRecordingItem = false;
    itemPcmChunks = [];
    continuousSpeechActive = false;
    practiceResponses.push({
      practiceOrder: practiceIndex + 1,
      stimulus: practiceStimuli[practiceIndex],
      reactionTime: Math.round(reactionTime),
      advanceTrigger,
      slotOnsetMs: currentSlotOnsetMs.slice(0, experimentConfig.responseCount)
    });
    practiceIndex += 1;
    if (practiceIndex < practiceStimuli.length) {
      showPracticeStimulus(practiceIndex);
    } else {
      showPracticeCompleteScreen();
    }
    return;
  }

  const stimWord = stimuli[currentIndex];
  const stimulusOrder = currentIndex + 1;
  const spokenMeta = isSpokenMode()
    ? finalizeSpokenItemRecording(stimulusOrder, stimWord, Math.round(reactionTime))
    : emptySpokenLog();
  const slotOnsets = currentSlotOnsetMs.slice(0, experimentConfig.responseCount);
  const slotCompleted = currentSlotCompletedMs.slice(0, experimentConfig.responseCount);

  responses.push({
    stimulusOrder,
    stimulus: stimWord,
    answers: ansList,
    slotOnsetMs: slotOnsets,
    slotCompletedMs: slotCompleted,
    stimulusStartedAt: currentStimulusStartedAt,
    stimulusEndedAt,
    elapsedSinceTestStartMs: Math.round(endTime - testStartMs),
    reactionTime,
    advanceTrigger,
    autoAdvanced: advanceTrigger === "timer",
    audio: { ...currentAudioLog },
    spoken: spokenMeta
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

function showPracticeCompleteScreen() {
  clearAutoNextTimer();
  activePhase = "practice_complete";
  document.getElementById("test-area").style.display = "none";
  const breakArea = document.getElementById("break-area");
  if (breakArea) {
    breakArea.style.display = "block";
  }
  setText("break-title", "practiceCompleteTitle");
  setText("break-message", "practiceCompleteMessage", { count: stimuli.length });
  window.scrollTo(0, 0);
  persistAutosave("practice_complete");
}

function continueAfterBreak() {
  if (activePhase !== "break" && activePhase !== "practice_complete") {
    return;
  }
  const wasPractice = activePhase === "practice_complete";
  const breakArea = document.getElementById("break-area");
  if (breakArea) {
    breakArea.style.display = "none";
  }
  document.getElementById("test-area").style.display = "block";
  activePhase = "association";
  if (wasPractice) {
    startedAt = new Date().toISOString();
    testStartMs = performance.now();
  }
  showStimulus(currentIndex);
  persistAutosave(wasPractice ? "main_test_started_after_practice" : "association_break_continue");
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
    progress.textContent = t("followupProgressPrefix", {
      current: followUpIndex + 1,
      total: stimuli.length,
      stage: label
    });
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
      const badge = document.getElementById(`${id}-value`);
      if (badge) {
        badge.textContent = `${value}%`;
      }
    }
  }
  for (const [name, value] of Object.entries(draft.radio || {})) {
    const input = Array.from(document.querySelectorAll(`input[name="${name}"]`))
      .find(candidate => candidate.value === value);
    if (input) {
      input.checked = true;
      input.closest("label")?.classList.add("selected");
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
  input.addEventListener("keydown", event => {
    if (event.key === "Enter" && !event.isComposing) {
      event.preventDefault();
      if (id === "heard-word" && followUpStage === "recognition") {
        nextFollowUpStep();
      }
    }
  });
  field.appendChild(labelEl);
  field.appendChild(input);
  parent.appendChild(field);
}

function appendSlider(parent, { id, label, leftLabel, rightLabel }) {
  const field = document.createElement("div");
  field.className = "followup-field";
  const labelEl = document.createElement("label");
  labelEl.setAttribute("for", id);
  const labelText = document.createElement("span");
  labelText.textContent = label;
  const valueBadge = document.createElement("span");
  valueBadge.id = `${id}-value`;
  valueBadge.className = "slider-value-badge";
  valueBadge.textContent = "50%";
  labelEl.append(labelText, valueBadge);
  const input = document.createElement("input");
  input.type = "range";
  input.id = id;
  input.min = "0";
  input.max = "100";
  input.step = "1";
  input.value = "50";
  input.addEventListener("input", () => {
    valueBadge.textContent = `${input.value}%`;
  });
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

function localizedProbePrompt(prompt, fallbackType = "") {
  const raw = String(prompt || fallbackType || "");
  if (interfaceLanguage !== "ja" || !raw) {
    return raw;
  }
  let match = raw.match(/^Which word often goes with (.+)\?$/);
  if (match) {
    return `「${match[1]}」とよく一緒に使われる語はどれですか？`;
  }
  match = raw.match(/^What kind of (?:thing|word) (?:is|are) (?:a |an )?(.+)\?$/);
  if (match) {
    return `「${match[1]}」はどのような種類のもの（語）ですか？`;
  }
  match = raw.match(/^Which (?:word|phrase|meaning) is closest(?: in meaning)? to (.+)\?$/);
  if (match) {
    return `「${match[1]}」に意味が最も近いものはどれですか？`;
  }
  match = raw.match(/^Which word is most opposite to (.+)\?$/);
  if (match) {
    return `「${match[1]}」の反対の意味に最も近い語はどれですか？`;
  }
  return raw;
}

function appendProbeOptions(parent, type, probe) {
  const group = document.createElement("div");
  group.className = "followup-options";
  group.setAttribute("role", "radiogroup");
  group.setAttribute("aria-labelledby", `probe-title-${type}`);
  const title = document.createElement("div");
  title.id = `probe-title-${type}`;
  title.className = "followup-options-title";
  title.textContent = localizedProbePrompt(probe.prompt, type);
  group.appendChild(title);
  for (const option of normalizedProbeOptions(probe)) {
    const label = document.createElement("label");
    const input = document.createElement("input");
    input.type = "radio";
    input.name = `probe-${type}`;
    input.value = option.id;
    input.addEventListener("change", () => {
      group.querySelectorAll("label").forEach(lbl => lbl.classList.remove("selected"));
      if (input.checked) {
        label.classList.add("selected");
      }
    });
    const optionText = document.createElement("span");
    optionText.textContent = option.id === "dont_know" ? t("dontKnowOption") : option.label;
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
  isRecordingItem = false;
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

  const downloadZipBtn = document.getElementById("download-zip-btn");
  if (downloadZipBtn) {
    downloadZipBtn.style.display = isSpokenMode() ? "inline-block" : "none";
    downloadZipBtn.onclick = downloadResultsAsZIP;
  }
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
  if (isSpokenMode()) {
    setDownloadStatus(t("autoDownloadSpokenStarted"));
    window.setTimeout(() => {
      downloadResultsAsZIP();
      setDownloadStatus(t("autoDownloadSpokenDone"));
    }, 120);
    return;
  }
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

function buildResultsCsvString() {
  const answerHeaders = Array.from(
    { length: experimentConfig.responseCount },
    (_item, index) => `Answer${index + 1}`
  );
  const slotOnsetHeaders = Array.from(
    { length: experimentConfig.responseCount },
    (_item, index) => `Slot${index + 1}Onset(ms)`
  );
  const slotCompletedHeaders = Array.from(
    { length: experimentConfig.responseCount },
    (_item, index) => `Slot${index + 1}Completed(ms)`
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
    ...followUpCsvHeaders(),
    "ResponseModality",
    "SpokenTaskStyle",
    "DiscreteAdvanceMode",
    "AssociationInstructionStyle",
    ...slotOnsetHeaders,
    ...slotCompletedHeaders,
    "SpokenAudioFile",
    "SpokenAudioSha256",
    "SpokenDuration(ms)",
    "SpokenSampleRate",
    "SpokenPeakRms",
    "SpokenNoiseFloorRms",
    "SpokenVadBurstCount",
    "SpokenClippedSamples",
    "StimulusSubset",
    "StimulusOrderPolicy"
  ];

  const rows = responses.map(response => {
    const onsets = Array.from(
      { length: experimentConfig.responseCount },
      (_item, idx) => response.slotOnsetMs?.[idx] ?? ""
    );
    const completed = Array.from(
      { length: experimentConfig.responseCount },
      (_item, idx) => response.slotCompletedMs?.[idx] ?? ""
    );
    const spk = response.spoken || {};
    return [
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
      ...followUpCsvValues(response),
      experimentConfig.responseModality || "written",
      experimentConfig.spokenTaskStyle || "",
      isDiscreteNamingMode() ? experimentConfig.discreteAdvanceMode : "",
      experimentConfig.associationInstructionStyle || "free",
      ...onsets,
      ...completed,
      spk.audioFile || "",
      spk.sha256 || "",
      spk.durationMs ?? "",
      spk.sampleRate || "",
      spk.peakRms ?? "",
      spk.noiseFloorRms ?? "",
      spk.vadBurstCount ?? "",
      spk.clippedSamples ?? "",
      experimentConfig.stimulusSubset || "all",
      experimentConfig.stimulusOrderPolicy || "fixed"
    ];
  });

  return [
    header.map(csvCell).join(","),
    ...rows.map(row => row.map(csvCell).join(","))
  ].join("\n");
}

function downloadResultsAsCSV() {
  const csv = buildResultsCsvString();
  const fileName = `${completedExportStem()}.csv`;
  triggerBlobDownload(new Blob([csv], { type: "text/csv;charset=utf-8;" }), fileName);
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

async function downloadLatestSavedBackup() {
  const saved = readLatestAutosave();
  if (!saved) {
    showInlineNotice("participant-inline-notice", t("alertNoBackup"), "warn");
    updateSavedBackupControl();
    return;
  }
  const typedParticipant = (
    participantID || document.getElementById("participant-id")?.value || ""
  ).trim();
  const participant = saved.payload?.participant?.participantId || "anonymous";
  if (!typedParticipant || typedParticipant !== participant) {
    showInlineNotice("participant-inline-notice", t("alertBackupParticipant"), "error");
    return;
  }
  clearInlineNotices();
  const session = saved.payload?.participant?.participantSessionId || "session";
  const experiment = saved.payload?.experiment?.experimentId || experimentConfig.experimentId;
  const stem = `${experimentConfig.downloadPrefix}_${sanitizeFilePart(experiment)}_${sanitizeFilePart(participant)}_${sanitizeFilePart(session)}_saved_backup`;
  if (saved.payload?.experiment?.responseModality === "spoken") {
    const idbWavs = await loadSpokenWavsFromIdb(saved.key);
    if (idbWavs.length > 0) {
      const encoder = new TextEncoder();
      const entries = [
        { name: `${stem}.json`, bytes: encoder.encode(JSON.stringify(saved.payload, null, 2)) },
        ...idbWavs.map(rec => ({ name: rec.fileName, bytes: rec.wavBytes }))
      ];
      triggerBlobDownload(new Blob([buildZipBytes(entries)], { type: "application/zip" }), `${stem}.zip`);
      return;
    }
  }
  downloadJsonPayload(saved.payload, `${stem}.json`);
}

function clearLatestSavedBackup() {
  const saved = readLatestAutosave();
  if (!saved) {
    showInlineNotice("participant-inline-notice", t("alertNoBackup"), "warn");
    updateSavedBackupControl();
    return;
  }
  const typedParticipant = (
    participantID || document.getElementById("participant-id")?.value || ""
  ).trim();
  const participant = saved.payload?.participant?.participantId || "anonymous";
  if (!typedParticipant || typedParticipant !== participant) {
    showInlineNotice("participant-inline-notice", t("alertClearParticipant"), "error");
    return;
  }
  if (!window.confirm(t("confirmClearBackup"))) {
    return;
  }
  removeAutosaveRecord(saved.key);
  deleteSpokenWavsFromIdb(saved.key);
  updateSavedBackupControl();
  if (activePhase === "complete") {
    setDownloadStatus(t("alertBackupCleared"));
  } else {
    showInlineNotice("participant-inline-notice", t("alertBackupCleared"), "warn");
  }
}

function triggerBlobDownload(blob, fileName) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function downloadJsonPayload(payload, fileName) {
  triggerBlobDownload(new Blob([JSON.stringify(payload, null, 2)], { type: "application/json;charset=utf-8;" }), fileName);
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
      responseModality: experimentConfig.responseModality || "written",
      spokenTaskStyle: experimentConfig.spokenTaskStyle || "",
      discreteAdvanceMode: isDiscreteNamingMode() ? experimentConfig.discreteAdvanceMode : "",
      associationInstructionStyle: experimentConfig.associationInstructionStyle || "free",
      stimulusSubset: experimentConfig.stimulusSubset || "all",
      stimulusOrderPolicy: experimentConfig.stimulusOrderPolicy || "fixed",
      practiceCount: experimentConfig.practiceCount || 0,
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
      interfaceLanguage,
      microphone: isSpokenMode()
        ? {
            trackSettings: micTrackSettings,
            noiseFloorRms: Number(micNoiseFloorRms.toFixed(5)),
            targetSampleRate: SPOKEN_TARGET_SAMPLE_RATE
          }
        : null
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
      practiceCompletedCount: practiceResponses.length,
      exportReason: options.exportReason || ""
    },
    currentDraft: options.includeDraft ? collectCurrentDraft() : null,
    practiceResponses,
    responses,
    followUpResponses
  };
}

function collectCurrentDraft() {
  if (!testInProgress) {
    return null;
  }
  if (activePhase === "practice" || activePhase === "practice_complete") {
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
  return {
    stimulusOrder: currentIndex + 1,
    stimulus: stimuli[currentIndex] || "",
    answers: collectAssociationAnswers({ includePending: true }),
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
  const savedCard = document.getElementById("saved-backup-card");
  const savedSummary = document.getElementById("saved-backup-summary");
  const saved = readLatestAutosave();
  const visible = saved ? "inline-block" : "none";
  if (savedCard) {
    savedCard.classList.toggle("visible", Boolean(saved));
  }
  if (savedSummary && saved) {
    const done = saved.payload?.state?.completedResponseCount ?? (saved.payload?.responses?.length || 0);
    const total = saved.payload?.state?.totalStimuli ?? (experimentConfig.stimuli?.length || 30);
    savedSummary.textContent = t("savedBackupSummary", { done, total });
  }
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

function showInlineNotice(elementId, message, kind = "warn") {
  const el = document.getElementById(elementId);
  if (!el) {
    if (typeof alert === "function") {
      alert(message);
    }
    return;
  }
  el.textContent = message;
  el.classList.toggle("error", kind === "error");
  el.classList.add("visible");
  if (inlineNoticeTimer) {
    clearTimeout(inlineNoticeTimer);
  }
  inlineNoticeTimer = setTimeout(() => {
    el.classList.remove("visible");
  }, 4500);
}

function clearInlineNotices() {
  if (inlineNoticeTimer) {
    clearTimeout(inlineNoticeTimer);
    inlineNoticeTimer = null;
  }
  for (const id of ["participant-inline-notice", "mic-inline-notice", "task-inline-notice"]) {
    const el = document.getElementById(id);
    if (el) {
      el.classList.remove("visible", "error");
      el.textContent = "";
    }
  }
}

function resetItemTimerVisual() {
  const bar = document.getElementById("item-timer-bar");
  const pill = document.getElementById("timer-pill");
  const totalSec = experimentConfig.timerSeconds || 30;
  if (bar) {
    bar.style.width = "100%";
    bar.classList.remove("urgent");
  }
  if (pill) {
    pill.classList.remove("urgent");
    pill.textContent = experimentConfig.stimulusPresentation === "audio" && !currentResponseTimerStarted
      ? t("timerWaitingAudio")
      : `${totalSec}s`;
  }
}

function updateItemTimerVisual() {
  if (!currentResponseTimerStarted || startTime <= 0) {
    return;
  }
  const bar = document.getElementById("item-timer-bar");
  const pill = document.getElementById("timer-pill");
  const totalMs = (experimentConfig.timerSeconds || 30) * 1000;
  const elapsedMs = Math.max(0, performance.now() - startTime);
  const remainMs = Math.max(0, totalMs - elapsedMs);
  const remainSec = Math.ceil(remainMs / 1000);
  const pct = totalMs > 0 ? Math.max(0, Math.min(100, (remainMs / totalMs) * 100)) : 0;
  const urgent = remainSec <= 6;
  if (bar) {
    bar.style.width = `${pct.toFixed(1)}%`;
    bar.classList.toggle("urgent", urgent);
  }
  if (pill) {
    pill.textContent = `${remainSec}s`;
    pill.classList.toggle("urgent", urgent);
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
  updateItemTimerVisual();
  if (timerTickInterval) {
    clearInterval(timerTickInterval);
  }
  timerTickInterval = setInterval(updateItemTimerVisual, 250);
  autoNextTimer = setTimeout(() => {
    nextStimulus("timer");
  }, experimentConfig.timerSeconds * 1000);
}

function clearAutoNextTimer() {
  if (timerTickInterval) {
    clearInterval(timerTickInterval);
    timerTickInterval = null;
  }
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
  if (isSpokenMode()) {
    startSpokenItemRecording();
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

function emptySpokenLog() {
  return {
    audioFile: "",
    sha256: "",
    durationMs: "",
    sampleRate: "",
    peakRms: "",
    noiseFloorRms: "",
    vadBurstCount: "",
    clippedSamples: ""
  };
}

function resetSpokenItemState() {
  isRecordingItem = false;
  itemPcmChunks = [];
  itemPeakRms = 0;
  currentSpokenSlot = 0;
  slotSpeechActive = false;
  slotSpeechAboveSinceMs = 0;
  slotSilenceSinceMs = 0;
  vadBursts = [];
  continuousSpeechActive = false;
  continuousBurstStartMs = 0;
  continuousSilenceSinceMs = 0;
  isStimulusAudioPlaying = false;
  stimulusAudioEndedPerfMs = 0;
  updateSpokenUi(false);
}

function startSpokenItemRecording() {
  resetSpokenItemState();
  isRecordingItem = true;
  updateSpokenUi(false);
}

function updateSpokenUi(voiceActive) {
  if (!isSpokenMode()) {
    return;
  }
  const badge = document.getElementById("spoken-rec-badge");
  const summary = document.getElementById("spoken-slot-summary");
  if (badge) {
    if (!currentResponseTimerStarted && experimentConfig.stimulusPresentation === "audio") {
      badge.textContent = t("spokenRecWaiting");
      badge.className = "rec-badge";
    } else if (voiceActive) {
      badge.textContent = `● ${t("spokenRecSpeaking")}`;
      badge.className = "rec-badge speaking";
    } else if (isRecordingItem) {
      badge.textContent = `● ${t("spokenRecActive")}`;
      badge.className = "rec-badge recording";
    } else {
      badge.textContent = "-";
      badge.className = "rec-badge";
    }
  }
  if (summary) {
    if (isDiscreteNamingMode()) {
      const shown = Math.min(currentSpokenSlot + 1, experimentConfig.responseCount);
      summary.textContent = t("answerCount", { count: shown, total: experimentConfig.responseCount });
    } else {
      const detected = Math.min(vadBursts.length, experimentConfig.responseCount);
      summary.textContent = t("answerCount", { count: detected, total: experimentConfig.responseCount });
    }
  }
  const cards = document.querySelectorAll("#spoken-slots-grid .spoken-slot-card");
  cards.forEach((card, idx) => {
    const statusEl = card.querySelector("[data-spoken-slot-status]");
    const onset = currentSlotOnsetMs[idx];
    const done = currentSlotCompletedMs[idx] !== "" && currentSlotCompletedMs[idx] !== undefined;
    card.classList.toggle("active", isDiscreteNamingMode() && isRecordingItem && idx === currentSpokenSlot);
    card.classList.toggle("done", done);
    if (statusEl) {
      if (onset !== "" && onset !== undefined) {
        statusEl.textContent = t("spokenSlotRecorded", { ms: onset });
      } else if (isDiscreteNamingMode() && isRecordingItem && idx === currentSpokenSlot) {
        statusEl.textContent = t("spokenSlotActive");
      } else {
        statusEl.textContent = t("spokenSlotWaiting");
      }
    }
  });
}

async function enableMicrophone() {
  const enableBtn = document.getElementById("mic-enable-btn");
  const testBtn = document.getElementById("mic-test-btn");
  const continueBtn = document.getElementById("mic-continue-btn");
  if (enableBtn) {
    enableBtn.disabled = true;
  }
  try {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      throw new Error("navigator.mediaDevices.getUserMedia is unavailable (use HTTPS or localhost)");
    }
    try {
      micStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: false,
          noiseSuppression: false,
          autoGainControl: false,
          channelCount: 1
        }
      });
    } catch (_strictErr) {
      micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    }
    const track = micStream.getAudioTracks()[0];
    micTrackSettings = track && track.getSettings ? track.getSettings() : {};

    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    audioContext = new AudioCtx();
    if (audioContext.state === "suspended") {
      await audioContext.resume();
    }
    micSourceNode = audioContext.createMediaStreamSource(micStream);
    // shortcut: ScriptProcessorNode runs on main thread (~46-85ms blocks); upgrade to a static AudioWorklet module if sub-10ms live VAD jitter is required (offline WAV onset in transcribe_spoken_lex30.py is already 1ms-exact).
    micProcessorNode = audioContext.createScriptProcessor(2048, 1, 1);
    micZeroGainNode = audioContext.createGain();
    micZeroGainNode.gain.value = 0;
    micProcessorNode.onaudioprocess = event => {
      onMicAudioFrame(event.inputBuffer.getChannelData(0));
    };
    micSourceNode.connect(micProcessorNode);
    micProcessorNode.connect(micZeroGainNode);
    micZeroGainNode.connect(audioContext.destination);

    micCalibrating = true;
    micCalibrationSamples = [];
    setText("mic-check-status", "micCalibrating");
    window.setTimeout(() => {
      micCalibrating = false;
      if (micCalibrationSamples.length > 0) {
        const sorted = micCalibrationSamples.slice().sort((a, b) => a - b);
        const medianRms = sorted[Math.floor(sorted.length / 2)];
        micNoiseFloorRms = Math.min(Math.max(medianRms, 0.002), 0.05);
      }
      micReady = true;
      setText("mic-check-status", "micReady", { rms: micNoiseFloorRms.toFixed(4) });
      if (testBtn) {
        testBtn.disabled = false;
      }
      if (continueBtn) {
        continueBtn.disabled = false;
      }
      if (enableBtn) {
        enableBtn.disabled = false;
      }
    }, 1000);
  } catch (error) {
    if (enableBtn) {
      enableBtn.disabled = false;
    }
    setText("mic-check-status", "micError", { message: error?.message || String(error) });
  }
}

function recordMicTestClip() {
  if (!micReady || !audioContext || micTestRecording) {
    return;
  }
  const testBtn = document.getElementById("mic-test-btn");
  const playbackWrap = document.getElementById("mic-test-playback-wrap");
  const playbackEl = document.getElementById("mic-test-playback");
  micTestChunks = [];
  micTestRecording = true;
  if (testBtn) {
    testBtn.disabled = true;
  }
  setText("mic-check-status", "micTesting");
  window.setTimeout(() => {
    micTestRecording = false;
    if (testBtn) {
      testBtn.disabled = false;
    }
    const encoded = encodeWav16kMono(micTestChunks, audioContext.sampleRate);
    micTestChunks = [];
    if (playbackEl && playbackWrap) {
      const blob = new Blob([encoded.wavBytes], { type: "audio/wav" });
      playbackEl.src = URL.createObjectURL(blob);
      playbackWrap.style.display = "block";
    }
    setText("mic-check-status", "micTestDone");
  }, 2000);
}

function frameRms(samples) {
  if (!samples || !samples.length) {
    return 0;
  }
  let sumSq = 0;
  for (let i = 0; i < samples.length; i++) {
    const v = samples[i];
    sumSq += v * v;
  }
  return Math.sqrt(sumSq / samples.length);
}

function onMicAudioFrame(inputChannel) {
  const rms = frameRms(inputChannel);
  const meterPercent = Math.min(100, Math.round(Math.pow(Math.min(rms * 8, 1), 0.65) * 100));
  const checkFill = document.getElementById("mic-check-meter-fill");
  if (checkFill) {
    checkFill.style.width = `${meterPercent}%`;
  }
  const spokenFill = document.getElementById("spoken-meter-fill");
  if (spokenFill) {
    spokenFill.style.width = `${meterPercent}%`;
  }
  if (micCalibrating) {
    micCalibrationSamples.push(rms);
    return;
  }
  if (micTestRecording) {
    micTestChunks.push(new Float32Array(inputChannel));
  }
  if (!isRecordingItem || !isAssociationOrPracticePhase()) {
    return;
  }

  if (activePhase === "association") {
    itemPcmChunks.push(new Float32Array(inputChannel));
  }
  if (rms > itemPeakRms) {
    itemPeakRms = rms;
  }

  const nowPerf = performance.now();
  const bleedBlocked = experimentConfig.stimulusPresentation === "audio" && (
    isStimulusAudioPlaying ||
    (stimulusAudioEndedPerfMs > 0 && nowPerf - stimulusAudioEndedPerfMs < 140)
  );
  if (bleedBlocked || startTime <= 0) {
    updateSpokenUi(false);
    return;
  }

  const speechThresh = Math.max(micNoiseFloorRms * 3.2, 0.014);
  const silenceThresh = Math.max(micNoiseFloorRms * 1.8, 0.009);
  const relMs = Math.max(0, Math.round(nowPerf - startTime));

  // Track speech bursts for continuous_4 diagnostics and slot onset pre-filling.
  if (rms >= speechThresh) {
    continuousSilenceSinceMs = 0;
    if (!continuousSpeechActive) {
      continuousSpeechActive = true;
      continuousBurstStartMs = relMs;
      if (!isDiscreteNamingMode() && vadBursts.length < experimentConfig.responseCount) {
        const slotIdx = vadBursts.length;
        if (currentSlotOnsetMs[slotIdx] === "" || currentSlotOnsetMs[slotIdx] === undefined) {
          currentSlotOnsetMs[slotIdx] = relMs;
        }
      }
    }
  } else if (continuousSpeechActive && rms < silenceThresh) {
    if (continuousSilenceSinceMs === 0) {
      continuousSilenceSinceMs = nowPerf;
    } else if (nowPerf - continuousSilenceSinceMs >= 260) {
      const endRelMs = Math.max(continuousBurstStartMs, Math.round(continuousSilenceSinceMs - startTime));
      if (endRelMs - continuousBurstStartMs >= 90) {
        const burstIdx = vadBursts.length;
        vadBursts.push({ onsetMs: continuousBurstStartMs, offsetMs: endRelMs });
        if (!isDiscreteNamingMode() && burstIdx < experimentConfig.responseCount) {
          currentSlotOnsetMs[burstIdx] = continuousBurstStartMs;
          currentSlotCompletedMs[burstIdx] = endRelMs;
        }
      }
      continuousSpeechActive = false;
      continuousSilenceSinceMs = 0;
    }
  }

  if (isDiscreteNamingMode() && currentSpokenSlot < experimentConfig.responseCount) {
    if (rms >= speechThresh) {
      slotSilenceSinceMs = 0;
      if (!slotSpeechActive) {
        if (slotSpeechAboveSinceMs === 0) {
          slotSpeechAboveSinceMs = nowPerf;
        }
        if (nowPerf - slotSpeechAboveSinceMs >= 45 || rms >= speechThresh * 1.6) {
          slotSpeechActive = true;
          if (currentSlotOnsetMs[currentSpokenSlot] === "" || currentSlotOnsetMs[currentSpokenSlot] === undefined) {
            currentSlotOnsetMs[currentSpokenSlot] = Math.max(0, Math.round(slotSpeechAboveSinceMs - startTime));
          }
        }
      }
    } else if (rms < silenceThresh) {
      slotSpeechAboveSinceMs = 0;
      if (slotSpeechActive && isVadAdvanceEnabled()) {
        if (slotSilenceSinceMs === 0) {
          slotSilenceSinceMs = nowPerf;
        } else if (nowPerf - slotSilenceSinceMs >= 450) {
          currentSlotCompletedMs[currentSpokenSlot] = Math.max(0, Math.round(slotSilenceSinceMs - startTime));
          advanceSpokenSlot("vad");
          return;
        }
      }
    }
  }

  updateSpokenUi(rms >= speechThresh || slotSpeechActive);
}

function advanceSpokenSlot(trigger = "key") {
  if (!testInProgress || !isAssociationOrPracticePhase() || !isDiscreteNamingMode()) {
    return;
  }
  if (experimentConfig.stimulusPresentation === "audio" && !currentResponseTimerStarted) {
    alert(t("alertPlayAudio"));
    return;
  }
  if (currentSpokenSlot >= experimentConfig.responseCount) {
    return;
  }
  const nowRel = startTime > 0 ? Math.max(0, Math.round(performance.now() - startTime)) : 0;
  if (currentSlotCompletedMs[currentSpokenSlot] === "" || currentSlotCompletedMs[currentSpokenSlot] === undefined) {
    if (slotSpeechActive && (currentSlotOnsetMs[currentSpokenSlot] === "" || currentSlotOnsetMs[currentSpokenSlot] === undefined)) {
      currentSlotOnsetMs[currentSpokenSlot] = nowRel;
    }
    currentSlotCompletedMs[currentSpokenSlot] = nowRel;
  }
  currentSpokenSlot += 1;
  slotSpeechActive = false;
  slotSpeechAboveSinceMs = 0;
  slotSilenceSinceMs = 0;
  updateSpokenUi(false);

  if (currentSpokenSlot >= experimentConfig.responseCount) {
    if (trigger === "vad") {
      const expectedPhase = activePhase;
      const expectedOrder = activePhase === "practice" ? practiceIndex : currentIndex;
      window.setTimeout(() => {
        const currentOrd = activePhase === "practice" ? practiceIndex : currentIndex;
        if (testInProgress && activePhase === expectedPhase && currentOrd === expectedOrder) {
          nextStimulus("vad_slots_complete");
        }
      }, 300);
    } else {
      nextStimulus("slots_complete");
    }
    return;
  }
  setTimerInstruction(responseNavigationText());
  persistAutosave(`spoken_slot_${currentSpokenSlot}`);
}

function finalizeSpokenItemRecording(stimulusOrder, stimWord, fallbackDurationMs) {
  isRecordingItem = false;
  if (continuousSpeechActive && startTime > 0) {
    const endRelMs = Math.max(continuousBurstStartMs, Math.round(performance.now() - startTime));
    if (endRelMs - continuousBurstStartMs >= 90) {
      const burstIdx = vadBursts.length;
      vadBursts.push({ onsetMs: continuousBurstStartMs, offsetMs: endRelMs });
      if (!isDiscreteNamingMode() && burstIdx < experimentConfig.responseCount) {
        currentSlotOnsetMs[burstIdx] = continuousBurstStartMs;
        currentSlotCompletedMs[burstIdx] = endRelMs;
      }
    }
    continuousSpeechActive = false;
  }

  const srcRate = audioContext?.sampleRate || 48000;
  const encoded = encodeWav16kMono(itemPcmChunks, srcRate);
  itemPcmChunks = [];
  const orderPad = String(stimulusOrder).padStart(2, "0");
  const safeWord = sanitizeFilePart(stimWord).toLowerCase();
  const fileName = `audio/${orderPad}-${safeWord}.wav`;
  const sha256 = sha256HexSync(encoded.wavBytes);
  const meta = {
    audioFile: fileName,
    sha256,
    durationMs: encoded.durationMs || fallbackDurationMs,
    sampleRate: SPOKEN_TARGET_SAMPLE_RATE,
    peakRms: Number(itemPeakRms.toFixed(5)),
    noiseFloorRms: Number(micNoiseFloorRms.toFixed(5)),
    vadBurstCount: vadBursts.length,
    vadBursts: vadBursts.slice(),
    clippedSamples: encoded.clippedSamples
  };
  recordedItemWavs.set(stimulusOrder, {
    stimulusOrder,
    stimulus: stimWord,
    fileName,
    wavBytes: encoded.wavBytes,
    ...meta
  });
  saveSpokenWavToIdb(autosaveSessionKey(), stimulusOrder, fileName, encoded.wavBytes, sha256);
  return meta;
}

function encodeWav16kMono(chunks, sourceSampleRate) {
  let totalSourceSamples = 0;
  for (const chunk of chunks) {
    totalSourceSamples += chunk.length;
  }
  const merged = new Float32Array(totalSourceSamples);
  let offset = 0;
  for (const chunk of chunks) {
    merged.set(chunk, offset);
    offset += chunk.length;
  }

  const safeSrcRate = Number(sourceSampleRate) > 0 ? Number(sourceSampleRate) : 48000;
  const ratio = safeSrcRate / SPOKEN_TARGET_SAMPLE_RATE;
  const outLength = totalSourceSamples > 0 ? Math.max(1, Math.round(totalSourceSamples / ratio)) : 0;
  const dataByteLen = outLength * 2;
  const wavBytes = new Uint8Array(44 + dataByteLen);
  const view = new DataView(wavBytes.buffer);

  writeAscii(view, 0, "RIFF");
  view.setUint32(4, 36 + dataByteLen, true);
  writeAscii(view, 8, "WAVE");
  writeAscii(view, 12, "fmt ");
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, 1, true);
  view.setUint32(24, SPOKEN_TARGET_SAMPLE_RATE, true);
  view.setUint32(28, SPOKEN_TARGET_SAMPLE_RATE * 2, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);
  writeAscii(view, 36, "data");
  view.setUint32(40, dataByteLen, true);

  let clippedSamples = 0;
  for (let i = 0; i < outLength; i++) {
    const start = Math.floor(i * ratio);
    const end = Math.min(totalSourceSamples, Math.max(start + 1, Math.floor((i + 1) * ratio)));
    let sum = 0;
    for (let j = start; j < end; j++) {
      sum += merged[j];
    }
    const sample = sum / (end - start);
    if (Math.abs(sample) >= 0.995) {
      clippedSamples += 1;
    }
    const clamped = Math.max(-1, Math.min(1, sample));
    const pcm16 = clamped < 0 ? Math.round(clamped * 32768) : Math.round(clamped * 32767);
    view.setInt16(44 + i * 2, pcm16, true);
  }

  return {
    wavBytes,
    durationMs: Math.round((outLength / SPOKEN_TARGET_SAMPLE_RATE) * 1000),
    clippedSamples
  };
}

function writeAscii(view, offset, text) {
  for (let i = 0; i < text.length; i++) {
    view.setUint8(offset + i, text.charCodeAt(i));
  }
}

function downloadResultsAsZIP() {
  const stem = completedExportStem();
  const encoder = new TextEncoder();
  const csvBytes = encoder.encode(buildResultsCsvString());
  const jsonPayload = buildResultsPayload({ includeDraft: false, exportReason: "complete_zip" });
  const jsonBytes = encoder.encode(JSON.stringify(jsonPayload, null, 2));
  const manifest = {
    schemaVersion: "lex30-spoken-recording-manifest-v1",
    generatedAt: new Date().toISOString(),
    experimentId: experimentConfig.experimentId,
    participantId: participantID,
    participantSessionId,
    spokenTaskStyle: experimentConfig.spokenTaskStyle,
    discreteAdvanceMode: isDiscreteNamingMode() ? experimentConfig.discreteAdvanceMode : "",
    associationInstructionStyle: experimentConfig.associationInstructionStyle,
    sampleRate: SPOKEN_TARGET_SAMPLE_RATE,
    channels: 1,
    bitsPerSample: 16,
    microphoneTrackSettings: micTrackSettings,
    ambientNoiseFloorRms: Number(micNoiseFloorRms.toFixed(5)),
    csvFile: `${stem}.csv`,
    jsonFile: `${stem}.json`,
    recordings: Array.from(recordedItemWavs.values()).map(rec => ({
      stimulusOrder: rec.stimulusOrder,
      stimulus: rec.stimulus,
      file: rec.fileName,
      bytes: rec.wavBytes.byteLength,
      sha256: rec.sha256,
      durationMs: rec.durationMs,
      peakRms: rec.peakRms,
      vadBurstCount: rec.vadBurstCount,
      clippedSamples: rec.clippedSamples
    }))
  };
  const entries = [
    { name: `${stem}.csv`, bytes: csvBytes },
    { name: `${stem}.json`, bytes: jsonBytes },
    { name: "recording_manifest.json", bytes: encoder.encode(JSON.stringify(manifest, null, 2)) }
  ];
  for (const rec of recordedItemWavs.values()) {
    entries.push({ name: rec.fileName, bytes: rec.wavBytes });
  }
  const zipBytes = buildZipBytes(entries);
  triggerBlobDownload(new Blob([zipBytes], { type: "application/zip" }), `${stem}.zip`);
}

const CRC32_TABLE = (() => {
  const table = new Uint32Array(256);
  for (let i = 0; i < 256; i++) {
    let c = i;
    for (let k = 0; k < 8; k++) {
      c = (c & 1) ? (0xedb88320 ^ (c >>> 1)) : (c >>> 1);
    }
    table[i] = c >>> 0;
  }
  return table;
})();

function crc32Bytes(bytes) {
  let crc = 0xffffffff;
  for (let i = 0; i < bytes.length; i++) {
    crc = CRC32_TABLE[(crc ^ bytes[i]) & 0xff] ^ (crc >>> 8);
  }
  return (crc ^ 0xffffffff) >>> 0;
}

function buildZipBytes(entries) {
  const encoder = new TextEncoder();
  const prepared = entries.map(entry => {
    const nameBytes = encoder.encode(entry.name);
    const data = entry.bytes instanceof Uint8Array ? entry.bytes : new Uint8Array(entry.bytes);
    return { nameBytes, data, crc: crc32Bytes(data), offset: 0 };
  });

  let localSize = 0;
  let centralSize = 0;
  for (const item of prepared) {
    item.offset = localSize;
    localSize += 30 + item.nameBytes.length + item.data.length;
    centralSize += 46 + item.nameBytes.length;
  }

  const out = new Uint8Array(localSize + centralSize + 22);
  const view = new DataView(out.buffer);
  let pos = 0;

  for (const item of prepared) {
    view.setUint32(pos, 0x04034b50, true);
    view.setUint16(pos + 4, 20, true);
    view.setUint16(pos + 6, 0x0800, true);
    view.setUint16(pos + 8, 0, true);
    view.setUint16(pos + 10, 0, true);
    view.setUint16(pos + 12, 0x21, true);
    view.setUint32(pos + 14, item.crc, true);
    view.setUint32(pos + 18, item.data.length, true);
    view.setUint32(pos + 22, item.data.length, true);
    view.setUint16(pos + 26, item.nameBytes.length, true);
    view.setUint16(pos + 28, 0, true);
    out.set(item.nameBytes, pos + 30);
    out.set(item.data, pos + 30 + item.nameBytes.length);
    pos += 30 + item.nameBytes.length + item.data.length;
  }

  const centralStart = pos;
  for (const item of prepared) {
    view.setUint32(pos, 0x02014b50, true);
    view.setUint16(pos + 4, 20, true);
    view.setUint16(pos + 6, 20, true);
    view.setUint16(pos + 8, 0x0800, true);
    view.setUint16(pos + 10, 0, true);
    view.setUint16(pos + 12, 0, true);
    view.setUint16(pos + 14, 0x21, true);
    view.setUint32(pos + 16, item.crc, true);
    view.setUint32(pos + 20, item.data.length, true);
    view.setUint32(pos + 24, item.data.length, true);
    view.setUint16(pos + 28, item.nameBytes.length, true);
    view.setUint16(pos + 30, 0, true);
    view.setUint16(pos + 32, 0, true);
    view.setUint16(pos + 34, 0, true);
    view.setUint16(pos + 36, 0, true);
    view.setUint32(pos + 38, 0, true);
    view.setUint32(pos + 42, item.offset, true);
    out.set(item.nameBytes, pos + 46);
    pos += 46 + item.nameBytes.length;
  }

  view.setUint32(pos, 0x06054b50, true);
  view.setUint16(pos + 4, 0, true);
  view.setUint16(pos + 6, 0, true);
  view.setUint16(pos + 8, prepared.length, true);
  view.setUint16(pos + 10, prepared.length, true);
  view.setUint32(pos + 12, centralSize, true);
  view.setUint32(pos + 16, centralStart, true);
  view.setUint16(pos + 20, 0, true);
  return out;
}

const SHA256_K = new Uint32Array([
  0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
  0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
  0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
  0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
  0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
  0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
  0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
  0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]);

function sha256HexSync(bytes) {
  const bitLenHi = Math.floor((bytes.length * 8) / 0x100000000);
  const bitLenLo = (bytes.length * 8) >>> 0;
  const padLen = ((bytes.length + 9 + 63) & ~63);
  const msg = new Uint8Array(padLen);
  msg.set(bytes);
  msg[bytes.length] = 0x80;
  const view = new DataView(msg.buffer);
  view.setUint32(padLen - 8, bitLenHi, false);
  view.setUint32(padLen - 4, bitLenLo, false);

  let h0 = 0x6a09e667, h1 = 0xbb67ae85, h2 = 0x3c6ef372, h3 = 0xa54ff53a;
  let h4 = 0x510e527f, h5 = 0x9b05688c, h6 = 0x1f83d9ab, h7 = 0x5be0cd19;
  const w = new Uint32Array(64);

  for (let offset = 0; offset < padLen; offset += 64) {
    for (let i = 0; i < 16; i++) {
      w[i] = view.getUint32(offset + i * 4, false);
    }
    for (let i = 16; i < 64; i++) {
      const s0 = ((w[i - 15] >>> 7) | (w[i - 15] << 25)) ^ ((w[i - 15] >>> 18) | (w[i - 15] << 14)) ^ (w[i - 15] >>> 3);
      const s1 = ((w[i - 2] >>> 17) | (w[i - 2] << 15)) ^ ((w[i - 2] >>> 19) | (w[i - 2] << 13)) ^ (w[i - 2] >>> 10);
      w[i] = (w[i - 16] + s0 + w[i - 7] + s1) >>> 0;
    }
    let a = h0, b = h1, c = h2, d = h3, e = h4, f = h5, g = h6, h = h7;
    for (let i = 0; i < 64; i++) {
      const S1 = ((e >>> 6) | (e << 26)) ^ ((e >>> 11) | (e << 21)) ^ ((e >>> 25) | (e << 7));
      const ch = (e & f) ^ (~e & g);
      const temp1 = (h + S1 + ch + SHA256_K[i] + w[i]) >>> 0;
      const S0 = ((a >>> 2) | (a << 30)) ^ ((a >>> 13) | (a << 19)) ^ ((a >>> 22) | (a << 10));
      const maj = (a & b) ^ (a & c) ^ (b & c);
      const temp2 = (S0 + maj) >>> 0;
      h = g; g = f; f = e; e = (d + temp1) >>> 0;
      d = c; c = b; b = a; a = (temp1 + temp2) >>> 0;
    }
    h0 = (h0 + a) >>> 0; h1 = (h1 + b) >>> 0; h2 = (h2 + c) >>> 0; h3 = (h3 + d) >>> 0;
    h4 = (h4 + e) >>> 0; h5 = (h5 + f) >>> 0; h6 = (h6 + g) >>> 0; h7 = (h7 + h) >>> 0;
  }
  return [h0, h1, h2, h3, h4, h5, h6, h7]
    .map(word => word.toString(16).padStart(8, "0"))
    .join("");
}

function openSpokenIdb() {
  return new Promise((resolve, reject) => {
    if (!window.indexedDB) {
      resolve(null);
      return;
    }
    const request = window.indexedDB.open(SPOKEN_IDB_NAME, 1);
    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains(SPOKEN_IDB_STORE)) {
        const store = db.createObjectStore(SPOKEN_IDB_STORE, { keyPath: "id" });
        store.createIndex("sessionKey", "sessionKey", { unique: false });
      }
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

function saveSpokenWavToIdb(sessionKey, stimulusOrder, fileName, wavBytes, sha256) {
  openSpokenIdb()
    .then(db => {
      if (!db) return;
      const tx = db.transaction(SPOKEN_IDB_STORE, "readwrite");
      tx.objectStore(SPOKEN_IDB_STORE).put({
        id: `${sessionKey}:${stimulusOrder}`,
        sessionKey,
        stimulusOrder,
        fileName,
        wavBytes,
        sha256,
        savedAt: new Date().toISOString()
      });
    })
    .catch(() => {});
}

function loadSpokenWavsFromIdb(sessionKey) {
  return openSpokenIdb()
    .then(db => {
      if (!db) return [];
      return new Promise(resolve => {
        const tx = db.transaction(SPOKEN_IDB_STORE, "readonly");
        const index = tx.objectStore(SPOKEN_IDB_STORE).index("sessionKey");
        const req = index.getAll(sessionKey);
        req.onsuccess = () => {
          const items = Array.isArray(req.result) ? req.result : [];
          items.sort((a, b) => Number(a.stimulusOrder) - Number(b.stimulusOrder));
          resolve(items);
        };
        req.onerror = () => resolve([]);
      });
    })
    .catch(() => []);
}

function deleteSpokenWavsFromIdb(sessionKey) {
  openSpokenIdb()
    .then(db => {
      if (!db) return;
      const tx = db.transaction(SPOKEN_IDB_STORE, "readwrite");
      const store = tx.objectStore(SPOKEN_IDB_STORE);
      const req = store.index("sessionKey").getAllKeys(sessionKey);
      req.onsuccess = () => {
        for (const key of req.result || []) {
          store.delete(key);
        }
      };
    })
    .catch(() => {});
}
