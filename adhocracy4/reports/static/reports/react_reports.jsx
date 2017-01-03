var api = require('adhocracy4').api
var Modal = require('../../../contrib/static/js/Modal')

var $ = require('jquery')
var React = require('react')
var django = require('django')

var ReportModal = React.createClass({
  getInitialState: function () {
    return {
      report: '',
      showSuccessMessage: false,
      showErrorMessage: false,
      showReportForm: true
    }
  },
  handleTextChange: function (e) {
    this.setState({report: e.target.value})
  },
  resetModal: function () {
    if (!$('#' + this.props.name).is(':visible')) {
      this.setState({
        report: '',
        showSuccessMessage: false,
        showErrorMessage: false,
        showReportForm: true,
        errors: null
      })
    } else {
      setTimeout(this.resetModal, 500)
    }
  },
  closeModal: function () {
    $('#' + this.props.name).modal('hide')
    this.resetModal()
  },
  submitReport: function (e) {
    api.report.submit({
      description: this.state.report,
      content_type: this.props.contentType,
      object_pk: this.props.objectId
    })
      .done(function () {
        this.setState({
          report: '',
          showSuccessMessage: true,
          showReportForm: false,
          showErrorMessage: false
        })
      }.bind(this))
  },
  render: function () {
    let partials = {}
    if (this.state.showSuccessMessage) {
      partials.title = (<span><i className="fa fa-check" /> Thank you! We are taking care of it.</span>)
      partials.hideFooter = true
      partials.bodyClass = 'success'
    } else if (this.state.showReportForm) {
      partials.title = this.props.title
      partials.body = (
        <div className="form-group">
          <textarea rows="5" className="form-control report-message" value={this.state.report}
            placeholder={django.gettext('Your message here')} onChange={this.handleTextChange} />
          {this.state.errors && <span className="help-block">{this.state.errors.description}</span>}
        </div>
      )
    }

    return (
      <Modal
        abort={this.props.abort}
        name={this.props.name}
        closeHandler={this.closeModal}
        submitHandler={this.submitReport}
        action={django.gettext('Send Report')}
        partials={partials}
        dismissOnSubmit={false}
      />
    )
  }
})

module.exports = ReportModal
