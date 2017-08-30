/* globals django */
export default {
  removeActiveRequired () {
    const activeIcon = document.querySelector('.dashboard-nav__item.is-active .fa-exclamation-circle')
    activeIcon.parentNode.removeChild(activeIcon)
  },

  addActiveRequired () {
    const missingTranslation = django.gettext('Missing fields for publication')
    const activeIcon = document.createElement('i')
    const active = document.querySelector('.dashboard-nav__item.is-active')

    activeIcon.className = 'fa fa-exclamation-circle u-danger'
    activeIcon.title = missingTranslation
    activeIcon.setAttribute('aria-label', missingTranslation)
    active.appendChild(activeIcon)
  }
}
