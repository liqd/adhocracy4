import React from 'react'
import PropTypes from 'prop-types'
import django from 'django'

export const Modal = (props) => {
  const dismiss = props.dismissOnSubmit ? 'modal' : 'false'
  return (
    <div
      className="modal fade" id={props.name} tabIndex="-1"
      role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"
    >
      <div className="modal-dialog modal-lg" role="document">
        <div className="modal-content">
          <div className="modal-header">
            <button
              className="close" aria-label={props.abort}
              data-bs-dismiss="modal" onClick={props.handleClose}
            >
              <i className="fa fa-times" />
            </button>
          </div>

          <div
            className={'modal-body ' + props.partials.bodyClass}
          >
            <h3 className="modal-title u-first-heading">{props.partials.title}</h3>
            {props.partials.body}
          </div>
          {!props.partials.hideFooter &&
            <div className="modal-footer">
              <div>
                <button
                  className="cancel-button" data-bs-dismiss="modal"
                  onClick={props.handleClose}
                >{props.abort}
                </button>
              </div>
              <div>
                <button
                  className="submit-button" data-bs-dismiss={dismiss}
                  onClick={props.handleSubmit}
                >{props.action}
                </button>
              </div>
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

module.exports = Modal
