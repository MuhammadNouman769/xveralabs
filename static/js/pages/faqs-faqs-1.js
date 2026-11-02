// FAQ page: search, topic filter, one answer open at a time, and FAQ structured data for search engines
(function () {
  'use strict';
  var list = document.getElementById('fqList');
  if (!list) return;

  var items = [].slice.call(list.querySelectorAll('.fq-item'));
  var chips = [].slice.call(document.querySelectorAll('.fq-chip'));
  var input = document.getElementById('fqSearch');
  var count = document.getElementById('fqCount');
  var empty = document.getElementById('fqEmpty');
  var cat = 'all';

  function apply() {
    var q = (input.value || '').trim().toLowerCase(), shown = 0;
    items.forEach(function (it) {
      var okCat = cat === 'all' || it.getAttribute('data-cat') === cat;
      var okText = !q || it.textContent.toLowerCase().indexOf(q) !== -1;
      var show = okCat && okText;
      it.hidden = !show;
      if (!show) it.open = false;
      if (show) shown++;
    });
    count.textContent = shown === 1 ? '1 question' : shown + ' questions';
    empty.hidden = shown !== 0;
  }

  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      cat = c.getAttribute('data-cat');
      chips.forEach(function (o) { var on = o === c; o.classList.toggle('is-on', on); o.setAttribute('aria-pressed', on ? 'true' : 'false'); });
      apply();
    });
  });
  input.addEventListener('input', apply);

  items.forEach(function (it) {
    it.addEventListener('toggle', function () {
      if (!it.open) return;
      items.forEach(function (o) { if (o !== it) o.open = false; });
    });
  });

  // structured data built from the visible questions, so it always matches the page
  try {
    var data = {
      '@context': 'https://schema.org',
      '@type': 'FAQPage',
      mainEntity: items.map(function (it) {
        return {
          '@type': 'Question',
          name: it.querySelector('summary').textContent.trim(),
          acceptedAnswer: { '@type': 'Answer', text: it.querySelector('.fq-a').textContent.trim() }
        };
      })
    };
    var s = document.createElement('script');
    s.type = 'application/ld+json';
    s.textContent = JSON.stringify(data);
    document.head.appendChild(s);
  } catch (e) { /* ignore */ }

  apply();
})();