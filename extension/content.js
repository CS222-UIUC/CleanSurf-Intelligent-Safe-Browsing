'use strict';

document.addEventListener('DOMContentLoaded', () => {
  chrome.storage.sync.set({'blurThreshold': 0.5});
});

(function() {
  const imagesMap = new Map();

  /**
   * Wait for the image to load
   *
   * @param {Element} imgElem
   * @return {Promise<unknown>}
   */
  function waitForImage(imgElem) {
    return new Promise((res, rej) => {
      if (imgElem.complete) {
        return res();
      }
      imgElem.onload = () => res();
      imgElem.onerror = () => rej(imgElem);
    });
  }

  /**
   * Returns the base64 encoded image
   *
   * @param {Element} img
   * @return {Promise<unknown>}
   */
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

  /**
   * Cleans the image element
   *
   * @param {Element} image
   */
  function clean(image) {
    imagesMap.set(image, false);
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
          imagesMap.set(image, true);
          const verdict = data['verdict'];
          console.log(verdict);
          chrome.storage.sync.get(['blurThreshold'], (values) => {
            if (verdict['unsafe'] > 1-values.blurThreshold) {
              console.log(verdict['unsafe']);
              image.style.filter = `blur(10px) opacity(1)`;
            }
          });
        }).catch((err) => {
          imagesMap.set(image, true);
          console.log('Response error: ', err);
        });
        // image.src = 'data:image/png;base64,' + res.json()['image'];
      }).catch((err) => {
        imagesMap.set(image, true);
        console.log('Network error: ', err);
      });
    }).catch((err) => {
      imagesMap.set(image, true);
      console.log('Image error: ', err);
    });
  }

  /**
   * Cleans all images on the page
   *
   * @return {Promise<void>}
   */
  function cleanAll() {
    const images = document.querySelectorAll('img');
    for (const image of images) {
      if (!imagesMap.has(image)) {
        clean(image);
      } else {
        console.log('Image already cleaned');
      }
    }

    return new Promise((res, rej) => {
      const interval = setInterval(() => {
        if (Array.from(imagesMap.values()).every((val) => val)) {
          clearInterval(interval);
          res();
        }
      });
    });
  }

  chrome.runtime.onMessage.addListener(
      function(request, sender, sendResponse) {
        const overlay = document.createElement('div');
        overlay.setAttribute('style',
            'position: fixed; top: 0; left: 0; width: 100%; height: 100%;' +
            'background-color: rgba(111, 255, 224); opacity: 0.6; ',
        );

        const text = document.createElement('div');
        text.innerHTML = 'CLEANING...';
        text.setAttribute('style',
            'position: absolute; top: 50%; left: 50%; transform: ' +
            'translate(-50%, 0%); font-size: 50px; color: white; ' +
            'font-weight: bold; text-align: center; width: 100%; ' +
            'height: 100%; font-family: \'Source Code Pro\', monospace; ',
        );

        overlay.appendChild(text);
        document.body.appendChild(overlay);
        if (request.status === 'clean') {
          cleanAll().then(() => {
            console.log('Done');
            text.innerHTML = 'PAGE CLEANED';
            // Create overlay div on page that says DONE in capital letters
            const fade = setInterval(function() {
              if (overlay.style.opacity > 0) {
                overlay.style.opacity -= 0.01;
              } else {
                overlay.remove();
                clearInterval(fade);
              }
            }, 25);
          });
        }
      });
})();
