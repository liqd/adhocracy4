import React, { useState } from 'react'
import django from 'django'

import Modal from '../../../static/Modal'

export const UrlModal = (props) => {
  const [clicked, setClicked] = useState(false)
  const buttonTextCopy = django.gettext('Copy')
  const buttonTextCopied = django.gettext('Copied')
  const partials = {}
  partials.hideHeader = true
  partials.hideFooter = true
  partials.title = props.title
  partials.body = (
    <div className="input-group">
      <input
        id={'share-url-' + props.objectId}
        type="text"
        className="form-control"
        value={props.url}
        readOnly
      />
      <button
        className="btn btn--primary input-group-append"
        data-bs-toggle="button"
        aria-pressed="false"
        autoComplete="off"
        onClick={(e) => copyUrl(e)}
      >
        {clicked ? buttonTextCopied : buttonTextCopy}
      </button>
    </div>
  )

  const copyUrl = () => {
    const copyText = document.getElementById('share-url-'.concat(props.objectId))
    copyText.select()
    document.execCommand('copy')
    setClicked(true)
  }

  return (
    <Modal
      abort={props.abort}
      name={props.name}
      partials={partials}
      keepOpenOnSubmit
    />
  )
}
