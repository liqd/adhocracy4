const React = require('react')
const PropTypes = require('prop-types')
const django = require('django')

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
              data-dismiss="modal" onClick={props.handleClose}
            >
              <i className="fa fa-times" />
            </button>
          </div>

          <div
            className={'modal-body ' + props.partials.bodyClass}
          >
            <h3 className="modal-title">{props.partials.title}</h3>
            {props.partials.body}
          </div>
          {!props.partials.hideFooter &&
            <div className="modal-footer">
              <div className="row">
                <button
                  className="submit-button" data-dismiss={dismiss}
                  onClick={props.handleSubmit}
                >{props.action}
                </button>
              </div>
              <div className="row">
                <button
                  className="cancel-button" data-dismiss="modal"
                  onClick={props.handleClose}
                >{props.abort}
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
