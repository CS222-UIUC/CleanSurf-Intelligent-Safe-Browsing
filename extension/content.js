'use strict';


(function() {
  function waitForImage(imgElem) {
    return new Promise((res, rej) => {
      if (imgElem.complete) {
        return res();
      }
      imgElem.onload = () => res();
      imgElem.onerror = () => rej(imgElem);
    });
  }

  async function getBase64Image(img) {
    const altImg = new Image();
    // wait for the image to load
    altImg.crossOrigin = 'anonymous';
    altImg.src = img.src;

    await waitForImage(altImg);

    const canvas = document.createElement('canvas');
    canvas.width = altImg.width;
    canvas.height = altImg.height;
    const ctx = canvas.getContext('2d');
    // img.setAttribute('crossorigin', 'anonymous');
    ctx.drawImage(altImg, 0, 0);
    const dataURL = canvas.toDataURL('image/png');

    return dataURL.replace(/^data:image\/(png|jpg);base64,/, '');
  }

  function clean(image) {
    // image.style.filter = `blur(10px) opacity(1)`;
    // log the image's base64 string
    getBase64Image(image).then((data) => {
      fetch('http://localhost:5000/image', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify({image: data}),
      }).then((res) => {
        res.json().then((data) => {
          image.src = 'data:image/png;base64,' + data['image'];
        }).catch((err) => {
          console.log('Response error: ', err);
        });
        // image.src = 'data:image/png;base64,' + res.json()['image'];
      }).catch((err) => {
        console.log('Network error: ', err);
      });
    }).catch((err) => {
      console.log('Image error: ', err);
    });
    // console.log(getBase64Image(image));
  }

  function cleanAll() {
    const images = document.querySelectorAll('img');
    for (const image of images) {
      clean(image);
    }
  }

  chrome.runtime.onMessage.addListener(
      function(request, sender, sendResponse) {
        if (request.status === 'clean') {
          cleanAll();
        }
      });
})();
