window.addEventListener("paste", function(thePasteEvent){
    // Use thePasteEvent object here ...
    alert("You Pasted something? You called?");
}, false);

function copyText(context){
    navigator.clipboard.writeText(this.innerHTML); 
    document.getElementById('tooltipCopied').style.transition = "0.25s";
    document.getElementById('tooltipCopied').style.display = 'flex';
  }
  function addButton(){
    document.getElementById("bodyContainer").innerHTML+= "<button onhover='document.getElementById(\"btnDelete\").style.display=\"block\"; onclick=\"copyText(this)\">Blank Pasted Text</button>"
  }