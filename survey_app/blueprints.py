from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app

from .models import db, User, UserRecommendations, RecommendationsTable, ModelS1, ModelS2, ModelS2Products, ModelS3, ModelS4, ModelS5, ModelS6, ModelS7, ModelSp1, ModelSp2, ModelSp3, ModelSp4
from .forms import RegisterForm, LoginForm, FormS1, FormS2, FormS3, FormS4, FormS5, FormS6, FormS7, FormSp1, FormSp2, FormSp3, FormSp4
from .recommendations import Recommendations

import requests

bp = Blueprint('blueprints', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def index():
	return redirect(url_for('blueprints.section1'))


@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('blueprints.index'))


@bp.route('/recommendations')
def recommendations():
	if 'user_id' in session:
		user = User.query.filter_by(id=session['user_id']).first()
		rec_table = RecommendationsTable.query.all()

		results = Recommendations(user).get_recommendations()


		return render_template('recommendations.html', recommendations=results)
	else:
		return redirect(url_for('blueprints.index'))


@bp.route('/section1', methods=['GET', 'POST'])
def section1():
	Form = FormS1
	Model = ModelS1
	if request.method == 'GET':
		if 'user_id' in session:
			user = User.query.filter_by(id=session['user_id']).first()
			model = Model.query.filter_by(user=user).first()
			if model:
				form = Form(obj=model)
				form.company_id.data = user.company_id
				form.country_code.data = user.country_code
			else:
				form = Form(request.form)
		else:
			form = Form(request.form)

	if request.method == 'POST':
		form = Form(request.form)
		if form.validate():
			if 'user_id' in session:
				user = User.query.filter_by(id=session['user_id']).first()
				model = Model.query.filter_by(user=user).first()
				user.company_id = form.company_id.data
				user.country_code = form.country_code.data
			else:
				user = User(company_id=form.company_id.data, country_code=form.country_code.data, sections_completed=1)
				model = Model(user=user)
			form.populate_obj(model)
			db.session.add(model)
			db.session.commit()
			session['user_id'] = user.id
			session['country_code'] = form.country_code.data
			print(form.country_code.data)

			return redirect(url_for('blueprints.section2'))

	return render_template('section1.html', form=form, title='Información general de la empresa')


def get_currencies():
	user = User.query.filter_by(id=session['user_id']).first()
	if 'currencies' in session and session['country_code'] == session['currencies'][0]:
		return session['currencies']
	else:
		try:
			uri = 'https://restcountries.eu/rest/v2/alpha/' + user.country_code
			data = requests.get(uri).json()
			currencies = [user.country_code]
			for currency in data['currencies']:
				money = currency['code'] + ' ' + currency['symbol']
				currencies.append(money)
			if not 'USD $' in currencies:
				currencies.append('USD $')
			session['currencies'] = currencies
			return currencies
		except requests.ConnectionError:
			flash('No se pudo cargar la moneda para el país.')
			return ['US', 'USD $']


@bp.route('/section2', methods=['GET', 'POST'])
def section2():
	if not 'user_id' in session:
		return redirect(url_for('blueprints.section1'))

	Form = FormS2
	Model = ModelS2

	currencies = get_currencies()

	if request.method == 'GET':
		user = User.query.filter_by(id=session['user_id']).first()
		if user.sections_completed < 1:
			return redirect(url_for('blueprints.section1'))

		model = Model.query.filter_by(user=user).first()
		products_model = ModelS2Products.query.filter_by(user=user).first()
	
		if model:
			form = Form(obj=model)
			local_products = ModelS2Products.query.filter_by(user=user, product_type='Local').all()
			exterior_products = ModelS2Products.query.filter_by(user=user, product_type='Exterior').all()
			if local_products:
				for i in range(len(local_products)):
					form.local_product_description[i].data = local_products[i].product_description
					form.local_product_quantity[i].data = local_products[i].product_quantity
					form.local_product_unit[i].data = local_products[i].product_unit
			if exterior_products:
				# form.exports_check.data = True
				for i in range(len(exterior_products)):
					form.exterior_product_country[i].data = exterior_products[i].product_country
					form.exterior_product_description[i].data = exterior_products[i].product_description
					form.exterior_product_quantity[i].data = exterior_products[i].product_quantity
					form.exterior_product_unit[i].data = exterior_products[i].product_unit
		else:
			form = Form(request.form)

	if request.method == 'POST':
		form = Form(request.form)
		if form.validate():
			user = User.query.filter_by(id=session['user_id']).first()
			model = Model.query.filter_by(user=user).first()
			products = ModelS2Products.query.filter_by(user=user).all()

			if not model:
				model = Model(user=user)

			# update number of sections completed
			if user.sections_completed == 1:
				user.sections_completed = 2

			# delete current entries of products in db
			if products:
				for product in products:
					db.session.delete(product)
				db.session.commit()
			
			# add new local products to db
			for i in range(int(form.local_products_entries.data)):
				description = form.local_product_description[i].data
				quantity = form.local_product_quantity[i].data
				unit = form.local_product_unit[i].data
				products_query = ModelS2Products(user=user, 
					product_type='Local',
					product_description=description,
					product_quantity=quantity,
					product_unit=unit)
				db.session.add(products_query)

			# add new exterior products to db
			for i in range(int(form.exterior_products_entries.data)):
				country = form.exterior_product_country[i].data
				description = form.exterior_product_description[i].data
				quantity = form.exterior_product_quantity[i].data
				unit = form.exterior_product_unit[i].data
				products_query = ModelS2Products(user=user, 
					product_type='Exterior',
					product_country=country,
					product_description=description,
					product_quantity=quantity,
					product_unit=unit)
				db.session.add(products_query)

			form.populate_obj(model)
			db.session.add(model)
			db.session.commit()

			return redirect(url_for('blueprints.section3'))

	return render_template('section2.html', form=form, currencies=currencies[1:], title='Información sobre la oferta de la empresa')


