import React, { useState, useRef } from 'react'
import django from 'django'

import Modal from '../../../static/Modal'

const translated = {
  share: django.gettext('Share'),
  buttonTextCopy: django.gettext('Copy'),
  buttonTextCopied: django.gettext('Copied')
}

export const UrlModal = (props) => {
  const [copied, setCopied] = useState(false)
  const inputRef = useRef(null)

  const copyUrl = (e) => {
    e.preventDefault()
    if (inputRef.current) {
      navigator.clipboard.writeText(inputRef.current.value)
        .then(() => {
          setCopied(true)
          return true
        })
        .catch((err) => {
          console.error('Failed to copy text: ', err)
        })
    }
  }

  const handleModalClose = () => {
    setCopied(false)
  }

  const partials = {
    hideHeader: true,
    hideFooter: true,
    title: props.title,
    body: (
      <div className="input-group a4-url-modal__body">
        <input
          id={'share-url-' + props.objectId}
          ref={inputRef}
          type="text"
          className="form-control"
          value={props.url}
          readOnly
        />
        <button
          className="a4-url-modal__button"
          aria-pressed={copied}
          autoComplete="off"
          onClick={(e) => copyUrl(e)}
        >
          {copied ? translated.buttonTextCopied : translated.buttonTextCopy}
        </button>
      </div>
    )
  }

  return (
    <Modal
      abort={props.abort}
      partials={partials}
      toggle={<><i className="fas fa-share" aria-hidden="true" /> {translated.share}</>}
      keepOpenOnSubmit
      onClose={handleModalClose}
    />
  )
}
