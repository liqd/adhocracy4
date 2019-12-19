const api = require('../../../static/api')
const Modal = require('../../../static/Modal')

const $ = require('jquery')
const React = require('react')
const django = require('django')

class ReportModal extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      report: '',
      showSuccessMessage: false,
      showErrorMessage: false,
      showReportForm: true
    }
  }

  handleTextChange (e) {
    this.setState({ report: e.target.value })
  }

  resetModal () {
    if (!$('#' + this.props.name).is(':visible')) {
      this.setState({
        report: '',
        showSuccessMessage: false,
        showErrorMessage: false,
        showReportForm: true,
        errors: null
      })
    } else {
      setTimeout(this.resetModal.bind(this), 500)
    }
  }

  closeModal () {
    $('#' + this.props.name).modal('hide')
    this.resetModal()
  }

  submitReport () {
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
  }

  render () {
    const thankyouText = django.gettext('Thank you! We are taking care of it.')
    const placeholderText = django.gettext('Your message')
    const sendReportTag = django.gettext('Send Report')
    const partials = {}
    if (this.state.showSuccessMessage) {
      partials.title = (<span><i className="fa fa-check" /> {thankyouText}</span>)
      partials.hideFooter = true
      partials.bodyClass = 'success'
    } else if (this.state.showReportForm) {
      partials.title = this.props.title
      partials.body = (
        <div className="form-group">
          <textarea
            rows="5" className="form-control report-message" value={this.state.report}
            placeholder={placeholderText} onChange={this.handleTextChange.bind(this)}
          />
          {this.state.errors && <span className="help-block">{this.state.errors.description}</span>}
        </div>
      )
    }

    return (
      <Modal
        abort={this.props.abort}
        name={this.props.name}
        handleClose={this.closeModal.bind(this)}
        handleSubmit={this.submitReport.bind(this)}
        action={sendReportTag}
        partials={partials}
        dismissOnSubmit={false}
      />
    )
  }
}

module.exports = ReportModal
