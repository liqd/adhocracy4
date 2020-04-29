const $ = require('jquery')
const elementsToUpdate = ['.l-menu__menu', '.l-menu__aside', '.js-selector-update-dashboard']

module.exports = {
  /**
   * Makes an ajax call to the current page and updates the elements menu and
   * progress.
   */
  updateDashboard () {
    $.get(window.location.pathname, { dataType: 'html' }, function (data) {
      const selector = elementsToUpdate.join(', ')
      const $newElements = $(data).find(selector)
      const $oldElements = $(selector)

      $oldElements.each(function (i, e) {
        $(e).replaceWith($newElements.eq(i))
      })
    })
  }
}
