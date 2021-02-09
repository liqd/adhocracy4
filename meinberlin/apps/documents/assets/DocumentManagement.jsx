const api = require('adhocracy4').api
const React = require('react')
const django = require('django')
const dashboard = require('adhocracy4/adhocracy4/dashboard/assets/dashboard')
const update = require('immutability-helper')
const ChapterNav = require('./ChapterNav')
const ChapterForm = require('./ChapterForm')
const Alert = require('../../contrib/assets/Alert')

class DocumentManagement extends React.Component {
  constructor (props) {
    super(props)
    this.maxLocalKey = 0

    let chapters = this.props.chapters
    if (!chapters || chapters.length === 0) {
      chapters = [
        this.getNewChapter(django.gettext('first chapter'))
      ]
    }

    this.state = {
      chapters: chapters,
      errors: null,
      alert: null,
      editChapterIndex: 0
    }
  }

  getNextLocalKey () {
    /** Get an artificial key for non-committed items.
     *
     *  The key is prefixed to prevent collisions with real database keys.
     */
    this.maxLocalKey++
    return 'local_' + this.maxLocalKey
  }

  /*
  |--------------------------------------------------------------------------
  | Chapter state related handlers
  |--------------------------------------------------------------------------
  */

  getNewChapter (name) {
    return {
      name: name,
      key: this.getNextLocalKey(),
      paragraphs: []
    }
  }

  handleChapterMoveUp (index) {
    const value = this.state.chapters[index]
    const diff = { $splice: [[index, 1], [index - 1, 0, value]] }
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
  }

  handleChapterMoveDown (index) {
    const value = this.state.chapters[index]
    const diff = { $splice: [[index, 1], [index + 1, 0, value]] }
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
  }

  handleChapterDelete (index) {
    const diff = { $splice: [[index, 1]] }
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
  }

  handleChapterAppend () {
    const newChapter = this.getNewChapter(django.gettext('new chapter'))
    const newChapterIndex = this.state.chapters.length

    const diff = { $push: [newChapter] }
    this.setState({
      chapters: update(this.state.chapters, diff),
      editChapterIndex: newChapterIndex
    }, () => { this.focusOnChapter(newChapter) })
  }

  handleChapterNameChange (index, name) {
    const diff = {}
    diff[index] = {
      $merge: {
        name: name
      }
    }
    this.setState({
      chapters: update(this.state.chapters, diff)
    })
  }

  handleChapterEdit (index) {
    const chapter = this.state.chapters[index]
    this.setState({
      editChapterIndex: index
    }, () => { this.focusOnChapter(chapter) })
  }

  focusOnChapter (chapter) {
    const key = chapter.id || chapter.key
    const id = 'id_chapters-' + key + '-name'
    window.document.getElementById(id).focus()
  }

  /*
  |--------------------------------------------------------------------------
  | Paragraph state related handlers
  |--------------------------------------------------------------------------
  */

  getNewParagraph (name = '', text = '') {
    return {
      name: name,
      text: text,
      key: this.getNextLocalKey()
    }
  }

  handleParagraphAppend (chapterIndex) {
    const newParagraph = this.getNewParagraph()

    const diff = {}
    diff[chapterIndex] = {
      paragraphs: {
        $push: [newParagraph]
      }
    }

    this.setState({
      chapters: update(this.state.chapters, diff)
    }, () => { this.focusOnParagraph(newParagraph) })
  }

  handleParagraphMoveUp (chapterIndex, paragraphIndex) {
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
  }

  handleParagraphMoveDown (chapterIndex, paragraphIndex) {
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
  }

  handleParagraphDelete (chapterIndex, paragraphIndex) {
    const diff = {}
    diff[chapterIndex] = {
      paragraphs: {
        $splice: [[paragraphIndex, 1]]
      }
    }
    this.setState({
      chapters: update(this.state.chapters, diff)
    })
  }

  handleParagraphNameChange (chapterIndex, paragraphIndex, name) {
    const diff = {}
    diff[chapterIndex] = { paragraphs: [] }
    diff[chapterIndex].paragraphs[paragraphIndex] = {
      $merge: {
        name: name
      }
    }
    this.setState({
      chapters: update(this.state.chapters, diff)
    })
  }

  handleParagraphTextChange (chapterIndex, paragraphIndex, text) {
    const diff = {}
    diff[chapterIndex] = { paragraphs: [] }
    diff[chapterIndex].paragraphs[paragraphIndex] = {
      $merge: {
        text: text
      }
    }
    this.setState({
      chapters: update(this.state.chapters, diff),
      // Workaround missing change events when using CKEDITOR
      alert: null
    })
  }

  focusOnParagraph (paragraph) {
    const key = paragraph.id || paragraph.key
    const id = 'id_paragraphs-' + key + '-name'
    window.document.getElementById(id).focus()
  }

  /*
  |--------------------------------------------------------------------------
  | Document form and submit logic
  |--------------------------------------------------------------------------
  */

  removeAlert () {
    this.setState({
      alert: null
    })
  }

  handleSubmit (e) {
    if (e) {
      e.preventDefault()
    }

    const submitData = {
      urlReplaces: { moduleId: this.props.module },
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
        if (this.props.reloadOnSuccess) {
          dashboard.updateDashboard()
        }
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
  }

  render () {
    const chapterIndex = this.state.editChapterIndex
    const chapterErrors = this.state.errors && this.state.errors[chapterIndex] ? this.state.errors[chapterIndex] : {}
    const chapter = this.state.chapters[chapterIndex]
    const key = chapter.id || chapter.key

    return (
      <form onSubmit={this.handleSubmit.bind(this)} onChange={this.removeAlert.bind(this)}>

        <h2>{django.gettext('Contents')}</h2>
        <ChapterNav
          chapters={this.state.chapters}
          activeChapter={this.state.chapters[chapterIndex]}
          onMoveUp={this.handleChapterMoveUp.bind(this)}
          onMoveDown={this.handleChapterMoveDown.bind(this)}
          onDelete={this.handleChapterDelete.bind(this)}
          onChapterAppend={this.handleChapterAppend.bind(this)}
          onClick={this.handleChapterEdit.bind(this)}
          errors={this.state.errors}
        />

        <h2>{django.gettext('Edit chapter')}</h2>
        <ChapterForm
          id={key}
          onChapterNameChange={(name) => { this.handleChapterNameChange(chapterIndex, name) }}
          onParagraphNameChange={(paragraphIndex, name) => { this.handleParagraphNameChange(chapterIndex, paragraphIndex, name) }}
          onParagraphTextChange={(paragraphIndex, text) => { this.handleParagraphTextChange(chapterIndex, paragraphIndex, text) }}
          onParagraphAppend={() => { this.handleParagraphAppend(chapterIndex) }}
          onParagraphMoveUp={(paragraphIndex) => { this.handleParagraphMoveUp(chapterIndex, paragraphIndex) }}
          onParagraphMoveDown={(paragraphIndex) => { this.handleParagraphMoveDown(chapterIndex, paragraphIndex) }}
          onParagraphDelete={(paragraphIndex) => { this.handleParagraphDelete(chapterIndex, paragraphIndex) }}
          config={this.props.config}
          chapter={chapter}
          errors={chapterErrors}
        />

        <Alert onClick={this.removeAlert.bind(this)} {...this.state.alert} />

        <button type="submit" className="btn btn--primary">{django.gettext('Save')}</button>
      </form>
    )
  }
}

module.exports = DocumentManagement
