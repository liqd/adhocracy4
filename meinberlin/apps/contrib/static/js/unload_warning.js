/* global $ CKEDITOR */

$(function () {
  var submitted = false
  var changeHandler = function () {
    $(window).on('beforeunload', function () {
      if (!submitted) {
        return false
      }
    })
  }

  // eslint-disable-next-line no-constant-condition
  if (!typeof CKEDITOR === 'undefined') {
    CKEDITOR.on('instanceReady', function (e) {
      e.editor.on('change', changeHandler)
    })
  }

  $(document).one('change', changeHandler)
    .on('submit', function () {
      submitted = true
    })
})
