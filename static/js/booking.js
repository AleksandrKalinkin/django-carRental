document.addEventListener('DOMContentLoaded', function() {
    // Установка минимальной даты (сегодня)
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('start_date').min = today;

    // Обновление минимальной даты окончания при выборе даты начала
    document.getElementById('start_date').addEventListener('change', function() {
        document.getElementById('end_date').min = this.value;
    });

    // Валидация возраста
    document.getElementById('age').addEventListener('change', function() {
        if (this.value < 21) {
            alert('Минимальный возраст для аренды - 21 год');
            this.value = 21;
        }
    });
});