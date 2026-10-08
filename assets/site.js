const toggle = document.querySelector('.theme-toggle');
if (toggle) {
  toggle.hidden = false;
  const renderTheme = () => {
    const dark = document.documentElement.dataset.theme === 'dark';
    toggle.textContent = dark ? '☀' : '☾';
    toggle.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
  };
  renderTheme();
  toggle.addEventListener('click', () => {
    const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem('garren-theme', theme); } catch {}
    renderTheme();
  });
}
