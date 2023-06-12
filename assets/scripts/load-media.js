const INTERSECTION_THRESHOLDS = [0.25];

window.addEventListener('DOMContentLoaded', () => {
  let figures = document.querySelectorAll('article figure');
  let umami = window.umami || null;

  figures.forEach((figure, index) => {
    let src = figure.dataset.src;
    let media = figure.querySelector('picture img, video');
    let parents = [media.parentElement, figure];

    // Set data attrs
    ['load', 'loadeddata'].map(event => media.addEventListener(event, () => {
      parents.map(el => el.dataset.loaded = 'true');
      media.playbackRate = parseFloat(media.dataset.playbackRate) || 1.0;
    }));
    parents.map(el => el.dataset.loaded = media.complete ? 'true' : 'false');

    // Observe figure visibility
    let observer = new IntersectionObserver(
      ([entry, ..._]) => onObserve(entry, observer),
      {threshold: INTERSECTION_THRESHOLDS}
    );
    observer.observe(figure);

    // Send tracker events
    if (umami) {
      media.onerror = () => umami.track('media-loading-failed', {src: src});
    }
  });
});

function onObserve(entry, observer) {
  if (!entry.isIntersecting)
    return;

  let element = entry.target;
  element.dataset.visible = 'true';

  let lazyVideo = element.querySelector('video[data-loading="lazy"]');
  if (lazyVideo) {
    [...lazyVideo.children].map(source => source.src = source.dataset.src);
    lazyVideo.load();
    lazyVideo.playbackRate = parseFloat(lazyVideo.dataset.playbackRate) || 1.0;
  }

  observer.unobserve(element);
}
