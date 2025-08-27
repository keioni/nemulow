// JavaScript
(function () {
    const icons = document.querySelectorAll('.theme-icon');
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    const STORAGE_KEY = 'theme-mode';

    function applyTheme(mode) {
        let theme = mode === 'system'
            ? (mq.matches ? 'dark' : 'light')
            : mode;
        document.documentElement.setAttribute('data-theme', theme);
        // アイコンの選択状態更新
        icons.forEach(i => {
            i.classList.toggle('selected', i.dataset.mode === mode);
        });
    }

    // クリックでモード切替
    icons.forEach(icon => {
        icon.addEventListener('click', () => {
            const mode = icon.dataset.mode;
            localStorage.setItem(STORAGE_KEY, mode);
            applyTheme(mode);
        });
    });

    // システム設定変化時
    mq.addEventListener('change', () => {
        const current = localStorage.getItem(STORAGE_KEY) || 'system';
        if (current === 'system') applyTheme('system');
    });

    // 初期化
    const saved = localStorage.getItem(STORAGE_KEY) || 'system';
    applyTheme(saved);
})();
