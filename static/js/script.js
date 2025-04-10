// Функция для переключения темы
const toggleTheme = () => {
  const body = document.body;
  if (body.classList.contains('dark-theme')) {
    body.classList.remove('dark-theme');
    localStorage.setItem('theme', 'light-theme');
  } else {
    body.classList.add('dark-theme');
    localStorage.setItem('theme', 'dark-theme');
  }
};

// Функции для модального окна помощи
const toggleHelpModal = () => {
  const helpModal = document.getElementById('helpModal');
  helpModal.style.display = helpModal.style.display === 'block' ? 'none' : 'block';
};

const closeHelpModal = () => {
  document.getElementById('helpModal').style.display = 'none';
};

// Закрытие при клике вне окна
document.addEventListener('click', (event) => {
  const helpModal = document.getElementById('helpModal');
  if (!event.target.closest('.help-modal-content') &&
      !event.target.closest('.help-button') &&
      helpModal.style.display === 'block') {
    helpModal.style.display = 'none';
  }
});

// Закрытие при нажатии Escape
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    document.getElementById('helpModal').style.display = 'none';
  }
});

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', () => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark-theme') {
    document.body.classList.add('dark-theme');
  }
  document.getElementById('helpModal').style.display = 'none';
});