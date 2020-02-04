import React from 'react'
import django from 'django'
import PropTypes from 'prop-types'

const Modal = (props) => {
  const dismiss = props.dismissOnSubmit ? 'modal' : 'false'
  return (
    <div
      className="modal fade" id={props.name} tabIndex="-1"
      role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"
    >
      <div className="modal-dialog modal-lg modal-dialog-centered" role="document">
        <div className="modal-content">
          <span className="modal--close pt-3 pr-3">
            <button
              className="close" aria-label={props.abort}
              data-dismiss="modal" onClick={props.handleClose}
            >
              <i className="fas fa-times" />
            </button>
          </span>
          {!props.partials.hideHeader &&
            <div className="modal-header">
              <h4 className="modal-title mt-0">{props.partials.title}</h4>
            </div>}
          {props.partials.body &&
            <div
              className={'modal-body ' + (props.partials.bodyClass || '')}
            >
              {props.partials.body}
            </div>}
          {!props.partials.hideFooter &&
            <div className="modal-footer">
              <button
                className="mx-auto mx-lg-4 cancel-button" data-dismiss="modal"
                onClick={props.handleClose}
              >{props.abort}
              </button>
              <button
                className="mx-auto mx-lg-0 submit-button" data-dismiss={dismiss}
                onClick={props.handleSubmit}
              >{props.action}
              </button>
            </div>}
        </div>
      </div>
    </div>
  )
}

Modal.propTypes = {
  handleSubmit: PropTypes.func,
  handleClose: PropTypes.func
}

Modal.defaultProps = {
  partials: {},
  abort: django.gettext('Abort'),
  dismissOnSubmit: true
}

export default Modal
