let placeSearch;
let autocomplete;
const componentForm = {
	country: {id:'country',type:'long_name'},
	administrative_area_level_1: {id:'admin_div_1',type:'short_name'},
	administrative_area_level_2: {id:'admin_div_2',type:'long_name'},
	route: {id:'street',type:'long_name'},
	street_number: {id:'street_number',type:'short_name'}
};

function initAutocomplete() {
	// Create the autocomplete object, restricting the search predictions to
	// geographical location types.
	autocomplete = new google.maps.places.Autocomplete(
		document.getElementById('address'),
		{ types: ['geocode'] }
	);
	// Avoid paying for data that you don't need by restricting the set of
	// place fields that are returned to just the address components.
	autocomplete.setFields(['address_component']);
	// When the user selects an address from the drop-down, populate the
	// address fields in the form.
	autocomplete.addListener('place_changed', fillInAddress);
}

function fillInAddress() {
	// Get the place details from the autocomplete object.
	const place = autocomplete.getPlace();

	for (const component in componentForm) {
		document.getElementById(componentForm[component].id).value = '';
		document.getElementById(componentForm[component].id).disabled = false;
	}

	// Get each component of the address from the place details,
	// and then fill-in the corresponding field on the form.
	for (const component of place.address_components) {
		console.log(component)
		const addressType = component.types[0];

		if (componentForm[addressType]) {
			const val = component[componentForm[addressType].type];
			document.getElementById(componentForm[addressType].id).value = val;
		}

		// Country code
		if (component.types[0] == 'country') {
			document.getElementById('country_code').value = (component['short_name']);
		}
	}
}

// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition((position) => {
			const geolocation = {
				lat: position.coords.latitude,
				lng: position.coords.longitude,
			};
			const circle = new google.maps.Circle({
				center: geolocation,
				radius: position.coords.accuracy,
			});
			autocomplete.setBounds(circle.getBounds());
		});
	}
}