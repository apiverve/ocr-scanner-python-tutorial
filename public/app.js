import { api, busy, esc, showError } from './ui.js';

const MAX_BYTES = 4 * 1024 * 1024;
const TYPES = ['image/jpeg', 'image/png', 'image/gif'];

const form = document.getElementById('form');
const drop = document.getElementById('drop');
const file = document.getElementById('file');
const prompt = document.getElementById('prompt');
const go = document.getElementById('go');
const result = document.getElementById('result');
let image = null;

function pick(chosen) {
  result.innerHTML = '';
  image = null;
  go.disabled = true;
  if (!chosen) return;
  if (!TYPES.includes(chosen.type)) return showError(result, 'Use a JPG, PNG or GIF image.');
  if (chosen.size > MAX_BYTES) return showError(result, 'Images must be 4 MB or smaller.');
  image = chosen;
  go.disabled = false;
  prompt.innerHTML = `<img src="${URL.createObjectURL(chosen)}" alt="The image you chose">`;
}

file.addEventListener('change', () => pick(file.files[0]));
drop.addEventListener('dragover', (e) => {
  e.preventDefault();
  drop.classList.add('over');
});
drop.addEventListener('dragleave', () => drop.classList.remove('over'));
drop.addEventListener('drop', (e) => {
  e.preventDefault();
  drop.classList.remove('over');
  pick(e.dataTransfer.files[0]);
});

form.addEventListener('submit', (e) => {
  e.preventDefault();
  if (!image) return;
  const body = new FormData();
  body.append('image', image);
  busy(go, 'Reading…', async () => {
    try {
      const d = await api('/api/scan', { method: 'POST', body });
      const text = (d.text || '').trim();
      if (!text) {
        result.innerHTML = '<p class="hint">No text found in this image.</p>';
        return;
      }
      const lines = text.split('\n').filter((l) => l.trim()).length;
      result.innerHTML = `
        <pre class="text">${esc(text)}</pre>
        <div class="actions">
          <button type="button" class="ghost" id="copy">Copy text</button>
          <span class="hint">${text.length.toLocaleString()} characters, ${lines} lines</span>
        </div>`;
      document.getElementById('copy').addEventListener('click', async (ev) => {
        await navigator.clipboard.writeText(text);
        ev.target.textContent = 'Copied';
      });
    } catch (err) {
      showError(result, err);
    }
  });
});