@bp.route('/section3', methods=['GET', 'POST'])
def section3():
	if not 'user_id' in session:
		return redirect(url_for('blueprints.section1'))
		
	Form = FormS3
	Model = ModelS3

	currencies = get_currencies()

	if request.method == 'GET':
		user = User.query.filter_by(id=session['user_id']).first()
		if user.sections_completed < 2:
			return redirect(url_for('blueprints.section2'))

		model = Model.query.filter_by(user=user).first()
	
		if model:
			form = Form(obj=model)
		else:
			form = Form(request.form)

	if request.method == 'POST':
		form = Form(request.form)
		if form.validate():
			user = User.query.filter_by(id=session['user_id']).first()
			model = Model.query.filter_by(user=user).first()

			if not model:
				model = Model(user=user)

			# update number of sections completed
			if user.sections_completed == 2:
				user.sections_completed = 3

			form.populate_obj(model)
			db.session.add(model)
			db.session.commit()

			return redirect(url_for('blueprints.section4'))

	return render_template('section3.html', form=form, currencies=currencies[1:], title='Información de la producción de la empresa')


@bp.route('/section4', methods=['GET', 'POST'])
def section4():
	if not 'user_id' in session:
		return redirect(url_for('blueprints.section1'))
	
	Form = FormS4
	Model = ModelS4

	if request.method == 'GET':
		user = User.query.filter_by(id=session['user_id']).first()
		if user.sections_completed < 3:
			n = user.sections_completed + 1
			return redirect(url_for(f'blueprints.section{n}'))

		model = Model.query.filter_by(user=user).first()
	
		if model:
			form = Form(obj=model)
		else:
			form = Form(request.form)

	if request.method == 'POST':
		form = Form(request.form)
		if form.validate():
			user = User.query.filter_by(id=session['user_id']).first()
			model = Model.query.filter_by(user=user).first()

			if not model:
				model = Model(user=user)

			# update number of sections completed
			if user.sections_completed == 3:
				user.sections_completed = 4

			form.populate_obj(model)
			db.session.add(model)
			db.session.commit()

			return redirect(url_for('blueprints.section5'))

	return render_template('section4.html', form=form, title='Absorción tecnológica')


@bp.route('/section5', methods=['GET', 'POST'])
def section5():
	if not 'user_id' in session:
		return redirect(url_for('blueprints.section1'))
		
	Form = FormS5
	Model = ModelS5

	currencies = get_currencies()

	if request.method == 'GET':
		user = User.query.filter_by(id=session['user_id']).first()
		if user.sections_completed < 4:
			n = user.sections_completed + 1
			return redirect(url_for(f'blueprints.section{n}'))

		model = Model.query.filter_by(user=user).first()
	
		if model:
			form = Form(obj=model)
		else:
			form = Form(request.form)

	if request.method == 'POST':
		form = Form(request.form)
		if form.validate():
			user = User.query.filter_by(id=session['user_id']).first()
			model = Model.query.filter_by(user=user).first()

			if not model:
				model = Model(user=user)

			# update number of sections completed
			if user.sections_completed == 4:
				user.sections_completed = 5

			form.populate_obj(model)
			db.session.add(model)
			db.session.commit()

			return redirect(url_for('blueprints.section6'))

	return render_template('section5.html', form=form, currencies=currencies[1:], title='Gestión energética y medioambiental')


