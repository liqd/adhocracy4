/* This code is used to save closed accordions in the dashboard in a cookie */

import Cookies from 'js-cookie'

function init () {
  const cookieName = 'dashboard_projects_closed_accordions'

  if (Cookies.get(cookieName) === undefined) {
    Cookies.set(cookieName, '[]')
  }

  $('.dashboard-nav__checkbox').change(function (e) {
    const currentId = parseInt(this.id.split('--')[1])
    const cookie = Cookies.get(cookieName)
    let currentList = []

    if (cookie) {
      currentList = JSON.parse(cookie)
    }

    if (!this.checked && !currentList.includes(currentId)) {
      currentList.push(currentId)
      Cookies.set(cookieName, JSON.stringify(currentList))
    } else if (this.checked && currentList.includes(currentId)) {
      currentList.splice(currentList.indexOf(currentId), 1)
      Cookies.set(cookieName, JSON.stringify(currentList))
    }
  })
}

document.addEventListener('DOMContentLoaded', init)
