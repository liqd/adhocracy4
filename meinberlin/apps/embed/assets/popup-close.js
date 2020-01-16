// if this page was opened from an embed for login, notify it about success
if (window.opener) {
  window.opener.postMessage(
    JSON.stringify({ name: 'popup-close' }),
    location.origin
  )
}
