document.querySelectorAll('.size-option').forEach(function(button) {
    button.addEventListener('click', function() {
        // Убираем активный класс с других кнопок
        document.querySelectorAll('.size-option').forEach(function(btn) {
            btn.classList.remove('active');
        });

        // Добавляем активный класс к нажатой кнопке
        this.classList.add('active');

        // Можно добавить логику обработки выбранного размера здесь
        console.log("Selected size:", this.getAttribute('data-size'));
    });
});