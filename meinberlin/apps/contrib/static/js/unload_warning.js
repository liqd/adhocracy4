/* global $ CKEDITOR */

$(function () {
  let submitted = false
  const changeHandler = function () {
    $(window).on('beforeunload', function () {
      if (!submitted) {
        return false
      }
    })
  }

  if (CKEDITOR) {
    CKEDITOR.on('instanceReady', function (e) {
      e.editor.on('change', changeHandler)
    })
  }

  $(document).one('change', changeHandler)
    .on('submit', function () {
      submitted = true
    })
})
