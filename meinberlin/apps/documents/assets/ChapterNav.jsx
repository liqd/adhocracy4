const React = require('react')
const FlipMove = require('react-flip-move').default
const django = require('django')
const ChapterNavItem = require('./ChapterNavItem')

const ChapterNav = (props) => {
  const activeKey = props.activeChapter.id || props.activeChapter.key
  return (
    <nav aria-label={django.gettext('Chapter navigation')}>
      <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)" typeName="ol" className="u-list-reset">
        {
          props.chapters.map((chapter, index, arr) => {
            const key = chapter.id || chapter.key
            return (
              <li key={key}>
                <ChapterNavItem
                  name={chapter.name}
                  index={index}
                  onMoveUp={index !== 0 ? () => { props.onMoveUp(index) } : null}
                  onMoveDown={index < arr.length - 1 ? () => { props.onMoveDown(index) } : null}
                  onDelete={arr.length > 1 ? () => { props.onDelete(index) } : null}
                  onClick={() => { props.onClick(index) }}
                  errors={props.errors ? props.errors[index] : {}}
                  active={key === activeKey}
                />
              </li>
            )
          })
        }
      </FlipMove>

      <p>
        <button
          className="btn btn--light btn--small"
          onClick={props.onChapterAppend}
          type="button"
        >
          <i className="fa fa-plus" /> {django.gettext('Add a new chapter')}
        </button>
      </p>
    </nav>
  )
}

module.exports = ChapterNav
