window.onload = () => {
	const localFieldEntries = document.getElementById('local_products_entries');
	const exteriorFieldEntries = document.getElementById('exterior_products_entries');
	const localProducts = document.getElementsByClassName('local-product');
	const exteriorProducts = document.getElementsByClassName('exterior-product');
	const exportsContainer = document.getElementById('exports_container');
	const exportsCheck = document.getElementById('exports_check');
	const salesVolumeSpan = document.getElementById('sales_volume_span');
	const salesVolumeCurrency = document.getElementById('sales_volume_currency');
	const units = {'unidades':'unitario', 'm³':'metros cúbicos', 'L':'litros', 'kg':'kilogramos'}

	if (!localFieldEntries.value)
		localFieldEntries.value = '1';
	if (!exteriorFieldEntries.value || exteriorFieldEntries.value == 0)
		exteriorFieldEntries.value = '1';
	if (exportsCheck.checked)
		exportsContainer.hidden = false;
	else
		exportsContainer.hidden = true;
		
	if(!salesVolumeCurrency.value)
		salesVolumeCurrency.value = 'USD $'
	salesVolumeSpan.innerText = salesVolumeCurrency.value


	exportsCheck.onclick = () => {
		if (exportsCheck.checked)
			exportsContainer.hidden = false;
		else
			exportsContainer.hidden = true;
	}

	const changeUnitOnload = (unitField, unitSpan) => {
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
	}

	for (let i=0; i<7; i++) {
		const unitField = document.getElementById(`local_product_unit-${i}`);
		const unitSpan = document.getElementById(`local_product_unit_span-${i}`);
		changeUnitOnload(unitField, unitSpan);
	}
	
	for (let i=0; i<7; i++) {
		const unitField = document.getElementById(`exterior_product_unit-${i}`);
		const unitSpan = document.getElementById(`exterior_product_unit_span-${i}`);
		changeUnitOnload(unitField, unitSpan);
	}

	renderFields(localFieldEntries, localProducts);
	renderFields(exteriorFieldEntries, exteriorProducts);
	clearFieldsValidation(localFieldEntries, localProducts);
	clearFieldsValidation(exteriorFieldEntries, exteriorProducts);
}

function clearFieldsValidation(fieldEntries, products) {
	for (let i = fieldEntries.value; i < 7; i++) {
		for (element of products[i].getElementsByClassName('is-invalid'))
			element.classList.remove('is-invalid');
		for (element of products[i].getElementsByClassName('is-invalid'))
			element.classList.remove('is-invalid');
	}
}

function productsAddField(type) {
	const fieldEntries = document.getElementById(`${type}_products_entries`);
	if (fieldEntries.value >= 7) return false;
	const products = document.getElementsByClassName(`${type}-product`);

	fieldEntries.value = parseInt(fieldEntries.value) + 1;
	renderFields(fieldEntries, products)
}

function productsRemoveField(type) {
	const fieldEntries = document.getElementById(`${type}_products_entries`);
	if (fieldEntries.value == 1) return false;
	const products = document.getElementsByClassName(`${type}-product`);

	fieldEntries.value = parseInt(fieldEntries.value) - 1;
	renderFields(fieldEntries, products)
}

function renderFields(fieldEntries, products) {
	clearFieldsValidation(fieldEntries, products);
	let n = fieldEntries.value;

	if (n == 7) fieldEntries.previousElementSibling.hidden = true;
	else fieldEntries.previousElementSibling.hidden = false;

	for (let i = 0; i < 7; i++) {
		if (i == n-1 && i != 0) {
			products[i].querySelector('button.btn-close').disabled = false;
		} else {
			products[i].querySelector('button.btn-close').disabled = true;
		}
		if (i < n) {
			products[i].hidden = false;
		} else {
			products[i].hidden = true;
		}
	}
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