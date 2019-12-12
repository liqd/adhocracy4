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
    partials.hideFooter = true
    partials.hideHeader = true
    partials.body = (
      <div className="d-flex mb-3 mb-md-5 modal-url-bar">
        <input id={'share-url-' + this.props.objectId} type="text" className="text-left modal-url-bar-input pl-3" value={this.props.url} readOnly />
        <button className="btn btn--upper btn--transparent modal-url-bar-button p-0 ml-auto mr-3" onClick={(e) => this.copyUrl(e)}>{django.gettext('Copy')}</button>
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
