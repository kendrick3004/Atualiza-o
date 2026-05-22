/**
 * ARQUIVO: firebase-config.js
 * DESCRICAO: Configuracao Central do Firebase para a Suite
 * FUNCIONALIDADES: Inicializa Firebase Auth e Realtime Database com as chaves carregadas do servidor
 * VERSAO: 1.3.0 - Inicializacao sincronizada com Promise
 */

// Configuracao do Firebase sera carregada dinamicamente
let firebaseConfig = null;
let firebaseInitPromise = null;

// Carregamento dinamico do SDK do Firebase via CDN (Firebase v10+ Compat)
const FIREBASE_VERSION = "10.8.0";

async function loadFirebaseSDK() {
    const modules = [
        `https://www.gstatic.com/firebasejs/${FIREBASE_VERSION}/firebase-app-compat.js`,
        `https://www.gstatic.com/firebasejs/${FIREBASE_VERSION}/firebase-auth-compat.js`,
        `https://www.gstatic.com/firebasejs/${FIREBASE_VERSION}/firebase-database-compat.js`
    ];

    for (const src of modules) {
        await new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = src;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }
}

async function loadFirebase() {
    if (window.firebaseApp) return;

    // Aguardar o carregamento das chaves do servidor
    const apiKey = await ENV.getAsync('FIREBASE_API_KEY');
    const authDomain = await ENV.getAsync('FIREBASE_AUTH_DOMAIN');
    const projectId = await ENV.getAsync('FIREBASE_PROJECT_ID');
    const storageBucket = await ENV.getAsync('FIREBASE_STORAGE_BUCKET');
    const messagingSenderId = await ENV.getAsync('FIREBASE_MESSAGING_SENDER_ID');
    const appId = await ENV.getAsync('FIREBASE_APP_ID');
    const measurementId = await ENV.getAsync('FIREBASE_MEASUREMENT_ID');
    const databaseURL = await ENV.getAsync('FIREBASE_DATABASE_URL');

    // Validar se as chaves foram carregadas
    if (!apiKey || !projectId) {
        console.error('❌ Erro: Chaves do Firebase nao foram carregadas do servidor');
        throw new Error('Firebase configuration keys not loaded');
    }

    // Montar a configuracao com as chaves carregadas
    firebaseConfig = {
        apiKey: apiKey,
        authDomain: authDomain,
        projectId: projectId,
        storageBucket: storageBucket,
        messagingSenderId: messagingSenderId,
        appId: appId,
        measurementId: measurementId,
        databaseURL: databaseURL
    };

    // Carregar os SDKs do Firebase
    await loadFirebaseSDK();

    // Inicializa o Firebase com as chaves carregadas do servidor
    window.firebaseApp = firebase.initializeApp(firebaseConfig);
    window.firebaseAuth = firebase.auth();
    window.firebaseDb = firebase.database();
    
    console.log("🔥 Firebase inicializado com sucesso! (Chaves carregadas dinamicamente do servidor)");
    
    // Sinalizar que o Firebase esta pronto
    window.firebaseReady = true;
    
    // Disparar evento customizado para que outros scripts saibam que o Firebase esta pronto
    window.dispatchEvent(new CustomEvent('firebaseReady'));
}

// Criar uma Promise que sera resolvida quando o Firebase estiver pronto
firebaseInitPromise = loadFirebase().catch(err => {
    console.error("❌ Erro ao carregar Firebase:", err);
    window.firebaseReady = false;
});

// Funcao auxiliar para aguardar o Firebase estar pronto
window.waitForFirebase = async function() {
    if (window.firebaseReady) return;
    if (firebaseInitPromise) {
        await firebaseInitPromise;
    }
    // Aguardar ate que firebaseAuth esteja disponivel
    return new Promise((resolve) => {
        const checkInterval = setInterval(() => {
            if (window.firebaseAuth) {
                clearInterval(checkInterval);
                resolve();
            }
        }, 100);
        // Timeout de 10 segundos
        setTimeout(() => {
            clearInterval(checkInterval);
            resolve();
        }, 10000);
    });
};
