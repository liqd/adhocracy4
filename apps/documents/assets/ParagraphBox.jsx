var api = require('adhocracy4').api
var Paragraph = require('./Paragraph.jsx')
var React = require('react')
var ReactDOM = require('react-dom')
var update = require('react-addons-update')
var django = require('django')
var FlipMove = require('react-flip-move')

var ParagraphBox = React.createClass({
  getInitialState: function () {
    return {
      id: this.props.id,
      name: this.props.name,
      paragraphs: this.props.paragraphs,
      nameErrors: [],
      paragraphsErrors: [],
      maxParagraphKey: 0,
      successMessage: ''
    }
  },
  handleDocumentNameChange: function (e) {
    this.setState({
      name: e.target.value
    })
  },
  getNextParagraphKey: function () {
    /** Get an artifical key for non-commited paragraphs.
     *
     *  Prefix to prevent collisions with real database keys;
     */
    var paragraphKey = 'local_' + (this.state.maxParagraphKey + 1)
    this.setState({maxParagraphKey: this.state.maxParagraphKey + 1})
    return paragraphKey
  },
  getNewParagraph: function (name, text) {
    var newParagraph = {}
    newParagraph['name'] = name
    newParagraph['text'] = text
    newParagraph['paragraph_key'] = this.getNextParagraphKey()
    return newParagraph
  },
  deleteParagraph: function (index) {
    var newArray = update(this.state.paragraphs, {$splice: [[index, 1]]})
    this.setState({
      paragraphs: newArray
    })
  },
  moveParagraphUp: function (index) {
    var paragraph = this.state.paragraphs[index]
    var paragraphs = update(this.state.paragraphs, {
      $splice: [[index, 1], [index - 1, 0, paragraph]]
    })
    this.setState({
      paragraphs: paragraphs
    })
  },
  moveParagraphDown: function (index) {
    var paragraph = this.state.paragraphs[index]
    var paragraphs = update(this.state.paragraphs, {
      $splice: [[index, 1], [index + 1, 0, paragraph]]
    })
    this.setState({
      paragraphs: paragraphs
    })
  },
  addParagraphBeforeIndex: function (index) {
    var newParagraph = this.getNewParagraph('', '')
    var newArray = update(this.state.paragraphs, {$splice: [[index, 0, newParagraph]]})
    this.setState({
      paragraphs: newArray
    })
  },
  appendParagraph: function () {
    var newParagraph = this.getNewParagraph('', '')
    var newArray = update(this.state.paragraphs, {$push: [newParagraph]})
    this.setState({
      paragraphs: newArray
    })
  },
  updateParagraphName: function (index, name) {
    var diff = {}
    diff[index] = {$merge: {name: name}}
    this.setState({
      paragraphs: update(this.state.paragraphs, diff)
    })
  },
  updateParagraphText: function (index, text) {
    var diff = {}
    diff[index] = {$merge: {text: text}}
    this.setState({
      paragraphs: update(this.state.paragraphs, diff)
    })
  },
  submitDocument: function (e) {
    if (e) {
      e.preventDefault()
    }

    var submitData = {
      urlReplaces: {moduleId: this.props.module}
    }
    submitData['name'] = this.state.name
    this.state.paragraphs.forEach(function (val, index) { val.weight = index })
    submitData['paragraphs'] = this.state.paragraphs

    var promise = null

    if (typeof this.state.id !== 'undefined') {
      promise = this.updateDocument(submitData, this.state.id)
    } else {
      promise = this.createDocument(submitData)
    }

    return promise
      .done(function () {
        setTimeout(function () {
          this.setState({
            successMessage: ''
          })
        }.bind(this), 1500)
      }.bind(this))
      .fail(function (xhr, status, err) {
        this.setState({
          nameErrors: xhr.responseJSON.name || [],
          paragraphsErrors: xhr.responseJSON.paragraphs || []
        })
      }.bind(this))
  },
  updateDocument: function (submitData, id) {
    return api.document.change(submitData, id)
      .done(function (data) {
        this.setState({
          name: data.name,
          paragraphs: data.paragraphs,
          successMessage: django.gettext('Your document has been updated.')
        })
      }.bind(this))
  },
  createDocument: function (submitData) {
    return api.document.add(submitData)
      .done(function (data) {
        this.setState({
          id: data.id,
          name: data.name,
          paragraphs: data.paragraphs,
          successMessage: django.gettext('Your document has been saved.')
        })
      }.bind(this))
  },
  getErrors: function (index) {
    return this.state.paragraphsErrors[index]
  },
  render: function () {
    return (
      <form onSubmit={this.submitDocument}>
        <div className="form-group">
          <label>
            {django.gettext('Title')}
            <input
              type="text"
              defaultValue={this.state.name}
              onChange={this.handleDocumentNameChange} />
          </label>
          {this.state.nameErrors.length ? <ul className="errorlist">
            {this.state.nameErrors.map(function (msg, index) {
              return <li key={msg}>{msg}</li>
            })}
          </ul> : null}
        </div>
        <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)">
          {
            this.state.paragraphs.map(function (paragraph, index) {
              return (
                <Paragraph
                  key={paragraph.paragraph_key || paragraph.id}
                  id={paragraph.paragraph_key || paragraph.id}
                  index={index}
                  paragraph={paragraph}
                  errors={this.getErrors(index)}
                  config={this.props.config}
                  deleteParagraph={this.deleteParagraph}
                  moveParagraphUp={index !== 0 ? this.moveParagraphUp : null}
                  moveParagraphDown={index < this.state.paragraphs.length - 1 ? this.moveParagraphDown : null}
                  addParagraphBeforeIndex={this.addParagraphBeforeIndex}
                  updateParagraphName={this.updateParagraphName}
                  updateParagraphText={this.updateParagraphText}
                />
              )
            }.bind(this))
          }
        </FlipMove>
        <button
          className="button button--full"
          onClick={this.appendParagraph}
          type="button">
          <i className="fa fa-plus" /> {django.gettext('Add a new paragraph')}
        </button>
        { this.state.successMessage
          ? <p className="alert alert-success ">
            {this.state.successMessage}
          </p> : null
        }
        <button type="submit" className="button button--primary">{django.gettext('Save')}</button>
      </form>
    )
  }
})

module.exports.renderParagraphs = function (mountpoint) {
  let el = document.getElementById(mountpoint)

  let module = el.getAttribute('data-module')
  let doc = JSON.parse(el.getAttribute('data-document'))
  let config = JSON.parse(el.getAttribute('data-config'))

  ReactDOM.render(<ParagraphBox
    name={doc.name}
    id={doc.id}
    module={module}
    paragraphs={doc.paragraphs}
    config={config} />,
    el
  )
}
