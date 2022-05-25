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

const textImageMode = '&gt; ' + django.gettext('Image mode')
const textTextMode = '&gt; ' + django.gettext('Text mode')
const textLabel = django.gettext('Switch between image and text question')

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
      switchLabel.innerHTML = textImageMode
      imgQ.style.display = 'none'
      accQ.style.display = 'initial'
      imgA.style.display = 'none'
      accA.style.display = 'initial'

      accA.innerHTML = "<input type='text' name='captcheck_selected_answer' aria-label='Type your answer here.' autocomplete='off' autofill='off'/>"
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

  let nonce = ''
  /* Loop over all the CAPTCHA containers on the page, setting up a different CAPTCHA in each */
  Array.prototype.forEach.call(document.getElementsByClassName('captcheck_container'), function (container) {
    if (container.dataset.stylenonce) {
      nonce = container.dataset.stylenonce
    }
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
            answers += "<a class='captcheck_answer_label' href='' data-prefix='" + idp + "' data-answer='" + data.answers[i] + "' tabindex='0' aria-role='button'><input id='captcheck_" + idp + '_answer_' + data.answers[i] + "' type='radio' name='captcheck_selected_answer' value='" + data.answers[i] + "' data-prefix='" + idp + "' data-answer='" + data.answers[i] + "' /><img src='" + src + "' data-prefix='" + idp + "' data-answer='" + data.answers[i] + "'/></a>"
          }
          answers += '</div>'
          const answerDiv = document.createElement('div')
          answerDiv.innerHTML = answers + "<div class='captcheck_answer_access' id='captcheck_" + idp + "_answer_access'></div>"
          /* Create question */
          const questionDiv = document.createElement('div')
          questionDiv.setAttribute('class', 'captcheck_label_message')
          questionDiv.setAttribute('id', 'captcheck_' + idp + '_label_message')
          questionDiv.innerHTML = "<span class='captcheck_question_image' id='captcheck_" + idp + "_question_image'>" + data.question_i + "</span><span class='captcheck_question_access' id='captcheck_" + idp + "_question_access'>" + data.question_a + "</span><a href='' class='captcheck_alt_question_button' data-prefix='" + idp + "' id='captcheck_" + idp + "_alt_question_button' aria-role='button' aria-label='" + textLabel + "' tabindex='0'>" + textTextMode + '</a>'

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

  /* Add custom styles */
  const styles = document.createElement('style')
  if (nonce !== '') {
    styles.setAttribute('nonce', nonce)
  }
  /* Remove newlines/comments from captcheck.css and put it here */
  styles.innerHTML = '.captcheck_box{font-family:Ubuntu,Arial,sans-serif;color:black;border:1px solid #e0e0e0;border-radius:3px;display:inline-block;padding:3px;margin:5px 2px 5px 1px;background-color:#f5f5f5;text-decoration:none}.captcheck_label_message,.captcheck_label_message b{color:black;font-family:Ubuntu,Roboto,Arial,sans-serif}.captcheck_answer_label{border:0}.captcheck_answer_label>input{visibility:hidden;position:absolute}.captcheck_answer_label>input+img{cursor:pointer;border:2px solid transparent;border-radius:3px;min-width:32px;width:18%;max-width:64px}.captcheck_answer_label>input:checked+img{cursor:pointer;border:2px solid #424242;border-radius:3px}.captcheck_error_message{color:red}.captcheck_question_image{display:initial}.captcheck_question_access{display:none}.captcheck_alt_question_button{float:right;font-size:80%;cursor:pointer;color:inherit;text-decoration:inherit;border:0}.captcheck_answer_images{display:initial}.captcheck_answer_access{display:none}'
  document.body.appendChild(styles)
}
