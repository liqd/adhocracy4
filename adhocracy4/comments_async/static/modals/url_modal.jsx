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
    partials.hideHeader = true
    partials.hideFooter = true
    partials.body = (
      <div className="input-group">
        <input id={'share-url-' + this.props.objectId} type="text" className="form-control" value={this.props.url} readOnly />
        <button className="btn btn--transparent input-group-append modal-url-bar-button" data-toggle="button" aria-pressed="false" autoComplete="off" onClick={(e) => this.copyUrl(e)}>{django.gettext('Copy')}</button>
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
