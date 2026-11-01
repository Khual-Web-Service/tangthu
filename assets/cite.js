// Cite-this-page box: fills the access date with today's date and wires the Copy buttons.
(function(){var M=["January","February","March","April","May","June","July","August","September","October","November","December"],d=new Date(),m=M[d.getMonth()];
document.querySelectorAll(".acc").forEach(function(e){e.textContent=e.dataset.f==="mla"?d.getDate()+" "+(m.length>4?m.slice(0,3)+".":m)+" "+d.getFullYear():m+" "+d.getDate()+", "+d.getFullYear();});
document.querySelectorAll(".copycite").forEach(function(b){b.addEventListener("click",function(){var t=b.previousElementSibling.textContent;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){b.textContent="Copied";setTimeout(function(){b.textContent="Copy"},1500)},function(){});});});})();
