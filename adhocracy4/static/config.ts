const loginUrl = '/accounts/login'

export const getLoginUrl = function () {
  const next = window.adhocracy4!.getCurrentPath()
  return loginUrl + '?next=' + encodeURIComponent(next)
}

export default {
  getLoginUrl
}
