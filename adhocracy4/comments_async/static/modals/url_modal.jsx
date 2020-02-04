import React from 'react'
import django from 'django'

import Modal from './modal'

export default class UrlModal extends React.Component {
  copyUrl () {
    var copyText = document.getElementById('share-url-'.concat(this.props.objectId))
    copyText.select()
    document.execCommand('copy')
  }

  render () {
    const partials = {}
    partials.title = django.gettext('Share comment URL')
    partials.hideFooter = true
    partials.body = (
      <div className="form-inline">
        <input id={'share-url-' + this.props.objectId} type="text" className="modal-url-bar-input mb-0" value={this.props.url} readOnly />
        <button className="btn btn--transparent modal-url-bar-button ml-auto" onClick={(e) => this.copyUrl(e)}>{django.gettext('Copy')}</button>
      </div>
    )

    return (
      <Modal
        abort={this.props.abort}
        name={this.props.name}
        partials={partials}
        dismissOnSubmit={false}
      />
    )
  }
}
