function init () {
  const clearInputs = document.querySelectorAll('input[data-upload-clear]')
  const previewImages = document.querySelectorAll('img[data-upload-preview]')

  previewImages.forEach(function (previewImage, index) {
    previewImage = document.getElementById(previewImage.id)
    const inputId = previewImage.dataset.uploadPreview
    const clearInput = Array.from(clearInputs).filter(el => el.matches('[data-upload-clear="' + inputId + '"]'))
    document.querySelector('#' + inputId).addEventListener('change', function (e) {
      const domInput = e.target
      if (domInput.files && domInput.files[0]) {
        const name = domInput.files[0].name
        const text = document.querySelector('#text-' + inputId)
        if (text != null) {
          text.value = name
        }
        previewImage.alt = name
        if (window.FileReader) {
          const reader = new window.FileReader()
          reader.addEventListener('load', function (e) {
            previewImage.setAttribute('src', e.target.result)
            clearInput.checked = false
          })
          reader.readAsDataURL(domInput.files[0])
        } else {
          clearInput.checked = false
        }
      }
    })
  })
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
