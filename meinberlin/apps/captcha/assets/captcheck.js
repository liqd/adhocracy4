/* based on https://source.netsyms.com/Netsyms/Captcheck/src/branch/master/captcheck.js */
/* Copyright (C) 2017-2019 Netsyms Technologies.
/* Copyright (C) 2020 Liquid Democracy e.V.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 the Software, and to permit persons to whom the Software is furnished to do so,
 subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
NETSYMS TECHNOLOGIES BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name and other identifying marks of
Netsyms Technologies shall not be used in advertising or otherwise to promote
the sale, use or other dealings in this Software without prior written
authorization from Netsyms Technologies.
*/

/* global django */
const ariaLabelImage = django.gettext('Click for image-based question')
const ariaLabelText = django.gettext('Click for text-based question')
const textImageMode = '&gt; ' + django.gettext('Image mode')
const textTextMode = '&gt; ' + django.gettext('Text mode')

window.onload = function () {
  function chooseAnswer (idp, ans, session, combinedAnswerId) {
    const inputField = document.getElementById(combinedAnswerId)
    inputField.value = ans + ':' + session

    const box = document.getElementById('captcheck_' + idp + '_answer_' + ans)
    if (box) {
      box.checked = true
    }
  }

  function clearAnswer (idp, combinedAnswerId) {
    const inputField = document.getElementById(combinedAnswerId)
    inputField.value = ''

    const imgA = document.getElementById('captcheck_' + idp + '_answer_images')
    imgA.childNodes.forEach(e => {
      e.firstElementChild.checked = false
    })
  }

  function switchMode (idp, session, combinedAnswerId) {
    const switchLabel = document.getElementById('captcheck_' + idp + '_alt_question_button')
    const imgQ = document.getElementById('captcheck_' + idp + '_question_image')
    const accQ = document.getElementById('captcheck_' + idp + '_question_access')
    const imgA = document.getElementById('captcheck_' + idp + '_answer_images')
    const accA = document.getElementById('captcheck_' + idp + '_answer_access')

    clearAnswer(idp, combinedAnswerId)

    if (switchLabel.innerHTML === textTextMode) {
      switchLabel.setAttribute('aria-label', ariaLabelImage)
      switchLabel.innerHTML = textImageMode
      imgQ.style.display = 'none'
      accQ.style.display = 'initial'
      imgA.style.display = 'none'
      accA.style.display = 'initial'

      accA.innerHTML = "<input id='captcheck_" + idp + "_question_access-answer' type='text' name='captcheck_selected_answer' aria-label='Type your answer here.' autocomplete='off' autofill='off'/>"
      accA.firstElementChild.addEventListener('input', function (ev) {
        ev.preventDefault()
        chooseAnswer(idp, this.value, session, combinedAnswerId)
      })
    } else {
      switchLabel.innerHTML = textTextMode
      imgQ.style.display = 'initial'
      accQ.style.display = 'none'
      imgA.style.display = 'initial'
      accA.style.display = 'none'
      accA.innerHTML = ''
    }
  }

  /* Loop over all the CAPTCHA containers on the page, setting up a different CAPTCHA in each */
  Array.prototype.forEach.call(document.getElementsByClassName('captcheck_container'), function (container) {
    const apiUrl = container.getAttribute('data-api_url')
    const combinedAnswerId = container.getAttribute('combined_answer_id')
    const xhr = new XMLHttpRequest()
    xhr.open('GET', apiUrl + '?action=new', true)
    xhr.onreadystatechange = function () {
      if (this.readyState === 4) {
        const status = this.status
        const json = this.responseText
        /* Prevent rare bug where two CAPTCHAs appear in one container */
        if (container.innerHTML.trim() !== '') {
          return
        }
        /* Create captcha div */
        const captcha = document.createElement('div')
        captcha.setAttribute('class', 'captcheck_box')
        container.appendChild(captcha)

        if (status === 200) {
          const data = JSON.parse(json)
          // ID prefix to use for this instance
          const idp = data.id_prefix
          /* Create answer buttons */
          let answers = "<div class='captcheck_answer_images' id='captcheck_" + idp + "_answer_images'>"
          for (let i = 0, len = data.answers.length; i < len; i++) {
            const src = apiUrl + '?action=img&s=' + data.session + '&c=' + data.answers[i]
            answers +=
            "<a class='captcheck_answer_label' href='' data-prefix='" + idp + "' data-answer='" + data.answers[i] + "' tabindex='0' aria-role='button'>" +
            "<input id='captcheck_" + idp + '_answer_' + data.answers[i] + "' aria-labelledby='captcheck_" + idp + "_question_image' type='radio' name='captcheck_selected_answer' value='" + data.answers[i] + "' data-prefix='" + idp + "' data-answer='" + data.answers[i] + "' />" +
            "<img src='" + src + "' data-prefix='" + idp + "' data-answer='" + data.answers[i] + "'/></a>"
          }
          answers += '</div>'
          const answerDiv = document.createElement('div')
          answerDiv.innerHTML = answers + "<div class='captcheck_answer_access' id='captcheck_" + idp + "_answer_access'></div>"
          /* Create question */
          const questionDiv = document.createElement('div')
          questionDiv.setAttribute('class', 'captcheck_label_message')
          questionDiv.setAttribute('id', 'captcheck_' + idp + '_label_message')
          questionDiv.innerHTML =
          "<label class='captcheck_question_image' id='captcheck_" + idp + "_question_image' tabindex='0'>" + data.question_i + '</label>' +
          "<label class='captcheck_question_access' id='captcheck_" + idp + "_question_access' tabindex='0'>" + data.question_a + '</label>' +
          "<a href='' class='captcheck_alt_question_button' data-prefix='" + idp + "' id='captcheck_" + idp + "_alt_question_button' aria-role='button' tabindex='0' aria-label='" + ariaLabelText + "'>" + textTextMode + '</a>'

          /* Add question and answers */
          captcha.appendChild(questionDiv)
          captcha.appendChild(answerDiv)

          /* Add hidden session ID element */
          const skeyInput = document.createElement('span')
          skeyInput.innerHTML = "<input type='hidden' name='captcheck_session_code' value='" + data.session + "' />"
          captcha.appendChild(skeyInput)

          const answerButtons = document.querySelectorAll('.captcheck_answer_label[data-prefix="' + idp + '"]')
          for (let k = 0; k < answerButtons.length; k++) {
            answerButtons[k].addEventListener('click', function (ev) {
              chooseAnswer(ev.target.getAttribute('data-prefix'), ev.target.getAttribute('data-answer'), data.session, combinedAnswerId)
              ev.preventDefault()
            })
            answerButtons[k].addEventListener('keydown', function (ev) {
              if (ev.key === 'Enter' || ev.which === 13 || ev.keyCode === 13 || ev.key === ' ' || ev.which === 32 || ev.keyCode === 32) {
                chooseAnswer(ev.target.getAttribute('data-prefix'), ev.target.getAttribute('data-answer'), data.session, combinedAnswerId)
                ev.preventDefault()
              }
            })
          }
          document.querySelector('.captcheck_alt_question_button[data-prefix="' + idp + '"]').addEventListener('click', function (ev) {
            ev.preventDefault()
            switchMode(ev.target.getAttribute('data-prefix'), data.session, combinedAnswerId)
          })
          document.querySelector('.captcheck_alt_question_button[data-prefix="' + idp + '"]').addEventListener('keydown', function (ev) {
            if (ev.key === 'Enter' || ev.which === 13 || ev.keyCode === 13 || ev.key === ' ' || ev.which === 32 || ev.keyCode === 32) {
              ev.preventDefault()
              switchMode(ev.target.getAttribute('data-prefix'), data.session, combinedAnswerId)
            }
          })
        } else {
          /* Add error message */
          captcha.innerHTML = "<span class='captcheck_error_message'>There was a problem loading the CAPTCHA.</span>"
        }
      }
    }
    xhr.send()
  })
}
