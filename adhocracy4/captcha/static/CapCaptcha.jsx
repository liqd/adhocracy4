import React, { useEffect, useRef, useState } from 'react'
import django from 'django'

const translated = {
  error: django.gettext('There was a problem loading the CAPTCHA.'),
  noscript: django.gettext('Please enable JavaScript to complete the captcha.')
}

const scriptPromises = {}

function loadWidget (src, wasmUrl, hashwxUrl) {
  if (!src) {
    return Promise.reject(new Error('Missing Cap widget URL'))
  }
  if (scriptPromises[src]) {
    return scriptPromises[src]
  }
  if (window.customElements && window.customElements.get('cap-widget')) {
    scriptPromises[src] = Promise.resolve()
    return scriptPromises[src]
  }
  if (wasmUrl) {
    window.CAP_CUSTOM_WASM_URL = wasmUrl
  }
  if (hashwxUrl) {
    window.CAP_CUSTOM_HASHWX_URL = hashwxUrl
  }
  scriptPromises[src] = new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.src = src
    script.async = true
    script.onload = resolve
    script.onerror = () => {
      delete scriptPromises[src]
      reject(new Error('Failed to load Cap widget'))
    }
    document.head.appendChild(script)
  })
  return scriptPromises[src]
}

const CapCaptcha = ({
  endpoint,
  widgetUrl,
  wasmUrl,
  hashwxUrl,
  name,
  lang,
  refresh,
  onChange
}) => {
  const widgetRef = useRef(null)
  const onChangeRef = useRef(onChange)
  const [error, setError] = useState('')

  onChangeRef.current = onChange

  useEffect(() => {
    const widget = widgetRef.current
    if (!widget) {
      return
    }

    const handleSolve = (event) => {
      setError('')
      onChangeRef.current(event.detail.token)
    }
    const handleReset = () => {
      setError('')
      onChangeRef.current('')
    }
    const handleError = () => {
      setError(translated.error)
      onChangeRef.current('')
    }

    widget.addEventListener('solve', handleSolve)
    widget.addEventListener('reset', handleReset)
    widget.addEventListener('error', handleError)

    loadWidget(widgetUrl, wasmUrl, hashwxUrl).catch(() => {
      setError(translated.error)
    })

    return () => {
      widget.removeEventListener('solve', handleSolve)
      widget.removeEventListener('reset', handleReset)
      widget.removeEventListener('error', handleError)
    }
  }, [widgetUrl, wasmUrl, hashwxUrl])

  useEffect(() => {
    const widget = widgetRef.current
    if (widget && typeof widget.reset === 'function') {
      widget.reset()
    }
  }, [refresh])

  return (
    <div className="a4-cap-captcha">
      <cap-widget
        ref={widgetRef}
        data-cap-api-endpoint={endpoint}
        data-cap-hidden-field-name={name || 'captcha'}
        data-cap-lang={lang}
      />
      {error && <p className="a4-cap-captcha__error">{error}</p>}
      <noscript>
        <p className="form-hint">{translated.noscript}</p>
      </noscript>
    </div>
  )
}

export default CapCaptcha
