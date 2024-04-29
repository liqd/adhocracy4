import React from 'react'
import django from 'django'

const Modal = (props) => {
  const dismiss = props.dismissOnSubmit ? 'modal' : 'false'
  const abortStr = props.abort || django.gettext('Abort')
  const bodyCssClass = props.partials.bodyClass || ''

  return (
    <div
      className="modal fade"
      id={props.name}
      tabIndex="-1"
      role="dialog"
      aria-label={props.partials.title || 'Modal'}
      aria-hidden="true"
    >
      <div
        className="modal-dialog modal-dialog-centered modal-lg"
        role="document"
      >
        <div className="modal-content">
          <div className="modal-header">
            {props.partials.title && (
              <h2 className="u-no-margin-bottom u-spacer-top-one-half">
                {props.partials.title}
              </h2>)}
            <button
              className="close"
              aria-label={abortStr}
              data-bs-dismiss="modal"
              onClick={props.handleClose}
            >
              <i className="fa fa-times" aria-hidden="true" />
            </button>
          </div>

          <div
            className={'modal-body ' + bodyCssClass}
          >
            <div className="u-spacer-bottom">
              {props.partials.description}
            </div>
            {props.partials.body}
          </div>
          {!props.partials.hideFooter &&
            <div className="modal-footer">
              <button
                className="submit-button"
                data-bs-dismiss={dismiss}
                onClick={props.handleSubmit}
              >
                {props.action}
              </button>
              <button
                className="cancel-button"
                data-bs-dismiss="modal"
                onClick={props.handleClose}
              >
                {abortStr}
              </button>
            </div>}
        </div>
      </div>
    </div>
  )
}

module.exports = Modal
