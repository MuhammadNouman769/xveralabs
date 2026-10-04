document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    var chipsWrap = document.getElementById('crChips');
    var jobsWrap = document.getElementById('crJobs');
    var countEl = document.getElementById('crCount');
    if (!chipsWrap || !jobsWrap) return;

    var chips = chipsWrap.querySelectorAll('.cr-chip');
    var jobs = jobsWrap.querySelectorAll('.cr-job');

    function applyFilter(filter) {
        var shown = 0;

        jobs.forEach(function (job) {
            var match = filter === 'all' || job.getAttribute('data-dept') === filter;
            job.hidden = !match;
            if (match) shown += 1;
        });

        chips.forEach(function (chip) {
            var active = chip.getAttribute('data-filter') === filter;
            chip.classList.toggle('is-active', active);
            chip.setAttribute('aria-pressed', active ? 'true' : 'false');
        });

        if (countEl) countEl.textContent = shown;
    }

    chipsWrap.addEventListener('click', function (e) {
        var chip = e.target.closest('.cr-chip');
        if (!chip) return;
        applyFilter(chip.getAttribute('data-filter'));
    });

    applyFilter('all');
});