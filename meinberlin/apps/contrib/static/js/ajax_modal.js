/* globals $ django */
$(function () {
  var modalHTML = (
    '<div class="modal">' +
      '<div class="modal-dialog modal-lg" role="document">' +
        '<div class="modal-content">' +
          '<div class="modal-header"><h2 class="modal-title u-first-heading"></h2>' +
            '<button type="button" class="close" data-dismiss="modal" aria-label="' + django.gettext('Close') + '"><span aria-hidden="true">&times;</span></button>' +
          '</div>' +
          '<div class="modal-body"></div>' +
      '  </div>' +
      '</div>' +
    '</div>'
  )
  var $backdrop = $('<div class="modal-backdrop" />')

  var extractScripts = function ($root, selector, attr) {
    var $existingValues = $('head').find(selector).map(function (i, e) {
      return $(e).attr(attr)
    })

    $root.find(selector).each(function (i, script) {
      var $script = $(script)
      var $matches = $existingValues.filter(function (i, v) {
        return v === $script.attr(attr)
      })
      if ($matches.length === 0) {
        $('head').append($script)
      }
    })
  }

  $(document).on('click', '[data-toggle="ajax-modal"]', function (e) {
    e.preventDefault()
    var target = this.href + ' ' + this.dataset.targetSelector
    var $newModal = $(modalHTML)
    var _this = this

    $newModal.find('.close').on('click', function () {
      $newModal.remove()
      $backdrop.remove()
    })

    $newModal.find('.modal-body').load(target, function (html) {
      var $root = $('<div>').html(html)
      var title = $root.find('h1').text()
      $newModal.find('.modal-title').text(title)
      extractScripts($root, 'script[src]', 'src')
      extractScripts($root, 'link[rel="stylesheet"]', 'href')
      $backdrop.appendTo(document.documentElement)
      $newModal.insertAfter(_this).show()
    })
  })
})
