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
    // NOTE: event.target.href is resolved against /embed/
    var url = event.target.getAttribute('href')

    if (!event.target.target && url && url[0] !== '#') {
      event.preventDefault()
      // FIXME: some links should be opened on the platform
      // FIXME: external links should not be opened in the iframe
      // FIXME: relative links should be resolved against currently loaded url
      $.ajax({
        url: url,
        success: loadHtml
      })
    }
  })

  $(document).on('submit', 'form[action]', function (event) {
    event.preventDefault()
    var form = event.target

    $.ajax({
      url: form.action,
      method: form.method,
      data: $(form).serialize(),
      success: loadHtml
    })
  })

  $.ajax({
    url: 'http://localhost:8000/projects/project/',
    success: loadHtml
  })
})
