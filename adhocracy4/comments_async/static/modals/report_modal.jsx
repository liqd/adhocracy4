import $ from 'jquery'
import React from 'react'
import django from 'django'

import api from '../../../static/api'
import Modal from './modal'

export default class ReportModal extends React.Component {
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
    const partials = {}
    if (this.state.showSuccessMessage) {
      partials.title = (<span><i className="fas fa-check" aria-hidden="true" /> {django.gettext('Thanks for the feedback. It will be checked by the moderators as soon as possible.')}</span>)
      partials.hideFooter = true
      partials.bodyClass = 'success'
    } else if (this.state.showReportForm) {
      partials.title = this.props.title
      partials.body = (
        <div className="form-group">
          <textarea
            rows="5" className="form-control report-message" value={this.state.report}
            placeholder={django.gettext('Your message')} onChange={this.handleTextChange.bind(this)}
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
        action={django.gettext('Send Report')}
        partials={partials}
        dismissOnSubmit={false}
      />
    )
  }
}
