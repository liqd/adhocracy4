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
  for (let key in CKEDITOR.instances) {
    if (CKEDITOR.instances.hasOwnProperty(key)) {
      CKEDITOR.instances[key].on('change', changeHandler)
    }
  }

  $(document).one('change', changeHandler)
    .on('submit', function () {
      submitted = true
    })
})
