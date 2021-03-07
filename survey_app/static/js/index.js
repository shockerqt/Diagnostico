function changeForm(step) {
	const login_form = document.getElementById('login_form');
	const register_form = document.getElementById('signup_form');

	if (step == 'Login') {
		register_form.hidden = true;
		login_form.hidden = false;
	}
	else if (step == 'Register') {
		register_form.hidden = false;
		login_form.hidden = true;
	}
}