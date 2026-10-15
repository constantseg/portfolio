// Filtre de la page Documentation par catégorie.
(function () {
  var buttons = document.querySelectorAll(".filter");
  var items = document.querySelectorAll(".docs > li");

  buttons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var cat = btn.dataset.cat;
      buttons.forEach(function (b) { b.setAttribute("aria-pressed", b === btn ? "true" : "false"); });
      items.forEach(function (li) { li.hidden = cat !== "all" && li.dataset.cat !== cat; });
    });
  });
})();
