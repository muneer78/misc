// ==UserScript==
// @name         Strip YouTube Embeds (SFGate-safe)
// @match        *://*/*
// @run-at       document-start
// ==/UserScript==

(function () {
  function removeEmbeds(root) {
    // Remove entire embed blocks
    root.querySelectorAll('div[data-block-type="embed"]').forEach(el => {
      el.remove();
    });

    // Fallback: raw YouTube iframes
    root.querySelectorAll(
      'iframe[src*="youtube.com"], iframe[src*="youtu.be"]'
    ).forEach(el => el.remove());
  }

  // Initial pass
  document.addEventListener('DOMContentLoaded', () => {
    removeEmbeds(document);
  });

  // Catch dynamically inserted embeds
  const observer = new MutationObserver(mutations => {
    for (const m of mutations) {
      for (const node of m.addedNodes) {
        if (node.nodeType === 1) {
          removeEmbeds(node);
        }
      }
    }
  });

  observer.observe(document.documentElement, {
    childList: true,
    subtree: true
  });
})();