@bp.route('/section6', methods=['GET', 'POST'])
def section6():
	if not 'user_id' in session:
		return redirect(url_for('blueprints.section1'))

	Form = FormS6
	Model = ModelS6

	if request.method == 'GET':
		user = User.query.filter_by(id=session['user_id']).first()
		if user.sections_completed < 5:
			n = user.sections_completed + 1
			return redirect(url_for(f'blueprints.section{n}'))

		model = Model.query.filter_by(user=user).first()
	
		if model:
			form = Form(obj=model)
		else:
			form = Form(request.form)

	if request.method == 'POST':
		form = Form(request.form)
		if form.validate():
			user = User.query.filter_by(id=session['user_id']).first()
			model = Model.query.filter_by(user=user).first()

			if not model:
				model = Model(user=user)

			# update number of sections completed
			if user.sections_completed == 5:
				user.sections_completed = 6

			form.populate_obj(model)
			db.session.add(model)
			db.session.commit()

			return redirect(url_for('blueprints.section7'))

	return render_template('section6.html', form=form, title='Calificación y entrenamiento', zipped=zip(form.operative_team, form.administrative_team, form.management_team))


@bp.route('/section7', methods=['GET', 'POST'])
def section7():
	if not 'user_id' in session:
		return redirect(url_for('blueprints.section1'))

	Form = FormS7
	Model = ModelS7

	if request.method == 'GET':
		user = User.query.filter_by(id=session['user_id']).first()
		if user.sections_completed < 6:
			n = user.sections_completed + 1
			return redirect(url_for(f'blueprints.section{n}'))

		model = Model.query.filter_by(user=user).first()
	
		if model:
			form = Form(obj=model)
		else:
			form = Form(request.form)

	if request.method == 'POST':
		form = Form(request.form)
		if form.validate():
			user = User.query.filter_by(id=session['user_id']).first()
			model = Model.query.filter_by(user=user).first()

			if not model:
				model = Model(user=user)

			# update number of sections completed
			if user.sections_completed == 6:
				user.sections_completed = 7

			form.populate_obj(model)
			db.session.add(model)
			db.session.commit()

			return redirect(url_for('blueprints.recommendations'))

	return render_template('section7.html', form=form, title='Activos tecnológicos')


@bp.route('/specificsections')
def specificsections():
	if 'user_id' in session:
		user = User.query.filter_by(id=session['user_id']).first()
		if user.sections_completed < 7:
			n = user.sections_completed + 1
			return redirect(url_for(f'blueprints.section{n}'))
		
		economic_sector = ModelS1.query.filter_by(user=user).first().economic_sector
		if economic_sector == 'Alimentos y bebidas':
			return redirect(url_for('blueprints.sectionsp1'))
		return redirect(url_for('blueprints.sectionsp1'))

	else:
		return redirect(url_for('blueprints.section1'))


@bp.route('/sectionsp1', methods=['GET', 'POST'])
def sectionsp1():
	if not 'user_id' in session:
		return redirect(url_for('blueprints.section1'))

	Form = FormSp1
	Model = ModelSp1

	if request.method == 'GET':
		user = User.query.filter_by(id=session['user_id']).first()
		if user.sections_completed < 6:
			n = user.sections_completed + 1
			return redirect(url_for(f'blueprints.section{n}'))

		model = Model.query.filter_by(user=user).first()
	
		if model:
			form = Form(obj=model)
		else:
			form = Form(request.form)

	if request.method == 'POST':
		form = Form(request.form)
		if form.validate():
			user = User.query.filter_by(id=session['user_id']).first()
			model = Model.query.filter_by(user=user).first()

			if not model:
				model = Model(user=user)

			# update number of sections completed
			if user.sections_completed == 7:
				user.sections_completed = 8

			form.populate_obj(model)
			db.session.add(model)
			db.session.commit()

			return redirect(url_for('blueprints.sectionsp1'))

	return render_template('sectionsp1.html', form=form, title='Alimentos y bebidas')


@bp.route('/sectionsp2', methods=['GET', 'POST'])
def sectionsp2():
	if not 'user_id' in session:
		return redirect(url_for('blueprints.section1'))

	Form = FormSp2
	Model = ModelSp2

	if request.method == 'GET':
		user = User.query.filter_by(id=session['user_id']).first()
		if user.sections_completed < 6:
			n = user.sections_completed + 1
			return redirect(url_for(f'blueprints.section{n}'))

		model = Model.query.filter_by(user=user).first()
	
		if model:
			form = Form(obj=model)
		else:
			form = Form(request.form)

	if request.method == 'POST':
		form = Form(request.form)
		if form.validate():
			user = User.query.filter_by(id=session['user_id']).first()
			model = Model.query.filter_by(user=user).first()

			if not model:
				model = Model(user=user)

			# update number of sections completed
			if user.sections_completed == 7:
				user.sections_completed = 8

			form.populate_obj(model)
			db.session.add(model)
			db.session.commit()

			return redirect(url_for('blueprints.sectionsp1'))

	return render_template('sectionsp2.html', form=form, title='Aserraderos')