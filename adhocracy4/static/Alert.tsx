import React, { useRef, useEffect } from 'react'
import django from 'django'

interface AlertProps {
  type?: 'info' | 'success' | 'warning' | 'danger';
  title?: string;
  message?: string;
  onClick?: () => void;
  timeInMs?: number;
}

const Alert: React.FC<AlertProps> = ({
  type = 'info',
  title,
  message,
  onClick = () => {},
  timeInMs
}) => {
  const timer = useRef<NodeJS.Timeout>(setTimeout(() => 0))
  const closeTag = django.gettext('Close')

  useEffect(() => {
    if (timeInMs) {
      timer.current = setTimeout(onClick, timeInMs)
      return () => {
        if (timer.current) {
          clearTimeout(timer.current)
        }
      }
    }
  }, [timeInMs, onClick])

  // Only check for message now since type has a default
  if (!message) {
    return null
  }

  // Use alert role for danger/warning, status for others
  const ariaRole = ['danger', 'warning'].includes(type) ? 'alert' : 'status'

  return (
    <div
      id="alert"
      role={ariaRole}
      className={`alert alert--${type}`}
      aria-atomic="true"
    >
      <div className="alert__content">
        {title && <h3 className="alert__headline">{title}</h3>}
        {message}
        {onClick && (
          <button
            type="button"
            className="alert__close"
            aria-label={closeTag}
            onClick={onClick}
          >
            <span className="fa fa-times" aria-hidden="true" />
          </button>
        )}
      </div>
    </div>
  )
}

export default Alert
