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

        // O calendário não requer autenticação - permitir acesso livre
        if (window.location.pathname.includes('/calendar')) {
            console.log('[auth-gate] Calendário acessado - sem requerer autenticação');
            return;
        }

        window.firebaseAuth.onAuthStateChanged(async user => {
            const now = Date.now();
            const authTimestamp = localStorage.getItem('auth_timestamp');
            
            // Verifica se o usuário está logado no Firebase
            if (!user) {
                // Limpar cookie se não houver usuário
                document.cookie = "firebase_auth_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
                redirectToLogin();
                return;
            }

            // Sincronizar Token com o Backend (Cookie)
            // Isso permite que rotas protegidas pelo Flask (como upload/zip) funcionem
            try {
                const token = await user.getIdToken();
                // Definir cookie com validade de 7 dias para o backend
                const maxAge = 7 * 24 * 60 * 60;
                document.cookie = `firebase_auth_token=${token}; path=/; max-age=${maxAge}; SameSite=Lax`;
            } catch (e) {
                console.error("[auth-gate] Erro ao sincronizar token:", e);
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
        
        // Evita loop se já estiver na página de login, na Suite ou no Calendário (que gerencia sua própria autenticação)
        // O calendário permite acesso sem login - o usuário pode clicar em "Conectar" se desejar
        if (!window.location.pathname.includes('/login') && 
            !window.location.pathname.includes('/calendar') && 
            window.location.pathname !== '/') {
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
