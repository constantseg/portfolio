// Thème : suit le système tant que le visiteur n'a rien choisi ;
// le bouton impose un choix, mémorisé et partagé entre les onglets.
(function () {
  var KEY = "cs-theme";
  var root = document.documentElement;
  var btn = document.querySelector(".theme-toggle");
  var media = window.matchMedia("(prefers-color-scheme: dark)");

  function stored() {
    try { var t = localStorage.getItem(KEY); return t === "light" || t === "dark" ? t : null; }
    catch (e) { return null; }
  }

  function apply(theme) {
    root.dataset.theme = theme;
    if (!btn) return;
    var next = theme === "dark" ? "clair" : "sombre";
    btn.textContent = next;
    btn.setAttribute("aria-label", "Passer en thème " + next);
  }

  apply(stored() || (media.matches ? "dark" : "light"));

  if (btn) {
    btn.addEventListener("click", function () {
      var next = root.dataset.theme === "dark" ? "light" : "dark";
      try { localStorage.setItem(KEY, next); } catch (e) {}
      apply(next);
    });
  }

  // Changement du réglage système, tant qu'aucun choix n'est mémorisé.
  media.addEventListener("change", function (e) {
    if (!stored()) apply(e.matches ? "dark" : "light");
  });

  // Choix fait dans un autre onglet.
  window.addEventListener("storage", function (e) {
    if (e.key === KEY) apply(stored() || (media.matches ? "dark" : "light"));
  });
})();
