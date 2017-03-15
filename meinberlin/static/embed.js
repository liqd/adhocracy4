/* global $ */
$(document).ready(function () {
  var $main = $('main')

  var loadHtml = function (html) {
    var $root = $(html).filter('main')
    $main.empty()
    $main.append($root.children())
    onReady()
  }

  var onReady = function () {
    // adhocracy4.onReady($main)
  }

  $(document).on('click', function (event) {
    if (event.target.href && !event.target.target) {
      event.preventDefault()
      // FIXME: skip internal links
      // FIXME: some links should be opened on the platform
      // FIXME: external links should not be opened in the iframe
      // FIXME: jump links should not trigger a request
      // FIXME: relative links should be resolved against currently loaded url
      $.ajax({
        url: event.target.href,
        success: loadHtml
      })
    }
  })

  $(document).on('submit', 'form[action]', function (event) {
    event.preventDefault()
    var form = event.target

    // timeout required for use with CKEditor
    setTimeout(function () {
      $.ajax({
        url: form.action,
        method: form.method,
        data: $(form).serialize(),
        success: loadHtml
      })
    })
  })

  $.ajax({
    url: 'http://localhost:8000/projects/project/',
    success: loadHtml
  })
})
