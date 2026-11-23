// Suraag evidence board: a Streamlit custom component with no build step.
// Python passes the three exhibits; a click on a row toggles it as a citation for the active question
// and the new citation map goes back to Python, which does the grading. After grading, Python passes
// `marks` and this draws the strings: solid green where a citation holds, dashed where it does not.
(function () {
  const send = (value) => window.parent.postMessage({ isStreamlitMessage: true, type: "streamlit:setComponentValue", value, dataType: "json" }, "*");
  const frame = (h) => window.parent.postMessage({ isStreamlitMessage: true, type: "streamlit:setFrameHeight", height: h }, "*");
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  let args = null, cites = {};

  function highlight(text, needles) {
    let out = esc(text);
    (needles || []).forEach((n) => {
      if (!n) return;
      const e = esc(n).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      out = out.replace(new RegExp(e, "gi"), (m) => `<mark>${m}</mark>`);
    });
    return out;
  }

  function rowHtml(key, num, text, st) {
    const active = (cites[args.active.id] || []).includes(key);
    const m = (args.marks || []).find((x) => x.key === key && x.qid === args.active.id);
    const cls = ["row"];
    if (m) cls.push(m.label === "valid" ? "holds" : m.label === "partial" ? "partial" : "snapped");
    else if (active) cls.push("cited");
    const word = m ? (m.label === "valid" ? args.labels.holds : m.label === "partial" ? args.labels.partial : args.labels.snapped) : "";
    const needles = m && m.label === "valid" ? (args.needles[key] || []) : [];
    return `<div class="${cls.join(" ")}" data-key="${esc(key)}" id="r-${esc(key.replace(/[^\w]/g, "_"))}">` +
           `<span class="n">${esc(num)}</span><span class="t" title="${esc(text)}">${highlight(text, needles)}</span>` +
           (word ? `<span class="mark">${esc(word)}</span>` : "") + `</div>`;
  }

  function render() {
    const a = args, L = a.labels;
    const chat = a.chat.map((r) => r.n === 1
      ? `<div class="row head"><span class="n">1</span><span class="t">${esc(r.text)}</span></div>`
      : rowHtml(`chat:${r.n}`, r.n, r.text)).join("");
    const calls = a.calls.map((r) => rowHtml(`calls:${r.row}`, r.row, r.text)).join("");
    const exif = a.exif.map((r) => rowHtml(`photo:${r.tag}`, "", `${r.tag}: ${r.value}`)).join("");
    const trayItems = (cites[a.active.id] || []).map((k) => {
      const m = (a.marks || []).find((x) => x.key === k && x.qid === a.active.id);
      const cls = m ? (m.label === "valid" ? "holds" : "snapped") : "";
      const pretty = k.replace("chat:", "chat.txt:").replace("calls:", "calls.csv:").replace("photo:", "photo.jpg:");
      return `<div class="sticky ${cls}" id="t-${esc(k.replace(/[^\w]/g, "_"))}"><span class="q">${esc(a.active.label)}</span><span class="loc">${esc(pretty)}</span></div>`;
    }).join("") || `<div class="empty">${esc(L.empty)}</div>`;

    document.getElementById("root").innerHTML =
      `<div class="board" id="board">
        <section class="card" style="flex:1.45"><h3><i style="background:var(--exhibit-chat)"></i>chat.txt</h3><div class="rows">${chat}</div></section>
        <section class="card" style="flex:1.1"><h3><i style="background:var(--exhibit-calls)"></i>calls.csv</h3><div class="rows">${calls}</div></section>
        <section class="card" style="flex:.95"><h3><i style="background:var(--exhibit-photo)"></i>photo.jpg</h3>
          <div class="photo"><img alt="photo.jpg" src="${a.photo || ""}"></div><div class="rows">${exif}</div></section>
        <aside class="tray"><h4>${esc(L.tray)}</h4>${trayItems}</aside>
        <svg class="strings" id="strings"></svg>
      </div>`;
    document.querySelectorAll(".row[data-key]").forEach((el) => el.addEventListener("click", () => toggle(el.dataset.key)));
    document.querySelectorAll(".rows").forEach((el) => el.addEventListener("scroll", drawStrings));
    frame(700);
    requestAnimationFrame(drawStrings);
  }

  function toggle(key) {
    if (args.locked) return;
    const q = args.active.id, list = cites[q] || [];
    cites[q] = list.includes(key) ? list.filter((k) => k !== key) : [...list, key];
    send({ cites });
    render();
  }

  function drawStrings() {
    const svg = document.getElementById("strings"), board = document.getElementById("board");
    if (!svg || !board || !(args.marks || []).length) return;
    const b = board.getBoundingClientRect();
    let html = "";
    (args.marks || []).filter((m) => m.qid === args.active.id).forEach((m) => {
      const id = m.key.replace(/[^\w]/g, "_");
      const row = document.getElementById("r-" + id), tip = document.getElementById("t-" + id);
      if (!row || !tip) return;
      const r = row.getBoundingClientRect(), t = tip.getBoundingClientRect(), holds = m.label === "valid";
      const clipped = r.top < b.top + 40 || r.bottom > b.bottom;
      if (clipped) return;
      const x1 = r.right - b.left - 4, y1 = r.top + r.height / 2 - b.top, x2 = t.left - b.left, y2 = t.top + t.height / 2 - b.top;
      const dx = Math.max(40, (x2 - x1) / 2), color = holds ? "var(--success)" : "var(--danger)";
      html += `<path d="M${x1} ${y1} C${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}" stroke="${color}" ${holds ? "" : 'stroke-dasharray="5 4"'}/>` +
              `<circle cx="${x1}" cy="${y1}" r="5" fill="${color}"/><circle cx="${x2}" cy="${y2}" r="5" fill="${color}"/>`;
    });
    svg.innerHTML = html;
  }

  window.addEventListener("message", (e) => {
    if (e.data && e.data.type === "streamlit:render") {
      args = e.data.args;
      cites = JSON.parse(JSON.stringify(args.cites || {}));
      render();
    }
  });
  window.addEventListener("resize", drawStrings);
  window.parent.postMessage({ isStreamlitMessage: true, type: "streamlit:componentReady", apiVersion: 1 }, "*");
})();
