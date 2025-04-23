// Search Event function
function searchEvents() {
    let searchQuery = document.getElementById('search-events').value.toLowerCase();
    let events = document.querySelectorAll('.event-card');

    events.forEach(event => {
        let eventName = event.querySelector('h3').textContent.toLowerCase();
        if (eventName.includes(searchQuery)) {
            event.style.display = 'block';
        } else {
            event.style.display = 'none';
        }
    });
}

// Filter Events by Category
function filterCategory() {
    let selectedCategory = document.getElementById('category-filter').value;
    let events = document.querySelectorAll('.event-card');

    events.forEach(event => {
        let eventCategory = event.getAttribute('data-category');
        if (selectedCategory === 'all' || eventCategory === selectedCategory) {
            event.style.display = 'block';
        } else {
            event.style.display = 'none';
        }
    });
}
