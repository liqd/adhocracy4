/* global $ */
$(document).ready(function () {
  var $main = $('main')
  var currentPath

  var loadHtml = function (html, textStatus, xhr) {
    var $root = $(html).filter('main')
    currentPath = xhr.getResponseHeader('x-ajax-path')
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

      if (url[0] === '?') {
        url = currentPath + url
      }

      // FIXME: some links should be opened on the platform
      // FIXME: external links should not be opened in the iframe
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
