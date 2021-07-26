/* global $ */
function init () {
  const clearInputs = $('input[data-upload-clear]')
  const previewImages = $('img[data-upload-preview]')

  previewImages.each(function (index, previewImage) {
    previewImage = $(previewImage)
    const inputId = previewImage.data('uploadPreview')
    const clearInput = clearInputs.filter('[data-upload-clear="' + inputId + '"]')
    $('#' + inputId).change(function (e) {
      const domInput = e.target
      if (domInput.files && domInput.files[0]) {
        const name = domInput.files[0].name
        $('#text-' + inputId).val(name)
        previewImage.alt = name
        if (window.FileReader) {
          const reader = new window.FileReader()
          reader.onload = function (e) {
            previewImage.attr('src', e.target.result)
            clearInput.prop('checked', false)
          }
          reader.readAsDataURL(domInput.files[0])
        } else {
          clearInput.prop('checked', false)
        }
      }
    })
  })
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
