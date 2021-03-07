// SECTION 1
// Triggered on direction change
function handleCountryChange(countryCode) {
	let countryData;
	fetch(`https://restcountries.eu/rest/v2/alpha/${countryCode}`)
		.then(res => res.json())
		.then(data => handleCountryData(data))
		.catch(err => console.log("Error:", err));
}

// Change all currencies
function handleCountryData(data) {
	const spans = document.getElementsByClassName('currency-span');
	const dropdowns = document.getElementsByClassName('currency-dropdown');

	for (let i = 0; i < spans.length; i++) {
		const currencyCode = data.currencies[0].code;

		if (currencyCode == 'USD') {
			dropdowns[i].innerHTML = `<li><a class="dropdown-item" href="javascript:changeSpanText('USD$', '${spans[i].id}');">USD$</a></li>`;
			spans[i].innerText = 'USD$';
		} else {
			dropdowns[i].innerHTML = '';
			for (let k = 0; k < data.currencies.length; k++) {
				const currency = `${data.currencies[k].code}${data.currencies[k].symbol}`;
				dropdowns[i].innerHTML += `<li><a class="dropdown-item" href="javascript:changeSpanText('${currency}', '${spans[i].id}');">${currency}</a></li>`;
				spans[i].innerText = `${data.currencies[k].code}${data.currencies[k].symbol}`;
				console.log(currency);
			}
			dropdowns[i].innerHTML += `<li><a class="dropdown-item" href="javascript:changeSpanText('USD$', '${spans[i].id}');">USD$</a></li>`;
		}
	}

	// const salesVolume = document.getElementById('salesVolume');
	// const salesVolumeDropdown = document.getElementById('salesVolumeDropdown');
	// const currencyCode = data.currencies[0].code;

	// if (currencyCode == 'USD') {
	// 	salesVolumeDropdown.innerHTML = `<li><a class="dropdown-item" href="javascript:changeSpanText('USD$', 'salesVolume');">USD$</a></li>`;
	// 	salesVolume.innerText = 'USD$';
	// } else {
	// 	salesVolumeDropdown.innerHTML = '';
	// 	for (let i = 0; i < data.currencies.length; i++) {
	// 		const currency = `${data.currencies[i].code}${data.currencies[i].symbol}`;
	// 		salesVolumeDropdown.innerHTML += `<li><a class="dropdown-item" href="javascript:changeSpanText('${currency}', 'salesVolume');">${currency}</a></li>`;
	// 		salesVolume.innerText = `${data.currencies[i].code}${data.currencies[i].symbol}`;

	// 		console.log(currency);
	// 	}
	// 	salesVolumeDropdown.innerHTML += `<li><a class="dropdown-item" href="javascript:changeSpanText('USD$', 'salesVolume');">USD$</a></li>`
	// }
}