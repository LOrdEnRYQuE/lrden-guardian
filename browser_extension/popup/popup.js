/**
 * LRDEnE Guardian - Popup Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  const apiKeyInput = document.getElementById('apiKey');
  const saveBtn = document.getElementById('saveBtn');

  // Load saved API key
  chrome.storage.local.get(['apiKey'], (result) => {
    if (result.apiKey) {
      apiKeyInput.value = result.apiKey;
    }
  });

  // Save API key
  saveBtn.addEventListener('click', () => {
    const apiKey = apiKeyInput.value.trim();
    if (apiKey) {
      chrome.storage.local.set({ apiKey }, () => {
        saveBtn.innerText = "✓ Saved";
        saveBtn.style.background = "#059669";
        setTimeout(() => {
          saveBtn.innerText = "Save Configuration";
          saveBtn.style.background = "#10b981";
        }, 2000);
      });
    }
  });
});
