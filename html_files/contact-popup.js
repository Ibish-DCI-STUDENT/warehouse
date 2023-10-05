// Open the contact us popup
document.getElementById('contact-link').addEventListener('click', function() {
    document.querySelector('.contact-popup').style.display = 'block';
  });
  
  // Close the contact us popup
  document.querySelector('.contact-popup-close').addEventListener('click', function() {
    document.querySelector('.contact-popup').style.display = 'none';
  });
  