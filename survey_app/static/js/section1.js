window.onload = () => {
	const respondantPositionField = document.getElementById('respondant_position');
	const respondantPositionOtherContainer = document.getElementById('respondant_position_other_container');

	if (respondantPositionField.value == 'Otro')
		respondantPositionOtherContainer.hidden = false;

	respondantPositionField.onchange = () => {
		if (respondantPositionField.value == 'Otro')
			respondantPositionOtherContainer.hidden = false;
		else
			respondantPositionOtherContainer.hidden = true;
	}
}

function respondantPosition(selector) {
	const container = document.getElementById('respondant_position_container');
	const respondantPosition = document.getElementById('respondant_position');
	if (selector.value == 'Otro') {
		respondantPosition.value = '';
		container.hidden = false;
	}
	else {
		container.hidden = true;
		respondantPosition.value = selector.value;
	}
}