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
	$("#vis-holder-one").html("")
	$("#vis-holder-two").html("")

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
 * Display the Plotly Instruction pop up.
 */
function displayPlotlyInstruction() {
	// Setup the instruction message we want to display.
	const instruction = `Upon hovering over the top right corner of the plot, you will see several
	clickable icons which will help you better understand the visualization. Looking at the icons from
	the left to the right, the first icon is a camera which allows you to download the plot to your computer
	as a png. The next icon allows you to zoom in on a certain area of the plot by dragging the cursor across
	the specific portion of data that you wish to view in greater detail. The pan icon allows you to drag the
	plot data both vertically and horizontally to view specific areas of the plot and is especially useful after
	using the zoom in or zoom out icons. In order to return to the original plot view, simply double click anywhere on
	the plot. The autoscale button zooms in on the plot in order to create an optimal view of the data but it does not
	account for the range of the axes. On the other hand, the reset axes button includes the axes range if it was previously
	determined by the user. If the axes range was not previously determined, an optimal view of all of the data in the plot
	is displayed instead. The toggle spike lines button generates a horizontal and vertical line that spans across the data
	at the point where the cursor is located. This feature allows you to identify the relationship between the different
	variables in the multivariate dataset. Click on the toggle spike lines button again to hide these lines. Lastly, the show
	closest data on hover displays the data at a single point where the cursor is located. The compare data on hover button
	shows the data for all points that share the same x-value according to the cursor's location.` 

	// Display the message with a jQuery Confirm window.
	$.confirm({
		type: "blue",
		title: "Plotly Instructions",
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
	
	//Plotly Instruction alert button.
	$("#plotly").click(() => {
		displayPlotlyInstruction()
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