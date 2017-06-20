var React = require('react')
var django = require('django')

function getErrorCount (props) {
  if (props.errors && Object.keys(props.errors).length > 0) {
    let errorCount = Object.keys(props.errors).length
    if (props.errors['paragraphs']) {
      errorCount = errorCount - 1 + Object.keys(props.errors['paragraphs']).length
    }
    return <span className="errorcount"> ({errorCount})</span>
  }
}

const ChapterListItem = (props) => {
  return (
    <div className="commenting">
      <button className="commenting__content commenting--toc__button button button--light button--small" type="button" onClick={props.onClick}>
        {props.name}
        {getErrorCount(props)}
      </button>

      <div className="commenting__actions button-group">
        <button
          className="button button--light button--small"
          onClick={props.onMoveUp}
          disabled={!props.onMoveUp}
          title={django.gettext('Move up')}
          type="button">
          <i className="fa fa-chevron-up"
            aria-label={django.gettext('Move up')} />
        </button>
        <button
          className="button button--light button--small"
          onClick={props.onMoveDown}
          disabled={!props.onMoveDown}
          title={django.gettext('Move down')}
          type="button">
          <i className="fa fa-chevron-down"
            aria-label={django.gettext('Move down')} />
        </button>
        <button
          className="button button--light button--small"
          onClick={props.onDelete}
          title={django.gettext('Delete')}
          type="button">
          <i className="fa fa-trash"
            aria-label={django.gettext('Delete')} />
        </button>
      </div>
    </div>
  )
}

module.exports = ChapterListItem
