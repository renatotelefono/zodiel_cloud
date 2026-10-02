/* ==========================================================
   Zodiel – Google Analytics 4 + consenso cookie (GDPR)
   GA viene caricato SOLO dopo che il visitatore clicca "Accetta".
   ========================================================== */
(function () {
  var GA_ID = "G-B1SZLGV6DR";
  var CHIAVE = "zodiel_consenso_cookie"; // valori: "si" | "no"

  // --- gtag di base (gli eventi restano in coda finché GA non è caricato) ---
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };

  // Consent Mode v2: tutto negato di default
  gtag("consent", "default", {
    analytics_storage: "denied",
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied"
  });

  function leggiConsenso() {
    try { return localStorage.getItem(CHIAVE); } catch (e) { return null; }
  }
  function salvaConsenso(valore) {
    try { localStorage.setItem(CHIAVE, valore); } catch (e) {}
  }

  var gaCaricato = false;
  function caricaGA() {
    if (gaCaricato) return;
    gaCaricato = true;
    gtag("consent", "update", { analytics_storage: "granted" });
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    document.head.appendChild(s);
    gtag("js", new Date());
    gtag("config", GA_ID);
  }

  // --- Helper per gli eventi personalizzati: traccia("nome", {parametri}) ---
  window.traccia = function (nome, parametri) {
    if (leggiConsenso() !== "si") return;
    gtag("event", nome, parametri || {});
  };

  // --- Banner ---
  function mostraBanner() {
    if (document.getElementById("banner-cookie")) return;

    var stile = document.createElement("style");
    stile.textContent =
      "#banner-cookie{position:fixed;left:16px;right:16px;bottom:16px;z-index:9999;" +
      "max-width:720px;margin:0 auto;background:rgba(10,10,10,.96);color:#40E0D0;" +
      "border:1px solid #40E0D0;border-radius:15px;box-shadow:0 0 20px #40E0D0;" +
      "padding:18px 20px;font-family:'Playfair Display',serif;font-size:16px;line-height:1.5;text-align:left}" +
      "#banner-cookie a{color:#40E0D0;text-decoration:underline}" +
      "#banner-cookie .bc-pulsanti{display:flex;gap:12px;justify-content:flex-end;margin-top:12px;flex-wrap:wrap}" +
      "#banner-cookie button{margin:0;padding:8px 22px;border-radius:15px;font-weight:bold;font-size:15px;" +
      "cursor:pointer;border:1px solid #40E0D0;transform:none;box-shadow:none}" +
      "#banner-cookie .bc-accetta{background:#40E0D0;color:#000}" +
      "#banner-cookie .bc-rifiuta{background:transparent;color:#40E0D0}";
    document.head.appendChild(stile);

    var b = document.createElement("div");
    b.id = "banner-cookie";
    b.setAttribute("role", "dialog");
    b.setAttribute("aria-label", "Consenso cookie");
    b.innerHTML =
      "Usiamo Google Analytics per capire in forma aggregata come viene usato il sito. " +
      "Questi cookie si attivano solo se accetti. " +
      '<a href="privacy.html">Informativa privacy</a>' +
      '<div class="bc-pulsanti">' +
      '<button type="button" class="bc-rifiuta">Rifiuta</button>' +
      '<button type="button" class="bc-accetta">Accetta</button>' +
      "</div>";
    document.body.appendChild(b);

    b.querySelector(".bc-accetta").addEventListener("click", function () {
      salvaConsenso("si");
      b.remove();
      caricaGA();
    });
    b.querySelector(".bc-rifiuta").addEventListener("click", function () {
      salvaConsenso("no");
      b.remove();
      // rimuove eventuali cookie _ga rimasti da un consenso precedente
      document.cookie.split(";").forEach(function (c) {
        var n = c.split("=")[0].trim();
        if (n.indexOf("_ga") === 0) {
          document.cookie = n + "=; Max-Age=0; path=/";
          document.cookie = n + "=; Max-Age=0; path=/; domain=." + location.hostname.replace(/^www\./, "");
        }
      });
    });
  }

  // Permette di riaprire la scelta (link "Preferenze cookie" nella pagina privacy)
  window.apriPreferenzeCookie = function () {
    try { localStorage.removeItem(CHIAVE); } catch (e) {}
    mostraBanner();
  };

  // --- Avvio ---
  var scelta = leggiConsenso();
  if (scelta === "si") {
    caricaGA();
  } else if (scelta !== "no") {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", mostraBanner);
    } else {
      mostraBanner();
    }
  }
})();
