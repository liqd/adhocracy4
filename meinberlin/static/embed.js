/* global $ location */
$(document).ready(function () {
  var $main = $('main')
  var currentPath
  var patternsForPopup = /\/accounts\b/

  var headers = {
    'X-Embed': ''
  }

  var loadHtml = function (html, textStatus, xhr) {
    var $root = $(html).filter('main')
    var nextPath = xhr.getResponseHeader('x-ajax-path')

    if (patternsForPopup.test(nextPath)) {
      var popup = new PlatformPopup(nextPath, true)
      PlatformPopup.popups.push(popup)
      return false
    }
    // only update the currentPath if there was no popup opened
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

  $.ajax({
    url: $('body').data('url'),
    headers: headers,
    success: loadHtml
  })

  $('.js-embed-login').on('click', function (e) {
    e.preventDefault()

    var popup = new PlatformPopup(this.getAttribute('href'))
    PlatformPopup.popups.push(popup)
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

  var PlatformPopup = function (url, isAsync) {
    this.url = url
    this.isPending = false
    if (isAsync) {
      this.askForLogin()
    } else {
      this.openLoginPopup()
    }
  }
  PlatformPopup.popups = []

  PlatformPopup.prototype.askForLogin = function () {
    if (!this.isPending) {
      this.isPending = true
      var template = $('#embed-confirm').html()
      this.$embedConfirm = $(template).appendTo('.embed-header')

      this.$embedConfirm.on('click', this.handleConfirm.bind(this))
    }
  }

  PlatformPopup.prototype.handleConfirm = function (e) {
    var $target = $(e.target)

    if ($target.is('.js-embed-login')) {
      e.preventDefault()
      this.openLoginPopup()
    }

    this.$embedConfirm.remove()
    this.isPending = false
  }

  PlatformPopup.prototype.openLoginPopup = function () {
    this.popup = window.open(
      this.url,
      'embed_popup',
      'height=650,width=500,location=yes,menubar=no,toolbar=no,status=no'
    )
    // The popup will send a message when the user is logged in. Only after
    // this message the Popup will close.
    window.addEventListener('message', this.handlePopupMessage.bind(this), false)
  }

  PlatformPopup.prototype.handlePopupMessage = function (e) {
    if (e.origin === location.origin) {
      var data = JSON.parse(e.data)

      if (data.name === 'popup-close') {
        this.popup.close()
        location.reload()
      }
    }
  }
})
