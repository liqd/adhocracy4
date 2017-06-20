var React = require('react')
var django = require('django')
var ChapterListItem = require('./ChapterListItem')

const ChapterList = (props) => {
  return (
    <nav aria-label={django.gettext('Chapter navigation')}>
      <ol className="u-list-reset">
        {
          props.chapters.map((chapter, index, arr) =>
            <ChapterListItem
              key={chapter.id || chapter.key}
              name={chapter.name}
              onMoveUp={index !== 0 ? () => { props.onMoveUp(index) } : null}
              onMoveDown={index < arr.length - 1 ? () => { props.onMoveDown(index) } : null}
              onDelete={() => { props.onDelete(index) }}
              onClick={() => { props.onClick(index) }}
              errors={props.errors ? props.errors[index] : {}}
              />
          )
        }
      </ol>

      <p>
        <button
          className="button button--light button--small"
          onClick={props.onChapterAppend}
          type="button">
          <i className="fa fa-plus" /> {django.gettext('Add a new chapter')}
        </button>
      </p>
    </nav>
  )
}

module.exports = ChapterList
