let React = require('react')
let django = require('django')

export const Modal = React.createClass({
  render: function () {
    let dismiss = this.props.dismissOnSubmit ? 'modal' : 'false'
    return (
      <div className="modal fade" id={this.props.name} tabIndex="-1"
        role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div className="modal-dialog modal-lg" role="document">
          <div className="modal-content">
            <div className="modal-header">
              <button className="close" aria-label={this.props.abort}
                data-dismiss="modal" onClick={this.props.closeHandler}>
                <i className="fa fa-times" />
              </button>
            </div>

            <div
              className={'modal-body ' + this.props.partials.bodyClass}>
              <h3 className="modal-title">{this.props.partials.title}</h3>
              {this.props.partials.body}
            </div>
            {!this.props.partials.hideFooter &&
            <div className="modal-footer">
              <div className="row">
                <button className="submit-button" data-dismiss={dismiss}
                  onClick={this.props.submitHandler}>{this.props.action}</button>
              </div>
              <div className="row">
                <button className="cancel-button" data-dismiss="modal"
                  onClick={this.props.closeHandler}>{this.props.abort}</button>
              </div>
            </div>
            }
          </div>
        </div>
      </div>
    )
  }
})

Modal.propTypes = {
  submitHandler: React.PropTypes.func,
  closeHandler: React.PropTypes.func
}

Modal.defaultProps = {
  partials: {},
  abort: django.gettext('Abort'),
  dismissOnSubmit: true
}

module.exports = Modal
