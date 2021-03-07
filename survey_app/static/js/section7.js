window.onload = () => {
	const checkbox1 = document.getElementById('surveillance_activities-0');
	const checkbox2 = document.getElementById('surveillance_activities-1');
	const cont1 = document.getElementById('surveillance_activities_specification_container');
	const cont2 = document.getElementById('surveillance_activities_frequency_container');

	if (checkbox1.checked) {
		cont1.hidden = false;
		cont2.hidden = false;
	}

	checkbox1.onclick = () => {
		if (checkbox1.checked) {
			cont1.hidden = false;
			cont2.hidden = false;
		}
	}

	checkbox2.onclick = () => {
		if (checkbox2.checked) {
			cont1.hidden = true;
			cont2.hidden = true;
		}
	}
}