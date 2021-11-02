const mainContent = document.getElementById("main-content");
const menuLogin = document.getElementById("menu-login");
const loginModal = document.getElementById("login-modal");
const container = document.getElementById("content-container");

// APT
const apiKey =
  "W7rRGCTEuCgKF9Ml%2FwKJbHCJf0duO218F3SYriSEGGFnjmztdsdfE9CmzyEcW8vma%2FwxwqteC1HIXU4bTgjjOg%3D%3D";
const apiUrl = `http://api.visitkorea.or.kr/openapi/service/rest/GoCamping/basedList?ServiceKey=${apiKey}&numOfRows=50&pageNo=4&MobileOS=ETC&MobileApp=TestApp&_type=json`;

const fetchData = async () => {
  const res = await fetch(apiUrl);
  const data = await res.json();

  const items = data.response.body.items.item;
  const filteredItems = items.filter((item) => item.firstImageUrl);

  filteredItems.map((item) => {
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
    mainContent.insertAdjacentHTML("beforeend", html);
  });

  console.log(items);
};

const loginShow = () => {
  loginModal.classList.remove("hidden");
};
const loginHidden = (e) => {
  if (e.target === loginModal) {
    loginModal.classList.add("hidden");
  }

  console.log(e.target);
};

menuLogin.addEventListener("click", loginShow);
loginModal.addEventListener("click", loginHidden);
window.addEventListener("load", fetchData);
