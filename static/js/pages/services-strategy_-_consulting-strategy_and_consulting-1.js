document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    // Sirf is page ka consultation form.
    // Pehle document.querySelectorAll('form') tha, jis se base.html ke chat form pe bhi
    // ye handler lag jata tha aur do dafa alert aata tha.
    var form = document.getElementById('consultationForm');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        // TODO: yahan Django view / API pe fetch() se data bhejein
        // var data = new FormData(form);

        alert('Thank you! A consultant will reach out within 24 hours.');
        form.reset();
    });
});