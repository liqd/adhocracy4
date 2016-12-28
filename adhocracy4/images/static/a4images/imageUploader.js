window.jQuery(document).ready(function () {
  var $ = window.jQuery
  var clearInputs = $('input[data-upload-clear]')
  var previewImages = $('img[data-upload-preview]')

  previewImages.each(function (index, previewImage) {
    previewImage = $(previewImage)
    var inputId = previewImage.data('uploadPreview')
    var clearInput = clearInputs.filter('[data-upload-clear="' + inputId + '"]')
    $('#' + inputId).change(function (e) {
      var domInput = e.target
      if (domInput.files && domInput.files[0]) {
        if (window.FileReader) {
          var reader = new window.FileReader()
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
})
