/**
 * ARQUIVO: env-loader.js
 * DESCRIÇÃO: Carregador de variáveis de ambiente para o front-end.
 * SEGURANÇA: Centraliza as chaves que o front-end precisa para funcionar.
 */

const ENV = (function() {
    'use strict';

    // Estas chaves são carregadas aqui para que o resto do site as utilize.
    // Em um ambiente de produção real, estas chaves seriam injetadas pelo servidor
    // ou carregadas de um endpoint seguro.
    const config = {
        FIREBASE_API_KEY: "AIzaSyDYaFrq8MphGFmR-zU00bO9fKBEUIH4UYM",
        WEATHER_API_KEY: "55e2f6c107b54f808f6145707252712"
    };

    return {
        get: (key) => config[key] || null
    };
})();
