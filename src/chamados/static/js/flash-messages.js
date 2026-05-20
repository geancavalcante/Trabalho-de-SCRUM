/**
 * Auto-fecha mensagens flash apos 5s, com fade.
 */
export function initFlashMessages(rootSelector = '.messages') {
    const root = document.querySelector(rootSelector);
    if (!root) return;

    const items = root.querySelectorAll('li');
    items.forEach((item) => {
        setTimeout(() => {
            item.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            item.style.opacity = '0';
            item.style.transform = 'translateY(-6px)';
            setTimeout(() => item.remove(), 450);
        }, 5000);
    });
}