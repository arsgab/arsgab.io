window.addEventListener('DOMContentLoaded', initArticleTOC);
window.addEventListener('DOMContentLoaded', trackArticleBottomViewEvent);

function initArticleTOC() {
	let root = document.querySelector('article [data-prop="content"]');
	if (!root) return;
	let TOCHeadings = root.querySelectorAll('h2[id]');
	let TOC = root.querySelector('[data-article-toc]');
	if (!TOCHeadings || !TOC) return;

	let TOCObserver = new IntersectionObserver(
		([entry, ..._]) => {
			entry.target.dataset.visible = entry.isIntersecting + '';
		},
		{threshold: [.95]}
	);
	TOCObserver.observe(TOC);
}

function trackArticleBottomViewEvent() {
	let umami = window.umami || null;
	let article = document.querySelector('article');
	if (!article || !umami) return;

	let articleID = article.dataset.slug || location.pathname;
	let footer = article.querySelector('footer');
	if (!footer) return;

	let observer = new IntersectionObserver(
		([entry, ..._]) => {
			if (!entry.isIntersecting)
				return;
			umami.track('article-bottom-viewed', {article: articleID});
			observer.unobserve(entry.target);
		},
		{threshold: [.1]}
	);
	observer.observe(footer);
}
