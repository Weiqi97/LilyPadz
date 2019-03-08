/**
 * Get the toad data toggle option status.
 * @returns {Boolean} If toggle is no, return true and false otherwise.
 */
function getToggleStatus () {
  return $('#mode-toggle').prop('checked')
}

/**
 * Display proper toad selection button corresponding to the toggle status.
 */
function toggleToadSelection () {
  if (getToggleStatus()) {
    $('#one-toad-option').css('display', 'none')
    $('#multiple-toad-option').css('display', 'block')
  } else {
    $('#one-toad-option').css('display', 'block')
    $('#multiple-toad-option').css('display', 'none')
  }
}

/**
 * Get all front end options.
 * @returns {string} Pass the string to backend.
 */
function getOption () {
  // Get the toad selected.
  let toadSelection
  if (getToggleStatus()) {
    toadSelection = Array.prototype.join.call(
      $('#multiple-toad-selection').val(), '!'
    )
  } else {
    toadSelection = $('#one-toad-selection').val()
  }

  // Get the visualization method selected.
  const visSelection = $('#vis-selection').val()

  // Get variables selected.
  const variableSelection = $('#variable').val()

  // Get the phase selected.
  const phaseSelection = $('#phase-selection').val()

  // Return the JSON string.
  return JSON.stringify({
    variable_selection: Array.prototype.join.call(variableSelection, '!'),
    phase_selection: phaseSelection,
    toad_selection: toadSelection,
    vis_selection: visSelection
  })
}

/**
 * Use an ajax call to get the parallel coordinate.
 */
function getGraph () {
  $('#vis-holder').html('')
  $('#color-toad').html('')
  $('#spinner').css('display', 'block')

  $.ajax({
    url: '/get_graph',
    type: 'POST',
    data: getOption(),
    contentType: 'application/json; charset=utf-8'
  })
    .done(function (result) {
      // Put the result in to the proper html div.
      $('#vis-holder').html(result['plot'])
      $('#color-toad').html(
        `<div class="col-12" style="margin-top: 10px">
              <h5><em>Toads are colored in the following ways:</em></h5>
         </div><hr>` +
        result['color_toad'].map(function (data) {
          return `<div class="col-2 text-center" style="color: ${data[0]}">${data[1]}</div>`
        }).join('')
      )
    })
    .fail(
      // When ajax has error, print in the console.
      function (jqXHR, textStatus, errorThrown) {
        console.log(`textStatus: ${textStatus}`)
        console.log(`errorThrown: ${errorThrown}`)
      })
    .always(
      function () {
        $('#spinner').css('display', 'none')
      }
    )
}

/**
 * Display the instruction pop up.
 */
function displayInstruction () {
  $.confirm({
    type: 'blue',
    title: 'Instruction',
    content: 'The input file is All_Hopping_Info.csv. The variables that we' +
      ' will be utilizing from this file are ID, Hop Number, Hop Phase,' +
      ' Sight, Phase Duration (s), Mean Elb, Mean Pro/Ret, Mean Elev/Dep' +
      ' and Hop Duration. Make sure your .csv file contains these headers and ' +
      'the associated data. The ID column must contain the name of each of' +
      ' the toads being analyzed i.e. Atlas, Fortuna, Gelos, Talos, and' +
      ' Zeus. The Hop Number must contain a number that has not yet been' +
      ' used. The Hop Phase must be one of the four phases: Initiation,' +
      ' Forelimb LO, Impact Preparation and Landing. The Sight column will' +
      ' contain the values Sighted or Blind. The Phase Duration (s) column' +
      ' will contain the number of seconds of the duration of that' +
      ' particular phase. Mean Elb, Mean Pro/Ret and Mean Elev/Dep will' +
      ' respectively contain an average of the Elbow Flexion/Extension,' +
      ' Humeral Protraction/Retraction and Humeral Elevation/Depression.' +
      ' Lastly, the Hop Duration column has the number of seconds that each' +
      ' hop takes overall for each toad.',
    columnClass: 'col-10',
    buttons: {
      confirm: {
        text: 'Got it!',
        btnClass: 'btn-info'
      }
    }
  })
}

/**
 * Do the ajax call to upload file.
 */
function upload () {
  const fileName = $('input[type=file]').val().split('\\').pop()
  console.log(fileName)
  $.ajax({
    type: 'POST',
    cache: false,
    url: '/upload',
    contentType: false,
    processData: false,
    data: new FormData($('#upload')[0])
  })
    .done(function () {
      $.confirm({
        type: 'green',
        icon: 'fas fa-check-circle',
        theme: 'modern',
        title: 'File uploaded!',
        content: '',
        buttons: {
          confirm: {
            text: 'Got it!',
            btnClass: 'btn-info'
          }
        }
      })
    })
    .fail(function () {
      $.confirm({
        type: 'red',
        icon: 'fas fa-exclamation-triangle',
        theme: 'modern',
        title: 'Error!',
        content: 'Did you select file first?',
        buttons: {
          confirm: {
            text: 'Got it!',
            btnClass: 'btn-info'
          }
        }
      })
    })
}

/**
 * When page is done loading, run these functions.
 */
$(function () {
  // Save the toggle element.
  const toggle = $('#mode-toggle')
  // Set the toggle to on by default - compare toads.
  toggle.bootstrapToggle('on')
  // Bind the toggle with on change element.
  toggle.change(() => {
    toggleToadSelection()
  })

  // When click on upload button, trigger file input.
  $('#file-input').click(() => {
    $('#file-input-trigger').click()
  })

  // Perform the upload.
  $('#do-upload').click(() =>
    upload()
  )

  // Generate the graph.
  $('#get-graph').click(() => {
    getGraph()
  })

  // Instruction alert button.
  $('#instruction').click(() => {
    displayInstruction()
  })
})