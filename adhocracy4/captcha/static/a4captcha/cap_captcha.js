function initializeCapCaptcha () {
  document.querySelectorAll('cap-widget[data-a4-cap-wasm-url]').forEach(function (widget) {
    window.CAP_CUSTOM_WASM_URL = widget.dataset.a4CapWasmUrl
  })
  document.querySelectorAll('cap-widget[data-a4-cap-hashwx-url]').forEach(function (widget) {
    window.CAP_CUSTOM_HASHWX_URL = widget.dataset.a4CapHashwxUrl
  })
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeCapCaptcha, false)
} else {
  initializeCapCaptcha()
}
document.addEventListener('a4.embed.ready', initializeCapCaptcha, false)
document.addEventListener('htmx:afterSwap', initializeCapCaptcha, false)
