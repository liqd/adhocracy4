/* global $ CKEDITOR django */

$(function () {
  var submitted = false
  var changeHandler = function () {
    $(window).on('beforeunload', function (e) {
      if (!submitted) {
        var string = django.gettext('If you leave this page changes you made will not be saved.')
        e.returnValue = string
        return string
      }
    })
  }

  if (window.CKEDITOR) {
    CKEDITOR.on('instanceReady', function (e) {
      e.editor.on('change', changeHandler)
    })
  }

  $(document).one('change', changeHandler)
    .on('submit', function (e) {
      if ($(e.target).data('ignore-submit') === true) {
        return true
      }
      submitted = true
    })
})
