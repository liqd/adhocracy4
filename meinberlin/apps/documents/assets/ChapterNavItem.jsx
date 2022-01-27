const React = require('react')
const django = require('django')
const classNames = require('classnames')
const moveUpStr = django.gettext('Move up')
const moveDownStr = django.gettext('Move down')
const deleteStr = django.gettext('Delete')

function getErrorCount (props) {
  if (props.errors && Object.keys(props.errors).length > 0) {
    let errorCount = Object.keys(props.errors).length
    if (props.errors.paragraphs) {
      errorCount = errorCount - 1 + Object.keys(props.errors.paragraphs).length
    }
    return <span className="u-danger"> ({errorCount})</span>
  }
}

const ChapterNavItem = (props) => {
  return (
    <div className="commenting">
      <button
        type="button"
        className={classNames('commenting__content', 'commenting--toc__button', 'btn btn--light', 'btn--small', { active: props.active })}
        onClick={props.onClick}
      >
        {props.index + 1}. {props.name}
        {getErrorCount(props)}
      </button>

      <div className="commenting__actions btn-group" role="group">
        <button
          className="btn btn--light btn--small"
          onClick={props.onMoveUp}
          disabled={!props.onMoveUp}
          title={moveUpStr}
          type="button"
        >
          <i
            className="fa fa-chevron-up"
            aria-label={moveUpStr}
          />
        </button>
        <button
          className="btn btn--light btn--small"
          onClick={props.onMoveDown}
          disabled={!props.onMoveDown}
          title={moveDownStr}
          type="button"
        >
          <i
            className="fa fa-chevron-down"
            aria-label={moveDownStr}
          />
        </button>
        <button
          className="btn btn--light btn--small"
          onClick={props.onDelete}
          disabled={!props.onDelete}
          title={deleteStr}
          type="button"
        >
          <i
            className="fas fa-trash-alt"
            aria-label={deleteStr}
          />
        </button>
      </div>
    </div>
  )
}

module.exports = ChapterNavItem
