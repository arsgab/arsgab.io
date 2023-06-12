window.addEventListener('DOMContentLoaded', () => {
	let toc = document.querySelector('[data-article-toc]');
	if (!toc) return;
	let observer = new IntersectionObserver(
		([entry, ..._]) => {
			entry.target.dataset.visible = entry.isIntersecting + '';
		},
		{threshold: [.95]}
	);
	observer.observe(toc);
});

window.addEventListener('DOMContentLoaded', () => {
	let umami = window.umami || null;
	let article = document.querySelector('article');
	if (!article || !umami) return;

	let articleID = article.dataset.slug || location.pathname;
	let footer = article.querySelector('article footer');
	if (!footer) return;

	let observer = new IntersectionObserver(
		([entry, ..._]) => {
			if (!entry.isIntersecting)
				return;
			umami.track('article-bottom-viewed', {article: articleID});
		},
		{threshold: [.1]}
	);
	observer.observe(footer);
});
