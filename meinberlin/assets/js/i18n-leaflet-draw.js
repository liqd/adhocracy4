window.L.drawLocal = {
  draw: {
    toolbar: {
      actions: {
        title: 'Bereich entfernen',
        text: 'Abbrechen'
      },
      finish: {
        title: 'Bereich übernehmen',
        text: 'Übernehmen'
      },
      undo: {
        title: 'Letzten Punkt entfernen',
        text: 'Letzten Punkt entfernen'
      },
      buttons: {
        polyline: 'Draw a polyline',
        polygon: 'Einen Bereich einzeichnen',
        rectangle: 'Ein Rechteck einzeichnen',
        circle: 'Draw a circle',
        marker: 'Draw a marker',
        circlemarker: 'Draw a circlemarker'
      }
    },
    handlers: {
      circle: {
        tooltip: {
          start: 'Click and drag to draw circle.'
        },
        radius: 'Radius'
      },
      circlemarker: {
        tooltip: {
          start: 'Click map to place circle marker.'
        }
      },
      marker: {
        tooltip: {
          start: 'Click map to place marker.'
        }
      },
      polygon: {
        tooltip: {
          start: 'Klicken, um den Bereich anzufangen.',
          cont: 'Klicken, um hier einen Punkt zu setzen.',
          end: 'Den ersten Punkt anklicken, um den Bereich abzuschließen.'
        }
      },
      polyline: {
        error: '<strong>Error:</strong> shape edges cannot cross!',
        tooltip: {
          start: 'Click to start drawing line.',
          cont: 'Click to continue drawing line.',
          end: 'Click last point to finish line.'
        }
      },
      rectangle: {
        tooltip: {
          start: 'Klicken und ziehen um ein Rechteck zu zeichnen.'
        }
      },
      simpleshape: {
        tooltip: {
          end: 'Maustaste loslassen um den Bereich abzuschließen.'
        }
      }
    }
  },
  edit: {
    toolbar: {
      actions: {
        save: {
          title: 'Änderungen speichern',
          text: 'Speichern'
        },
        cancel: {
          title: 'Bearbeitung abbrechen, Änderungen verwerfen',
          text: 'Abbrechen'
        },
        clearAll: {
          title: 'Alle Ebenen entfernen',
          text: 'Alles entfernen'
        }
      },
      buttons: {
        edit: 'Ebenen bearbeiten',
        editDisabled: 'Keine Ebenen zum Bearbeiten',
        remove: 'Ebenen löschen',
        removeDisabled: 'Keine Ebenen zum Löschen'
      }
    },
    handlers: {
      edit: {
        tooltip: {
          text: 'Die Eckpunkte ziehen um den Bereich zu ändern.',
          subtext: 'Abbrechen klicken um die Änderungen zu verwerfen..'
        }
      },
      remove: {
        tooltip: {
          text: 'Einen Bereich anklicken um ihn zu entfernen.'
        }
      }
    }
  }
}
