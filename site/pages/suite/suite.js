/**
 * ARQUIVO: suite.js
 * DESCRIÇÃO: Gerenciamento de temas, interações e persistência de estado offline.
 * FUNCIONALIDADES: Alternância de tema, Easter Egg e persistência de sessão para recarregamento offline.
 * VERSÃO: 2.3.1 - Acesso Público ao Calendário Corrigido
 */

const SuiteModule = (function() {
    'use strict';

    // Chave para persistência de estado na sessão atual
    const SESSION_KEY = 'suite_session_state';
    const THEME_KEY = 'suite_theme'; // Persistência entre páginas
    
    /**
     * Estado inicial da aplicação.
     * isDarkMode: Inicia em true (Dark Mode é o padrão a partir da v2.4.0)
     * darkModeToggleCount: Contador para Easter Egg (desativado)
     * isLoginRevealed: Controla se o botão de login foi revelado
     */
    let state = {
        darkModeToggleCount: 0,
        isDarkMode: true,  // Dark Mode é o padrão agora
        isLoginRevealed: false
    };

    /**
     * Salva o estado atual no SessionStorage.
     * O SessionStorage persiste ao recarregar a página, mas é limpo ao fechar a aba/navegador.
     */
    function saveState() {
        try {
            sessionStorage.setItem(SESSION_KEY, JSON.stringify(state));
        } catch (e) {
            console.error('[Suite] Erro ao salvar estado da sessão:', e);
        }
    }

    /**
     * Carrega o estado salvo do SessionStorage.
     */
    function loadState() {
        try {
            const saved = sessionStorage.getItem(SESSION_KEY);
            if (saved) {
                state = JSON.parse(saved);
                return true;
            }
        } catch (e) {
            console.error('[Suite] Erro ao carregar estado da sessão:', e);
        }
        return false;
    }

    /**
     * Carrega o tema salvo em localStorage para sincronizar entre páginas.
     * Se não houver tema salvo, define o Dark Mode como padrão (v2.4.0).
     */
    function loadThemeFromStorage() {
        try {
            const savedTheme = localStorage.getItem(THEME_KEY);
            if (savedTheme) {
                state.isDarkMode = savedTheme === 'dark';
            } else {
                // Se não houver tema salvo, o padrão é Dark Mode
                state.isDarkMode = true;
                localStorage.setItem(THEME_KEY, 'dark');
            }
            return true;
        } catch (e) {
            console.error('[Suite] Erro ao carregar tema do localStorage:', e);
        }
        return false;
    }

    /**
     * Inicializa o sistema de alternância de temas (Dark/Light).
     * Carrega o tema salvo do localStorage e aplica com transição suave.
     * Adiciona delay na mudança de tema para efeito visual melhorado.
     */
    function initThemeSwitch() {
        const switchBtn = document.querySelector('.switch');
        const toggle = document.querySelector('.switch-toggle');
        const body = document.body;

        if (!switchBtn || !toggle) return;

        // Carrega tema do localStorage (sincroniza entre páginas)
        loadThemeFromStorage();

        // Aplica o estado carregado ou o padrão (Dark Mode)
        if (state.isDarkMode) {
            body.classList.add('dark-mode');
            toggle.classList.add('switch-toggle-right');
        } else {
            body.classList.remove('dark-mode');
            toggle.classList.remove('switch-toggle-right');
        }

        // Se o login já estava revelado, reconstrói ele
        if (state.isLoginRevealed) {
            revealLoginButton(true); // true indica que é uma restauração silenciosa
        }

        switchBtn.addEventListener('click', () => {
            // Mudança de tema instantânea (sem delay)
            state.isDarkMode = body.classList.toggle('dark-mode');
            toggle.classList.toggle('switch-toggle-right');
            
            if (state.isDarkMode) {
                state.darkModeToggleCount++;
               checkEasterEgg();
            }
            
            saveState();
            // Salvar tema em localStorage para sincronizar entre páginas
            localStorage.setItem(THEME_KEY, state.isDarkMode ? 'dark' : 'light');
            console.log(`[Suite] Tema alterado para: ${state.isDarkMode ? 'Escuro' : 'Claro'}`);
        });
    }

    function checkEasterEgg() {
        // Easter Egg desativado temporariamente
    }

    /**
     * Revela o botão de login e atualiza o estado.
     */
    function revealLoginButton(isRestoring = false) {
        // Implementação removida conforme solicitado
    }

    /**
     * Verifica se o usuário está autenticado no Firebase.
     * Se não estiver, redireciona para o login com parâmetro de destino.
     */
    function checkAuthBeforeNavigation() {
        // Aguarda o Firebase carregar
        if (!window.firebaseAuth) {
            setTimeout(checkAuthBeforeNavigation, 100);
            return;
        }

        // Monitora o estado de autenticação
        window.firebaseAuth.onAuthStateChanged(user => {
            const now = Date.now();
            const authTimestamp = localStorage.getItem('auth_timestamp');
            const SESSION_DURATION = 7 * 24 * 60 * 60 * 1000; // 7 dias
            
            // Verifica se a sessão expirou
            if (user && authTimestamp && (now - parseInt(authTimestamp)) > SESSION_DURATION) {
                console.log("[Suite] Sessão expirada (7 dias).");
                window.firebaseAuth.signOut();
                localStorage.removeItem('auth_user');
                localStorage.removeItem('auth_timestamp');
            }
        });
    }

    /**
     * Intercepta cliques nos links de Calendário e Database.
     * Se o usuário não estiver autenticado, redireciona para login com destino.
     */
    function initAuthGates() {
        // Aguarda o Firebase carregar
        if (!window.firebaseAuth) {
            setTimeout(initAuthGates, 100);
            return;
        }

        // Encontra o link do Calendário - ACESSO PÚBLICO (v2.3.1)
        const calendarLink = document.querySelector('a[href="/calendar"]');
        if (calendarLink) {
            calendarLink.addEventListener('click', (e) => {
                // Não interceptar: o calendário agora é público
                console.log('[Suite] Navegando para o calendário (acesso público)');
            });
        }

        // Encontra o link do Database - REQUER LOGIN
        const databaseLink = document.querySelector('a[href="/database"]');
        if (databaseLink) {
            databaseLink.addEventListener('click', (e) => {
                e.preventDefault();
                window.firebaseAuth.onAuthStateChanged(user => {
                    if (!user) {
                        // Não autenticado: redireciona para login com destino
                        window.location.href = '/login?redirect=' + encodeURIComponent('/database');
                    } else {
                        // Autenticado: vai para o database
                        window.location.href = '/database';
                    }
                });
            });
        }
    }

    return {
        init: function() {
            loadState(); // Tenta recuperar o estado antes de iniciar
            initThemeSwitch();
            checkAuthBeforeNavigation(); // Verifica autenticação
            initAuthGates(); // Intercepta navegação para Calendar/Database
        }
    };
})();

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', SuiteModule.init);
} else {
    SuiteModule.init();
}
