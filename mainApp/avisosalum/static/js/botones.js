document.addEventListener('DOMContentLoaded', function() {
  const tabs = Array.from(document.querySelectorAll('#myTab button'));
  const prevButton = document.getElementById('prevButton');
  const nextButton = document.getElementById('nextButton');

  function updateButtons() {
    const activeTab = document.querySelector('#myTab .active');
    const activeIndex = tabs.indexOf(activeTab);

    prevButton.style.display = activeIndex === 0 ? 'none' : 'inline-block';
    nextButton.style.display = activeIndex === tabs.length - 1 ? 'none' : 'inline-block';

    // Deshabilitar el botón "Anterior" en la primera sección
    prevButton.disabled = activeIndex === 0;
  }

  prevButton.addEventListener('click', function() {
    const activeTab = document.querySelector('#myTab .active');
    const activeIndex = tabs.indexOf(activeTab);
    if (activeIndex > 0) {
      tabs[activeIndex - 1].click();
    }
  });

  nextButton.addEventListener('click', function() {
    const activeTab = document.querySelector('#myTab .active');
    const activeIndex = tabs.indexOf(activeTab);
    if (activeIndex < tabs.length - 1) {
      tabs[activeIndex + 1].click();
    }
  });

  tabs.forEach(tab => {
    tab.addEventListener('click', updateButtons);
  });

  updateButtons();
});
