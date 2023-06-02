const INTERSECTION_THRESHOLDS = [0.25];

window.addEventListener('load', () => {
  let figures = document.querySelectorAll('article figure');
  let figuresLastIndex = figures.length - 1;
  let umami = window.umami || null;

  figures.forEach((figure, index) => {
    let src = figure.dataset.src;
    let isLastFigure = index === figuresLastIndex;
    let img = figure.querySelector('picture img');
    let parents = [img.parentElement, figure];

    // Set data attrs
    img.onload = () => parents.map(el => el.dataset.loaded = 'true');
    parents.map(el => el.dataset.loaded = img.complete + '');

    // Observe picture visibility
    let observer = new IntersectionObserver(([element, ..._]) => {
      if (!element.isIntersecting) return;
      figure.dataset.visible = 'true';
      observer.unobserve(figure);
      if (isLastFigure && umami) umami.track('page-bottom-viewed', {path: window.location.pathname});
    }, {threshold: INTERSECTION_THRESHOLDS});
    observer.observe(figure);

    // Send tracker events
    if (umami) {
      img.onerror = () => umami.track('image-loading-failed', {src: src});
    }
  });
});
