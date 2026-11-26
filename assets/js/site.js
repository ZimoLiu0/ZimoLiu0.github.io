const menu = document.querySelector(".menu-toggle");
const nav = document.querySelector("#site-nav");
const compact = window.matchMedia("(max-width: 690px)");

function syncMenu() {
  menu.hidden = !compact.matches;
  nav.hidden = compact.matches;
  menu.setAttribute("aria-expanded", "false");
}

menu.addEventListener("click", () => {
  nav.hidden = !nav.hidden;
  menu.setAttribute("aria-expanded", String(!nav.hidden));
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && compact.matches && !nav.hidden) {
    nav.hidden = true;
    menu.setAttribute("aria-expanded", "false");
    menu.focus();
  }
});

compact.addEventListener("change", syncMenu);
syncMenu();
