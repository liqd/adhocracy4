var React = require('react')
var django = require('django')
var classNames = require('classnames')

function getErrorCount (props) {
  if (props.errors && Object.keys(props.errors).length > 0) {
    let errorCount = Object.keys(props.errors).length
    if (props.errors['paragraphs']) {
      errorCount = errorCount - 1 + Object.keys(props.errors['paragraphs']).length
    }
    return <span className="u-danger"> ({errorCount})</span>
  }
}

const ChapterNavItem = (props) => {
  return (
    <div className="commenting">
      <button
        type="button"
        className={classNames('commenting__content', 'commenting--toc__button', 'btn btn--light', 'btn--small', { 'active': props.active })}
        onClick={props.onClick}>
        {props.index + 1}. {props.name}
        {getErrorCount(props)}
      </button>

      <div className="commenting__actions btn-group" role="group">
        <button
          className="btn btn--light btn--small"
          onClick={props.onMoveUp}
          disabled={!props.onMoveUp}
          title={django.gettext('Move up')}
          type="button">
          <i className="fa fa-chevron-up"
            aria-label={django.gettext('Move up')} />
        </button>
        <button
          className="btn btn--light btn--small"
          onClick={props.onMoveDown}
          disabled={!props.onMoveDown}
          title={django.gettext('Move down')}
          type="button">
          <i className="fa fa-chevron-down"
            aria-label={django.gettext('Move down')} />
        </button>
        <button
          className="btn btn--light btn--small"
          onClick={props.onDelete}
          disabled={!props.onDelete}
          title={django.gettext('Delete')}
          type="button">
          <i className="fas fa-trash-alt"
            aria-label={django.gettext('Delete')} />
        </button>
      </div>
    </div>
  )
}

module.exports = ChapterNavItem
