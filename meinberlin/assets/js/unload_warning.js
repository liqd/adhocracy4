/* This code checks if something has been changed in a form but not submitted.
   If the user wants to leave the the page there will be warning. */

/* global CKEDITOR django */

$(function () {
  var submitted = false
  var changeHandler = function () {
    var target = event.target.id
    if (target.includes('dashboard-nav')) {
      submitted = true
    }
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
