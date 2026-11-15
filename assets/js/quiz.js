(function () {
  const root = document.querySelector(".quiz");
  if (!root) return;
  const module = root.dataset.module;
  const total = Number(root.dataset.total);
  const bestKey = "pyl:" + module + ":quiz";
  const $ = (id) => document.getElementById(id);
  let answered = 0, correct = 0;

  const store = {
    get: (k) => { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} },
  };

  function showBest() {
    const b = store.get(bestKey);
    $("best").textContent = b === null ? "-" : b + "/" + total;
  }

  root.querySelectorAll(".q").forEach((q) => {
    q.querySelectorAll(".opt").forEach((btn) => {
      btn.addEventListener("click", () => {
        if (q.classList.contains("done")) return;
        q.classList.add("done");
        const right = q.dataset.answer;
        const picked = btn.dataset.letter;
        const ok = picked === right;
        q.querySelectorAll(".opt").forEach((o) => {
          o.disabled = true;
          if (o.dataset.letter === right) o.classList.add("right");
        });
        if (!ok) btn.classList.add("wrong");
        const fb = q.querySelector(".feedback");
        fb.hidden = false;
        fb.classList.add(ok ? "ok" : "bad");
        fb.querySelector(".verdict").textContent = ok
          ? "Correct."
          : "Not quite. The correct answer is " + right + ".";
        answered += 1;
        if (ok) correct += 1;
        $("answered").textContent = answered;
        $("correct").textContent = correct;
        if (answered === total) finish();
      });
    });
  });

  function finish() {
    const prev = store.get(bestKey);
    if (prev === null || correct > Number(prev)) store.set(bestKey, String(correct));
    showBest();
    const s = $("summary");
    s.hidden = false;
    s.textContent = "You scored " + correct + " out of " + total + ". " +
      (correct === total ? "Perfect. Move on to the assignments."
        : "Review the explanations above, re-read the Learn page, then press Reset and try again.");
  }

  $("reset").addEventListener("click", () => {
    answered = 0; correct = 0;
    $("answered").textContent = "0"; $("correct").textContent = "0";
    $("summary").hidden = true;
    root.querySelectorAll(".q").forEach((q) => {
      q.classList.remove("done");
      q.querySelectorAll(".opt").forEach((o) => {
        o.disabled = false; o.classList.remove("right", "wrong");
      });
      const fb = q.querySelector(".feedback");
      fb.hidden = true; fb.classList.remove("ok", "bad");
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  showBest();
})();
