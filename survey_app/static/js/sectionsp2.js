window.onload = () => {

	const toggle = (check, container) => {
		if (check.checked) {
			container.disabled = false;
		} else {
			container.disabled = true;
		}
	};

	const CCameraFrontal = document.getElementById('c_camara_frontal');
	const CCameraFrontalN = document.getElementById('c_camara_frontal_n');
	const CCameraFrontalVol = document.getElementById('c_camara_frontal_vol');
	toggle(CCameraFrontal, CCameraFrontalN);
	toggle(CCameraFrontal, CCameraFrontalVol);
	CCameraFrontal.onclick = () => {
		toggle(CCameraFrontal, CCameraFrontalN);
		toggle(CCameraFrontal, CCameraFrontalVol);
	}

	const CCameraDoubleTunnel = document.getElementById('c_camara_doble_tunel');
	const CCameraDoubleTunnelN = document.getElementById('c_camara_doble_tunel_n');
	const CCameraDoubleTunnelVol = document.getElementById('c_camara_doble_tunel_vol');
	toggle(CCameraDoubleTunnel, CCameraDoubleTunnelN);
	toggle(CCameraDoubleTunnel, CCameraDoubleTunnelVol);
	CCameraDoubleTunnel.onclick = () => {
		toggle(CCameraDoubleTunnel, CCameraDoubleTunnelN);
		toggle(CCameraDoubleTunnel, CCameraDoubleTunnelVol);
	}

	const CCameraTunnel = document.getElementById('c_camara_tunel');
	const CCameraTunnelN = document.getElementById('c_camara_tunel_n');
	const CCameraTunnelVol = document.getElementById('c_camara_tunel_vol');
	toggle(CCameraTunnel, CCameraTunnelN);
	toggle(CCameraTunnel, CCameraTunnelVol);
	CCameraTunnel.onclick = () => {
		toggle(CCameraTunnel, CCameraTunnelN);
		toggle(CCameraTunnel, CCameraTunnelVol);
	}
}