document.addEventListener('DOMContentLoaded', () => {
  const filterButtons = document.querySelectorAll('.filter button');
  const topicCards = document.querySelectorAll('.temki > a');

  filterButtons.forEach(button => {
    button.addEventListener('click', () => {
      const filter = button.getAttribute('data-filter');

      topicCards.forEach(card => {
        const tema = card.querySelector('div[data-category]');
        const category = tema ? tema.getAttribute('data-category') : null;

        if (filter === 'all' || category === filter) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });

      filterButtons.forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');
    });
  });
});




document.addEventListener('DOMContentLoaded', () => {
  const favoriteButtons = document.querySelectorAll('.ficon');

  // Загрузка избранных из localStorage
  let favorites = JSON.parse(localStorage.getItem('favorites')) || [];

  // Обновляем кнопки на странице по сохранённым избранным
  favoriteButtons.forEach(button => {
    const card = button.closest('div[data-id]');
    const id = card ? card.getAttribute('data-id') : null;
    if (id && favorites.includes(id)) {
      button.classList.add('active'); // например, добавляем класс active для подсветки
    }

    button.addEventListener('click', (e) => {
      e.preventDefault(); // чтобы не срабатывал переход по ссылке

      if (!id) return;

      if (favorites.includes(id)) {
        // Убрать из избранных
        favorites = favorites.filter(favId => favId !== id);
        button.classList.remove('active');
      } else {
        // Добавить в избранные
        favorites.push(id);
        button.classList.add('active');
      }

      // Сохраняем обновлённый список в localStorage
      localStorage.setItem('favorites', JSON.stringify(favorites));
    });
  });
});