function disableContact (disable, disableTextfield) {
  document.getElementById('id_contact_email_0_0').disabled = disable
  document.getElementById('id_contact_email_0_1').disabled = disable
  document.getElementById('id_contact_email_1').disabled = disableTextfield
  document.getElementById('id_contact_phone').disabled = disable
  document.getElementById('id_contact_storage_consent').disabled = disable
}

function init () {
  const allowContact = document.getElementById('id_allow_contact')
  const accountEmail = document.getElementById('id_contact_email_0_0')
  const otherEmail = document.getElementById('id_contact_email_0_1')
  let otherEmailChecked = otherEmail.checked

  if (!accountEmail.checked & !otherEmail.checked) {
    accountEmail.checked = true
  }

  if (!allowContact.checked) {
    disableContact(true, true)
  } else if (accountEmail.checked) {
    document.getElementById('id_contact_email_1').disabled = true
  }

  allowContact.addEventListener('change', function () {
    if (this.checked) {
      disableContact(false, !otherEmailChecked)
    } else {
      disableContact(true, true)
    }
  })

  accountEmail.addEventListener('change', function () {
    if (this.checked) {
      document.getElementById('id_contact_email_1').disabled = true
      otherEmailChecked = false
    }
  })

  otherEmail.addEventListener('change', function () {
    if (this.checked) {
      document.getElementById('id_contact_email_1').disabled = false
      otherEmailChecked = true
    }
  })
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
