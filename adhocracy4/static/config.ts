const loginUrl: string = '/accounts/login'

interface Adhocracy4Global {
  getCurrentPath: () => string
}

declare global {
  interface Window {
    adhocracy4: Adhocracy4Global
  }
}

const getLoginUrl = (): string => {
  const next = window.adhocracy4.getCurrentPath()
  return loginUrl + '?next=' + encodeURIComponent(next)
}

export {
  getLoginUrl
}