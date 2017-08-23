/* globals $ */
$(function () {
  var $ajaxModals = $('[data-toggle="ajax-modal"]')
  var modalHTML = (
    '<div class="modal">' +
      '<div class="modal-dialog modal-lg" role="document">' +
        '<div class="modal-content">' +
          '<div class="modal-header"><h2 class="modal-title u-first-heading"></h2><button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>' +
          '<div class="modal-body"></div>' +
      '  </div>' +
      '</div>' +
    '</div>'
  )
  var $backdrop = $('<div class="modal-backdrop" />')

  $ajaxModals.on('click', function (e) {
    e.preventDefault()
    var target = this.href + ' ' + this.dataset.targetSelector
    var $newModal = $(modalHTML)
    var _this = this

    $newModal.find('.close').on('click', function () {
      $newModal.remove()
      $backdrop.remove()
    })

    $newModal.find('.modal-body').load(target, function (html) {
      var title = $(html).find('h1').text()
      $newModal.find('.modal-title').text(title)
      $backdrop.appendTo(document.documentElement)
      $newModal.insertAfter(_this).show()
    })
  })
})
