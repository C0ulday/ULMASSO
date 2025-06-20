//Fonctions pour se déplacer entre les semaines (bouttons avancer, today, reculer)
function avancer(){
	context.clearRect(0, 0, canvas.width, canvas.height);
	nbWeek += 1;
	mainCalendar();
}

function reculer(){
	context.clearRect(0, 0, canvas.width, canvas.height);
	nbWeek -= 1;
	mainCalendar();
	
}

function aujourdhui(){
	context.clearRect(0, 0, canvas.width, canvas.height);
	nbWeek = 0;
	mainCalendar();
}