/**
 * ARQUIVO: login-firebase.js
 * DESCRICAO: Logica de autenticacao usando Firebase Auth
 * VERSAO: 1.1.0 - Aguarda Firebase estar pronto
 */

window.addEventListener('DOMContentLoaded', async () => {
    // Aguardar o Firebase estar pronto
    await window.waitForFirebase();
    
    const errorDiv = document.getElementById("loginError");
    const form = document.getElementById("loginForm");
    const button = document.getElementById("loginSubmitBtn");

    form.addEventListener("submit", async function(e) {
        e.preventDefault();
        const email = document.getElementById("username").value.trim();
        const pass = document.getElementById("password").value;

        if (!email || !pass) {
            errorDiv.textContent = "Preencha email e senha.";
            errorDiv.style.color = "var(--error-color)";
            return;
        }

        // Garante que o Firebase está carregado
        if (!window.firebaseAuth) {
            errorDiv.textContent = "Erro: Firebase não carregado.";
            return;
        }

        button.disabled = true;
        button.textContent = "Entrando...";
        errorDiv.textContent = "Validando credenciais...";
        errorDiv.style.color = "var(--text-secondary)";

        try {
            // Autenticacao com Firebase
            const userCredential = await window.firebaseAuth.signInWithEmailAndPassword(email, pass);
            const user = userCredential.user;

            // Sincronizar Token imediatamente
            const token = await user.getIdToken();
            const maxAge = 7 * 24 * 60 * 60;
            document.cookie = `firebase_auth_token=${token}; path=/; max-age=${maxAge}; SameSite=Lax`;

            errorDiv.textContent = "Login realizado! Sincronizando dados...";
            errorDiv.style.color = "#4caf50";
            
            // Redirecionamento para o calendario de oracoes
            const urlParams = new URLSearchParams(window.location.search);
            const redirectUrl = urlParams.get('redirect');
            setTimeout(() => {
                // Padrao: redireciona para o calendario (sem .html)
                window.location.href = redirectUrl ? decodeURIComponent(redirectUrl) : "/calendar";
            }, 1000);

        } catch (error) {
            console.error('[Firebase Login] Erro:', error);
            button.disabled = false;
            button.textContent = "Entrar";
            errorDiv.style.color = "var(--error-color)";
            
            switch (error.code) {
                case 'auth/user-not-found':
                case 'auth/wrong-password':
                case 'auth/invalid-credential':
                    errorDiv.textContent = "Email ou senha incorretos.";
                    break;
                case 'auth/too-many-requests':
                    errorDiv.textContent = "Muitas tentativas. Tente mais tarde.";
                    break;
                default:
                    errorDiv.textContent = "Erro ao fazer login. Verifique sua conexao.";
            }
        }
    });
});
