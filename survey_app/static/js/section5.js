window.onload = () => {
	const energySourcesField = document.getElementById('energy_sources');
	const energySourcesList = document.getElementById('energy_sources_list');
	const energyCostsSpan = document.getElementById('energy_costs_span');
	const energyCostsCurrency = document.getElementById('energy_costs_currency');
	const waterCostsSpan = document.getElementById('water_costs_span');
	const waterCostsCurrency = document.getElementById('water_costs_currency');
	const unitField = document.getElementById('water_consumption_unit');
	const unitSpan = document.getElementById('water_consumption_span');
	const units = {'m³':'metros cúbicos', 'L':'litros', 'gal':'galones'};

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

	if (energySourcesField.value) {
		let energy = energySourcesField.value.split(',');
		for (let i = 0; i < 6; i++) {
			console.log(energySourcesList.children[i].lastElementChild.lastElementChild)
			energySourcesList.children[i].lastElementChild.lastElementChild.innerText = energy[i];
		}
	}

	const energyList = new Sortable(energySourcesList, {
		handle: '.handle',
		animation: 150,
		ghostClass: 'blue-background-class',
		onEnd: function (event) {
			let energySources = []
			for (child of event.to.children) {
				energySources.push(child.lastElementChild.innerText)
			}
			energySourcesField.value = energySources.join(',');
		}
	});

	if(!energyCostsCurrency.value) energyCostsCurrency.value = 'USD $'
	energyCostsSpan.innerText = energyCostsCurrency.value
	if(!waterCostsCurrency.value) waterCostsCurrency.value = 'USD $'
	waterCostsSpan.innerText = waterCostsCurrency.value
}

function changeCurrency(currency, spanId, hiddenId) {
	const hiddenField = document.getElementById(hiddenId);
	const span = document.getElementById(spanId);

	hiddenField.value = currency;
	span.innerText = currency;
	return false;
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