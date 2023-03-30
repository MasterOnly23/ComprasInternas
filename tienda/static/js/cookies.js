// Mostrar el popup si no se ha aceptado o rechazado el uso de cookies
if (!localStorage.getItem('cookie-consent')) {
  document.getElementById('cookie-popup').style.display = 'block';
}else {
  document.getElementById('cookie-popup').style.display = 'none';
}

document.getElementById('accept-cookie').addEventListener('click', function() {
  localStorage.setItem('cookie-consent', 'accepted');
  document.getElementById('cookie-popup').style.display = 'none';
});

  