/**
 * Get the toad data toggle option status.
 * @returns {Boolean} If toggle is no, return true and false otherwise.
 */
function getToggleStatus() {
	return $("#mode-toggle").prop("checked")
}

/**
 * Display proper toad selection button corresponding to the toggle status.
 */
function toggleToadSelection() {
	if (getToggleStatus()) {
		$("#one-toad-option").css("display", "none")
		$("#multiple-toad-option").css("display", "block")
	} else {
		$("#one-toad-option").css("display", "block")
		$("#multiple-toad-option").css("display", "none")
	}
}

/**
 * Get all front end options.
 * @returns {string} Pass the string to backend.
 */
function getOption() {
	// Get the toad selected.
	let toad
	if (getToggleStatus()) {
		toad = Array.prototype.join.call(
			$("#multiple-toad-selection").val(), "!"
		)
	} else {
		toad = $("#one-toad-selection").val()
	}

	// Get the visualization method selected.
	const visMethod = $("#vis-selection").val()

	// Get variables selected.
	const smallSeriesVar = $("#small-series-variable").val()
	const clusteringVar = $("#clustering-variable").val()
	const regressionXVar = $("#regression-x-variable").val()
	const regressionYVar = $("#regression-y-variable").val()

	// Return the JSON string.
	return JSON.stringify({
		small_series_variable: Array.prototype.join.call(smallSeriesVar, "!"),
		clustering_variable: Array.prototype.join.call(clusteringVar, "!"),
		regression_x_variable: regressionXVar,
		regression_y_variable: regressionYVar,
		toad_selection: toad,
		vis_selection: visMethod
	})
}

/**
 * Use an ajax call to get the parallel coordinate.
 */
function getGraph() {
	// Clear the boxed before rendering new element.
	$("#vis-holder").html("")
	$("#color-toad").html("")

	// Display a spinner to indicate users that element are being loaded.
	$("#spinner").css("display", "block")

	// Do an ajax call to get the graph.
	$.ajax({
		url: "/small_series",
		type: "POST",
		data: getOption(),
		contentType: "application/json; charset=utf-8"
	})
		.done(function (result) {
			// Put the result in to the proper html div.
			$("#vis-holder-one").html(result['fp_plot'])
			$("#vis-holder-two").html(result['kinematic_plot'])
		})
		.fail(
			// When ajax has error, print in the console.
			function (jqXHR, textStatus, errorThrown) {
				console.log(jqXHR.status)
				console.log(`textStatus: ${textStatus}`)
				console.log(`errorThrown: ${errorThrown}`)
			})
		.always(
			function () {
				$("#spinner").css("display", "none")
			}
		)
}

/**
 * Display the instruction pop up.
 */
function displayInstruction() {
	// Setup the instruction message we want to display.
	const instruction = `The input file is All_Hopping_Info.csv. The variables 
		that we will be utilizing from this file are ID, Hop Number, Hop Phase, 
		Sight, Phase Duration (s), Mean Elb, Mean Pro/Ret, Mean Elev/Dep and 
		Hop Duration. Make sure your .csv file contains these headers and the 
		associated data. The ID column must contain the name of each of the 
		toads being analyzed i.e. Atlas, Fortuna, Gelos, Talos, and Zeus. The 
		Hop Number must contain a number that has not yet been used. The Hop 
		Phase must be one of the four phases: Initiation, Forelimb LO, Impact 
		Preparation and Landing. The Sight column will contain the values 
		Sighted or Blind. The Phase Duration (s) column will contain the 
		number of seconds of the duration of that particular phase. Mean Elb, 
		Mean Pro/Ret and Mean Elev/Dep will respectively contain an average of 
		the Elbow Flexion/Extension, Humeral Protraction/Retraction and 
		Humeral Elevation/Depression. Lastly, the Hop Duration column has the 
		number of seconds that each hop takes overall for each toad.`

	// Display the message with a jQuery Confirm window.
	$.confirm({
		type: "blue",
		title: "Instruction",
		content: instruction,
		columnClass: "col-10",
		buttons: {
			confirm: {
				text: "Got it!",
				btnClass: "btn-info"
			}
		}
	})
}

/**
 * Do the ajax call to upload file.
 */
function upload() {
	$.ajax({
		type: "POST",
		cache: false,
		url: "/upload",
		contentType: false,
		processData: false,
		data: new FormData($("#upload")[0])
	})
		.done(function () {
			$.confirm({
				type: "green",
				icon: "fas fa-check-circle",
				theme: "modern",
				title: "File uploaded!",
				content: "",
				buttons: {
					confirm: {
						text: "Got it!",
						btnClass: "btn-info"
					}
				}
			})
		})
		.fail(function () {
			$.confirm({
				type: "red",
				icon: "fas fa-exclamation-triangle",
				theme: "modern",
				title: "Error!",
				content: "Did you select file first?",
				buttons: {
					confirm: {
						text: "Got it!",
						btnClass: "btn-info"
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
	const toggle = $("#mode-toggle")
	// Set the toggle to on by default - compare toads.
	toggle.bootstrapToggle("on")
	// Bind the toggle with on change element.
	toggle.change(() => {
		toggleToadSelection()
	})

	// When click on upload button, trigger file input.
	$("#file-input").click(() => {
		$("#file-input-trigger").click()
	})

	// Perform the upload.
	$("#do-upload").click(() =>
		upload()
	)

	// Generate the graph.
	$("#get-graph").click(() => {
		getGraph()
	})

	// Instruction alert button.
	$("#instruction").click(() => {
		displayInstruction()
	})

	$("#vis-selection").change(() => {
		const visSelection = $("#vis-selection").val()
		if (visSelection === "Small Series") {
			$("#small-series-display").css("display", "block")
			$("#clustering-display").css("display", "none")
			$("#regression-display").css("display", "none")
		} else if (visSelection === "Clustering") {
			$("#small-series-display").css("display", "none")
			$("#clustering-display").css("display", "block")
			$("#regression-display").css("display", "none")
		} else {
			$("#small-series-display").css("display", "none")
			$("#clustering-display").css("display", "none")
			$("#regression-display").css("display", "block")
		}
	})
})