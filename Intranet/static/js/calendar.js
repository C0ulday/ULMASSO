//Variables globales	
var l_table = window.innerWidth*.65, //largeur du tableau du calendrier
	h_table = window.innerHeight*.5, //hauteur du tableau du calendrier
	h_init = 6, //heure initiale (6:00)
	h_end = 22, //heure finale (22:00)
	pxMinute = h_table/((h_end-h_init-1)*60), //Nombre de pixels par minute
	l_cell = l_table/7, //largeur d'une cellule d'une heure
	today = new Date(), //Date d'aujourd'hui
	day = ["Dimanche","Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"], //Jours de la semaine
	nbWeek = 0, //nombre de semaines avant ou après aujourd'hui (0 = semaine courrante)
	month = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Décembre"], //Mois de l'année
	canvas = document.getElementById("canv"),
	context = canvas.getContext("2d");
	
function mainCalendar(){
	drawCalendar();
	if (allMyReservation){
		for (let i = 0; i < allMyReservation.length; i += 1){
			myReservation = allMyReservation[i]
			mainReservation(myReservation[0], myReservation[1], myReservation[2], myReservation[3], myReservation[4])
		}
	}
}

//Dessin du calendrier
function drawCalendar(){
	let newToday = dateAddDays(nbWeek*7,today); //Date d'aujourd'hui incrémenté de nbWeek x 7 jours
	//Mois
	drawMonth(newToday);
	//Tableau
	drawTable(newToday);
	//Initialisation des tables des jours et des dates	
	let dayWeek = new Array(7);
	let dateWeek = new Array(7);
	for (let i = 0; i < 7; i++){	
		dateWeek[i] = newToday.getDate();
		dayWeek[i] = day[newToday.getDay()];
		newToday = dateAddDays(1, newToday);
	}
	//Jours et dates
	drawDays(dayWeek, dateWeek);
    //Horaires
    drawHours();   
} 

//Fonction pour avancer d'un jour 
function dateAddDays(a, b) {
  	var d = new Date(b || new Date());
  	d.setDate(d.getDate() + a);
  	return d;
}

//Fonction pour écrire le mois
function drawMonth(jour){
	currentMonth = month[jour.getMonth()]
	context.font="22px Lucida Grande";
	context.fillText(currentMonth + " " + jour.getFullYear(), 0, 20)
}

//Fonction pour dessiner le tableau
function drawTable(jour){
	let h_cell = pxMinute * 60; //hauteur d'une cellule d'une heure
	for (let i = 0; i < 7; i++){
		context.lineWidth=0.25;
    	context.strokeStyle = 'grey';
		if ((jour.getDay() === 0) || (jour.getDay() === 6)){
			context.fillStyle = "rgb(210,210,210,0.5)"; 
			for (let j = 0; j<h_end-h_init-1; j++){ //nb lignes = nb d'heures volables
				context.fillRect(50+l_cell*i,70+h_cell*j,l_cell,h_cell);
				context.strokeRect(50+l_cell*i,70+h_cell*j,l_cell,h_cell);
			}
		}
		else {
			for (let j = 0; j<h_end-h_init-1; j++){ //nb lignes = nb d'heures volables
				context.strokeRect(50+l_cell*i,70+h_cell*j,l_cell,h_cell);
			}
		}
		jour = dateAddDays(1, jour);
	}
}

//Fonction pour écrire les jours et les dates
function drawDays(dayWeek, dateWeek){
	context.font="16px Lucida Grande";
	context.fillStyle = "black"
	for (let i = 0; i < 7; i++){ 
		jour = dayWeek[i] + " " + dateWeek[i];
		l_jour = jour.length;
    	context.fillText(jour, 50+l_cell*i+l_cell/2 - (l_jour*9/2), 60); //Centré	
    }
}

//Fonction pour écrire les heures
function drawHours(){
	let h_cell = pxMinute * 60; //hauteur d'une cellule d'une heure
	context.font="14px Lucida Grande";
    for (let j = 0; j<h_end-h_init; j++){ //nb lignes = nb d'heures volables
    	hour = h_init + j + ":00";
    	l_hour = hour.length
    	context.fillText(hour, 50 - l_hour*10, 75+(h_cell*j));	
    }	
}