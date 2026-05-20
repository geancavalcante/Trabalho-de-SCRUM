/**
 * Entry point do frontend Helpdesk Labs.
 * Carrega os modulos e inicializa quando o DOM esta pronto.
 */
import { initFlashMessages } from './flash-messages.js';
import { initConfirmActions } from './confirm-actions.js';

function boot() {
    initFlashMessages();
    initConfirmActions();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
} else {
    boot();
}