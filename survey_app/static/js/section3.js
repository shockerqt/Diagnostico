window.onload = () => {
	const recentInvestmentsYesRadio = document.getElementById('recent_investments-0');
	const recentInvestmentsNoRadio = document.getElementById('recent_investments-1');
	const recentInvestmentsAmountCont = document.getElementById('recent_investments_amount_cont');
	const unitField = document.getElementById('production_area_unit');
	const unitSpan = document.getElementById('production_area_span');
	const units = {'m²':'metros cuadrados', 'ft²':'pies cuadrados', 'ha': 'hectáreas'};
	const recentInvestmentsAmountSpan = document.getElementById('recent_investments_amount_span');
	const recentInvestmentsAmountCurrency = document.getElementById('recent_investments_amount_currency');

	let inUnits = false;
	for (const [key, value] of Object.entries(units)) {
		if (value == unitField.value) {
			unitSpan.innerText = key;
			unitField.hidden = true;
			unitSpan.hidden = false;
			inUnits = true;
		}
	}
	if (!inUnits) {
		unitSpan.hidden = true;
		unitField.hidden = false;
	}

	if (recentInvestmentsYesRadio.checked)
		recentInvestmentsAmountCont.hidden = false;
	else
		recentInvestmentsAmountCont.hidden = true;

	if(!recentInvestmentsAmountCurrency.value)
		recentInvestmentsAmountCurrency.value = 'USD $'
	recentInvestmentsAmountSpan.innerText = recentInvestmentsAmountCurrency.value

	recentInvestmentsYesRadio.onclick = () => {
		if (recentInvestmentsYesRadio.checked)
			recentInvestmentsAmountCont.hidden = false;
	}
	recentInvestmentsNoRadio.onclick = () => {
		if (recentInvestmentsNoRadio.checked)
			recentInvestmentsAmountCont.hidden = true;
	}
}

function changeUnit(unit, spanId, unitId) {
	const unitField = document.getElementById(unitId);
	const unitSpan = document.getElementById(spanId);

	if (unit == 'otro') {
		unitSpan.hidden = true;
		unitField.hidden = false;
		unitField.value = '';
		return false;
	}

	unitField.value = unit[1];
	unitSpan.innerText = unit[0];
	unitSpan.hidden = false;
	unitField.hidden = true;
	return false;
}

function changeCurrency(currency, spanId, hiddenId) {
	const hiddenField = document.getElementById(hiddenId);
	const span = document.getElementById(spanId);

	hiddenField.value = currency;
	span.innerText = currency;
	return false;
}