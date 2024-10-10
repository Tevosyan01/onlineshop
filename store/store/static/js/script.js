// Открытие и закрытие бокового меню
document.getElementById('menu-toggle').addEventListener('click', function() {
    document.getElementById('sidebar-menu').classList.toggle('open');
    document.body.classList.toggle('sidebar-open');
});

document.getElementById('close-btn').addEventListener('click', function() {
    document.getElementById('sidebar-menu').classList.remove('open');
    document.body.classList.remove('sidebar-open');
});
