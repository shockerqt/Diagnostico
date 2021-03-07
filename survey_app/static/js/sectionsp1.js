window.onload = () => {

	const toggle = (check, container) => {
		if (check.checked) {
			container.hidden = false;
		} else {
			container.hidden = true;
		}
	};

	const toggleChecks = (noCheck, checks) => {
		if (noCheck.checked) {
			for (const check of checks) {
				check.checkbox.disabled = true;
				check.checkbox.checked = false;
				toggle(check.checkbox, check.container);
			}
		} else {
			for (const check of checks) {
				check.checkbox.disabled = false;
			}
		}
	}

	// Software for sales toggle
	const softwareForSales = document.getElementById('software_for_sales');
	const softwareForSalesContainer = document.getElementById('software_for_sales_container');
	toggle(softwareForSales, softwareForSalesContainer);
	softwareForSales.onclick = () => toggle(softwareForSales, softwareForSalesContainer);

	// Software for production toggle
	const softwareForProduction = document.getElementById('software_for_production');
	const softwareForProductionContainer = document.getElementById('software_for_production_container');
	toggle(softwareForProduction, softwareForProductionContainer);
	softwareForProduction.onclick = () => toggle(softwareForProduction, softwareForProductionContainer);

	// Authority cert date toggle
	const AuthorityCert = document.getElementById('authority_cert');
	const AuthorityCertContainer = document.getElementById('authority_cert_container');
	toggle(AuthorityCert, AuthorityCertContainer);
	AuthorityCert.onclick = () => toggle(AuthorityCert, AuthorityCertContainer);

	// GMP cert date toggle
	const GmpCert = document.getElementById('gmp_cert');
	const GmpCertContainer = document.getElementById('gmp_cert_container');
	toggle(GmpCert, GmpCertContainer);
	GmpCert.onclick = () => toggle(GmpCert, GmpCertContainer);

	// HACCP cert date toggle
	const HaccpCert = document.getElementById('haccp_cert');
	const HaccpCertContainer = document.getElementById('haccp_cert_container');
	toggle(HaccpCert, HaccpCertContainer);
	HaccpCert.onclick = () => toggle(HaccpCert, HaccpCertContainer);

	// FSSC22000 cert date toggle
	const Fssc22000Cert = document.getElementById('fssc22000_cert');
	const Fssc22000CertContainer = document.getElementById('fssc22000_cert_container');
	toggle(Fssc22000Cert, Fssc22000CertContainer);
	Fssc22000Cert.onclick = () => toggle(Fssc22000Cert, Fssc22000CertContainer);

	// GLOBAL GAP cert date toggle
	const GlobalGapCert = document.getElementById('global_gap_cert');
	const GlobalGapCertContainer = document.getElementById('global_gap_cert_container');
	toggle(GlobalGapCert, GlobalGapCertContainer);
	GlobalGapCert.onclick = () => toggle(GlobalGapCert, GlobalGapCertContainer);

	// No software
	const notSoftwareButNeeded = document.getElementById('not_software_but_needed');
	const notSoftwareNeeded = document.getElementById('not_software_needed');
	const softwareChecks = [
		{ checkbox:softwareForSales, container:softwareForSalesContainer },
		{ checkbox:softwareForProduction, container:softwareForProductionContainer }
	];
	toggleChecks(notSoftwareButNeeded, softwareChecks);
	notSoftwareButNeeded.onclick = () => {
		toggleChecks(notSoftwareButNeeded, softwareChecks);
		if (notSoftwareButNeeded.checked) {
			notSoftwareNeeded.checked = false;
		}
	};
	toggleChecks(notSoftwareNeeded, softwareChecks);
	notSoftwareNeeded.onclick = () => {
		toggleChecks(notSoftwareNeeded, softwareChecks);
		if (notSoftwareNeeded.checked) {
			notSoftwareButNeeded.checked = false;
		}
	};

	// No cert
	const noCert = document.getElementById('no_cert');
	const certChecks = [
		{ checkbox:AuthorityCert, container:AuthorityCertContainer },
		{ checkbox:GmpCert, container:GmpCertContainer },
		{ checkbox:HaccpCert, container:HaccpCertContainer },
		{ checkbox:Fssc22000Cert, container:Fssc22000CertContainer },
		{ checkbox:GlobalGapCert, container:GlobalGapCertContainer }
	];
	toggleChecks(noCert, certChecks);
	noCert.onclick = () => toggleChecks(noCert, certChecks);

};