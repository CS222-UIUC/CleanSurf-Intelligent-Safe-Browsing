function sendMessage(message) {
  console.log(message);
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, {status: message}, () => {});
  });
}

const btn = document.getElementById('clean-btn');
btn.addEventListener('click', function onClick(event) {
  sendMessage('clean');
});
