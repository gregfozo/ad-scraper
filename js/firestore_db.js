

// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.1.2/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.1.2/firebase-analytics.js"
import { getFirestore, collection, getDocs, orderBy, query, where } from 'https://www.gstatic.com/firebasejs/9.1.2/firebase-firestore.js';
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBR4jOOgy1WOIFLH68pX_6zsDu2ryPy_rM",
  authDomain: "ad-crawler-f2916.firebaseapp.com",
  projectId: "ad-crawler-f2916",
  storageBucket: "ad-crawler-f2916.appspot.com",
  messagingSenderId: "634136299291",
  appId: "1:634136299291:web:d52941a57d1678aba2b5be",
  measurementId: "G-JD4XBFLGKR"
};

// Initialize Firebase + database
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const db = getFirestore(app);

// Declaration for collections, getting snapshot
const gbCol = collection(db, 'gameboy');
const gbSnapshot = await getDocs(gbCol);
const segaCol = collection(db, 'gamegear');
const segaSnapshot = await getDocs(segaCol);
const gamesCol = collection(db, 'games');
const gamesSnapshot = await getDocs(gamesCol);
const neogeoCol = collection(db, 'neogeo');
const neogeoSnapshot = await getDocs(neogeoCol);
const miniCol = collection(db, 'miniconsoles');
const miniSnapshot = await getDocs(miniCol);
// Get list of Gameboys
const gbTable = document.getElementById('gb-tbody1');
async function getProducts(db, snap){


  const prodList = snap.docs.forEach(doc => {
    let trow = document.createElement('tr');
    let td1 = document.createElement('td');
    let td2 = document.createElement('td');

    trow.classList.add("trows");
    td1.innerHTML = (doc.data().name).link(doc.data().link);
    td2.innerHTML = doc.data().price;


    trow.appendChild(td1);
    trow.appendChild(td2);


    gbTable.appendChild(trow)

  })
  return prodList;

}

window.onload = getProducts(db, gbSnapshot);

//NAVBAR--------------------------------------

const gbLink = document.getElementById('gbButton');
const segaLink = document.getElementById('segaButton');
const ngLink = document.getElementById('ngButton');
const minicLink = document.getElementById('minicButton');
const gamesLink = document.getElementById('gamesButton');
const navbarCheck = document.getElementById('active');

gbLink.addEventListener('click', function(e){
  navbarCheck.checked = false;
  searchInput.value = null;
  gbTable.innerHTML = "";
  getProducts(db, gbSnapshot);
  gbthead.removeAttribute("class");
  gbthead.innerHTML = "Price(MXN) &#x25A0;"
})

segaLink.addEventListener('click', function(e){
  navbarCheck.checked = false;
  searchInput.value = null;
  gbTable.innerHTML = "";
  getProducts(db, segaSnapshot);
  gbthead.removeAttribute("class");
  gbthead.innerHTML = "Price(MXN) &#x25A0;"
})

ngLink.addEventListener('click', function(e){
  navbarCheck.checked = false;
  searchInput.value = null;
  gbTable.innerHTML = "";
  getProducts(db, neogeoSnapshot);
  gbthead.removeAttribute("class");
  gbthead.innerHTML = "Price(MXN) &#x25A0;"
})

minicLink.addEventListener('click', function(e){
  navbarCheck.checked = false;
  searchInput.value = null;
  gbTable.innerHTML = "";
  getProducts(db, miniSnapshot);
  gbthead.removeAttribute("class");
  gbthead.innerHTML = "Price(MXN) &#x25A0;"
})

gamesLink.addEventListener('click', function(e){
  navbarCheck.checked = false;
  searchInput.value = null;
  gbTable.innerHTML = "";
  getProducts(db, gamesSnapshot);
  gbthead.removeAttribute("class");
  gbthead.innerHTML = "Price(MXN) &#x25A0;"
})
//Price(MXN) &#x25A0;
