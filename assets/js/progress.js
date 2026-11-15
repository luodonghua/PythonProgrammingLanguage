// Progress is stored in localStorage under "pyl:<module>:<part>".
(function () {
  const get = (k) => { try { return localStorage.getItem(k); } catch (e) { return null; } };
  const set = (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} };
  const del = (k) => { try { localStorage.removeItem(k); } catch (e) {} };

  // Checkboxes on topic pages: <input type="checkbox" data-progress="module:part">
  document.querySelectorAll("input[data-progress]").forEach((box) => {
    const key = "pyl:" + box.dataset.progress;
    box.checked = get(key) === "1";
    box.addEventListener("change", () => (box.checked ? set(key, "1") : del(key)));
  });

  // Roadmap badges: <span data-badge="module">
  document.querySelectorAll("[data-badge]").forEach((el) => {
    const m = el.dataset.badge;
    const parts = [];
    if (get("pyl:" + m + ":learn") === "1") parts.push("read");
    const best = get("pyl:" + m + ":quiz");
    if (best !== null) parts.push("quiz " + best + "/10");
    if (get("pyl:" + m + ":assignments") === "1") parts.push("assignments done");
    el.textContent = parts.join(" · ");
  });
})();
