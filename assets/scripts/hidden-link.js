const SELECTOR = 'data-hidden-href';

window.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll(`a[${SELECTOR}]`).forEach(link => {
    let encodedHref = link.dataset.hiddenHref;
    if (!encodedHref)
      return false;
    try {
      link.href = atob(encodedHref);
    } catch (_) {
      return false;
    }
    link.removeAttribute(SELECTOR);
  });
});
