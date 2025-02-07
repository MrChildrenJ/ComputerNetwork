let nav = document.querySelector("nav");

window.addEventListener("scroll", () => {
  if (window.scrollY > 0) {
    nav.classList.add("scrolled");
  } else {
    nav.classList.remove("scrolled");
  }
});

const navLinks = document.querySelectorAll("nav ul li a");

navLinks.forEach((link) => {
  link.style.transition = "all 1s ease";

  link.addEventListener("mouseenter", () => {
    link.style.color = "rgb(177, 78, 72)";
    link.style.fontSize = "32px";
  });

  link.addEventListener("mouseleave", () => {
    link.style.color = "darkolivegreen";
    link.style.fontSize = "16px";
  });
});

const allParas = document.querySelectorAll("p");
allParas.forEach((para) => {
  para.style.transition = "all 1s ease";

  para.addEventListener("click", () => {
    window.alert("Don't click!!!!");
  });
});

const bars = document.querySelectorAll(".about-me div .progress div");
bars.forEach((bar) => {
  bar.addEventListener("click", () => {
    bar.style.width = "100%";
  });
});
