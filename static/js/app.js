document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('q');
    if (searchInput) {
        searchInput.setAttribute('placeholder', 'Search tasks by title...');
    }
});