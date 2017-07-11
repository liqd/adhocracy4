var api = require('adhocracy4').api
var React = require('react')
var django = require('django')
var update = require('react-addons-update')
var ChapterNav = require('./ChapterNav')
var ChapterForm = require('./ChapterForm')
var Alert = require('../../contrib/assets/Alert')

const DocumentManagement = React.createClass({
  getInitialState: function () {
    let chapters = this.props.chapters
    if (!chapters || chapters.length === 0) {
      chapters = [
        this.getNewChapter(django.gettext('first chapter'))
      ]
    }

    return {
      chapters: chapters,
      errors: null,
      alert: null,
      editChapterIndex: 0
    }
  },

  maxLocalKey: 0,
  getNextLocalKey: function () {
    /** Get an artificial key for non-committed items.
     *
     *  The key is prefixed to prevent collisions with real database keys.
     */
    this.maxLocalKey++
    return 'local_' + this.maxLocalKey
  },

  /*
  |--------------------------------------------------------------------------
  | Chapter state related handlers
  |--------------------------------------------------------------------------
  */

  getNewChapter: function (name) {
    return {
      name: name,
      key: this.getNextLocalKey(),
      paragraphs: []
    }
  },

  handleChapterMoveUp: function (index) {
    const value = this.state.chapters[index]
    const diff = {$splice: [[index, 1], [index - 1, 0, value]]}
    let editChapterIndex = this.state.editChapterIndex
    if (index === editChapterIndex) {
      editChapterIndex--
    } else if (index - 1 === editChapterIndex) {
      editChapterIndex++
    }
    this.setState({
      chapters: update(this.state.chapters, diff),
      editChapterIndex: editChapterIndex
    })
  },

  handleChapterMoveDown: function (index) {
    const value = this.state.chapters[index]
    const diff = {$splice: [[index, 1], [index + 1, 0, value]]}
    let editChapterIndex = this.state.editChapterIndex
    if (index === editChapterIndex) {
      editChapterIndex++
    } else if (index + 1 === editChapterIndex) {
      editChapterIndex--
    }
    this.setState({
      chapters: update(this.state.chapters, diff),
      editChapterIndex: editChapterIndex
    })
  },

  handleChapterDelete: function (index) {
    const diff = {$splice: [[index, 1]]}
    let editChapterIndex = this.state.editChapterIndex
    if (index < editChapterIndex) {
      editChapterIndex--
    } else if (index === editChapterIndex) {
      editChapterIndex = 0
    }
    this.setState({
      chapters: update(this.state.chapters, diff),
      editChapterIndex: editChapterIndex
    })
  },

  handleChapterAppend: function () {
    const newChapter = this.getNewChapter(django.gettext('new chapter'))
    const diff = {$push: [newChapter]}
    this.setState({
      chapters: update(this.state.chapters, diff)
    })
  },

  handleChapterNameChange: function (index, name) {
    const diff = {}
    diff[index] = {
      $merge: {
        name: name
      }
    }
    this.setState({
      chapters: update(this.state.chapters, diff)
    })
  },

  handleChapterEdit: function (index) {
    this.setState({
      editChapterIndex: index
    })
    if (this.titleInput) {
      this.titleInput.focus()
    }
  },

  /*
  |--------------------------------------------------------------------------
  | Paragraph state related handlers
  |--------------------------------------------------------------------------
  */

  getNewParagraph: function (name = '', text = '') {
    return {
      name: name,
      text: text,
      key: this.getNextLocalKey()
    }
  },

  handleParagraphAppend: function (chapterIndex) {
    const newParagraph = this.getNewParagraph()
    const diff = {}
    diff[chapterIndex] = {
      paragraphs: {
        $push: [newParagraph]
      }
    }
    this.setState({
      chapters: update(this.state.chapters, diff)
    })
  },

  handleParagraphMoveUp: function (chapterIndex, paragraphIndex) {
    const value = this.state.chapters[chapterIndex].paragraphs[paragraphIndex]
    const diff = {}
    diff[chapterIndex] = {
      paragraphs: {
        $splice: [[paragraphIndex, 1], [paragraphIndex - 1, 0, value]]
      }
    }
    this.setState({
      chapters: update(this.state.chapters, diff)
    })
  },

  handleParagraphMoveDown: function (chapterIndex, paragraphIndex) {
    const value = this.state.chapters[chapterIndex].paragraphs[paragraphIndex]
    const diff = {}
    diff[chapterIndex] = {
      paragraphs: {
        $splice: [[paragraphIndex, 1], [paragraphIndex + 1, 0, value]]
      }
    }
    this.setState({
      chapters: update(this.state.chapters, diff)
    })
  },

  handleParagraphDelete: function (chapterIndex, paragraphIndex) {
    const diff = {}
    diff[chapterIndex] = {
      paragraphs: {
        $splice: [[paragraphIndex, 1]]
      }
    }
    this.setState({
      chapters: update(this.state.chapters, diff)
    })
  },

  handleParagraphNameChange: function (chapterIndex, paragraphIndex, name) {
    const diff = {}
    diff[chapterIndex] = {paragraphs: []}
    diff[chapterIndex]['paragraphs'][paragraphIndex] = {
      $merge: {
        name: name
      }
    }
    this.setState({
      chapters: update(this.state.chapters, diff)
    })
  },

  handleParagraphTextChange: function (chapterIndex, paragraphIndex, text) {
    const diff = {}
    diff[chapterIndex] = {paragraphs: []}
    diff[chapterIndex]['paragraphs'][paragraphIndex] = {
      $merge: {
        text: text
      }
    }
    this.setState({
      chapters: update(this.state.chapters, diff)
    })
  },

  removeAlert: function () {
    this.setState({
      alert: null
    })
  },

  handleSubmit: function (e) {
    if (e) {
      e.preventDefault()
    }

    const submitData = {
      urlReplaces: {moduleId: this.props.module},
      chapters: this.state.chapters
    }

    api.document.add(submitData)
      .done((data) => {
        this.setState({
          alert: {
            type: 'success',
            message: django.gettext('The document has been updated.')
          },
          errors: [],
          chapters: data.chapters
        })
      })
      .fail((xhr, status, err) => {
        let errors = []
        if (xhr.responseJSON && 'chapters' in xhr.responseJSON) {
          errors = xhr.responseJSON.chapters
        }

        this.setState({
          alert: {
            type: 'danger',
            message: django.gettext('The document could not be updated.')
          },
          errors: errors
        })
      })
  },

  render: function () {
    const chapterIndex = this.state.editChapterIndex
    const chapterErrors = this.state.errors && this.state.errors[chapterIndex] ? this.state.errors[chapterIndex] : {}

    return (
      <form onSubmit={this.handleSubmit} onChange={this.removeAlert}>

        <h2>{django.gettext('Contents')}</h2>
        <ChapterNav
          chapters={this.state.chapters}
          activeChapter={this.state.chapters[chapterIndex]}
          onMoveUp={this.handleChapterMoveUp}
          onMoveDown={this.handleChapterMoveDown}
          onDelete={this.handleChapterDelete}
          onChapterAppend={this.handleChapterAppend}
          onClick={this.handleChapterEdit}
          errors={this.state.errors}
        />

        <h2>{django.gettext('Edit chapter')}</h2>
        <ChapterForm
          titleRef={(el) => { this.titleInput = el }}
          onChapterNameChange={(name) => { this.handleChapterNameChange(chapterIndex, name) }}
          onParagraphNameChange={(paragraphIndex, name) => { this.handleParagraphNameChange(chapterIndex, paragraphIndex, name) }}
          onParagraphTextChange={(paragraphIndex, text) => { this.handleParagraphTextChange(chapterIndex, paragraphIndex, text) }}
          onParagraphAppend={(paragraphIndex) => { this.handleParagraphAppend(chapterIndex, paragraphIndex) }}
          onParagraphMoveUp={(paragraphIndex) => { this.handleParagraphMoveUp(chapterIndex, paragraphIndex) }}
          onParagraphMoveDown={(paragraphIndex) => { this.handleParagraphMoveDown(chapterIndex, paragraphIndex) }}
          onParagraphDelete={(paragraphIndex) => { this.handleParagraphDelete(chapterIndex, paragraphIndex) }}
          config={this.props.config}
          chapter={this.state.chapters[chapterIndex]}
          errors={chapterErrors}
        />

        <Alert onClick={this.removeAlert} {...this.state.alert} />

        <button type="submit" className="button button--primary">{django.gettext('Save')}</button>
      </form>
    )
  }
})

module.exports = DocumentManagement
