// Careers pages: filters on the list, and the application form helpers. Every block is guarded.
(function () {
  'use strict';

  // ----- list: type chips + department + search (also reads ?type=internship) -----
  var jobsBox = document.getElementById('crJobs');
  if (jobsBox) {
    var jobs = [].slice.call(jobsBox.querySelectorAll('.cr-job'));
    var chips = [].slice.call(document.querySelectorAll('#crTypes .cr-chip'));
    var dept = document.getElementById('crDept'), search = document.getElementById('crSearch');
    var count = document.getElementById('crCount'), empty = document.getElementById('crEmpty');
    var type = 'all';

    function apply() {
      var q = (search.value || '').trim().toLowerCase(), d = dept.value, shown = 0;
      jobs.forEach(function (j) {
        var ok = (type === 'all' || j.getAttribute('data-type') === type) &&
                 (d === 'all' || j.getAttribute('data-dept') === d) &&
                 (!q || j.getAttribute('data-text').indexOf(q) !== -1);
        j.hidden = !ok; if (ok) shown++;
      });
      count.textContent = shown + (shown === 1 ? ' role' : ' roles');
      empty.hidden = shown !== 0;
    }
    function setType(t) {
      type = t;
      chips.forEach(function (c) { var on = c.getAttribute('data-type') === t; c.classList.toggle('is-on', on); c.setAttribute('aria-pressed', on ? 'true' : 'false'); });
      apply();
    }
    chips.forEach(function (c) { c.addEventListener('click', function () { setType(c.getAttribute('data-type')); }); });
    dept.addEventListener('change', apply);
    search.addEventListener('input', apply);

    [].slice.call(document.querySelectorAll('[data-filter-type]')).forEach(function (b) {
      b.addEventListener('click', function () {
        setType(b.getAttribute('data-filter-type'));
        document.getElementById('positions').scrollIntoView({ behavior: 'smooth' });
      });
    });

    try {
      var wanted = new URLSearchParams(window.location.search).get('type');
      if (wanted && chips.some(function (c) { return c.getAttribute('data-type') === wanted; })) setType(wanted); else apply();
    } catch (e) { apply(); }
  }

  // ----- application form -----
  var form = document.getElementById('crForm');
  if (!form) return;
  var MAX = 5 * 1024 * 1024;
  var file = form.querySelector('input[type="file"]'), name = document.getElementById('crFileName');
  var note = form.querySelector('textarea'), cnt = document.getElementById('crCount2');
  var hint = name ? name.textContent : '';

  if (file && name) {
    file.addEventListener('change', function () {
      var f = file.files && file.files[0], box = file.closest('.cr-file');
      if (!f) { name.textContent = hint; box.classList.remove('has-file'); return; }
      if (f.size > MAX) { file.value = ''; name.textContent = 'File is too large (max 5 MB)'; box.classList.remove('has-file'); return; }
      name.textContent = f.name; box.classList.add('has-file');
    });
  }
  function updateCount() { if (note && cnt) cnt.textContent = note.value.length + ' / ' + (note.getAttribute('maxlength') || 1500); }
  if (note) { note.addEventListener('input', updateCount); updateCount(); }

  form.addEventListener('submit', function (e) {
    if (!form.checkValidity()) { e.preventDefault(); form.reportValidity(); return; }
    var btn = form.querySelector('.cr-submit');
    if (btn) { btn.disabled = true; btn.textContent = 'Sending...'; }   // stop double submits
  });
})();