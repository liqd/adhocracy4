/* global $ */
$(function () {
  $('[data-toggle="popover"]').popover()
})

$('body').on('click', function (e) {
  $('[data-toggle="popover"]').each(function () {
    if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
      $(this).popover('hide')
    }
  })
})
