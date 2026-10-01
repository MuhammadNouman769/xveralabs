document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      alert('✅ Thank you! A consultant will reach out within 24 hours.');
    });
  });
