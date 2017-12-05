var loginUrl = '/accounts/login'

var getLoginUrl = function () {
  let next = window.adhocracy4.getCurrentPath()
  return loginUrl + '?next=' + encodeURIComponent(next)
}

module.exports = {
  getLoginUrl: getLoginUrl
}
