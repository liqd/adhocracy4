import React, { useState, useEffect } from 'react'
import django from 'django'

const translated = {
  ariaLabelImage: django.gettext('Click for image-based question'),
  ariaLabelText: django.gettext('Click for text-based question'),
  imageMode: '> ' + django.gettext('Image mode'),
  textMode: '> ' + django.gettext('Text mode'),
  notArobot: django.gettext('I am not a robot'),
  helpText: django.gettext(
    'Solve the math problem and click on the correct result. <strong>If you are having difficulty please contact us by {}email{}.</strong>'
  ),
  error: django.gettext('There was a problem loading the CAPTCHA.')
}

const CaptCheck = ({ apiUrl, name, onChange, refresh }) => {
  const [answer, setAnswer] = useState('')
  const [captcha, setCaptcha] = useState(null)
  const [error, setError] = useState('')
  const [isImageMode, setIsImageMode] = useState(true)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchCaptcha = async () => {
      const fetchUrl = apiUrl + '?action=new'
      try {
        const response = await fetch(fetchUrl)
        const data = await response.json()
        setCaptcha(data)
        setLoading(false)
      } catch (error) {
        setError('Error loading captcha')
      }
    }
    setLoading(true)
    fetchCaptcha()
  }, [apiUrl, refresh])

  function createHelptext () {
    const [, pre, email, post] = translated.helpText.match(/(.*){}(.*){}(.*)/)
    return pre + '<a href="mailto:help@adhocracy.plus">' + email + '</a>' + post
  }

  const isSelectKey = (e) => {
    return e.key === 'Enter' ||
        e.which === 13 ||
        e.keyCode === 13 ||
        e.key === ' ' ||
        e.which === 32 ||
        e.keyCode === 32
  }

  const chooseAnswer = (e, ans, keyPress = false) => {
    if (keyPress && !isSelectKey(e)) {
      return
    }
    e.preventDefault()
    const combinedAnswer = ans + ':' + captcha.session
    setAnswer(ans)
    onChange(combinedAnswer)
  }

  const switchMode = (e, keyPress = false) => {
    if (keyPress && !isSelectKey(e)) {
      return
    }
    e.preventDefault()
    setAnswer('')
    setIsImageMode((isImageMode) => !isImageMode)
  }

  if (error) {
    return <span className="captcheck_error_message">{translated.error}</span>
  }

  if (loading) {
    return <p>Loading CAPTCHA...</p>
  }

  return (
    <>
      <div>
        <label htmlFor={name}>
          {translated.notArobot}
          <span role="presentation" title="This field is required">
            *
          </span>
        </label>
        <p
          className="form-hint"
          id={'hint_' + name}
          dangerouslySetInnerHTML={{ __html: createHelptext() }}
        />
        <input
          id={name}
          type="hidden"
          name={name}
          value={answer + ':' + captcha.session}
        />
      </div>

      <div className="captcheck_box">
        <div
          id={'captcheck' + captcha.id_prefix + '_label_message'}
          className="captcheck_label_message"
        >
          {isImageMode
            ? (
              <label
                className="captcheck_question_image"
                id={'captcheck_' + captcha.id_prefix + '_question_image'}
              >
                {captcha.question_i + ' = ?'}
              </label>
              )
            : (
              <label
                className="captcheck_question_access react_captcha"
                id={'captcheck_' + captcha.id_prefix + '_question_access'}
              >
                {captcha.question_a + ' = ?'}
              </label>
              )}
          {/* eslint-disable-next-line */}
          <a
            onClick={switchMode}
            onKeyPress={(e) => (switchMode(e, true))}
            href=""
            className="captcheck_alt_question_button"
            id={'captcheck_' + captcha.id_prefix + '_alt_question_button'}
            role="button"
            tabIndex="0"
            aria-label={
              isImageMode ? translated.ariaLabelText : translated.ariaLabelImage
            }
          >
            {isImageMode ? translated.textMode : translated.imageMode}
          </a>
        </div>

        <div>
          {isImageMode
            ? (
              <div
                className="captcheck_answer_images"
                id={'captcheck_' + captcha.id_prefix + '_answer_images'}
              >
                {captcha.answers.map((ans, index) => (
                  // eslint-disable-next-line jsx-a11y/anchor-is-valid
                  <a
                    key={index}
                    className="captcheck_answer_label"
                    onClick={(e) => chooseAnswer(e, ans)}
                    onKeyPress={(e) => chooseAnswer(e, ans, true)}
                    href=""
                    tabIndex="0"
                    role="button"
                  >
                    <input
                      id={'captcheck_' + captcha.id_prefix + '_answer_'}
                      aria-labelledby={
                      'captcheck_' + captcha.id_prefix + '_question_image'
                    }
                      type="radio"
                      name="captcheck_selected_answer"
                      value={ans}
                      checked={answer === ans}
                      onChange={() => console.log('click')}
                    />
                    {/* eslint-disable-next-line */}
                  <img
                    src={
                      apiUrl + '?action=img&s=' + captcha.session + '&c=' + ans
                    }
                  />
                  </a>
                ))}
              </div>
              )
            : (
              <div
                className="captcheck_answer_access react_captcha"
                id={'captcheck_' + captcha.id_prefix + '_answer_access'}
              >
                <input
                  id={
                  'captcheck_' + captcha.id_prefix + '_question_access-answer'
                  }
                  type="text"
                  name="captcheck_selected_answer"
                  aria-label="Type your answer here."
                  autoComplete="off"
                  onInput={(e) => chooseAnswer(e, e.target.value, false)}
                />
              </div>
              )}
        </div>

        <span>
          <input
            type="hidden"
            name="captcheck_session_code"
            value={captcha.session}
          />
        </span>
      </div>
    </>
  )
}

export default CaptCheck
