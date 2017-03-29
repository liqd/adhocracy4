/* global $ location django */
$(document).ready(function () {
  var $main = $('main')
  var currentPath
  var popup
  var patternsForPopup = /\/accounts\b/

  var headers = {
    'X-Embed': ''
  }

  var loadHtml = function (html, textStatus, xhr) {
    var $root = $(html).filter('main')
    var nextPath = xhr.getResponseHeader('x-ajax-path')

    if (patternsForPopup.test(nextPath)) {
      $('#embed-confirm').modal('show')
      return false
    }
    // only update the currentPath if there was no modal opened
    currentPath = nextPath

    $main.empty()
    $main.append($root.children())
    onReady()
  }

  var onReady = function () {
    // adhocracy4.onReady($main)
  }

  var getEmbedTarget = function ($element, url) {
    var embedTarget = $element.data('embedTarget')

    if (embedTarget) {
      return embedTarget
    } else if (!url || url[0] === '#' || $element.attr('target')) {
      return 'ignore'
    } else if ($element.is('.rich-text a')) {
      return 'external'
    } else if (patternsForPopup.test(url)) {
      return 'popup'
    } else {
      return 'internal'
    }
  }

  $(document).on('click', 'a[href]', function (event) {
    // NOTE: event.target.href is resolved against /embed/
    var url = event.target.getAttribute('href')
    var $link = $(event.target)
    var embedTarget = getEmbedTarget($link, url)

    if (embedTarget === 'internal') {
      event.preventDefault()

      if (url[0] === '?') {
        url = currentPath + url
      }

      $.ajax({
        url: url,
        headers: headers,
        success: loadHtml
      })
    } else if (embedTarget === 'popup') {
      event.preventDefault()
      popup = window.open(
        url,
        'embed_popup',
        'height=650,width=500,location=yes,menubar=no,toolbar=no,status=no'
      )
    }
  })

  $(document).on('submit', 'form[action]', function (event) {
    var form = event.target
    var $form = $(form)
    var embedTarget = getEmbedTarget($form, form.method)

    if (embedTarget === 'internal') {
      event.preventDefault()

      $.ajax({
        url: form.action,
        method: form.method,
        headers: headers,
        data: $form.serialize(),
        success: loadHtml
      })
    }
  })

  $('.js-embed-logout').on('click', function (e) {
    e.preventDefault()
    $.post(
      '/accounts/logout/',
      function () {
        location.reload()
      }
    )
  })

  // The popup will send a message when the user is logged in. Only after
  // this message the Popup will close.
  window.addEventListener('message', function (e) {
    if (e.origin === location.origin) {
      var data = JSON.parse(e.data)

      if (data.name === 'popup-close' && popup) {
        popup.close()
        location.reload()
      }
    }
  }, false)

  $(document).ajaxError(function (event, jqxhr) {
    var text
    var $error = $('<p class="embed-status__message embed-status__message--error" role="alert"></p>')
    var $close = $('<button class="embed-status__close"><i class="fa fa-times" aria-hidden="true"></i></button>')

    var removeMessage = function () {
      $error.remove()
    }

    switch (jqxhr.status) {
      case 404:
        text = django.gettext('We couldn\'t find what you were looking for.')
        break
      case 400:
        text = django.gettext('You don\'t have the permission to view this page.')
        break
      default:
        text = django.gettext('Something went wrong!')
        break
    }

    $error.text(text)
    $error.append($close)
    $error.prependTo($('#embed-status'))
    $close.attr('title', django.gettext('Close'))

    $close.on('click', removeMessage)
    setTimeout(removeMessage, 6000)
  })

  $.ajax({
    url: $('body').data('url'),
    headers: headers,
    success: loadHtml
  })
})
