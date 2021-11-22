//Gives target=_blank to links that have no target attributes
document.addEventListener("click", function(e) {
   if (e.target.tagName == "A" &&
           !e.target.hasAttribute("target"))
   {
       e.target.setAttribute("target", "_blank");
   }
});
//Give class if descending already
let gbthead = document.getElementById("gbthead");
document.addEventListener("click", function(e){
  if(e.target.id == "gbthead" && !e.target.hasAttribute("class")){
    e.target.setAttribute("class", "descending");
    gbthead.innerHTML = "Price(MXN) &#9660;"
  } else if(e.target.id != "gbthead"){
    return;
  } else {
    e.target.removeAttribute("class");
    gbthead.innerHTML = "Price(MXN) &#9650;"
  }
})

//SORT TABLE JS-------------------------------------------------

function sortTable(){
  var table, rows, switching,i, x, y, shouldSwitch;
  table = document.getElementById("gbTable");
  switching = true;
  //Loop continues until no switching has been done
  while(switching){
    //No switching is done:
    switching = false;
    rows = table.rows;
    //Looping through all rows(except first which is header)
    for (i = 1; i < (rows.length -1); i++){
      //Default: no switch needed
      shouldSwitch = false;
      //Getting 2 elements to compare, current row vs next:
      x = rows[i].getElementsByTagName("td")[1];
      y = rows[i+1].getElementsByTagName("td")[1];
      //Check if rows should switch
      if(gbthead.hasAttribute("class") === true && Number(x.innerHTML) > Number(y.innerHTML)){
        shouldSwitch = true;
        break;
      } else if (gbthead.hasAttribute("class") === false && Number(y.innerHTML) > Number(x.innerHTML)){
        shouldSwitch = true;
        break;
      }
    }

    if (shouldSwitch){
      //If a switch has been marked, make the switch and mark that a switch has been done
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}

//SEARCH TABLE----------------------------------------------------

const searchInput = document.getElementById('search');
const rows = document.getElementsByClassName('trows');

searchInput.addEventListener('keyup', function(event) {
  const q = event.target.value.toLowerCase();
  for (i = 0; i < rows.length; i++) {
    rows[i].querySelector('td').textContent.toLowerCase().includes(q)
    ? (rows[i].style.display = "table-row")
    : (rows[i].style.display = "none");
  }
})
