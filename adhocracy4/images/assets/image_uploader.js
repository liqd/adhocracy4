function init () {
  const clearInputs = document.querySelectorAll('input[data-upload-clear]')
  const previewImages = document.querySelectorAll('img[data-upload-preview]')

  previewImages.forEach(function (previewImage) {
    previewImage = document.getElementById(previewImage.id)
    const inputId = previewImage.dataset.uploadPreview
    const clearInput = Array.from(clearInputs).filter(function (el) {
      return el.matches('[data-upload-clear="' + inputId + '"]')
    })

    document.querySelector('#' + inputId).addEventListener('change', function (e) {
      const domInput = e.target
      if (domInput.files && domInput.files[0]) {
        const file = domInput.files[0]
        const name = file.name
        const sizeInBytes = file.size
        const sizeInMB = (sizeInBytes / (1024 * 1024)).toFixed(2) // Convert bytes to MB and round to 2 decimal places
        const text = document.querySelector('#text-' + inputId)

        // Update the file name and size in the associated text input
        if (text != null) {
          text.value = name + ' - ' + sizeInMB + ' MB of 5MB'

          // Highlight in red if the size exceeds 5MB
          if (sizeInMB > 5) {
            text.style.color = 'red'
          } else {
            text.style.color = '' // Reset to default color
          }
        }

        // Add the file size to a custom data attribute on the preview image
        previewImage.dataset.fileSize = sizeInBytes

        // If supported, read the file as a URL for preview purposes
        if (window.FileReader) {
          const reader = new window.FileReader()
          reader.addEventListener('load', function (e) {
            previewImage.setAttribute('src', e.target.result)
            clearInput[0].checked = false
          })
          reader.readAsDataURL(file)
        } else {
          clearInput[0].checked = false
        }

        // Add the file size to the URL (if required for backend processing)
        const currentUrl = new URL(window.location.href)
        currentUrl.searchParams.set('file_size', sizeInBytes) // Add file_size as a query parameter
        window.history.replaceState(null, '', currentUrl.toString())
      }
    })
  })
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
