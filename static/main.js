const cardContainer = document.getElementById("card-container");

const apiKey =
  "W7rRGCTEuCgKF9Ml%2FwKJbHCJf0duO218F3SYriSEGGFnjmztdsdfE9CmzyEcW8vma%2FwxwqteC1HIXU4bTgjjOg%3D%3D";
const apiUrl = `http://api.visitkorea.or.kr/openapi/service/rest/GoCamping/basedList?ServiceKey=${apiKey}&numOfRows=100&pageNo=1&MobileOS=ETC&MobileApp=TestApp&_type=json`;

const cardHtml = `
<div class="card">
<div class="card__img">
  <img src="#" alt="#" />
</div>
<div class="card__description">
  <h3 class="description__name">name</h3>
  <p class="description__adr">address</p>
</div>
</div>
`;

const fetchData = async () => {
  const res = await fetch(apiUrl);
  const data = await res.json();

  const items = data.response.body.items.item;
  const filteredItems = items.filter((item) => item.firstImageUrl);

  const cardContent = filteredItems.map((item) => {
    const html = `
    <div class="card-container" id="card-container">
        <div class="card">
            <div class="card__img">
                <img src=${item.firstImageUrl} />
            </div>
            <div class="card__description">
                <h3 class="description__name">${item.facltNm}</h3>
                <p class="description__adr">${item.addr1}</p>
            </div>
        </div>
    </div>
          `;
    cardContainer.insertAdjacentHTML("beforeend", html);
  });

  console.log(cardContent);
};

window.addEventListener("load", fetchData);
