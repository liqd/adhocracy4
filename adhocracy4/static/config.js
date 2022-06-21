const loginUrl = '/accounts/login'

const getLoginUrl = function () {
  const next = window.adhocracy4.getCurrentPath()
  return loginUrl + '?next=' + encodeURIComponent(next)
}

module.exports = {
  getLoginUrl
}
