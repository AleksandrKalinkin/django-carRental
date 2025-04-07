document.addEventListener('DOMContentLoaded', function() {
  const themeToggle = document.querySelector('.theme-toggle');
  const body = document.body;

  // Проверяем сохраненную тему в localStorage
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    body.classList.add(savedTheme);
  }

  // Обработчик клика по кнопке
  themeToggle.addEventListener('click', function() {
    body.classList.toggle('dark-theme');

    // Сохраняем выбор темы
    const currentTheme = body.classList.contains('dark-theme') ? 'dark-theme' : '';
    localStorage.setItem('theme', currentTheme);
  });
});