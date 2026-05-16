/**
 * ARQUIVO: auth-gate.js
 * DESCRIÇÃO: Proteção de rotas e gerenciamento de sessão (7 dias)
 */

(function() {
    const SESSION_DURATION = 7 * 24 * 60 * 60 * 1000; // 7 dias em ms

    function checkAuth() {
        // Aguarda o Firebase carregar se necessário
        if (!window.firebaseAuth) {
            setTimeout(checkAuth, 100);
            return;
        }

        window.firebaseAuth.onAuthStateChanged(user => {
            const now = Date.now();
            const authTimestamp = localStorage.getItem('auth_timestamp');
            
            // Verifica se o usuário está logado no Firebase
            if (!user) {
                redirectToLogin();
                return;
            }

            // Verifica a expiração de 7 dias
            if (authTimestamp && (now - parseInt(authTimestamp)) > SESSION_DURATION) {
                console.log("Sessão expirada (7 dias).");
                logout();
                return;
            }

            // Se estiver logado e dentro do prazo, atualiza o timestamp para manter ativo
            // (Opcional: o usuário pediu "após 7 dias expira automaticamente", 
            // se for 7 dias desde o ÚLTIMO login, atualizamos aqui. 
            // Se for 7 dias fixos, não atualizamos.)
            // Vamos manter fixo conforme o pedido para ser rigoroso, ou atualizar se houver atividade.
            // Por segurança, vamos apenas validar.
        });
    }

    function logout() {
        if (window.firebaseAuth) {
            window.firebaseAuth.signOut().then(() => {
                localStorage.removeItem('auth_user');
                localStorage.removeItem('auth_timestamp');
                redirectToLogin();
            });
        }
    }

    function redirectToLogin() {
        const currentPath = window.location.pathname + window.location.search;
        const loginUrl = "/login?redirect=" + encodeURIComponent(currentPath);
        
        // Evita loop se já estiver na página de login ou na Suite (que gerencia sua própria autenticação)
        if (!window.location.pathname.includes('/login') && window.location.pathname !== '/') {
            window.location.href = loginUrl;
        }
    }

    // Inicia a verificação
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', checkAuth);
    } else {
        checkAuth();
    }
})();
