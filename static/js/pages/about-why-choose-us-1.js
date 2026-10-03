document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    // ===== CONSULTATION FORM =====
    // Chat ab sirf base.html wala robot hai, is page ka alag chat hata diya gaya hai.
    var form = document.getElementById('consultationForm');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        // TODO: yahan Django view / API pe fetch() se data bhejein
        alert("Consultation request submitted! We'll contact you within 24 hours.");
        form.reset();
    });
});