class Reservation {
	constructor(enabled, posX, posY, width, height, pilot, typeVol){
	    this.enabled = enabled;
	    this.posX = posX;
		this.posY = posY;
	    this.width = width;
	    this.height = height;
	    this.pilot = pilot;
	    this.typeVol = typeVol;
	 };
    show() {
		context.lineWidth=0.5;
        context.fillStyle = "rgba(255, 165, 0, .5)";
        context.fillRect(this.posX, this.posY, this.width, this.height);
        context.fillStyle = "black";
        context.strokeStyle = "black";
        context.strokeRect(this.posX, this.posY, this.width, this.height);
        context.font = "12" + "px Ubuntu";
        context.fillText(this.pilot, this.posX+5, this.posY+10);
        context.fillText(this.typeVol, this.posX+5, this.posY+25);
    };
    /*onClick(e){
		var rect = canvas.getBoundingClientRect();
		pos.x = e.clientX - rect.left;
		pos.y = e.clientY - rect.top;
		alert(pos.x)
	};*/
}

var pos = {x:0, y:0};
console.log(pos);

function mainReservation(hInit, hEnd, date, pilot, vol){
	//Matrice [Année, Mois, Jour]
	let dateArray = date.split('-')
	
	if (test_resaInWeek(dateArray) === true){
		//Calcul des HH:MM en MM
		let hInitMn = time2minutes(hInit)
		let hEndMn = time2minutes(hEnd)
		test_resaInWeek(dateArray)
		//Position du boutton
		let pos_resa = time2pos(hInitMn, hEndMn, dateArray)
		//Création du boutton
		let button = new Reservation(true, pos_resa[0], pos_resa[1], pos_resa[2], pos_resa[3], pilot, vol);
		//alert(pos_resa)
		//document.addEventListener("click", button.onClick)
		//document.getElementById(button).onclick = button.onClick
		button.show();	
	}
		
}

function time2minutes(time){
	timeArray = time.split(":")
	return (timeArray[0])*60 + (timeArray[1])*1
}

function time2pos(start, end, resa_date){
	let pos = new Array(4)
	//Jour, mois, année du premier jour de la semaine affichée
	let firstDayWeek = dateAddDays(nbWeek*7,today)
	//Jour de la réservation
	let resa_day = resa_date[2];
	
	for(let i = 0; i < 7; i++){
		dayWeek = dateAddDays(i,firstDayWeek)
		if(resa_day - dayWeek.getDate() === 0 ){
			nbDays = i;
		}
	}
	pos[0] = 50 + nbDays * l_cell//posX
	pos[1] = 70 + (start - h_init * 60) * pxMinute //posY
	pos[2] = l_cell //width
	pos[3] = (end - start) * pxMinute
	return pos
}

function test_resaInWeek(resa_date){
	//Jour, mois, année de la réservation
	let resa_day = resa_date[2]
	let resa_month = resa_date[1]
	let resa_year = resa_date[0]
	//Jour, mois, année du premier jour de la semaine affichée
	firstDayWeek = dateAddDays(nbWeek*7,today)

	result = false
	for (let i = 0; i < 7; i++){
		dayWeek = dateAddDays(i,firstDayWeek)
		if (resa_year - (dayWeek.getFullYear()) === 0 && resa_month - (dayWeek.getMonth() + 1) === 0 && resa_day - dayWeek.getDate() === 0){
			result = true
		}
	}
	return result	
}