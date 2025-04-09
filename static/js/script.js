// Ожидаем полной загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    // Получаем элементы
    const themeToggle = document.querySelector('.theme-toggle');
    const body = document.body;

    // Проверяем сохраненную тему в localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark-theme') {
        body.classList.add('dark-theme');  // Применяем темную тему, если была сохранена
    }

    // Обработчик клика по кнопке темы
    themeToggle.addEventListener('click', function() {
        if (body.classList.contains('dark-theme')) {
            // Переключаем на светлую тему
            body.classList.remove('dark-theme');
            localStorage.setItem('theme', 'light-theme');
        } else {
            // Переключаем на темную тему
            body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark-theme');
        }
    });
});