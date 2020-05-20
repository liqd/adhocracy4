(function (init) {
  document.addEventListener('DOMContentLoaded', init, false)
  document.addEventListener('a4.embed.ready', init, false)
})(function () {
  const $ = window.jQuery
  if ($.fn.selectdropdown) {
    $('.select-dropdown').selectdropdown()
  }
})
