// handle token download button clicks

/* global django */

document.addEventListener('DOMContentLoaded', initTokenDownloadButtons)

function initTokenDownloadButtons () {
  const buttons = document.querySelectorAll('[id^="download-link-"]')
  buttons.forEach((button, index) => {
    if (!button.classList.contains('disabled')) {
      button.onclick = () => {
        button.classList.add('btn--light', 'disabled')
        button.classList.remove('btn--secondary')
        button.innerHTML = django.gettext('Encrypted')
      }
    }
  })
}
