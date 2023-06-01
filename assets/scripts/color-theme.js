const STORAGE_KEY = 'colorTheme';
const DARKMODE = '(prefers-color-scheme: dark)';

window.addEventListener('DOMContentLoaded', initColorTheme);
window.matchMedia(DARKMODE).addEventListener('change', ({matches}) => {
  let savedThemeValue = _getSavedColorThemeValue();
  if (savedThemeValue !== 'default')
    return;
  setColorTheme(matches ? 'dark' : 'light');
});

function initColorTheme() {
  let themeSwitchBtn = document.querySelector('[data-color-theme-btn]');
  let themeSwitchDropdown = document.querySelector('[data-color-theme-dropdown]');

  // Set OS-inherited theme if no switch presented
  if (!themeSwitchBtn || !themeSwitchDropdown) {
    setColorTheme(window.matchMedia(DARKMODE).matches ? 'dark' : 'light');
    return;
  }

  let themes = themeSwitchDropdown.querySelectorAll('[name="color_theme"]');
  let savedThemeValue = _getSavedColorThemeValue();

  setColorTheme(savedThemeValue);
  themeSwitchBtn.onclick = () => {
    themeSwitchDropdown.hidden = !themeSwitchDropdown.hidden;
    themeSwitchBtn.dataset.active = themeSwitchDropdown.hidden ? 'false' : 'true';
  };
  themes.forEach(theme => {
    theme.checked = theme.value === savedThemeValue;
    theme.onchange = () => setColorTheme(theme.value) && _saveColorThemeValue(theme.value);
  });
}

function setColorTheme(theme) {
  if (theme === 'default' && window.matchMedia(DARKMODE).matches)
    theme = 'dark';
  document.documentElement.dataset.colorTheme = theme;
}

function _getSavedColorThemeValue() {
  let value;
  try {
    value = localStorage.getItem(STORAGE_KEY);
  } catch (e) {
    value = null;
  }
  return value || 'default';
}

function _saveColorThemeValue(value) {
  try {
    localStorage.setItem(STORAGE_KEY, value);
  } catch (_) {
    console.warn('Color theme not set');
  }
}
