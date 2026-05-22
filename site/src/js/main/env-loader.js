/**
 * ARQUIVO: env-loader.js
 * DESCRICAO: Carregador de variaveis de ambiente para o front-end.
 * SEGURANCA: Carrega chaves seguras do endpoint /api/config do servidor.
 */

const ENV = (function() {
    'use strict';

    let config = {};
    let isLoaded = false;
    let loadPromise = null;
    let errorCount = 0;

    // Funcao para carregar as chaves do servidor
    async function loadConfig() {
        if (isLoaded) return config;
        if (loadPromise) return loadPromise;

        loadPromise = (async () => {
            try {
                // Timeout de 5 segundos para a requisição
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 5000);

                const response = await fetch('/api/config', { signal: controller.signal });
                clearTimeout(timeoutId);

                if (!response.ok) throw new Error(`Erro HTTP: ${response.status}`);
                
                const data = await response.json();
                config = data;
                isLoaded = true;
                console.log('✅ Configuracao do frontend carregada com sucesso do servidor');
                return config;
            } catch (error) {
                errorCount++;
                console.error('❌ Erro ao carregar configuracao do servidor:', error);
                
                // Se falhar, marcamos como carregado (vazio) para nao travar o resto do site
                isLoaded = true;
                config = {};
                
                // Disparar evento de erro para que a UI possa reagir
                window.dispatchEvent(new CustomEvent('configLoadError', { detail: error.message }));
                
                return config;
            }
        })();

        return loadPromise;
    }

    // Iniciar carregamento imediatamente
    loadConfig();

    return {
        get: (key) => config[key] || null,
        getAsync: async (key) => {
            await loadConfig();
            return config[key] || null;
        },
        isReady: () => isLoaded,
        hasError: () => errorCount > 0
    };
})();
