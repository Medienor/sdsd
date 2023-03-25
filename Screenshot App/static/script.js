const form = document.querySelector('form');
const screenshotContainer = document.querySelector('#screenshot-container');
const loader = document.querySelector('.loader');
const loaderPercent = document.querySelector('.loader-percent');
const successMessage = document.querySelector('#success-message');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const url = document.querySelector('#url-input').value;
  const response = await fetch('/screenshot?url=' + encodeURIComponent(url) + '&screenshot_type=' + document.querySelector('#screenshot-type').value);
  const screenshotUrl = await response.text();
  const latestScreenshot = screenshotUrl.split('/').pop();
  const screenshotImg = document.createElement('img');
  const screenshotWrapper = document.createElement('div');
  screenshotWrapper.classList.add('screenshot-wrapper');
  screenshotImg.src = screenshotUrl;
  screenshotWrapper.appendChild(screenshotImg);
  loader.style.display = 'block';
  screenshotContainer.innerHTML = '';
  screenshotContainer.appendChild(screenshotWrapper);

  let percent = 0;
  const intervalId = setInterval(() => {
    percent += 10;
    loaderPercent.textContent = `${percent}%`;
    if (percent >= 100) {
      clearInterval(intervalId);
      loader.style.display = 'none';
      successMessage.classList.remove('hidden');
      document.querySelector('#latest-screenshot').value = latestScreenshot;
    }
  }, 1000);
});
