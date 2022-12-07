/**
 * Sends a message to the content script
 *
 * @param {string} message
 * @param {function} onReceive
 */
function sendMessage(message, onReceive) {
  console.log(message);
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, {status: message}, () => {});
  });
}

/**
 * Animates the button
 */
function animateButton() {
  console.log('Animating button');
  const button = document.getElementById('clean-btn');
  button.classList.add('animate');
  setTimeout(() => {
    button.classList.remove('animate');
  }, 1000);
}

document.addEventListener('DOMContentLoaded', function() {
  const btn = document.getElementById('clean-btn');
  btn.addEventListener('click', function onClick(event) {
    sendMessage('clean', animateButton);
  });
});


const slider = document.getElementById('intensity-slider');
slider.addEventListener('input', () => {
  chrome.storage.sync.set({'blurThreshold': slider.value / 10});
});

document.addEventListener('DOMContentLoaded', () => {
  chrome.storage.sync.get(['blurThreshold'], (values) => {
    const slider = document.getElementById('intensity-slider');
    slider.value = values.blurThreshold * 10;
  });
});
