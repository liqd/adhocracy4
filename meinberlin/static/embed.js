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

  $(document).on('click', 'a[href]', function (event) {
    // NOTE: event.target.href is resolved against /embed/
    var url = event.target.getAttribute('href')
    var $link = $(event.target)
    var embedTarget = $link.data('embedTarget')

    if (
      url &&
      url[0] !== '#' &&
      !event.target.target &&
      embedTarget !== 'platform' &&
      embedTarget !== 'external' &&
      !$link.is('.rich-text *')
    ) {
      event.preventDefault()

      if (url[0] === '?') {
        url = currentPath + url
      }

      $.ajax({
        url: url,
        success: loadHtml
      })
    }
  })

  $(document).on('submit', 'form[action]', function (event) {
    var form = event.target
    var $form = $(form)
    var embedTarget = $form.data('embedTarget')

    if (embedTarget !== 'platform' && embedTarget !== 'external') {
      event.preventDefault()

      $.ajax({
        url: form.action,
        method: form.method,
        data: $form.serialize(),
        success: loadHtml
      })
    }
  })

  $.ajax({
    url: 'http://localhost:8000/projects/project/',
    success: loadHtml
  })
})
