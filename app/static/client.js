

var el = x => document.getElementById(x);

function showPicker(inputId) { el('file-input').click(); }

function showPicked(input) {    //  takes a file as input (image file ! )
    el('upload-label').innerHTML = input.files[0].name;
    var reader = new FileReader();
    reader.onload = function (e) {
        el('image-picked').src = e.target.result;
        el('image-picked').className = '';
    }
    reader.readAsDataURL(input.files[0]);
}

function analyze() {  // on click of analze btn --> function is triggered
    var uploadFiles = el('file-input').files;
    if (uploadFiles.length != 1){
		alert('Please select 1 file to analyze!');
		return;
	
	}
    el('analyze-button').innerHTML = 'Analyzing...';
	console.log("analyyzeee");
    var xhr = new XMLHttpRequest();
   // var loc = window.location;
	
    //xhr.open('POST', '${loc.protocol}//${loc.hostname}:${loc.port}/analyze', true); // go to " /analyze "
	//console.log(loc);
	xhr.open("POST", 'http://127.0.0.1:8080/analyze', true);

    xhr.onerror = function() {
      alert (xhr.responseText);
      return;
    };

    xhr.onload = function(e) {
        console.log(this.readyState);
        if (this.readyState === 4) {
            var response = e.target.responseText;
      			console.log(response);
 
        el('analyze-button').innerHTML = 'Analyze';
        }
    }

	xhr.onreadystatechange = function() {//Call a function when the state changes.
		if(xhr.readyState == 4 && xhr.status == 200) {
			alert("aaaaaa");
		}
	}
	//xhr.send("foo=bar&lorem=ipsum");
      var fileData = new FormData();
      fileData.append('file', uploadFiles[0]);
      xhr.send(fileData);
}



//classes = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']



function analyzed() {  // on click of analze btn --> function is triggered
    var xhr = new XMLHttpRequest();
	xhr.open("POST", 'http://127.0.0.1:8080/analyze', true);

	//Send the proper header information along with the request
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

	xhr.onreadystatechange = function() { // Call a function when the state changes.
		if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
			// Request finished. Do processing here. 
			console.log(readyState)
		}
	}
	xhr.send("foo=bar&lorem=ipsum");
}