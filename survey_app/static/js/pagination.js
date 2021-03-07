window.addEventListener('DOMContentLoaded', (event) => {
	console.log('DOM fully loaded and parsed');
	const title = document.getElementById('title');
	const progressBar = document.getElementById('progressBar');

	const firstSection = document.getElementById('firstSection');
	const secondSection = document.getElementById('secondSection');
	const thirdSection = document.getElementById('thirdSection');
	const fourthSection = document.getElementById('fourthSection');
	const fifthSection = document.getElementById('fifthSection');
	const sixthSection = document.getElementById('sixthSection');
	const seventhSection = document.getElementById('seventhSection');

	function hideAllSections() {
		window.scrollTo({top: 0, behavior: 'smooth'});
		firstSection.hidden = true;
		secondSection.hidden = true;
		thirdSection.hidden = true;
		fourthSection.hidden = true;
		fifthSection.hidden = true;
		sixthSection.hidden = true;
		seventhSection.hidden = true;
	}

	function showFirstSection() {
		hideAllSections();
		title.innerText = "Información general de la empresa";
		progressBar.style = "width:12.5%"
		firstSection.hidden = false;
	}

	function showSecondSection() {
		hideAllSections();
		title.innerText = "Información sobre la oferta de la empresa";
		progressBar.style = "width:25%"
		secondSection.hidden = false;
	}

	function showThirdSection() {
		hideAllSections();
		title.innerText = "Información de la producción de la empresa";
		progressBar.style = "width:37.5%"
		thirdSection.hidden = false;
	}

	function showFourthSection() {
		hideAllSections();
		title.innerText = "Absorción tecnológica";
		progressBar.style = "width:50%"
		fourthSection.hidden = false;
	}

	function showFifthSection() {
		hideAllSections();
		title.innerText = "Gestión energética y medioambiental";
		progressBar.style = "width:62.5%"
		fifthSection.hidden = false;
	}

	function showSixthSection() {
		hideAllSections();
		title.innerText = "Calificación y entrenamiento";
		progressBar.style = "width:75%"
		sixthSection.hidden = false;
	}

	function showSeventhSection() {
		hideAllSections();
		title.innerText = "Activos tecnológicos";
		progressBar.style = "width:87.5%"
		seventhSection.hidden = false;
	}

	// Next buttons
	document.getElementById('firstSectionNextButton').onclick = showSecondSection;
	document.getElementById('secondSectionNextButton').onclick = showThirdSection;
	document.getElementById('thirdSectionNextButton').onclick = showFourthSection;
	document.getElementById('fourthSectionNextButton').onclick = showFifthSection;
	document.getElementById('fifthSectionNextButton').onclick = showSixthSection;
	document.getElementById('sixthSectionNextButton').onclick = showSeventhSection;

	// Back buttons
	document.getElementById('secondSectionBackButton').onclick = showFirstSection;
	document.getElementById('thirdSectionBackButton').onclick = showSecondSection;
	document.getElementById('fourthSectionBackButton').onclick = showThirdSection;
	document.getElementById('fifthSectionBackButton').onclick = showFourthSection;
	document.getElementById('sixthSectionBackButton').onclick = showFifthSection;
	document.getElementById('seventhSectionBackButton').onclick = showSixthSection;

	showFirstSection();
});