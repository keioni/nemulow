// scroll-to-top.js

document.addEventListener('DOMContentLoaded', function () {
    const scrollToTopBtn = document.getElementById('scroll-to-top');

    // ダークモードかどうかを判定して画像を切り替え
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    scrollToTopBtn.src = isDark ? './image/icon/up-arrow-dark.svg' : './image/icon/up-arrow-light.svg';

    // スクロール位置によって表示/非表示を切り替え
    window.addEventListener('scroll', () => {
        scrollToTopBtn.style.display = window.scrollY > 100 ? 'block' : 'none';
    });

    // クリックで先頭へスムーズにスクロール
    scrollToTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});
