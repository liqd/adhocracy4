var React = require('react')
var django = require('django')
var ChapterListItem = require('./ChapterListItem')
var FlipMove = require('react-flip-move')

const ChapterList = (props) => {
  return (
    <nav aria-label={django.gettext('Chapter navigation')}>
      <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)" typeName="ol" className="u-list-reset">
        {
          props.chapters.map((chapter, index, arr) =>
            <li key={chapter.id || chapter.key}>
              <ChapterListItem
                name={chapter.name}
                onMoveUp={index !== 0 ? () => { props.onMoveUp(index) } : null}
                onMoveDown={index < arr.length - 1 ? () => { props.onMoveDown(index) } : null}
                onDelete={() => { props.onDelete(index) }}
                onClick={() => { props.onClick(index) }}
                errors={props.errors ? props.errors[index] : {}}
                />
            </li>
          )
        }
      </FlipMove>

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
