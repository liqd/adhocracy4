var React = require('react')
var django = require('django')
var ChapterListItem = require('./ChapterListItem')

const ChapterList = React.createClass({
  render: function () {
    return (
      <section>
        {
          this.props.chapters.map((chapter, index, arr) =>
            <ChapterListItem
              key={chapter.id || chapter.key}
              name={chapter.name}
              onMoveUp={index !== 0 ? () => { this.props.onMoveUp(index) } : null}
              onMoveDown={index < arr.length - 1 ? () => { this.props.onMoveDown(index) } : null}
              onDelete={() => { this.props.onDelete(index) }}
              onClick={() => { this.props.onClick(index) }}
              />
          )
        }

        <p>
          <button
            className="button button--light"
            onClick={this.props.onChapterAppend}
            type="button">
            <i className="fa fa-plus" /> {django.gettext('Add a new chapter')}
          </button>
        </p>
      </section>
    )
  }
})

module.exports = ChapterList
