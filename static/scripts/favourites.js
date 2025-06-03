document.addEventListener('DOMContentLoaded', () => {
  const favorites = JSON.parse(localStorage.getItem('favorites')) || [];
  const temkiContainer = document.querySelector('.temki');

  if (favorites.length === 0) {
    temkiContainer.innerHTML = '<p class="no-fav">Избранных чатов пока нет</p>';
    return;
  }

  function createCard(data) {
    const a = document.createElement('a');
    a.href = data.url;
    a.style.textDecoration = 'none';
    a.classList.add('ta' + data.id);

    const temaDiv = document.createElement('div');
    temaDiv.classList.add('tema' + data.id);
    temaDiv.setAttribute('data-category', data.category);
    temaDiv.setAttribute('data-id', data.id);
    temaDiv.setAttribute('data-title', data.title);
    temaDiv.setAttribute('data-img', data.img);

    temaDiv.innerHTML = `
      <div class="favor">
        <img src="${data.img}" alt="" class="t${data.id}">
        <button class="ficon">
          <img src="/static/img/Vector (5).png" alt="" class="favimg" style="width: 20px; height: 20px;">
        </button>
      </div>
      <p class="tt${data.id}">${data.title}</p>
      <p class="ttt${data.id}">${data.participants} участников<br>сообщества</p>
    `;

    a.appendChild(temaDiv);
    return a;
  }

  const cardsData = {
    "1": { id: "1", title: "Бег", img: "/static/img/image 3.png", category: "sports", participants: 25, url: "running.html" },
    "2": { id: "2", title: "Собаки", img: "/static/img/image 4.png", category: "animals", participants: 135, url: "dogs.html" },
    "3": { id: "3", title: "Кошки", img: "/static/img/image 5.png", category: "animals", participants: 775, url: "cats.html" },
    "4": { id: "4", title: "Футбол", img: "/static/img/image.png", category: "sports", participants: 2000, url: "soccer.html" },
    "5": { id: "5", title: "Велоспорт", img: "/static/img/image (1).png", category: "sports", participants: 1529, url: "cycling.html" },
    "6": { id: "6", title: "Кемпинг", img: "/static/img/image (2).png", category: "travel", participants: 245, url: "camping.html" },
    "7": { id: "7", title: "Хайкинг", img: "/static/img/hiking.jpg", category: "travel", participants: 91, url: "hiking.html" },
    "8": { id: "8", title: "Боевики", img: "/static/img/boevik.png", category: "movies", participants: 460, url: "boeviki.html" },
    "9": { id: "9", title: "Фантастика", img: "/static/img/scifi.png", category: "movies", participants: 513, url: "scifi.html" },
  };

  temkiContainer.innerHTML = '';

  favorites.forEach(id => {
    const data = cardsData[id];
    if (data) {
      const card = createCard(data);
      temkiContainer.appendChild(card);

      // ✅ Прямо здесь добавляем обработчик
      const favButton = card.querySelector('.ficon');
      favButton.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();

        let favs = JSON.parse(localStorage.getItem('favorites')) || [];
        favs = favs.filter(favId => favId !== id);
        localStorage.setItem('favorites', JSON.stringify(favs));

        card.remove();

        if (favs.length === 0) {
    temkiContainer.innerHTML = '<p class="no-fav">Избранных чатов пока нет</p>';
  }
      });
    }
  });
});




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