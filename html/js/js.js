// Listen for paste events
window.onload = function(){
  document.getElementById("bodyContainer").onload = updatePage();
  document.addEventListener('paste', (event) => {pasteContent()});
}

function updatePage(){
  updateTimer = setInterval(function(){loadData()}, 1000);
}

function pasteContent(){
  // navigator.permissions.query({name:'clipboard-read'}).then(function(result){
  //   if(result.state=='granted'){console.log("Permission to paste allowed.")}
  //   if(result.state=='prompt'){console.log("Permission to paste prompted?")}
  //   if(result.state=='denied'){console.log("Permission to paste denied.")}
  // });
  navigator.clipboard.readText().then(text => addButton(text));
}

function copyText(context){
    //navigator.clipboard.writeText(this.innerHTML); 
    document.getElementById('tooltipCopied').style.transition = "0.25s";
    document.getElementById('tooltipCopied').style.display = 'flex';
}
function addButton(pasteTxt){
  //clipText = navigator.clipboard.readText()
  console.log("Clipboard has: " + pasteTxt);
  //htmlAdd = "<button id='pasteContent'>"+pasteTxt+"</button>"
  //document.getElementById("bodyContainer").innerHTML+= htmlAdd;
  postData(pasteTxt);
  console.log("Button created from paste event");
  //document.getElementById("bodyContainer").innerHTML+= "<button onhover='document.getElementById(\"btnDelete\").style.display=\"block\"; onclick=\"copyText(this)\">Blank Pasted Text</button>"
}

function postData(data){
  // Send content to be upated to server.
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      //on responseText => add padding before being sent over & scan for <script> content
      document.getElementById("updateContainer").innerHTML += this.responseText;
    }
    
  };
  xhttp.open("POST","/updateMainPage", true);
  //xml can't set content length header
  //xhttp.setRequestHeader("Content-Length", (new TextEncoder().encode(data)).length)
  xhttp.send(data);
}

function loadData(){
  // Load updated data from server.
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("updateContainer").innerHTML = this.responseText;
    }
  };
  //Change this request to a post to keep everything temp instead of logging
  // otherwise it will log that it's sending all the updated things to 
  xhttp.open("GET","/updateMainPage", true);
  xhttp.send();
}