const toggleButton = document.getElementById('toggleMode');
const currentMode = localStorage.getItem('theme') || 'light';
document.body.dataset.theme = currentMode;
updateButtonLabel();

toggleButton.addEventListener('click', () => {
    const newMode = document.body.dataset.theme === 'dark' ? 'light' : 'dark';
    document.body.dataset.theme = newMode;
    localStorage.setItem('theme', newMode);
    updateButtonLabel();
});

function updateButtonLabel() {
    toggleButton.textContent = document.body.dataset.theme === 'dark' ? 'ライトモードに切り替え' : 'ダークモードに切り替え';
}
