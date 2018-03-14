/* global $ */
(function (init) {
  $(init)
  $(document).on('a4.embed.ready', init)
})(function () {
  if ($.fn.selectdropdown) {
    $('.select-dropdown').selectdropdown()
  }
})
