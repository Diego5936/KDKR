const tabContainers = document.querySelectorAll('.tab-content');
tabContainers.forEach(c => c.style.display = c.id === 'overview' ? 'block' : 'none');

const buttons = document.querySelectorAll('.rounded-btn');
buttons.forEach(btn => {
  btn.addEventListener('click', () => {
    const tab = btn.getAttribute('data-tab');

    tabContainers.forEach(c => {
      c.style.display = c.id === tab ? 'block' : 'none';
    });

    buttons.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});
